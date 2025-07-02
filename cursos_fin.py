import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TuContraseñaSegura",
        database="academia"
    )

# 🔹 Crear registro de curso finalizado
def finalizar_curso(alumno_id, curso_id, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cursos_fin (alumno_id, curso_id, fecha_fin) VALUES (%s, %s, %s)",
        (alumno_id, curso_id, fecha_fin)
    )
    conn.commit()
    cursor.close()
    conn.close()

# 🔹 Obtener todos los cursos finalizados (join con nombres)
def obtener_cursos_finalizados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT cf.id, a.nombre, a.apellidos, c.nombre_curso, cf.fecha_fin
        FROM cursos_fin cf
        JOIN alumnos a ON cf.alumno_id = a.id
        JOIN cursos c ON cf.curso_id = c.id
        ORDER BY cf.id DESC
    ''')
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return datos

# 🔹 Borrar un curso finalizado
def borrar_curso_finalizado(id_finalizado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cursos_fin WHERE id = %s", (id_finalizado,))
    conn.commit()
    cursor.close()
    conn.close()
