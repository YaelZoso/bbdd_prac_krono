# AcademyGo - Gestión Profesional de Alumnos

**Desarrollado por PRACTICADORES.DEV**

---

## 📖 Descripción

**AcademyGo** es una solución profesional, visual y moderna para la gestión integral de alumnos en academias, colegios o centros de formación. Permite la gestión completa de los datos del alumnado con una interfaz intuitiva, pantalla de bienvenida personalizada, base de datos robusta MySQL/MariaDB, exportación a PDF, e impresión directa.

---

## 🚀 Características

- **Gestión profesional de alumnos**: alta, edición, borrado y consulta.
- **Interfaz gráfica moderna** (Tkinter + PIL).
- **Pantalla de bienvenida** a pantalla completa con logo y branding.
- **Base de datos MariaDB/MySQL**: robusta, multiusuario, escalable.
- **Exportación a PDF** del listado de alumnos con un clic.
- **Impresión directa** del listado.
- **Código modular**: fácil de mantener y ampliar.
- **Branding PRACTICADORES.DEV**.

---

## 🗂️ Estructura de archivos

```
academygo/
├── main.py               # Arranque del programa
├── ui.py                 # Interfaz gráfica y lógica de usuario
├── alumno_crud.py        # Operaciones CRUD sobre la base de datos MySQL
├── database.py           # Utilidades de conexión/creación BD/tablas
├── pdf_export.py         # Exportación e impresión de listados en PDF
├── academygo.png         # Logo de la academia (¡colócalo aquí!)
└── README.md             # Este archivo
```

---

## 🗄️ Estructura de la Base de Datos

El sistema utiliza una base de datos **MySQL/MariaDB** llamada `academia` con la siguiente tabla principal:

```sql
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    dni VARCHAR(20),
    telf VARCHAR(20),
    mail VARCHAR(100),
    f_nacimiento VARCHAR(20),
    niv_academico VARCHAR(50)
);
```

**Descripción de los campos:**

| Campo         | Tipo           | Descripción                               |
|---------------|----------------|-------------------------------------------|
| id            | INT            | Identificador único (auto-increment)      |
| nombre        | VARCHAR(100)   | Nombre del alumno                         |
| apellidos     | VARCHAR(100)   | Apellidos del alumno                      |
| dni           | VARCHAR(20)    | DNI o identificación                      |
| telf          | VARCHAR(20)    | Teléfono de contacto                      |
| mail          | VARCHAR(100)   | Correo electrónico                        |
| f_nacimiento  | VARCHAR(20)    | Fecha de nacimiento (formato libre)       |
| niv_academico | VARCHAR(50)    | Nivel académico                           |

---

## 🖥️ Requisitos

- **Python 3.8 o superior**
- **MariaDB o MySQL** en funcionamiento (local o remoto)
- Las siguientes librerías Python:
  - `mysql-connector-python`
  - `Pillow`
  - `reportlab`

Instala las dependencias con:

```bash
pip install pillow reportlab mysql-connector-python
```

---

## 🛠️ Instalación y Primer uso

1. **Clona o descarga este repositorio.**
2. **Configura la base de datos:**
   - Crea una base de datos llamada `academia` en tu MySQL/MariaDB.
   - Ejecuta el script SQL anterior para crear la tabla `alumnos` si es necesario.
   - Ajusta usuario y contraseña en `alumno_crud.py` y `database.py` si lo necesitas.

3. **Coloca tu logo** como `academygo.png` en la raíz del proyecto.

4. **Lanza el programa:**
   ```bash
   python main.py
   ```

---

## 🧩 Uso del programa

- Al abrir, verás una **pantalla de bienvenida a pantalla completa** con el logo y dos botones:
  - **Comenzar:** accede a la gestión de alumnos.
  - **Salir:** cierra la aplicación.
- En la pantalla principal puedes **añadir, modificar, borrar y consultar** alumnos.
- Exporta la lista completa a PDF o imprímela directamente con los botones bajo la tabla.

---

## 🎨 Personalización

- **Logo:** Reemplaza `academygo.png` por tu propio logo.
- **Colores y fuentes:** Modifica en `ui.py` los parámetros de color o fuente para adaptar el diseño a tu imagen corporativa.
- **Campos:** Puedes añadir o modificar campos en la base de datos y formularios según las necesidades de tu academia.

---

## 🔒 Seguridad

- El acceso a la base de datos requiere usuario y contraseña, definidos en los archivos de conexión.
- Para despliegues multiusuario, limita los permisos del usuario MySQL/MariaDB.
- Considera cifrar las copias de seguridad.

---

## 🧑‍💻 Ejemplo de conexión a la base de datos (Python)

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TuContraseñaSegura",
    database="academia"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM alumnos")
for fila in cursor.fetchall():
    print(fila)
conn.close()
```

---

## ❓ FAQ

- **¿Qué hago si el programa no conecta a la base de datos?**  
  Revisa usuario/contraseña en los archivos fuente, verifica que MySQL/MariaDB está activo y que la base de datos `academia` existe.

- **¿Puedo poner la base de datos en otro ordenador o servidor?**  
  Sí. Cambia el parámetro `host` en los scripts de conexión y asegúrate de que el servidor MySQL acepte conexiones remotas.

- **¿Es multiusuario?**  
  Sí, al usar MariaDB/MySQL, puedes acceder a la aplicación desde varios puestos si la red lo permite.

- **¿Puedo ampliar con otros módulos (familias, cursos, pagos, etc.)?**  
  Sí. El código es modular y puede ampliarse fácilmente.

---

## 🤝 Créditos

Desarrollado por **PRACTICADORES.DEV**  
2025

---
