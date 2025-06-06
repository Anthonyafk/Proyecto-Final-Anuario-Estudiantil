-- Usuario
INSERT INTO app_usuario ("numCuenta", nombre, primer_apellido, segundo_apellido, "correoE", nombre_usuario, contraseña, "esAdmin")
VALUES (100001, 'Juan', 'Pérez', 'López', 'juan.perez@ciencias.unam.mx', 'juanp', 'clave_segura123', FALSE);

-- Crear un grupo
INSERT INTO app_grupo (codigo, nombre, descripcion, foto_portada)
VALUES (DEFAULT, 'Grupo 1', 'Grupo de prueba para nominaciones', '');

INSERT INTO app_grupo (codigo, nombre, descripcion, foto_portada)
VALUES (DEFAULT, 'Grupo 2', 'otro grupo', '');

-- Obtener el ID del grupo insertado (si se usa secuencia)
-- Suponemos que el grupo tiene código = 1 (ajústalo si tu secuencia es diferente)

-- Asociar el usuario al grupo
INSERT INTO app_pertenecer ("numCuenta_id", codigo_id)
VALUES (117001778, 1);

INSERT INTO app_pertenecer ("numCuenta_id", codigo_id)
VALUES (114007889, 1);


-- Premios
INSERT INTO app_ganar ("premio_id", "activa", "idNominacion_id", "numCuenta_id")
VALUES (1, true, 4, 114007889);

INSERT INTO app_ganar ("premio_id", "activa", "idNominacion_id", "numCuenta_id")
VALUES (2, true, 2, 114007889);

-- Comentario
insert into app_comentario ("contenido", "fecha_creacion", "hora_creacion", "idPerfil_id", "numCuenta_id")
values ('Mi comentario dice hola', '2025-02-19', '08:00:00', 1, 114007889)

insert into app_comentario ("contenido", "fecha_creacion", "hora_creacion", "idPerfil_id", "numCuenta_id")
values ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2025-02-19', '24:00:00', 1, 114007889)


-- Marcos
insert into app_marco ("marco")
values ('marco/Marco1.png');

insert into app_marco ("marco")
values ('marco/Marco2.png');

-- Insertar 5 nominaciones
INSERT INTO app_nominacion (categoria, descripcion, activa)
VALUES 
  ('Mejor Proyecto', 'Reconocimiento al mejor proyecto del año', TRUE),
  ('Espíritu de Equipo', 'Para quien demuestra colaboración constante', TRUE),
  ('Líder Inspirador', 'Por liderazgo destacado', TRUE),
  ('Innovador del Año', 'Por ideas fuera de lo común', TRUE),
  ('Crecimiento Personal', 'Por superación personal notable', TRUE);

-- Crear el perfil del usuario
INSERT INTO app_perfil (foto_perfil, foto_portada, biografia)
VALUES ('', '', 'Biografía de Juan');

-- Obtener el ID del perfil creado (se asume es 1 si es el primero insertado)
-- Asociar usuario con perfil
INSERT INTO app_tener ("numCuenta_id", "idPerfil_id")
VALUES (100001, 1);

insert into app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
values 
	(1, 1, '2025-05-01 08:00:00', '2025-06-01 23:59:59'),
  	(2, 1, '2025-05-01 08:00:00', '2025-06-01 23:59:59'),
  	(3, 2, '2025-05-01 08:00:00', '2025-06-01 23:59:59'),
  	(4, 2, '2025-05-01 08:00:00', '2025-06-01 23:59:59'),
  	(4, 1, '2025-05-01 08:00:00', '2025-06-01 23:59:59');

INSERT INTO app_nominacion (categoria, descripcion, activa)
VALUES 
 ('No deberia aparecer', 'esta categoria no esta activa', False),
 ('Otra inactiva', ' categoria no activa', False);

insert into app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
values 
	(5, 2, '2025-05-01 08:00:00', '2025-06-01 23:59:59'),
  	(6, 1, '2025-05-01 08:00:00', '2025-06-01 23:59:59');

-- Alumnos Postulados en Nominaciones
  insert into app_postular ("idNominacion_id", "numCuenta_id")
	values 
  	(6, 100001);
