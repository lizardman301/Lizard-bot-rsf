const { SlashCommandBuilder } = require('@discordjs/builders');
const utilities = require('util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('liz')
		.setDescription('Replies with !liz'),
	async execute(interaction) {
		console.log(utilities.format('Pinged by %s', interaction.member.user.tag));
		await interaction.reply('Fuck you, Lizardman');
	},
};
