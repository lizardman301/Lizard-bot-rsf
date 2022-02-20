const { getSetting } = require('../utilities/database/db_util');

function bold(string) {
	return '**' + string + '**';
}

async function get_bot_role(interaction) {
	const botrole = await getSetting('guild', 'botrole', interaction.guildId);
	let botrole_name;

	try {
		botrole_name = interaction.guild.roles.cache.get(String(botrole)).name;
	}
	catch {
		botrole_name = 'everyone';
	}

	return botrole_name;
}

function get_randomselect_data(game, random_type) {
	const rs_info = require('./rs.json');
	const games = Object.keys(rs_info[random_type]);

	if (!games.includes(game)) {
		return [[], games];
	}
	const values = Object.values(rs_info[random_type][game]);
	return [values.slice(0, values.length - 1), games];
}

// Perform regex to find out if a string is a Discord channel
exports.is_channel = function(channel) {
	const regex = new RegExp('<#[0-9]*>');
	if (channel.match(regex)) {
		// eslint-disable-next-line no-undef
		return BigInt(channel.slice(2, -1));
		// Return only the channel ID
	}
	return 0;
};

// Simplify removing pings more
exports.pings_b_gone = function(mentions) {
	const mention_list = {};
	// Empty dict to store values in

	// For each mention, get the name and the mention value
	mentions.forEach(mention => {
		const ping = '<@!' + String(mention.id) + '>';
		if (mention.nick) {
			mention_list[mention.nick] = ping;
			return;
		}
		mention_list[mention.name] = ping;
	});

	return mention_list;
};

/** Function that count occurrences of a substring in a string;
 * @param {String} string		The string
 * @param {String} subString	The sub string to search for
 * @param {Boolean} [allowOverlapping]	Optional. (Default:false)
 *
 * @author Vitim.us https://gist.github.com/victornpb/7736865/edit
 */
function occurrences(string, subString, allowOverlapping) {

	string += '';
	subString += '';
	if (subString.length <= 0) return (string.length + 1);

	let n = 0,
		pos = 0;
	const step = allowOverlapping ? 1 : subString.length;

	// eslint-disable-next-line no-constant-condition
	while (true) {
		pos = string.indexOf(subString, pos);
		if (pos >= 0) {
			++n;
			pos += step;
		}
		else {
			break;
		}
	}
	return n;
}

module.exports = {
	bold,
	occurrences,
	get_randomselect_data,
	get_bot_role,
};