import tkinter as tk
from tkinter import ttk, messagebox
from curso_crud import obtener_cursos_finalizados
from alumno_crud import obtener_alumnos
from pdf_export import exportar_a_pdf

def abrir_reportes(parent=None):
    ventana = tk.Toplevel(parent)
    ventana.title("Reportes y Listados")
    ventana.geometry("950x500")
    ventana.configure(bg="#eaf3fc")

    tabs = ttk.Notebook(ventana)
    tabs.pack(fill="both", expand=True, padx=10, pady=10)

    # TAB 1: Listado de Alumnos
    tab_alumnos = tk.Frame(tabs, bg="#f7fbff")
    tabs.add(tab_alumnos, text="Alumnos")

    cols = ("ID", "Nombre", "Apellidos", "DNI", "Teléfono", "Mail", "Fecha nacimiento", "Nivel académico")
    tree = ttk.Treeview(tab_alumnos, columns=cols, show="headings", height=16)
    for i, c in enumerate(cols):
        tree.heading(c, text=c)
        tree.column(c, width=120 if i != 0 else 65, anchor="center")
    tree.pack(fill="both", padx=10, pady=8, expand=True)

    def cargar_alumnos():
        for i in tree.get_children():
            tree.delete(i)
        for a in obtener_alumnos():
            tree.insert("", "end", values=a)
    cargar_alumnos()

    btns1 = ttk.Frame(tab_alumnos); btns1.pack(pady=4)
    ttk.Button(btns1, text="Exportar a PDF", command=lambda: exportar_a_pdf(
        [tree.item(f, "values") for f in tree.get_children()],
        cols
    )).pack(side="left", padx=8, ipadx=4, ipady=2)
    ttk.Button(btns1, text="Cerrar", command=ventana.destroy).pack(side="left", padx=8, ipadx=4, ipady=2)

    # TAB 2: Cursos Finalizados
    tab_cfin = tk.Frame(tabs, bg="#eaf3fc")
    tabs.add(tab_cfin, text="Cursos Finalizados")
    cols2 = ("ID", "Alumno", "Apellidos", "Curso", "Fecha Fin")
    tree2 = ttk.Treeview(tab_cfin, columns=cols2, show="headings", height=16)
    for c in cols2:
        tree2.heading(c, text=c)
        tree2.column(c, width=130, anchor="center")
    tree2.pack(fill="both", padx=10, pady=8, expand=True)

    def cargar_finalizados():
        for i in tree2.get_children():
            tree2.delete(i)
        for d in obtener_cursos_finalizados():
            tree2.insert("", "end", values=d)
    cargar_finalizados()

    btns2 = ttk.Frame(tab_cfin); btns2.pack(pady=4)
    ttk.Button(btns2, text="Exportar a PDF", command=lambda: exportar_a_pdf(
        [tree2.item(f, "values") for f in tree2.get_children()],
        cols2
    )).pack(side="left", padx=8, ipadx=4, ipady=2)
    ttk.Button(btns2, text="Cerrar", command=ventana.destroy).pack(side="left", padx=8, ipadx=4, ipady=2)

    # Puedes añadir más tabs (familias, cursos, etc.) aquí...

