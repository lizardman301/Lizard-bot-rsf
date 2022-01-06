const { SlashCommandBuilder } = require('@discordjs/builders');
const utilities = require('util');
const { bold } = require('../utilities/utilities');
const { checkin, get_users, start_challonge } = require('../utilities/chal_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('challonge-checkin')
		.setDescription('Placeholder text'),
	async execute(interaction) {
		const all_members = await interaction.guild.members.fetch();
		await interaction.deferReply();
		// eslint-disable-next-line no-unused-vars
		const [parts, tourUrl] = await start_challonge(interaction.channelId, interaction.guildId);

		const [not_checked_in_parts, not_discord_parts] = checkin(parts, get_users(all_members));

		await interaction.editReply(utilities.format(bold('NOT CHECKED:') + ' %s\n' + bold('NOT IN DISCORD:') + '%s\n' + bold('Your Discord nickname must match your challonge. If it does *NOT*, you will show as *NOT IN DISCORD*'), not_checked_in_parts.join(', '), not_discord_parts.join(', ')));
	},
};