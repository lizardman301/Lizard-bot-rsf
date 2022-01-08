const { SlashCommandBuilder } = require('@discordjs/builders');

const { bold } = require('../utilities/utilities');
const { settingsExist, setSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('edit-tos')
		.addChannelOption(option => option.setName('channel').setDescription('Set a different channel to edit'))
		.addUserOption(option => option.setName('to_num1').setDescription('The first TO for the provided channel'))
		.addUserOption(option => option.setName('to_num2').setDescription('A second TO for the provided channel'))
		.setDescription('Edit the /TOs info in this channel or another'),
	async execute(interaction) {
		let channel = interaction.options.getChannel('channel');
		const to_1 = interaction.options.getMember('to_num1');
		const to_2 = interaction.options.getMember('to_num2');

		const to_pings = [];
		const to_names = [];

		if (to_1) {
			to_pings.push('<@' + to_1.id + '>');
			to_names.push(to_1.displayName);
		}
		if (to_2) {
			to_pings.push('<@' + to_2.id + '>');
			to_names.push(to_2.displayName);
		}

		if (!channel) {
			channel = interaction.channel;
		}
		else {
			await settingsExist(interaction.guildId, channel.id);
		}

		await setSetting('channel', 'tos', channel.id, to_pings.join(' '));
		await interaction.reply('In channel: ' + bold(channel.name) + ', the ' + bold('TOs') + ' command has been updated to: ' + bold(to_names.join(' & ')));
	},
};