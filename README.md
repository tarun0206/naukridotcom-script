# Naukri Profile Auto-Updater

An automated script that keeps your Naukri.com profile active by updating it at random intervals (2-12 minutes). This helps maintain visibility to recruiters by keeping your profile fresh in search results.

## Features
- Automated login to Naukri.com
- Headless operation (runs in background)
- Random interval updates (2-12 minutes)
- Maintains single browser session for efficiency
- Detailed logging of all activities
- Secure credential management
- Automatic error recovery
- Graceful shutdown support

## Prerequisites
- Python 3.7+
- Google Chrome browser
- Windows OS

## Installation

1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd naukri-profile-updater
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Naukri.com credentials:
   ```
   NAUKRI_EMAIL=your_email@example.com
   NAUKRI_PASSWORD=your_password
   ```

## Usage

Run the script:
```bash
python naukri_profile_updater.py
```

The script will:
- Start Chrome in headless mode
- Log in to your Naukri account
- Update your profile at random intervals (2-12 minutes)
- Keep running until stopped or an error occurs
- Log all activities to `naukri_updater.log`

To stop the script, press Ctrl+C in the terminal window.

## Logging
All activities are logged in `naukri_updater.log`. Check this file to monitor:
- Login attempts
- Profile updates
- Waiting intervals
- Any errors that occur

## Security Notes
- Never commit your `.env` file
- Keep your credentials secure
- Regularly update your password
- Monitor the log file for unauthorized access attempts

## Troubleshooting
If you encounter issues:
1. Check `naukri_updater.log` for error messages
2. Verify your credentials in `.env` file
3. Ensure Chrome is properly installed
4. Check your internet connection
5. Make sure Naukri.com is accessible

## Contributing
Feel free to fork the repository and submit pull requests for any improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This tool is for educational purposes only. Use it responsibly and in accordance with Naukri.com's terms of service.
