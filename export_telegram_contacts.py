from telethon.sync import TelegramClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from telethon.tl.functions.contacts import GetContactsRequest

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_export.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

class TelegramContactExporter:
    def __init__(self):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone_number = os.getenv('TELEGRAM_PHONE')
        self.sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'Telegram Contacts')
        
        if not all([self.api_id, self.api_hash, self.phone_number]):
            raise ValueError("Missing required environment variables. Please check your .env file.")

    def setup_google_sheets(self):
        """Set up Google Sheets connection"""
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            gclient = gspread.authorize(creds)
            return gclient.open(self.sheet_name).sheet1
        except Exception as e:
            logging.error(f"Failed to setup Google Sheets: {str(e)}")
            raise

    def categorize_contact(self, first_name, last_name, username):
        """Categorize contact based on name and username"""
        text_blob = f"{first_name} {last_name} {username}".lower()
        
        # Add your categorization logic here
        categories = {
            'google': 'Google',
            'founder': 'Founder',
            'hr': 'HR',
            'developer': 'Developer',
            'manager': 'Manager',
            'designer': 'Designer'
        }
        
        for keyword, category in categories.items():
            if keyword in text_blob:
                return category
        return 'Other'

    async def export_contacts(self):
        """Main function to export contacts"""
        try:
            # Initialize Telegram client
            client = TelegramClient('contact_scraper_session', self.api_id, self.api_hash)
            
            # Get Google Sheet
            sheet = self.setup_google_sheets()
            
            # Start Telegram client
            await client.start(phone=self.phone_number)
            logging.info("Successfully connected to Telegram")
            
            # Get contacts
            contacts = await client(GetContactsRequest(hash=0))
            logging.info(f"Found {len(contacts.users)} contacts")
            
            # Clear existing data and add headers
            sheet.clear()
            headers = ['First Name', 'Last Name', 'Username', 'Phone', 'Category', 'Last Updated']
            sheet.append_row(headers)
            
            rows = []
            for user in contacts.users:
                first = user.first_name or ''
                last = user.last_name or ''
                username = user.username or ''
                phone = user.phone or ''
                category = self.categorize_contact(first, last, username)
                last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                rows.append([first, last, username, phone, category, last_updated])
            
            if rows:
                sheet.append_rows(rows)
            
            logging.info("Successfully exported all contacts to Google Sheets")
            
        except Exception as e:
            logging.error(f"Error during export: {str(e)}")
            raise
        finally:
            await client.disconnect()

async def main():
    exporter = TelegramContactExporter()
    await exporter.export_contacts()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 