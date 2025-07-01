# curso_crud.py

import mysql.connector
from database import conectar

# CRUD Cursos
def agregar_curso(ref, nombre, fam_id, desc, fecha, nivel_prof):
    conn = conectar()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO cursos (ref_curso, nombre_curso, fam_curso, desc_curso, fecha_curso, niv_prof)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (ref, nombre, fam_id, desc, fecha, nivel_prof))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_cursos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT cursos.id, ref_curso, nombre_curso, fam_prof.nombre_fam, desc_curso, fecha_curso, niv_prof
        FROM cursos
        LEFT JOIN fam_prof ON cursos.fam_curso = fam_prof.id
        ORDER BY cursos.id DESC
    ''')
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return cursos

def actualizar_curso(id, ref, nombre, fam_id, desc, fecha, nivel_prof):
    conn = conectar()
    cursor = conn.cursor()
    sql = '''
        UPDATE cursos SET ref_curso=%s, nombre_curso=%s, fam_curso=%s, desc_curso=%s, fecha_curso=%s, niv_prof=%s
        WHERE id=%s
    '''
    cursor.execute(sql, (ref, nombre, fam_id, desc, fecha, nivel_prof, id))
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

# CRUD Familias Profesionales
def agregar_familia(nombre, desc):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO fam_prof (nombre_fam, desc_fam) VALUES (%s, %s)"
    cursor.execute(sql, (nombre, desc))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_familias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_fam, desc_fam FROM fam_prof ORDER BY id DESC")
    familias = cursor.fetchall()
    cursor.close()
    conn.close()
    return familias

def actualizar_familia(id, nombre, desc):
    conn = conectar()
    cursor = conn.cursor()
    sql = "UPDATE fam_prof SET nombre_fam=%s, desc_fam=%s WHERE id=%s"
    cursor.execute(sql, (nombre, desc, id))
    conn.commit()
    cursor.close()
    conn.close()

def borrar_familia(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fam_prof WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

# CRUD Inscripciones (alumno_curso)
def inscribir_alumno(alumno_id, curso_id):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO alumno_curso (alumno_id, curso_id) VALUES (%s, %s)"
    cursor.execute(sql, (alumno_id, curso_id))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_inscripciones():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT alumno_curso.id, alumnos.nombre, alumnos.apellidos, cursos.nombre_curso
        FROM alumno_curso
        JOIN alumnos ON alumno_curso.alumno_id = alumnos.id
        JOIN cursos ON alumno_curso.curso_id = cursos.id
        ORDER BY alumno_curso.id DESC
    ''')
    inscripciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return inscripciones

def borrar_inscripcion(inscripcion_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alumno_curso WHERE id=%s", (inscripcion_id,))
    conn.commit()
    cursor.close()
    conn.close()

# CRUD Cursos Finalizados (cursos_fin)
def finalizar_curso(alumno_id, curso_id, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO cursos_fin (alumno_id, curso_id, fecha_fin) VALUES (%s, %s, %s)"
    cursor.execute(sql, (alumno_id, curso_id, fecha_fin))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_cursos_finalizados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT cursos_fin.id, alumnos.nombre, alumnos.apellidos, cursos.nombre_curso, cursos_fin.fecha_fin
        FROM cursos_fin
        JOIN alumnos ON cursos_fin.alumno_id = alumnos.id
        JOIN cursos ON cursos_fin.curso_id = cursos.id
        ORDER BY cursos_fin.id DESC
    ''')
    finalizados = cursor.fetchall()
    cursor.close()
    conn.close()
    return finalizados

def borrar_curso_finalizado(finalizado_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cursos_fin WHERE id=%s", (finalizado_id,))
    conn.commit()
    cursor.close()
    conn.close()
