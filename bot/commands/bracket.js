const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('bracket')
		.setDescription('Returns bracket information'),
	async execute(interaction) {
		let bracket = await getSetting('channel', 'bracket', interaction.channelId);

		if (!bracket) {
			bracket = 'There is no bracket set for this channel';
		}

		await interaction.reply(bracket);
	},
};