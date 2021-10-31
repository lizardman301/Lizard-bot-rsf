const { SlashCommandBuilder } = require('@discordjs/builders');
const utilities = require('util');
const { bold, get_randomselect_data } = require('../utilities/utilities');
const raw_rs = require('../utilities/rs.json');

const init_games = Object.keys(Object.values(raw_rs)[0]).filter(function(obj) { return Object.keys(Object.values(raw_rs)[1]).indexOf(obj) >= -1; });

const types = [];
const supported_games = [];

Object.keys(raw_rs).forEach(type => {
	types.push([type, type]);
});

init_games.forEach(game => {
	supported_games.push([game, game]);
});

module.exports = {
	data: new SlashCommandBuilder()
		.setName('rs')
		.setDescription('Returns a random character or stage for a supported game')
		.addStringOption(option => option.setName('type').setDescription('Character or Stage').addChoices(types).setRequired(true))
		.addStringOption(option => option.setName('game').setDescription('Choose a supported game').addChoices(supported_games).setRequired(true)),
	async execute(interaction) {
		const type = interaction.options.getString('type').toLowerCase();
		const game = interaction.options.getString('game').toLowerCase();

		let data, games;
		try {
			[data, games] = get_randomselect_data(game, type);
		}
		catch (err) {
			console.log(err);
		}

		if (!data) {
			await interaction.reply(utilities.format('Invalid game %s: Valid games are: %s', game, bold(games.join(', '))));
		}
		else if (type === 'stage') {
			await interaction.reply(utilities.format('Your randomly selected stage is: %s', bold(data[Math.floor(Math.random() * data.length)])));
		}
		else {
			await interaction.reply(utilities.format('Your randomly selected character is: %s', bold(data[Math.floor(Math.random() * data.length)])));
		}
	},
};