const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');
const { bold } = require('../utilities/utilities');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('status')
		.setDescription('Returns lobby information'),
	async execute(interaction) {
		const currentRound = await getSetting('channel', 'round', interaction.channelId);
		if (currentRound) {
			try {
				const message = await getSetting('channel', 'status', interaction.channelId);
				await interaction.reply((bold(message).replace(/\{0\}/g, currentRound)));
			}
			catch (err) {
				await interaction.reply(bold('Status') + ': Round message includes invalid {}. Please correct the status message to include only {0}');
			}
		}
		else {
			await interaction.reply(bold('Tournament has not begun. Please wait for the TOs to start Round 1!'));
		}
	},
};