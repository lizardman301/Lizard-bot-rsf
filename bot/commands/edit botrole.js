const { SlashCommandBuilder } = require('@discordjs/builders');

const { setSetting } = require('../utilities/database/db_util');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('edit-botrole')
		.addRoleOption(option => option.setName('botrole').setDescription('Select the new botrole').setRequired(true))
		.setDescription('Edit the role that can access privileged commands'),
	async execute(interaction) {
		const botrole = interaction.options.getRole('botrole');
		await setSetting('guild', 'botrole', interaction.guildId, botrole.id);
		await interaction.reply('The new **botrole** is: ' + botrole.name);
	},
};