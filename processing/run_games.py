import os

NUM_GAMES = 1
OFFSET = 3 # Change this to equal how many files are in the "processed" directory
MAP = "AncientCisternAIE"
P1 = "robo"
P2 = "ai.terran.veryhard.random"
OUTSTEM = "processing/raw_data/game"

def main():
    """ Main entry point of the app """
    os.chdir("..")

    for i in range(NUM_GAMES):
        print(f"Begin")
        os.system(f"python run_custom.py -m {MAP} -p1 {P1} -p2 {P2} > {OUTSTEM}{i + OFFSET + 1}.txt")
        print(f"Finished running game {i + 1} of {NUM_GAMES}")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()