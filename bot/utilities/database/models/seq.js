const secrets = require('../../../secret.json');
const sequelize = require('sequelize');
const guildModel = require('./guild');
const guild_settingModel = require('./guild_setting');
const channelModel = require('./channel');
const channel_settingModel = require('./channel_setting');
const statsModel = require('./stats');

// This is our connection to the database
const seq = new sequelize({
	host: secrets.sql_host,
	port: secrets.sql_port,
	username: secrets.sql_user,
	password: secrets.sql_pw,
	database: secrets.sql_db,
	dialect: 'mariadb',
	dialectOptions: {
		supportBigNumbers: true,
		bigNumberStrings: true,
	},
	logging: false,
	pool: {
		max: 500,
		min: 0,
		idle: 5000,
		acquire: 1000000,
		evict: 5000,
		handleDisconnects: true,
	},
});

const guild = guildModel(seq, sequelize);
const guild_setting = guild_settingModel(seq, sequelize);
const channel = channelModel(seq, sequelize);
const channel_setting = channel_settingModel(seq, sequelize);
const stats = statsModel(seq, sequelize);

// Our connections between the tables
guild_setting.belongsTo(guild, { foreignKey: 'guild_id' });
channel_setting.belongsTo(channel, { foreignKey: 'channel_id' });

module.exports = {
	guild,
	guild_setting,
	channel,
	channel_setting,
	stats,
	seq,
};