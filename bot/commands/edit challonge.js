const { SlashCommandBuilder } = require('@discordjs/builders');

const { bold } = require('../utilities/utilities');
const { setSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('edit-challonge')
		.addStringOption(option => option.setName('subdomain').setDescription('Sets the stream message for the channel'))
		.setDescription('Edit the subdomain all the /challonge commands will use for the server'),
	async execute(interaction) {
		const subdomain = interaction.options.getString('subdomain') ? interaction.options.getString('subdomain') : '';

		if (subdomain.length > 60) {
			await interaction.reply({ content: 'Challonge Subdomain is too long. Are you sure that is a Challonge subdomain?', ephemeral: true });
			return;
		}

		await setSetting('guild', 'challonge', interaction.guildId, subdomain);
		await interaction.reply('The ' + bold('challonge') + ' commands has been updated to use: ' + bold(subdomain) + ' as the Challonge Subdomain');
	},
};