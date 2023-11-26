import json
import csv
from pathlib import Path
import os

STATE_INFO = {"MY_UNITS:", "ENEMY_UNITS:", "MINERALS:", "GAS:"}
IN_DIR = "raw_data"
OUT_DIR = "processed_data"

# load unit costs into a dict from file
unit_costs = None
possible_enemy_units = None
def load_unit_costs():
    global unit_costs, possible_enemy_units
    with open("unit_costs.json", "r") as file:
        data = json.load(file)
    
    unit_costs = {}
    for unit in data["Unit"]:
        unit_costs[unit["name"].upper()] = (unit["minerals"], unit["gas"])
    
    possible_enemy_units = []
    for unit in data["Unit"]:
        if unit["race"] == "Protoss":
            possible_enemy_units.append(unit["name"].upper())

def calc_reward(curr, prev):
    reward = (curr["minerals"] + curr["gas"]) - (prev["s"]["minerals"] + prev["s"]["gas"])

    for unit in curr["my_units"]:
        unit = unit.upper()
        reward += curr["my_units"][unit] * (unit_costs[unit][0] + unit_costs[unit][1])
    for unit in prev["s"]["my_units"]:
        unit = unit.upper()
        reward -= prev["s"]["my_units"][unit] * (unit_costs[unit][0] + unit_costs[unit][1])
    
    return reward

def get_cheapest_action_wanted(actions_wanted):
    cheapest_action = None
    cheapest_action_cost = 0
    for action in actions_wanted:
        unit = action.split("_")[1].upper()
        cost = unit_costs[unit]
        if cheapest_action == None or cost < cheapest_action_cost:
            cheapest_action = action
            cheapest_action_cost = cost
    return cheapest_action

def process_file(inpath, outjson, outjsonl):
    data = []
    with open(inpath, "r") as f:
        reader = csv.reader(f, delimiter=' ')
        
        for _ in range(2): # skip headers
            next(f)

        seen_enemy_units = {unit: 0 for unit in possible_enemy_units}
        tuple = {} # our current (s, a, r, s') tuple
        state = {} # our current state s
        actions_wanted = []
        action_made = None
        for line in reader:
            if not line: # reached "break" between updates
                tuple["s"] = state

                if action_made: # if there was an action made, go with that
                    tuple["a"] = action_made
                else: # otherwise, we will most likely make the lowest cost action in the future
                    tuple["a"] = get_cheapest_action_wanted(actions_wanted)
                
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
                action_made = None
                continue

            heading = line[0]
            if heading in STATE_INFO:
                dict_str = ''.join(line[1:])
                dict_str = dict_str.replace("\'", "\"")

                state[heading[:-1].lower()] = json.loads(dict_str)

                # making unit names uppercase
                if heading == "MY_UNITS:" or heading == "ENEMY_UNITS:":
                    state[heading[:-1].lower()] = {k.upper(): v for k, v in state[heading[:-1].lower()].items()}
                
                # aggregate enemy unit observations into binary variables
                if heading == "ENEMY_UNITS:":
                    for unit in seen_enemy_units:
                        if seen_enemy_units[unit] == 0 and unit in state[heading[:-1].lower()]:
                            seen_enemy_units[unit] = 1
                    state[heading[:-1].lower()] = seen_enemy_units

                # Uncomment this for a "binary" representation of enemy units
                # This simply puts all the enemy units into a list, without the counts
                # Note: sets are not valid JSON objects
                # if heading == "ENEMY_UNITS:":
                #     state[heading[:-1].lower()] = list(json.loads(dict_str).keys())
            elif heading == "ACTION_WANTED:":
                actions_wanted.append(line[-1])
            else: # heading == ACTION_MADE:
                action_made = line[-1]

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