-- MySQL dump 10.13  Distrib 5.7.24, for osx11.1 (x86_64)
--
-- Host: localhost    Database: T2D
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `Gene_Functions`
--

DROP TABLE IF EXISTS `Gene_Functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Gene_Functions` (
  `gene_id` int NOT NULL AUTO_INCREMENT,
  `gene_name` varchar(50) NOT NULL,
  `function_description` text,
  PRIMARY KEY (`gene_id`),
  UNIQUE KEY `gene_name` (`gene_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gene_Functions`
--

LOCK TABLES `Gene_Functions` WRITE;
/*!40000 ALTER TABLE `Gene_Functions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Gene_Functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Phenotypes`
--

DROP TABLE IF EXISTS `Phenotypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Phenotypes` (
  `phenotype_id` int NOT NULL AUTO_INCREMENT,
  `phenotype_name` varchar(100) NOT NULL,
  PRIMARY KEY (`phenotype_id`),
  UNIQUE KEY `phenotype_name` (`phenotype_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Phenotypes`
--

LOCK TABLES `Phenotypes` WRITE;
/*!40000 ALTER TABLE `Phenotypes` DISABLE KEYS */;
/*!40000 ALTER TABLE `Phenotypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Populations`
--

DROP TABLE IF EXISTS `Populations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Populations` (
  `pop_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `region` varchar(50) NOT NULL,
  PRIMARY KEY (`pop_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Populations`
--

LOCK TABLES `Populations` WRITE;
/*!40000 ALTER TABLE `Populations` DISABLE KEYS */;
/*!40000 ALTER TABLE `Populations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Selection_Statistics`
--

DROP TABLE IF EXISTS `Selection_Statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Selection_Statistics` (
  `stat_id` int NOT NULL AUTO_INCREMENT,
  `snp_id` varchar(20) NOT NULL,
  `pop_id` int NOT NULL,
  `fst_value` float NOT NULL,
  `ihs_value` float NOT NULL,
  PRIMARY KEY (`stat_id`),
  KEY `fk_stat_snp_id` (`snp_id`),
  KEY `fk_stat_pop_id` (`pop_id`),
  CONSTRAINT `fk_stat_pop_id` FOREIGN KEY (`pop_id`) REFERENCES `Populations` (`pop_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_stat_snp_id` FOREIGN KEY (`snp_id`) REFERENCES `SNPs` (`snp_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Selection_Statistics`
--

LOCK TABLES `Selection_Statistics` WRITE;
/*!40000 ALTER TABLE `Selection_Statistics` DISABLE KEYS */;
/*!40000 ALTER TABLE `Selection_Statistics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SNP_Phenotype`
--

DROP TABLE IF EXISTS `SNP_Phenotype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SNP_Phenotype` (
  `snp_id` varchar(20) NOT NULL,
  `phenotype_id` int NOT NULL,
  PRIMARY KEY (`snp_id`,`phenotype_id`),
  KEY `fk_phenotype_id` (`phenotype_id`),
  CONSTRAINT `fk_phenotype_id` FOREIGN KEY (`phenotype_id`) REFERENCES `Phenotypes` (`phenotype_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_snp_id` FOREIGN KEY (`snp_id`) REFERENCES `SNPs` (`snp_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SNP_Phenotype`
--

LOCK TABLES `SNP_Phenotype` WRITE;
/*!40000 ALTER TABLE `SNP_Phenotype` DISABLE KEYS */;
/*!40000 ALTER TABLE `SNP_Phenotype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SNPs`
--

DROP TABLE IF EXISTS `SNPs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SNPs` (
  `snp_id` varchar(20) NOT NULL,
  `chromosome` int NOT NULL,
  `position` int NOT NULL,
  `gene_name` varchar(50) DEFAULT NULL,
  `p_value` float NOT NULL,
  PRIMARY KEY (`snp_id`),
  KEY `fk_gene_name` (`gene_name`),
  CONSTRAINT `fk_gene_name` FOREIGN KEY (`gene_name`) REFERENCES `Gene_Functions` (`gene_name`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SNPs`
--

LOCK TABLES `SNPs` WRITE;
/*!40000 ALTER TABLE `SNPs` DISABLE KEYS */;
/*!40000 ALTER TABLE `SNPs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-04 14:51:21
