function bold(string) {
	return '**' + string + '**';
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

module.exports = {
	bold,
	get_randomselect_data,
};