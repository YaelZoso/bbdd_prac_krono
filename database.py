import mysql.connector

def crear_base_si_no_existe():
    # Conecta al servidor MariaDB sin especificar base
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="TuContraseñaSegura"  # Cambia por la tuya
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS academia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.commit()
    cursor.close()
    conn.close()

def crear_tablas():
    # Conecta a la base ya existente (o recién creada)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="TuContraseñaSegura",  # Cambia por la tuya
        database="academia"
    )
    cursor = conn.cursor()

    # 1. Tabla de Familias Profesionales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fam_prof (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre_fam VARCHAR(100),
            desc_fam TEXT
        )
    ''')

    # 2. Tabla de Cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ref_curso VARCHAR(50),
            nombre_curso VARCHAR(100),
            fam_curso INT,
            desc_curso TEXT,
            fecha_curso DATE,
            niv_prof VARCHAR(100),
            FOREIGN KEY (fam_curso) REFERENCES fam_prof(id)
        )
    ''')

    # 3. Tabla de Alumnos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            apellidos VARCHAR(100),
            nombre VARCHAR(100),
            dni VARCHAR(20) UNIQUE,
            telf VARCHAR(20),
            mail VARCHAR(100),
            f_nacimiento DATE,
            niv_academico VARCHAR(100)
        )
    ''')

    # 4. Tabla N:M de relación Alumnos-Cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumno_curso (
            id INT AUTO_INCREMENT PRIMARY KEY,
            alumno_id INT,
            curso_id INT,
            FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    ''')

    # 5. Tabla de finalización de cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos_fin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            alumno_id INT,
            curso_id INT,
            fecha_fin DATE,
            FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()
