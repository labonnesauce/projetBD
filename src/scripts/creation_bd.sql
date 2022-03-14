DROP DATABASE IF EXISTS glo_2005_webapp;
CREATE DATABASE IF NOT EXISTS glo_2005_webapp CHARACTER SET utf8;

DROP USER IF EXISTS 'newUser'@'localhost';
flush privileges;

CREATE USER 'newUser'@'localhost' IDENTIFIED BY 'newUserPassword';
GRANT ALL ON glo_2005_webapp.* TO 'newUser'@'localhost';