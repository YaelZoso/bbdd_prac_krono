# alumno_crud.py
import sqlite3

def agregar_alumno(nombre, apellidos, dni, fecha_nacimiento, estudios, email, telefono):
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO alumnos (nombre, apellidos, dni, fecha_nacimiento, estudios, email, telefono) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nombre, apellidos, dni, fecha_nacimiento, estudios, email, telefono)
    )
    conn.commit()
    conn.close()

def obtener_alumnos():
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()
    conn.close()
    return alumnos
