import pandas as pd
import json
import os

def convert_sheet_to_json_files(file_path, output_directory="translations"):
    """
    Convert Google Sheet with translations to individual JSON files for each language
    
    Args:
        file_path (str): Path to the Excel/CSV file from Google Sheets
        output_directory (str): Directory to save JSON files
    """
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created directory: {output_directory}")
    
    # Read the file (works with both .xlsx and .csv)
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            raise ValueError("File must be .xlsx or .csv format")
            
        print(f"Successfully loaded file: {file_path}")
        print(f"Sheet dimensions: {df.shape}")
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Get column names (language codes)
    columns = df.columns.tolist()
    key_column = columns[0]  # First column contains keys
    language_columns = columns[1:]  # Rest are language columns
    
    print(f"Key column: {key_column}")
    print(f"Language columns: {language_columns}")
    
    # Process each language column
    for lang_code in language_columns:
        if pd.isna(lang_code) or lang_code == '':
            print(f"Skipping empty column")
            continue
            
        print(f"\nProcessing language: {lang_code}")
        
        # Create JSON object for this language
        json_data = {}
        
        # Iterate through rows
        for index, row in df.iterrows():
            key = row[key_column]
            value = row[lang_code]
            
            # Skip if key or value is empty/NaN
            if pd.isna(key) or pd.isna(value) or key == '' or value == '':
                print(f"  Skipping empty row {index}: key='{key}', value='{value}'")
                continue
            
            # Clean up the value (remove extra whitespace, handle line breaks)
            cleaned_value = str(value).strip()
            json_data[str(key)] = cleaned_value
        
        # Generate filename
        filename = f"{lang_code}.json"
        filepath = os.path.join(output_directory, filename)
        
        # Write JSON file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            print(f"  ✓ Created: {filepath} ({len(json_data)} translations)")
            
        except Exception as e:
            print(f"  ✗ Error creating {filepath}: {e}")
    
    print(f"\n🎉 Translation files created in '{output_directory}' directory")

def preview_data(file_path, num_rows=5):
    """
    Preview the first few rows of your data to verify structure
    """
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        
        print("=== DATA PREVIEW ===")
        print(f"Columns: {list(df.columns)}")
        print(f"Shape: {df.shape}")
        print("\nFirst few rows:")
        print(df.head(num_rows))
        
        return df
        
    except Exception as e:
        print(f"Error previewing file: {e}")
        return None

def validate_json_files(directory="translations"):
    """
    Validate that all generated JSON files are properly formatted
    """
    print("\n=== VALIDATING JSON FILES ===")
    
    if not os.path.exists(directory):
        print(f"Directory {directory} doesn't exist")
        return
    
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    for filename in json_files:
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✓ {filename}: Valid JSON ({len(data)} keys)")
        except Exception as e:
            print(f"✗ {filename}: Invalid JSON - {e}")

# Main execution
if __name__ == "__main__":
    # Replace with your file path
    input_file = "translation.xlsx"  # or "translations.csv"
    
    print("🚀 Starting translation file conversion...")
    
    # Preview data first (optional)
    preview_data(input_file)
    
    # Convert to JSON files
    convert_sheet_to_json_files(input_file)
    
    # Validate generated files
    validate_json_files()
    
    print("\n✅ Process completed!")