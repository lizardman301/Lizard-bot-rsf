const { SlashCommandBuilder } = require('@discordjs/builders');

const { setChanSettings } = require('../utilities/edit_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('edit-stream')
		.addChannelOption(option => option.setName('channel').setDescription('Set a different channel to edit'))
		.addStringOption(option => option.setName('message').setDescription('Sets the stream message for the channel'))
		.setDescription('Edit the /stream info in this channel or another'),
	async execute(interaction) {
		try {
			await setChanSettings(interaction, 'stream');
		}
		catch (err) {
			interaction.reply({ content: err, ephemeral: true });
		}
	},
};