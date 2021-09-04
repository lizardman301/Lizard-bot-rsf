const { SlashCommandBuilder } = require('@discordjs/builders');

const { setChanSettings } = require('../utilities/edit_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('edit-bracket')
		.addChannelOption(option => option.setName('channel').setDescription('Set a different channel to edit'))
		.addStringOption(option => option.setName('message').setDescription('Sets the bracket message for the channel'))
		.setDescription('Edit the /bracket info in this channel or another'),
	async execute(interaction) {
		try {
			await setChanSettings(interaction, 'bracket');
		}
		catch (err) {
			interaction.reply({ content: err, ephemeral: true });
		}
	},
};