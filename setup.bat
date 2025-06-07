@echo off
REM Telegram Contacts Exporter Setup Script

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Setup steps:
echo 1. Copy .env.example to .env and fill in your Telegram and Google credentials.
echo 2. Download your Google credentials.json and place it in this folder.
echo 3. Create a Google Sheet named "Telegram Contacts" and share it with your service account email.
echo 4. Run python export_telegram_contacts.py to export your contacts.
echo.
pause 