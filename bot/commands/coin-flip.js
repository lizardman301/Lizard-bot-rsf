const { SlashCommandBuilder } = require('@discordjs/builders');
const utilities = require('util');
const { bold } = require('../utilities/utilities');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('coin-flip')
		.setDescription('Flips a coin'),
	async execute(interaction) {
		await interaction.reply(utilities.format('The coin landed on: %s', bold(['Heads', 'Tails'][Math.floor(Math.random() * 2)])));
	},
};