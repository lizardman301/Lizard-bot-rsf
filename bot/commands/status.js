const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');
const { bold } = require('../utilities/utilities');

async function getStatus(channelId) {
	const currentRound = await getSetting('channel', 'round', channelId);
	if (currentRound) {
		try {
			const message = await getSetting('channel', 'status', channelId);
			return (bold(message).replace(/\{0\}/g, currentRound));
		}
		catch (err) {
			return bold('Status') + ': Round message includes invalid {}. Please correct the status message to include only {0}';
		}
	}
	else {
		return bold('Tournament has not begun. Please wait for the TOs to start Round 1!');
	}
}

module.exports = {
	data: new SlashCommandBuilder()
		.setName('status')
		.setDescription('Returns the tournament round status'),
	async execute(interaction) {
		await interaction.reply(await getStatus(interaction.channelId));
	},
};