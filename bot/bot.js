const { Client, Intents } = require('discord.js');
const util = require('util');
// const secrets = require('./secret.json');
const db_util = require('./database/db_util');

/* try {
	db_util.settingsExist(745298426979418206n, 745298689840513106n);
}
catch (err) {
	console.err('Failed to created settings');
} */

db_util.setSetting('guild', 'challonge', 745298426979418205n, 'ritfgc');

// Create a new client instance
const intentions = new Intents(Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_BANS, Intents.FLAGS.GUILD_EMOJIS_AND_STICKERS, Intents.FLAGS.GUILD_INTEGRATIONS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS, Intents.FLAGS.GUILD_MESSAGE_TYPING);
intentions.add(Intents.FLAGS.GUILD_MEMBERS);
const client = new Client({ intents:  intentions });

// When the client is ready, run this code (only once)
client.once('ready', () => {
	console.log(util.format('\nLogged in as %s', client.user.tag));
	console.log('-------------------------------');
	const guilds = client.guilds.cache.map(r => {return r;});
	for (let i = 0; i < guilds.length; i++) {
		console.log(util.format('Joined guild: %s', guilds[i]));
	}
});


client.on('interactionCreate', async interaction => {
	if (!interaction.isCommand()) return;

	const command = client.commands.get(interaction.commandName);

	if (!command) return;

	try {
		await command.execute(interaction);
	}
	catch (error) {
		console.error(error);
		return interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
	}
});

// Login to Discord with your client's token
// client.login(secrets.token);