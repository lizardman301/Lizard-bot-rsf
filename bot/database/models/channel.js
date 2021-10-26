// There's not much to this
// It's the channels SQL table sequelized
module.exports = function(sequelize, DataTypes) {
	return sequelize.define('channel', {
		channel_id: {
			type: DataTypes.BIGINT(20).UNSIGNED,
			allowNull: false,
			primaryKey: true,
		},
	},
	{ timestamps: false });
};