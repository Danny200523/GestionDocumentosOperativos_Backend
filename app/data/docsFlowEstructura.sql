CREATE DATABASE IF NOT EXISTS docsflow;
USE docsflow;

CREATE TABLE `departments` (
  `id_department` int PRIMARY KEY AUTO_INCREMENT,
  `name_department` varchar(255) NOT NULL
);

CREATE TABLE `users` (
  `id_user` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` text NOT NULL,
  `role` enum('admin','operator') NOT NULL DEFAULT 'operator',
  `id_department` int NOT NULL,
  CONSTRAINT `fk_users_department` FOREIGN KEY (`id_department`) REFERENCES `departments` (`id_department`) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE `extrated_data` (
  `id_table` int PRIMARY KEY AUTO_INCREMENT,
  `department_id` int NOT NULL,
  `table_data` json NOT NULL,
  CONSTRAINT `fk_extrated_data_department` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id_department`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `key_data` (
  `id_data` int PRIMARY KEY AUTO_INCREMENT,
  `department_id` int NOT NULL,
  `table_id` int NOT NULL,
  `key` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  CONSTRAINT `fk_key_data_department` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id_department`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_key_data_tabla` FOREIGN KEY (`table_id`) REFERENCES `extrated_data` (`id_table`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `reset_password_tokens` (
  `id_token` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `token` varchar(255) NOT NULL,
  CONSTRAINT `fk_reset_tokens_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `login_attempts` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `email` varchar(255) NOT NULL UNIQUE,
  `attempts` int NOT NULL DEFAULT 0,
  `is_blocked` bool NOT NULL DEFAULT false,
  `last_attempt` datetime NOT NULL
);


