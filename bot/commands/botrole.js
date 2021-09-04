const { SlashCommandBuilder } = require('@discordjs/builders');
const utilities = require('util');
const { getSetting } = require('../utilities/database/db_util');
const { bold } = require('../utilities/utilities');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('botrole')
		.setDescription('Returns Botrole information'),
	async execute(interaction) {
		const botrole = await getSetting('guild', 'botrole', interaction.guildId);
		let botrole_name;

		try {
			botrole_name = interaction.guild.roles.cache.get(String(botrole)).name;
		}
		catch {
			botrole_name = 'everyone';
		}

		await interaction.reply(utilities.format('The bot role is: %s', bold(botrole_name)));
	},
};