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
-- Dumping structure for table lizardbot.settings
CREATE TABLE IF NOT EXISTS `settings` (
  `setting_id` bigint(20) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `chan_id` bigint(20) unsigned NOT NULL,
  `round` int(4) unsigned NOT NULL DEFAULT 0,
  `round_msg` varchar(2000) DEFAULT "Winner's Round {0} can play! Losers can play till top 8 losers side. If you have a bye Round {0}, Please Wait!",
  `status` varchar(2000) DEFAULT "Winner's side Round {0} is allowed to play! Losers can play till top 8.",
  `stream` varchar(2000) DEFAULT 'There are no streams set for this channel',
  PRIMARY KEY (`setting_id`),
  KEY `chan_id` (`chan_id`),
  CONSTRAINT `chan_id_fk` FOREIGN KEY (`chan_id`) REFERENCES `channels` (`chan_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
