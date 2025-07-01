# ui.py
import tkinter as tk
from tkinter import messagebox
from alumno_crud import agregar_alumno, obtener_alumnos

def crear_interfaz():
    root = tk.Tk()
    root.title("Gestión de Academia")

    tk.Label(root, text="Apellidos").grid(row=0, column=0)
    tk.Label(root, text="Nombre").grid(row=1, column=0)
    tk.Label(root, text="DNI").grid(row=2, column=0)
    tk.Label(root, text="Fecha Nacimiento").grid(row=3, column=0)
    tk.Label(root, text="Estudios").grid(row=4, column=0)
    tk.Label(root, text="Email").grid(row=5, column=0)
    tk.Label(root, text="Teléfono").grid(row=6, column=0)

    identificador = tk.Entry(root) 
    apellidos = tk.Entry(root)
    nombre = tk.Entry(root)
    dni = tk.Entry(root)
    fecha_nacimiento = tk.Entry(root)
    estudios = tk.Entry(root)
    email = tk.Entry(root)
    telefono = tk.Entry(root)

    identificador.grid(row=0, column=1)
    apellidos.grid(row=1, column=1)
    nombre.grid(row=2, column=1)
    dni.grid(row=3, column=1)
    fecha_nacimiento.grid(row=4, column=1)
    estudios.grid(row=5, column=1)
    email.grid(row=6, column=1)
    telefono.grid(row=7, column=1)

    def guardar():
        agregar_alumno(identificador.get(), apellidos.get(), nombre.get(), dni.get(), fecha_nacimiento(), estudios.get(), email.get(), telefono.get(), )
        messagebox.showinfo("Éxito", "Alumno agregado")

    tk.Button(root, text="Guardar alumno", command=guardar).grid(row=7, column=0, columnspan=2)

    root.mainloop()
