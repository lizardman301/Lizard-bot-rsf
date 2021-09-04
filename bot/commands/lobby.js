const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('lobby')
		.setDescription('Returns lobby information'),
	async execute(interaction) {
		let lobby = await getSetting('channel', 'lobby', interaction.channelId);

		if (!lobby) {
			lobby = 'There is no lobby command set for this channel';
		}

		await interaction.reply(lobby);
	},
};