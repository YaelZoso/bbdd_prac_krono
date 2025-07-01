# adjuntos_utils.py
import os
import shutil
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TuContraseñaSegura",
        database="academia"
    )

def adjuntar_documento(alumno_id, ruta_origen):
    carpeta_destino = f"adjuntos/{alumno_id}/"
    os.makedirs(carpeta_destino, exist_ok=True)
    nombre_archivo = os.path.basename(ruta_origen)
    ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
    shutil.copy2(ruta_origen, ruta_destino)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO adjuntos (alumno_id, nombre_archivo, ruta_archivo) VALUES (%s, %s, %s)",
        (alumno_id, nombre_archivo, ruta_destino)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return ruta_destino

def listar_adjuntos(alumno_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_archivo, ruta_archivo, fecha_subida FROM adjuntos WHERE alumno_id = %s", (alumno_id,))
    archivos = cursor.fetchall()
    cursor.close()
    conn.close()
    return archivos

def borrar_adjunto(adjunto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT ruta_archivo FROM adjuntos WHERE id=%s", (adjunto_id,))
    row = cursor.fetchone()
    if row:
        ruta = row[0]
        if os.path.exists(ruta):
            os.remove(ruta)
    cursor.execute("DELETE FROM adjuntos WHERE id=%s", (adjunto_id,))
    conn.commit()
    cursor.close()
    conn.close()
