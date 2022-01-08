const { bold, occurrences } = require('../utilities/utilities');
const { setSetting, settingsExist } = require('../utilities/database/db_util');

exports.setChanSettings = async function(interaction, command) {
	let channel = interaction.options.getChannel('channel');
	const msg = interaction.options.getString('message') ? interaction.options.getString('message') : '';

	if (!channel) {
		channel = interaction.channel;
	}
	else {
		await settingsExist(interaction.guildId, channel.id);
	}

	if (command === 'status' && occurrences(msg, '{0}', false) === 0) {
		throw 'Status message must include {0} to substitute the round number';
	}
	else if (msg && command === 'seeding' && (!msg.match(/[a-zA-Z0-9-_]+/g) || msg.length > 80)) {
		throw 'Invalid Sheets spreadsheet ID. Please view <https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md> for a walkthrough';
	}
	else if (msg.length > 1945) {
		throw 'Message is too long to be stored. Shorten your message to 1945 characters or less';
	}

	await setSetting('channel', command, channel.id, msg);
	await interaction.reply('In channel: ' + bold(channel.name) + ', the ' + bold(command) + ' command has been updated to: ' + bold(msg));
};