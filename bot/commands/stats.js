const { SlashCommandBuilder, bold } = require('@discordjs/builders');
const { MessageButton, MessageEmbed } = require('discord.js');
const paginationEmbed = require('discordjs-button-pagination');

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
				.setAuthor('Lizard-BOT', 'https://raw.githubusercontent.com/lizardman301/Lizard-bot-rsf/master/doc/assets/images/cmface.png', 'https://github.com/lizardman301/Lizard-bot-rsf');
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

		const buttonList = [
			back,
			forward,
		];

		try {
			paginationEmbed(interaction, pages, buttonList);
		}
		catch (err) {
			console.log(err);
		}
	},
};