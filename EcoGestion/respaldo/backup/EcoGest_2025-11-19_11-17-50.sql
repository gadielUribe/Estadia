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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AsignacionVoluntario`
--

LOCK TABLES `AsignacionVoluntario` WRITE;
/*!40000 ALTER TABLE `AsignacionVoluntario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `AsignacionVoluntario` VALUES
(1,58,'Poda - Gerbera',NULL,'','2025-11-17 04:22:07.596581',1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ChatGeneral`
--

LOCK TABLES `ChatGeneral` WRITE;
/*!40000 ALTER TABLE `ChatGeneral` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ChatGeneral` VALUES
(1,'Hola','2025-11-10 05:23:51.222069',1),
(2,'Ok mañana <3','2025-11-12 03:00:56.615849',4);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ChatPrivado`
--

LOCK TABLES `ChatPrivado` WRITE;
/*!40000 ALTER TABLE `ChatPrivado` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ChatPrivado` VALUES
(1,'Justo ayer dejamos de programar <3','2025-11-12 03:05:36.317444',4,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Existencia`
--

LOCK TABLES `Existencia` WRITE;
/*!40000 ALTER TABLE `Existencia` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Existencia` VALUES
(1,3,'2025-11-10 22:41:28.255722',1);
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
  `estado` varchar(20) NOT NULL,
  PRIMARY KEY (`id_herramienta`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Herramienta`
--

LOCK TABLES `Herramienta` WRITE;
/*!40000 ALTER TABLE `Herramienta` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Herramienta` VALUES
(1,'Tijeras','Grandes','disponible'),
(2,'Manguera','30 metros','disponible'),
(3,'Pala','25 cm','disponible'),
(4,'Mesa','','disponible');
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
  `periodicidad_riego` varchar(40) NOT NULL,
  `periodicidad_poda` varchar(40) NOT NULL,
  `periodicidad_fumigacion` varchar(40) NOT NULL,
  `lat` double DEFAULT NULL,
  `lng` double DEFAULT NULL,
  PRIMARY KEY (`id_planta`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PlantaArbol`
--

LOCK TABLES `PlantaArbol` WRITE;
/*!40000 ALTER TABLE `PlantaArbol` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `PlantaArbol` VALUES
(3,'Gerbera','Asteraceae','Margarita africana','2025-11-22','plantas/2025/11/Gerbera.jpg','19','23','22',18.889743,-99.139621);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Producto`
--

LOCK TABLES `Producto` WRITE;
/*!40000 ALTER TABLE `Producto` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Producto` VALUES
(1,'Insecticida','Para hormigas','2025-11-01'),
(2,'Abono','Fertilizante para plantas','2025-12-21'),
(3,'Veneno','',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SaludHistorial`
--

LOCK TABLES `SaludHistorial` WRITE;
/*!40000 ALTER TABLE `SaludHistorial` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `SaludHistorial` VALUES
(3,'2025-11-12 02:48:59.336222','verde','Coloridas con colores muy vibrantes',3,4);
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
  UNIQUE KEY `SaludRegistro_planta_id_49e42c7b_uniq` (`planta_id`),
  KEY `SaludRegistro_usuario_id_5b52c30b_fk_usuario_usuario_id_usuario` (`usuario_id`),
  KEY `SaludRegistro_fecha_actualizacion_8f9373ef` (`fecha_actualizacion`),
  KEY `SaludRegistro_estado_salud_09f37a8f` (`estado_salud`),
  KEY `SaludRegist_planta__82fb0a_idx` (`planta_id`,`fecha_actualizacion`),
  KEY `SaludRegist_estado__f83fae_idx` (`estado_salud`),
  CONSTRAINT `SaludRegistro_planta_id_49e42c7b_fk_PlantaArbol_id_planta` FOREIGN KEY (`planta_id`) REFERENCES `PlantaArbol` (`id_planta`),
  CONSTRAINT `SaludRegistro_usuario_id_5b52c30b_fk_usuario_usuario_id_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SaludRegistro`
--

LOCK TABLES `SaludRegistro` WRITE;
/*!40000 ALTER TABLE `SaludRegistro` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `SaludRegistro` VALUES
(3,'2025-11-12 02:48:59.333787','verde','Coloridas con colores muy vibrantes',3,4);
/*!40000 ALTER TABLE `SaludRegistro` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `TareaMantenimiento`
--

DROP TABLE IF EXISTS `TareaMantenimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `TareaMantenimiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(20) NOT NULL,
  `fecha_programada` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha_realizacion` datetime(6) DEFAULT NULL,
  `observaciones` longtext,
  `creado_en` datetime(6) NOT NULL,
  `actualizado_en` datetime(6) NOT NULL,
  `herramienta_id` int DEFAULT NULL,
  `modificado_por_id` int DEFAULT NULL,
  `planta_id` int NOT NULL,
  `producto_id` int DEFAULT NULL,
  `usuario_responsable_id` int DEFAULT NULL,
  `recordatorio_24h_enviado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `TareaMantenimiento_herramienta_id_1263d95b_fk_Herramien` (`herramienta_id`),
  KEY `TareaMantenimiento_modificado_por_id_c5e28838_fk_usuario_u` (`modificado_por_id`),
  KEY `TareaMantenimiento_planta_id_fa610b44_fk_PlantaArbol_id_planta` (`planta_id`),
  KEY `TareaMantenimiento_producto_id_f390f16c_fk_Producto_id_producto` (`producto_id`),
  KEY `TareaMantenimiento_usuario_responsable__0f7416c1_fk_usuario_u` (`usuario_responsable_id`),
  CONSTRAINT `TareaMantenimiento_herramienta_id_1263d95b_fk_Herramien` FOREIGN KEY (`herramienta_id`) REFERENCES `Herramienta` (`id_herramienta`),
  CONSTRAINT `TareaMantenimiento_modificado_por_id_c5e28838_fk_usuario_u` FOREIGN KEY (`modificado_por_id`) REFERENCES `usuario_usuario` (`id_usuario`),
  CONSTRAINT `TareaMantenimiento_planta_id_fa610b44_fk_PlantaArbol_id_planta` FOREIGN KEY (`planta_id`) REFERENCES `PlantaArbol` (`id_planta`),
  CONSTRAINT `TareaMantenimiento_producto_id_f390f16c_fk_Producto_id_producto` FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id_producto`),
  CONSTRAINT `TareaMantenimiento_usuario_responsable__0f7416c1_fk_usuario_u` FOREIGN KEY (`usuario_responsable_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TareaMantenimiento`
--

LOCK TABLES `TareaMantenimiento` WRITE;
/*!40000 ALTER TABLE `TareaMantenimiento` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `TareaMantenimiento` VALUES
(52,'riego','2025-12-12 13:00:00.000000','realizada','2025-11-12 02:57:41.643656','','2025-11-12 02:56:07.676865','2025-11-12 02:57:41.644172',2,4,3,2,3,0),
(53,'riego','2025-12-19 13:00:00.000000','realizada','2025-11-18 18:07:42.480744','','2025-11-12 02:56:07.705059','2025-11-18 18:07:42.480983',2,1,3,2,3,0),
(54,'riego','2025-12-26 13:00:00.000000','realizada','2025-11-18 18:07:47.559895','','2025-11-12 02:56:07.724809','2025-11-18 18:07:47.560087',2,1,3,2,3,0),
(55,'riego','2026-01-02 13:00:00.000000','pendiente',NULL,'','2025-11-12 02:56:07.740833','2025-11-12 02:56:07.740856',2,NULL,3,2,3,0),
(56,'riego','2026-01-09 13:00:00.000000','pendiente',NULL,'','2025-11-12 02:56:07.757106','2025-11-12 02:56:07.757130',2,NULL,3,2,3,0),
(57,'fumigacion','2025-11-29 03:52:00.000000','realizada','2025-11-18 18:06:43.082652','','2025-11-17 03:52:30.901853','2025-11-18 18:06:43.082931',NULL,1,3,NULL,2,0),
(58,'poda','2025-11-17 18:25:00.000000','pendiente',NULL,'','2025-11-17 04:22:07.567039','2025-11-17 04:22:58.421857',4,NULL,3,NULL,NULL,0),
(59,'fumigacion','2025-11-20 06:59:00.000000','realizada','2025-11-19 07:11:51.021227','','2025-11-19 06:58:06.066558','2025-11-19 07:11:51.021400',NULL,1,3,NULL,3,1);
/*!40000 ALTER TABLE `TareaMantenimiento` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Voluntario`
--

LOCK TABLES `Voluntario` WRITE;
/*!40000 ALTER TABLE `Voluntario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Voluntario` VALUES
(1,'Adrian','Villafuerte','adrianvillafuerteuribe@gmail.com','7772240321','estudiante','2025-11-12 03:08:12.931115'),
(2,'Monica','Uribe','dianserrrat@gmail.com','7771912374','externo','2025-11-12 03:09:51.774906');
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
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
(84,'Can view notificacion',21,'view_notificacion'),
(85,'Can add tarea mantenimiento',22,'add_tareamantenimiento'),
(86,'Can change tarea mantenimiento',22,'change_tareamantenimiento'),
(87,'Can delete tarea mantenimiento',22,'delete_tareamantenimiento'),
(88,'Can view tarea mantenimiento',22,'view_tareamantenimiento'),
(89,'Can add Evento ambiental',23,'add_eventoambiental'),
(90,'Can change Evento ambiental',23,'change_eventoambiental'),
(91,'Can delete Evento ambiental',23,'delete_eventoambiental'),
(92,'Can view Evento ambiental',23,'view_eventoambiental');
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
(23,'eventos','eventoambiental'),
(12,'herramientas','asignacionherramienta'),
(11,'herramientas','herramienta'),
(18,'incidencias','incidenciaambiental'),
(22,'mantenimiento','tareamantenimiento'),
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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-11-05 17:51:44.993500'),
(2,'contenttypes','0002_remove_content_type_name','2025-11-05 17:51:45.271643'),
(3,'auth','0001_initial','2025-11-05 17:51:46.058692'),
(4,'auth','0002_alter_permission_name_max_length','2025-11-05 17:51:46.269060'),
(5,'auth','0003_alter_user_email_max_length','2025-11-05 17:51:46.317692'),
(6,'auth','0004_alter_user_username_opts','2025-11-05 17:51:46.375717'),
(7,'auth','0005_alter_user_last_login_null','2025-11-05 17:51:46.425282'),
(8,'auth','0006_require_contenttypes_0002','2025-11-05 17:51:46.443451'),
(9,'auth','0007_alter_validators_add_error_messages','2025-11-05 17:51:46.521167'),
(10,'auth','0008_alter_user_username_max_length','2025-11-05 17:51:46.560057'),
(11,'auth','0009_alter_user_last_name_max_length','2025-11-05 17:51:46.627104'),
(12,'auth','0010_alter_group_name_max_length','2025-11-05 17:51:46.710546'),
(13,'auth','0011_update_proxy_permissions','2025-11-05 17:51:46.758245'),
(14,'auth','0012_alter_user_first_name_max_length','2025-11-05 17:51:46.800099'),
(15,'usuario','0001_initial','2025-11-05 17:51:47.737959'),
(16,'admin','0001_initial','2025-11-05 17:51:48.161125'),
(17,'admin','0002_logentry_remove_auto_add','2025-11-05 17:51:48.193398'),
(18,'admin','0003_logentry_add_action_flag_choices','2025-11-05 17:51:48.251638'),
(19,'chat','0001_initial','2025-11-05 17:51:48.880755'),
(20,'chat','0002_alter_chatgeneral_options_alter_chatprivado_options','2025-11-05 17:51:48.942670'),
(21,'herramientas','0001_initial','2025-11-05 17:51:49.490951'),
(22,'plantas','0001_initial','2025-11-05 17:51:49.595027'),
(23,'incidencias','0001_initial','2025-11-05 17:51:50.047691'),
(24,'productos','0001_initial','2025-11-05 17:51:51.089021'),
(25,'mantenimiento','0001_initial','2025-11-05 17:51:52.090006'),
(26,'notificaciones','0001_initial','2025-11-05 17:51:52.781453'),
(27,'plantas','0002_alter_plantaarbol_periodicidad_fumigacion_and_more','2025-11-05 17:51:53.280745'),
(28,'respaldo','0001_initial','2025-11-05 17:51:53.626125'),
(29,'salud','0001_initial','2025-11-05 17:51:54.282350'),
(30,'salud','0002_saludhistorial','2025-11-05 17:51:54.671412'),
(31,'sessions','0001_initial','2025-11-05 17:51:54.790632'),
(32,'usuario','0002_alter_usuario_correo','2025-11-05 17:51:54.851029'),
(33,'usuario','0003_rename_correo_usuario_email','2025-11-05 17:51:55.017158'),
(34,'voluntarios','0001_initial','2025-11-05 17:51:55.513873'),
(35,'plantas','0003_alter_plantaarbol_fecha_plantacion_and_more','2025-11-10 05:20:57.923486'),
(36,'mantenimiento','0002_tareamantenimiento_uniq_herramienta_fecha_pendiente','2025-11-11 03:12:13.816572'),
(37,'mantenimiento','0003_remove_tareamantenimiento_uniq_herramienta_fecha_pendiente','2025-11-11 04:18:08.530933'),
(38,'mantenimiento','0004_tareamantenimiento_recordatorio_24h_enviado','2025-11-11 05:01:41.464206'),
(39,'salud','0003_alter_saludregistro_estado_salud_and_more','2025-11-16 03:41:49.296567'),
(40,'herramientas','0002_herramienta_estado','2025-11-16 22:56:47.739942'),
(41,'eventos','0001_initial','2025-11-17 03:26:34.676193');
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
('0chw5tomvk0r3bqkfa90hoi0vlnftm3r','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vKrSn:VU-D2WH_BuSNbOHfEaDUr_Cta2gGKKnCsny-VMPfr4g','2025-11-17 05:37:41.899191'),
('0xkozsqz0h460pf93wyy06wlht3bts2k','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIcDt:S6u9JWbXLjRIEhtdKjLa10KM7RxseSMb1VEaTuE9kE4','2025-11-11 00:57:01.431660'),
('11pdene2jjt33wxi90mzmktyz3h3fxt5','.eJxVy8sOwiAQheF3YW2agSk3l-59BjIMJRCNJlBWxne3Tbqo2--c_yMCjbWE0ZcWahJXMYvL2SLxY3ntw-iDWn1Ph_TpTmurPJ50Oz5_YaFetgozAkttAaVLGSBq65EikMrGpuTixrMyVgGySwaV9No5FSUBeyApvj_wVTQQ:1vJ0mq:Och04DIvV85TcvC9gz-ncEdMeX9rN0nhGsUj5Ue2SR0','2025-11-12 03:10:44.697443'),
('1x531uutp85a6hrpidg4v5cvzscf8jr9','e30:1vKmoR:DyKl0LOzkl2YqKscibMxCoXIL2gj7qe85CmqA3BWMt0','2025-11-17 00:39:43.515023'),
('3dugo5e0texn9voxwpbxblw72v9agofi','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vKmoT:NTiz_0QuBUeW6Q0Y7wy_E7LBTnCamnzJu0VQ3RCGIRM','2025-11-17 00:39:45.208318'),
('3zeqwh3fsob55k4dejb7iwyd8gxl6ani','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vKiUi:r5HTfnCA9f16ijWA8vWm-5LwKmB6BZAwlOgOXToQl1c','2025-11-16 20:03:04.110507'),
('45xvd03f8320w8nqbas1thdcyte0rs82','e30:1vKmoS:t9Kn_N_0Y8mrtamtqyUT-l3Mak4SnYfDE0wnujw6kWc','2025-11-17 00:39:44.672950'),
('4i45m3pq1tmvritn625asrs336w4o3dt','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLbTc:b9NStlwA741dM6vywaUIFDutxtRnUbDJUxnINJmnhuA','2025-11-19 06:45:36.770525'),
('4o1juy1js6uzpzxbc1f1vy2p7o9qmmao','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLbx8:oVd_h6O6yK2kX6EUm1lfSmHGEJIEcuczDGpUmy9ZPY4','2025-11-19 07:16:06.832863'),
('5wzhvsjxozptldjc905hnsnrlvxysypp','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIgME:ilt-wHhBE0F_NysRgBFUOGbqizy3TX-KvWNKSl-ZA6Y','2025-11-11 05:21:54.651860'),
('67rsni9cwqm8wxlpfkmkpt7z33xej8zj','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLloD:NoA2eD5_0tgd6gNyD7ZJFBgnDheg5PX_07-crFmnqK0','2025-11-19 17:47:33.674842'),
('7xptugvgsjd703yzfdjjgkenomnl9s8p','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLRbz:vBq1Wn1GBkMhxj5ksyv5LzLJf0aywo3BtSLvquxK49o','2025-11-18 20:13:35.449714'),
('89r09clgohe0hy8vdlrmc4s7erbh4nga','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJjemRkdXEtM2FlMGY4NjBjZmM3MjMzNWFmNWYwM2M2NTQ2ZTVkMGIifQ:1vKljN:tVJ_oFxbqZ3JRE4hJ2dW5cEJwm3sx-QFTUY8dsyaOL4','2025-11-16 23:30:25.642235'),
('95iy36gkr52791bc838x96akw5eqcfdj','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vGhsl:bAR-UZ8YZrMkwtXcdDR67t9oVukjXV_LQj8-Hp0re_M','2025-11-05 18:35:19.513573'),
('a8ap3lfw9nnsx5w3x2nwl00nyc892q52','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIb27:MPdMtL_0UL3bUXU9gElXas-9sk-uQwihGvA_2LVaBgg','2025-11-10 23:40:47.461407'),
('c9ou8k6b0tw8bijqvznsv4vlb69qii4u','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLQ1m:zUCo5XGzjNm4dj7fmqoqgj0wXdLGzrkOUeJJjtJqX_o','2025-11-18 18:32:06.999472'),
('cxe8jk0vkct3s3sdznpwjfk0x983bu8t','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vKnTJ:VoMCLHDhYWH6N765w8vklSLD19ltJ6ADnU2WvLq_XP8','2025-11-17 01:21:57.453419'),
('cy26qyc2mwnaoyejm37316tw6czopo8p','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLQ2w:JMl6ZZwZNoj4mWeN9dzZnHm8a6O10EmKr9BTg72QVUc','2025-11-18 18:33:18.451912'),
('grhfwtk45vt2wj2mj3mksw2xoz1fxp91','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIsjm:lFNgZNE0-KeOA_NDMrHxdYcuFeRpcDn9eFPoKjlDEnc','2025-11-11 18:35:02.722637'),
('gsi56adgadgaf3vzyguk54nlhess3vsk','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIfkh:T1k6oGwfSwlLwGDwjTtggJzEB6BGvMflk1qReqt-H1U','2025-11-11 04:43:07.003640'),
('j94jq4aajl46e3ie6s11py05yooj694b','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLcTM:572P3HOY_88ojtNOZZW4Cna6IbBxlnhtOZjyYb7-vRA','2025-11-19 07:49:24.444835'),
('k69s93eoylqu1dp9cubclqkgzndqwe4d','.eJxVi7EOwiAURf_lzaYpRR7U0b3fQG6BF4hGEyiT8d-tSQcd7nLuOS_y6Fv2vaXqS6QLaTr9shXhlh7fo7eOWp7DQdqwYKsl9Duuh_MXZrS8V1YkBQSWoNwUlZ5mnIERVmbHBsnJyqN2UNqwsUasAZzmpPZxjEzvDzPnNYg:1vIhuE:TxnNpigddwEL3ebzcjAohc0zknZLF_-xC41FYVbjjQI','2025-11-11 07:01:06.435039'),
('kaskelz5802giiq5zyarweob8zvhail6','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIcum:gDrW-cT8DV88E_iz-YHOi2lpp7IbYedH9_kd_r-ZHNc','2025-11-11 01:41:20.567064'),
('ny7p4iogjoounz9m1iywrxn6fdg93w3q','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIvEC:2stTbeg0b2WVlMRpYuQPe57MAwW9jRU2FTGh_iy_000','2025-11-11 21:14:36.155926'),
('oua4x4q0457hcta33jljx2ygjaam7rxs','.eJxVy8sOwiAQheF3YW2agSk3l-59BjIMJRCNJlBWxne3Tbqo2--c_yMCjbWE0ZcWahJXMYvL2SLxY3ntw-iDWn1Ph_TpTmurPJ50Oz5_YaFetgozAkttAaVLGSBq65EikMrGpuTixrMyVgGySwaV9No5FSUBeyApvj_wVTQQ:1vJ1Hr:xKv2lpmTDbCURjyzC2HohjCuYDOZ8OWYlWkuU9Mlb6M','2025-11-12 03:42:47.985733'),
('pi6brpbwvyrihsa1ck9oxhtlcdydlfv1','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLZdW:JFscRgJMotWK6MYMKkFpJKUM2ymhg5zFx3LL0GVK_ok','2025-11-19 04:47:42.826218'),
('s6i8envy0jxfsbcu9joc630vnzb9s84z','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIbgT:JMv-TICAq_Xh-y8LAvOCRIh6a_cCWxTFa_ikUMHOIJ4','2025-11-11 00:22:29.458148'),
('sewedwj73l367avb06u6swaz0xiojdxk','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vKpx5:Jfa1Orkrf67QvKp3bXbsWrhoFMG9Q9rDqCkPlgf_Ihw','2025-11-17 04:00:51.159181'),
('sgqc8gl9mkgulpabk7jr6rxp9jm9w17l','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIh9D:UXgPKa7LLi4uVOnhabbzVallv_hsV_DQeUXxvrUW0aY','2025-11-11 06:12:31.390367'),
('su90nes7pbml0gqidbm7j4zednn2cloj','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIdvj:XVKW9xH-wCEZKQn19lX-y4ScOD-Xk-YoDCYFVfpA1To','2025-11-11 02:46:23.006407'),
('t4lrokvoq7f1jw3voxsekmyx0hgyee2o','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLlJS:vqiOg2uDQT_6CEjUZp3kxIHHKwvB4p_cgPAXKECieAo','2025-11-19 17:15:46.165053'),
('t5tfnzhyeo4fojb1uhpttgqsd2fbkcwf','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIei7:uIO0bnRfNPbu5VxViZpyrgQaZLu5eFegiLKhvX-5mIU','2025-11-11 03:36:23.548784'),
('ter7s9i0wpropflcgk08xrwjldxpp54m','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIdQc:5WFEYhB1UFx9uhPhvfIAyr_M8ggEQOJHfeqo6W_-g9Y','2025-11-11 02:14:14.821488'),
('v2c1uo0n0udpje7djyl8ez0rn1tkkn1x','e30:1vJ0bj:aBzvjYJxekYqzq8DKUQ6i7rpVRBxwMwgCtU1CC2FdnA','2025-11-12 02:59:15.545462'),
('vlvexf1ww6e9j7kkypxkz5ghsla62nr8','e30:1vIhsG:ZIuXT3FH8ge0x4wiBVgOkoIHYnXWCZXj6lZqA1-PuTE','2025-11-11 06:59:04.326879'),
('vzvvthhsm15yjvls1z3uowg4taclwx3v','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIaWQ:S_uHn6Q177zCXPhy2txBk-r_rAnlCVC7MSdcT_no8g4','2025-11-10 23:08:02.073806'),
('x6orhd355pdvrm4gwhoxqbo0xwy0o6tv','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vIKM5:hwUmf4b8Lcyl4OPzeuZDBGl8z1Ev4XjQmZEw7T-665s','2025-11-10 05:52:17.708823'),
('xpwzc41uy0r36xt4nur3zjlcwuj1vlgt','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLR7a:cog9LQ2y6goH7pBzAKIPWOAlt1_uudSVzkIZjr1v4DE','2025-11-18 19:42:10.016171'),
('ybl4hgu2wy5rmra7wzkztvse78vzwb7l','.eJxVizsOAiEQQO9CbTZ8hJ2xtPcMZBiGQDSawFIZ764mW2j7Pk8VaW41ziE9tqxOyqjDL0vEV7l_xRyTenssOxnLhbbeeN7ovDd_Y6VRP5egQNLeWQOlAByDCCOjhZKsC6GI9YGdJMqwGtLFZ61xRWMRiTx59XoDGi81NA:1vKqXo:iVJX-PEqixgTJu7JjIXTeK4NhnQCPFH1_379WYqXxoI','2025-11-17 04:38:48.160090'),
('zh3m8y66h4nzmnszksoq7ndfqme7mo86','.eJxVizsOwyAQBe9CHVksn4BTpvcZ0AK7AiVKJDBVlLvbllwkzSvmzXxEwLGWMDq1ULO4CRCXXxYxPeh1HKMPbPU9naRPC66tpvHE--n8hQV72StExnRVjiFraRWzJyO9NgDWZLAzRaccemOTiSTJuSwVzzpLjsD7iO8GF_Y1aw:1vLazE:cxjPGbbPYEaGPccvHL8hUE2bp4AAnhSppT__vRed99A','2025-11-19 06:14:12.799429');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `eventos_eventoambiental`
--

DROP TABLE IF EXISTS `eventos_eventoambiental`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos_eventoambiental` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(150) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_inicio` datetime(6) NOT NULL,
  `fecha_fin` datetime(6) DEFAULT NULL,
  `creado_en` datetime(6) NOT NULL,
  `actualizado_en` datetime(6) NOT NULL,
  `organizador_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `eventos_eventoambien_organizador_id_517feff0_fk_usuario_u` (`organizador_id`),
  CONSTRAINT `eventos_eventoambien_organizador_id_517feff0_fk_usuario_u` FOREIGN KEY (`organizador_id`) REFERENCES `usuario_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_eventoambiental`
--

LOCK TABLES `eventos_eventoambiental` WRITE;
/*!40000 ALTER TABLE `eventos_eventoambiental` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `eventos_eventoambiental` VALUES
(1,'Cafe cantante','Bailes, Coro','2025-11-18 03:34:00.000000','2025-11-26 07:34:00.000000','2025-11-17 03:32:35.130818','2025-11-17 03:32:35.130866',1),
(2,'Dia del maiz','Mucho maiz','2025-11-17 03:59:00.000000','2025-11-18 18:01:00.000000','2025-11-17 03:58:02.101108','2025-11-17 03:58:02.101130',2),
(3,'Dia Upemor','Puestos de comida','2025-11-28 17:53:00.000000','2025-11-28 21:00:00.000000','2025-11-18 17:53:27.737111','2025-11-18 17:53:27.737150',1);
/*!40000 ALTER TABLE `eventos_eventoambiental` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificaciones_notificacion`
--

LOCK TABLES `notificaciones_notificacion` WRITE;
/*!40000 ALTER TABLE `notificaciones_notificacion` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `notificaciones_notificacion` VALUES
(1,'warning',46,46,'Recordatorio: Poda para Girasol',0,1,0,'2025-11-11 05:30:49.549713',22,3,22),
(2,'warning',47,47,'Recordatorio: Poda para MariaJuana',0,1,0,'2025-11-11 05:58:46.261189',22,3,22),
(3,'warning',49,49,'Recordatorio: Fumigación para MariaJuana',0,1,0,'2025-11-11 06:45:06.281675',22,3,22),
(4,'warning',50,50,'Recordatorio: Riego para Girasol',1,1,0,'2025-11-11 18:00:06.130257',22,3,22),
(5,'warning',59,59,'Recordatorio: Fumigación para Gerbera',1,1,0,'2025-11-19 07:10:06.357177',22,3,22);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respaldo_backupaudit`
--

LOCK TABLES `respaldo_backupaudit` WRITE;
/*!40000 ALTER TABLE `respaldo_backupaudit` DISABLE KEYS */;
set autocommit=0;
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_usuario`
--

LOCK TABLES `usuario_usuario` WRITE;
/*!40000 ALTER TABLE `usuario_usuario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `usuario_usuario` VALUES
('pbkdf2_sha256$1000000$K0stJNxiXhLCG4yJjDg33i$tkyh4Hw8UQUwQKkzfBUJD9CqioAjcdSLIHxCzUnZLL0=','2025-11-19 17:17:33.655988',1,1,'VUGO222163','vugo222163@upemor.edu.mx','Gadiel Villafuerte Uribe','administrador',1,1),
('pbkdf2_sha256$1000000$vSXO0hbsVnmQjTuu9TSBf3$oeKSaEat1NC7ewK82muqsdMPLIfKli9dRuOpwo0Cl7E=',NULL,0,2,'aoco220155','aoco220155@upemor.edu.mx','Carlos Gerardo Ascencio Onofre','mantenimiento',1,0),
('pbkdf2_sha256$1000000$QfWAPk99iPg2uNGml2wIzF$weSVSOAwAGAU/xHL+RqNHXsQbUo4Ajx+1wOFuDi2opo=','2025-11-11 18:04:18.760163',0,3,'tgro220987','gadielvillaf@gmail.com','Gadiel Villafuerte','mantenimiento',1,0),
('pbkdf2_sha256$1000000$wFAqBAgrNWFO7Jf5IOF6YU$Kvxs3PyiOFud2E0MltH3AIuXD1OuyfbZIyxd/CpOPKM=','2025-11-12 03:12:47.973267',0,4,'VUMO193455','im.monvu07@gmail.com','Villafuerte Uribe Monserrat','administrador',1,0),
('pbkdf2_sha256$1000000$4LjhC5RULYrU0rHfYRanDB$/cQ5oLZRCqJS4pSSRmWIe4ODDGHT4Iw2ADUniQ2l3x0=',NULL,0,5,'NSAO22134','NSAO220388@upemor.edu.mx','Axel Nava Sanchez','mantenimiento',1,0);
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

-- Dump completed on 2025-11-19 11:17:50
