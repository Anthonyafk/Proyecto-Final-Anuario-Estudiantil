BEGIN;

INSERT INTO app_usuario (
    "numCuenta", nombre, primer_apellido, segundo_apellido, 
    "correoE", nombre_usuario, contraseña, "esAdmin"
) VALUES

(33001, 'Alondra',        'Felipe',      'Ramirez',        'AlondraFelp@ciencias.unam.mx',    'alfel33',   'pbkdf2_sha256$600000$ABC...XYZ', FALSE),
(33002, 'Dylan Enrique',  'Juarez',      'Martínez',       'DylanJuarez@ciencias.unam.mx',    'dyjua33',   'pbkdf2_sha256$600000$DEF...UVW', FALSE),
(33003, 'Eduardo',        'García',      'Gómez',          'EduardoGomez@ciencias.unam.mx',   'edgar33',   'pbkdf2_sha256$600000$GHI...RST', FALSE),
(33004, 'Fernanda Ixchel','Velazquez',   'Vilchis',        'FernandaV@ciencias.unam.mx',      'fvela33',   'pbkdf2_sha256$600000$JKL...MNO', FALSE),
(33005, 'Israel',         'Rivera',      '',             'IsraelRiv@ciencias.unam.mx',      'isriv33',   'pbkdf2_sha256$600000$OPQ...STU', FALSE),
(33006, 'Jimena',         'Ugalde',      'Flores',         'JimenaUgal@ciencias.unam.mx',     'jiuga33',   'pbkdf2_sha256$600000$VWX...YZA', FALSE),
(33007, 'Juan Carlos',    'Torres',      'Gongora',        'JuanCTorres@ciencias.unam.mx',    'jutor33',   'pbkdf2_sha256$600000$BCD...EFG', FALSE),
(33008, 'Kevin Steve',    'Quezada',     'Ordoñes',        'KevinQS@ciencias.unam.mx',        'keque33',   'pbkdf2_sha256$600000$HIJ...KLM', FALSE),
(33009, 'Marco',          'Flores',      'Cid',            'MarcoFlores@ciencias.unam.mx',    'maflo33',   'pbkdf2_sha256$600000$NOP...QRS', FALSE),
(33010, 'Regina',         'Razo',        'Castillo',       'ReginaRazo@ciencias.unam.mx',     'reraz33',   'pbkdf2_sha256$600000$TUV...WXY', FALSE),
(42001, 'Alberto Sebastián','Barradas',  'González',       'AlbertoSB@ciencias.unam.mx',      'albar42',   'pbkdf2_sha256$600000$ZAB...CDE', FALSE),
(42002, 'José Adolfo',    'Vázquez',     'Dávila',         'JoseAVaz@ciencias.unam.mx',       'jovaz42',   'pbkdf2_sha256$600000$FGH...IJK', FALSE),
(42003, 'Levi',           'Iparrea',     'Granados',       'LeviIparrea@ciencias.unam.mx',    'leipa42',   'pbkdf2_sha256$600000$LMN...OPQ', FALSE),
(42004, 'Pedro Joshue',   'Pintor',      'Muñoz',          'PedroPJ@ciencias.unam.mx',        'pepin42',   'pbkdf2_sha256$600000$QRS...TUV', FALSE),
(42005, 'Victor Manuel',  'Casarrubias', 'Casarrubias',    'VictorVC@ciencias.unam.mx',       'vicas42',   'pbkdf2_sha256$600000$WXY...ZAB', FALSE),

(11600, 'Moisés',         'Corpus',      'García',         'MoisesCG@ciencias.unam.mx',       'moico116',  'pbkdf2_sha256$600000$CDE...FGH', FALSE),
(11700, 'Nancy Elena',    'del Valle',   'Vera',           'NancyDV@ciencias.unam.mx',        'nadel117',  'pbkdf2_sha256$600000$IJK...LMN', FALSE),

(31201, 'Benjamín',       'Martínez',    '',             'BenjaminM@ciencias.unam.mx',      'benmar312', 'pbkdf2_sha256$600000$OPQ...RST', FALSE),
(31202, 'Edwin',          'Rodríguez',   'Nevarez',        'EdwinRN@ciencias.unam.mx',        'edwrod312', 'pbkdf2_sha256$600000$UVW...XYZ', FALSE),

(31500, 'Sergio',         'Mejía',       'Caballero',      'SergioMC@ciencias.unam.mx',       'sermej315', 'pbkdf2_sha256$600000$ABC...DEF', FALSE),
(31600, 'Ivette',         'González',    'Mancera',        'IvetteGM@ciencias.unam.mx',       'ivgon316',  'pbkdf2_sha256$600000$GHI...JKL', FALSE),

(31701, 'Huriel',         'Osorio',      'Escandon',       'HurielOE@ciencias.unam.mx',       'huros317',  'pbkdf2_sha256$600000$MNO...PQR', FALSE),
(31702, 'Irvin Javier',   'Cruz',        'Gónzalez',       'IrvinCJ@ciencias.unam.mx',        'ircruz317', 'pbkdf2_sha256$600000$STU...VWX', FALSE),

(31801, 'Karla',          'Clemente',    'Herrera',        'KarlaCH@ciencias.unam.mx',        'karcle318', 'pbkdf2_sha256$600000$YZA...BCD', FALSE),
(31802, 'Luis Ernesto',   'Hérnandez',   'Rosas',          'LuisHR@ciencias.unam.mx',         'luher318',  'pbkdf2_sha256$600000$EFG...HIJ', FALSE),
(31803, 'Roberto Samuel', 'Sánchez',     'Rosas',          'RobertoSR@ciencias.unam.mx',      'robsan318', 'pbkdf2_sha256$600000$KLM...NOP', FALSE),
(31804, 'Violeta Ardeni', 'Castillo',    'Camacho',        'VioletaVC@ciencias.unam.mx',      'vicas318',  'pbkdf2_sha256$600000$QRS...TUV', FALSE),

(31901, 'Alan Oliver',    'López',       'Robles',         'AlanLR@ciencias.unam.mx',         'alolop319', 'pbkdf2_sha256$600000$WXY...ZAB', FALSE),
(31902, 'Andres Rodrigo', 'Cataneo',     'Tortolero',      'AndresCT@ciencias.unam.mx',       'ancat319',  'pbkdf2_sha256$600000$CDE...FGH', FALSE),
(31903, 'Daniel',         'Alcántara',   'Andrade',        'DanielAA@ciencias.unam.mx',       'daalc319',  'pbkdf2_sha256$600000$IJK...LMN', FALSE),
(31904, 'David',          'Ortega',      'Medina',         'DavidOM@ciencias.unam.mx',        'daort319',  'pbkdf2_sha256$600000$OPQ...RST', FALSE),
(31905, 'Etni Sarai',     'Castro',      'Sierra',         'EtniCS@ciencias.unam.mx',         'etcas319',  'pbkdf2_sha256$600000$UVW...XYZ', FALSE),
(31906, 'Luis Gerardo',   'Estrada',     'García',         'LuisEG@ciencias.unam.mx',         'luesg319',  'pbkdf2_sha256$600000$ABC...DEF', FALSE),
(31907, 'Moisés',         'Lira',        'Rivera',         'MoisesLR@ciencias.unam.mx',       'molir319',  'pbkdf2_sha256$600000$GHI...JKL', FALSE),
(31908, 'Paola Mildred',  'Martínez',    '',             'PaolaMM@ciencias.unam.mx',        'pamart319', 'pbkdf2_sha256$600000$MNO...PQR', FALSE),
(31909, 'Ramón',          'Arcos',       'Morales',        'RamonAM@ciencias.unam.mx',        'raarc319',  'pbkdf2_sha256$600000$STU...VWX', FALSE),
(31910, 'Uziel Vidal',    'Cruz',        'Vargas',         'UzielCV@ciencias.unam.mx',        'uzcru319',  'pbkdf2_sha256$600000$YZA...BCD', FALSE),

(32001, 'Aldo Emilio',    'Jurado',      'Guadalupe',      'AldoJG@ciencias.unam.mx',         'aljur320',  'pbkdf2_sha256$600000$EFG...HIJ', FALSE),
(32002, 'Alejandro',      'Sánchez',     'Estrada',        'AlejandroSE@ciencias.unam.mx',    'alsan320',  'pbkdf2_sha256$600000$KLM...NOP', FALSE),
(32003, 'Alexa Paola',    'Ramírez',     'Venegas',        'AlexaRV@ciencias.unam.mx',        'alram320',  'pbkdf2_sha256$600000$QRS...TUV', FALSE),
(32004, 'Antonio',        'Castillo',    'Hernández',      'AntonioCH@ciencias.unam.mx',      'ancas320',  'pbkdf2_sha256$600000$WXY...ZAB', FALSE),
(32005, 'Ariadna Beatríz','Pérez',       'Aparicio',       'AriadnaPA@ciencias.unam.mx',      'arper320',  'pbkdf2_sha256$600000$CDE...FGH', FALSE),
(32006, 'Danna Lizette',  'Márquez',     'Corona',         'DannaMC@ciencias.unam.mx',        'damar320',  'pbkdf2_sha256$600000$IJK...LMN', FALSE),
(32007, 'Eris',           'Pérez',       'Evaristo',       'ErisPE@ciencias.unam.mx',         'erper320',  'pbkdf2_sha256$600000$OPQ...RST', FALSE),
(32008, 'Francisco Javier','Mendiola',  'Gutiérrez',      'FranciscoJM@ciencias.unam.mx',    'frmen320',  'pbkdf2_sha256$600000$UVW...XYZ', FALSE),
(32009, 'Ingrid Aylen',   'Martínez',    '',             'IngridMA@ciencias.unam.mx',       'inmar320',  'pbkdf2_sha256$600000$ABC...DEF', FALSE),
(32010, 'Itzel Paola',    'Flores',      'Carrillo',       'ItzelFC@ciencias.unam.mx',        'itflo320',  'pbkdf2_sha256$600000$GHI...JKL', FALSE),
(32011, 'Joshua',         'Juárez',      'Cruz',           'JoshuaJC@ciencias.unam.mx',       'josju320',  'pbkdf2_sha256$600000$MNO...PQR', FALSE),
(32012, 'Joshua Abel',    'Hurtado',     'Aponte',         'JoshuaAH@ciencias.unam.mx',       'joshur320', 'pbkdf2_sha256$600000$STU...VWX', FALSE),
(32013, 'Leslie Paola',   'Sánchez',     'Victoria',       'LeslieSV@ciencias.unam.mx',       'lesan320',  'pbkdf2_sha256$600000$YZA...BCD', FALSE),
(32014, 'Mauricio',       'Flores',      'Muñoz',          'MauricioFM@ciencias.unam.mx',     'mauflo320', 'pbkdf2_sha256$600000$EFG...HIJ', FALSE),
(32015, 'Miguel Akira',   'López',       'Asano',          'MiguelLA@ciencias.unam.mx',       'milop320',  'pbkdf2_sha256$600000$KLM...NOP', FALSE),
(32016, 'Raúl Emiliano',  'Labonne',     'Arizmendi',      'RaulLA@ciencias.unam.mx',         'ralab320',  'pbkdf2_sha256$600000$QRS...TUV', FALSE),
(32017, 'Victor Manuel',  'Mendiola',    'Montes',         'VictorMM@ciencias.unam.mx',       'vicmen320', 'pbkdf2_sha256$600000$WXY...ZAB', FALSE),

(41300, 'Yuznhio',        'Sierra',      'Casiano',        'YuznhioSC@ciencias.unam.mx',      'yusie413',  'pbkdf2_sha256$600000$CDE...FGH', FALSE);

COMMIT;