import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from alumno_crud import agregar_alumno, obtener_alumnos, actualizar_alumno, borrar_alumno
from crud_otros import agregar_curso, obtener_cursos, actualizar_curso, borrar_curso
from pdf_export import exportar_a_pdf, imprimir_pdf
import platform
import math

# Colores más fuertes para las pestañas
TAB_COLORS = [
    "#d4e2fc",   # Alumnos - azul claro fuerte
    "#c1d6f8",   # Cursos
    "#d9d6f2",   # Inscripciones
    "#e2d9f4",   # Cursos Finalizados
    "#dce4f7",   # Familias Profesionales
    "#d0f0ed",   # Adjuntos
]

PAGINA_TAMANO = 20  # filas por página

def limpiar_formulario(campos):
    for campo in campos.values():
        campo.delete(0, tk.END)

# --- Funciones para cargar datos con paginación ---

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

# --- INTERFAZ PRINCIPAL ---

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

    # Notebook / pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=9, pady=9)

    # Crear pestañas con colores más fuertes
    tab_alumnos = tk.Frame(notebook, bg=TAB_COLORS[0])
    notebook.add(tab_alumnos, text="Alumnos")

    tab_cursos = tk.Frame(notebook, bg=TAB_COLORS[1])
    notebook.add(tab_cursos, text="Cursos")

    tab_inscr = tk.Frame(notebook, bg=TAB_COLORS[2])
    notebook.add(tab_inscr, text="Inscripciones")

    tab_cfin = tk.Frame(notebook, bg=TAB_COLORS[3])
    notebook.add(tab_cfin, text="Cursos Finalizados")

    tab_familias = tk.Frame(notebook, bg=TAB_COLORS[4])
    notebook.add(tab_familias, text="Familias Profesionales")

    tab_adj = tk.Frame(notebook, bg=TAB_COLORS[5])
    notebook.add(tab_adj, text="Adjuntos")

    # Contenido y paginación en ALUMNOS
    contenido_alumnos(tab_alumnos, root)

    # Contenido y paginación en CURSOS
    contenido_cursos(tab_cursos, root)

    # Maquetas para otras pestañas
    pestaña_maqueta(tab_inscr, "Gestión de Inscripciones\n(Próximamente)", TAB_COLORS[2])
    pestaña_maqueta(tab_cfin, "Cursos Finalizados\n(Próximamente)", TAB_COLORS[3])
    pestaña_maqueta(tab_familias, "Gestión Familias\n(Próximamente)", TAB_COLORS[4])
    pestaña_maqueta(tab_adj, "Adjuntos/Documentos\n(Próximamente)", TAB_COLORS[5])

    # Footer
    tk.Label(
        root,
        text="Desarrollado por PRACTICADORES.DEV  |  AcademyGo",
        font=("Segoe UI", 11, "italic"),
        bg="#e9f0fb", fg="#666"
    ).pack(side='bottom', pady=3)

    root.mainloop()

# --- CONTENIDO PESTAÑA ALUMNOS ---

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

    # Botones CRUD
    btns = ttk.Frame(form)
    btns.grid(row=7, column=0, columnspan=2, pady=(18, 10))

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'), foreground="white", background="#416bce")
    style.map('Accent.TButton', background=[('active', '#2b488a')])
    style.configure('Treeview',
                    background="#f7fbff",
                    foreground="#222",
                    rowheight=38,
                    fieldbackground="#f7fbff",
                    font=('Segoe UI', 12))
    style.configure('Treeview.Heading',
                    background="#375aab",
                    foreground="white",
                    font=('Segoe UI', 13, 'bold'),
                    relief='flat')
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

    ttk.Button(btns, text="💾 Guardar", command=guardar, style='Accent.TButton').pack(side='left', padx=7)
    ttk.Button(btns, text="✏️ Actualizar", command=actualizar).pack(side='left', padx=7)
    ttk.Button(btns, text="🗑️ Borrar", command=borrar).pack(side='left', padx=7)
    ttk.Button(btns, text="🧹 Limpiar", command=limpiar).pack(side='left', padx=7)

    # Tabla alumnos
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

    # Botones paginación
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

    # Botones PDF/Imprimir/Inicio/Salir (debajo de la tabla)
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

    ttk.Button(extra_btns, text="📄 Exportar a PDF", command=exportar, style='Accent.TButton').pack(side='left', padx=6,
                                                                                                     ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🖨️ Imprimir", command=imprimir).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🏠 Volver a inicio", command=volver_a_bienvenida, style='Accent.TButton').pack(side='left',
                                                                                                             padx=6,
                                                                                                             ipadx=4,
                                                                                                             ipady=3)
    ttk.Button(extra_btns, text="❌ Salir", command=salir_app, style='Accent.TButton').pack(side='left', padx=6, ipadx=4,
                                                                                           ipady=3)


# --- CONTENIDO PESTAÑA CURSOS ---

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

    # Botones CRUD
    btns = ttk.Frame(form)
    btns.grid(row=7, column=0, columnspan=2, pady=(18, 10))

    style = ttk.Style()
    style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'), foreground="white", background="#416bce")
    style.map('Accent.TButton', background=[('active', '#2b488a')])

    pagina_actual = [0]

    def limpiar_formulario():
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
            limpiar_formulario()
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
            limpiar_formulario()
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
                limpiar_formulario()
                tab.selected_id = None
                messagebox.showinfo("Éxito", "Curso borrado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo borrar: {e}")

    ttk.Button(btns, text="💾 Guardar", command=guardar, style='Accent.TButton').pack(side='left', padx=7)
    ttk.Button(btns, text="✏️ Actualizar", command=actualizar).pack(side='left', padx=7)
    ttk.Button(btns, text="🗑️ Borrar", command=borrar).pack(side='left', padx=7)
    ttk.Button(btns, text="🧹 Limpiar", command=limpiar_formulario).pack(side='left', padx=7)

    # Tabla cursos
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

    # Paginación
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

    # Botones Exportar, Imprimir, Volver e Salir
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

    ttk.Button(extra_btns, text="📄 Exportar a PDF", command=exportar, style='Accent.TButton').pack(side='left', padx=6,
                                                                                                     ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🖨️ Imprimir", command=imprimir).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🏠 Volver a inicio", command=volver_a_bienvenida, style='Accent.TButton').pack(side='left',
                                                                                                             padx=6,
                                                                                                             ipadx=4,
                                                                                                             ipady=3)
    ttk.Button(extra_btns, text="❌ Salir", command=salir_app, style='Accent.TButton').pack(side='left', padx=6, ipadx=4,
                                                                                           ipady=3)

# --- MAQUETAS PESTAÑAS VACÍAS ---

def pestaña_maqueta(tab, texto="Funcionalidad en desarrollo...", color="#fafafa"):
    f = tk.Frame(tab, bg=color)
    f.pack(expand=True, fill="both")
    tk.Label(f, text=texto, font=("Segoe UI", 24, "italic"), bg=color, fg="#375aab").pack(expand=True)

# --- PANTALLA DE BIENVENIDA ---

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
        # base
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

    tk.Label(
        welcome,
        text="AcademyGo",
        bg="#375aab",
        fg="white",
        font=("Segoe UI", 42, "bold")
    ).pack(pady=4)

    tk.Label(
        welcome,
        text="PRACTICADORES.DEV",
        bg="#375aab",
        fg="#c7e0fa",
        font=("Segoe UI", 20, "italic")
    ).pack(pady=2)

    botones = tk.Frame(welcome, bg="#375aab")
    botones.pack(pady=30)

    def comenzar():
        welcome.destroy()
        crear_interfaz()

    style = ttk.Style(welcome)
    style.theme_use('clam')
    style.configure('Big.TButton', font=('Segoe UI', 17, 'bold'), foreground="white", background="#416bce", padding=13)
    style.map('Big.TButton', background=[('active', '#2b488a')])

    ttk.Button(
        botones, text="Comenzar", command=comenzar, style='Big.TButton'
    ).pack(side='left', padx=30, ipadx=8, ipady=6)

    ttk.Button(
        botones, text="Salir", command=welcome.quit, style='Big.TButton'
    ).pack(side='left', padx=30, ipadx=8, ipady=6)

    tk.Label(
        welcome,
        text="© 2025 PRACTICADORES.DEV ver.2.0",
        bg="#375aab",
        fg="#9dc7fb",
        font=("Segoe UI", 13, "italic")
    ).pack(side='bottom', pady=14)

    welcome.mainloop()
