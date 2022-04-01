DROP DATABASE IF EXISTS projet_glo2005;
CREATE DATABASE IF NOT EXISTS projet_glo2005 CHARACTER SET utf8;

CREATE USER IF NOT EXISTS 'newUser'@'localhost' IDENTIFIED BY 'newUserPassword';
GRANT ALL privileges ON projet_glo2005.* TO 'newUser'@'localhost';
FLUSH PRIVILEGES;

ALTER DATABASE projet_glo2005 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;