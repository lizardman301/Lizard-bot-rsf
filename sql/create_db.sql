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
  `channel_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`channel_id`)
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
  `setting_id` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `guild_id` bigint(20) unsigned NOT NULL,
  `prefix-lizard` varchar(1) NOT NULL DEFAULT '!',
  `botrole` bigint(20) unsigned NOT NULL DEFAULT 0,
  `challonge` VARCHAR(60) NOT NULL DEFAULT '',
  `disabled_list` VARCHAR(2000) NULL DEFAULT '',
  PRIMARY KEY (`setting_id`),
  KEY `guild_id` (`guild_id`),
  CONSTRAINT `guild_id_fk` FOREIGN KEY (`guild_id`) REFERENCES `guilds` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table lizardbot.channel_settings
CREATE TABLE IF NOT EXISTS `channel_settings` (
  `setting_id` BIGINT(20) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
  `channel_id` BIGINT(20) UNSIGNED NOT NULL,
  `tos` VARCHAR(380) NULL DEFAULT '',
  `round` VARCHAR(50) NULL DEFAULT '',
  `status` VARCHAR(1953) NULL DEFAULT 'Winner\'s Round {0} can play! Losers can play till top 8 losers side. If you have a bye Round {0}, Please Wait!',
  `stream` VARCHAR(2000) NULL DEFAULT 'There are no streams set for this channel',
  `bracket` VARCHAR(2000) NULL DEFAULT 'There is no bracket set for this channel',
  `pingtest` VARCHAR(2000) NULL DEFAULT 'Use <https://testmyspeed.onl/> for ping tests.',
  `seeding` VARCHAR(80) NULL DEFAULT '',
  PRIMARY KEY (`setting_id`),
  INDEX `channel_id` (`channel_id`),
  CONSTRAINT `channel_id_fk` FOREIGN KEY (`channel_id`) REFERENCES `channels` (`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table lizardbot.stats
CREATE TABLE IF NOT EXISTS `stats` (
  `stat_id` INT(3) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
  `command` VARCHAR(20) NOT NULL DEFAULT '',
  `used` INT(20) NOT NULL DEFAULT 1,
  PRIMARY KEY (`stat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;