/*
	Inserta marcos de perfil. 
	Son los premios por ganar una nominación.
*/

INSERT INTO app_marco ("marco", "es_multiple")
VALUES 
  ('marco/Marco1.png', false),
  ('marco/Marco2.png', false),
  ('marco/Marco3.png', false),
  ('marco/Marco4.png', false),
  ('marco/Marco5.png', false),
  ('marco/Marco6.png', false),
  ('marco/Marco7.png', false),
  ('marco/Marco8.png', false);


/*
	Inserta nominaciones.
*/
INSERT INTO app_nominacion (categoria, descripcion, activa, mostrar_resultados, "premio_id")
VALUES 
  ('Más Participativo', 'Reconocimiento al alumno que mas ha participado en el grupo.', true, true, 1),
  ('Más Gracioso', 'Reconocimiento al alumno con los mejores chistes en el grupo.', true, true, 2),
  ('Mejor Peinado', 'Reconocimiento al alumno con el mejor estilo de cabello.', true, true, 3),
  ('Mejor Proyecto', 'Reconocimiento al mejor proyecto del año.', true, true, 4),
  ('Líder Inspirador', 'Reconocimiento al alumno por liderazgo destacado.', true, true, 5),
  ('Innovador del Año', 'Reconocimiento al alumno con ideas fuera de lo común.', true, true, 6),
  ('Compañero Ideal', 'Reconocimiento al alumno que siempre está dispuesto a ayudar a los demás.', true, true, 7),
  ('Espíritu Escolar', 'Reconocimiento al alumno que representa mejor los valores del grupo.', true, true, 8);


/*
	Activa las nominaciones asumiendo que tiene creado un grupo.

	Si ha creado otros grupos como administrador desde la aplicación, puede 
	asignar las mismas categorías a esos grupos modificando la segunda entrada 
	de cada tupla con un número n, donde 1 ≤ n ≤ #total de grupos creados como administrador.

 */
INSERT INTO app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
VALUES 
  (1, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59'),
  (2, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59'),
  (3, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59'),
  (4, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59'),
  (5, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59'),
  (6, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59'),
  (7, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59'),
  (8, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59');


