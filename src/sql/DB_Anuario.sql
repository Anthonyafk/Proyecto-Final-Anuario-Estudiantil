-------------------------------
-- 1. CREACIÓN DE TABLAS
-------------------------------

--------------------------------------------------------------------------------------------
-- Entidades
--------------------------------------------------------------------------------------------

-- Tabla: Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    numCuenta        INT             PRIMARY KEY,
    nombre           VARCHAR(50)     NOT NULL,
    primer_apellido  VARCHAR(50)     NOT NULL,
    segundo_apellido VARCHAR(50)     NOT NULL,
    correoE          VARCHAR(100)    UNIQUE NOT NULL,
    nombre_usuario   VARCHAR(50)     UNIQUE NOT NULL,
    contraseña       VARCHAR(12)     NOT NULL,
    esAdmin          BOOLEAN         NOT NULL DEFAULT FALSE
);

-- Tabla: Perfil
CREATE TABLE IF NOT EXISTS Perfil (
    idPerfil      SERIAL           PRIMARY KEY,
    foto_perfil   TEXT,
    foto_portada  TEXT,
    biografia     TEXT
);

-- Tabla: Grupo
CREATE TABLE IF NOT EXISTS Grupo (
    codigo        SERIAL           PRIMARY KEY,
    nombre        VARCHAR(50)      NOT NULL,
    descripcion   TEXT,
    foto_portada  TEXT
);

-- Tabla: Comentario
CREATE TABLE IF NOT EXISTS Comentario (
    idComentario    SERIAL         PRIMARY KEY,
    idPerfil        INT            NOT NULL,  -- FK a Perfil
    numCuenta       INT            NOT NULL,  -- FK a Usuario
    contenido       TEXT           NOT NULL,
    fecha_creacion  DATE           NOT NULL,
    hora_creacion   TIME           NOT NULL,
    FOREIGN KEY (idPerfil)
      REFERENCES Perfil(idPerfil)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (numCuenta)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Publicacion
CREATE TABLE IF NOT EXISTS Publicacion (
    idPublicacion   SERIAL         PRIMARY KEY,
    numCuenta       INT            NOT NULL,  -- FK a Usuario
    fecha_creacion  DATE           NOT NULL,
    hora_creacion   TIME           NOT NULL,
    descripcion     TEXT,
    imagen          TEXT,
    FOREIGN KEY (numCuenta)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Nominacion
CREATE TABLE IF NOT EXISTS Nominacion (
    idNominacion    SERIAL         PRIMARY KEY,
    categoria       VARCHAR(50)    NOT NULL,
    descripcion     TEXT
);

--------------------------------------------------------------------------------------------
-- Relaciones
--------------------------------------------------------------------------------------------

-- Tabla: Ganar
CREATE TABLE IF NOT EXISTS Ganar (
    idNominacion    INT            NOT NULL,  -- FK a Nominacion
    numCuenta       INT            NOT NULL,  -- FK a Usuario
    premio          TEXT,
    PRIMARY KEY (idNominacion, numCuenta),
    FOREIGN KEY (idNominacion)
      REFERENCES Nominacion(idNominacion)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (numCuenta)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Votar
CREATE TABLE IF NOT EXISTS Votar (
    numCuenta       INT            NOT NULL,  -- FK a Usuario (emisor)
    idNominacion    INT            NOT NULL,  -- FK a Nominacion
    alumnoVotado    INT            NOT NULL,  -- FK a Usuario (receptor)
    PRIMARY KEY (numCuenta, idNominacion, alumnoVotado),
    FOREIGN KEY (numCuenta)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (idNominacion)
      REFERENCES Nominacion(idNominacion)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (alumnoVotado)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Poseer
CREATE TABLE IF NOT EXISTS Poseer (
    idComentario    INT            NOT NULL,  -- FK a Comentario
    idPublicacion   INT            NOT NULL,  -- FK a Publicacion
    PRIMARY KEY (idComentario, idPublicacion),
    FOREIGN KEY (idComentario)
      REFERENCES Comentario(idComentario)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (idPublicacion)
      REFERENCES Publicacion(idPublicacion)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Existe
CREATE TABLE IF NOT EXISTS Existe (
    idNominacion    INT            NOT NULL,  -- FK a Nominacion
    codigo          INT            NOT NULL,  -- FK a Grupo
    fecha_inicio    TIMESTAMP      NOT NULL,
    fecha_fin       TIMESTAMP      NOT NULL,
    PRIMARY KEY (idNominacion, codigo),
    FOREIGN KEY (idNominacion)
      REFERENCES Nominacion(idNominacion)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (codigo)
      REFERENCES Grupo(codigo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Gestionar
CREATE TABLE IF NOT EXISTS Gestionar (
    numCuenta       INT            NOT NULL,  -- FK a Usuario
    codigo          INT            NOT NULL,  -- FK a Grupo
    PRIMARY KEY (numCuenta, codigo),
    FOREIGN KEY (numCuenta)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (codigo)
      REFERENCES Grupo(codigo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Pertenecer
CREATE TABLE IF NOT EXISTS Pertenecer (
    numCuenta       INT            NOT NULL,  -- FK a Usuario
    codigo          INT            NOT NULL,  -- FK a Grupo
    PRIMARY KEY (numCuenta, codigo),
    FOREIGN KEY (numCuenta)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (codigo)
      REFERENCES Grupo(codigo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Tener (1‑1 Usuario–Perfil)
CREATE TABLE IF NOT EXISTS Tener (
    numCuenta       INT            PRIMARY KEY,      -- FK a Usuario
    idPerfil        INT            NOT NULL UNIQUE,  -- FK a Perfil
    FOREIGN KEY (numCuenta)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (idPerfil)
      REFERENCES Perfil(idPerfil)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Tabla: Postular
CREATE TABLE IF NOT EXISTS Postular (
    numCuenta       INT            NOT NULL,  -- FK a Usuario
    idNominacion    INT            NOT NULL,  -- FK a Nominacion
    PRIMARY KEY (numCuenta, idNominacion),
    FOREIGN KEY (numCuenta)
      REFERENCES Usuario(numCuenta)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (idNominacion)
      REFERENCES Nominacion(idNominacion)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

--------------------------------------------------------------------------------------------
-- Multivaluados
--------------------------------------------------------------------------------------------

-- Tabla: marcoFoto
CREATE TABLE IF NOT EXISTS marcoFoto (
    idPerfil        INT            NOT NULL,  -- FK a Perfil
    marco_foto      TEXT           NOT NULL,
    PRIMARY KEY (idPerfil, marco_foto),
    FOREIGN KEY (idPerfil)
      REFERENCES Perfil(idPerfil)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-----------------------------------
-- 2. RESTRICCIONES ADICIONALES
-----------------------------------

-- Validaciones en Usuario
ALTER TABLE Usuario
  ADD CONSTRAINT ck_usuario_numCuenta_range
    CHECK (numCuenta BETWEEN 1 AND 999999999),
  ADD CONSTRAINT ck_usuario_correoE_format
    CHECK (correoE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

