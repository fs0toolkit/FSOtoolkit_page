-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: fs0tool
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `review_type` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `sol_area` varchar(255) DEFAULT NULL,
  `req_area` varchar(255) DEFAULT NULL,
  `release_label` varchar(255) DEFAULT NULL,
  `rat` varchar(255) DEFAULT NULL,
  `review_start_date` date DEFAULT NULL,
  `review_end_date` date DEFAULT NULL,
  `primary_tm` varchar(255) DEFAULT NULL,
  `sign_off` varchar(255) DEFAULT NULL,
  `review_summary` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=234241 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (234234,'dsfgsadff','dsfgsadff','dsfgsadff',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(234235,NULL,'wegwrag','krishna@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(234236,'New_Review','xtgjngx','krishna@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(234237,'New_Review','xf,jbn;zfbh','krishna@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(234238,'New_Review','sgagg','krishna@gmail.com','Cloud','SA/RandT1','RA/RandT3','23R1','5G',NULL,NULL,NULL,'yes',NULL),(234239,'New_Review','egvswgbaDG','krishna@gmail.com','Operability','SA/RandT2','RA/RandT1','23R2',NULL,'2023-08-31','2023-09-09','sgsgrf@gmail.com',NULL,'gbfbh@gmail.com'),(234240,'New_Review','wdgaegD','krishna@gmail.com','Cloud','SA/RandT1','RA/RandT2','23R2','5G','2023-08-24','2023-09-07','wsgaw@gmail.com','no','wsgaw@gmail.com');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-07  9:24:59
