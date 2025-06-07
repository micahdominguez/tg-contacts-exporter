#!/bin/bash
# Telegram Contacts Exporter Setup Script

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo
cat << EOF
Setup steps:
1. Copy .env.example to .env and fill in your Telegram and Google credentials.
2. Download your Google credentials.json and place it in this folder.
3. Create a Google Sheet named "Telegram Contacts" and share it with your service account email.
4. Run python export_telegram_contacts.py to export your contacts.
EOF 