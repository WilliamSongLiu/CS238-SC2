import json
import csv
from pathlib import Path
import os

STATE_INFO = {"MY_UNITS:", "ENEMY_UNITS:", "MINERALS:", "GAS:"}
IN_DIR = "raw_data"
OUT_DIR = "processed_data"

# load unit costs into a dict from file
unit_costs = None
def load_unit_costs():
    global unit_costs
    with open("unit_costs.json", "r") as file:
        data = json.load(file)
    
    unit_costs = {}
    for unit in data["Unit"]:
        unit_costs[unit["name"]] = (unit["minerals"], unit["gas"])

def calc_reward(curr, prev):
    reward = (curr["minerals"] + curr["gas"]) - (prev["s"]["minerals"] + prev["s"]["gas"])

    for unit in curr["my_units"]:
        reward += curr["my_units"][unit] * (unit_costs[unit][0] + unit_costs[unit][1])
    for unit in prev["s"]["my_units"]:
        reward -= prev["s"]["my_units"][unit] * (unit_costs[unit][0] + unit_costs[unit][1])
    
    return reward

def process_file(inpath, outjson, outjsonl):
    data = []
    with open(inpath, "r") as f:
        reader = csv.reader(f, delimiter=' ')
        
        for _ in range(2): # skip headers
            next(f)

        tuple = {} # our current (s, a, r, s') tuple, currently modified to also include all actions_wanted
        state = {} # our current state s
        actions_wanted = []
        for line in reader:
            if not line: # reached "break" between updates
                tuple["s"] = state
                tuple["a"] = actions_wanted
                
                if data: # not the first tuple
                    # current s is s' for the last tuple
                    data[-1]["sp"] = state

                    # calculate reward based on change from previous state
                    prev = data[-1]
                    tuple["r"] = calc_reward(state, prev)
                else:
                    tuple["r"] = 0 # default 0 reward

                data.append(tuple)
                tuple = {}
                state = {}
                actions_wanted = []
                continue

            heading = line[0]
            if heading in STATE_INFO:
                dict_str = ''.join(line[1:])
                dict_str = dict_str.replace("\'", "\"")

                state[heading[:-1].lower()] = json.loads(dict_str)

                # Uncomment this for a "binary" representation of enemy units
                # This simply puts all the enemy units into a list, without the counts
                # Note: sets are not valid JSON objects
                # if heading == "ENEMY_UNITS:":
                #     state[heading[:-1].lower()] = list(json.loads(dict_str).keys())
            elif heading == "ACTION_WANTED:":
                actions_wanted.append(line[-1])
            else: # heading == ACTION_MADE:
                tuple["a"] = line[-1]

    with open(outjson, "w") as out:
        json.dump(data, out)

    with open(outjsonl, "w") as out:
        for object in data:
            out.write(json.dumps(object) + "\n")

def main():
    """ Main entry point of the app """

    print("Loading unit costs")
    load_unit_costs()

    # match all files with the .txt in the input directory
    pathlist = Path(IN_DIR).glob("*.txt")

    for inpath in pathlist:
        outjson = Path(os.path.join(OUT_DIR, "jsons", f"{inpath.stem}.json"))
        outjsonl = Path(os.path.join(OUT_DIR, "jsonls", f"{inpath.stem}.jsonl"))

        print(f"Processing file {inpath.name}")
        process_file(inpath, outjson, outjsonl)

        # move processed input files to finished directory
        finished_dir = os.path.join(IN_DIR, "finished", inpath.name)
        os.rename(inpath, finished_dir)

    print(f"Finished processing all files in {IN_DIR}")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()