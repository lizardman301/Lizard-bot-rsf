const { SlashCommandBuilder } = require('@discordjs/builders');
const wait = require('util').promisify(setTimeout);
const utilities = require('util');
const { bold } = require('../utilities/utilities');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('remind')
		.setDescription('Reminds the user after the determined wait time (optional: message)')
		.addIntegerOption(option => option.setName('time').setDescription('Time to wait in minutes. Up to 15 minutes').setRequired(true))
		.addStringOption(option => option.setName('message').setDescription('Message to be reminded of')),
	async execute(interaction) {
		let time;
		const msg = interaction.options.getString('message');

		try {
			time = parseInt(interaction.options.getInteger('time'));

			if (time < 1 || time > 15) {
				throw 'Time must be positive and less than 15 minutes';
			}
		}
		catch (err) {
			await interaction.reply({ content: err, ephemeral: true });
			time = 0;
		}

		if (time) {
			let formatted_msg;
			if (msg) {
				formatted_msg = utilities.format('OK! I will ping you in %d minutes to remind you about "%s"', time, msg);
			}
			else {
				formatted_msg = utilities.format('OK! I will ping you in %d minutes to remind you about something', time);
			}
			await interaction.reply({ content: formatted_msg, ephemeral: true });

			await wait(time * 59500);

			if (msg) {
				formatted_msg = utilities.format('It has been %d minutes, don\'t forget "%s"', time, msg);
			}
			else {
				formatted_msg = utilities.format('It has been %d minutes, you have been reminded!', time);
			}
			await interaction.followUp(bold(formatted_msg));
		}
	},
};