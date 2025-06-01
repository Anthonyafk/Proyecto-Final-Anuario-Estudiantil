/*
	Inserta marcos de perfil. 
	Son los premios por ganar una nominación.
*/

insert into app_marco ("marco")
values ('marco/Marco1.png');

insert into app_marco ("marco")
values ('marco/Marco2.png');

insert into app_marco ("marco")
values ('marco/Marco3.png');

insert into app_marco ("marco")
values ('marco/Marco4.png');

insert into app_marco ("marco")
values ('marco/Marco5.png');

insert into app_marco ("marco")
values ('marco/Marco6.png');

insert into app_marco ("marco")
values ('marco/Marco7.png');

insert into app_marco ("marco")
values ('marco/Marco8.png');


/*
	Inserta nominaciones.
*/
INSERT INTO app_nominacion (categoria, descripcion, activa, mostrar_resultados)
VALUES ('Más Participativo', 'Reconocimiento al alumno que mas ha participado en el grupo.', true, True);

INSERT INTO app_nominacion (categoria, descripcion, activa, mostrar_resultados)
VALUES ('Más Gracioso', 'Reconocimiento al alumno con los mejores chistes en el grupo.', true, True);

INSERT INTO app_nominacion (categoria, descripcion, activa, mostrar_resultados)
VALUES ('Mejor Peinado', 'Reconocimiento al alumno con el mejor estilo de cabello.', true, True);

INSERT INTO app_nominacion (categoria, descripcion, activa, mostrar_resultados)
VALUES ('Mejor Proyecto', 'Reconocimiento al mejor proyecto del año.', true, True);

INSERT INTO app_nominacion (categoria, descripcion, activa, mostrar_resultados)
VALUES ('Líder Inspirador', 'Reconocimiento al alumno por liderazgo destacado.', true, True);

INSERT INTO app_nominacion (categoria, descripcion, activa, mostrar_resultados)
VALUES ('Innovador del Año', 'Reconocimiento al alumno con ideas fuera de lo común.', true, True);


/*
	Activa las nominaciones asumiendo que tiene creado un grupo.

	Si ha creado otros grupos como administrador desde la aplicación, puede 
	asignar las mismas categorías a esos grupos modificando la segunda entrada 
	de cada tupla con un número n, donde 1 ≤ n ≤ #total de grupos creados como administrador.

 */
insert into app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
values (1, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59');

insert into app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
values (2, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59');

insert into app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
values (3, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59');

insert into app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
values (4, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59');

insert into app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
values (5, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59');

insert into app_existe("idNominacion_id", codigo_id, fecha_inicio, fecha_fin)
values (6, 1, '2025-05-01 08:00:00', '2025-07-01 23:59:59');


/*
	Asignación de Premios. 

	Reemplace el carácter '_' con el número de cuenta del usuario al que desee 
	asignarle un marco de perfil en la aplicación, con el fin de permitirle visualizar 
	los marcos de perfil sin necesidad de haber ganado una nominación.
*/

/*
INSERT INTO app_ganar ("premio_id", "activa", "idNominacion_id", "numCuenta_id" )
VALUES (5, true, 1, _ );

INSERT INTO app_ganar ("premio_id", "activa", "idNominacion_id", "numCuenta_id" )
VALUES (7, true, 2, _ );

INSERT INTO app_ganar ("premio_id", "activa", "idNominacion_id", "numCuenta_id" )
VALUES (6, true, 3, _ );

INSERT INTO app_ganar ("premio_id", "activa", "idNominacion_id", "numCuenta_id" )
VALUES (2, true, 4, _ );

INSERT INTO app_ganar ("premio_id", "activa", "idNominacion_id", "numCuenta_id" )
VALUES (3, true, 5, _ );

INSERT INTO app_ganar ("premio_id", "activa", "idNominacion_id", "numCuenta_id" )
VALUES (8, true, 6, _ );
*/