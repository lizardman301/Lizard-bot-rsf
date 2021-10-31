const { SlashCommandBuilder } = require('@discordjs/builders');
const { setSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('reset')
		.setDescription('Resets the round counter'),
	async execute(interaction) {
		setSetting('channel', 'round', interaction.channelId, '');
		await interaction.reply('The round has been reset');
	},
};
