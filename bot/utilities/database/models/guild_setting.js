// There's not much to this
// It's the guild_settings SQL table sequelized
module.exports = function(sequelize, DataTypes) {
	return sequelize.define('guild_setting', {
		setting_id: {
			type: DataTypes.BIGINT(20).ZEROFILL.UNSIGNED,
			allowNull: false,
			primaryKey: true,
			autoIncrement: true,
		},
		guild_id: {
			type: DataTypes.BIGINT(20).UNSIGNED,
			allowNull: false,
			references: {
				model: 'guild',
				key: 'guild_id',
			},
		},
		prefixLizard: {
			type: DataTypes.STRING(1),
			allowNull: false,
			defaultValue: '!',
			field: 'prefix-lizard',
		},
		botrole: {
			type: DataTypes.BIGINT(20).UNSIGNED,
			allowNull: false,
			defaultValue: 0,
		},
		challonge: {
			type: DataTypes.STRING(60),
			allowNull: false,
			defaultValue: '',
		},
		disabled_list: {
			type: DataTypes.STRING(2000),
			allowNull: false,
			defaultValue: '[""]',
		},
	},
	{ timestamps: false });
};