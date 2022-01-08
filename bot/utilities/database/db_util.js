const sequelize = require('sequelize');
const { guild, guild_setting, channel, channel_setting, seq, stats } = require('./models/seq');
const model_references = {
	'guild': [guild, guild_setting],
	'channel': [channel, channel_setting],
};

exports.settingsExist = async function(guild_id, chan_id) {
	const levels = [[guild, guild_setting], [channel, channel_setting]];
	levels.forEach(async level => {
		const id = level[0].name === 'guild' ? guild_id : chan_id;

		level.forEach(async model => {
			const sql = 'INSERT IGNORE INTO `' + model.name + 's` (`' + level[0].name + '_id`) VALUES ((SELECT CAST(? AS INT)))';

			await seq.query(sql, {
				replacements: [String(id)],
			});
		});
	});
};

exports.getSetting = async function(level, setting, id) {
	const model = model_references[level][1];

	const res = await model.findAll({
		attributes: [setting],
		where: sequelize.where(sequelize.col(level + '_id'), {
			[sequelize.Op.eq]: String(id),
		}),
	});
	return res[0].dataValues[setting];
};

exports.setSetting = async function(level, setting, id, data, options = {}) {
	if (Object.keys(options).includes('commandChannel')) {
		id = options['commandChannel'];
	}
	const sql = 'UPDATE `' + level + '_settings` SET `' + setting + '` = ? WHERE `' + level + '_id` = (SELECT CAST(? AS INT))';
	await seq.query(sql, {
		replacements: [data, String(id)],
	});
};

exports.addStat = async function(command) {
	const res = await stats.findAll({
		attributes: ['used'],
		where: sequelize.where(sequelize.col('command'), {
			[sequelize.Op.eq]: command,
		}),
	});

	if (res.length > 0) {
		await stats.update({
			used: res[0].dataValues['used'] + 1,
		},
		{
			where: {
				command: command,
			},
		});
	}
	else {
		await stats.create({
			command: command,
		});
	}
};

exports.readStat = async function(command) {
	let sql = '';

	if (command) {
		sql = 'SELECT command, used FROM stats WHERE command = ?';
		await seq.query(sql, {
			replacements: command,
		});
	}
	else {
		sql = 'SELECT command, used FROM stats';
	}
};