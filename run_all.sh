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
