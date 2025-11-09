/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.3-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: db    Database: EcoGest
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `AsignacionHerramienta`
--

DROP TABLE IF EXISTS `AsignacionHerramienta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `AsignacionHerramienta` (
  `id_asignacion` int NOT NULL AUTO_INCREMENT,
  `tarea_id` int unsigned NOT NULL,
  `tarea_descripcion` varchar(255) NOT NULL,
  `fecha_asignacion` datetime(6) NOT NULL,
  `asignado_por_id` int DEFAULT NULL,
  `herramienta_id` int NOT NULL,
  PRIMARY KEY (`id_asignacion`),
  KEY `AsignacionHerramient_asignado_por_id_077590f0_fk_usuario_u` (`asignado_por_id`),
  KEY `AsignacionHerramient_herramienta_id_7ec414e5_fk_Herramien` (`herramienta_id`),
  CONSTRAINT `AsignacionHerramient_asignado_por_id_077590f0_fk_usuario_u` FOREIGN KEY (`asignado_por_id`) REFERENCES `usuario_usuario` (`id_usuario`),
  CONSTRAINT `AsignacionHerramient_herramienta_id_7ec414e5_fk_Herramien` FOREIGN KEY (`herramienta_id`) REFERENCES `Herramienta` (`id_herramienta`),
  CONSTRAINT `AsignacionHerramienta_chk_1` CHECK ((`tarea_id` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AsignacionHerramienta`
--

LOCK TABLES `AsignacionHerramienta` WRITE;
/*!40000 ALTER TABLE `AsignacionHerramienta` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `AsignacionHerramienta` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `AsignacionProducto`
--

DROP TABLE IF EXISTS `AsignacionProducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `AsignacionProducto` (
  `id_asignacion` int NOT NULL AUTO_INCREMENT,
  `tarea_id` int unsigned NOT NULL,
  `cantidad` int unsigned NOT NULL,
  `fecha_asignacion` datetime(6) NOT NULL,
  `asignado_por_id` int DEFAULT NULL,
  `producto_id` int NOT NULL,
  PRIMARY KEY (`id_asignacion`),
  KEY `AsignacionProducto_asignado_por_id_125eb25b_fk_usuario_u` (`asignado_por_id`),
  KEY `AsignacionProducto_producto_id_ff2e7c81_fk_Producto_id_producto` (`producto_id`),
  CONSTRAINT `AsignacionProducto_asignado_por_id_125eb25b_fk_usuario_u` FOREIGN KEY (`asignado_por_id`) REFERENCES `usuario_usuario` (`id_usuario`),
  CONSTRAINT `AsignacionProducto_producto_id_ff2e7c81_fk_Producto_id_producto` FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id_producto`),
  CONSTRAINT `AsignacionProducto_chk_1` CHECK ((`tarea_id` >= 0)),
  CONSTRAINT `AsignacionProducto_chk_2` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AsignacionProducto`
--

LOCK TABLES `AsignacionProducto` WRITE;
/*!40000 ALTER TABLE `AsignacionProducto` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `AsignacionProducto` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `AsignacionVoluntario`
--

DROP TABLE IF EXISTS `AsignacionVoluntario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `AsignacionVoluntario` (
  `id_asignacion` int NOT NULL AUTO_INCREMENT,
  `tarea_id` int unsigned NOT NULL,
  `actividad` varchar(150) NOT NULL,
  `evento_id` int unsigned DEFAULT NULL,
  `evento_nombre` varchar(150) NOT NULL,
  `fecha_asignacion` datetime(6) NOT NULL,
  `asignado_por_id` int DEFAULT NULL,
  `voluntario_id` int NOT NULL,
  PRIMARY KEY (`id_asignacion`),
  KEY `AsignacionVoluntario_asignado_por_id_0d9cd0ab_fk_usuario_u` (`asignado_por_id`),
  KEY `AsignacionVoluntario_voluntario_id_f691d1db_fk_Voluntari` (`voluntario_id`),
  CONSTRAINT `AsignacionVoluntario_asignado_por_id_0d9cd0ab_fk_usuario_u` FOREIGN KEY (`asignado_por_id`) REFERENCES `usuario_usuario` (`id_usuario`),
  CONSTRAINT `AsignacionVoluntario_voluntario_id_f691d1db_fk_Voluntari` FOREIGN KEY (`voluntario_id`) REFERENCES `Voluntario` (`id_voluntario`),
  CONSTRAINT `AsignacionVoluntario_chk_1` CHECK ((`tarea_id` >= 0)),
  CONSTRAINT `AsignacionVoluntario_chk_2` CHECK ((`evento_id` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AsignacionVoluntario`
--

LOCK TABLES `AsignacionVoluntario` WRITE;
/*!40000 ALTER TABLE `AsignacionVoluntario` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `AsignacionVoluntario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `ChatGeneral`
--

DROP TABLE IF EXISTS `ChatGeneral`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ChatGeneral` (
  `id_mensaje` int NOT NULL AUTO_INCREMENT,
  `mensaje` longtext NOT NULL,
  `fecha_envio` datetime(6) NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id_mensaje`),
  KEY `ChatGeneral_usuario_id_b4ceebb0_fk_usuario_usuario_id_usuario` (`usuario_id`),
  CONSTRAINT `ChatGeneral_usuario_id_b4ceebb0_fk_usuario_usuario_id_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ChatGeneral`
--

LOCK TABLES `ChatGeneral` WRITE;
/*!40000 ALTER TABLE `ChatGeneral` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `ChatGeneral` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `ChatPrivado`
--

DROP TABLE IF EXISTS `ChatPrivado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ChatPrivado` (
  `id_chat` int NOT NULL AUTO_INCREMENT,
  `mensaje` longtext NOT NULL,
  `fecha_envio` datetime(6) NOT NULL,
  `emisor_id` int NOT NULL,
  `receptor_id` int NOT NULL,
  PRIMARY KEY (`id_chat`),
  KEY `ChatPrivado_emisor_id_9a615525_fk_usuario_usuario_id_usuario` (`emisor_id`),
  KEY `ChatPrivado_receptor_id_c1856882_fk_usuario_usuario_id_usuario` (`receptor_id`),
  CONSTRAINT `ChatPrivado_emisor_id_9a615525_fk_usuario_usuario_id_usuario` FOREIGN KEY (`emisor_id`) REFERENCES `usuario_usuario` (`id_usuario`),
  CONSTRAINT `ChatPrivado_receptor_id_c1856882_fk_usuario_usuario_id_usuario` FOREIGN KEY (`receptor_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ChatPrivado`
--

LOCK TABLES `ChatPrivado` WRITE;
/*!40000 ALTER TABLE `ChatPrivado` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `ChatPrivado` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Existencia`
--

DROP TABLE IF EXISTS `Existencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Existencia` (
  `id_existencia` int NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `id_producto` int NOT NULL,
  PRIMARY KEY (`id_existencia`),
  UNIQUE KEY `id_producto` (`id_producto`),
  CONSTRAINT `Existencia_id_producto_f36d006f_fk_Producto_id_producto` FOREIGN KEY (`id_producto`) REFERENCES `Producto` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Existencia`
--

LOCK TABLES `Existencia` WRITE;
/*!40000 ALTER TABLE `Existencia` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `Existencia` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Herramienta`
--

DROP TABLE IF EXISTS `Herramienta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Herramienta` (
  `id_herramienta` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  PRIMARY KEY (`id_herramienta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Herramienta`
--

LOCK TABLES `Herramienta` WRITE;
/*!40000 ALTER TABLE `Herramienta` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `Herramienta` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `IncidenciaAmbiental`
--

DROP TABLE IF EXISTS `IncidenciaAmbiental`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `IncidenciaAmbiental` (
  `id_incidencia` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(150) NOT NULL,
  `descripcion` varchar(600) NOT NULL,
  `fecha_reporte` datetime(6) NOT NULL,
  `area_campus` varchar(100) NOT NULL,
  `estado` varchar(40) NOT NULL,
  `id_planta_id` int DEFAULT NULL,
  `id_usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id_incidencia`),
  KEY `IncidenciaAmbiental_id_planta_id_ba428368_fk_PlantaArb` (`id_planta_id`),
  KEY `IncidenciaAmbiental_id_usuario_id_b8c6c1a8_fk_usuario_u` (`id_usuario_id`),
  CONSTRAINT `IncidenciaAmbiental_id_planta_id_ba428368_fk_PlantaArb` FOREIGN KEY (`id_planta_id`) REFERENCES `PlantaArbol` (`id_planta`),
  CONSTRAINT `IncidenciaAmbiental_id_usuario_id_b8c6c1a8_fk_usuario_u` FOREIGN KEY (`id_usuario_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `IncidenciaAmbiental`
--

LOCK TABLES `IncidenciaAmbiental` WRITE;
/*!40000 ALTER TABLE `IncidenciaAmbiental` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `IncidenciaAmbiental` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `PlantaArbol`
--

DROP TABLE IF EXISTS `PlantaArbol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `PlantaArbol` (
  `id_planta` int NOT NULL AUTO_INCREMENT,
  `nombre_comun` varchar(50) NOT NULL,
  `nombre_cientifico` varchar(100) NOT NULL,
  `descripcion` varchar(600) NOT NULL,
  `fecha_plantacion` date DEFAULT NULL,
  `imagen_url` varchar(100) DEFAULT NULL,
  `periodicidad_riego` int NOT NULL,
  `periodicidad_poda` int NOT NULL,
  `periodicidad_fumigacion` int NOT NULL,
  `lat` double DEFAULT NULL,
  `lng` double DEFAULT NULL,
  PRIMARY KEY (`id_planta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PlantaArbol`
--

LOCK TABLES `PlantaArbol` WRITE;
/*!40000 ALTER TABLE `PlantaArbol` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `PlantaArbol` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Producto`
--

DROP TABLE IF EXISTS `Producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Producto` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_llegada` date DEFAULT NULL,
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Producto`
--

LOCK TABLES `Producto` WRITE;
/*!40000 ALTER TABLE `Producto` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `Producto` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `SaludHistorial`
--

DROP TABLE IF EXISTS `SaludHistorial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `SaludHistorial` (
  `id_historial` int NOT NULL AUTO_INCREMENT,
  `fecha_evento` datetime(6) NOT NULL,
  `estado_salud` varchar(8) NOT NULL,
  `observaciones` longtext NOT NULL,
  `planta_id` int NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id_historial`),
  KEY `SaludHistorial_planta_id_9de18015_fk_PlantaArbol_id_planta` (`planta_id`),
  KEY `SaludHistorial_usuario_id_169f33fb_fk_usuario_usuario_id_usuario` (`usuario_id`),
  CONSTRAINT `SaludHistorial_planta_id_9de18015_fk_PlantaArbol_id_planta` FOREIGN KEY (`planta_id`) REFERENCES `PlantaArbol` (`id_planta`),
  CONSTRAINT `SaludHistorial_usuario_id_169f33fb_fk_usuario_usuario_id_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SaludHistorial`
--

LOCK TABLES `SaludHistorial` WRITE;
/*!40000 ALTER TABLE `SaludHistorial` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `SaludHistorial` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `SaludRegistro`
--

DROP TABLE IF EXISTS `SaludRegistro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `SaludRegistro` (
  `id_registro` int NOT NULL AUTO_INCREMENT,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `estado_salud` varchar(8) NOT NULL,
  `observaciones` longtext NOT NULL,
  `planta_id` int NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id_registro`),
  KEY `SaludRegistro_usuario_id_5b52c30b_fk_usuario_usuario_id_usuario` (`usuario_id`),
  KEY `SaludRegistro_fecha_actualizacion_8f9373ef` (`fecha_actualizacion`),
  KEY `SaludRegistro_estado_salud_09f37a8f` (`estado_salud`),
  KEY `SaludRegist_planta__82fb0a_idx` (`planta_id`,`fecha_actualizacion`),
  KEY `SaludRegist_estado__f83fae_idx` (`estado_salud`),
  CONSTRAINT `SaludRegistro_planta_id_49e42c7b_fk_PlantaArbol_id_planta` FOREIGN KEY (`planta_id`) REFERENCES `PlantaArbol` (`id_planta`),
  CONSTRAINT `SaludRegistro_usuario_id_5b52c30b_fk_usuario_usuario_id_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SaludRegistro`
--

LOCK TABLES `SaludRegistro` WRITE;
/*!40000 ALTER TABLE `SaludRegistro` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `SaludRegistro` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Voluntario`
--

DROP TABLE IF EXISTS `Voluntario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Voluntario` (
  `id_voluntario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(80) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `telefono` varchar(25) NOT NULL,
  `tipo_participacion` varchar(20) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  PRIMARY KEY (`id_voluntario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Voluntario`
--

LOCK TABLES `Voluntario` WRITE;
/*!40000 ALTER TABLE `Voluntario` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `Voluntario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_permission` VALUES
(1,'Can add usuario',1,'add_usuario'),
(2,'Can change usuario',1,'change_usuario'),
(3,'Can delete usuario',1,'delete_usuario'),
(4,'Can view usuario',1,'view_usuario'),
(5,'Can add log entry',2,'add_logentry'),
(6,'Can change log entry',2,'change_logentry'),
(7,'Can delete log entry',2,'delete_logentry'),
(8,'Can view log entry',2,'view_logentry'),
(9,'Can add permission',3,'add_permission'),
(10,'Can change permission',3,'change_permission'),
(11,'Can delete permission',3,'delete_permission'),
(12,'Can view permission',3,'view_permission'),
(13,'Can add group',4,'add_group'),
(14,'Can change group',4,'change_group'),
(15,'Can delete group',4,'delete_group'),
(16,'Can view group',4,'view_group'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add planta arbol',7,'add_plantaarbol'),
(26,'Can change planta arbol',7,'change_plantaarbol'),
(27,'Can delete planta arbol',7,'delete_plantaarbol'),
(28,'Can view planta arbol',7,'view_plantaarbol'),
(29,'Can add backup audit',8,'add_backupaudit'),
(30,'Can change backup audit',8,'change_backupaudit'),
(31,'Can delete backup audit',8,'delete_backupaudit'),
(32,'Can view backup audit',8,'view_backupaudit'),
(33,'Can add chat general',9,'add_chatgeneral'),
(34,'Can change chat general',9,'change_chatgeneral'),
(35,'Can delete chat general',9,'delete_chatgeneral'),
(36,'Can view chat general',9,'view_chatgeneral'),
(37,'Can add chat privado',10,'add_chatprivado'),
(38,'Can change chat privado',10,'change_chatprivado'),
(39,'Can delete chat privado',10,'delete_chatprivado'),
(40,'Can view chat privado',10,'view_chatprivado'),
(41,'Can add herramienta',11,'add_herramienta'),
(42,'Can change herramienta',11,'change_herramienta'),
(43,'Can delete herramienta',11,'delete_herramienta'),
(44,'Can view herramienta',11,'view_herramienta'),
(45,'Can add asignacion herramienta',12,'add_asignacionherramienta'),
(46,'Can change asignacion herramienta',12,'change_asignacionherramienta'),
(47,'Can delete asignacion herramienta',12,'delete_asignacionherramienta'),
(48,'Can view asignacion herramienta',12,'view_asignacionherramienta'),
(49,'Can add producto',13,'add_producto'),
(50,'Can change producto',13,'change_producto'),
(51,'Can delete producto',13,'delete_producto'),
(52,'Can view producto',13,'view_producto'),
(53,'Can add asignacion producto',14,'add_asignacionproducto'),
(54,'Can change asignacion producto',14,'change_asignacionproducto'),
(55,'Can delete asignacion producto',14,'delete_asignacionproducto'),
(56,'Can view asignacion producto',14,'view_asignacionproducto'),
(57,'Can add existencia',15,'add_existencia'),
(58,'Can change existencia',15,'change_existencia'),
(59,'Can delete existencia',15,'delete_existencia'),
(60,'Can view existencia',15,'view_existencia'),
(61,'Can add voluntario',16,'add_voluntario'),
(62,'Can change voluntario',16,'change_voluntario'),
(63,'Can delete voluntario',16,'delete_voluntario'),
(64,'Can view voluntario',16,'view_voluntario'),
(65,'Can add asignacion voluntario',17,'add_asignacionvoluntario'),
(66,'Can change asignacion voluntario',17,'change_asignacionvoluntario'),
(67,'Can delete asignacion voluntario',17,'delete_asignacionvoluntario'),
(68,'Can view asignacion voluntario',17,'view_asignacionvoluntario'),
(69,'Can add incidencia ambiental',18,'add_incidenciaambiental'),
(70,'Can change incidencia ambiental',18,'change_incidenciaambiental'),
(71,'Can delete incidencia ambiental',18,'delete_incidenciaambiental'),
(72,'Can view incidencia ambiental',18,'view_incidenciaambiental'),
(73,'Can add salud registro',19,'add_saludregistro'),
(74,'Can change salud registro',19,'change_saludregistro'),
(75,'Can delete salud registro',19,'delete_saludregistro'),
(76,'Can view salud registro',19,'view_saludregistro'),
(77,'Can add salud historial',20,'add_saludhistorial'),
(78,'Can change salud historial',20,'change_saludhistorial'),
(79,'Can delete salud historial',20,'delete_saludhistorial'),
(80,'Can view salud historial',20,'view_saludhistorial'),
(81,'Can add notificacion',21,'add_notificacion'),
(82,'Can change notificacion',21,'change_notificacion'),
(83,'Can delete notificacion',21,'delete_notificacion'),
(84,'Can view notificacion',21,'view_notificacion');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_usuario_usuario_id_usuario` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_usuario_usuario_id_usuario` FOREIGN KEY (`user_id`) REFERENCES `usuario_usuario` (`id_usuario`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(2,'admin','logentry'),
(4,'auth','group'),
(3,'auth','permission'),
(9,'chat','chatgeneral'),
(10,'chat','chatprivado'),
(5,'contenttypes','contenttype'),
(12,'herramientas','asignacionherramienta'),
(11,'herramientas','herramienta'),
(18,'incidencias','incidenciaambiental'),
(21,'notificaciones','notificacion'),
(7,'plantas','plantaarbol'),
(14,'productos','asignacionproducto'),
(15,'productos','existencia'),
(13,'productos','producto'),
(8,'respaldo','backupaudit'),
(20,'salud','saludhistorial'),
(19,'salud','saludregistro'),
(6,'sessions','session'),
(1,'usuario','usuario'),
(17,'voluntarios','asignacionvoluntario'),
(16,'voluntarios','voluntario');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-11-05 16:22:48.061791'),
(2,'contenttypes','0002_remove_content_type_name','2025-11-05 16:22:48.476465'),
(3,'auth','0001_initial','2025-11-05 16:22:49.314580'),
(4,'auth','0002_alter_permission_name_max_length','2025-11-05 16:22:49.514224'),
(5,'auth','0003_alter_user_email_max_length','2025-11-05 16:22:49.529086'),
(6,'auth','0004_alter_user_username_opts','2025-11-05 16:22:49.543453'),
(7,'auth','0005_alter_user_last_login_null','2025-11-05 16:22:49.558461'),
(8,'auth','0006_require_contenttypes_0002','2025-11-05 16:22:49.566358'),
(9,'auth','0007_alter_validators_add_error_messages','2025-11-05 16:22:49.584342'),
(10,'auth','0008_alter_user_username_max_length','2025-11-05 16:22:49.598019'),
(11,'auth','0009_alter_user_last_name_max_length','2025-11-05 16:22:49.608935'),
(12,'auth','0010_alter_group_name_max_length','2025-11-05 16:22:49.647086'),
(13,'auth','0011_update_proxy_permissions','2025-11-05 16:22:49.660218'),
(14,'auth','0012_alter_user_first_name_max_length','2025-11-05 16:22:49.673566'),
(15,'usuario','0001_initial','2025-11-05 16:22:50.669610'),
(16,'admin','0001_initial','2025-11-05 16:22:51.101248'),
(17,'admin','0002_logentry_remove_auto_add','2025-11-05 16:22:51.118174'),
(18,'admin','0003_logentry_add_action_flag_choices','2025-11-05 16:22:51.133095'),
(19,'chat','0001_initial','2025-11-05 16:22:51.827141'),
(20,'chat','0002_alter_chatgeneral_options_alter_chatprivado_options','2025-11-05 16:22:51.846917'),
(21,'herramientas','0001_initial','2025-11-05 16:22:52.333313'),
(22,'plantas','0001_initial','2025-11-05 16:22:52.392914'),
(23,'incidencias','0001_initial','2025-11-05 16:22:52.790230'),
(24,'notificaciones','0001_initial','2025-11-05 16:22:53.500918'),
(25,'productos','0001_initial','2025-11-05 16:22:54.267144'),
(26,'respaldo','0001_initial','2025-11-05 16:22:54.515928'),
(27,'salud','0001_initial','2025-11-05 16:22:55.129154'),
(28,'salud','0002_saludhistorial','2025-11-05 16:22:55.562271'),
(29,'sessions','0001_initial','2025-11-05 16:22:55.684924'),
(30,'usuario','0002_alter_usuario_correo','2025-11-05 16:22:55.709722'),
(31,'usuario','0003_rename_correo_usuario_email','2025-11-05 16:22:55.801217'),
(32,'voluntarios','0001_initial','2025-11-05 16:22:56.354357');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_session` VALUES
('4ius9egykawpaz49uftf98fk9pevsuql','.eJxVizsOAiEQQO9CbTYwOHws7fcMZGbAQDSawFIZ764mW2j7Pk-VaG41zVF6almdlFGHX8Yk13L_ijkm9fZYdjKWlbbeZN7ovDd_Y6VRPxey9i5Y7y5yDCWSCdkhBDCoNVsEAWHkCJBNQW8pGqetw0BiybOP6vUG5Ogz-Q:1vGgIl:KXSgAfwLoo59qIRHS1a5ubZUrv-9kzDJVH_HcUxE818','2025-11-05 16:54:03.384794'),
('hnmevb25pvz2vr7ux6ytpsnwoiwbxtew','.eJxVizsOAiEQQO9CbTYwOHws7fcMZGbAQDSawFIZ764mW2j7Pk-VaG41zVF6almdlFGHX8Yk13L_ijkm9fZYdjKWlbbeZN7ovDd_Y6VRPxey9i5Y7y5yDCWSCdkhBDCoNVsEAWHkCJBNQW8pGqetw0BiybOP6vUG5Ogz-Q:1vGgvo:YAxny03TH3sJsrLapkNcyKwaRubBZpzufBpv5EhLLz0','2025-11-05 17:34:24.040807');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `notificaciones_notificacion`
--

DROP TABLE IF EXISTS `notificaciones_notificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificaciones_notificacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `level` varchar(20) NOT NULL,
  `object_id_actor` int unsigned NOT NULL,
  `object_id_target` int unsigned DEFAULT NULL,
  `verbo` varchar(255) NOT NULL,
  `no_leido` tinyint(1) NOT NULL,
  `publico` tinyint(1) NOT NULL,
  `eliminar` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `actor_content_type_id` int NOT NULL,
  `destiny_id` int DEFAULT NULL,
  `target_content_type_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `notificaciones_notif_actor_content_type_i_a2ae15b0_fk_django_co` (`actor_content_type_id`),
  KEY `notificaciones_notif_destiny_id_e683c187_fk_usuario_u` (`destiny_id`),
  KEY `notificaciones_notif_target_content_type__66c356c5_fk_django_co` (`target_content_type_id`),
  KEY `notificaciones_notificacion_timestamp_a2dac771` (`timestamp`),
  CONSTRAINT `notificaciones_notif_actor_content_type_i_a2ae15b0_fk_django_co` FOREIGN KEY (`actor_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `notificaciones_notif_destiny_id_e683c187_fk_usuario_u` FOREIGN KEY (`destiny_id`) REFERENCES `usuario_usuario` (`id_usuario`),
  CONSTRAINT `notificaciones_notif_target_content_type__66c356c5_fk_django_co` FOREIGN KEY (`target_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `notificaciones_notificacion_chk_1` CHECK ((`object_id_actor` >= 0)),
  CONSTRAINT `notificaciones_notificacion_chk_2` CHECK ((`object_id_target` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificaciones_notificacion`
--

LOCK TABLES `notificaciones_notificacion` WRITE;
/*!40000 ALTER TABLE `notificaciones_notificacion` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `notificaciones_notificacion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `respaldo_backupaudit`
--

DROP TABLE IF EXISTS `respaldo_backupaudit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `respaldo_backupaudit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(10) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `run_at` datetime(6) NOT NULL,
  `log` longtext NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `respaldo_backupaudit_user_id_65c9ebaa_fk_usuario_u` (`user_id`),
  CONSTRAINT `respaldo_backupaudit_user_id_65c9ebaa_fk_usuario_u` FOREIGN KEY (`user_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respaldo_backupaudit`
--

LOCK TABLES `respaldo_backupaudit` WRITE;
/*!40000 ALTER TABLE `respaldo_backupaudit` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `respaldo_backupaudit` VALUES
(1,'BACKUP','EcoGest_2025-11-05_11-11-53.sql','2025-11-05 17:11:54.066440','OK mysqldump\n',1);
/*!40000 ALTER TABLE `respaldo_backupaudit` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuario_usuario`
--

DROP TABLE IF EXISTS `usuario_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_usuario` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `matricula` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `nombre_completo` varchar(100) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `matricula` (`matricula`),
  UNIQUE KEY `correo` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_usuario`
--

LOCK TABLES `usuario_usuario` WRITE;
/*!40000 ALTER TABLE `usuario_usuario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `usuario_usuario` VALUES
('pbkdf2_sha256$1000000$AyYyhts03aHiNxuwNs0AKO$FYVNK3NNxcwNQN7GoThZ/LXpzxxEvXKobgMVGR7ExaQ=','2025-11-05 17:04:24.022274',1,1,'aoco220155','aoco220155@upemor.edu.mx','aoco220155','administrador',1,1);
/*!40000 ALTER TABLE `usuario_usuario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuario_usuario_groups`
--

DROP TABLE IF EXISTS `usuario_usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_usuario_groups_usuario_id_group_id_a4cfb0b8_uniq` (`usuario_id`,`group_id`),
  KEY `usuario_usuario_groups_group_id_b9c090f8_fk_auth_group_id` (`group_id`),
  CONSTRAINT `usuario_usuario_grou_usuario_id_62de76a1_fk_usuario_u` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id_usuario`),
  CONSTRAINT `usuario_usuario_groups_group_id_b9c090f8_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_usuario_groups`
--

LOCK TABLES `usuario_usuario_groups` WRITE;
/*!40000 ALTER TABLE `usuario_usuario_groups` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `usuario_usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuario_usuario_user_permissions`
--

DROP TABLE IF EXISTS `usuario_usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_usuario_user_per_usuario_id_permission_id_c0a85055_uniq` (`usuario_id`,`permission_id`),
  KEY `usuario_usuario_user_permission_id_5cad0a4b_fk_auth_perm` (`permission_id`),
  CONSTRAINT `usuario_usuario_user_permission_id_5cad0a4b_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `usuario_usuario_user_usuario_id_5969a193_fk_usuario_u` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_usuario_user_permissions`
--

LOCK TABLES `usuario_usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `usuario_usuario_user_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `usuario_usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping events for database 'EcoGest'
--

--
-- Dumping routines for database 'EcoGest'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-11-05 11:28:55
