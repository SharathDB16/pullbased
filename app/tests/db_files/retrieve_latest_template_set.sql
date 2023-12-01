-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: database    Database: provisioning_store_test
-- ------------------------------------------------------
-- Server version	5.7.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `provisioning_store_test`
--

/*!40000 DROP DATABASE IF EXISTS `provisioning_store_test`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `provisioning_store_test` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `provisioning_store_test`;

--
-- Table structure for table `config_template`
--

DROP TABLE IF EXISTS `config_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config_template` (
  `id` mediumint(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  `owner` varchar(45) DEFAULT NULL,
  `group` varchar(45) DEFAULT NULL,
  `permissions` int(11) NOT NULL,
  `path` varchar(645) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config_template`
--

LOCK TABLES `config_template` WRITE;
/*!40000 ALTER TABLE `config_template` DISABLE KEYS */;
INSERT INTO `config_template` VALUES (1,'create_test1','This is the first created config template','new-noc','new-root',644,'/etc/memcache/memcache-2.ini','2021-05-21 14:21:28','2021-05-21 14:21:28'),(2,'create_test2','This is the 2nd created config template','new-noc','new-root',644,'/etc/memcache/memcache-3.ini','2021-05-21 14:21:28','2021-05-21 14:21:28');
/*!40000 ALTER TABLE `config_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `config_template_version`
--

DROP TABLE IF EXISTS `config_template_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config_template_version` (
  `id` mediumint(4) NOT NULL AUTO_INCREMENT,
  `config_template_id` mediumint(4) NOT NULL,
  `comment` varchar(45) NOT NULL,
  `version_no` decimal(10,2) NOT NULL,
  `template_file` blob,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_config_template_version_2_idx` (`config_template_id`),
  CONSTRAINT `fk_config_template_version_1` FOREIGN KEY (`config_template_id`) REFERENCES `config_template` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config_template_version`
--

LOCK TABLES `config_template_version` WRITE;
/*!40000 ALTER TABLE `config_template_version` DISABLE KEYS */;
INSERT INTO `config_template_version` VALUES (1,1,'First version for template id 1',0.01,'This is the first uploaded file.\nThis file will be uploaded to template ids 1 and 2','2021-05-21 14:21:28'),(2,2,'First version for template id 2',0.01,'This is the first uploaded file.\nThis file will be uploaded to template ids 1 and 2','2021-05-21 14:21:29'),(3,1,'Second version for template id 1',0.02,'This is the 2nd uploaded file.\nThis file will be attached to template id 1 only','2021-05-21 14:21:29');
/*!40000 ALTER TABLE `config_template_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `config_variable`
--

DROP TABLE IF EXISTS `config_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config_variable` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config_variable`
--

LOCK TABLES `config_variable` WRITE;
/*!40000 ALTER TABLE `config_variable` DISABLE KEYS */;
/*!40000 ALTER TABLE `config_variable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `edge_config_variable`
--

DROP TABLE IF EXISTS `edge_config_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `edge_config_variable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `edge_type_id` tinyint(3) NOT NULL,
  `config_variable_id` mediumint(4) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_edge_config_variable_1_idx` (`edge_type_id`),
  KEY `fk_edge_config_variable_2_idx` (`config_variable_id`),
  CONSTRAINT `fk_edge_config_variable_1` FOREIGN KEY (`edge_type_id`) REFERENCES `edge_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_edge_config_variable_2` FOREIGN KEY (`config_variable_id`) REFERENCES `config_variable` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edge_config_variable`
--

LOCK TABLES `edge_config_variable` WRITE;
/*!40000 ALTER TABLE `edge_config_variable` DISABLE KEYS */;
/*!40000 ALTER TABLE `edge_config_variable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `edge_package`
--

DROP TABLE IF EXISTS `edge_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `edge_package` (
  `id` mediumint(4) NOT NULL AUTO_INCREMENT,
  `edge_type_id` tinyint(3) NOT NULL,
  `master_package_id` mediumint(4) NOT NULL,
  `status` mediumint(4) NOT NULL DEFAULT '1',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_edge_template_mapping_1_idx` (`edge_type_id`),
  KEY `fk_edge_package_1_idx` (`master_package_id`),
  CONSTRAINT `fk_edge_package_1` FOREIGN KEY (`master_package_id`) REFERENCES `master_package` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_edge_package_2` FOREIGN KEY (`edge_type_id`) REFERENCES `edge_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edge_package`
--

LOCK TABLES `edge_package` WRITE;
/*!40000 ALTER TABLE `edge_package` DISABLE KEYS */;
INSERT INTO `edge_package` VALUES (1,1,1,1,'2021-05-22 03:25:06','2021-05-22 03:25:06'),(2,1,2,1,'2021-05-22 03:25:12','2021-05-22 03:25:12'),(3,2,2,1,'2021-05-22 03:25:55','2021-05-22 03:25:55'),(4,5,1,1,'2021-05-22 06:01:13','2021-05-22 06:01:13');
/*!40000 ALTER TABLE `edge_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `edge_telemetry_code`
--

DROP TABLE IF EXISTS `edge_telemetry_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `edge_telemetry_code` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edge_telemetry_code`
--

LOCK TABLES `edge_telemetry_code` WRITE;
/*!40000 ALTER TABLE `edge_telemetry_code` DISABLE KEYS */;
INSERT INTO `edge_telemetry_code` VALUES (1,'package_download_success'),(2,'package_download_fail'),(3,'package_consumption_success'),(4,'package_consumption_fail');
/*!40000 ALTER TABLE `edge_telemetry_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `edge_telemetry_info`
--

DROP TABLE IF EXISTS `edge_telemetry_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `edge_telemetry_info` (
  `id` mediumint(4) NOT NULL AUTO_INCREMENT,
  `code_id` tinyint(3) NOT NULL,
  `edge_id` varchar(255) NOT NULL,
  `package_name` varchar(255) NOT NULL,
  `template_set_version` decimal(10,2) NOT NULL,
  `report_status` longtext NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `code_id` (`code_id`),
  CONSTRAINT `edge_telemetry_info_ibfk_1` FOREIGN KEY (`code_id`) REFERENCES `edge_telemetry_code` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edge_telemetry_info`
--

LOCK TABLES `edge_telemetry_info` WRITE;
/*!40000 ALTER TABLE `edge_telemetry_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `edge_telemetry_info` ENABLE KEYS */;
UNLOCK TABLES;

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
  `pre_gen_script_file` blob,
  `post_gen_script_file` blob,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edge_type`
--

LOCK TABLES `edge_type` WRITE;
/*!40000 ALTER TABLE `edge_type` DISABLE KEYS */;
INSERT INTO `edge_type` VALUES (1,'static','static','default','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"/opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n','2019-01-29 06:24:33','2019-05-30 13:23:51'),(2,'mid','mid','default','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"//opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n','2019-01-29 06:24:33','2019-05-30 13:23:51'),(3,'mobile','mobile','default','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"/opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n','2019-01-29 06:24:33','2019-05-30 13:23:51'),(4,'kontron_metro','mobile','kontronmetro','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"//opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n','2019-01-29 06:24:33','2019-05-30 13:23:51'),(5,'c2cbus','mobile','c2cbus','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"//opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n','2019-01-29 06:24:33','2019-05-30 13:23:51'),(6,'pseudotp','mid','parent_pseudo_tp','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"//opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n','2019-03-04 06:42:31','2019-05-30 13:23:51'),(7,'pseudotp','mid','child_pseudo_tp','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"//opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n','2019-03-04 06:42:40','2019-05-30 13:23:51'),(8,'nuc','static','nuc','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"/opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n','2019-06-13 10:09:25','2019-06-13 10:09:25'),(9,'ct_static','static','ct_static','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"/opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n\n','2020-01-06 17:56:08','2020-01-06 17:56:14'),(10,'railtel_pilot_ec','mobile','railtel_pilot_ec','#!/bin/bash\n\necho \"======================TAKING BACKUP============================\"\necho \"Executing pre_gen script\"\nsudo rsync -avP --files-from=template_path.txt / \"/opt/sugarbox/provisioningagent/config/backup/etc_baks\"\necho \"Executed pre_gen script\"\necho \"======================BACKUP DONE==============================\"\n','#!/bin/bash\n\necho \"===============================================================\"\necho \"Executing post_gen script\"\nif [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then\n	echo \"Restoring backup\"\n	sudo rsync -aAvr /opt/sugarbox/provisioningagent/config/backup/etc_baks/etc/* /etc/\n	sudo rm -fR /opt/sugarbox/provisioningagent/config/backup/etc_baks\nfi\necho \"Executed post_gen script\"\necho \"===============================================================\"\n\n','2020-03-11 07:30:57','2020-03-11 07:32:21');
/*!40000 ALTER TABLE `edge_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_package`
--

DROP TABLE IF EXISTS `master_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_package` (
  `id` mediumint(4) NOT NULL AUTO_INCREMENT,
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_package`
--

LOCK TABLES `master_package` WRITE;
/*!40000 ALTER TABLE `master_package` DISABLE KEYS */;
INSERT INTO `master_package` VALUES (1,'Updated master name','The master name was updated for id 1',NULL,NULL,NULL,NULL,'This is an uninstall file for master teplate id 1 after it is updated',1,NULL,'This is the prescript file for mater template id 1 after it is updated','This is the post script file for master template id 1, after it is updated','2021-05-21 14:21:29','2021-05-21 14:21:29'),(2,'Second Master package','This is the second master package created',NULL,NULL,NULL,NULL,'This is an uninstall file for master teplate id 2',1,NULL,'This is the prescript file for mater template id 2','This is the post script file for master template id 2','2021-05-21 14:21:29','2021-05-21 14:21:29');
/*!40000 ALTER TABLE `master_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_package_config_template`
--

DROP TABLE IF EXISTS `master_package_config_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_package_config_template` (
  `id` mediumint(4) NOT NULL AUTO_INCREMENT,
  `master_package_id` mediumint(4) NOT NULL,
  `config_template_id` mediumint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_master_package_config_template_1_idx` (`master_package_id`),
  KEY `fk_master_package_config_template_2_idx` (`config_template_id`),
  CONSTRAINT `fk_master_package_config_template_1` FOREIGN KEY (`master_package_id`) REFERENCES `master_package` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_master_package_config_template_2` FOREIGN KEY (`config_template_id`) REFERENCES `config_template` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_package_config_template`
--

LOCK TABLES `master_package_config_template` WRITE;
/*!40000 ALTER TABLE `master_package_config_template` DISABLE KEYS */;
INSERT INTO `master_package_config_template` VALUES (1,1,1),(2,1,2),(6,2,1);
/*!40000 ALTER TABLE `master_package_config_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `switch_package`
--

DROP TABLE IF EXISTS `switch_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `switch_package` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `switch_type_id` tinyint(3) NOT NULL,
  `master_package_id` mediumint(4) NOT NULL,
  `edge_type_id` tinyint(3) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_switch_package_1_idx` (`switch_type_id`),
  KEY `fk_switch_package_2_idx` (`edge_type_id`),
  KEY `fk_switch_package_3_idx` (`master_package_id`),
  CONSTRAINT `fk_switch_package_1` FOREIGN KEY (`switch_type_id`) REFERENCES `switch_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_switch_package_2` FOREIGN KEY (`edge_type_id`) REFERENCES `edge_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_switch_package_3` FOREIGN KEY (`master_package_id`) REFERENCES `master_package` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `switch_package`
--

LOCK TABLES `switch_package` WRITE;
/*!40000 ALTER TABLE `switch_package` DISABLE KEYS */;
/*!40000 ALTER TABLE `switch_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `switch_type`
--

DROP TABLE IF EXISTS `switch_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `switch_type` (
  `id` tinyint(3) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `switch_type`
--

LOCK TABLES `switch_type` WRITE;
/*!40000 ALTER TABLE `switch_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `switch_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `template_config_variable`
--

DROP TABLE IF EXISTS `template_config_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `template_config_variable` (
  `id` mediumint(4) NOT NULL AUTO_INCREMENT,
  `config_template_id` mediumint(4) NOT NULL,
  `config_variable_id` mediumint(4) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_template_config_variable_1_idx` (`config_template_id`),
  KEY `fk_template_config_variable_2_idx` (`config_variable_id`),
  CONSTRAINT `fk_template_config_variable_1` FOREIGN KEY (`config_template_id`) REFERENCES `config_template` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_template_config_variable_2` FOREIGN KEY (`config_variable_id`) REFERENCES `config_variable` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `template_config_variable`
--

LOCK TABLES `template_config_variable` WRITE;
/*!40000 ALTER TABLE `template_config_variable` DISABLE KEYS */;
/*!40000 ALTER TABLE `template_config_variable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `template_set_version`
--

DROP TABLE IF EXISTS `template_set_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `template_set_version` (
  `id` mediumint(4) NOT NULL AUTO_INCREMENT,
  `set_version_no` decimal(10,2) NOT NULL,
  `config_template_id` mediumint(4) NOT NULL,
  `template_version_no` decimal(10,2) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_template_set_version_2_idx` (`config_template_id`),
  CONSTRAINT `fk_template_set_version_1` FOREIGN KEY (`config_template_id`) REFERENCES `config_template` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `template_set_version`
--

LOCK TABLES `template_set_version` WRITE;
/*!40000 ALTER TABLE `template_set_version` DISABLE KEYS */;
INSERT INTO `template_set_version` VALUES (1,0.01,1,0.01,'2021-05-21 14:21:28'),(2,0.02,2,0.01,'2021-05-21 14:21:29'),(3,0.03,1,0.02,'2021-05-21 14:21:29');
/*!40000 ALTER TABLE `template_set_version` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-22 21:39:14
