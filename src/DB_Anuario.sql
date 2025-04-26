-------------------------------
-- 1. CREACIÓN DE TABLAS
-------------------------------

CREATE TABLE IF NOT EXISTS Usuario (
    numCuenta       INT     PRIMARY KEY,
    nombre          VARCHAR(50),
    primer_apellido VARCHAR(50),
    segundo_apellido VARCHAR(50),
    correoE         VARCHAR(100),
    nombre_usuario  VARCHAR(50),
    contraseña      VARCHAR(100),
    esEstudiante    BOOLEAN,
    esAdmin         BOOLEAN
);

CREATE TABLE IF NOT EXISTS Grupo (
    Codigo      INT     PRIMARY KEY,
    nombre      VARCHAR(100),
    descripción TEXT
);

CREATE TABLE IF NOT EXISTS Perfil (
    idPerfil     INT     PRIMARY KEY,
    foto_perfil  BYTEA,
    foto_portada BYTEA,
    biografía    TEXT
);

CREATE TABLE IF NOT EXISTS marcoFoto (
    idPerfil    INT,
    marco_foto  VARCHAR(100),
    PRIMARY KEY (idPerfil, marco_foto)
    -- FK a Perfil se añade abajo
);

CREATE TABLE IF NOT EXISTS Nominación (
    idNominación INT     PRIMARY KEY,
    categoria    VARCHAR(50),
    descripción  TEXT,
    fecha_inicio DATE,
    fecha_fin    DATE,
    premio       TEXT,
    numCuenta    INT        -- FK a Usuario
);

CREATE TABLE IF NOT EXISTS Publicación (
    idPublicación INT     PRIMARY KEY,
    numCuenta     INT,       -- FK a Usuario
    hora_creación TIME,
    fecha_creación DATE,
    descripción   TEXT,
    imagen        BYTEA
);

CREATE TABLE IF NOT EXISTS Comentario (
    idComentario  INT     PRIMARY KEY,
    contenido      TEXT,
    fecha_creación DATE,
    hora_creación  TIME,
    idPerfil       INT,      -- FK a Perfil
    numCuenta      INT       -- FK a Usuario
);

-- Tablas intermedias

CREATE TABLE IF NOT EXISTS Tener (
    numCuenta INT,
    idPerfil  INT,
    PRIMARY KEY (numCuenta)
    -- UNIQUE(idPerfil) y FKs se añaden abajo
);

CREATE TABLE IF NOT EXISTS Postular (
    numCuenta     INT,
    idNominación  INT,
    PRIMARY KEY (numCuenta, idNominación)
);

CREATE TABLE IF NOT EXISTS Votar (
    numCuenta     INT,
    idNominación  INT,
    alumnoVotado  INT,
    PRIMARY KEY (numCuenta, idNominación, alumnoVotado)
    -- FKs se añaden abajo
);

CREATE TABLE IF NOT EXISTS Gestionar (
    numCuenta INT,
    codigo    INT,
    PRIMARY KEY (numCuenta, codigo)
);

CREATE TABLE IF NOT EXISTS Pertenecer (
    numCuenta INT,
    codigo    INT,
    PRIMARY KEY (numCuenta, codigo)
);

CREATE TABLE IF NOT EXISTS Existe (
    idNominación INT,
    codigo       INT,
    fecha_inicio DATE,
    fecha_fin    DATE,
    PRIMARY KEY (idNominación, codigo)
);

CREATE TABLE IF NOT EXISTS Poseer (
    idComentario  INT,
    idPublicación INT,
    PRIMARY KEY (idComentario, idPublicación)
);

CREATE TABLE IF NOT EXISTS Ganar (
    idNominación INT,
    numCuenta    INT,
    premio       TEXT,
    PRIMARY KEY (idNominación, numCuenta)
    -- FKs se añaden abajo
);


-----------------------------------
-- 2. RESTRICCIONES 
-----------------------------------

-- Verificaciones en Usuario
ALTER TABLE Usuario
  ADD CONSTRAINT ck_usuario_numCuenta_range 
    CHECK (numCuenta BETWEEN 1 AND 999999999),
  ADD CONSTRAINT ck_usuario_correoE_format 
    CHECK (correoE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- 1–1 Usuario <--> Perfil
ALTER TABLE Tener
  ADD CONSTRAINT uq_tener_perfil UNIQUE(idPerfil),
  ADD CONSTRAINT fk_tener_usuario FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta),
  ADD CONSTRAINT fk_tener_perfil FOREIGN KEY(idPerfil)
    REFERENCES Perfil(idPerfil);

-- Perfil <-- marcoFoto
ALTER TABLE marcoFoto
  ADD CONSTRAINT fk_mf_perfil FOREIGN KEY(idPerfil)
    REFERENCES Perfil(idPerfil);

-- Usuario <-- Nominación
ALTER TABLE Nominación
  ADD CONSTRAINT fk_nom_usuario FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta);

-- Usuario <-- Publicación
ALTER TABLE Publicación
  ADD CONSTRAINT fk_pub_usuario FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta);

-- Perfil, Usuario <-- Comentario
ALTER TABLE Comentario
  ADD CONSTRAINT fk_com_perfil FOREIGN KEY(idPerfil)
    REFERENCES Perfil(idPerfil),
  ADD CONSTRAINT fk_com_usuario FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta);

-- Usuario, Nominación <-- Postular
ALTER TABLE Postular
  ADD CONSTRAINT fk_postular_usuario FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta),
  ADD CONSTRAINT fk_postular_nominacion FOREIGN KEY(idNominación)
    REFERENCES Nominación(idNominación);

-- Usuario, Nominación <-- Votar
ALTER TABLE Votar
  ADD CONSTRAINT fk_votar_emisor FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta),
  ADD CONSTRAINT fk_votar_nominacion FOREIGN KEY(idNominación)
    REFERENCES Nominación(idNominación),
  ADD CONSTRAINT fk_votar_receptor FOREIGN KEY(alumnoVotado)
    REFERENCES Usuario(numCuenta);

-- Usuario, Grupo <-- Gestionar
ALTER TABLE Gestionar
  ADD CONSTRAINT fk_gestionar_usuario FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta),
  ADD CONSTRAINT fk_gestionar_grupo FOREIGN KEY(codigo)
    REFERENCES Grupo(Codigo);

-- Usuario, Grupo <-- Pertenecer
ALTER TABLE Pertenecer
  ADD CONSTRAINT fk_pertenecer_usuario FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta),
  ADD CONSTRAINT fk_pertenecer_grupo FOREIGN KEY(codigo)
    REFERENCES Grupo(Codigo);

-- Nominación, Grupo <-- Existe
ALTER TABLE Existe
  ADD CONSTRAINT fk_existe_nominacion FOREIGN KEY(idNominación)
    REFERENCES Nominación(idNominación),
  ADD CONSTRAINT fk_existe_grupo FOREIGN KEY(codigo)
    REFERENCES Grupo(Codigo);

-- Comentario, Publicación <-- Poseer
ALTER TABLE Poseer
  ADD CONSTRAINT fk_poseer_comentario FOREIGN KEY(idComentario)
    REFERENCES Comentario(idComentario),
  ADD CONSTRAINT fk_poseer_publicacion FOREIGN KEY(idPublicación)
    REFERENCES Publicación(idPublicación);

-- Nominación, Usuario <-- Ganar
ALTER TABLE Ganar
  ADD CONSTRAINT fk_ganar_nominacion FOREIGN KEY(idNominación)
    REFERENCES Nominación(idNominación),
  ADD CONSTRAINT fk_ganar_usuario FOREIGN KEY(numCuenta)
    REFERENCES Usuario(numCuenta);

