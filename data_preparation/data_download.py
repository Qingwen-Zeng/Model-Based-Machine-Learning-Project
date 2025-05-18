#%%
import kagglehub

# Download latest version
path = kagglehub.dataset_download("sujaykapadnis/nfl-stadium-attendance-dataset")

#%% [markdown]
# Downloading csv

#%%
import os
import shutil

# List all files in the dataset directory
files = os.listdir(path)

# Filter for .csv files
csv_files = [file for file in files if file.endswith('.csv')]

# Specify the destination folder
destination_folder = "./original_data"
os.makedirs(destination_folder, exist_ok=True)

# Copy the .csv files to the destination folder
for csv_file in csv_files:
    shutil.copy(os.path.join(path, csv_file), destination_folder)

print(f"Downloaded CSV files: {csv_files}")