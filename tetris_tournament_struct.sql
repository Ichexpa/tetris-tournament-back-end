-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: tetris_tournament
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matches` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `round` tinyint NOT NULL DEFAULT '1',
  `player1_id` int unsigned DEFAULT NULL,
  `player2_id` int unsigned DEFAULT NULL,
  `score_p1` tinyint DEFAULT '0',
  `score_p2` tinyint DEFAULT '0',
  `winner_id` int unsigned DEFAULT NULL,
  `tournament_id` int unsigned DEFAULT NULL,
  `next_match_id` int unsigned DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `player1_id` (`player1_id`),
  KEY `player2_id` (`player2_id`),
  KEY `winner_id` (`winner_id`),
  KEY `fk_matches_tournament` (`tournament_id`),
  CONSTRAINT `fk_matches_tournament` FOREIGN KEY (`tournament_id`) REFERENCES `tournaments` (`id`) ON DELETE SET NULL,
  CONSTRAINT `matches_ibfk_1` FOREIGN KEY (`player1_id`) REFERENCES `players` (`id`) ON DELETE SET NULL,
  CONSTRAINT `matches_ibfk_2` FOREIGN KEY (`player2_id`) REFERENCES `players` (`id`) ON DELETE SET NULL,
  CONSTRAINT `matches_ibfk_3` FOREIGN KEY (`winner_id`) REFERENCES `players` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=190 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `matches_results`
--

DROP TABLE IF EXISTS `matches_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matches_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_id` int unsigned DEFAULT NULL,
  `player_id` int unsigned NOT NULL,
  `points` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_matches_result_player` (`player_id`),
  KEY `fk_matches_result_match` (`match_id`),
  CONSTRAINT `fk_matches_result_match` FOREIGN KEY (`match_id`) REFERENCES `matches` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_matches_result_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `organizers`
--

DROP TABLE IF EXISTS `organizers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizers` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_organizer_user_idx` (`user_id`),
  CONSTRAINT `fk_organizer_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `score` int unsigned DEFAULT '100',
  `user_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_player_user_idx` (`user_id`),
  CONSTRAINT `fk_student_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tournaments`
--

DROP TABLE IF EXISTS `tournaments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tournaments` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `capacity` int DEFAULT '8',
  `total_points` int NOT NULL,
  `organizer_id` int unsigned NOT NULL,
  `status` enum('Activo','En curso','Finalizado','Cancelado') NOT NULL DEFAULT 'Activo',
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `best_of` tinyint NOT NULL DEFAULT '3',
  PRIMARY KEY (`id`),
  KEY `fk_tournament_organizer` (`organizer_id`),
  CONSTRAINT `fk_tournament_organizer` FOREIGN KEY (`organizer_id`) REFERENCES `organizers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tournamentsxplayers`
--

DROP TABLE IF EXISTS `tournamentsxplayers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tournamentsxplayers` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `player_id` int unsigned NOT NULL,
  `tournament_id` int unsigned NOT NULL,
  `registered_data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `confirm_register_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `player_id` (`player_id`,`tournament_id`),
  KEY `fk_tournamentXplayers_player` (`player_id`),
  KEY `fk_tournamentXplayers_tournament` (`tournament_id`),
  CONSTRAINT `fk_tournamentXplayers_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`),
  CONSTRAINT `fk_tournamentXplayers_tournament` FOREIGN KEY (`tournament_id`) REFERENCES `tournaments` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varbinary(60) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'tetris_tournament'
--
/*!50003 DROP PROCEDURE IF EXISTS `create_player` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_player`(
	IN p_email VARCHAR(100),
    IN p_password VARBINARY(60),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    OUT user_id INT UNSIGNED
)
BEGIN
    -- Insert into users table
    INSERT INTO users (email, password, first_name, last_name, created_at)
    VALUES (p_email, p_password, p_first_name, p_last_name, NOW());
    
    SET user_id = LAST_INSERT_ID();
    
    -- Insert into students table
    INSERT INTO players (user_id)
    VALUES (user_id);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `create_tournament` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_tournament`(
	IN name VARCHAR(255),
    IN capacity INT,
    IN total_points INT,
    IN user_id INT,
    IN status varchar(100),
    IN start_date DATE,
    IN end_date DATE,
    IN best_of tinyint,
    OUT tournament_id INT)
BEGIN
	IF status IN('Activo','En curso','Finalizado','Cancelado') THEN
		INSERT INTO tournaments(name,capacity,total_points,organizer_id,status,start_date,end_date,best_of) 
		VALUE(name,capacity,total_points,(SELECT o.id FROM organizers o INNER JOIN users u ON u.id = p.user_id WHERE u.id=user_id),status,start_date,end_date,best_of);
        SET tournament_id = LAST_INSERT_ID();
	ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid status value';
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `generate_initial_matches` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `generate_initial_matches`(
    IN tournament_id INT, 
    IN player_ids_list VARCHAR(255)  -- Nueva entrada para recibir los IDs de los jugadores
)
BEGIN
    DECLARE total_rounds INT;
    DECLARE current_round INT;
    DECLARE num_matches INT;
    DECLARE num_players INT;
    DECLARE player_offset INT DEFAULT 1;  -- Empezar desde 1
    DECLARE player_id VARCHAR(10);
    DECLARE player1_id INT;
    DECLARE player2_id INT;
    DECLARE i INT;
    
    -- Obtengo la cantidad de jugadores permitidos en el torneo
    SET num_players = (SELECT capacity FROM tournaments WHERE id = tournament_id);

    -- Calcular el número total de rondas
    SET total_rounds = CEIL(LOG2(num_players));
    
    

    -- Crear partidos para cada ronda
    SET current_round = 1;

    -- Dividir la lista de IDs en partes
    WHILE current_round <= total_rounds DO
        -- Calcular el número de partidos en la ronda actual
        SET num_matches = POWER(2, total_rounds - current_round);

        SET i = 1;

        WHILE i <= num_matches DO
            SET player1_id = NULL;
            SET player2_id = NULL;

            -- Asignar jugadores aleatoriamente usando la lista de IDs
            IF current_round = 1 THEN
                -- Obtener el ID del primer jugador
                SET player1_id = SUBSTRING_INDEX(SUBSTRING_INDEX(player_ids_list, ',', player_offset), ',', -1);
                SET player_offset = player_offset + 1;

                -- Obtener el ID del segundo jugador
                SET player2_id = SUBSTRING_INDEX(SUBSTRING_INDEX(player_ids_list, ',', player_offset), ',', -1);
                SET player_offset = player_offset + 1;
            END IF;

            -- Insertar el partido en la tabla sin vincular (`next_match_id` será NULL)
            INSERT INTO matches (round, player1_id, player2_id, next_match_id, tournament_id)
            VALUES (current_round, player1_id, player2_id, NULL, tournament_id);

            -- Incrementar el contador del partido actual
            SET i = i + 1;
        END WHILE;

        -- Pasar a la siguiente ronda
        SET current_round = current_round + 1;
    END WHILE;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `link_tournament_matches` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `link_tournament_matches`(
    IN p_tournament_id INT
)
BEGIN
    DECLARE total_rounds INT;
    DECLARE current_round INT;
    DECLARE match_id INT;
    DECLARE next_match_id INT;
    DECLARE i INT;
    DECLARE match_offset INT;

    -- Calcular el número total de rondas
    SET total_rounds = (SELECT MAX(round) FROM matches WHERE tournament_id = p_tournament_id);

    -- Enlazar partidos desde la primera ronda hasta la penúltima
    SET current_round = 1;

    WHILE current_round < total_rounds DO
        -- Enlazar cada partido de la ronda actual
        SET i = 1;

        WHILE i <= (SELECT COUNT(*) FROM matches WHERE tournament_id = p_tournament_id AND round = current_round) DO
            -- Calcular el OFFSET para obtener el partido actual
            SET match_offset = i - 1;

            -- Obtener el ID del partido actual utilizando el OFFSET
            SELECT id INTO match_id
            FROM matches
            WHERE tournament_id = p_tournament_id AND round = current_round
            LIMIT 1 OFFSET match_offset;

            -- Calcular el OFFSET para el partido en la siguiente ronda
            SET match_offset = FLOOR((i - 1) / 2);

            -- Obtener el ID del partido en la siguiente ronda
            SELECT id INTO next_match_id
            FROM matches
            WHERE tournament_id = p_tournament_id AND round = current_round + 1
            LIMIT 1 OFFSET match_offset;

            -- Actualizar el `next_match_id` del partido actual
            UPDATE matches
            SET next_match_id = next_match_id
            WHERE id = match_id AND tournament_id = p_tournament_id;

            -- Incrementar el contador del partido actual
            SET i = i + 1;
        END WHILE;

        -- Pasar a la siguiente ronda
        SET current_round = current_round + 1;
    END WHILE;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-28 17:46:40
