import json
import os

INPUT_FOLDER = "docs/data_json"
OUTPUT_FOLDER = "docs/data_json/converted"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def convert_file(input_path, output_path, date_str):
    with open(input_path, "r") as f:
        data = json.load(f)

    formatted_date = f"20{date_str[-2:]}-{date_str[2:4]}-{date_str[0:2]}"  # DDMMYY → YYYY-MM-DD

    converted = []
    for item in data:
        converted.append({
            "SYMBOL": item.get("ScripId", ""),
            "DATE": formatted_date,
            "REG_FLAG": item.get("GSM", "0"),
            "ASM_STAGE": (
                "1" if item.get("Short_Term_Additional_Surveillance_Measure (Short Term ASM)") == "100" else "0"
            )
        })

    with open(output_path, "w") as f:
        json.dump(converted, f, indent=2)

def main():
    index_list = []
    for filename in os.listdir(INPUT_FOLDER):
        if filename.startswith("REG_IND") and filename.endswith(".json"):
            date_part = filename.replace("REG_IND", "").replace(".json", "")
            input_file = os.path.join(INPUT_FOLDER, filename)
            output_file = os.path.join(OUTPUT_FOLDER, f"IND{date_part}.json")
            convert_file(input_file, output_file, date_part)
            index_list.append(f"converted/IND{date_part}.json")

    # Write index.json listing converted filenames
    with open(os.path.join(INPUT_FOLDER, "index.json"), "w") as f:
        json.dump(index_list, f, indent=2)

    print(f"✅ Converted {len(index_list)} files. index.json updated.")

if __name__ == "__main__":
    main()
