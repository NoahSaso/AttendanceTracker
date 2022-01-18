from dotenv import load_dotenv
import os

# load explicitly from the same directory as this file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT = os.path.join(os.path.dirname(__file__), "service_account.json")

EMAIL_RANGE = os.getenv("EMAIL_RANGE")
EMAILS_ROW_START = int(EMAIL_RANGE[1])
EMAIL_REGEX = r"^[^@+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

CODE_RANGE = os.getenv("CODE_RANGE")
# subtract the value of the letter column from the value of the start column to get the numeric position of the column
CODES_COL_START = ord(CODE_RANGE[0]) - ord("A") + 1

MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL") == "True"
MAIL_DEFAULT_SENDER_NAME = os.getenv("MAIL_DEFAULT_SENDER_NAME")
MAIL_DEFAULT_SENDER_EMAIL = os.getenv("MAIL_DEFAULT_SENDER_EMAIL")
