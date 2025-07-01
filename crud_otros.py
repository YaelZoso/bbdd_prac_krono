import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TuContraseñaSegura",
        database="academia"
    )

# CRUD para Cursos
def agregar_curso(ref_curso, nombre_curso, fam_curso, desc_curso, fecha_curso, niv_prof):
    conn = conectar()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO cursos (ref_curso, nombre_curso, fam_curso, desc_curso, fecha_curso, niv_prof)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (ref_curso, nombre_curso, fam_curso, desc_curso, fecha_curso, niv_prof))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_cursos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, ref_curso, nombre_curso, fam_curso, desc_curso, fecha_curso, niv_prof FROM cursos ORDER BY id DESC")
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return cursos

def actualizar_curso(id, ref_curso, nombre_curso, fam_curso, desc_curso, fecha_curso, niv_prof):
    conn = conectar()
    cursor = conn.cursor()
    sql = '''
        UPDATE cursos SET ref_curso=%s, nombre_curso=%s, fam_curso=%s, desc_curso=%s, fecha_curso=%s, niv_prof=%s
        WHERE id=%s
    '''
    cursor.execute(sql, (ref_curso, nombre_curso, fam_curso, desc_curso, fecha_curso, niv_prof, id))
    conn.commit()
    cursor.close()
    conn.close()

def borrar_curso(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cursos WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
