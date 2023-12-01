-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: provisioning_store
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.16.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `config_template`
--

DROP TABLE IF EXISTS `config_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config_template` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `master_package_id` tinyint(3) NOT NULL,
  `name` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  `owner` varchar(45) NOT NULL,
  `group` varchar(45) NOT NULL,
  `permissions` int(11) NOT NULL,
  `path` varchar(645) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path_UNIQUE` (`path`),
  KEY `fk_config_template_1_idx` (`master_package_id`),
  CONSTRAINT `fk_config_template_1` FOREIGN KEY (`master_package_id`) REFERENCES `master_package` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `config_template_version`
--

DROP TABLE IF EXISTS `config_template_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config_template_version` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `master_package_id` tinyint(3) NOT NULL,
  `config_template_id` tinyint(3) NOT NULL,
  `comment` varchar(45) NOT NULL,
  `version_no` decimal(10,2) NOT NULL,
  `template_file` blob,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_config_template_version_1_idx` (`master_package_id`),
  KEY `fk_config_template_version_2_idx` (`config_template_id`),
  CONSTRAINT `fk_config_template_version_1` FOREIGN KEY (`master_package_id`) REFERENCES `master_package` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_config_template_version_2` FOREIGN KEY (`config_template_id`) REFERENCES `config_template` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `config_variable`
--

DROP TABLE IF EXISTS `config_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config_variable` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `edge_config_variable`
--

DROP TABLE IF EXISTS `edge_config_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `edge_config_variable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `edge_type_id` tinyint(3) NOT NULL,
  `config_variable_id` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_edge_config_variable_1_idx` (`edge_type_id`),
  KEY `fk_edge_config_variable_2_idx` (`config_variable_id`),
  CONSTRAINT `fk_edge_config_variable_1` FOREIGN KEY (`edge_type_id`) REFERENCES `edge_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_edge_config_variable_2` FOREIGN KEY (`config_variable_id`) REFERENCES `config_variable` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `edge_package`
--

DROP TABLE IF EXISTS `edge_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `edge_package` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `edge_type_id` tinyint(3) NOT NULL,
  `master_package_id` tinyint(3) NOT NULL,
  `status` tinyint(3) NOT NULL DEFAULT '1',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_edge_template_mapping_1_idx` (`edge_type_id`),
  KEY `fk_edge_package_1_idx` (`master_package_id`),
  CONSTRAINT `fk_edge_package_1` FOREIGN KEY (`master_package_id`) REFERENCES `master_package` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_edge_package_2` FOREIGN KEY (`edge_type_id`) REFERENCES `edge_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `edge_type`
--

DROP TABLE IF EXISTS `edge_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `edge_type` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `sub_type` varchar(255) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edge_type`
--

LOCK TABLES `edge_type` WRITE;
/*!40000 ALTER TABLE `edge_type` DISABLE KEYS */;
INSERT INTO `edge_type` VALUES (1,'static','static','default','2019-01-29 06:24:33','2019-01-29 06:24:33'),(2,'mid','mid','default','2019-01-29 06:24:33','2019-01-29 06:24:33'),(3,'mobile','mobile','default','2019-01-29 06:24:33','2019-01-29 06:24:33'),(4,'kontron_metro','mobile','kontronmetro','2019-01-29 06:24:33','2019-01-29 06:24:33'),(5,'c2cbus','mobile','c2cbus','2019-01-29 06:24:33','2019-01-29 06:24:33');
/*!40000 ALTER TABLE `edge_type` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `master_package`
--

DROP TABLE IF EXISTS `master_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_package` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `path` varchar(255) DEFAULT NULL,
  `user` varchar(255) DEFAULT NULL,
  `group` varchar(255) DEFAULT NULL,
  `permission` varchar(255) DEFAULT NULL,
  `uninstall_file` blob NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `execution_sequence` int(11) DEFAULT NULL,
  `pre_script_file` blob NOT NULL,
  `post_script_file` blob NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `master_package_config_template`
--

DROP TABLE IF EXISTS `master_package_config_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_package_config_template` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `master_package_id` tinyint(3) NOT NULL,
  `config_template_id` tinyint(3) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_master_package_config_template_1_idx` (`master_package_id`),
  KEY `fk_master_package_config_template_2_idx` (`config_template_id`),
  CONSTRAINT `fk_master_package_config_template_1` FOREIGN KEY (`master_package_id`) REFERENCES `master_package` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_master_package_config_template_2` FOREIGN KEY (`config_template_id`) REFERENCES `config_template` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `template_config_variable`
--

DROP TABLE IF EXISTS `template_config_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `template_config_variable` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `config_template_id` tinyint(3) NOT NULL,
  `config_variable_id` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_template_config_variable_1_idx` (`config_template_id`),
  KEY `fk_template_config_variable_2_idx` (`config_variable_id`),
  CONSTRAINT `fk_template_config_variable_1` FOREIGN KEY (`config_template_id`) REFERENCES `config_template` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_template_config_variable_2` FOREIGN KEY (`config_variable_id`) REFERENCES `config_variable` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `template_set_version`
--

DROP TABLE IF EXISTS `template_set_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `template_set_version` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `set_version_no` decimal(10,2) NOT NULL,
  `master_package_id` tinyint(3) NOT NULL,
  `config_template_id` tinyint(3) NOT NULL,
  `template_version_no` decimal(10,2) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_template_set_version_1_idx` (`master_package_id`),
  KEY `fk_template_set_version_2_idx` (`config_template_id`),
  CONSTRAINT `fk_template_set_version_1` FOREIGN KEY (`master_package_id`) REFERENCES `master_package` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_template_set_version_2` FOREIGN KEY (`config_template_id`) REFERENCES `config_template` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-22 11:46:55