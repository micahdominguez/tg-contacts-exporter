# Telegram Contacts Exporter

## 🐍 Install Python (Required)

If you do not already have Python 3.8 or newer installed, follow these steps:

1. Go to the official Python download page: https://www.python.org/downloads/
2. Click the yellow "Download Python" button (the latest version is recommended).
3. Run the downloaded installer.
4. **Important:** On the first screen, check the box that says "Add Python to PATH" before clicking "Install Now".
5. Complete the installation.
6. To verify Python is installed, open a terminal (Command Prompt on Windows, Terminal on Mac/Linux) and run:
   ```bash
   python --version
   ```
   You should see something like `Python 3.10.0` or higher.

Now you are ready to continue with the Quick Start below!

## 🚀 Quick Start

**Clone the repository:**
```bash
git clone https://github.com/micahdominguez/tg-contacts-exporter.git
cd tg-contacts-exporter
```

**Run the setup script:**

- **Windows:**  
  Double-click `setup.bat` or run:
  ```bash
  setup.bat
  ```

- **Mac/Linux:**  
  Open a terminal and run:
  ```bash
  bash setup.sh
  ```

**Follow the on-screen instructions:**
1. Copy `.env.example` to `.env` and fill in your Telegram and Google credentials.
2. Download your Google `credentials.json` and place it in this folder.
3. Create a Google Sheet named `Telegram Contacts` and share it with your service account email.
4. **Important:** Activate the Google Drive API for your Google Cloud project at https://console.cloud.google.com/apis/library/drive.googleapis.com

## Running the Export

1. Run the script:
   ```bash
   python export_telegram_contacts.py
   ```

2. The script will:
   - First export your added contacts (this may take several minutes due to Telegram's rate limits)
   - Then ask if you want to export users you've messaged but haven't added as contacts
   - Process messaged users in batches of 50 with 60-second pauses between batches

**Important Notes:**
- The export process may take 15-20 minutes or longer depending on your number of contacts
- Telegram's rate limits will cause the script to pause periodically (this is normal)
- You'll see progress updates in the terminal
- The script handles rate limits automatically - just let it run
- Check `telegram_export.log` for detailed progress information

## What to Expect

When running the script, you'll see:
1. Connection to Telegram
2. Number of contacts found
3. Progress updates with occasional pauses due to rate limits
4. Option to export messaged users
5. Batch processing updates if exporting messaged users
6. Final confirmation when export is complete

**Processing Times:**
- Added contacts: ~1-2 minutes per 100 contacts (including rate limit pauses)
- Messaged users: ~3-4 minutes per 50 users (including batch pauses)
- Total time depends on your number of contacts and messaged users

**Rate Limit Behavior:**
- The script will automatically pause when hitting Telegram's rate limits
- Pauses typically last 25-30 seconds
- Progress updates will show remaining time
- No action needed - just let the script continue running

The exported data includes:
- Username
- First Name
- Last Name
- Phone Number
- Bio
- Company/Project (if detected in bio)
- Category (based on bio keywords)
- Contact Type (Added/Messaged)

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get Telegram API credentials:
   - Visit https://my.telegram.org
   - Log in and go to "API Development Tools"
   - Create a new application
   - Copy your API ID and API Hash

3. Set up Google Sheets API:
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Enable Google Sheets API
   - Create Service Account credentials
   - Download credentials.json
   - Create a new Google Sheet named "Telegram Contacts"
   - Share the sheet with the service account email

4. Configure environment:
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     TELEGRAM_API_ID=your_api_id_here
     TELEGRAM_API_HASH=your_api_hash_here
     TELEGRAM_PHONE=your_phone_number_here
     GOOGLE_SHEET_NAME=Telegram Contacts
     ```

## Features

- Direct integration with Telegram API
- Automatic contact categorization
- Google Sheets integration
- Detailed logging
- Error handling
- Environment variable configuration
- Support for both added contacts and messaged users
- Automatic rate limit handling
- Batch processing for large contact lists

## Customization

- Modify the `categorize_contact` method in `export_telegram_contacts.py` to change categorization logic
- Add more fields to export by modifying the headers and row data
- Adjust logging level in the script if needed
- Modify batch size and delay times for rate limit handling

## Troubleshooting

- Check `telegram_export.log` for detailed error messages
- Ensure all environment variables are set correctly
- Verify Google Sheets API credentials and permissions
- Make sure the Google Sheet exists and is shared with the service account
- If you see rate limit messages, this is normal - the script will handle them automatically
- If the script seems stuck, check the log file for progress updates

## Security Notes

- Never commit your `.env` file or `credentials.json` to version control
- Keep your API credentials secure
- Regularly rotate your API credentials if possible
- The script uses Telegram's official API and follows their rate limits
- No data is stored locally except for the session file

## Screenshots

### Exported Telegram Contacts in Google Sheets
![Exported Google Sheet with bios](screenshots/google-sheet-example.png)
*Your contacts, including bios, exported to Google Sheets.*

### Setup Instructions in Terminal
![Setup instructions in terminal](screenshots/setup-instructions.png)
*Quick setup instructions shown in the terminal for easy onboarding.*

### .env Example File
![.env.example file](screenshots/env-example.png)
*Example .env file—fill in your own credentials as shown.*