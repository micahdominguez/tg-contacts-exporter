# Telegram Contacts Exporter

Automatically export and categorize your Telegram contacts to Google Sheets.

## Features

- Direct integration with Telegram API
- Automatic contact categorization
- Google Sheets integration
- Detailed logging
- Error handling
- Environment variable configuration

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

5. Run the script:
   ```bash
   python export_telegram_contacts.py
   ```

## Customization

- Modify the `categorize_contact` method in `export_telegram_contacts.py` to change categorization logic
- Add more fields to export by modifying the headers and row data
- Adjust logging level in the script if needed

## Troubleshooting

- Check `telegram_export.log` for detailed error messages
- Ensure all environment variables are set correctly
- Verify Google Sheets API credentials and permissions
- Make sure the Google Sheet exists and is shared with the service account

## Security Notes

- Never commit your `.env` file or `credentials.json` to version control
- Keep your API credentials secure
- Regularly rotate your API credentials if possible 