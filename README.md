# Naukri Profile Auto-Updater

This script automatically updates your Naukri.com profile at random intervals (2-12 minutes) to keep it active and visible to recruiters.

## Features
- Automated login to Naukri.com
- Random interval updates (2-12 minutes)
- Headless browser operation (runs in background)
- Detailed logging of all activities
- Secure credential management using environment variables

## Setup Instructions

1. Install Python requirements:
   ```
   pip install -r requirements.txt
   ```

2. Configure your credentials:
   - Open the `.env` file
   - Replace `your_email@example.com` with your Naukri.com email
   - Replace `your_password` with your Naukri.com password

3. Run the script:
   ```
   python naukri_profile_updater.py
   ```

## Logging
- All activities are logged in `naukri_updater.log`
- Check this file to monitor the script's operation

## Important Notes
- The script runs continuously until stopped
- Uses Chrome in headless mode (no visible browser window)
- Automatically retries on errors
- Maintains random intervals between updates to avoid detection

## Requirements
- Python 3.7+
- Chrome browser installed
- Internet connection
