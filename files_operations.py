import os 

def most_recent_file(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, file) for file in files]
    most_recent = max(paths, key=os.path.getctime)
    most_recent_name = os.path.basename(most_recent)
    return most_recent_name

def delete_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file}")
            else:
                print(f"Skipped: {file} is not a file")
        except Exception as e:
            print(f"Failed to delete {file}: {e}")
