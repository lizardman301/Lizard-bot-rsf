# Hosting a Google Sheet for Challonge seeding

Written below are steps for 3 different options: creating a new Google Sheet, adapting an existing Google Sheet, or information about how r/StreetFighter

NOTE: This bot was designed with r/StreetFighter in mind. As such, decisions about how a sheet needs to be formatted is based on how their ranking sheets look. For information about how [sniffulls](https://twitter.com/Sniffulls) manages FOUR(!) different weekly's points, please view [his documentation](https://drive.google.com/drive/folders/14VqkUtccASi6BuPPpak0Hl0eBYcF0HsP?usp=sharing)

## Using r/StreetFighter Template

This option is for those looking to copy r/StreetFighter's layout and formula to Google Sheets
### 1. Read about sniffulls process for updating the sheet

You have to know what you are getting into
1. Go to <https://docs.google.com/document/d/13FWt1BgcHsiFCu06y_uWOh5tQXiu3GpZXp_hVbK7JQE/edit?usp=sharing>
2. Read the process
3. Decide if you are going to continue

### 2. Copying Template

Got to have a good base
1. Go to <https://docs.google.com/spreadsheets/d/1hbbFZLhe4avpH3DLNxcOy5owtG3YMgTXbNSODCcgPyU/edit?usp=sharing>
2. Under the File menu, choose 'Make a copy'
Make sure you choose the appropriate name and destination folder

### 3. Add Lizard-BOT as a viewer of the sheet

Give permissions to Lizard-BOT to view your sheet
1. Click share in the upper right
2. Copy 'INSERT ACCOUNT EMAIL'
3. Paste that into the invite box and push Enter on your keyboard
4. On the followup page, change the access from Editor to Viewer
5. Uncheck Notify people
6. Click Share

![Share menu](/doc/assets/images/spreadsheet_share1.png)

![Making sure the account is Viewer access and has 'Notify people' unchecked](/doc/assets/images/spreadsheet_share2.png)

### 4. Add Spreadsheet ID to the channel

Now, that there is a spreadsheet with points that Lizard-BOT has access to. We need to know to use that spreadsheet
1. Open up the Google Sheet that will be used
2. Look at the URL
	- It should look like: <https://docs.google.com/spreadsheets/d/1Msq8pgWFj83DwLumVdgk84fSmBG_Uq3UcaJ7Ro_mk6Q/edit>
3. Copy the spreadsheet ID from the URL
	- The spreadsheet ID is between 'spreadsheet/d/' and '/edit'
	- 1Msq8pgWFj83DwLumVdgk84fSmBG_Uq3UcaJ7Ro_mk6Q in this case
4. Navigate to a Discord Sever with Lizard-BOT and where you have edit access to the bot
5. Use command `edit [CHANNEL_MENTION] seeding [SPREADSHEET_ID]`
	- Replace the brackets with the unique information

### End of r/StreetFighter Template

## New Google Sheet

Use this when a more basic setup is preferred.

This option also allows for more unique customizations if desired
### 1. Create New Sheet

A spreadsheet needs to exist
1. Navigate to sheets.google.com (Log in if necessary)
2. Create a blank spreadsheet

![Create new blank spreadsheet](/doc/assets/images/new_spreadsheet.png)

### 2. Rename Sheet to Seeding

In the lower left corner of the spreadsheet, the sheet will be defaultly named 'Sheet1'
There will be a little arrow to the right of the sheet name.
1. Click that and choose 'Rename'
2. Rename the sheet to 'Seeding'

![Menu to find Rename](/doc/assets/images/sheet_rename1.png)

![Rename showing 'Seeding'](/doc/assets/images/sheet_rename2.png)

### 3. Add the headers

Row 1 columns A and B will be our headers for the table of data
1. In A1, type in 'Challonge'
2. In B1, type in 'Points'

![Headers showing Challonge and Points](/doc/assets/images/sheet_headers.png)

Optional: Lock headers to the top
1. View > Freeze > 1 row will lock the first row

![Menu path to find the freeze option](/doc/assets/images/sheet_headers_freeze.png)

### 4. Add data

IMPORTANT: **When adding data make sure that the challonge column contains challonge *USERNAMES (Usernames are different from display names)***

![The difference between a display name and a challonge username](/doc/assets/images/challonge_name_vs_challonge_name.png)

Each row will be for a specific player.
1. In the Challonge column, insert the player's username as dictated by challonge
2. In the Points column, insert the player's point total (via manual or formulaic means)

### 5. Add Lizard-BOT as a viewer of the sheet

Give permissions to Lizard-BOT to view your sheet
1. Click share in the upper right
2. Copy 'INSERT ACCOUNT EMAIL'
3. Paste that into the invite box and push Enter on your keyboard
4. On the followup page, change the access from Editor to Viewer
5. Uncheck Notify people
6. Click Share

![Share menu](/doc/assets/images/spreadsheet_share1.png)

![Making sure the account is Viewer access and has 'Notify people' unchecked](/doc/assets/images/spreadsheet_share2.png)

### 6. Add Spreadsheet ID to the channel

Now, that there is a spreadsheet with points that Lizard-BOT has access to. We need to know to use that spreadsheet
1. Open up the Google Sheet that will be used
2. Look at the URL
	- It should look like: <https://docs.google.com/spreadsheets/d/1Msq8pgWFj83DwLumVdgk84fSmBG_Uq3UcaJ7Ro_mk6Q/edit>
3. Copy the spreadsheet ID from the URL
	- The spreadsheet ID is between 'spreadsheet/d/' and '/edit'
	- 1Msq8pgWFj83DwLumVdgk84fSmBG_Uq3UcaJ7Ro_mk6Q in this case
4. Navigate to a Discord Sever with Lizard-BOT and where you have edit access to the bot
5. Use command `edit [CHANNEL_MENTION] seeding [SPREADSHEET_ID]`
	- Replace the brackets with the unique information

### End of New Google Sheet

## Adapting a Google Sheet

This is the most difficult option and requires manual work to update player names to challonge usernames

There is no way for to cover each unique spreadsheet configuration
#### Use this as guidelines to adapting your sheet and not a step by step
### 1. Adding an additional sheet for Seeding

Here we add the explicit sheet for Lizard-BOT to query
1. Create a new sheet
2. Rename it 'Seeding'

![Menu to find Rename](/doc/assets/images/sheet_rename1.png)

![Rename showing 'Seeding'](/doc/assets/images/sheet_rename2.png)

### 2. Add the headers

Row 1 columns A, and B will be our headers for the table of data
1. In A1, type in 'Challonge'
2. In B1, type in 'Points'

![Headers showing Challonge and Points](/doc/assets/images/sheet_headers.png)

Optional: Lock headers to the top
1. View > Freeze > 1 row will lock the first row

![Menu path to find the freeze option](/doc/assets/images/sheet_headers_freeze.png)

### 3. Add data

IMPORTANT: **When adding data make sure that the challonge column contains challonge *USERNAMES (Usernames are different from display names)***

![The difference between a display name and a challonge username](/doc/assets/images/challonge_name_vs_challonge_name.png)

Each row will be for a specific player.
1. In the Challonge column, insert the player's username as dictated by challonge
2. In the Points column, insert the player's point total (via manual or formulaic means)

If you have a sheet named 'Main' set up with the 1st column as challonge usernames and the 4th column as your points, you can use the formula: `=iferror(vlookup($A2, Main!A:D, 4, false), 0)`
Note: If your Sheet was created in a European country, it may be necessary to use: `=iferror(vlookup($A2; Main!A:D; 4; false); 0)`

![Main sheet with extra information](/doc/assets/images/sheet_adapt1.png)

![Seeding sheet with only the proper information](/doc/assets/images/sheet_adapt2.png)

### 4. Add Lizard-BOT as a viewer of the sheet

Give permissions to Lizard-BOT to view your sheet
1. Click share in the upper right
2. Copy 'INSERT ACCOUNT EMAIL'
3. Paste that into the invite box and push Enter on your keyboard
4. On the followup page, change the access from Editor to Viewer
5. Uncheck Notify people
6. Click Share

![Share menu](/doc/assets/images/spreadsheet_share1.png)

![Making sure the account is Viewer access and has 'Notify people' unchecked](/doc/assets/images/spreadsheet_share1.png)

### 5. Add Spreadsheet ID to the channel

Now, that there is a spreadsheet with points that Lizard-BOT has access to. We need to know to use that spreadsheet
1. Open up the Google Sheet that will be used
2. Look at the URL
	- It should look like: <https://docs.google.com/spreadsheets/d/1Msq8pgWFj83DwLumVdgk84fSmBG_Uq3UcaJ7Ro_mk6Q/edit>
3. Copy the spreadsheet ID from the URL
	- The spreadsheet ID is between 'spreadsheet/d/' and '/edit'
	- 1Msq8pgWFj83DwLumVdgk84fSmBG_Uq3UcaJ7Ro_mk6Q in this case
4. Navigate to a Discord Sever with Lizard-BOT and where you have edit access to the bot
5. Use command `edit [CHANNEL_MENTION] seeding [SPREADSHEET_ID]`
	- Replace the brackets with the unique information

### End of Adapting a Google Sheet