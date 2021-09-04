const { SlashCommandBuilder } = require('@discordjs/builders');
const { Util } = require('discord.js');

const { getSetting } = require('../utilities/database/db_util');
const { seeding, start_challonge } = require('../utilities/chal_util');

const baseUrl = 'https://api.challonge.com/v1/tournaments/';

module.exports = {
	data: new SlashCommandBuilder()
		.setName('challonge-seeding')
		.addIntegerOption(option => option.setName('seed_num').setDescription('Number of players to seed'))
		.setDescription('Placeholder text'),
	async execute(interaction) {
		let seed_num = parseInt(interaction.options.getInteger('seed_num'));

		if (!seed_num) {
			seed_num = 0;
		}
		else if (seed_num < 0) {
			await interaction.editReply({ content: 'Seeding number must be a positive integer or 0 for everybody', ephemeral: true });
			return;
		}
		await interaction.deferReply();
		const [parts, tourUrl] = await start_challonge(interaction.channelId, interaction.guildId);

		const sheet_id = await getSetting('channel', 'seeding', interaction.channelId);

		if (!sheet_id) {
			await interaction.editReply({ content: 'There is no seeding sheet for this channel. Please view <https://github.com/lizardman301/Lizard-bot-rsf/blob/master/doc/seeding_with_sheets.md> for a walkthrough', ephemeral: true });
			return;
		}

		const seeds = await seeding(sheet_id, parts, baseUrl + tourUrl, seed_num);

		await interaction.editReply('**SEEDING**:\n' + Util.escapeMarkdown(JSON.stringify(seeds).replace(/[{}"]/g, '').replace(/:/g, ': ').replace(/,/g, 'pts,\n')) + 'pts\n**SEEDING IS NOW COMPLETE!\nPLEASE REFRESH YOUR BRACKETS\nWAIT FOR THE ROUND 1 ANNOUNCEMENT TO START PLAYING**');
	},
};