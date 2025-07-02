import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from alumno_crud import agregar_alumno, obtener_alumnos, actualizar_alumno, borrar_alumno
from curso_crud import agregar_curso, obtener_cursos, actualizar_curso, borrar_curso, \
    agregar_familia, obtener_familias, actualizar_familia, borrar_familia, \
    obtener_cursos_finalizados, borrar_curso_finalizado
from pdf_export import exportar_a_pdf, imprimir_pdf
from backup_utils import backup_base_datos
import platform
import math

TAB_COLORS = [
    "#d4e2fc",   # Alumnos
    "#c1d6f8",   # Cursos
    "#d9d6f2",   # Inscripciones
    "#e2d9f4",   # Cursos Finalizados
    "#dce4f7",   # Familias Profesionales
    "#d0f0ed",   # Adjuntos
]
PAGINA_TAMANO = 20

def limpiar_formulario(campos):
    for campo in campos.values():
        campo.delete(0, tk.END)

def cargar_datos_alumnos(tree, pagina=0):
    for fila in tree.get_children():
        tree.delete(fila)
    alumnos = obtener_alumnos()
    inicio = pagina * PAGINA_TAMANO
    fin = inicio + PAGINA_TAMANO
    alumnos_pagina = alumnos[inicio:fin]
    for i, alumno in enumerate(alumnos_pagina):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', tk.END, values=alumno, tags=(tag,))
    tree.tag_configure('evenrow', background='#eaf3fc')
    tree.tag_configure('oddrow', background='#f7fbff')
    return len(alumnos)

def cargar_datos_cursos(tree, pagina=0):
    for fila in tree.get_children():
        tree.delete(fila)
    cursos = obtener_cursos()
    inicio = pagina * PAGINA_TAMANO
    fin = inicio + PAGINA_TAMANO
    cursos_pagina = cursos[inicio:fin]
    for i, curso in enumerate(cursos_pagina):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', tk.END, values=curso, tags=(tag,))
    tree.tag_configure('evenrow', background='#eaf3fc')
    tree.tag_configure('oddrow', background='#f7fbff')
    return len(cursos)

def cargar_datos_finalizados(tree, pagina=0):
    for fila in tree.get_children():
        tree.delete(fila)
    datos = obtener_cursos_finalizados()
    inicio = pagina * PAGINA_TAMANO
    fin = inicio + PAGINA_TAMANO
    datos_pagina = datos[inicio:fin]
    for i, d in enumerate(datos_pagina):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', tk.END, values=d, tags=(tag,))
    tree.tag_configure('evenrow', background='#eaf3fc')
    tree.tag_configure('oddrow', background='#f7fbff')
    return len(datos)

def cargar_datos_familias(tree, pagina=0):
    for fila in tree.get_children():
        tree.delete(fila)
    familias = obtener_familias()
    inicio = pagina * PAGINA_TAMANO
    fin = inicio + PAGINA_TAMANO
    familias_pagina = familias[inicio:fin]
    for i, fam in enumerate(familias_pagina):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', tk.END, values=fam, tags=(tag,))
    tree.tag_configure('evenrow', background='#eaf3fc')
    tree.tag_configure('oddrow', background='#f7fbff')
    return len(familias)

# -------- INTERFAZ PRINCIPAL --------
def crear_interfaz():
    root = tk.Tk()
    root.title("AcademyGo - Gestión Integral")
    sistema = platform.system()
    if sistema == 'Windows':
        root.state('zoomed')
    else:
        root.attributes('-zoomed', True)
    root.configure(bg="#e9f0fb")

    # Header
    header = tk.Frame(root, bg="#375aab", height=76)
    header.pack(fill='x', side='top')
    logo_img = Image.open("academygo.png").resize((52, 52), Image.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header, image=logo_tk, bg="#375aab")
    logo_label.image = logo_tk
    logo_label.pack(side="left", padx=22, pady=9)
    tk.Label(header, text="AcademyGo", bg="#375aab", fg="white", font=("Segoe UI", 25, "bold")).pack(side="left", padx=16)
    tk.Label(header, text="Gestión profesional", bg="#375aab", fg="#c7e0fa", font=("Segoe UI", 17, "italic")).pack(side="left", padx=8, pady=24)

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=9, pady=9)
    tab_alumnos = tk.Frame(notebook, bg=TAB_COLORS[0]); notebook.add(tab_alumnos, text="Alumnos")
    tab_cursos = tk.Frame(notebook, bg=TAB_COLORS[1]); notebook.add(tab_cursos, text="Cursos")
    tab_cfin = tk.Frame(notebook, bg=TAB_COLORS[3]); notebook.add(tab_cfin, text="Cursos Finalizados")
    tab_familias = tk.Frame(notebook, bg=TAB_COLORS[4]); notebook.add(tab_familias, text="Familias Profesionales")
    tab_adj = tk.Frame(notebook, bg=TAB_COLORS[5]); notebook.add(tab_adj, text="Adjuntos")

    contenido_alumnos(tab_alumnos, root)
    contenido_cursos(tab_cursos, root)
    contenido_finalizados(tab_cfin, root)
    contenido_familias(tab_familias, root)
    pestaña_maqueta(tab_adj, "Adjuntos/Documentos\n(Próximamente)", TAB_COLORS[5])

    tk.Label(root, text="Desarrollado por PRACTICADORES.DEV  |  AcademyGo",
             font=("Segoe UI", 11, "italic"), bg="#e9f0fb", fg="#666").pack(side='bottom', pady=3)
    root.mainloop()

# -------- CRUD ALUMNOS --------
def contenido_alumnos(tab, root):
    frame = ttk.Frame(tab, padding=22)
    frame.pack(fill='both', expand=True, padx=26, pady=18)
    labels = ['Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Mail', 'Fecha nacimiento (YYYY-MM-DD)', 'Nivel académico']
    keys = ['nombre', 'apellidos', 'dni', 'telefono', 'mail', 'f_nacimiento', 'niv_academico']
    campos = {}
    form = ttk.LabelFrame(frame, text="Datos del Alumno", padding=(20,12))
    form.grid(row=0, column=0, sticky='nw', rowspan=3, pady=12)

    for i, (label, key) in enumerate(zip(labels, keys)):
        ttk.Label(form, text=label + ":", anchor='w').grid(row=i, column=0, pady=7, sticky='e')
        entry = ttk.Entry(form, width=25, font=('Segoe UI', 12))
        entry.grid(row=i, column=1, pady=7, padx=7, sticky='w')
        campos[key] = entry

    btns = ttk.Frame(form)
    btns.grid(row=7, column=0, columnspan=2, pady=(18, 10))
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'), foreground="white", background="#416bce")
    style.map('Accent.TButton', background=[('active', '#2b488a')])
    style.configure('Treeview', background="#f7fbff", foreground="#222", rowheight=38, fieldbackground="#f7fbff", font=('Segoe UI', 12))
    style.configure('Treeview.Heading', background="#375aab", foreground="white", font=('Segoe UI', 13, 'bold'), relief='flat')
    style.map('Treeview', background=[('selected', '#c6e0fc')])

    pagina_actual = [0]
    def guardar():
        valores = [campos[k].get() for k in keys]
        if not valores[0]:
            messagebox.showwarning("Atención", "El nombre es obligatorio.")
            return
        try:
            agregar_alumno(*valores)
            pagina_actual[0] = 0
            cargar_y_actualizar()
            limpiar_formulario(campos)
            messagebox.showinfo("Éxito", "Alumno agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def actualizar():
        if not hasattr(root, 'selected_id') or not root.selected_id:
            messagebox.showwarning("Selecciona", "Selecciona un alumno de la tabla.")
            return
        valores = [campos[k].get() for k in keys]
        try:
            actualizar_alumno(root.selected_id, *valores)
            cargar_y_actualizar()
            limpiar_formulario(campos)
            root.selected_id = None
            messagebox.showinfo("Éxito", "Alumno actualizado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def borrar():
        if not hasattr(root, 'selected_id') or not root.selected_id:
            messagebox.showwarning("Selecciona", "Selecciona un alumno de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar este alumno?"):
            try:
                borrar_alumno(root.selected_id)
                pagina_actual[0] = 0
                cargar_y_actualizar()
                limpiar_formulario(campos)
                root.selected_id = None
                messagebox.showinfo("Éxito", "Alumno borrado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo borrar: {e}")

    def limpiar():
        limpiar_formulario(campos)
        root.selected_id = None

    def hacer_backup():
        archivo = backup_base_datos()
        if archivo:
            messagebox.showinfo("Backup realizado", f"Backup creado en:\n{archivo}")
        else:
            messagebox.showerror("Error", "No se pudo realizar el backup.")

    ttk.Button(btns, text="💾 Guardar", command=guardar, style='Accent.TButton').pack(side='left', padx=7)
    ttk.Button(btns, text="✏️ Actualizar", command=actualizar).pack(side='left', padx=7)
    ttk.Button(btns, text="🗑️ Borrar", command=borrar).pack(side='left', padx=7)
    ttk.Button(btns, text="🧹 Limpiar", command=limpiar).pack(side='left', padx=7)
    ttk.Button(btns, text="💽 Backup BD", command=hacer_backup).pack(side='left', padx=7)

    cols = ('ID', 'Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Mail', 'Fecha nacimiento', 'Nivel académico')
    tree = ttk.Treeview(frame, columns=cols, show='headings', height=14)
    for i, col in enumerate(cols):
        tree.heading(col, text=col)
        ancho = 65 if i == 0 else 120 if i == 6 else 110
        tree.column(col, width=ancho, anchor='center')
    tree.grid(row=0, column=1, padx=(30, 5), pady=10, sticky='n')

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=2, sticky='ns', pady=10)
    tree.configure(yscrollcommand=scrollbar.set)

    def cargar_y_actualizar():
        total = cargar_datos_alumnos(tree, pagina_actual[0])
        btn_anterior.config(state=tk.NORMAL if pagina_actual[0] > 0 else tk.DISABLED)
        max_pagina = max(0, (total - 1) // PAGINA_TAMANO)
        btn_siguiente.config(state=tk.NORMAL if pagina_actual[0] < max_pagina else tk.DISABLED)
        lbl_pagina.config(text=f"Página {pagina_actual[0] + 1} de {max_pagina + 1}")

    paginacion_frame = ttk.Frame(frame)
    paginacion_frame.grid(row=2, column=1, pady=8, sticky='w')
    btn_anterior = ttk.Button(paginacion_frame, text="◀ Anterior", command=lambda: cambiar_pagina(-1))
    btn_anterior.pack(side='left', padx=5)
    btn_siguiente = ttk.Button(paginacion_frame, text="Siguiente ▶", command=lambda: cambiar_pagina(1))
    btn_siguiente.pack(side='left', padx=5)
    lbl_pagina = ttk.Label(paginacion_frame, text="Página 1")
    lbl_pagina.pack(side='left', padx=10)
    def cambiar_pagina(direccion):
        pagina_actual[0] += direccion
        cargar_y_actualizar()
    cargar_y_actualizar()

    def seleccionar_fila(event):
        item = tree.focus()
        if item:
            datos = tree.item(item, 'values')
            for key, entry, value in zip(keys, campos.values(), datos[1:]):
                entry.delete(0, tk.END)
                entry.insert(0, value)
            root.selected_id = datos[0]
        else:
            root.selected_id = None

    tree.bind('<<TreeviewSelect>>', seleccionar_fila)

    extra_btns = ttk.Frame(frame)
    extra_btns.grid(row=1, column=1, pady=(14, 0), sticky='w')
    def exportar():
        datos = [tree.item(f, 'values') for f in tree.get_children()]
        cols = ('ID', 'Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Mail', 'Fecha nacimiento', 'Nivel académico')
        exportar_a_pdf(datos, cols)
    def imprimir():
        imprimir_pdf()
    def volver_a_bienvenida():
        root.destroy()
        from ui import pantalla_bienvenida
        pantalla_bienvenida()
    def salir_app():
        root.destroy()
    ttk.Button(extra_btns, text="📄 Exportar a PDF", command=exportar, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🖨️ Imprimir", command=imprimir).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🏠 Volver a inicio", command=volver_a_bienvenida, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="❌ Salir", command=salir_app, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)

# -------- CRUD CURSOS --------
def contenido_cursos(tab, root):
    frame = ttk.Frame(tab, padding=22)
    frame.pack(fill='both', expand=True, padx=26, pady=18)
    labels = ['Referencia', 'Nombre curso', 'Familia ID', 'Descripción', 'Fecha curso (YYYY-MM-DD)', 'Nivel profesional']
    keys = ['ref_curso', 'nombre_curso', 'fam_curso', 'desc_curso', 'fecha_curso', 'niv_prof']
    campos = {}
    form = ttk.LabelFrame(frame, text="Datos del Curso", padding=(20, 12))
    form.grid(row=0, column=0, sticky='nw', rowspan=3, pady=12)
    for i, (label, key) in enumerate(zip(labels, keys)):
        ttk.Label(form, text=label + ":", anchor='w').grid(row=i, column=0, pady=7, sticky='e')
        entry = ttk.Entry(form, width=30, font=('Segoe UI', 12))
        entry.grid(row=i, column=1, pady=7, padx=7, sticky='w')
        campos[key] = entry

    btns = ttk.Frame(form)
    btns.grid(row=7, column=0, columnspan=2, pady=(18, 10))
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'), foreground="white", background="#416bce")
    style.map('Accent.TButton', background=[('active', '#2b488a')])
    pagina_actual = [0]
    def limpiar_formulario_c():
        for campo in campos.values():
            campo.delete(0, tk.END)
    def cargar_y_actualizar():
        total = cargar_datos_cursos(tree, pagina_actual[0])
        btn_anterior.config(state=tk.NORMAL if pagina_actual[0] > 0 else tk.DISABLED)
        max_pagina = max(0, (total - 1) // PAGINA_TAMANO)
        btn_siguiente.config(state=tk.NORMAL if pagina_actual[0] < max_pagina else tk.DISABLED)
        lbl_pagina.config(text=f"Página {pagina_actual[0] + 1} de {max_pagina + 1}")

    def guardar():
        valores = [campos[k].get() for k in keys]
        if not valores[0]:
            messagebox.showwarning("Atención", "La referencia es obligatoria.")
            return
        try:
            agregar_curso(*valores)
            pagina_actual[0] = 0
            cargar_y_actualizar()
            limpiar_formulario_c()
            messagebox.showinfo("Éxito", "Curso agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def actualizar():
        if not hasattr(tab, 'selected_id') or not tab.selected_id:
            messagebox.showwarning("Selecciona", "Selecciona un curso de la tabla.")
            return
        valores = [campos[k].get() for k in keys]
        try:
            actualizar_curso(tab.selected_id, *valores)
            cargar_y_actualizar()
            limpiar_formulario_c()
            tab.selected_id = None
            messagebox.showinfo("Éxito", "Curso actualizado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def borrar():
        if not hasattr(tab, 'selected_id') or not tab.selected_id:
            messagebox.showwarning("Selecciona", "Selecciona un curso de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar este curso?"):
            try:
                borrar_curso(tab.selected_id)
                cargar_y_actualizar()
                limpiar_formulario_c()
                tab.selected_id = None
                messagebox.showinfo("Éxito", "Curso borrado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo borrar: {e}")

    def hacer_backup():
        archivo = backup_base_datos()
        if archivo:
            messagebox.showinfo("Backup realizado", f"Backup creado en:\n{archivo}")
        else:
            messagebox.showerror("Error", "No se pudo realizar el backup.")

    ttk.Button(btns, text="💾 Guardar", command=guardar, style='Accent.TButton').pack(side='left', padx=7)
    ttk.Button(btns, text="✏️ Actualizar", command=actualizar).pack(side='left', padx=7)
    ttk.Button(btns, text="🗑️ Borrar", command=borrar).pack(side='left', padx=7)
    ttk.Button(btns, text="🧹 Limpiar", command=limpiar_formulario_c).pack(side='left', padx=7)
    ttk.Button(btns, text="💽 Backup BD", command=hacer_backup).pack(side='left', padx=7)

    cols = ('ID', 'Referencia', 'Nombre curso', 'Familia ID', 'Descripción', 'Fecha curso', 'Nivel profesional')
    tree = ttk.Treeview(frame, columns=cols, show='headings', height=14)
    for i, col in enumerate(cols):
        tree.heading(col, text=col)
        ancho = 65 if i == 0 else 130 if i in (2, 4) else 110
        tree.column(col, width=ancho, anchor='center')
    tree.grid(row=0, column=1, padx=(30, 5), pady=10, sticky='n')

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=2, sticky='ns', pady=10)
    tree.configure(yscrollcommand=scrollbar.set)

    paginacion_frame = ttk.Frame(frame)
    paginacion_frame.grid(row=2, column=1, pady=8, sticky='w')
    btn_anterior = ttk.Button(paginacion_frame, text="◀ Anterior", command=lambda: cambiar_pagina(-1))
    btn_anterior.pack(side='left', padx=5)
    btn_siguiente = ttk.Button(paginacion_frame, text="Siguiente ▶", command=lambda: cambiar_pagina(1))
    btn_siguiente.pack(side='left', padx=5)
    lbl_pagina = ttk.Label(paginacion_frame, text="Página 1")
    lbl_pagina.pack(side='left', padx=10)
    def cambiar_pagina(direccion):
        pagina_actual[0] += direccion
        cargar_y_actualizar()
    cargar_y_actualizar()

    def seleccionar_fila(event):
        item = tree.focus()
        if item:
            datos = tree.item(item, 'values')
            for key, entry, value in zip(keys, campos.values(), datos[1:]):
                entry.delete(0, tk.END)
                entry.insert(0, value)
            tab.selected_id = datos[0]
        else:
            tab.selected_id = None

    tree.bind('<<TreeviewSelect>>', seleccionar_fila)

    extra_btns = ttk.Frame(frame)
    extra_btns.grid(row=1, column=1, pady=(14, 0), sticky='w')
    def exportar():
        datos = [tree.item(f, 'values') for f in tree.get_children()]
        cols = ('ID', 'Referencia', 'Nombre curso', 'Familia ID', 'Descripción', 'Fecha curso', 'Nivel profesional')
        exportar_a_pdf(datos, cols)
    def imprimir():
        imprimir_pdf()
    def volver_a_bienvenida():
        root.destroy()
        from ui import pantalla_bienvenida
        pantalla_bienvenida()
    def salir_app():
        root.destroy()
    ttk.Button(extra_btns, text="📄 Exportar a PDF", command=exportar, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🖨️ Imprimir", command=imprimir).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🏠 Volver a inicio", command=volver_a_bienvenida, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="❌ Salir", command=salir_app, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)

# -------- CRUD FINALIZADOS --------
def contenido_finalizados(tab, root):
    frame = ttk.Frame(tab, padding=22)
    frame.pack(fill='both', expand=True, padx=26, pady=18)
    cols = ('ID', 'Nombre', 'Apellidos', 'Curso', 'Fecha Fin')
    tree = ttk.Treeview(frame, columns=cols, show='headings', height=14)
    for i, col in enumerate(cols):
        tree.heading(col, text=col)
        tree.column(col, width=120 if i in (1, 2) else 95, anchor='center')
    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=scrollbar.set)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    pagina_actual = [0]

    def cargar_y_actualizar():
        total = cargar_datos_finalizados(tree, pagina_actual[0])
        btn_ant.config(state=tk.NORMAL if pagina_actual[0] > 0 else tk.DISABLED)
        max_pagina = max(0, (total - 1) // PAGINA_TAMANO)
        btn_sig.config(state=tk.NORMAL if pagina_actual[0] < max_pagina else tk.DISABLED)
        lbl_pag.config(text=f"Página {pagina_actual[0]+1} de {max_pagina+1}")

    def cambiar_pagina(direccion):
        pagina_actual[0] += direccion
        cargar_y_actualizar()

    def borrar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un curso finalizado.")
            return
        idfin = tree.item(sel, 'values')[0]
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar este registro?"):
            try:
                borrar_curso_finalizado(idfin)
                cargar_y_actualizar()
                messagebox.showinfo("Éxito", "Registro eliminado.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # --- Botones CRUD y paginación ---
    btns = ttk.Frame(frame)
    btns.grid(row=1, column=0, pady=8, sticky='w')
    ttk.Button(btns, text="🗑️ Borrar", command=borrar).pack(side='left', padx=8)
    btn_ant = ttk.Button(btns, text="◀ Anterior", command=lambda: cambiar_pagina(-1))
    btn_ant.pack(side='left', padx=4)
    btn_sig = ttk.Button(btns, text="Siguiente ▶", command=lambda: cambiar_pagina(1))
    btn_sig.pack(side='left', padx=4)
    lbl_pag = ttk.Label(btns, text="Página 1")
    lbl_pag.pack(side='left', padx=12)

    cargar_y_actualizar()

    # --- Botones Exportar PDF, Imprimir, Volver e Salir ---
    extra_btns = ttk.Frame(frame)
    extra_btns.grid(row=2, column=0, pady=(14, 0), sticky='w')

    def exportar_pdf():
        datos = [tree.item(f, 'values') for f in tree.get_children()]
        cols = ('ID', 'Nombre', 'Apellidos', 'Curso', 'Fecha Fin')
        exportar_a_pdf(datos, cols)

    def imprimir():
        imprimir_pdf()

    def volver_a_bienvenida():
        root.destroy()
        from ui import pantalla_bienvenida
        pantalla_bienvenida()

    def salir_app():
        root.destroy()

    ttk.Button(extra_btns, text="📄 Exportar a PDF", command=exportar_pdf).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🖨️ Imprimir", command=imprimir).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🏠 Volver a inicio", command=volver_a_bienvenida).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="❌ Salir", command=salir_app).pack(side='left', padx=6, ipadx=4, ipady=3)


# -------- CRUD FAMILIAS --------
def contenido_familias(tab, root):
    frame = ttk.Frame(tab, padding=22)
    frame.pack(fill='both', expand=True, padx=26, pady=18)
    campos = {'nombre': None, 'desc': None}
    form = ttk.LabelFrame(frame, text="Familia Profesional", padding=(20, 12))
    form.grid(row=0, column=0, sticky='nw', pady=12)
    ttk.Label(form, text="Nombre:", anchor='w').grid(row=0, column=0, pady=7, sticky='e')
    campos['nombre'] = ttk.Entry(form, width=30, font=('Segoe UI', 12))
    campos['nombre'].grid(row=0, column=1, pady=7, padx=7)
    ttk.Label(form, text="Descripción:", anchor='w').grid(row=1, column=0, pady=7, sticky='e')
    campos['desc'] = ttk.Entry(form, width=30, font=('Segoe UI', 12))
    campos['desc'].grid(row=1, column=1, pady=7, padx=7)

    # --- Botones CRUD ---
    btns = ttk.Frame(form); btns.grid(row=2, column=0, columnspan=2, pady=(16, 8))
    ttk.Button(btns, text="💾 Guardar", command=lambda: guardar()).pack(side='left', padx=6)
    ttk.Button(btns, text="✏️ Actualizar", command=lambda: actualizar()).pack(side='left', padx=6)
    ttk.Button(btns, text="🗑️ Borrar", command=lambda: borrar()).pack(side='left', padx=6)
    ttk.Button(btns, text="🧹 Limpiar", command=lambda: limpiar()).pack(side='left', padx=6)

    # --- Tabla familias ---
    cols = ('ID', 'Nombre', 'Descripción')
    tree = ttk.Treeview(frame, columns=cols, show='headings', height=14)
    for i, col in enumerate(cols):
        tree.heading(col, text=col)
        tree.column(col, width=120 if i == 1 else 90, anchor='center')
    tree.grid(row=0, column=1, padx=(30, 5), pady=10, sticky='n')
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=2, sticky='ns')
    tree.configure(yscrollcommand=scrollbar.set)

    pagina_actual = [0]
    selected_id = [None]

    def cargar_y_actualizar():
        total = cargar_datos_familias(tree, pagina_actual[0])
        btn_ant.config(state=tk.NORMAL if pagina_actual[0] > 0 else tk.DISABLED)
        max_pagina = max(0, (total - 1) // PAGINA_TAMANO)
        btn_sig.config(state=tk.NORMAL if pagina_actual[0] < max_pagina else tk.DISABLED)
        lbl_pag.config(text=f"Página {pagina_actual[0]+1} de {max_pagina+1}")

    def cambiar_pagina(direccion):
        pagina_actual[0] += direccion
        cargar_y_actualizar()

    def guardar():
        nombre = campos['nombre'].get()
        desc = campos['desc'].get()
        if not nombre:
            messagebox.showwarning("Campo requerido", "El nombre es obligatorio.")
            return
        try:
            agregar_familia(nombre, desc)
            cargar_y_actualizar()
            limpiar()
            messagebox.showinfo("Éxito", "Familia guardada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar():
        if not selected_id[0]:
            messagebox.showwarning("Selecciona", "Selecciona una familia de la tabla.")
            return
        nombre = campos['nombre'].get()
        desc = campos['desc'].get()
        try:
            actualizar_familia(selected_id[0], nombre, desc)
            cargar_y_actualizar()
            limpiar()
            selected_id[0] = None
            messagebox.showinfo("Éxito", "Familia actualizada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def borrar():
        if not selected_id[0]:
            messagebox.showwarning("Selecciona", "Selecciona una familia de la tabla.")
            return
        if messagebox.askyesno("¿Seguro?", "¿Seguro que quieres borrar esta familia?"):
            try:
                borrar_familia(selected_id[0])
                cargar_y_actualizar()
                limpiar()
                selected_id[0] = None
                messagebox.showinfo("Éxito", "Familia borrada.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def limpiar():
        for v in campos.values():
            v.delete(0, tk.END)
        selected_id[0] = None

    def seleccionar_fila(event):
        item = tree.focus()
        if item:
            datos = tree.item(item, 'values')
            campos['nombre'].delete(0, tk.END)
            campos['desc'].delete(0, tk.END)
            campos['nombre'].insert(0, datos[1])
            campos['desc'].insert(0, datos[2])
            selected_id[0] = datos[0]
        else:
            selected_id[0] = None

    tree.bind('<<TreeviewSelect>>', seleccionar_fila)

    # --- Paginación ---
    paginacion = ttk.Frame(frame)
    paginacion.grid(row=1, column=1, pady=8, sticky='w')
    btn_ant = ttk.Button(paginacion, text="◀ Anterior", command=lambda: cambiar_pagina(-1))
    btn_ant.pack(side='left', padx=4)
    btn_sig = ttk.Button(paginacion, text="Siguiente ▶", command=lambda: cambiar_pagina(1))
    btn_sig.pack(side='left', padx=4)
    lbl_pag = ttk.Label(paginacion, text="Página 1"); lbl_pag.pack(side='left', padx=12)
    cargar_y_actualizar()

    # --- Botones Exportar PDF, Imprimir, Volver e Salir ---
    extra_btns = ttk.Frame(frame)
    extra_btns.grid(row=2, column=1, pady=(14, 0), sticky='w')

    def exportar_pdf():
        datos = [tree.item(f, 'values') for f in tree.get_children()]
        cols = ('ID', 'Nombre', 'Descripción')
        exportar_a_pdf(datos, cols)

    def imprimir():
        imprimir_pdf()

    def volver_a_bienvenida():
        root.destroy()
        from ui import pantalla_bienvenida
        pantalla_bienvenida()

    def salir_app():
        root.destroy()

    ttk.Button(extra_btns, text="📄 Exportar a PDF", command=exportar_pdf).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🖨️ Imprimir", command=imprimir).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🏠 Volver a inicio", command=volver_a_bienvenida).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="❌ Salir", command=salir_app).pack(side='left', padx=6, ipadx=4, ipady=3)


def pestaña_maqueta(tab, texto="Funcionalidad en desarrollo...", color="#fafafa"):
    f = tk.Frame(tab, bg=color)
    f.pack(expand=True, fill="both")
    tk.Label(f, text=texto, font=("Segoe UI", 24, "italic"), bg=color, fg="#375aab").pack(expand=True)

def pantalla_bienvenida():
    welcome = tk.Tk()
    welcome.title("Bienvenido a AcademyGo")
    welcome.attributes('-fullscreen', True)
    welcome.configure(bg="#375aab")
    screen_width = welcome.winfo_screenwidth()
    screen_height = welcome.winfo_screenheight()
    logo_size = min(int(screen_height * 0.18), 220)
    canvas_h = int(screen_height * 0.22)
    canvas = tk.Canvas(welcome, width=screen_width, height=canvas_h, bg="#375aab", highlightthickness=0)
    canvas.pack()
    welcome.update_idletasks()
    center_x = canvas.winfo_width() // 2
    center_y = canvas.winfo_height() // 2
    size = min(canvas_h // 2, 85)
    angle = 0
    def draw_pyramid(a):
        canvas.delete("pyramid")
        base_coords = [(-size, size), (size, size), (0, -size)]
        apex = (0, -size * 1.5)
        def rotate(x, y, angle_deg):
            rad = math.radians(angle_deg)
            xr = x * math.cos(rad) - y * math.sin(rad)
            yr = x * math.sin(rad) + y * math.cos(rad)
            return xr, yr
        rotated_base = [rotate(x, y, a) for x, y in base_coords]
        rotated_apex = rotate(*apex, a)
        points_base = [(center_x + x, center_y + y) for x, y in rotated_base]
        apex_abs = (center_x + rotated_apex[0], center_y + rotated_apex[1])
        for i in range(3):
            p1 = points_base[i]
            p2 = points_base[(i + 1) % 3]
            canvas.create_polygon(p1, p2, apex_abs, fill="#4f8a8b", outline="#ffffff", tags="pyramid")
        canvas.create_polygon(*points_base, fill="#36608a", outline="#ffffff", tags="pyramid")
    def animate():
        nonlocal angle
        draw_pyramid(angle)
        angle += 2
        canvas.after(40, animate)
    animate()
    logo_img = Image.open("academygo.png")
    logo_img = logo_img.resize((logo_size, logo_size), Image.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(welcome, image=logo_tk, bg="#375aab")
    logo_label.image = logo_tk
    logo_label.pack(pady=8)
    tk.Label(welcome, text="AcademyGo", bg="#375aab", fg="white", font=("Segoe UI", 42, "bold")).pack(pady=4)
    tk.Label(welcome, text="PRACTICADORES.DEV", bg="#375aab", fg="#c7e0fa", font=("Segoe UI", 20, "italic")).pack(pady=2)
    botones = tk.Frame(welcome, bg="#375aab"); botones.pack(pady=30)
    def comenzar():
        welcome.destroy()
        crear_interfaz()
    style = ttk.Style(welcome)
    style.theme_use('clam')
    style.configure('Big.TButton', font=('Segoe UI', 17, 'bold'), foreground="white", background="#416bce", padding=13)
    style.map('Big.TButton', background=[('active', '#2b488a')])
    ttk.Button(botones, text="Comenzar", command=comenzar, style='Big.TButton').pack(side='left', padx=30, ipadx=8, ipady=6)
    ttk.Button(botones, text="Salir", command=welcome.quit, style='Big.TButton').pack(side='left', padx=30, ipadx=8, ipady=6)
    tk.Label(welcome, text="© 2025 PRACTICADORES.DEV ver.2.0",
             bg="#375aab", fg="#9dc7fb", font=("Segoe UI", 13, "italic")).pack(side='bottom', pady=14)
    welcome.mainloop()
