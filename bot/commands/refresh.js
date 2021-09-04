const { SlashCommandBuilder } = require('@discordjs/builders');
const { bold } = require('../utilities/utilities');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('refresh')
		.setDescription('Reminds users to refresh their brackets'),
	async execute(interaction) {
		await interaction.reply(bold('REFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS\nREFRESH YOUR BRACKETS'));
	},
};