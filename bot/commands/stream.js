const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('stream')
		.setDescription('Returns stream information'),
	async execute(interaction) {
		await interaction.reply(await getSetting('channel', 'stream', interaction.channelId));
	},
};