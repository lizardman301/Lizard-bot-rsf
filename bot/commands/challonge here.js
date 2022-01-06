const { SlashCommandBuilder } = require('@discordjs/builders');
const axios = require('axios');
const { bold } = require('../utilities/utilities');
const { start_challonge } = require('../utilities/chal_util');
const secrets = require('../secret.json');

const baseUrl = 'https://api.challonge.com/v1/tournaments/';

module.exports = {
	data: new SlashCommandBuilder()
		.setName('challonge-here')
		.addStringOption(option => option.setName('user').setDescription('User to check in').setRequired(true))
		.setDescription('Placeholder text'),
	async execute(interaction) {
		const user_to_checkin = interaction.options.getString('user');
		const here_parts = {};
		await interaction.deferReply();

		// eslint-disable-next-line no-unused-vars
		const [parts, tourUrl] = await start_challonge(interaction.channelId, interaction.guildId);

		parts.forEach(part => {
			here_parts[part['participant']['display_name'].toLowerCase()] = part['participant']['id'];
		});

		let checkin_id;
		try {
			checkin_id = here_parts[user_to_checkin.toLowerCase()];
		}
		catch (err) {
			interaction.editReply({ content:  'Lizard-BOT cannot find ' + bold(user_to_checkin) + ' in the tournament', ephemeral: true });
			checkin_id = '';
		}

		if (checkin_id) {
			try {
				await axios.post(baseUrl + tourUrl + '/participants/' + checkin_id + '/check_in.json', {}, {
					headers: {
						'User-Agent':'Lizard-BOT',
					},
					auth: {
						username: secrets.chal_user,
						password: secrets.api_key,
					},
				});
				interaction.editReply('Checked in: ' + bold(user_to_checkin));
			}
			catch (err) {
				interaction.editReply({ content:  'Challonge Here Error', ephemeral: true });
				console.log(err);
				if (err.response.status === 401) {
					console.log(bold('Challonge') + ': Lizard-BOT does not have access to that tournament');
				}
				else if (err.response.status === 422) {
					console.log(bold('Challonge') + ': The check-in window hasn\'t started or is over for the tournament');
				}
				else {
					console.log(bold('Challonge') + 'Unknown Challonge error for <' + err.config.url + '> while checking in: ' + user_to_checkin);
				}
			}
		}
	},
};