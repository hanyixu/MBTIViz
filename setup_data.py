import os
import shutil
import pandas as pd


def setup_data_directory():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')

    if not os.path.exists(data_dir):
        print(f"Creating data directory at {data_dir}")
        os.makedirs(data_dir)

    root_countries = os.path.join(script_dir, 'countries.csv')
    root_types = os.path.join(script_dir, 'types.csv')

    data_countries = os.path.join(data_dir, 'countries.csv')
    data_types = os.path.join(data_dir, 'types.csv')

    if os.path.exists(root_countries) and not os.path.exists(data_countries):
        print(f"Copying countries.csv to data directory")
        shutil.copy(root_countries, data_countries)

    if os.path.exists(root_types) and not os.path.exists(data_types):
        print(f"Copying types.csv to data directory")
        shutil.copy(root_types, data_types)

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')

    countries_path = os.path.join(data_dir, 'countries.csv')
    types_path = os.path.join(data_dir, 'types.csv')

    if not os.path.exists(countries_path) or not os.path.exists(types_path):
        print("Cannot verify CSV structure: Files not found")
        return False

    try:
        countries_df = pd.read_csv(countries_path)
        if 'Country' not in countries_df.columns:
            print("Error: 'Country' column missing from countries.csv")
            return False
        mbti_cols = [col for col in countries_df.columns if '-' in col]
        if len(mbti_cols) < 5:
            print("Warning: countries.csv may not have the expected MBTI type columns")
            print(f"Found columns: {countries_df.columns.tolist()}")
    except Exception as e:
        print(f"Error verifying countries.csv: {str(e)}")
        return False

    try:
        types_df = pd.read_csv(types_path)
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
    if setup_data_directory():
        verify_csv_structure()
