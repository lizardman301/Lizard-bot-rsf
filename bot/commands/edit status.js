const { SlashCommandBuilder } = require('@discordjs/builders');

const { setChanSettings } = require('../utilities/edit_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('edit-status')
		.addStringOption(option => option.setName('message').setDescription('Sets the status message for the channel').setRequired(true))
		.addChannelOption(option => option.setName('channel').setDescription('Set a different channel to edit'))
		.setDescription('Edit the /status info in this channel or another'),
	async execute(interaction) {
		try {
			await setChanSettings(interaction, 'status');
		}
		catch (err) {
			interaction.reply({ content: err, ephemeral: true });
		}
	},
};