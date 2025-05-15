import os
import json

def generate_index_json(data_folder='data_json', output_file='data_json/index.json'):
    # List all JSON files in data_folder (ignore index.json if exists)
    files = [f for f in os.listdir(data_folder) if f.endswith('.json') and f != 'index.json']
    files.sort()  # Optional: sort alphabetically

    # Write the list to index.json
    with open(output_file, 'w') as f:
        json.dump(files, f, indent=2)

    print(f"Generated {output_file} with {len(files)} files.")

if __name__ == '__main__':
    generate_index_json()
