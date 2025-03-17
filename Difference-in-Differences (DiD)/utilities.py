import os
import pandas as pd

def retrieve_and_open_csv_files(folder_path, keyword=None):
    """
    Retrieve and open CSV files from a folder, optionally filtering by a keyword in the filename.

    Parameters:
        folder_path (str): Path to the folder containing files.
        keyword (str, optional): A string to filter filenames. Only files containing this string will be opened.

    Returns:
        list: A list of pandas DataFrames for the matching CSV files.
    """
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
    
    # Retrieve CSV files
    csv_files = [
        os.path.join(folder_path, file) 
        for file in os.listdir(folder_path) 
        if file.endswith('.csv') and (keyword is None or keyword in file)
    ]
    
    if len(csv_files) != 1:
        # Read CSV files into DataFrames
        dataframes = [pd.read_csv(file) for file in csv_files]
    else:
        dataframes = pd.read_csv(csv_files[0])

    return dataframes
