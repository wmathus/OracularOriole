-- MySQL dump 10.13  Distrib 8.0.41, for macos15 (x86_64)
--
-- Host: sql8.freesqldatabase.com    Database: sql8762368
-- ------------------------------------------------------
-- Server version	5.5.62-0ubuntu0.14.04.1

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
-- Table structure for table `Gene_Functions`
--

DROP TABLE IF EXISTS `Gene_Functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Gene_Functions` (
  `gene_id` varchar(50) NOT NULL,
  `gene_description` text,
  `ensembl_id` varchar(20) DEFAULT NULL,
  `gene_start` bigint(20) DEFAULT NULL,
  `gene_end` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`gene_id`),
  UNIQUE KEY `ensembl_id` (`ensembl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gene_Functions`
--

LOCK TABLES `Gene_Functions` WRITE;
/*!40000 ALTER TABLE `Gene_Functions` DISABLE KEYS */;
INSERT INTO `Gene_Functions` VALUES ('ABHD6','abhydrolase domain containing 6, acylglycerol lipase','ENSG00000163686',58237532,58295693),('ADCY5','adenylate cyclase 5','ENSG00000173175',123282296,123449090),('AGMO','alkylglycerol monooxygenase','ENSG00000187546',5200317,15562015),('ARHGAP19','Rho GTPase activating protein 19','ENSG00000213390',97222173,97292673),('BMPR2','bone morphogenetic protein receptor type 2','ENSG00000204217',202376327,202567751),('CACNA2D3','calcium voltage-gated channel auxiliary subunit alpha2delta 3','ENSG00000157445',54122552,55074557),('CASR','calcium sensing receptor','ENSG00000036828',122183668,122291629),('CCK','cholecystokinin','ENSG00000187094',42257825,42266185),('CDK5RAP1','CDK5 regulatory subunit associated protein 1','ENSG00000101391',33358839,33401561),('CDKAL1','transcription factor 7 like 2','ENSG00000145996',112950247,113167678),('CDKL2','cyclin dependent kinase like 2','ENSG00000138769',75576496,75630716),('CEP120','centrosomal protein 120','ENSG00000168944',123344890,123423592),('CFAP61','cilia and flagella associated protein 61','ENSG00000089101',20052514,20360703),('CHD1L','chromodomain helicase DNA binding protein 1 like','ENSG00000131778',147242654,147295765),('COBLL1','cordon-bleu WH2 repeat protein like 1','ENSG00000082438',164653624,164843679),('DPPA3P3','DPPA3 pseudogene 3','ENSG00000270415',81114866,81115295),('EMB','embigin','ENSG00000170571',50396192,50443248),('EMSY','EMSY transcriptional repressor, BRCA2 interacting','ENSG00000158636',76444923,76553031),('GCKR','glucokinase regulator','ENSG00000084734',27496839,27523684),('GLI2','GLI family zinc finger 2','ENSG00000074047',120735623,120992653),('GRB14','growth factor receptor bound protein 14','ENSG00000115290',164492417,164621482),('GRID1','glutamate ionotropic receptor delta type subunit 1','ENSG00000182771',85599552,86366795),('GTF3AP5','general transcription factor IIIA pseudogene 5','ENSG00000225816',14985378,14986074),('GUCY1B1','guanylate cyclase 1 soluble subunit beta 1','ENSG00000061918',155758992,155807811),('HNRNPA1P23','heterogeneous nuclear ribonucleoprotein A1 pseudogene 23','ENSG00000240236',122317609,122318741),('IGF2BP2','insulin like growth factor 2 mRNA binding protein 2','ENSG00000073792',185643130,185825042),('IKZF2','IKAROS family zinc finger 2','ENSG00000030419',212999691,213152427),('JADE2','jade family PHD finger 2','ENSG00000043143',134524312,134583230),('KCNS3','potassium voltage-gated channel modifier subfamily S member 3','ENSG00000170745',17877847,18361616),('KLF7P1','KLF7 pseudogene 1','ENSG00000240704',170952850,170953897),('LINC00377','long intergenic non-protein coding RNA 377','ENSG00000229246',81018176,81044691),('LINC00558','long intergenic non-protein coding RNA 558','ENSG00000261517',53815419,53939960),('LINC00624','long intergenic non-protein coding RNA 624','ENSG00000278811',147258885,147517879),('LINC01141','long intergenic non-protein coding RNA 1141','ENSG00000236963',20360579,20439489),('LINC01450','long intergenic non-protein coding RNA 1450','ENSG00000232458',40964667,40979939),('LINC01875','long intergenic non-protein coding RNA 1875','ENSG00000225942',545805,546675),('LINC02915','long intergenic non-protein coding RNA 2915','ENSG00000175746',39250681,39254845),('LINC02950','long intergenic non-protein coding RNA 2950','ENSG00000254153',8449664,8461490),('LINC03019','long intergenic non-protein coding RNA 3019','ENSG00000254813',12765849,12811478),('MAP3K13','mitogen-activated protein kinase kinase kinase 13','ENSG00000073803',185282941,185489094),('MBNL1','muscleblind like splicing regulator 1','ENSG00000152601',152243828,152465780),('Metazoa_SRP','Metazoan signal recognition particle RNA','ENSG00000277950',20070716,20070965),('MIR4776-2','microRNA 4776-2','ENSG00000283637',212926257,212926336),('MIR5702','microRNA 5702','ENSG00000263363',226658710,226658793),('MTCO1P17','MT-CO1 pseudogene 17','ENSG00000223619',202614214,202614704),('MTNR1B','melatonin receptor 1B','ENSG00000134640',92969651,92985066),('NHSL1','NHS like 1','ENSG00000135540',138422043,138692571),('NYAP2','neuronal tyrosine-phosphorylated phosphoinositide-3-kinase adaptor 2','ENSG00000144460',225399710,225729887),('PARP8','poly(ADP-ribose) polymerase family member 8','ENSG00000151883',50665899,50846519),('PLEKHM2','pleckstrin homology and RUN domain containing M2','ENSG00000116786',15684320,15734769),('PPARG','peroxisome proliferator activated receptor gamma','ENSG00000132170',12287368,12434356),('PRDM6','PR/SET domain 6','ENSG00000061455',123089241,123194266),('PROX1-AS1','PROX1 antisense RNA 1','ENSG00000230461',213817751,213988508),('PXK','PX domain containing serine/threonine kinase like','ENSG00000168297',58332880,58426127),('RDH14','retinol dehydrogenase 14','ENSG00000240857',18554723,18560679),('RNU1-70P','RNA, U1 small nuclear 70, pseudogene','ENSG00000199488',170994870,170995033),('RPP14','ribonuclease P/MRP subunit p14','ENSG00000163684',58306245,58324695),('RPS3AP18','RPS3A pseudogene 18','ENSG00000243417',152551277,152552364),('RREB1','ras responsive element binding protein 1','ENSG00000124782',7107597,7251980),('SALL4P6','spalt like transcription factor 4 pseudogene 6','ENSG00000231280',42321005,42322695),('SLC12A8','solute carrier family 12 member 8','ENSG00000221955',125082636,125212864),('SLC25A26','solute carrier family 25 member 26','ENSG00000144741',66133610,66388116),('SLC8A1','solute carrier family 8 member A1','ENSG00000183023',40097270,40611053),('SLC8A1-AS1','SLC8A1 antisense RNA 1','ENSG00000227028',39786453,40255209),('SPC25','SPC25 component of NDC80 kinetochore complex','ENSG00000152253',168834132,168913371),('SPRED2','sprouty related EVH1 domain containing 2','ENSG00000198369',65310851,65432637),('SSR1','signal sequence receptor subunit 1','ENSG00000124783',7268306,7347446),('ST6GAL1','ST6 beta-galactoside alpha-2,6-sialyltransferase 1','ENSG00000073849',186930325,187078553),('STRBP','spermatid perinuclear RNA binding protein','ENSG00000165209',123109500,123268586),('SUGCT','succinyl-CoA:glutarate-CoA transferase','ENSG00000175600',40135005,40860763),('TCF7L2','transcription factor 7 like 2','ENSG00000148737',112950247,113167678),('THBS1','thrombospondin 1','ENSG00000137801',39581079,39599466),('TMEM154','transmembrane protein 154','ENSG00000170006',152618628,152680012),('TMEM175','transmembrane protein 175','ENSG00000127419',932387,958656),('TMEM18','transmembrane protein 18','ENSG00000151353',663877,677406),('UBE2E2','ubiquitin conjugating enzyme E2 E2','ENSG00000182247',23203020,23591794),('WFS1','wolframin ER transmembrane glycoprotein','ENSG00000109501',6269849,6303265),('Y_RNA','Y RNA','ENSG00000201451',133337728,133337824),('ZFPM2','zinc finger protein, FOG family member 2','ENSG00000169946',104590733,105804539),('ZNF646P1','zinc finger protein 646 pseudogene 1','ENSG00000274316',53408882,53409876);
/*!40000 ALTER TABLE `Gene_Functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Gene_GO`
--

DROP TABLE IF EXISTS `Gene_GO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Gene_GO` (
  `gene_id` varchar(50) NOT NULL,
  `ensembl_id` varchar(20) DEFAULT NULL,
  `go_id` varchar(20) NOT NULL,
  `go_description` text NOT NULL,
  PRIMARY KEY (`gene_id`,`go_id`),
  CONSTRAINT `gene_go_ibfk_1` FOREIGN KEY (`gene_id`) REFERENCES `Gene_Functions` (`gene_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gene_GO`
--

LOCK TABLES `Gene_GO` WRITE;
/*!40000 ALTER TABLE `Gene_GO` DISABLE KEYS */;
INSERT INTO `Gene_GO` VALUES ('ABHD6','ENSG00000163686','GO:0010648','negative regulation of cell communication'),('ADCY5','ENSG00000173175','GO:0032880','regulation of hormone secretion'),('ADCY5','ENSG00000173175','GO:0035556','regulation of hormone secretion'),('ADCY5','ENSG00000173175','GO:0046883','regulation of hormone secretion'),('ADCY5','ENSG00000173175','GO:0050708','regulation of hormone secretion'),('ADCY5','ENSG00000173175','GO:0051046','regulation of hormone secretion'),('ADCY5','ENSG00000173175','GO:0051223','regulation of hormone secretion'),('ADCY5','ENSG00000173175','GO:0052652','regulation of hormone secretion'),('ADCY5','ENSG00000173175','GO:0090087','regulation of hormone secretion'),('ADCY5','ENSG00000173175','GO:0090276','regulation of hormone secretion'),('ARHGAP19','ENSG00000213390','GO:1902531','regulation of intracellular signal transduction'),('BMPR2','ENSG00000204217','GO:0007507','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0008361','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0030323','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0030324','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0035296','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0045596','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0045597','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0045906','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0048639','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0048660','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0050920','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0050921','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0051962','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0060173','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0072359','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0090092','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:0097746','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:1902531','blood vessel diameter maintenance'),('BMPR2','ENSG00000204217','GO:1903522','blood vessel diameter maintenance'),('CACNA2D3','ENSG00000157445','GO:0006812','ion transmembrane transport'),('CACNA2D3','ENSG00000157445','GO:0034220','ion transmembrane transport'),('CACNA2D3','ENSG00000157445','GO:0098660','ion transmembrane transport'),('CASR','ENSG00000036828','GO:0006812','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0008284','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0032880','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0034220','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0034284','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0035296','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0035556','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0043269','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0046883','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0046887','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0046942','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0050708','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0050920','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0050921','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0051046','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0051223','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0071295','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0071404','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0090087','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0090276','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0097746','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:0098660','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:1902531','regulation of hormone secretion'),('CASR','ENSG00000036828','GO:1903522','regulation of hormone secretion'),('CCK','ENSG00000187094','GO:0048812','neuron projection morphogenesis'),('CCK','ENSG00000187094','GO:0048858','neuron projection morphogenesis'),('CCK','ENSG00000187094','GO:0120039','neuron projection morphogenesis'),('CDK5RAP1','ENSG00000101391','GO:0008033','regulation of kinase activity'),('CDK5RAP1','ENSG00000101391','GO:0043549','regulation of kinase activity'),('CDK5RAP1','ENSG00000101391','GO:0045664','regulation of kinase activity'),('CDK5RAP1','ENSG00000101391','GO:0051348','regulation of kinase activity'),('CDKAL1','ENSG00000145996','GO:0008033','tRNA processing'),('CEP120','ENSG00000168944','GO:0032880','regulation of protein localization'),('EMB','ENSG00000082898','GO:0046942','carboxylic acid transport'),('EMB','ENSG00000082898','GO:0048812','carboxylic acid transport'),('EMB','ENSG00000170571','GO:0048858','carboxylic acid transport'),('EMB','ENSG00000082898','GO:0120039','carboxylic acid transport'),('GCKR','ENSG00000012983','GO:0034284','response to monosaccharide'),('GCKR','ENSG00000084734','GO:0043549','response to monosaccharide'),('GCKR','ENSG00000084734','GO:0051348','response to monosaccharide'),('GLI2','ENSG00000074047','GO:0007507','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0008284','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0009968','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0010648','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0030323','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0030324','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0045596','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0045597','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0045664','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0048812','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0048858','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0050678','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0060173','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0072359','positive regulation of cell population proliferation'),('GLI2','ENSG00000074047','GO:0120039','positive regulation of cell population proliferation'),('GRB14','ENSG00000115290','GO:0009968','negative regulation of cell communication'),('GRB14','ENSG00000115290','GO:0010648','negative regulation of cell communication'),('GRID1','ENSG00000182771','GO:0034220','ion transmembrane transport'),('GUCY1B1','ENSG00000061918','GO:0007263','intracellular signal transduction'),('GUCY1B1','ENSG00000061918','GO:0019934','intracellular signal transduction'),('GUCY1B1','ENSG00000061918','GO:0035556','intracellular signal transduction'),('GUCY1B1','ENSG00000061918','GO:0052652','intracellular signal transduction'),('JADE2','ENSG00000043143','GO:0045597','positive regulation of cell differentiation'),('JADE2','ENSG00000043143','GO:0048812','positive regulation of cell differentiation'),('JADE2','ENSG00000043143','GO:0048858','positive regulation of cell differentiation'),('JADE2','ENSG00000043143','GO:0051962','positive regulation of cell differentiation'),('JADE2','ENSG00000043143','GO:0120039','positive regulation of cell differentiation'),('KCNS3','ENSG00000170745','GO:0006812','ion transmembrane transport'),('KCNS3','ENSG00000170745','GO:0034220','ion transmembrane transport'),('KCNS3','ENSG00000170745','GO:0043269','ion transmembrane transport'),('KCNS3','ENSG00000170745','GO:0071805','ion transmembrane transport'),('KCNS3','ENSG00000170745','GO:0098660','ion transmembrane transport'),('MAP3K13','ENSG00000073803','GO:0008361','intracellular signal transduction'),('MAP3K13','ENSG00000073803','GO:0035556','intracellular signal transduction'),('MAP3K13','ENSG00000073803','GO:0043549','intracellular signal transduction'),('MAP3K13','ENSG00000073803','GO:0045597','intracellular signal transduction'),('MAP3K13','ENSG00000073803','GO:0045664','intracellular signal transduction'),('MAP3K13','ENSG00000073803','GO:0048639','intracellular signal transduction'),('MAP3K13','ENSG00000073803','GO:0051962','intracellular signal transduction'),('MAP3K13','ENSG00000073803','GO:1902531','intracellular signal transduction'),('MBNL1','ENSG00000152601','GO:0060173','limb development'),('MTNR1B','ENSG00000134640','GO:0009968','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0010648','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0032880','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0035296','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0045906','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0046883','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0050708','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0051223','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0090087','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0090276','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:0097746','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:1902531','regulation of hormone secretion'),('MTNR1B','ENSG00000134640','GO:1903522','regulation of hormone secretion'),('NYAP2','ENSG00000144460','GO:0035556','intracellular signal transduction'),('NYAP2','ENSG00000144460','GO:0048812','intracellular signal transduction'),('NYAP2','ENSG00000144460','GO:0048858','intracellular signal transduction'),('NYAP2','ENSG00000144460','GO:0120039','intracellular signal transduction'),('PARP8','ENSG00000151883','GO:0035556','intracellular signal transduction'),('PLEKHM2','ENSG00000116786','GO:0032880','regulation of protein localization'),('PPARG','ENSG00000132170','GO:0007507','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0009968','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0010648','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0031000','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0032880','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0035556','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0045596','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0045597','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0045598','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0046883','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0046887','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0046942','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0048660','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0050678','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0050708','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0051046','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0051223','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0051962','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0071295','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0071404','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0072359','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:0090092','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:1902531','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:1903844','regulation of hormone secretion'),('PPARG','ENSG00000132170','GO:2001233','regulation of hormone secretion'),('PRDM6','ENSG00000061455','GO:0045596','negative regulation of cell differentiation'),('PXK','ENSG00000168297','GO:0043269','regulation of monoatomic ion transport'),('RPP14','ENSG00000163684','GO:0008033','tRNA processing'),('RREB1','ENSG00000124782','GO:0008284','positive regulation of cell population proliferation'),('RREB1','ENSG00000124782','GO:0045597','positive regulation of cell population proliferation'),('RREB1','ENSG00000124782','GO:0045598','positive regulation of cell population proliferation'),('RREB1','ENSG00000124782','GO:0050678','positive regulation of cell population proliferation'),('SLC12A8','ENSG00000221955','GO:0006812','ion transmembrane transport'),('SLC12A8','ENSG00000221955','GO:0008361','ion transmembrane transport'),('SLC12A8','ENSG00000221955','GO:0034220','ion transmembrane transport'),('SLC12A8','ENSG00000221955','GO:0071805','ion transmembrane transport'),('SLC12A8','ENSG00000221955','GO:0098660','ion transmembrane transport'),('SLC25A26','ENSG00000144741','GO:0046942','carboxylic acid transport'),('SLC8A1','ENSG00000183023','GO:0006812','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0007507','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0031000','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0034220','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0035296','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0035556','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0043269','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0043549','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0051348','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0072359','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0097746','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:0098660','blood vessel diameter maintenance'),('SLC8A1','ENSG00000183023','GO:1903522','blood vessel diameter maintenance'),('SPC25','ENSG00000152253','GO:0035556','intracellular signal transduction'),('SPRED2','ENSG00000198369','GO:0009968','negative regulation of cell differentiation'),('SPRED2','ENSG00000198369','GO:0010648','negative regulation of cell differentiation'),('SPRED2','ENSG00000198369','GO:0045596','negative regulation of cell differentiation'),('SPRED2','ENSG00000198369','GO:0090092','negative regulation of cell differentiation'),('SPRED2','ENSG00000198369','GO:1902531','negative regulation of cell differentiation'),('SPRED2','ENSG00000198369','GO:1903844','negative regulation of cell differentiation'),('SSR1','ENSG00000124783','GO:0008284','positive regulation of cell population proliferation'),('ST6GAL1','ENSG00000073849','GO:0008284','positive regulation of cell population proliferation'),('ST6GAL1','ENSG00000073849','GO:0050920','positive regulation of cell population proliferation'),('TCF7L2','ENSG00000148737','GO:0008284','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0009968','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0010648','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0032880','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0034284','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0045597','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0046883','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0046887','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0048660','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0050678','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0050708','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0051046','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0051223','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0072359','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0090087','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:0090276','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:1902531','regulation of hormone secretion'),('TCF7L2','ENSG00000148737','GO:2001233','regulation of hormone secretion'),('THBS1','ENSG00000137801','GO:0007263','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0008284','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0009968','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0010648','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0019934','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0034284','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0035556','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0043549','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0048660','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0050678','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0050920','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0050921','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0072359','response to monosaccharide'),('THBS1','ENSG00000137801','GO:0090092','response to monosaccharide'),('THBS1','ENSG00000137801','GO:1902531','response to monosaccharide'),('THBS1','ENSG00000137801','GO:1903844','response to monosaccharide'),('THBS1','ENSG00000137801','GO:2001233','response to monosaccharide'),('TMEM175','ENSG00000127419','GO:0006812','ion transmembrane transport'),('TMEM175','ENSG00000127419','GO:0034220','ion transmembrane transport'),('TMEM175','ENSG00000127419','GO:0071805','ion transmembrane transport'),('TMEM175','ENSG00000127419','GO:0098660','ion transmembrane transport'),('WFS1','ENSG00000109501','GO:0009968','intracellular signal transduction'),('WFS1','ENSG00000109501','GO:0010648','intracellular signal transduction'),('WFS1','ENSG00000109501','GO:0035556','intracellular signal transduction'),('WFS1','ENSG00000109501','GO:0043269','intracellular signal transduction'),('WFS1','ENSG00000109501','GO:1902531','intracellular signal transduction'),('WFS1','ENSG00000109501','GO:2001233','intracellular signal transduction'),('ZFPM2','ENSG00000169946','GO:0007507','positive regulation of cell population proliferation'),('ZFPM2','ENSG00000169946','GO:0008284','positive regulation of cell population proliferation'),('ZFPM2','ENSG00000169946','GO:0030323','positive regulation of cell population proliferation'),('ZFPM2','ENSG00000169946','GO:0030324','positive regulation of cell population proliferation'),('ZFPM2','ENSG00000169946','GO:0045596','positive regulation of cell population proliferation'),('ZFPM2','ENSG00000169946','GO:0045598','positive regulation of cell population proliferation'),('ZFPM2','ENSG00000169946','GO:0048639','positive regulation of cell population proliferation'),('ZFPM2','ENSG00000169946','GO:0072359','positive regulation of cell population proliferation');
/*!40000 ALTER TABLE `Gene_GO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Phenotype`
--

DROP TABLE IF EXISTS `Phenotype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Phenotype` (
  `phenotype_id` varchar(50) NOT NULL,
  `phenotype_name` varchar(100) NOT NULL,
  `phenotype_description` text,
  PRIMARY KEY (`phenotype_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Phenotype`
--

LOCK TABLES `Phenotype` WRITE;
/*!40000 ALTER TABLE `Phenotype` DISABLE KEYS */;
INSERT INTO `Phenotype` VALUES ('BMI','body mass index','a value derived from the weight and height of a person'),('DR','diabetic retinopathy','An eye condition that causes damage to the retinal blood vessels due to chronically elevated blood sugar levels from diabetes'),('HBA1C','glycated hemoglobin','A diabetes marker that measures the amount of glucose attatched to the red blood cell\'s haemoglobin'),('HDL','High-density lipoprotein','Lower HDL cholestrol levels are associated with greater T2D risk'),('LDL','low-density lipoprotein','Higher lDL cholestrol levels are associated with greater T2D risk');
/*!40000 ALTER TABLE `Phenotype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Phenotype_SNP`
--

DROP TABLE IF EXISTS `Phenotype_SNP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Phenotype_SNP` (
  `phenotype_id` varchar(50) NOT NULL,
  `snp_id` varchar(50) NOT NULL,
  PRIMARY KEY (`phenotype_id`,`snp_id`),
  KEY `fk_phenotype_snp_snp` (`snp_id`),
  CONSTRAINT `fk_phenotype_snp_phenotype` FOREIGN KEY (`phenotype_id`) REFERENCES `Phenotype` (`phenotype_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_phenotype_snp_snp` FOREIGN KEY (`snp_id`) REFERENCES `SNPs` (`snp_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Phenotype_SNP`
--

LOCK TABLES `Phenotype_SNP` WRITE;
/*!40000 ALTER TABLE `Phenotype_SNP` DISABLE KEYS */;
INSERT INTO `Phenotype_SNP` VALUES ('HDL','rs10184004'),('HBA1C','rs10748694'),('HBA1C','rs10830963'),('HBA1C','rs11708067'),('HBA1C','rs1260326'),('DR','rs13130845'),('HBA1C','rs13130845'),('HBA1C','rs13257283'),('HBA1C','rs2065703'),('HBA1C','rs2191349'),('HDL','rs2203452'),('HBA1C','rs2488597'),('DR','rs2714343'),('HBA1C','rs2714343'),('HBA1C','rs329122'),('HBA1C','rs35142762'),('HBA1C','rs3775087'),('HBA1C','rs3887925'),('HBA1C','rs62366901'),('HDL','rs62486442'),('HDL','rs7123361'),('HBA1C','rs7261425'),('HDL','rs73689877'),('HBA1C','rs74790763'),('HBA1C','rs7531962'),('HBA1C','rs7626079'),('HBA1C','rs7629245'),('HBA1C','rs7756992'),('HBA1C','rs7765207'),('DR','rs7766070'),('HBA1C','rs7766070'),('HBA1C','rs7903146'),('BMI','rs9568861'),('DR','rs9808924'),('HBA1C','rs9808924'),('HBA1C','rs9854769');
/*!40000 ALTER TABLE `Phenotype_SNP` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Population`
--

DROP TABLE IF EXISTS `Population`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Population` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pop_id` varchar(50) NOT NULL,
  `population_name` varchar(100) DEFAULT NULL,
  `sample_size` int(11) DEFAULT NULL,
  `allele_frequency` decimal(10,5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Population`
--

LOCK TABLES `Population` WRITE;
/*!40000 ALTER TABLE `Population` DISABLE KEYS */;
INSERT INTO `Population` VALUES (1,'SAS','South Asian',22,0.30000),(2,'SAS','South Asian',22,0.41000),(3,'SAS','South Asian',22,0.75000),(4,'SAS','South Asian',22,0.29000),(5,'SAS','South Asian',22,0.54000),(6,'SAS','South Asian',22,0.41000),(7,'SAS','South Asian',197,0.11000),(8,'SAS','South Asian',272,0.32000),(9,'SAS','South Asian',197,0.28000),(10,'SAS','South Asian',197,0.64000),(11,'SAS','South Asian',197,0.60000),(12,'SAS','South Asian',272,0.94000),(13,'SAS','South Asian',197,0.39000),(14,'SAS','South Asian',272,0.12000),(15,'SAS','South Asian',264,0.48000),(16,'SAS','South Asian',190,0.34000),(17,'SAS','South Asian',272,0.92000),(18,'SAS','South Asian',272,0.84000),(19,'SAS','South Asian',271,0.47000),(20,'SAS','South Asian',272,0.42000),(21,'SAS','South Asian',228,0.69000),(22,'SAS','South Asian',272,0.15000),(23,'SAS','South Asian',186,0.01000),(24,'SAS','South Asian',197,0.33000),(25,'SAS','South Asian',272,0.71000),(26,'SAS','South Asian',197,0.15000),(27,'SAS','South Asian',41,0.78200),(28,'SAS','South Asian',41,0.43000),(29,'SAS','South Asian',41,0.26600),(30,'SAS','South Asian',41,0.74100),(31,'SAS','South Asian',41,0.75700),(32,'SAS','South Asian',41,0.75400),(33,'SAS','South Asian',41,0.85700),(34,'SAS','South Asian',41,0.88900),(35,'SAS','South Asian',41,0.88100),(36,'SAS','South Asian',41,0.76000),(37,'SAS','South Asian',41,0.55900),(38,'SAS','South Asian',41,0.96700),(39,'SAS','South Asian',41,0.38300),(40,'SAS','South Asian',41,0.46300),(41,'SAS','South Asian',41,0.61800),(42,'SAS','South Asian',41,0.20100),(43,'SAS','South Asian',41,0.70200),(44,'SAS','South Asian',41,0.24000),(45,'SAS','South Asian',41,0.54900),(46,'SAS','South Asian',41,0.44000),(47,'SAS','South Asian',41,0.88200),(48,'SAS','South Asian',41,0.03900),(49,'SAS','South Asian',41,0.41200),(50,'SAS','South Asian',41,0.05200),(51,'SAS','South Asian',41,0.14700),(52,'SAS','South Asian',41,0.14200),(53,'SAS','South Asian',41,0.04400),(54,'SAS','South Asian',41,0.75500),(55,'SAS','South Asian',41,0.40200),(56,'SAS','South Asian',41,0.94100),(57,'SAS','South Asian',41,0.40300),(58,'SAS','South Asian',41,0.63700),(59,'SAS','South Asian',41,0.28600),(60,'SAS','South Asian',41,0.72100),(61,'SAS','South Asian',41,0.29700),(62,'SAS','South Asian',41,0.16400);
/*!40000 ALTER TABLE `Population` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SNP_Gene`
--

DROP TABLE IF EXISTS `SNP_Gene`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SNP_Gene` (
  `snp_id` varchar(50) NOT NULL,
  `gene_id` varchar(50) NOT NULL,
  PRIMARY KEY (`snp_id`,`gene_id`),
  KEY `fk_snp_genome_gene` (`gene_id`),
  CONSTRAINT `fk_snp_genome_gene` FOREIGN KEY (`gene_id`) REFERENCES `Gene_Functions` (`gene_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_snp_genome_snp` FOREIGN KEY (`snp_id`) REFERENCES `SNPs` (`snp_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SNP_Gene`
--

LOCK TABLES `SNP_Gene` WRITE;
/*!40000 ALTER TABLE `SNP_Gene` DISABLE KEYS */;
INSERT INTO `SNP_Gene` VALUES ('rs62259319','ABHD6'),('rs11708067','ADCY5'),('rs2191349','AGMO'),('rs10748694','ARHGAP19'),('rs12463719','BMPR2'),('rs76263492','CACNA2D3'),('rs1393202','CASR'),('rs935112','CCK'),('rs2065703','CDK5RAP1'),('rs7756992','CDKAL1'),('rs7766070','CDKAL1'),('rs13142804','CDKL2'),('rs2203452','CDKL2'),('rs12655753','CEP120'),('rs74790763','CEP120'),('rs7261425','CFAP61'),('rs59689207','CHD1L'),('rs7531962','CHD1L'),('rs10184004','COBLL1'),('rs76141923','DPPA3P3'),('rs62366901','EMB'),('rs7123361','EMSY'),('rs1260326','GCKR'),('rs10864859','GLI2'),('rs10184004','GRB14'),('rs2114824','GRID1'),('rs2191349','GTF3AP5'),('rs3775087','GUCY1B1'),('rs1393202','HNRNPA1P23'),('rs9808924','IGF2BP2'),('rs9854769','IGF2BP2'),('rs16849467','IKZF2'),('rs329122','JADE2'),('rs7579323','KCNS3'),('rs1514895','KLF7P1'),('rs76141923','LINC00377'),('rs9568861','LINC00558'),('rs7531962','LINC00624'),('rs10916784','LINC01141'),('rs73689877','LINC01450'),('rs35142762','LINC01875'),('rs28790585','LINC02915'),('rs2980766','LINC02950'),('rs62486442','LINC03019'),('rs7629245','MAP3K13'),('rs13066678','MBNL1'),('rs10748694','Metazoa_SRP'),('rs16849467','MIR4776-2'),('rs2972145','MIR5702'),('rs12463719','MTCO1P17'),('rs10830963','MTNR1B'),('rs7765207','NHSL1'),('rs2972145','NYAP2'),('rs62366901','PARP8'),('rs12746673','PLEKHM2'),('rs17036160','PPARG'),('rs74790763','PRDM6'),('rs61818951','PROX1-AS1'),('rs7432739','PXK'),('rs7579323','RDH14'),('rs1514895','RNU1-70P'),('rs62259319','RPP14'),('rs6813195','RPS3AP18'),('rs2714343','RREB1'),('rs935112','SALL4P6'),('rs9873519','SLC12A8'),('rs7626079','SLC25A26'),('rs1012311','SLC8A1'),('rs1012311','SLC8A1-AS1'),('rs13387347','SPC25'),('rs61748094','SPRED2'),('rs2714343','SSR1'),('rs3887925','ST6GAL1'),('rs2488597','STRBP'),('rs73689877','SUGCT'),('rs7903146','TCF7L2'),('rs28790585','THBS1'),('rs6813195','TMEM154'),('rs34311866','TMEM175'),('rs35142762','TMEM18'),('rs13094957','UBE2E2'),('rs13130845','WFS1'),('rs10864859','Y_RNA'),('rs13257283','ZFPM2'),('rs9568861','ZNF646P1');
/*!40000 ALTER TABLE `SNP_Gene` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SNPs`
--

DROP TABLE IF EXISTS `SNPs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SNPs` (
  `snp_id` varchar(50) NOT NULL,
  `chromosome` int(11) NOT NULL,
  `possition` bigint(20) NOT NULL,
  `reference_allele` varchar(10) DEFAULT NULL,
  `effector_allele` varchar(10) DEFAULT NULL,
  `p_value` double NOT NULL,
  `odds_ratio` decimal(10,3) DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  `link` text,
  PRIMARY KEY (`snp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SNPs`
--

LOCK TABLES `SNPs` WRITE;
/*!40000 ALTER TABLE `SNPs` DISABLE KEYS */;
INSERT INTO `SNPs` VALUES ('rs1012311',2,40247882,'G','C',0.00025,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM29'),('rs10184004',2,164651879,'C','C',0.00000011,1.090,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM4'),('rs10748694',10,97296433,'A','A',0.0000000002,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/15'),('rs10830963',11,92975544,'C','G',0.0000824,1.160,'GWAS','https://pmc.ncbi.nlm.nih.gov/articles/PMC9119501/#:~:text=Genes%20%26%20Health%20%28G%26H%29%20is%20a%20large%2C%20population,is%20shared%20between%20BPB%20and%20European%20populations%20%28EUR%29.'),('rs10864859',2,120682642,'G','T',0.00014,1.140,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM30'),('rs10916784',1,20402958,'G','G',0.000018,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM11'),('rs11708067',3,123346931,'A','A',0.0000000044,1.110,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM1'),('rs12463719',2,202585957,'G','A',0.0000000001,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/3'),('rs1260326',2,27508073,'T','C',0.0000086,1.080,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM6'),('rs12655753',5,123347118,'G','G',0.00000044,1.120,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM8'),('rs12746673',1,15723975,'A','C',0.00019,1.080,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM25'),('rs13066678',3,152369044,'G','G',0.00018,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM20'),('rs13094957',3,23415589,'T','T',0.0000014,1.090,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM10'),('rs13130845',4,6295919,'A','C',0.00021,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM17'),('rs13142804',4,75586445,'A','T',0.0011,1.070,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM36'),('rs13257283',8,104596269,'G','G',0.00000004,1.070,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/12'),('rs13387347',2,168898336,'T','C',0.00064,1.050,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM31'),('rs1393202',3,122311754,'C','T',0.00044,1.120,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM24'),('rs1514895',3,170987904,'A','A',0.0045,1.050,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM34'),('rs16849467',2,212954007,'T','T',0.00065,1.050,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM32'),('rs17036160',3,12288284,'C','C',0.00000021,1.120,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM9'),('rs2065703',20,33378892,'C','T',0.00000000007,1.060,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/21'),('rs2114824',10,86359258,'A','G',0.00000005,1.030,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/14'),('rs2191349',7,15024684,'G','T',0.000138,1.140,'GWAS','https://pmc.ncbi.nlm.nih.gov/articles/PMC9119501/#:~:text=Genes%20%26%20Health%20%28G%26H%29%20is%20a%20large%2C%20population,is%20shared%20between%20BPB%20and%20European%20populations%20%28EUR%29.'),('rs2203452',2,226230042,'A','G',0.0000037,1.080,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM5'),('rs2488597',9,123229794,'A','A',0.000000003,1.050,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/13'),('rs2714343',6,7254724,'G','A',0.0007,1.050,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM14'),('rs28790585',15,39376669,'C','T',0.00000004,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/19'),('rs2972145',2,226236593,'A','G',0.0000312,1.190,'GWAS','https://pmc.ncbi.nlm.nih.gov/articles/PMC9119501/#:~:text=Genes%20%26%20Health%20%28G%26H%29%20is%20a%20large%2C%20population,is%20shared%20between%20BPB%20and%20European%20populations%20%28EUR%29.'),('rs2980766',8,8460585,'A','C',0.00000000008,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/10'),('rs329122',5,134528909,'G','A',0.00022,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM13'),('rs34311866',4,958159,'T','C',0.0046,1.050,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM35'),('rs35142762',2,636790,'C','T',0.00001,1.100,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM7'),('rs3775087',4,155781932,'G','A',0.00014,1.070,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM16'),('rs3887925',3,186947857,'C','T',0.00018,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM19'),('rs59689207',1,147250829,'G','A',0.00025,1.080,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM26'),('rs61748094',2,65344755,'G','G',0.000061,1.190,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM12'),('rs61818951',1,213856235,'C','G',0.00042,1.160,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM27'),('rs62259319',3,58304631,'T','C',0.00012,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM23'),('rs62366901',5,50634452,'T','T',0.00000001,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/6'),('rs62486442',8,12765954,'G','A',0.0000000002,1.050,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/11'),('rs6813195',4,152599323,'C','C',0.00011,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM15'),('rs7123361',11,76450345,'A','A',0.00000001,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/16'),('rs7261425',20,20087991,'C','C',0.0000000004,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/20'),('rs73689877',7,40865675,'G','A',0.000000006,1.060,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/9'),('rs7432739',3,58378923,'T','G',0.000000005,1.050,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/4'),('rs74790763',5,123339520,'C','C',0.00000000003,1.100,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/7'),('rs7531962',1,147274360,'G','A',0.00000003,1.060,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/2'),('rs7579323',2,18520808,'G','A',0.00089,1.060,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM28'),('rs76141923',13,81072495,'T','C',0.000000001,1.400,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/18'),('rs7626079',3,66376835,'C','C',0.0000000009,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/5'),('rs76263492',3,54794800,'G','T',0.00018,1.160,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM22'),('rs7629245',3,185424069,'C','T',0.00015,1.070,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM18'),('rs7756992',6,20679478,'C','A',0.000000000452,1.260,'GWAS','https://pmc.ncbi.nlm.nih.gov/articles/PMC9119501/#:~:text=Genes%20%26%20Health%20%28G%26H%29%20is%20a%20large%2C%20population,is%20shared%20between%20BPB%20and%20European%20populations%20%28EUR%29.'),('rs7765207',6,138536917,'C','T',0.000000004,1.040,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/8'),('rs7766070',6,20686342,'C','A',0.00000000000021,1.130,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM3'),('rs7903146',10,112998590,'C','T',1.73e-17,1.370,'GWAS','https://pmc.ncbi.nlm.nih.gov/articles/PMC9119501/#:~:text=Genes%20%26%20Health%20%28G%26H%29%20is%20a%20large%2C%20population,is%20shared%20between%20BPB%20and%20European%20populations%20%28EUR%29.'),('rs935112',3,42270000,'A','G',0.00056,1.080,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM21'),('rs9568861',13,53505311,'C','T',0.00000003,1.050,'GWAS','https://www.nature.com/articles/s42003-022-03248-5/tables/17'),('rs9808924',3,185796401,'G','A',0.000000000000022,1.120,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM2'),('rs9854769',3,185803160,'A','G',0.00000137,1.180,'GWAS','https://pmc.ncbi.nlm.nih.gov/articles/PMC9119501/#:~:text=Genes%20%26%20Health%20%28G%26H%29%20is%20a%20large%2C%20population,is%20shared%20between%20BPB%20and%20European%20populations%20%28EUR%29.'),('rs9873519',3,125202613,'C','T',0.002,1.050,'GWAS','https://www.nature.com/articles/s41586-024-07019-6#MOESM33');
/*!40000 ALTER TABLE `SNPs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Selection_Statistics`
--

DROP TABLE IF EXISTS `Selection_Statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Selection_Statistics` (
  `snp_id` varchar(50) NOT NULL,
  `population_id` int(11) NOT NULL,
  `fst_value` float NOT NULL,
  `ihs_value` float NOT NULL,
  PRIMARY KEY (`snp_id`,`population_id`),
  KEY `fk_selection_statistics_population` (`population_id`),
  CONSTRAINT `fk_selection_statistics_snp` FOREIGN KEY (`snp_id`) REFERENCES `SNPs` (`snp_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_selection_statistics_population` FOREIGN KEY (`population_id`) REFERENCES `Population` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Selection_Statistics`
--

LOCK TABLES `Selection_Statistics` WRITE;
/*!40000 ALTER TABLE `Selection_Statistics` DISABLE KEYS */;
/*!40000 ALTER TABLE `Selection_Statistics` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-18 10:20:02
