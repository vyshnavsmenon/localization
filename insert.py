import os
import json

# Function to convert the room key in each JSON file
def convert_pluralization(json_data):
    if "room" in json_data and isinstance(json_data["room"], list) and len(json_data["room"]) == 2:
        # Convert the "room" key to have "one" and "other" keys for pluralization
        json_data["room"] = {
            "one": json_data["room"][0],
            "other": json_data["room"][1]
        }
    return json_data

# Function to process all JSON files in a directory
def process_json_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            
            # Read the JSON file
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
            
            # Convert the pluralization for the "room" key
            updated_data = convert_pluralization(json_data)
            
            # Write the updated data back to the file
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)

# Directory containing all the JSON files (expand the ~ to the full home directory)
directory_path = os.path.expanduser("~/Desktop/localization_script/translations_D4")
process_json_files_in_directory(directory_path)
