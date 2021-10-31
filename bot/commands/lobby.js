const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('lobby')
		.setDescription('Returns lobby information'),
	async execute(interaction) {
		await interaction.reply(await getSetting('channel', 'lobby', interaction.channelId));
	},
};