const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('stream')
		.setDescription('Returns stream information'),
	async execute(interaction) {
		let stream = await getSetting('channel', 'stream', interaction.channelId);

		if (!stream) {
			stream = 'There are no streams set for this channel';
		}
		await interaction.reply(stream);
	},
};