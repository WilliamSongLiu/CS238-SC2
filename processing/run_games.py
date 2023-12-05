import os

NUM_GAMES = 500
OFFSET = 0 # Change this to equal how many games are in the "finished" directory
MAP = "AncientCisternAIE"
P1 = "explore"
P2 = "ai.protoss.hard.random"
OUTSTEM = "processing/raw_data/game"

def main():
    """ Main entry point of the app """
    os.chdir("..")

    for i in range(NUM_GAMES):
        os.system(f"python run_custom.py -m {MAP} -p1 {P1} -p2 {P2} > {OUTSTEM}{i + OFFSET + 1}.txt")
        print(f"Finished running game {i + 1} of {NUM_GAMES}")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()