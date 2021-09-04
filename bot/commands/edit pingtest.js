const { SlashCommandBuilder } = require('@discordjs/builders');

const { setChanSettings } = require('../utilities/edit_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('edit-pingtest')
		.addChannelOption(option => option.setName('channel').setDescription('Set a different channel to edit'))
		.addStringOption(option => option.setName('message').setDescription('Sets the pingtest message for the channel'))
		.setDescription('Edit the /pingtest info in this channel or another'),
	async execute(interaction) {
		try {
			await setChanSettings(interaction, 'pingtest');
		}
		catch (err) {
			interaction.reply({ content: err, ephemeral: true });
		}
	},
};