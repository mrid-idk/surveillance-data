# %%
import os
import csv
import json

# Your actual folders in repo
csv_folders = [
    "nse_data",              # NSE CSV files root folder
    "bse_data_1/csv_files"   # BSE CSV files nested folder
]

json_output_dir = "data_json"
os.makedirs(json_output_dir, exist_ok=True)

json_files = []

def csv_to_json(csv_path, json_path):
    with open(csv_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
    with open(json_path, mode='w', encoding='utf-8') as json_file:
        json.dump(rows, json_file, indent=2)
    print(f"✅ Converted {csv_path} → {json_path}")

for folder in csv_folders:
    if not os.path.exists(folder):
        print(f"Warning: CSV folder '{folder}' not found, skipping...")
        continue
    
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(root, file)
                json_file_name = file.replace(".csv", ".json")
                json_path = os.path.join(json_output_dir, json_file_name)
                csv_to_json(csv_path, json_path)
                json_files.append(json_file_name)

file_list_path = os.path.join(json_output_dir, "file_list.json")
with open(file_list_path, "w", encoding="utf-8") as f:
    json.dump(json_files, f, indent=2)

print(f"📄 Updated {file_list_path} with {len(json_files)} entries.")



