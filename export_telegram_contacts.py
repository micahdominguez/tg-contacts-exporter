from telethon.sync import TelegramClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User

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
            logging.info(f"Found {len(contacts.users)} contacts (added contacts)")
            
            # Clear existing data and add headers
            sheet.clear()
            headers = ['First Name', 'Last Name', 'Username', 'Phone', 'Category', 'Bio', 'Company/Project', 'Last Updated', 'Source']
            sheet.append_row(headers)
            
            rows = []
            # Export added contacts first
            for user in contacts.users:
                first = user.first_name or ''
                last = user.last_name or ''
                username = user.username or ''
                phone = user.phone or ''
                try:
                    full = await client(GetFullUserRequest(user.id))
                    bio = getattr(full.full_user, 'about', '')
                except Exception as e:
                    bio = ''
                    logging.warning(f"Could not fetch bio for user {username or phone}: {e}")
                category = self.categorize_contact(first, last, username)
                company = ''  # Leave empty for manual entry
                last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                rows.append([first, last, username, phone, category, bio, company, last_updated, 'Added Contact'])
            if rows:
                sheet.append_rows(rows)
            logging.info("Exported added contacts to Google Sheets")

            # Ask user if they want to also export messaged but not added contacts
            print("\nBy default, only your added Telegram contacts have been exported.")
            print("If you want, you can also export all users you've ever messaged (including those not in your contacts).\n")
            print("WARNING: This may take longer, is more likely to hit Telegram's rate limits, and could (in rare cases) risk your account if abused.")
            print("The script will process these in batches to minimize risk.\n")
            resp = input("Do you want to also export users you've messaged but not added as contacts? (y/n): ").strip().lower()
            if resp == 'y':
                from telethon.tl.types import PeerUser
                dialogs = await client.get_dialogs()
                messaged_users = []
                added_user_ids = {user.id for user in contacts.users}
                for dialog in dialogs:
                    entity = dialog.entity
                    if isinstance(entity, User) and not entity.bot and entity.id not in added_user_ids:
                        messaged_users.append(entity)
                logging.info(f"Found {len(messaged_users)} messaged but not added users.")
                batch_size = 50
                for i in range(0, len(messaged_users), batch_size):
                    batch = messaged_users[i:i+batch_size]
                    batch_rows = []
                    for user in batch:
                        first = user.first_name or ''
                        last = user.last_name or ''
                        username = user.username or ''
                        phone = user.phone or ''
                        try:
                            full = await client(GetFullUserRequest(user.id))
                            bio = getattr(full.full_user, 'about', '')
                        except Exception as e:
                            bio = ''
                            logging.warning(f"Could not fetch bio for user {username or phone}: {e}")
                        category = self.categorize_contact(first, last, username)
                        company = ''
                        last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        batch_rows.append([first, last, username, phone, category, bio, company, last_updated, 'Messaged Only'])
                    if batch_rows:
                        sheet.append_rows(batch_rows)
                    logging.info(f"Exported batch {i//batch_size+1} of messaged users to Google Sheets.")
                    if i + batch_size < len(messaged_users):
                        print(f"Sleeping for 60 seconds to avoid rate limits (processed {i+batch_size} of {len(messaged_users)})...")
                        await asyncio.sleep(60)
                print("All messaged users exported.")
            else:
                print("Skipped exporting messaged but not added users.")

            logging.info("Export complete.")
            
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