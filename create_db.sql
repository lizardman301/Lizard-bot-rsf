-- --------------------------------------------------------
-- Server version:               10.3.10-MariaDB - mariadb.org binary distribution
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for lizardbot
CREATE DATABASE IF NOT EXISTS `lizardbot` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `lizardbot`;

-- Dumping structure for table lizardbot.channels
CREATE TABLE IF NOT EXISTS `channels` (
  `chan_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`chan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table lizardbot.guilds
CREATE TABLE IF NOT EXISTS `guilds` (
  `guild_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table lizardbot.guild_settings
CREATE TABLE IF NOT EXISTS `guild_settings` (
  `g_setting_id` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `guild_id` bigint(20) unsigned NOT NULL,
  `prefix` varchar(1) NOT NULL DEFAULT '!',
  `bot_role` bigint(20) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`g_setting_id`),
  KEY `guild_id` (`guild_id`),
  CONSTRAINT `guild_id_fk` FOREIGN KEY (`guild_id`) REFERENCES `guilds` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table lizardbot.settings
CREATE TABLE IF NOT EXISTS `channel_settings` (
  `setting_id` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `chan_id` bigint(20) unsigned NOT NULL,
  `tos` varchar(380) DEFAULT '',
  `round` varchar(50) DEFAULT '',
  `status` varchar(1953) DEFAULT 'Winner''s Round {0} can play! Losers can play till top 8 losers side. If you have a bye Round {0}, Please Wait!',
  `stream` varchar(2000) DEFAULT 'There are no streams set for this channel',
  PRIMARY KEY (`setting_id`),
  KEY `chan_id` (`chan_id`),
  CONSTRAINT `chan_id_fk` FOREIGN KEY (`chan_id`) REFERENCES `channels` (`chan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
