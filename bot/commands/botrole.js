const { SlashCommandBuilder } = require('@discordjs/builders');
const utilities = require('util');
const { bold, get_bot_role } = require('../utilities/utilities');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('botrole')
		.setDescription('Returns Botrole information'),
	async execute(interaction) {
		const botrole_name = await get_bot_role(interaction);

		await interaction.reply(utilities.format('The bot role is: %s', bold(botrole_name)));
	},
};