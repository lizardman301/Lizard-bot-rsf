from googleapiclient.discovery import build # Builds the call
from googleapiclient.errors import HttpError # Catches HTTP errors
from google.oauth2 import service_account # Google Authentication
from os import path as os_path # OS-independent way of getting directory paths

def sheets(sheet_id):
    # Grab credentials
    creds = service_account.Credentials.from_service_account_file(os_path.join(os_path.dirname(__file__)) + '/credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=creds) # Build the connection to Sheets

    # Call the Sheets API
    try:
        # Look for a sheet called seeding and grab every value from A1 until the end of the table
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'Seeding'!A1:H").execute()
        values = result.get('values', [])

        # No Values raise error
        if not values:
            raise Exception("**Challonge**: **Sheets**: Seeding sheet returned nothing")

        # Lower usernames for later
        for x in range(len(values[0])):
            values[0][x] = values[0][x].lower()

        # Look for either 'name' or 'challonge' as the header
        name_index = values[0].index('name') if 'name' in values[0] else values[0].index('challonge')
        pts_index = values[0].index('points') # Column header for points should be called points
        players_to_points = {}

        # Grab the usernames and points for future processing
        for row in values[1:]:
            if len(row) >= 2:
                players_to_points.update({row[name_index]:row[pts_index]})

        return players_to_points
    except HttpError as err:
        status_code = str(err)[11:14]

        # Bad sheet ID
        if status_code == '404':
            raise Exception("**Challonge**: **Sheets**: Specified Google Sheets does not exist. Please ensure you pulled the Sheets ID properly.")
        # No access
        elif status_code == '403':
            raise Exception("**Challonge**: **Sheets**: Lizard-BOT does not have access to configured spreadsheet. Please share the spreadsheet with Lizard-BOT")
        # No sheet called Seeding
        elif status_code == '400':
            raise Exception("**Challonge**: **Sheets**: Configured spreadsheet does not contain a sheet named 'Seeding'. Please add a 'Seeding' sheet.")
        # Some other error
        else:
            raise Exception(str(err))