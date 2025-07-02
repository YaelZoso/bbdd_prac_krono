import random
import datetime
from database import conectar

def poblar_familias():
    familias = [
        ("Informática y Comunicaciones", "Tecnologías de la información"),
        ("Administración", "Gestión empresarial"),
        ("Sanidad", "Ámbito sanitario"),
        ("Electricidad", "Instalaciones eléctricas"),
        ("Automoción", "Mecánica y motores"),
        ("Hostelería", "Servicios de restauración"),
        ("Educación", "Formación docente"),
        ("Construcción", "Obras y proyectos"),
        ("Comercio", "Ventas y distribución"),
        ("Imagen y Sonido", "Medios audiovisuales"),
    ]
    conn = conectar()
    cur = conn.cursor()
    cur.executemany("INSERT INTO fam_prof (nombre_fam, desc_fam) VALUES (%s, %s)", familias)
    conn.commit()
    cur.close()
    conn.close()

def poblar_cursos():
    cursos = [
        ("C-001", "Python Avanzado", 1, "Curso avanzado de Python", "2024-09-15", "Superior"),
        ("C-002", "Ofimática Empresarial", 2, "Word, Excel, Access, PowerPoint", "2024-09-20", "Medio"),
        ("C-003", "Auxiliar de Enfermería", 3, "Primeros auxilios y atención sanitaria", "2024-09-10", "Medio"),
        ("C-004", "Electricista Básico", 4, "Montaje de cuadros eléctricos", "2024-10-02", "Básico"),
        ("C-005", "Mecánica del Automóvil", 5, "Motores, transmisiones y frenos", "2024-10-10", "Medio"),
        ("C-006", "Cocina Internacional", 6, "Platos de diferentes culturas", "2024-10-15", "Superior"),
        ("C-007", "Educación Infantil", 7, "Desarrollo y psicología infantil", "2024-09-25", "Medio"),
        ("C-008", "Albañilería Moderna", 8, "Técnicas actuales de construcción", "2024-11-05", "Básico"),
        ("C-009", "Gestión Comercial", 9, "Ventas, atención y marketing", "2024-09-29", "Medio"),
        ("C-010", "Edición de Video", 10, "Premiere, After Effects y DaVinci", "2024-10-20", "Superior"),
    ]
    conn = conectar()
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO cursos (ref_curso, nombre_curso, fam_curso, desc_curso, fecha_curso, niv_prof)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, cursos)
    conn.commit()
    cur.close()
    conn.close()

def poblar_alumnos():
    alumnos = [
        ("López", "Ismael", "11111111A", "600111111", "ismael@example.com", "1990-05-02", "Licenciado"),
        ("Martínez", "Lucía", "22222222B", "600222222", "lucia@example.com", "1995-03-14", "Graduada"),
        ("García", "Pedro", "33333333C", "600333333", "pedro@example.com", "1988-07-10", "Bachiller"),
        ("Sánchez", "Elena", "44444444D", "600444444", "elena@example.com", "2000-11-19", "ESO"),
        ("Ruiz", "Mario", "55555555E", "600555555", "mario@example.com", "1998-01-21", "Ciclo Medio"),
        ("Gómez", "Sara", "66666666F", "600666666", "sara@example.com", "1992-04-04", "Licenciada"),
        ("Fernández", "David", "77777777G", "600777777", "david@example.com", "1987-09-09", "Doctorado"),
        ("Díaz", "Ana", "88888888H", "600888888", "ana@example.com", "2001-06-23", "ESO"),
        ("Moreno", "Pablo", "99999999I", "600999999", "pablo@example.com", "1993-12-15", "Ciclo Superior"),
        ("Muñoz", "Laura", "10101010J", "601010101", "laura@example.com", "1997-02-07", "Graduada"),
    ]
    conn = conectar()
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO alumnos (apellidos, nombre, dni, telf, mail, f_nacimiento, niv_academico)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, alumnos)
    conn.commit()
    cur.close()
    conn.close()

def poblar_cursos_finalizados():
    # Cada alumno finaliza uno o dos cursos
    conn = conectar()
    cur = conn.cursor()
    for alumno_id in range(1, 11):
        cursos_ids = random.sample(range(1, 11), 2)  # Dos cursos distintos por alumno
        for curso_id in cursos_ids:
            fecha = datetime.date(2023, random.randint(1, 12), random.randint(1, 28))
            cur.execute(
                "INSERT INTO cursos_fin (alumno_id, curso_id, fecha_fin) VALUES (%s, %s, %s)",
                (alumno_id, curso_id, fecha)
            )
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    poblar_familias()
    poblar_cursos()
    poblar_alumnos()
    poblar_cursos_finalizados()
    print("¡Datos de ejemplo insertados correctamente en familias, cursos, alumnos y cursos finalizados!")
