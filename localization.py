import pandas as pd
import json
import os
from pathlib import Path

def excel_to_json_files(excel_file_path, output_directory=None):
    """
    Convert an Excel file to multiple JSON files.
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_directory (str, optional): Directory to save JSON files. 
                                        If None, saves in same directory as Excel file
    
    The function expects:
    - First row: JSON file names (starting from column B)
    - First column: Keys for JSON objects
    - Data starts from row 2, column 2
    """
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file_path)
        
        # Get the file names from the first row (excluding the first column)
        json_file_names = df.columns[1:].tolist()  # Skip first column
        
        # Get the keys from the first column (excluding the first row which is header)
        keys = df.iloc[:, 0].tolist()  # First column values
        
        # Set output directory
        if output_directory is None:
            output_directory = Path(excel_file_path).parent
        else:
            output_directory = Path(output_directory)
            output_directory.mkdir(parents=True, exist_ok=True)
        
        print(f"Converting Excel file: {excel_file_path}")
        print(f"Output directory: {output_directory}")
        print(f"Found {len(json_file_names)} JSON files to create")
        print(f"Found {len(keys)} keys")
        
        # Create JSON files
        for i, json_file_name in enumerate(json_file_names):
            # Get the column data (excluding header row)
            column_data = df.iloc[:, i + 1].tolist()  # i+1 because we skip first column
            
            # Create dictionary with keys and values
            json_data = {}
            for j, key in enumerate(keys):
                if j < len(column_data):
                    value = column_data[j]
                    # Handle NaN values
                    if pd.isna(value):
                        json_data[str(key)] = None
                    else:
                        json_data[str(key)] = value
            
            # Clean up file name (remove any invalid characters)
            safe_filename = "".join(c for c in str(json_file_name))
            if not safe_filename.endswith('.json'):
                safe_filename += '.json'
            
            # Create full path
            json_file_path = output_directory / safe_filename
            
            # Write JSON file
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, indent=2, ensure_ascii=False)
            
            print(f"Created: {json_file_path} with {len(json_data)} key-value pairs")
        
        print(f"\nSuccessfully converted Excel file to {len(json_file_names)} JSON files!")
        
    except FileNotFoundError:
        print(f"Error: Excel file '{excel_file_path}' not found.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def preview_excel_structure(excel_file_path, num_rows=5):
    """
    Preview the structure of the Excel file to verify the format.
    
    Args:
        excel_file_path (str): Path to the Excel file
        num_rows (int): Number of rows to preview
    """
    try:
        df = pd.read_excel(excel_file_path)
        
        print("Excel file structure preview:")
        print("=" * 50)
        print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print("\nFirst few rows:")
        print(df.head(num_rows))
        
        print(f"\nColumn names (will be JSON file names):")
        for i, col in enumerate(df.columns[1:], 1):
            print(f"  {i}. {col}")
        
        print(f"\nFirst column values (will be JSON keys):")
        for i, key in enumerate(df.iloc[:min(num_rows, len(df)), 0], 1):
            print(f"  {i}. {key}")
            
    except Exception as e:
        print(f"Error previewing file: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Replace with your Excel file path
    excel_file = "D6_2.xlsx"
    
    # Optional: Preview the file structure first
    print("Previewing Excel file structure:")
    preview_excel_structure(excel_file)
    
    print("\n" + "="*50 + "\n")
    
    # Convert Excel to JSON files
    # You can specify a custom output directory or leave it None to use the same directory
    output_dir = "translation_for_D6_3"  # Set to None to use same directory as Excel file
    
    excel_to_json_files(excel_file, output_dir)
    
    # Alternative: Save in same directory as Excel file
    # excel_to_json_files(excel_file)