#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import zipfile
import datetime
import shutil
import glob
import pandas as pd

# Configuration
BSE_DATA_DIR = "bse_data"
DOWNLOAD_DIR = os.path.expanduser("~/Downloads")  # Default downloads folder
PROCESSED_FLAG_FILE = os.path.join(BSE_DATA_DIR, "processed_files.txt")

# Create directories
os.makedirs(BSE_DATA_DIR, exist_ok=True)

def get_date_range_for_last_week():
    """Get date range for the last week."""
    today = datetime.date.today()
    dates = []
    
    # Generate dates for the past week (7 days)
    for i in range(1, 8):
        date = today - datetime.timedelta(days=i)
        # Skip weekends (Saturday is 5, Sunday is 6)
        if date.weekday() < 5:  # Only weekdays (0-4 are Mon-Fri)
            dates.append(date)
    
    return dates

def print_manual_download_instructions(dates):
    """Print instructions for manual downloading."""
    print("\n" + "="*80)
    print("📋 MANUAL DOWNLOAD INSTRUCTIONS 📋")
    print("="*80)
    print("Please download the following files from BSE:")
    print("1. Visit https://member.bseindia.com/")
    print("2. Navigate to: EQ > COMMON > MAY-2025")
    print("3. For each date below, select the date and download the REG1_IND file:")
    
    for date in dates:
        date_str = date.strftime("%d-%b-%Y")  # Format as "08-May-2025"
        print(f"   - {date_str}")
    
    print("\nThe files will typically download as 'rename.zip'")
    print("After each download, please rename the file to include the date before downloading the next file.")
    print("Suggested naming: rename_DDMMYY.zip (e.g., rename_080525.zip for May 8, 2025)")
    print("="*80)
    print("\nAfter downloading all files, run this script again to process them.")
    print("="*80 + "\n")

def process_downloaded_files(dates):
    """Process the manually downloaded zip files."""
    processed_files = set()
    
    # Load already processed files if the flag file exists
    if os.path.exists(PROCESSED_FLAG_FILE):
        with open(PROCESSED_FLAG_FILE, 'r') as f:
            processed_files = set(line.strip() for line in f.readlines())
    
    # Search for zip files in downloads directory
    zip_files = glob.glob(os.path.join(DOWNLOAD_DIR, "rename*.zip"))
    
    if not zip_files:
        print("❌ No BSE zip files found in your Downloads folder.")
        print("   Please download the files as per the instructions and try again.")
        return
    
    print(f"🔍 Found {len(zip_files)} zip files to process...")
    
    # Process each zip file
    success_count = 0
    
    for zip_path in zip_files:
        zip_filename = os.path.basename(zip_path)
        
        # Skip if already processed
        if zip_filename in processed_files:
            print(f"⏭️  Skipping {zip_filename} (already processed)")
            continue
        
        try:
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # List all files in the zip
                file_list = zip_ref.namelist()
                
                # Look for REG1_IND files
                reg_files = [f for f in file_list if "REG1_IND" in f]
                
                if reg_files:
                    for reg_file in reg_files:
                        # Extract the file
                        zip_ref.extract(reg_file, BSE_DATA_DIR)
                        extracted_path = os.path.join(BSE_DATA_DIR, reg_file)
                        
                        # Try to parse date from the filename (format: REG1_INDDDMMYY.csv)
                        try:
                            date_part = reg_file.split('REG1_IND')[1].split('.')[0]
                            date_obj = datetime.datetime.strptime(date_part, '%d%m%y').date()
                            date_str = date_obj.strftime('%Y-%m-%d')
                            
                            # Rename with better format
                            new_filename = f"BSE_REG1_IND_{date_str}.csv"
                            new_path = os.path.join(BSE_DATA_DIR, new_filename)
                            shutil.move(extracted_path, new_path)
                            
                            print(f"✅ Processed: {new_filename}")
                            success_count += 1
                        except Exception as e:
                            print(f"⚠️  Error parsing date from {reg_file}: {e}")
                            print(f"   Keeping original filename: {reg_file}")
                else:
                    print(f"⚠️  No REG1_IND files found in {zip_filename}")
            
            # Mark as processed
            processed_files.add(zip_filename)
            with open(PROCESSED_FLAG_FILE, 'a') as f:
                f.write(f"{zip_filename}\n")
                
        except Exception as e:
            print(f"❌ Error processing {zip_filename}: {e}")
    
    print(f"\n🎯 Successfully processed {success_count} BSE report(s).")
    
    # Summary of data if files were processed
    if success_count > 0:
        print_data_summary()

def print_data_summary():
    """Print a summary of the downloaded data."""
    csv_files = glob.glob(os.path.join(BSE_DATA_DIR, "*.csv"))
    
    if not csv_files:
        return
    
    print("\n" + "="*80)
    print("📊 DATA SUMMARY 📊")
    print("="*80)
    print(f"Total files available: {len(csv_files)}")
    
    # Get date range of available data
    dates = []
    for file in csv_files:
        try:
            # Try to extract date from filename (format: BSE_REG1_IND_YYYY-MM-DD.csv)
            filename = os.path.basename(file)
            if "BSE_REG1_IND_" in filename:
                date_str = filename.split('BSE_REG1_IND_')[1].split('.')[0]
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                dates.append(date_obj)
        except:
            continue
    
    if dates:
        print(f"Date range: {min(dates)} to {max(dates)}")
    
    # Try to read one file to show sample data structure
    try:
        sample_file = csv_files[0]
        df = pd.read_csv(sample_file)
        print(f"\nSample data structure (from {os.path.basename(sample_file)}):")
        print(f"Columns: {', '.join(df.columns)}")
        print(f"Rows: {len(df)}")
    except Exception as e:
        print(f"Could not read sample data: {e}")
    
    print("="*80)

def main():
    dates = get_date_range_for_last_week()
    
    # Check if we have any files in the BSE_DATA_DIR
    existing_files = glob.glob(os.path.join(BSE_DATA_DIR, "*.csv"))
    
    if not existing_files:
        # No files yet, provide instructions
        print_manual_download_instructions(dates)
    else:
        # We have some files, process any new downloads
        process_downloaded_files(dates)

if __name__ == "__main__":
    main()


# In[7]:


python bse_data_extraction.py

