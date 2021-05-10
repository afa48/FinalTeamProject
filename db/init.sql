CREATE DATABASE crashesData;
use crashesData;

CREATE TABLE IF NOT EXISTS `crash_catalonia` (
    `id` int AUTO_INCREMENT,
    `Day_of_Week` VARCHAR(9) CHARACTER SET utf8,
    `Number_of_Crashes` INT,
    PRIMARY KEY (`id`)
);

INSERT INTO `crash_catalonia` (Day_of_Week, Number_of_Crashes) VALUES
    ('Sunday',13664),
    ('Monday',17279),
    ('Tuesday',17337),
    ('Wednesday',17394),
    ('Thursday',17954),
    ('Friday',19147),
    ('Saturday',15714);
