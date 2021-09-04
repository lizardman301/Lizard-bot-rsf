const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('tos')
		.setDescription('Returns the channel\'s TO(s)'),
	async execute(interaction) {
		const tos = await getSetting('channel', 'tos', interaction.channelId);

		if (tos) {
			await interaction.reply(tos);
		}
		else {
			await interaction.reply('There are no TOs associated with this channel.');
		}
	},
};