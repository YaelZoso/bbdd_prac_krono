# AcademyGo - Gestión Profesional de Alumnos

**Desarrollado por PRACTICADORES.DEV**

---

## 📖 Descripción

**AcademyGo** es una solución profesional, visual y moderna para la gestión integral de alumnos en academias, colegios o centros de formación. Permite la gestión completa de los datos del alumnado con una interfaz intuitiva, pantalla de bienvenida personalizada, base de datos robusta MySQL/MariaDB, exportación a PDF, e impresión directa.

---

## 🚀 Características

- **Gestión profesional de alumnos**: alta, edición, borrado y consulta.
- **Gestión de cursos**: CRUD completo con vinculación a familias profesionales.
- **Interfaz gráfica moderna** (Tkinter + PIL).
- **Pantalla de bienvenida** a pantalla completa con logo, animación y branding.
- **Base de datos MariaDB/MySQL**: robusta, multiusuario, escalable.
- **Exportación a PDF** de listados de alumnos o cursos.
- **Impresión directa** desde la aplicación.
- **Sistema modular y extensible**.
- **Pestañas de funcionalidades futuras** ya estructuradas.
- **Branding PRACTICADORES.DEV**.

---

## 🗂️ Estructura de archivos

```
academygo/
├── main.py               # Arranque del programa
├── ui.py                 # Interfaz gráfica, pestañas y lógica de usuario
├── alumno_crud.py        # Operaciones CRUD sobre alumnos
├── crud_otros.py         # Operaciones CRUD sobre cursos y futuros módulos
├── database.py           # Utilidades para creación y conexión a BD
├── backup_utils.py       # Herramientas para exportar respaldo de la BD
├── pdf_export.py         # Exportación e impresión de datos
├── academygo.png         # Logo del sistema
└── README.md             # Este archivo
```

---

## 🛠️ Requisitos

- Python 3.8 o superior
- MariaDB o MySQL (local o remoto)
- Paquetes Python necesarios:
  - `mysql-connector-python`
  - `Pillow`
  - `reportlab`

Instalación:

```bash
pip install mysql-connector-python pillow reportlab
```

---

## 🛫 Instalación y ejecución

1. Clona este repositorio o descárgalo como `.zip`.
2. Ejecuta `main.py`. Se crearán automáticamente la base de datos y tablas si no existen.
3. Asegúrate de tener el archivo `academygo.png` en la raíz para el logo.
4. Inicia el programa:

```bash
python main.py
```

---

## 🧩 Funcionalidades actuales

### ✅ Implementadas:

- Gestión completa de **alumnos**.
- Gestión completa de **cursos**.
- **Exportación e impresión** de registros.
- **Pantalla de bienvenida personalizada**.
- **Paginación** de resultados.
- Botones: guardar, actualizar, borrar, limpiar, exportar, imprimir, salir, volver.

### 📦 Estructura de base de datos:

- **alumnos**
- **cursos**
- **alumno_curso**
- **cursos_fin**
- **fam_prof**
- **adjuntos**

---

## 🧪 Próximas mejoras / ideas futuras

- Gestión de inscripciones (alumno_curso).
- Gestión de finalización de cursos (cursos_fin).
- Gestión avanzada de familias profesionales.
- Carga y visualización de archivos adjuntos.
- Sistema de usuarios y permisos.
- Panel de administración/respaldo desde UI.
- Multiplataforma con empaquetado (EXE/AppImage).
- Modo oscuro y personalización de temas.

---

## 🛡️ Seguridad y buenas prácticas

- El acceso a la base de datos requiere credenciales configuradas en `database.py`.
- Usa usuarios SQL con permisos limitados en producción.
- La función de backup (`backup_utils.py`) genera copias `.sql` localmente.

---

## 🙋‍♀️ FAQ

**¿Qué pasa si no carga el logo?**  
Asegúrate de tener `academygo.png` en el mismo directorio que `main.py`.

**¿La aplicación es multiusuario?**  
Sí, si conectas a una BD remota accesible desde varios equipos.

**¿Cómo restauro una copia de seguridad?**  
Usa el archivo `.sql` generado por `backup_utils.py` con `mysql`:

```bash
mysql -u root -p academia < backups/academia_YYYYMMDD.sql
```

---

## 🧑‍💻 Contacto

Desarrollado por: **PRACTICADORES.DEV**  
Año: 2025  
Versión: 2.0

---