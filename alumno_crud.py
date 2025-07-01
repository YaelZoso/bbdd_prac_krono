import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TuContraseñaSegura",  # Cambia por la tuya
        database="academia"
    )

def agregar_alumno(nombre, apellidos, dni, telefono, mail, fecha_nacimiento, niv_academico):
    conn = conectar()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO alumnos (nombre, apellidos, dni, telf, mail, f_nacimiento, niv_academico)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (nombre, apellidos, dni, telefono, mail, fecha_nacimiento, niv_academico))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_alumnos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellidos, dni, telf, mail, f_nacimiento, niv_academico FROM alumnos ORDER BY id DESC")
    alumnos = cursor.fetchall()
    cursor.close()
    conn.close()
    return alumnos

def actualizar_alumno(id, nombre, apellidos, dni, telefono, mail, fecha_nacimiento, niv_academico):
    conn = conectar()
    cursor = conn.cursor()
    sql = '''
        UPDATE alumnos SET nombre=%s, apellidos=%s, dni=%s, telf=%s, mail=%s, f_nacimiento=%s, niv_academico=%s
        WHERE id=%s
    '''
    cursor.execute(sql, (nombre, apellidos, dni, telefono, mail, fecha_nacimiento, niv_academico, id))
    conn.commit()
    cursor.close()
    conn.close()

def borrar_alumno(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
