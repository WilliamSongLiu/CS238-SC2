import os
from pathlib import Path
import json

# Directory containing finished game files
GAMES_DIR = "raw_data/finished"

# List of buildings for checking the game state
BUILDINGS = {
    "NEXUS", "ASSIMILATOR", "PYLON", "GATEWAY", "FORGE", "CYBERNETICSCORE",
    "PHOTONCANNON", "TWILIGHTCOUNCIL", "STARGATE", "ROBOTICSFACILITY",
    "TEMPLARARCHIVE", "DARKSHRINE", "FLEETBEACON", "ROBOTICSBAY"
}

def is_game_lost(units):
    """ Determine if the game is lost based on the units in the last state. """
    return len(units) == 1 and list(units.keys())[0].upper() in BUILDINGS

def process_games(directory):
    wins, losses = 0, 0

    for game_file in Path(directory).glob("*.txt"):
        with open(game_file, 'r') as file:
            lines = file.readlines()
            last_state_line = next((line for line in reversed(lines) if "MY_UNITS:" in line), None)
            if last_state_line:
                units_str = last_state_line.split(":", 1)[1].strip()
                units = json.loads(units_str.replace("'", "\""))
                if is_game_lost(units):
                    losses += 1
                else:
                    wins += 1

    return wins, losses

def main():
    wins, losses = process_games(GAMES_DIR)
    total_games = wins + losses
    win_rate = wins / total_games * 100 if total_games > 0 else 0
    print(f"Total games: {total_games}, Wins: {wins}, Losses: {losses}, Win rate: {win_rate:.2f}%")

if __name__ == "__main__":
    main()
