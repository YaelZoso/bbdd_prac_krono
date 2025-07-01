-- Crear base de datos
CREATE DATABASE IF NOT EXISTS academia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE academia;

-- Tabla de Familias Profesionales
CREATE TABLE IF NOT EXISTS fam_prof (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_fam VARCHAR(100),
    desc_fam TEXT
);

-- Tabla de Cursos
CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ref_curso VARCHAR(50),
    nombre_curso VARCHAR(100),
    fam_curso INT,
    desc_curso TEXT,
    fecha_curso DATE,
    niv_prof VARCHAR(100),
    FOREIGN KEY (fam_curso) REFERENCES fam_prof(id)
);

-- Tabla de Alumnos
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    apellidos VARCHAR(100),
    nombre VARCHAR(100),
    dni VARCHAR(20) UNIQUE,
    telf VARCHAR(20),
    mail VARCHAR(100),
    f_nacimiento DATE,
    niv_academico VARCHAR(100)
);

-- Tabla N:M de relación Alumnos-Cursos
CREATE TABLE IF NOT EXISTS alumno_curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT,
    curso_id INT,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id)
);

-- Tabla de finalización de cursos
CREATE TABLE IF NOT EXISTS cursos_fin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT,
    curso_id INT,
    fecha_fin DATE,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id)
);
