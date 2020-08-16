from googleapiclient.discovery import build # Builds the call
from googleapiclient.errors import HttpError # Catches HTTP errors
from google.oauth2 import service_account # Google Authentication
import os # OS-independent way of getting directory paths

def sheets(sheet_id):
    creds = service_account.Credentials.from_service_account_file(os.path.join(os.path.dirname(__file__)) + '/credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    try:
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'Seeding'!A1:H").execute()
        values = result.get('values', [])

        if not values:
            return False

        for x in range(len(values[0])):
            values[0][x] = values[0][x].lower()
        name_index = values[0].index('name') if 'name' in values[0] else values[0].index('challonge')
        pts_index = values[0].index('points')
        players_to_points = {}

        for row in values[1:]:
            if len(row) >= 2:
                players_to_points.update({row[name_index]:row[pts_index]})

        return players_to_points
    except HttpError as err:
        status_code = str(err)[11:14]

        if status_code == '403':
            return "Lizard-BOT does not have access to configured spreadsheet. Please share the spreadsheet with Lizard-BOT"
        elif status_code == '400':
            return "Configured spreadsheet does not contain a sheet named 'Seeding'. Please add a 'Seeding' sheet."