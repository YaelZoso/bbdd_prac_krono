# backup_utils.py
import subprocess
import datetime
import os

def backup_base_datos(nombre_bd="academia", usuario="root", contraseña="TuContraseñaSegura", ruta_destino="backups"):
    os.makedirs(ruta_destino, exist_ok=True)
    fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_backup = os.path.join(ruta_destino, f"{nombre_bd}_{fecha}.sql")
    comando = f"mysqldump -u {usuario} -p{contraseña} {nombre_bd} > {archivo_backup}"
    resultado = subprocess.run(comando, shell=True)
    return archivo_backup if resultado.returncode == 0 else None
