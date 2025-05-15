#!/bin/bash

# Navigate to repo folder
cd /home/kadambi.mridula/Documents/surveillance-data || exit

# Run NSE data script
python3 nse_surveillance_data/nse_download.py

# Run BSE data script
python3 bse_surveillance_data/bse_data_extraction.py

# Add all changed files
#!/bin/bash

# Run NSE script
python3 /home/kadambi.mridula/Documents/surveillance-data/nse_surveillance_data/nse_download.py

# Run BSE script
python3 /home/kadambi.mridula/Documents/surveillance-data/bse_surveillance_data/bse_data_extraction.py

# Commit and push changes to GitHub
cd /home/kadambi.mridula/Documents/surveillance-data
git add .
git commit -m "Automated daily import: NSE + BSE data"
git push
git add .

# Commit with a timestamp message
git commit -m "Automated data update: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to GitHub (make sure you have credentials set or use SSH)
git push origin main
#!/bin/bash

cd "$(dirname "$0")"

# Run NSE data script
python3 nse_surveillance_data/nse_download.py

# Run BSE data script
python3 bse_surveillance_data/bse_data_extraction.py

# Git commit & push
git add .
git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
chmod +x run_all.sh
chmod +x run_all.sh
^T Execute

#!/bin/bash

cd /home/yourname/Documents/surveillance-data

# Run NSE script
python3 nse_surveillance_data/nse_download.py

# Run BSE script
python3 bse_surveillance_data/bse_data_extraction.py

# Git operations
git add .
git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
