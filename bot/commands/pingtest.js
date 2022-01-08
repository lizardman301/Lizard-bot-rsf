const { SlashCommandBuilder } = require('@discordjs/builders');
const { getSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('pingtest')
		.setDescription('Returns ping test information'),
	async execute(interaction) {
		let pingtest = await getSetting('channel', 'pingtest', interaction.channelId);

		if (!pingtest) {
			pingtest = 'Use <https://testmyspeed.onl/> for ping tests';
		}

		await interaction.reply(pingtest);
	},
};