BEGIN TRANSACTION;
CREATE TABLE codigos_verificacion (
	id INTEGER NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	codigo VARCHAR(6) NOT NULL, 
	intentos INTEGER, 
	fecha_creacion DATETIME NOT NULL, 
	fecha_expiracion DATETIME NOT NULL, 
	usado BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE TABLE historial_carga (
	id INTEGER NOT NULL, 
	nombre_archivo VARCHAR(255) NOT NULL, 
	cantidad_registros INTEGER NOT NULL, 
	registros_procesados INTEGER NOT NULL, 
	registros_error INTEGER, 
	fecha_carga DATETIME NOT NULL, 
	estado VARCHAR(50), 
	mensaje_error TEXT, 
	usuario_carga VARCHAR(120), 
	PRIMARY KEY (id)
);
CREATE TABLE reportes (
	id INTEGER NOT NULL, 
	wo VARCHAR(50) NOT NULL, 
	usuario_asignado VARCHAR(120) NOT NULL, 
	fecha DATE NOT NULL, 
	horas_aprobadas FLOAT NOT NULL, 
	horas_reales FLOAT NOT NULL, 
	grupo VARCHAR(100) NOT NULL, 
	status VARCHAR(100), 
	tipo VARCHAR(50), 
	fecha_carga DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "reportes" VALUES(1,'WO-1256','Juan Pérez','2025-12-11',4.46,5.74,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.858260');
INSERT INTO "reportes" VALUES(2,'WO-8508','Carlos López','2025-12-11',5.49,8.79,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(3,'WO-7498','Juan Pérez','2025-12-11',6.42,9.18,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(4,'WO-2244','Ana Martínez','2025-12-12',5.94,5.73,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(5,'WO-4608','José Rodríguez','2025-12-12',6.27,7.87,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(6,'WO-5018','José Rodríguez','2025-12-12',6.08,8.53,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(7,'WO-5106','Juan Pérez','2025-12-12',6.34,5.16,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(8,'WO-6120','María García','2025-12-12',4.27,4.07,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(9,'WO-4365','Laura Fernández','2025-12-13',6.05,7.37,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(10,'WO-6313','Juan Pérez','2025-12-13',7.66,9.99,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(11,'WO-3140','Miguel Sánchez','2025-12-13',7.74,8.23,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(12,'WO-2860','Miguel Sánchez','2025-12-13',6.77,8.43,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(13,'WO-6685','Isabel Gómez','2025-12-14',4.97,6.84,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(14,'WO-5774','Laura Fernández','2025-12-14',7.77,6.81,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(15,'WO-2025','Juan Pérez','2025-12-14',7.9,9.95,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(16,'WO-9171','Carlos López','2025-12-14',5.76,7.82,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(17,'WO-1838','Laura Fernández','2025-12-14',6.55,7.55,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(18,'WO-4260','Francisca Díaz','2025-12-15',7.05,4.28,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(19,'WO-3781','Miguel Sánchez','2025-12-15',4.03,8.79,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(20,'WO-7293','Laura Fernández','2025-12-15',5.74,9.8,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(21,'WO-7980','Antonio Ruiz','2025-12-15',5.05,8.75,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(22,'WO-4793','Antonio Ruiz','2025-12-16',4.5,5.6,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(23,'WO-1556','Francisca Díaz','2025-12-16',6.96,6.36,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(24,'WO-3136','Juan Pérez','2025-12-16',4.56,7.82,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(25,'WO-7470','Juan Pérez','2025-12-16',6.3,5.24,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(26,'WO-5572','José Rodríguez','2025-12-17',7.41,7.34,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(27,'WO-3872','José Rodríguez','2025-12-17',4.68,8.28,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(28,'WO-9624','Ana Martínez','2025-12-17',4.76,5.76,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(29,'WO-6500','Carlos López','2025-12-17',5.55,8.78,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(30,'WO-8863','Laura Fernández','2025-12-17',6.21,7.66,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(31,'WO-9323','Isabel Gómez','2025-12-18',7.29,7.59,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(32,'WO-4029','Isabel Gómez','2025-12-18',6.42,4.27,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(33,'WO-1457','Laura Fernández','2025-12-18',7.27,8.84,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(34,'WO-5196','José Rodríguez','2025-12-18',5.8,4.26,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(35,'WO-7587','Antonio Ruiz','2025-12-19',4.8,6.16,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(36,'WO-3539','Carlos López','2025-12-19',6.67,4.68,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(37,'WO-8985','Ana Martínez','2025-12-19',7.62,6.27,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(38,'WO-2628','Carlos López','2025-12-19',7.85,8.53,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(39,'WO-2402','Carlos López','2025-12-20',6.49,8.56,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(40,'WO-8883','Carlos López','2025-12-20',6.69,5.53,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(41,'WO-1460','Juan Pérez','2025-12-20',6.58,9.32,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(42,'WO-1110','Miguel Sánchez','2025-12-20',4.87,7.93,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(43,'WO-4813','María García','2025-12-21',7.19,9.27,'QA','Pending','Solicitud','2026-03-11 14:24:39.861324');
INSERT INTO "reportes" VALUES(44,'WO-9734','José Rodríguez','2025-12-21',5.06,4.93,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(45,'WO-8045','José Rodríguez','2025-12-21',5.15,7.44,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(46,'WO-1008','Laura Fernández','2025-12-21',5.88,8.03,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(47,'WO-8974','José Rodríguez','2025-12-22',6.2,6.64,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(48,'WO-3591','Ana Martínez','2025-12-22',5.59,7.04,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(49,'WO-8494','Laura Fernández','2025-12-22',6.92,6.22,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(50,'WO-6995','José Rodríguez','2025-12-23',6.03,6.53,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(51,'WO-5203','Francisca Díaz','2025-12-23',7.16,8.3,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(52,'WO-8483','Antonio Ruiz','2025-12-23',6.75,7.04,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(53,'WO-9332','Carlos López','2025-12-23',6.83,6.13,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(54,'WO-1611','José Rodríguez','2025-12-23',6.06,5.36,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(55,'WO-3682','María García','2025-12-24',4.67,7.57,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(56,'WO-5259','María García','2025-12-24',7.15,6.26,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(57,'WO-5710','Laura Fernández','2025-12-24',6.61,7.39,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(58,'WO-4394','Juan Pérez','2025-12-25',5.32,6.4,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(59,'WO-4211','María García','2025-12-25',4.67,4.29,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(60,'WO-3308','Laura Fernández','2025-12-25',5.09,6.51,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(61,'WO-3123','Antonio Ruiz','2025-12-26',7.31,7.67,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(62,'WO-7124','Ana Martínez','2025-12-26',7.44,8.73,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(63,'WO-5692','Isabel Gómez','2025-12-26',4.97,6.58,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(64,'WO-2034','José Rodríguez','2025-12-27',5.42,4.55,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(65,'WO-5276','Juan Pérez','2025-12-27',5.44,7.54,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(66,'WO-1397','Miguel Sánchez','2025-12-27',5.16,4.19,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(67,'WO-3389','María García','2025-12-27',5.78,4.66,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(68,'WO-6799','Carlos López','2025-12-28',7.16,6.42,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(69,'WO-3022','Isabel Gómez','2025-12-28',7.66,4.81,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(70,'WO-2236','Miguel Sánchez','2025-12-28',4.02,7.78,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(71,'WO-5607','Carlos López','2025-12-28',5.02,5.24,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(72,'WO-4319','María García','2025-12-28',6.35,7.09,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(73,'WO-5100','José Rodríguez','2025-12-29',7.44,6.27,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(74,'WO-7876','Juan Pérez','2025-12-29',6.09,9.92,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(75,'WO-5145','María García','2025-12-29',6.97,6.07,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(76,'WO-9383','Francisca Díaz','2025-12-30',6.72,5.08,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(77,'WO-5909','Francisca Díaz','2025-12-30',5.88,7.22,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(78,'WO-8558','Isabel Gómez','2025-12-30',4.63,7.7,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(79,'WO-3260','Carlos López','2025-12-31',5.91,8.21,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(80,'WO-7728','Laura Fernández','2025-12-31',5.77,5.35,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(81,'WO-1702','Carlos López','2025-12-31',6.82,4.37,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(82,'WO-1999','Isabel Gómez','2026-01-01',5.75,4.4,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(83,'WO-8325','Ana Martínez','2026-01-01',4.87,5.73,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(84,'WO-9074','Juan Pérez','2026-01-01',6.79,5.3,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(85,'WO-5032','Miguel Sánchez','2026-01-01',4.63,4.51,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(86,'WO-9731','Ana Martínez','2026-01-01',4.54,8.37,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(87,'WO-9201','José Rodríguez','2026-01-02',7.85,4.86,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(88,'WO-2461','Miguel Sánchez','2026-01-02',6.63,8.41,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(89,'WO-3157','Isabel Gómez','2026-01-02',7.46,9.05,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(90,'WO-1640','Carlos López','2026-01-02',7.34,4.5,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(91,'WO-1588','Miguel Sánchez','2026-01-02',7.62,8.48,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(92,'WO-9769','Carlos López','2026-01-03',4.55,6.63,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(93,'WO-1765','Ana Martínez','2026-01-03',6.84,9.63,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(94,'WO-2363','Juan Pérez','2026-01-03',7.0,6.7,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(95,'WO-7526','José Rodríguez','2026-01-04',4.28,6.5,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(96,'WO-4387','Antonio Ruiz','2026-01-04',4.63,5.52,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(97,'WO-4503','Miguel Sánchez','2026-01-04',5.26,7.51,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(98,'WO-7213','Antonio Ruiz','2026-01-04',4.82,5.4,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(99,'WO-5809','María García','2026-01-04',7.71,7.83,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(100,'WO-8591','Juan Pérez','2026-01-05',7.63,4.02,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(101,'WO-1016','José Rodríguez','2026-01-05',7.78,7.38,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(102,'WO-6858','Isabel Gómez','2026-01-05',5.08,7.1,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(103,'WO-8213','Carlos López','2026-01-05',6.72,6.24,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(104,'WO-3952','José Rodríguez','2026-01-06',4.7,6.21,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(105,'WO-7962','Francisca Díaz','2026-01-06',7.01,9.12,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(106,'WO-4107','Francisca Díaz','2026-01-06',7.47,5.85,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(107,'WO-6590','María García','2026-01-07',4.69,5.39,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(108,'WO-5428','Isabel Gómez','2026-01-07',7.78,5.89,'QA','Pending','Solicitud','2026-03-11 14:24:39.862849');
INSERT INTO "reportes" VALUES(109,'WO-5982','Antonio Ruiz','2026-01-07',5.95,7.73,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(110,'WO-9569','Laura Fernández','2026-01-08',5.59,9.4,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(111,'WO-4693','José Rodríguez','2026-01-08',7.49,9.18,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(112,'WO-2710','María García','2026-01-08',4.55,8.99,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(113,'WO-2264','María García','2026-01-09',5.44,6.68,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(114,'WO-2640','Juan Pérez','2026-01-09',5.76,6.85,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(115,'WO-8848','Francisca Díaz','2026-01-09',6.93,9.0,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(116,'WO-9099','María García','2026-01-09',7.12,6.75,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(117,'WO-3168','Laura Fernández','2026-01-09',5.24,5.72,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(118,'WO-2306','Laura Fernández','2026-01-10',4.13,5.25,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(119,'WO-6301','Juan Pérez','2026-01-10',5.79,6.74,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(120,'WO-4681','Isabel Gómez','2026-01-10',5.89,6.87,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(121,'WO-8853','Miguel Sánchez','2026-01-11',4.94,4.08,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(122,'WO-7574','José Rodríguez','2026-01-11',6.27,5.15,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(123,'WO-2668','Isabel Gómez','2026-01-11',6.1,6.26,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(124,'WO-2013','José Rodríguez','2026-01-12',5.82,5.51,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(125,'WO-5844','Antonio Ruiz','2026-01-12',6.54,5.74,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(126,'WO-7408','María García','2026-01-12',6.32,9.99,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(127,'WO-7536','Miguel Sánchez','2026-01-12',7.92,5.21,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(128,'WO-8312','Ana Martínez','2026-01-13',7.06,9.39,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(129,'WO-3292','Carlos López','2026-01-13',5.92,4.31,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(130,'WO-9161','Juan Pérez','2026-01-13',6.49,8.95,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(131,'WO-1305','Ana Martínez','2026-01-14',5.93,8.95,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(132,'WO-3905','José Rodríguez','2026-01-14',6.77,8.59,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(133,'WO-2127','Miguel Sánchez','2026-01-14',5.55,6.38,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(134,'WO-8932','Laura Fernández','2026-01-14',5.92,8.14,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(135,'WO-8395','Ana Martínez','2026-01-15',4.21,8.04,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(136,'WO-6386','José Rodríguez','2026-01-15',6.8,8.2,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(137,'WO-1966','Isabel Gómez','2026-01-15',4.44,8.91,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(138,'WO-4494','José Rodríguez','2026-01-15',4.16,6.11,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(139,'WO-8662','Antonio Ruiz','2026-01-15',4.58,7.5,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(140,'WO-6019','Juan Pérez','2026-01-16',7.83,8.02,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(141,'WO-2538','Francisca Díaz','2026-01-16',5.97,9.06,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(142,'WO-8367','Ana Martínez','2026-01-16',7.46,7.27,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(143,'WO-3048','Ana Martínez','2026-01-16',7.89,8.36,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(144,'WO-1515','Miguel Sánchez','2026-01-16',5.02,6.63,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(145,'WO-7192','Miguel Sánchez','2026-01-17',6.13,8.89,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(146,'WO-3246','Juan Pérez','2026-01-17',5.24,6.7,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(147,'WO-9260','José Rodríguez','2026-01-17',4.02,9.37,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(148,'WO-1154','Isabel Gómez','2026-01-17',5.61,6.9,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(149,'WO-7514','Isabel Gómez','2026-01-17',4.97,7.67,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(150,'WO-4662','Francisca Díaz','2026-01-18',7.87,8.61,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(151,'WO-9403','Juan Pérez','2026-01-18',4.1,5.53,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(152,'WO-2937','María García','2026-01-18',6.39,8.02,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(153,'WO-4451','Miguel Sánchez','2026-01-18',6.4,9.33,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(154,'WO-8921','Ana Martínez','2026-01-18',6.84,5.42,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(155,'WO-4829','María García','2026-01-19',7.67,6.39,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(156,'WO-3921','Francisca Díaz','2026-01-19',6.87,9.94,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(157,'WO-7369','María García','2026-01-19',4.3,4.7,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(158,'WO-9722','Laura Fernández','2026-01-19',5.43,7.86,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(159,'WO-7177','Francisca Díaz','2026-01-20',6.74,6.65,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(160,'WO-5157','Antonio Ruiz','2026-01-20',6.4,5.82,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(161,'WO-6898','Ana Martínez','2026-01-20',7.85,5.42,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(162,'WO-8673','Ana Martínez','2026-01-20',6.15,6.22,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(163,'WO-5070','Isabel Gómez','2026-01-20',7.11,8.09,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(164,'WO-5855','Antonio Ruiz','2026-01-21',6.01,6.16,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(165,'WO-7122','Miguel Sánchez','2026-01-21',7.73,5.05,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(166,'WO-7973','Antonio Ruiz','2026-01-21',7.6,6.47,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(167,'WO-1319','Miguel Sánchez','2026-01-21',6.13,8.92,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(168,'WO-3549','Antonio Ruiz','2026-01-21',5.04,9.6,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(169,'WO-1312','Miguel Sánchez','2026-01-22',7.73,8.81,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(170,'WO-7553','Francisca Díaz','2026-01-22',6.96,7.45,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(171,'WO-9785','Isabel Gómez','2026-01-22',5.44,8.83,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(172,'WO-1188','Laura Fernández','2026-01-23',5.98,7.61,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(173,'WO-2095','María García','2026-01-23',5.09,8.32,'QA','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(174,'WO-4053','Ana Martínez','2026-01-23',5.95,4.29,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(175,'WO-1951','Carlos López','2026-01-24',6.26,5.41,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.864366');
INSERT INTO "reportes" VALUES(176,'WO-5328','Juan Pérez','2026-01-24',7.38,6.44,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(177,'WO-7225','José Rodríguez','2026-01-24',5.67,8.7,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(178,'WO-8771','Antonio Ruiz','2026-01-24',5.99,7.16,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(179,'WO-9200','Juan Pérez','2026-01-24',5.29,6.72,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(180,'WO-4988','María García','2026-01-25',6.84,9.59,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(181,'WO-4935','Ana Martínez','2026-01-25',4.16,5.14,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(182,'WO-6245','Francisca Díaz','2026-01-25',5.9,7.05,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(183,'WO-6400','Antonio Ruiz','2026-01-26',4.13,6.91,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(184,'WO-8346','Isabel Gómez','2026-01-26',6.14,6.74,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(185,'WO-6225','José Rodríguez','2026-01-26',5.7,6.43,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(186,'WO-2795','José Rodríguez','2026-01-27',5.11,6.28,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(187,'WO-8583','Miguel Sánchez','2026-01-27',5.43,8.58,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(188,'WO-7986','Miguel Sánchez','2026-01-27',7.69,7.2,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(189,'WO-3940','Ana Martínez','2026-01-27',6.67,7.57,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(190,'WO-6529','Miguel Sánchez','2026-01-28',7.41,5.28,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(191,'WO-9764','Antonio Ruiz','2026-01-28',7.45,9.55,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(192,'WO-7870','Isabel Gómez','2026-01-28',6.91,9.53,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(193,'WO-7770','José Rodríguez','2026-01-29',4.3,7.84,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(194,'WO-6439','Miguel Sánchez','2026-01-29',7.69,6.37,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(195,'WO-7082','Isabel Gómez','2026-01-29',5.78,7.97,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(196,'WO-1267','Carlos López','2026-01-30',4.01,6.97,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(197,'WO-9534','Carlos López','2026-01-30',7.48,4.91,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(198,'WO-9985','Carlos López','2026-01-30',7.86,8.47,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(199,'WO-1110','María García','2026-01-30',6.1,4.32,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(200,'WO-5558','Isabel Gómez','2026-01-31',7.98,7.67,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(201,'WO-8067','Ana Martínez','2026-01-31',6.38,4.27,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(202,'WO-9476','Miguel Sánchez','2026-01-31',4.25,5.59,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(203,'WO-1259','Francisca Díaz','2026-02-01',6.52,7.43,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(204,'WO-3517','José Rodríguez','2026-02-01',6.45,8.13,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(205,'WO-8076','Isabel Gómez','2026-02-01',7.09,4.31,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(206,'WO-4569','Antonio Ruiz','2026-02-02',5.22,7.84,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(207,'WO-4753','Francisca Díaz','2026-02-02',4.25,5.69,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(208,'WO-3150','Miguel Sánchez','2026-02-02',4.96,9.23,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(209,'WO-3502','María García','2026-02-03',6.58,6.0,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(210,'WO-5946','Laura Fernández','2026-02-03',6.47,4.9,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(211,'WO-4383','Antonio Ruiz','2026-02-03',7.22,8.77,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(212,'WO-4832','Laura Fernández','2026-02-03',4.77,4.26,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(213,'WO-5386','Francisca Díaz','2026-02-03',6.04,9.33,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(214,'WO-5860','Miguel Sánchez','2026-02-04',5.77,8.9,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(215,'WO-5113','Ana Martínez','2026-02-04',6.62,5.64,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(216,'WO-1755','María García','2026-02-04',6.47,6.33,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(217,'WO-9535','Juan Pérez','2026-02-05',5.06,9.75,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(218,'WO-9552','Ana Martínez','2026-02-05',5.33,7.83,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(219,'WO-7370','Laura Fernández','2026-02-05',6.4,8.54,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(220,'WO-6687','Antonio Ruiz','2026-02-05',8.0,6.22,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(221,'WO-5412','Carlos López','2026-02-06',6.97,7.1,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(222,'WO-1091','Laura Fernández','2026-02-06',7.18,7.27,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(223,'WO-4419','Juan Pérez','2026-02-06',5.15,7.09,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(224,'WO-4228','María García','2026-02-07',4.83,9.7,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(225,'WO-4838','Juan Pérez','2026-02-07',4.72,6.09,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(226,'WO-6579','Miguel Sánchez','2026-02-07',4.17,4.35,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(227,'WO-4137','Miguel Sánchez','2026-02-07',5.37,8.52,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(228,'WO-2317','Antonio Ruiz','2026-02-08',7.14,6.45,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(229,'WO-8462','José Rodríguez','2026-02-08',7.99,9.79,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(230,'WO-4281','Laura Fernández','2026-02-08',5.2,6.85,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(231,'WO-5999','Carlos López','2026-02-08',6.15,9.94,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(232,'WO-2843','Francisca Díaz','2026-02-08',5.3,7.88,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(233,'WO-2769','Ana Martínez','2026-02-09',6.91,5.57,'QA','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(234,'WO-1423','Laura Fernández','2026-02-09',5.6,9.31,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(235,'WO-9557','Miguel Sánchez','2026-02-09',4.05,6.34,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(236,'WO-8322','Juan Pérez','2026-02-09',5.81,4.45,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(237,'WO-6688','Antonio Ruiz','2026-02-09',4.11,5.21,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(238,'WO-8866','Ana Martínez','2026-02-10',5.48,6.59,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(239,'WO-6084','Juan Pérez','2026-02-10',5.48,7.56,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(240,'WO-1731','Juan Pérez','2026-02-10',5.22,4.17,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(241,'WO-4524','Juan Pérez','2026-02-10',5.87,6.39,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.865885');
INSERT INTO "reportes" VALUES(242,'WO-5911','Ana Martínez','2026-02-11',7.12,4.2,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(243,'WO-7912','Laura Fernández','2026-02-11',4.64,7.14,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(244,'WO-8596','María García','2026-02-11',7.4,6.86,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(245,'WO-5852','Carlos López','2026-02-12',4.9,5.85,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(246,'WO-6883','Carlos López','2026-02-12',4.15,7.74,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(247,'WO-8013','Francisca Díaz','2026-02-12',5.36,7.28,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(248,'WO-5476','Laura Fernández','2026-02-12',7.76,4.6,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(249,'WO-6355','Antonio Ruiz','2026-02-13',6.43,8.79,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(250,'WO-8830','Laura Fernández','2026-02-13',4.03,4.01,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(251,'WO-7303','Miguel Sánchez','2026-02-13',4.98,6.49,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(252,'WO-2110','María García','2026-02-13',6.17,5.29,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(253,'WO-3412','Antonio Ruiz','2026-02-14',5.46,9.75,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(254,'WO-5780','Ana Martínez','2026-02-14',7.57,9.73,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(255,'WO-4874','Francisca Díaz','2026-02-14',6.32,9.38,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(256,'WO-6165','María García','2026-02-15',7.57,4.26,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(257,'WO-2144','José Rodríguez','2026-02-15',6.86,4.09,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(258,'WO-1314','Antonio Ruiz','2026-02-15',6.66,6.62,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(259,'WO-8128','Laura Fernández','2026-02-16',6.7,8.38,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(260,'WO-1106','Juan Pérez','2026-02-16',4.1,6.53,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(261,'WO-1093','Miguel Sánchez','2026-02-16',5.99,5.88,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(262,'WO-4668','Antonio Ruiz','2026-02-17',4.13,6.06,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(263,'WO-8377','Antonio Ruiz','2026-02-17',5.5,5.88,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(264,'WO-4508','Miguel Sánchez','2026-02-17',6.57,5.71,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(265,'WO-3916','Carlos López','2026-02-17',5.67,8.64,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(266,'WO-7707','María García','2026-02-17',4.84,9.53,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(267,'WO-7858','Miguel Sánchez','2026-02-18',4.96,9.91,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(268,'WO-2342','Juan Pérez','2026-02-18',7.82,7.26,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(269,'WO-1779','María García','2026-02-18',4.2,9.89,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(270,'WO-2755','Juan Pérez','2026-02-19',7.48,6.45,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(271,'WO-8397','José Rodríguez','2026-02-19',5.18,7.2,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(272,'WO-1234','Francisca Díaz','2026-02-19',4.05,4.38,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(273,'WO-8454','Juan Pérez','2026-02-20',6.22,4.5,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(274,'WO-1948','Carlos López','2026-02-20',6.1,5.14,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(275,'WO-2651','Francisca Díaz','2026-02-20',5.31,7.72,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(276,'WO-7436','María García','2026-02-20',6.05,6.24,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(277,'WO-8634','Ana Martínez','2026-02-21',5.44,8.44,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(278,'WO-1638','Carlos López','2026-02-21',7.33,7.35,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(279,'WO-1814','Ana Martínez','2026-02-21',6.23,9.35,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(280,'WO-5953','Laura Fernández','2026-02-21',4.57,5.83,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(281,'WO-3677','Miguel Sánchez','2026-02-22',5.47,5.83,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(282,'WO-9207','Carlos López','2026-02-22',5.44,7.64,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(283,'WO-6433','Laura Fernández','2026-02-22',6.03,7.02,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(284,'WO-4369','Ana Martínez','2026-02-22',4.78,4.58,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(285,'WO-1417','Francisca Díaz','2026-02-23',5.66,4.11,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(286,'WO-4002','Juan Pérez','2026-02-23',5.66,7.51,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(287,'WO-3045','Miguel Sánchez','2026-02-23',6.03,6.43,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(288,'WO-6140','Juan Pérez','2026-02-23',5.07,6.19,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(289,'WO-1579','Antonio Ruiz','2026-02-23',4.39,6.81,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(290,'WO-1118','Isabel Gómez','2026-02-24',5.1,6.93,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(291,'WO-8923','Francisca Díaz','2026-02-24',7.01,5.57,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(292,'WO-5077','Isabel Gómez','2026-02-24',4.73,7.68,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(293,'WO-2441','Ana Martínez','2026-02-25',6.23,5.25,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(294,'WO-5640','María García','2026-02-25',4.69,5.71,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(295,'WO-9183','Juan Pérez','2026-02-25',7.07,6.54,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(296,'WO-2528','Antonio Ruiz','2026-02-26',4.43,5.8,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(297,'WO-5949','Carlos López','2026-02-26',7.65,6.56,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(298,'WO-4415','María García','2026-02-26',5.11,9.31,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(299,'WO-7334','María García','2026-02-27',5.86,4.46,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(300,'WO-8728','Antonio Ruiz','2026-02-27',6.24,9.34,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(301,'WO-8227','Antonio Ruiz','2026-02-27',4.65,4.51,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(302,'WO-6747','Miguel Sánchez','2026-02-28',5.92,9.4,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(303,'WO-2155','Isabel Gómez','2026-02-28',4.42,9.07,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(304,'WO-7037','Ana Martínez','2026-02-28',4.58,5.97,'QA','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(305,'WO-7292','Francisca Díaz','2026-03-01',6.51,7.47,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.867416');
INSERT INTO "reportes" VALUES(306,'WO-4505','Juan Pérez','2026-03-01',5.87,6.53,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(307,'WO-9859','Ana Martínez','2026-03-01',6.25,5.33,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(308,'WO-8847','María García','2026-03-01',4.45,7.17,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(309,'WO-3557','Carlos López','2026-03-01',7.55,8.12,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(310,'WO-9122','José Rodríguez','2026-03-02',6.12,8.21,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(311,'WO-2563','Antonio Ruiz','2026-03-02',5.43,5.07,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(312,'WO-7526','Juan Pérez','2026-03-02',5.4,5.15,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(313,'WO-8637','José Rodríguez','2026-03-02',4.88,6.27,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(314,'WO-7425','Miguel Sánchez','2026-03-02',6.62,7.57,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(315,'WO-1455','Francisca Díaz','2026-03-03',6.58,9.8,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(316,'WO-9266','Francisca Díaz','2026-03-03',6.11,7.53,'QA','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(317,'WO-4017','Antonio Ruiz','2026-03-03',5.15,4.76,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(318,'WO-3151','Ana Martínez','2026-03-03',5.6,4.23,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(319,'WO-2721','Isabel Gómez','2026-03-04',6.48,8.15,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(320,'WO-2657','Carlos López','2026-03-04',5.34,7.53,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(321,'WO-3053','María García','2026-03-04',7.32,7.47,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(322,'WO-9786','Isabel Gómez','2026-03-04',6.46,7.76,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(323,'WO-9059','Laura Fernández','2026-03-04',6.76,4.34,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(324,'WO-5509','José Rodríguez','2026-03-05',5.72,8.2,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(325,'WO-1955','Laura Fernández','2026-03-05',6.61,4.5,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(326,'WO-8640','Ana Martínez','2026-03-05',6.85,8.44,'Diseño','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(327,'WO-7567','Francisca Díaz','2026-03-05',7.59,5.56,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(328,'WO-2208','Isabel Gómez','2026-03-05',5.96,9.92,'Análisis','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(329,'WO-3543','Antonio Ruiz','2026-03-06',4.48,9.26,'QA','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(330,'WO-9534','María García','2026-03-06',6.7,7.65,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(331,'WO-6202','Laura Fernández','2026-03-06',5.94,4.65,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(332,'WO-3512','Isabel Gómez','2026-03-06',7.01,9.73,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(333,'WO-2917','Antonio Ruiz','2026-03-06',4.16,6.1,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(334,'WO-8567','Juan Pérez','2026-03-07',7.61,4.41,'QA','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(335,'WO-6092','Antonio Ruiz','2026-03-07',6.64,5.8,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(336,'WO-6595','Ana Martínez','2026-03-07',4.6,9.31,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(337,'WO-7436','Antonio Ruiz','2026-03-07',7.3,4.19,'QA','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(338,'WO-2886','María García','2026-03-08',5.11,9.05,'QA','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(339,'WO-8419','Antonio Ruiz','2026-03-08',7.16,4.31,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(340,'WO-4204','Miguel Sánchez','2026-03-08',6.51,5.05,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(341,'WO-4682','Miguel Sánchez','2026-03-08',7.48,5.02,'QA','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(342,'WO-7518','Carlos López','2026-03-08',6.24,7.54,'QA','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(343,'WO-2262','Laura Fernández','2026-03-09',7.64,9.37,'QA','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(344,'WO-3555','Ana Martínez','2026-03-09',5.99,6.92,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(345,'WO-3331','José Rodríguez','2026-03-09',7.62,7.66,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(346,'WO-2743','Isabel Gómez','2026-03-10',5.83,4.79,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(347,'WO-9159','Ana Martínez','2026-03-10',7.83,4.55,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(348,'WO-9490','Carlos López','2026-03-10',4.47,9.66,'DevOps','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(349,'WO-6689','Isabel Gómez','2026-03-10',7.58,8.87,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
INSERT INTO "reportes" VALUES(350,'WO-8460','José Rodríguez','2026-03-10',7.33,5.74,'Desarrollo','Pending','Solicitud','2026-03-11 14:24:39.868935');
CREATE TABLE usuarios (
	id INTEGER NOT NULL, 
	nombre VARCHAR(120) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	rol VARCHAR(50), 
	activo BOOLEAN, 
	fecha_registro DATETIME NOT NULL, 
	ultimo_login DATETIME, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_usuarios_email ON usuarios (email);
CREATE INDEX ix_codigos_verificacion_email ON codigos_verificacion (email);
CREATE INDEX ix_codigos_verificacion_fecha_creacion ON codigos_verificacion (fecha_creacion);
CREATE INDEX ix_reportes_status ON reportes (status);
CREATE INDEX ix_reportes_usuario_asignado ON reportes (usuario_asignado);
CREATE INDEX ix_reportes_fecha ON reportes (fecha);
CREATE INDEX ix_reportes_grupo ON reportes (grupo);
CREATE INDEX idx_grupo_fecha ON reportes (grupo, fecha);
CREATE INDEX ix_reportes_tipo ON reportes (tipo);
CREATE INDEX idx_fecha_usuario ON reportes (fecha, usuario_asignado);
CREATE INDEX ix_reportes_wo ON reportes (wo);
CREATE INDEX idx_usuario_grupo ON reportes (usuario_asignado, grupo);
CREATE INDEX idx_usuario_fecha ON reportes (usuario_asignado, fecha);
CREATE INDEX idx_tipo ON reportes (tipo);
CREATE INDEX ix_historial_carga_fecha_carga ON historial_carga (fecha_carga);
COMMIT;
