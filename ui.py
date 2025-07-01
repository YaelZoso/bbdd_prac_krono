# ui.py
import tkinter as tk
from tkinter import messagebox
from alumno_crud import agregar_alumno, obtener_alumnos

def crear_interfaz():
    root = tk.Tk()
    root.title("Gestión de Academia")

    tk.Label(root, text="Nombre").grid(row=0, column=0)
    tk.Label(root, text="Email").grid(row=1, column=0)
    tk.Label(root, text="Teléfono").grid(row=2, column=0)

    nombre = tk.Entry(root)
    email = tk.Entry(root)
    telefono = tk.Entry(root)

    nombre.grid(row=0, column=1)
    email.grid(row=1, column=1)
    telefono.grid(row=2, column=1)

    def guardar():
        agregar_alumno(nombre.get(), email.get(), telefono.get())
        messagebox.showinfo("Éxito", "Alumno agregado")

    tk.Button(root, text="Guardar alumno", command=guardar).grid(row=3, column=0, columnspan=2)

    root.mainloop()
