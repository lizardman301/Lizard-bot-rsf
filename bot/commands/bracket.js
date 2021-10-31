const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('bracket')
		.setDescription('Returns bracket information'),
	async execute(interaction) {
		await interaction.reply(await getSetting('channel', 'bracket', interaction.channelId));
	},
};