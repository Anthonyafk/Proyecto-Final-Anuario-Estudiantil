CREATE TABLE Usuario (
    numCuenta SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    primer_apellido VARCHAR(50),
    segundo_apellido VARCHAR(50),
    correoE VARCHAR(100),
    nombre_usuario VARCHAR(50),
    contraseña VARCHAR(100),
    esEstudiante BOOLEAN,
    esAdmin BOOLEAN
);

CREATE TABLE Grupo (
    Codigo SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripción TEXT
);

CREATE TABLE Publicación (
    idPublicación SERIAL PRIMARY KEY,
    hora_creación TIME,
    fecha_creación DATE,
    descripción TEXT,
    imagen BYTEA
);

CREATE TABLE Perfil (
    idPerfil SERIAL PRIMARY KEY,
    foto_perfil BYTEA,
    foto_portada BYTEA,
    biografía TEXT
);

CREATE TABLE marcoFoto (
    idPerfil INT,
    marco_foto VARCHAR(100),
    PRIMARY KEY (idPerfil, marco_foto),
    FOREIGN KEY (idPerfil) REFERENCES Perfil(idPerfil)
);

CREATE TABLE Nominación (
    idNominación SERIAL PRIMARY KEY,
    categoria VARCHAR(50),
    descripción TEXT
);

CREATE TABLE Comentario (
    idComentario SERIAL PRIMARY KEY,
    contenido TEXT,
    fecha_creación DATE,
    hora_creación TIME
);

