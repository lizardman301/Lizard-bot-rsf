const { Client, Collection, Intents } = require('discord.js');
const fs = require('fs');
const path = require('path');
const utilities = require('util');

const { addStat, settingsExist } = require('./utilities/database/db_util');

const { token } = require('./secret.json');

// Create a new client instance
const intentions = new Intents(Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_BANS, Intents.FLAGS.GUILD_EMOJIS_AND_STICKERS, Intents.FLAGS.GUILD_INTEGRATIONS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS, Intents.FLAGS.GUILD_MESSAGE_TYPING);
intentions.add(Intents.FLAGS.GUILD_MEMBERS);

const client = new Client({ intents:  intentions });

client.commands = new Collection();
const commandFiles = fs.readdirSync(path.join(__dirname, 'commands')).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	client.commands.set(command.data.name, command);
}


function change_status() {
	const total = client.guilds.cache.size;
	let status = 'over %d server';

	if (total > 1) {
		status = status + 's!';
	}
	else {
		status = status + '!';
	}
	client.user.setActivity(utilities.format(status + ' | lizard-bot.com', total), { type: 'WATCHING' });
}

// When the client is ready, run this code (only once)
client.once('ready', () => {
	console.log(utilities.format('\nLogged in as %s', client.user.tag));
	console.log('-------------------------------');
	const guilds = client.guilds.cache.map(r => {return r;});
	for (let i = 0; i < guilds.length; i++) {
		console.log(utilities.format('Joined guild: %s', guilds[i]));
	}

	change_status();
	setInterval(change_status, 28800000);
});

client.on('interactionCreate', async interaction => {
	if (!interaction.isCommand()) return;

	const command = client.commands.get(interaction.commandName);

	if (!command) return;

	try {
		await settingsExist(interaction.guildId, interaction.channelId);
		await command.execute(interaction);
		await addStat(interaction.commandName);
	}
	catch (error) {
		console.error(error);
		return interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
	}
});

// Login to Discord with your client's token
client.login(token);