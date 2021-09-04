const { google } = require('googleapis');

exports.sheets = async function(sheet_id) {
	const auth = new google.auth.GoogleAuth({
		keyFile: './bot/utilities/sheets/credentials.json',
		scopes: ['https://www.googleapis.com/auth/spreadsheets.readonly'],
	});
	const creds = await auth.getClient();
	const service = google.sheets('v4');
	const request = {
		spreadsheetId: sheet_id,
		range: '\'Seeding\'!A1:H',
		auth: creds,
	};

	try {
		const response = (await service.spreadsheets.values.get(request));
		const values = response.data.values;

		if (!Array.isArray(values) || !values.length) {
			throw '**Challonge**: **Sheets**: Seeding sheet returned nothing';
		}

		for (let i = 0; i < values[0].length; i++) {
			values[0][i] = values[0][i].toLowerCase();
		}
		const name_index = values[0].includes('name') ? values[0].indexOf('name') : values[0].indexOf('challonge');
		const pts_index = values[0].indexOf('points');
		const players_to_points = {};

		values.slice(1).forEach(row => {
			if (row.length >= 2) {
				players_to_points[row[name_index]] = row[pts_index];
			}
		});

		return players_to_points;
	}
	catch (err) {
		console.error(err);
	}
};