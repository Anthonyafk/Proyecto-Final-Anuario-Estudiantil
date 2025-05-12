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
VALUES (100001, 1);

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

