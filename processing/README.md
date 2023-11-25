Please leave files and directories where they are. These scripts will likely break if you begin moving things.

For an example of how this works, please see raw_data/finished/game1_small.txt, processed_data/jsons/game1_small.json, processed_data/jsonls/game1_small.jsonl

Additional documentation can be found in the code comments.

To run multiple games:
- Make sure to change the constants at the top of this script so output files aren't overwritten!

> python run_games.py

To process:
- This script will process all files ending in ".txt" in the raw_data directory
- It will ignore all files in the finished directory
- This script outputs two files:
    - A JSON file in processed_data/jsons
        - The entire file is a properly formatted JSON object
    - A JSONL file in processed_data/jsonls
        - Each *line* is a properly formatted JSON object
        - This is so we can avoid reading the entire file into memory at once, and instead process the data line by line
> python process.py
    