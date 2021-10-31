const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('pingtest')
		.setDescription('Returns ping test information'),
	async execute(interaction) {
		await interaction.reply(await getSetting('channel', 'pingtest', interaction.channelId));
	},
};