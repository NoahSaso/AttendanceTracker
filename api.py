import traceback
from flask import Flask, jsonify, request
from flask_mail import Mail, Message
import pygsheets
import re
from itertools import chain
from datetime import datetime

from config import *

app = Flask(__name__)
# config mail
app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
app.config["MAIL_USE_SSL"] = MAIL_USE_SSL
app.config["MAIL_DEFAULT_SENDER"] = (
    MAIL_DEFAULT_SENDER_NAME,
    MAIL_DEFAULT_SENDER_EMAIL,
)
mail = Mail(app)
# config google
gc = pygsheets.authorize(service_account_file=SERVICE_ACCOUNT)
sheet: pygsheets.Worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1

error_invalid_email_address = lambda: (
    jsonify(success=False, error="Invalid email address."),
    400,
)
error_invalid_code = lambda: (
    jsonify(success=False, error="Invalid code."),
    400,
)


@app.route("/track", methods=["POST"])
def track():
    """
    Logs attendance in the spreadsheet.
    """

    try:
        # Extract parameters.

        email = request.json.get("email", "").strip().lower()
        code = request.json.get("code", "").strip().lower()

        # Validate parameters.

        if not email or not re.match(EMAIL_REGEX, email):
            logger.info(f"Invalid email: {email}")
            return error_invalid_email_address()
        if not code:
            logger.info(f"Invalid code: {code}")
            return error_invalid_code()

        # Get emails and codes from spreadsheet.

        # 2d matrix with one cell per row, flattened to a 1d list
        emails = list(
            chain(
                *sheet.range(
                    EMAIL_RANGE,
                    returnas="matrix",
                )
            )
        )
        codes = sheet.range(
            CODE_RANGE,
            returnas="matrix",
        )[0]

        # Isolate position of target cell while simultaneously verifing the code, because the code indicates which column to mark. If the code doesn't exist, it is invalid.

        email_row_index = -1
        try:
            email_row_index = emails.index(email)
        except ValueError:
            pass
        if email_row_index < 0:
            logger.info(f"Invalid email: {email}")
            return error_invalid_email_address()

        code_col_index = -1
        try:
            code_col_index = codes.index(code)
        except ValueError:
            pass
        if code_col_index < 0:
            logger.info(f"Invalid code: {code}")
            return error_invalid_code()

        # Update target cell with current date/time.

        datetime_str = datetime.now().strftime("%m/%d %H:%M")
        sheet.update_value(
            # start row/col are 1-indexed already, so no need to add 1 here
            (
                EMAILS_ROW_START + email_row_index,
                CODES_COL_START + code_col_index,
            ),
            datetime_str,
        )

        # for now, disable. Google disallows less secure apps now. Need to use oauth login.
#         # Email confirmation to student.

#         msg = Message(
#             recipients=[email],
#             subject="ItPS DeCal Attendance",
#             body=f"Your attendance was logged at {datetime_str}.\nThanks for showing up!",
#         )
#         mail.send(msg)

        # Return success.

        logging.info(f"Logged attendance for {email}. Code: {code}")

        return jsonify(success=True)

    except Exception as err:
        logger.critical(f"{err}\n{traceback.format_exc()}")
        print(err)
        print(traceback.print_exc())
        return jsonify(success=False, error="An unexpected error occurred :("), 500


if __name__ == "__main__":
    app.run(debug=True)
