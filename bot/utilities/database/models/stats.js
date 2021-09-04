// There's not much to this
// It's the stats SQL table sequelized
module.exports = function(sequelize, DataTypes) {
	return sequelize.define('stats', {
		stat_id: {
			type: DataTypes.INTEGER(3).ZEROFILL.UNSIGNED,
			allowNull: false,
			primaryKey: true,
			autoIncrement: true,
		},
		command: {
			type: DataTypes.STRING(20),
			allowNull: false,
			defaultValue: '',
		},
		used: {
			type: DataTypes.INTEGER(20),
			allowNull: false,
			defaultValue: 1,
		},
	},
	{ timestamps: false });
};