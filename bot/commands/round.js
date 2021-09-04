const { SlashCommandBuilder } = require('@discordjs/builders');
const { setSetting } = require('../utilities/database/db_util');
const status = require('./status');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('round')
		.addStringOption(option => option.setName('round').setDescription('The round to declare it now is').setRequired(true))
		.setDescription('Changes the current round number to the new value'),
	async execute(interaction) {
		let round_num = interaction.options.getString('round');

		try {

			if (round_num.length > 50) {
				throw 'Custom round number must be less then 50 characters';
			}

		}
		catch (err) {
			await interaction.reply({ content: err, ephemeral: true });
			round_num = '';
		}

		if (round_num) {
			await setSetting('channel', 'round', interaction.channelId, round_num);
			await status.execute(interaction);
		}
	},
};