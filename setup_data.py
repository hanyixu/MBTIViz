import os
import shutil
import pandas as pd

def setup_data_directory():
    """
    Creates the data directory and copies CSV files there if needed.
    This helps ensure the application can find the data files regardless of where it's run from.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define data directory path
    data_dir = os.path.join(script_dir, 'data')
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        print(f"Creating data directory at {data_dir}")
        os.makedirs(data_dir)
    
    # Check if CSV files are in the root directory and need to be moved
    root_countries = os.path.join(script_dir, 'countries.csv')
    root_types = os.path.join(script_dir, 'types.csv')
    
    data_countries = os.path.join(data_dir, 'countries.csv')
    data_types = os.path.join(data_dir, 'types.csv')
    
    # Copy countries.csv to data directory if needed
    if os.path.exists(root_countries) and not os.path.exists(data_countries):
        print(f"Copying countries.csv to data directory")
        shutil.copy(root_countries, data_countries)
    
    # Copy types.csv to data directory if needed
    if os.path.exists(root_types) and not os.path.exists(data_types):
        print(f"Copying types.csv to data directory")
        shutil.copy(root_types, data_types)
    
    # Verify data files exist
    missing_files = []
    if not os.path.exists(data_countries):
        missing_files.append('countries.csv')
    if not os.path.exists(data_types):
        missing_files.append('types.csv')
    
    if missing_files:
        print(f"Warning: Missing data files: {', '.join(missing_files)}")
        print(f"Please place these files in the {data_dir} directory")
        return False
    
    print("Data directory setup complete")
    return True

def verify_csv_structure():
    """
    Verifies that the CSV files have the expected structure.
    Returns True if verification passes, False otherwise.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    
    countries_path = os.path.join(data_dir, 'countries.csv')
    types_path = os.path.join(data_dir, 'types.csv')
    
    # Check if files exist
    if not os.path.exists(countries_path) or not os.path.exists(types_path):
        print("Cannot verify CSV structure: Files not found")
        return False
    
    # Verify countries.csv
    try:
        countries_df = pd.read_csv(countries_path)
        
        # Check required columns
        if 'Country' not in countries_df.columns:
            print("Error: 'Country' column missing from countries.csv")
            return False
        
        # Check for MBTI type columns (at least a few should exist)
        mbti_cols = [col for col in countries_df.columns if '-' in col]
        if len(mbti_cols) < 5:
            print("Warning: countries.csv may not have the expected MBTI type columns")
            print(f"Found columns: {countries_df.columns.tolist()}")
    except Exception as e:
        print(f"Error verifying countries.csv: {str(e)}")
        return False
    
    # Verify types.csv
    try:
        types_df = pd.read_csv(types_path)
        
        # Check required columns
        required_cols = ['Type', 'Description', 'Nickname']
        missing_cols = [col for col in required_cols if col not in types_df.columns]
        
        if missing_cols:
            print(f"Warning: Missing columns in types.csv: {', '.join(missing_cols)}")
            print(f"Found columns: {types_df.columns.tolist()}")
    except Exception as e:
        print(f"Error verifying types.csv: {str(e)}")
        return False
    
    print("CSV structure verification passed")
    return True

if __name__ == "__main__":
    # Run the setup when this script is executed directly
    if setup_data_directory():
        verify_csv_structure()
