// There's not much to this
// It's the channel_settings SQL table sequelized
module.exports = function(sequelize, DataTypes) {
	return sequelize.define('channel_setting', {
		setting_id: {
			type: DataTypes.BIGINT(20).ZEROFILL.UNSIGNED,
			allowNull: false,
			primaryKey: true,
			autoIncrement: true,
		},
		channel_id: {
			type: DataTypes.BIGINT(20).UNSIGNED,
			allowNull: false,
			references: {
				model: 'channel',
				key: 'channel_id',
			},
		},
		tos: {
			type: DataTypes.STRING(380),
			defaultValue: '',
		},
		round: {
			type: DataTypes.STRING(50),
			defaultValue: '',
		},
		status: {
			type: DataTypes.STRING(1953),
			defaultValue: 'Winner\'s Round {0} can play! Losers can play till top 8 losers side. If you have a bye Round {0}, Please Wait!',
		},
		stream: {
			type: DataTypes.STRING(2000),
			defaultValue: 'There are no streams set for this channel',
		},
		bracket: {
			type: DataTypes.STRING(2000),
			defaultValue: 'There is no bracket set for this channel',
		},
		pingtest: {
			type: DataTypes.STRING(2000),
			defaultValue: 'Use <https://testmyspeed.onl/> for ping tests.',
		},
		seeding: {
			type: DataTypes.STRING(80),
			defaultValue: '',
		},
		lobby: {
			type: DataTypes.STRING(2000),
			defaultValue: 'There is no lobby information set for this channel.',
		},
	},
	{ timestamps: false });
};