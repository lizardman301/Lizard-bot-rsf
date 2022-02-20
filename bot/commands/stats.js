const { SlashCommandBuilder, bold } = require('@discordjs/builders');
const { MessageButton, MessageEmbed, MessageActionRow } = require('discord.js');

const { readStat } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('stats')
		.setDescription('Returns how many times commands have been used')
		.addStringOption(option => option.setName('command').setDescription('Specify a command to read stats on')),
	async execute(interaction) {
		const command = interaction.options.getString('command') ? interaction.options.getString('command') : '';

		const stats = await readStat(command);

		const fields = [];

		for (let i = 0; i < stats.length; i++) {
			const stat = stats[i].dataValues;

			fields.push({ name: bold(stat['command']), value: String(stat['used']), inline: true });
		}

		const pages = [];
		let count = 1;
		while (fields.length > 0) {
			const embed = new MessageEmbed()
				.setColor('#0fa1dc')
				.setTitle('Page: ' + String(count))
				.setDescription('Stats!')
				.setAuthor({ name: 'Lizard-BOT', iconUrl: 'https://raw.githubusercontent.com/lizardman301/Lizard-bot-rsf/master/doc/assets/images/cmface.png', url: 'https://github.com/lizardman301/Lizard-bot-rsf' });
			const embedFields = fields.splice(0, 25);
			embed.addFields(embedFields);

			pages.push(embed);
			count++;
		}

		const back = new MessageButton()
			.setCustomId('back')
			.setLabel('Previous')
			.setStyle('SUCCESS');

		const forward = new MessageButton()
			.setCustomId('fwd')
			.setLabel('Next')
			.setStyle('SUCCESS');

		const row = new MessageActionRow().addComponents([
			back,
			forward,
		]);
		let activePage = 0;

		const curPage = await interaction.reply({
			embeds: [pages[activePage].setFooter({ text: `Page ${activePage + 1} / ${pages.length}` })],
			components: [row],
			fetchReply: true,
		});

		const filter = (interact) =>
			interact.customId === back.customId ||
			interact.customId === forward.customId;

		const collector = await curPage.createMessageComponentCollector({ filter, time: 30 * 1000 });

		collector.on('collect', async (interact) => {
			switch (interact.customId) {
			case back.customId:
				activePage = activePage > 0 ? --activePage : pages.length - 1;
				break;
			case forward.customId:
				activePage = activePage + 1 < pages.length ? ++activePage : 0;
				break;
			default:
				break;
			}
			await interact.deferUpdate();
			await interact.editReply({
				embeds: [pages[activePage].setFooter(`Page ${activePage + 1} / ${pages.length}`)],
				components: [row],
			});
			collector.resetTimer();
		});

		collector.on('end', async () => {
			try {
				await curPage.delete();
			}
			// eslint-disable-next-line no-empty
			catch {}
		});
	},
};