import traceback
from flask import Flask, jsonify, request
import pygsheets
import re
from itertools import chain

from config import *

app = Flask(__name__)
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
            return error_invalid_email_address()
        if not code:
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
            return error_invalid_email_address()

        code_col_index = -1
        try:
            code_col_index = codes.index(code)
        except ValueError:
            pass
        if code_col_index < 0:
            return error_invalid_code()

        # Update target cell with "y".

        sheet.update_value(
            # start row/col are 1-indexed already, so no need to add 1 here
            (
                EMAILS_ROW_START + email_row_index,
                CODES_COL_START + code_col_index,
            ),
            "y",
        )

        # Return success.

        return jsonify(success=True)

    except Exception as err:
        print(err)
        print(traceback.print_exc())
        return jsonify(success=False, error="An unexpected error occurred :("), 500


if __name__ == "__main__":
    app.run(debug=True)
