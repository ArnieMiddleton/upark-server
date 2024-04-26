DROP TABLE tst_upark.building;
CREATE TABLE tst_upark.building (id int unsigned NOT NULL, name varchar(128) NOT NULL, longitude decimal(20,16) NOT NULL, latitude decimal(20,16) NOT NULL, street_address varchar(64), enabled tinyint(1) DEFAULT 1, code varchar(32), PRIMARY KEY (id), INDEX building_name_idx (name)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 DEFAULT COLLATE=utf8mb3_general_ci;
DROP TABLE tst_upark.lot;
CREATE TABLE tst_upark.lot (id int unsigned NOT NULL, name varchar(64) NOT NULL, latitude decimal(20,16) NOT NULL, longitude decimal(20,16) NOT NULL, car_count int unsigned DEFAULT 0 NOT NULL, stall_count int unsigned NOT NULL, last_updated datetime, enabled tinyint(1) DEFAULT 1, PRIMARY KEY (id), INDEX lot_name_idx (name)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 DEFAULT COLLATE=utf8mb3_general_ci;
DROP TABLE tst_upark.permit;
CREATE TABLE tst_upark.permit (id int unsigned NOT NULL, name varchar(8) NOT NULL, PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 DEFAULT COLLATE=utf8mb3_general_ci;
DROP TABLE tst_upark.report;
CREATE TABLE tst_upark.report (id int NOT NULL AUTO_INCREMENT, user_id char(28) NOT NULL, lot_id int unsigned NOT NULL, longitude decimal(20,16), latitude decimal(20,16), time datetime DEFAULT CURRENT_TIMESTAMP NOT NULL, approx_fullness decimal(16,15) unsigned NOT NULL, weight int unsigned DEFAULT 1 NOT NULL, PRIMARY KEY (id), INDEX fk_report_user_id_idx (user_id), INDEX fk_report_lot_id_idx (lot_id), INDEX report_fullness_idx (approx_fullness)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 DEFAULT COLLATE=utf8mb3_general_ci;
DROP TABLE tst_upark.stall;
CREATE TABLE tst_upark.stall (lot_id int unsigned NOT NULL, stall_type_id int unsigned NOT NULL, PRIMARY KEY (lot_id, stall_type_id), INDEX fk_stall_stall_type_id (stall_type_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 DEFAULT COLLATE=utf8mb3_general_ci;
DROP TABLE tst_upark.stall_type;
CREATE TABLE tst_upark.stall_type (id int unsigned NOT NULL, name varchar(8) NOT NULL, PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 DEFAULT COLLATE=utf8mb3_general_ci;
DROP TABLE tst_upark.user;
CREATE TABLE tst_upark.user (id char(28) NOT NULL, name varchar(64) NOT NULL, colorblind tinyint(1) DEFAULT 0, PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 DEFAULT COLLATE=utf8mb3_general_ci;
DROP TABLE tst_upark.user_permit;
CREATE TABLE tst_upark.user_permit (user_id char(28) NOT NULL, permit_id int unsigned NOT NULL, PRIMARY KEY (user_id, permit_id), INDEX fk_user_permit_permit_id (permit_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 DEFAULT COLLATE=utf8mb3_general_ci;
ALTER TABLE `tst_upark`.`report` ADD CONSTRAINT fk_report_lot_id FOREIGN KEY (`lot_id`) REFERENCES `tst_upark`.`lot` (`id`) ;
ALTER TABLE `tst_upark`.`report` ADD CONSTRAINT fk_report_user_id FOREIGN KEY (`user_id`) REFERENCES `tst_upark`.`user` (`id`);
ALTER TABLE `tst_upark`.`stall` ADD CONSTRAINT fk_stall_lot_id FOREIGN KEY (`lot_id`) REFERENCES `tst_upark`.`lot` (`id`) ;
ALTER TABLE `tst_upark`.`stall` ADD CONSTRAINT fk_stall_stall_type_id FOREIGN KEY (`stall_type_id`) REFERENCES `tst_upark`.`stall_type` (`id`);
ALTER TABLE `tst_upark`.`user_permit` ADD CONSTRAINT fk_user_permit_permit_id FOREIGN KEY (`permit_id`) REFERENCES `tst_upark`.`permit` (`id`) ;
ALTER TABLE `tst_upark`.`user_permit` ADD CONSTRAINT fk_user_permit_user_id FOREIGN KEY (`user_id`) REFERENCES `tst_upark`.`user` (`id`);
DROP PROCEDURE tst_upark.create_tables;
--/
CREATE DEFINER=`u1287882`@`%` PROCEDURE tst_upark.create_tables()
BEGIN
CREATE TABLE IF NOT EXISTS `building` (
  `id` int unsigned NOT NULL,
  `name` varchar(128) NOT NULL,
  `longitude` decimal(20,16) NOT NULL,
  `latitude` decimal(20,16) NOT NULL,
  `street_address` varchar(64) DEFAULT NULL,
  `enabled` boolean DEFAULT TRUE,
  `code` VARCHAR(32),
  PRIMARY KEY (`id`),
  KEY `building_name_idx` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE IF NOT EXISTS `stall_type` (
    `id` INT UNSIGNED NOT NULL,
    `name` VARCHAR(8) NOT NULL,
    PRIMARY KEY (`id`)
)  ENGINE=INNODB AUTO_INCREMENT=7 DEFAULT CHARSET=UTF8MB3;

CREATE TABLE IF NOT EXISTS `permit` (
    `id` INT UNSIGNED NOT NULL,
    `name` VARCHAR(8) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE IF NOT EXISTS `lot` (
    `id` INT UNSIGNED NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `latitude` DECIMAL(20 , 16 ) NOT NULL,
    `longitude` DECIMAL(20 , 16 ) NOT NULL,
    `car_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `stall_count` INT UNSIGNED NOT NULL,
    `last_updated` DATETIME DEFAULT NULL,
    `enabled` BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (`id`),
    KEY `lot_name_idx` (`name`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB3;

CREATE TABLE IF NOT EXISTS `stall` (
    `lot_id` INT UNSIGNED NOT NULL,
    `stall_type_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`lot_id`, `stall_type_id`),
    CONSTRAINT `fk_stall_lot_id` FOREIGN KEY (`lot_id`) 
        REFERENCES `lot` (`id`),
    CONSTRAINT `fk_stall_stall_type_id` FOREIGN KEY (`stall_type_id`) 
        REFERENCES `stall_type` (`id`)
)  ENGINE=INNODB AUTO_INCREMENT=7 DEFAULT CHARSET=UTF8MB3;

CREATE TABLE IF NOT EXISTS `user` (
    `id` CHAR(28) NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `colorblind` BOOLEAN DEFAULT '0',
    PRIMARY KEY (`id`)
)  ENGINE=INNODB AUTO_INCREMENT=7 DEFAULT CHARSET=UTF8MB3;

CREATE TABLE IF NOT EXISTS `user_permit` (
    `user_id` CHAR(28) NOT NULL,
    `permit_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`user_id`, `permit_id`),
    CONSTRAINT `fk_user_permit_user_id` FOREIGN KEY (`user_id`) 
        REFERENCES `user` (`id`),
    CONSTRAINT `fk_user_permit_permit_id` FOREIGN KEY (`permit_id`) 
        REFERENCES `permit` (`id`)
)  ENGINE=INNODB AUTO_INCREMENT=7 DEFAULT CHARSET=UTF8MB3;

CREATE TABLE IF NOT EXISTS `report` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` CHAR(28) NOT NULL,
    `lot_id` INT UNSIGNED NOT NULL,
    `longitude` decimal(20,16),
    `latitude` decimal(20,16),
    `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `approx_fullness` DECIMAL(16 , 15 ) UNSIGNED NOT NULL,
    `weight` INT UNSIGNED NOT NULL DEFAULT 1,
    PRIMARY KEY (`id`),
    KEY `fk_report_user_id_idx` (`user_id`),
    KEY `fk_report_lot_id_idx` (`lot_id`),
    KEY `report_fullness_idx` (`approx_fullness`),
    CONSTRAINT `fk_report_lot_id` FOREIGN KEY (`lot_id`)
        REFERENCES `lot` (`id`),
    CONSTRAINT `fk_report_user_id` FOREIGN KEY (`user_id`)
        REFERENCES `user` (`id`)
)  ENGINE=INNODB AUTO_INCREMENT=1969 DEFAULT CHARSET=UTF8MB3;

END
/
DROP PROCEDURE tst_upark.reset_tables;
--/
CREATE DEFINER=`u1287882`@`%` PROCEDURE tst_upark.reset_tables()
BEGIN
    DECLARE `_rollback` BOOL DEFAULT 0;
    DECLARE rollback_message VARCHAR(255) DEFAULT 'Transaction rolled back: tables unaffected';
    DECLARE commit_message VARCHAR(255) DEFAULT 'Transaction completed: tables reset';
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET `_rollback` = 1;
    
    START TRANSACTION;
    
    -- Drop existing tables
    DROP TABLE IF EXISTS `building`;
    DROP TABLE IF EXISTS `user_permit`;
    DROP TABLE IF EXISTS `stall`;
    DROP TABLE IF EXISTS `report`;
    DROP TABLE IF EXISTS `user`;
    DROP TABLE IF EXISTS `permit`;
    DROP TABLE IF EXISTS `lot`;
    DROP TABLE IF EXISTS `stall_type`;
    
    -- Create tables from scratch
    CALL `create_tables`;
    
    -- Rollback if any errors
    IF `_rollback` THEN
        ROLLBACK;
    ELSE
        COMMIT;
    END IF;
END
/
