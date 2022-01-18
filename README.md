# AttendanceTracker

Flask webserver to automatically record attendance in a spreadsheet given an email address and a verification code.

## Setup

1. Create a virtual environment

   `python3 -m venv env`

2. Activate virtual environment

   `. env/bin/activate`

3. Install requirements

   `pip install -r requirements.txt`

4. Setup a [Google Cloud Platform](https://console.cloud.google.com) Project with the [Google Sheets API](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com) enabled and a corresponding Service Account.

5. Download the Service Account JSON and save it as `service_account.json` in this folder.

6. Share the Spreadsheet with the Service Account's email (`client_email` property in the JSON file)

7. Find the Spreadsheet ID in the URL

   docs.google.com/spreadsheets/d/`THIS_IS_THE_ID`/edit

8. Create a `.env` file in this folder with the necessary environment variables. Example:

   ```bash
   SPREADSHEET_ID=1-abc-123

   # column of emails
   EMAIL_RANGE=A3:A5
   # row of codes
   CODE_RANGE=B2:B6
   ```

## Example Spreadsheet

Matches `.env` example above.

| Email               | Class 1      | Class 2      | Class 3      | Class 4      | Class 5      |
| ------------------- | ------------ | ------------ | ------------ | ------------ | ------------ |
|                     | secret_code1 | secret_code2 | secret_code3 | secret_code4 | secret_code5 |
| student1@school.edu |              |              |              |              |              |
| student2@school.edu |              |              |              |              |              |
| student3@school.edu |              |              |              |              |              |
