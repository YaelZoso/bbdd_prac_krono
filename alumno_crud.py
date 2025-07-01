import mysql.connector
import re

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TuContraseñaSegura",  # Cambia por la tuya
        database="academia"
    )

# --- CRUD BÁSICO ---

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

# --- VALIDACIONES ---

def validar_dni(dni):
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    if not re.match(r'^\d{8}[A-Z]$', dni):
        return False
    numero = int(dni[:8])
    letra_correcta = letras[numero % 23]
    return dni[-1].upper() == letra_correcta

def validar_email(email):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None

# --- PAGINACIÓN Y FILTRO AVANZADO ---

def obtener_alumnos_paginados(offset=0, limit=20, filtro=None, ordenar=None):
    conn = conectar()
    cursor = conn.cursor()
    sql = "SELECT id, nombre, apellidos, dni, telf, mail, f_nacimiento, niv_academico FROM alumnos"
    params = []
    if filtro:
        sql += " WHERE nombre LIKE %s OR apellidos LIKE %s OR dni LIKE %s"
        filtro_param = f"%{filtro}%"
        params.extend([filtro_param, filtro_param, filtro_param])
    if ordenar:
        sql += f" ORDER BY {ordenar}"
    else:
        sql += " ORDER BY id DESC"
    sql += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    cursor.execute(sql, params)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def contar_alumnos(filtro=None):
    conn = conectar()
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM alumnos"
    params = []
    if filtro:
        sql += " WHERE nombre LIKE %s OR apellidos LIKE %s OR dni LIKE %s"
        filtro_param = f"%{filtro}%"
        params.extend([filtro_param, filtro_param, filtro_param])
    cursor.execute(sql, params)
    n = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return n
