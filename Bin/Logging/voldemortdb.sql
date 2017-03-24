CREATE DATABASE  IF NOT EXISTS `voldemortdb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `voldemortdb`;
-- MySQL dump 10.13  Distrib 5.6.13, for Win32 (x86)
--
-- Host: localhost    Database: voldemortdb
-- ------------------------------------------------------
-- Server version	5.6.16

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
-- Table structure for table `cycle`
--

DROP TABLE IF EXISTS `cycle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cycle` (
  `idcycle` int(11) NOT NULL AUTO_INCREMENT,
  `cycle_time` int(11) NOT NULL,
  `date_start` varchar(50) NOT NULL,
  `time_start` varchar(50) NOT NULL,
  `date_end` varchar(50) NOT NULL,
  `time_end` varchar(50) NOT NULL,
  PRIMARY KEY (`idcycle`),
  UNIQUE KEY `idCycle_UNIQUE` (`idcycle`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cycle`
--

LOCK TABLES `cycle` WRITE;
/*!40000 ALTER TABLE `cycle` DISABLE KEYS */;
INSERT INTO `cycle` VALUES (1,0,'02-08-2017','14:30:50','02-08-2017','14:35:50'),(2,0,'03-26-2017','10:20:00','03-27-2017','10:25:00');
/*!40000 ALTER TABLE `cycle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flow`
--

DROP TABLE IF EXISTS `flow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flow` (
  `idflow` int(11) NOT NULL AUTO_INCREMENT,
  `idcycle` int(11) NOT NULL,
  `src_ip` varchar(45) NOT NULL,
  `dest_ip` varchar(45) NOT NULL,
  `protocol` varchar(45) NOT NULL,
  `service` varchar(45) NOT NULL,
  `packetflg` varchar(45) NOT NULL,
  `datasize` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`idflow`),
  UNIQUE KEY `idflow_UNIQUE` (`idflow`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flow`
--

LOCK TABLES `flow` WRITE;
/*!40000 ALTER TABLE `flow` DISABLE KEYS */;
INSERT INTO `flow` VALUES (1,1,'1.1.1.1','2.2.2.2','tcp','http','none',10,0),(2,1,'1.1.1.1','3.3.3.3','tcp','syn','syn-ack',50,0),(3,2,'1.1.1.1','2.2.2.2','icmp','echo-reply','none',25,0),(4,2,'2.2.2.2','3.3.3.3','tcp','syn','syn',65,0);
/*!40000 ALTER TABLE `flow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `threshold`
--

DROP TABLE IF EXISTS `threshold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `threshold` (
  `idthresh` int(11) NOT NULL AUTO_INCREMENT,
  `idcycle` int(11) NOT NULL,
  `old_tcp` float NOT NULL,
  `old_udp` float NOT NULL,
  `old_icmp` float NOT NULL,
  `new_tcp` float NOT NULL,
  `new_udp` float NOT NULL,
  `new_icmp` float NOT NULL,
  PRIMARY KEY (`idthresh`),
  UNIQUE KEY `idthresh_UNIQUE` (`idthresh`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threshold`
--

LOCK TABLES `threshold` WRITE;
/*!40000 ALTER TABLE `threshold` DISABLE KEYS */;
INSERT INTO `threshold` VALUES (1,2,50,20,30,60,20,20);
/*!40000 ALTER TABLE `threshold` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-24 14:20:18
