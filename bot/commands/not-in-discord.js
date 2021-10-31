const { SlashCommandBuilder } = require('@discordjs/builders');
const { bold } = require('../utilities/utilities');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('not-in-discord')
		.setDescription('Informs about what Not In Discord means'),
	async execute(interaction) {
		await interaction.reply(bold('Your Discord nickname must match your challonge. If it does *NOT*, you will show as *NOT IN DISCORD*'));
	},
};