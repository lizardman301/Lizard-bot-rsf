const { Util } = require('discord.js');

const axios = require('axios');

const secrets = require('../secret.json');
const { bold } = require('./utilities');
const { sheets } = require('./sheets/sheets');
const { getSetting } = require('./database/db_util');

function get_chal_tour_id(bracket_msg) {
	// designed to return the tournament identifier if it exists in the database bracket text
	// returns empty string otherwise

	// regex for <community_url>.challonge.com/<tournament identifier> or challonge.com/<tournament identifier>
	const regex = new RegExp('[-a-zA-Z0-9@:%._+~#=]{0,256}.challonge.com/[a-zA-Z0-9_]+');
	let url = '';
	let tour_id = '';

	// find first match and make that the url to work off of
	// if no match, return empty string immediately
	const matches = regex.exec(bracket_msg);
	if (matches !== null) {
		url = matches[0];
	}
	else {
		throw 'No bracket link set';
	}

	// get the identifer from the back part of the url
	// should only be one slash so we split on that
	// get the last group in order to get the tournament identifier
	tour_id = url.split('/').pop();
	return tour_id;
}

// Get all users in a Discord
function get_users(users) {
	const userDict = {};

	// Get their distinct name and their nickname
	users.forEach(user => {
		try {
			userDict[user['user']['username'] + '#' + String(user['user']['discriminator'])] = [user['nickname'].toLowerCase(), user['user']['id']];
		}
		catch (err) {
			userDict[user['user']['username'] + '#' + String(user['user']['discriminator'])] = [user['user']['username'].toLowerCase(), '<@' + user['user']['id'] + '>'];
		}
	});

	return userDict;
}

function checkin(parts, users) {
	// Discord server usernames and mentions
	users = Object.values(users);
	// Used for people missing from the server
	const not_discord_parts = [];
	// Used for people not checked in
	const not_checked_in_parts = [];
	// Discord server usernames
	const usernames = [];
	// Discord server mentions
	const mentions = [];

	users.forEach(user => {
		const userValues = Object.values(user);
		usernames.push(userValues[0]);
		mentions.push(userValues[1]);
	});

	// Check each participant to see if they are in the server and checked in
	parts.forEach(p => {
		p = p['participant'];

		const name_lower = p['display_name'].toLowerCase();
		const name_escaped = Util.escapeMarkdown(p['display_name']);
		const challonge_name_lower = p['challonge_username'] ? p['challonge_username'].toLowerCase() : name_lower;

		if (!p['checked_in']) {
			not_checked_in_parts.push(name_escaped);
		}

		if (
			!(usernames.find(elem => {
				return elem.toLowerCase().includes(name_lower);
			})
			) &&
			!(usernames.find(elem => {
				return elem.toLowerCase().includes(challonge_name_lower);
			}))
		) {
			not_discord_parts.push(name_escaped);
		}

		if (
			(
				!(not_discord_parts.includes(name_escaped)) && (not_checked_in_parts.includes(name_escaped))
			) && (
				(usernames.find(elem => {
					return elem.toLowerCase().includes(name_lower);
				})) ||
				(usernames.find(elem => {
					return elem.toLowerCase().includes(challonge_name_lower);
				}))
			)
		) {
			const match = usernames.filter(elem => {
				elem = elem.toLowerCase();
				if (elem.includes(name_lower) || elem.includes(challonge_name_lower)) {
					return true;
				}
				else {
					return false;
				}
			});

			not_checked_in_parts[not_checked_in_parts.indexOf(name_escaped)] = mentions[usernames.indexOf(match[0])];
		}
	});

	not_checked_in_parts.sort();
	not_discord_parts.sort();

	return [not_checked_in_parts, not_discord_parts];
}

async function seeding(sheet_id, parts, url, seed_num) {
	// Stores "player point_value" for sorting later
	let player_points = [];

	// Get dict of associated players and their points
	const players_to_points = await sheets(sheet_id);

	// Check each participant and if they have points
	parts.forEach(p => {
		p = p['participant'];

		if (Object.keys(players_to_points).includes(p['challonge_username']) && p['checked_in']) {
			player_points.push(p['challonge_username'] + ' ' + players_to_points[p['challonge_username']]);
		}
	});

	player_points.sort(function(n, o) {
		n = n.split(' ')[0].toLowerCase();
		o = o.split(' ')[0].toLowerCase();
		if (n < o) {
			return -1;
		}
		else if (n > o) {
			return 1;
		}
		return 0;
	});
	player_points.sort(function(n, o) {
		n = parseInt(n.split(' ')[1]);
		o = parseInt(o.split(' ')[1]);
		if (n > o) {
			return -1;
		}
		else if (n < o) {
			return 1;
		}
		return 0;
	});

	if (seed_num > 0 && seed_num <= player_points.length) {
		player_points = player_points.slice(0, seed_num);
	}

	const finished_seeding = {};
	for (let n = 0; n < player_points.length; n++) {
		finished_seeding[n + 1] = player_points[n];
	}

	try {
		await axios.post(url + '/participants/randomize.json', {}, {
			headers: {
				'User-Agent':'Lizard-BOT',
			},
			auth: {
				username: secrets.chal_user,
				password: secrets.api_key,
			},
		});
	}
	catch (err) {
		if (err.response.status === 401) {
			console.log(err);
			console.log(bold('Challonge') + ': Lizard-BOT does not have access to that tournament');
		}
		else {
			console.log(err);
			console.log(bold('Challonge') + 'Unknown Challonge error for <' + err.config.url + '> while randomizing seeds');
		}
	}

	for (let key = 1; key <= Object.keys(finished_seeding).length; key++) {
		for (let i = 0; i < parts.length; i++) {
			const p = parts[i]['participant'];

			if (p['challonge_username'] === finished_seeding[key].split(' ')[0]) {
				try {
					await axios.put(url + '/participants/' + String(p['id']) + '.json', {}, {
						params: {
							'participant[seed]': parseInt(key),
						},
						headers: {
							'User-Agent': 'Lizard-BOT',
						},
						auth: {
							username: secrets.chal_user,
							password: secrets.api_key,
						},
					});
				}
				catch (err) {
					if (err.response.status === 401) {
						console.log(err);
						console.log(bold('Challonge') + ': Lizard-BOT does not have access to that tournament');
					}
					else {
						console.log(err);
						console.log(bold('Challonge') + 'Unknown Challonge error for <' + err.config.url + '> while seeding: ' + p['challonge_username']);
					}
				}
			}
		}
	}

	return finished_seeding;
}

async function start_challonge(channelId, guildId) {
	const baseUrl = 'https://api.challonge.com/v1/tournaments/';
	let tourUrl;
	try {
		tourUrl = get_chal_tour_id(await getSetting('channel', 'bracket', channelId));
	}
	catch (err) {
		console.log(err);
	}

	const subdomain = await getSetting('guild', 'challonge', guildId);

	if (subdomain) {
		tourUrl = subdomain + '-' + tourUrl;
	}

	try {
		const res = await axios.get(baseUrl + tourUrl + '/participants.json', {
			headers: {
				'User-Agent': 'Lizard-BOT',
			},
			auth: {
				username: secrets.chal_user,
				password: secrets.api_key,
			},
		});
		return [res.data, tourUrl];
	}
	catch (err) {
		if (err.response.status === 401) {
			console.log(err);
			console.log(bold('Challonge') + ': Lizard-BOT does not have access to that tournament');
		}
		else if (err.response.status === 404) {
			console.log(err);
			console.log(bold('Challonge') + ': Lizard-BOT can not find tournament: ' + tourUrl);
		}
		else {
			console.log(err);
			console.log(bold('Challonge') + 'Unknown Challonge error for <' + err.config.url + '> initializing connection to Challonge');
		}
	}
}

module.exports = {
	checkin,
	get_users,
	seeding,
	start_challonge,
};