-- MySQL dump 10.13  Distrib 5.7.33, for Win64 (x86_64)
--
-- Host: localhost    Database: MyProjectOne
-- ------------------------------------------------------
-- Server version	5.5.5-10.3.27-MariaDB-0+deb10u1

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
-- Table structure for table `Actie`
--

DROP TABLE IF EXISTS `Actie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Actie` (
  `ActieID` int(11) NOT NULL,
  `Beschrijving` varchar(145) DEFAULT NULL,
  PRIMARY KEY (`ActieID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Actie`
--

LOCK TABLES `Actie` WRITE;
/*!40000 ALTER TABLE `Actie` DISABLE KEYS */;
INSERT INTO `Actie` VALUES (1,'Waterniveau controleren in de grote bak'),(2,'Waterniveau controleren in de kleine bak'),(3,'Hoeveelheid voer controleren in de kleine bak'),(4,'Controle aanwezigheid hond bij bak met water'),(5,'Controle aanwezigheid hond bij bak met voer'),(6,'Voer aanvullen'),(7,'Water aanvullen');
/*!40000 ALTER TABLE `Actie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Device`
--

DROP TABLE IF EXISTS `Device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Device` (
  `DeviceID` int(11) NOT NULL,
  `Naam` varchar(45) DEFAULT NULL,
  `Beschrijving` varchar(45) DEFAULT NULL,
  `Type` varchar(45) DEFAULT NULL,
  `Aankoopkost` float DEFAULT NULL,
  `Meeteenheid` varchar(45) DEFAULT NULL,
  `Status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`DeviceID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Device`
--

LOCK TABLES `Device` WRITE;
/*!40000 ALTER TABLE `Device` DISABLE KEYS */;
INSERT INTO `Device` VALUES (1,'Water level sensor','Water level sensor voor grote bak','Sensor',15.1,'ml',0),(2,'Force sensing resistor','Force sensing resistor voor water','Sensor',13.11,'g',0),(3,'Force sensing resistor','Force sensing resistor voor voer','Sensor',13.11,'g',0),(4,'Distance measuring sensor','Distance measuring sensor voor voer','Sensor',6.31,'null',0),(5,'Distance measuring sensor','Distance measuring sensor voor water','Sensor',6.31,'null',0),(6,'Stepper motor','Stepper motor voor aanvulling voer','Actuator',19.33,'null',0),(7,'Waterpomp','Stepper motor voor aanvulling water','Actuator',19.33,'null',0);
/*!40000 ALTER TABLE `Device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Historiek`
--

DROP TABLE IF EXISTS `Historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Historiek` (
  `Volgnummer` int(11) NOT NULL,
  `DeviceID` int(11) NOT NULL,
  `ActieID` int(11) NOT NULL,
  `Actiedatum` datetime DEFAULT NULL,
  `Waarde` float DEFAULT NULL,
  PRIMARY KEY (`Volgnummer`),
  KEY `fk_Historiek_Device_idx` (`DeviceID`),
  KEY `fk_Historiek_Actie1_idx` (`ActieID`),
  CONSTRAINT `fk_Historiek_Actie1` FOREIGN KEY (`ActieID`) REFERENCES `Actie` (`ActieID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Historiek_Device` FOREIGN KEY (`DeviceID`) REFERENCES `Device` (`DeviceID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Historiek`
--

LOCK TABLES `Historiek` WRITE;
/*!40000 ALTER TABLE `Historiek` DISABLE KEYS */;
INSERT INTO `Historiek` VALUES (1,1,2,'2021-05-23 11:12:00',100),(2,1,2,'2021-05-23 11:22:00',150),(3,1,2,'2021-05-23 11:54:00',150),(4,1,2,'2021-05-23 12:12:00',120),(5,1,2,'2021-05-23 13:44:00',120),(6,1,2,'2021-05-23 14:12:00',130),(7,1,2,'2021-05-23 14:54:00',200),(8,6,6,'2021-05-23 15:12:00',NULL),(9,7,7,'2021-05-23 15:20:00',NULL),(10,7,7,'2021-05-23 16:12:00',NULL),(11,7,7,'2021-05-23 16:10:00',NULL),(12,7,7,'2021-05-23 16:15:00',NULL),(13,2,1,'2021-05-23 16:20:00',103),(14,1,2,'2021-05-23 16:33:00',92),(15,3,4,'2021-05-23 16:40:00',102),(16,3,4,'2021-05-23 16:55:00',67),(17,3,4,'2021-05-23 17:12:00',5),(18,7,7,'2021-05-23 17:33:00',NULL),(19,3,4,'2021-05-23 18:10:00',150),(20,3,4,'2021-05-23 20:10:00',12),(21,3,4,'2021-05-23 20:30:00',90),(22,3,4,'2021-05-23 20:55:00',54),(23,3,4,'2021-05-23 21:05:00',10),(24,7,7,'2021-05-23 21:20:00',NULL),(25,3,4,'2021-05-24 08:10:00',150),(26,3,4,'2021-05-24 08:15:00',90),(27,3,4,'2021-05-24 08:20:00',45),(28,3,4,'2021-05-24 09:30:00',12),(29,7,7,'2021-05-24 10:10:00',NULL),(30,3,4,'2021-05-24 10:44:00',150),(31,6,6,'2021-05-24 10:59:00',NULL),(32,1,2,'2021-05-24 11:10:00',200),(33,1,2,'2021-05-24 12:10:00',172),(34,1,2,'2021-05-24 12:25:00',154),(35,1,2,'2021-05-24 12:45:00',131),(36,1,2,'2021-05-24 13:43:00',93),(37,1,2,'2021-05-24 13:55:00',11),(38,6,6,'2021-05-24 14:10:00',NULL),(39,1,2,'2021-05-24 14:39:00',200),(40,1,2,'2021-05-24 15:10:00',90),(41,1,2,'2021-05-24 16:10:00',23),(42,7,7,'2021-05-24 17:33:00',NULL),(43,3,4,'2021-05-24 18:13:00',150),(44,3,4,'2021-05-24 18:19:00',21),(45,6,6,'2021-05-24 19:22:00',NULL),(46,1,2,'2021-05-24 19:55:00',200),(47,1,2,'2021-05-24 20:10:00',189),(48,1,2,'2021-05-24 20:44:00',143),(49,1,2,'2021-05-24 21:10:00',12),(50,7,7,'2021-05-24 22:01:00',NULL);
/*!40000 ALTER TABLE `Historiek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Voederschema`
--

DROP TABLE IF EXISTS `Voederschema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Voederschema` (
  `Volgnr` int(11) NOT NULL AUTO_INCREMENT,
  `Uur` time DEFAULT NULL,
  `Hoeveelheid` int(11) DEFAULT NULL,
  `ActieID` int(11) NOT NULL,
  PRIMARY KEY (`Volgnr`),
  KEY `fk_Voederschema_Actie1_idx` (`ActieID`),
  CONSTRAINT `fk_Voederschema_Actie1` FOREIGN KEY (`ActieID`) REFERENCES `Actie` (`ActieID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Voederschema`
--

LOCK TABLES `Voederschema` WRITE;
/*!40000 ALTER TABLE `Voederschema` DISABLE KEYS */;
INSERT INTO `Voederschema` VALUES (1,'09:00:00',30,6),(2,'13:00:00',30,6),(3,'18:00:00',30,6),(4,'10:00:00',45,7),(5,'14:00:00',45,7),(6,'19:00:00',45,7);
/*!40000 ALTER TABLE `Voederschema` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-08 10:08:12
