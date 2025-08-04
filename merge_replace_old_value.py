import json
import os
from pathlib import Path

def merge_json_files(folder1_path, folder2_path, output_folder=None):
    """
    Merge JSON files with the same names from two folders.
    Contents from folder2 files are merged with folder1 files, overwriting values for common keys.
    
    Args:
        folder1_path (str): Path to the first folder (translations_D4)
        folder2_path (str): Path to the second folder (translation_for_D4_2)
        output_folder (str, optional): Path to output folder. If None, overwrites folder1 files.
    """
    
    folder1 = Path(folder1_path)
    folder2 = Path(folder2_path)
    
    # Check if folders exist
    if not folder1.exists():
        print(f"Error: Folder '{folder1_path}' does not exist!")
        return
    
    if not folder2.exists():
        print(f"Error: Folder '{folder2_path}' does not exist!")
        return
    
    # Create output folder if specified
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = folder1
    
    # Get all JSON files from both folders
    folder1_files = {f.name: f for f in folder1.glob("*.json")}
    folder2_files = {f.name: f for f in folder2.glob("*.json")}
    
    # Find common files
    common_files = set(folder1_files.keys()) & set(folder2_files.keys())
    
    if not common_files:
        print("No common JSON files found between the two folders.")
        return
    
    print(f"Found {len(common_files)} common JSON files to merge:")
    for filename in sorted(common_files):
        print(f"  - {filename}")
    
    # Merge each common file
    for filename in common_files:
        try:
            print(f"\nMerging {filename}...")
            
            # Read first file (old JSON)
            with open(folder1_files[filename], 'r', encoding='utf-8') as f:
                data1 = json.load(f)
            
            # Read second file (new JSON)
            with open(folder2_files[filename], 'r', encoding='utf-8') as f:
                data2 = json.load(f)
            
            # Merge the data
            merged_data = merge_json_data(data1, data2)
            
            # Write merged data to output
            output_file = output_path / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✓ Successfully merged {filename}")
            
        except json.JSONDecodeError as e:
            print(f"  ✗ Error reading JSON from {filename}: {e}")
        except Exception as e:
            print(f"  ✗ Error processing {filename}: {e}")
    
    print(f"\nMerging complete! Files saved to: {output_path}")

def merge_json_data(data1, data2):
    """
    Merge two JSON data structures by overwriting common keys with the value from data2.
    
    Args:
        data1 (dict): The first JSON data (old data).
        data2 (dict): The second JSON data (new data).
    
    Returns:
        dict: The merged data with data2 overwriting data1 for common keys.
    """
    
    if isinstance(data1, dict) and isinstance(data2, dict):
        # Merge dictionaries by overwriting common keys with data2
        merged = data1.copy()
        for key, value in data2.items():
            merged[key] = value  # Overwrite with new value
        return merged
    
    elif isinstance(data1, list) and isinstance(data2, list):
        # Concatenate lists (if they are lists)
        return data1 + data2
    
    else:
        # For other types (including if one is a list and the other is a dict), return data2
        return data2

# Example usage
if __name__ == "__main__":
    # Set your folder paths here
    folder1_path = "translations_D4"
    folder2_path = "translation_for_D4_3"
    
    # Option 1: Overwrite files in folder1
    merge_json_files(folder1_path, folder2_path)
    
    # Option 2: Save merged files to a new folder (uncomment below)
    # merge_json_files(folder1_path, folder2_path, "merged_translations")
