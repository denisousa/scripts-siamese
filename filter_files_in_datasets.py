import pandas as pd
import shutil
import os

def delete_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

def copy_files(file_paths, destination_folder):
    for file_path in file_paths:
        # file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_folder, file_path)
        file_path = os.path.join(source_folder, file_path)
        shutil.copy(file_path, destination_path)


# STEP 1
file_name = 'clones_only_QS_EX_UD_NEW.csv'
df = pd.read_csv(file_name)
column_file2 = df['file2'].tolist()

# STEP 2
# folder_to_delete = 'my_projects/qualitas_corpus_clean_new'
# delete_files(folder_to_delete)

# STEP 3
source_folder = 'my_projects/qualitas_corpus_clean'
destination_folder = 'my_projects/qualitas_corpus_clean_new'
copy_files(column_file2, destination_folder)
