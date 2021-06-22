#***** COMANDOS PARA MARIADB **************
#********** Consultar usuarios **************
#SELECT User FROM mysql.user;

#********** Eliminar usuario ****************
#DROP USER 'userpoo'@'%';

#********** Crear usuario *******************
#CREATE USER 'userpoo'@'%' IDENTIFIED BY '123Admin';

#********* crear todos los privilegios ***************	
#GRANT ALL privileges ON poo.* TO 'userpoo'@'%' IDENTIFIED BY "123Admin";
#FLUSH PRIVILEGES;

#******** crear privilegios individuales **************
#GRANT select,insert,update,delete ON poo.* TO 'userpoo'@'%' IDENTIFIED BY "123Admin";
#FLUSH PRIVILEGES;

#******** Quitar los permisos de usuario **************
#REVOKE ALL ON poo.* from 'userpoo'@'%';
#FLUSH PRIVILEGES;

#******** Dar los privilegios totales incluso GRANT OPTION ****************
GRANT ALL ON poo.* TO 'userpoo'@'%' IDENTIFIED BY "123Admin" WITH GRANT OPTION;
FLUSH PRIVILEGES;

#******** Mostrar privilegios *************
#SHOW GRANTS FOR 'userpoo'@'%';


#************ Crear la BBDD ***************
CREATE DATABASE  IF NOT EXISTS 'poo'
USE 'poo';

#*************** Crear tabla de tipo de clientes ***************
DROP TABLE IF EXISTS `tipoclientes`;
CREATE TABLE `tipoclientes` (
    `codigo` varchar(20) NOT NULL,
    `tipo` varchar(80) DEFAULT NULL,
    PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

#********** Crear tabla clientes ***********
DROP TABLE IF EXISTS `clientes`;
CREATE TABLE `clientes` (
    `codigo` int NOT NULL AUTO_INCREMENT,
    `nif` varchar(15) DEFAULT NULL,
    `nombre` varchar(150) DEFAULT NULL,
    `direccion` varchar(150) DEFAULT NULL,
    `poblacion` varchar(100) DEFAULT NULL,
    `provincia` varchar(60) DEFAULT NULL,
    `cp` varchar(5) DEFAULT NULL,
    `telefono` varchar(15) DEFAULT NULL,
    `email` varchar(150) DEFAULT NULL,
    `recargo` tinyint DEFAULT NULL,
    `tipoCliente` varchar(20) DEFAULT NULL COMMENT 'clave ajena a tipoCliente',
    `fechaAlta` date DEFAULT NULL,
    `observaciones` varchar(500) DEFAULT NULL,
    `tipoDocumento` int DEFAULT 0,    
    PRIMARY KEY (`codigo`),
    KEY `nombre` (`nombre`) /*!80000 INVISIBLE */,
    KEY `nif` (`nif`),
    KEY `tipocliente_idx` (`tipoCliente`),
    CONSTRAINT `tipocliente` FOREIGN KEY (`tipoCliente`) REFERENCES `tipoclientes` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

#********** Insertar datos de tipo cliente *************
INSERT INTO `poo`.`tipoclientes` (`codigo`, `tipo`) VALUES ('1', 'Sociedad Anonima');

#********** Para exportar la base de datos **************
# mysqldump -u username -p database_name > data-dump.sql (ejecutar en consola donde esta mysql instalado)