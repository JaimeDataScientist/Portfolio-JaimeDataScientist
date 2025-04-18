import shutil
import os

def download_dataset_kaggle(destination_folder="../data",path=None):
    """
    Downloads the dataset from Kaggle using kagglehub and moves the files to the 'data' folder.

    Parameters:
        destination_folder (str): Path to the target directory where the dataset will be stored.

    Returns:
        tuple: (destination_folder, downloaded_filename)
    """
    # Ensure target folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Move files and detect CSV
    downloaded_filename = None
    for filename in os.listdir(path):
        full_file_path = os.path.join(path, filename)
        dest_path = os.path.join(destination_folder, filename)

        if os.path.isfile(full_file_path):
            shutil.copy(full_file_path, dest_path)
            if filename.endswith(".csv"):
                downloaded_filename = filename

    print(f" Dataset copied to: {destination_folder}")
    return destination_folder, downloaded_filename
