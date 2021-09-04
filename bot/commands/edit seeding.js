const { SlashCommandBuilder } = require('@discordjs/builders');

const { setChanSettings } = require('../utilities/edit_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('edit-seeding')
		.addChannelOption(option => option.setName('channel').setDescription('Set a different channel to edit'))
		.addStringOption(option => option.setName('message').setDescription('The ID of the Google Sheet for seeding'))
		.setDescription('Change the Google Sheet used for seeding the channels'),
	async execute(interaction) {
		try {
			await setChanSettings(interaction, 'seeding');
		}
		catch (err) {
			interaction.reply({ content: err, ephemeral: true });
		}
	},
};