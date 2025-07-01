import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from alumno_crud import agregar_alumno, obtener_alumnos, actualizar_alumno, borrar_alumno
from pdf_export import exportar_a_pdf, imprimir_pdf
import platform
import math

def limpiar_formulario(campos):
    for campo in campos.values():
        campo.delete(0, tk.END)

def cargar_datos(tree):
    for fila in tree.get_children():
        tree.delete(fila)
    for i, alumno in enumerate(obtener_alumnos()):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', tk.END, values=alumno, tags=(tag,))
    tree.tag_configure('evenrow', background='#eaf3fc')
    tree.tag_configure('oddrow', background='#f7fbff')

def crear_interfaz():
    root = tk.Tk()
    root.title("AcademyGo - Gestión de Alumnos")

    # Aplicar pantalla completa o maximizada según sistema operativo
    sistema = platform.system()
    if sistema == 'Windows':
        root.state('zoomed')
    else:
        root.attributes('-zoomed', True)

    root.configure(bg="#e9f0fb")

    # Cabecera con logo grande y título
    header = tk.Frame(root, bg="#375aab", height=170)
    header.pack(fill='x', side='top')

    # Logo grande
    logo_img = Image.open("academygo.png")
    logo_img = logo_img.resize((150, 150), Image.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header, image=logo_tk, bg="#375aab")
    logo_label.image = logo_tk
    logo_label.pack(side="left", padx=32, pady=10)

    tk.Label(header, text="AcademyGo", bg="#375aab", fg="white",
             font=("Segoe UI", 35, "bold"), pady=15).pack(side="left", padx=28)
    tk.Label(header, text="Gestión profesional de alumnos", bg="#375aab", fg="#c7e0fa",
             font=("Segoe UI", 16, "italic")).pack(side="left", padx=10, pady=25)

    frame = ttk.Frame(root, padding=26)
    frame.pack(fill='both', expand=True, padx=40, pady=18)

    labels = ['Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Mail', 'Fecha nacimiento (YYYY-MM-DD)', 'Nivel académico']
    keys = ['nombre', 'apellidos', 'dni', 'telefono', 'mail', 'f_nacimiento', 'niv_academico']
    campos = {}

    form = ttk.LabelFrame(frame, text="Datos del Alumno", padding=(20,12))
    form.grid(row=0, column=0, sticky='nw', rowspan=2, pady=12)

    for i, (label, key) in enumerate(zip(labels, keys)):
        ttk.Label(form, text=label + ":", anchor='w').grid(row=i, column=0, pady=7, sticky='e')
        entry = ttk.Entry(form, width=25, font=('Segoe UI', 12))
        entry.grid(row=i, column=1, pady=7, padx=7, sticky='w')
        campos[key] = entry

    btns = ttk.Frame(form)
    btns.grid(row=7, column=0, columnspan=2, pady=(18, 10))

    style = ttk.Style(root)
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

    def guardar():
        valores = [campos[k].get() for k in keys]
        if not valores[0]:
            messagebox.showwarning("Atención", "El nombre es obligatorio.")
            return
        try:
            agregar_alumno(*valores)
            cargar_datos(tree)
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
            cargar_datos(tree)
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
                cargar_datos(tree)
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

    cols = ('ID', 'Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Mail', 'Fecha nacimiento', 'Nivel académico')
    tree = ttk.Treeview(frame, columns=cols, show='headings', height=14)
    for i, col in enumerate(cols):
        tree.heading(col, text=col)
        ancho = 65 if i==0 else 120 if i==6 else 110
        tree.column(col, width=ancho, anchor='center')
    tree.grid(row=0, column=1, padx=(30,5), pady=10, sticky='n')

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=2, sticky='ns', pady=10)
    tree.configure(yscrollcommand=scrollbar.set)

    cargar_datos(tree)

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
    extra_btns.grid(row=1, column=1, pady=(14,0), sticky='w')

    def exportar():
        datos = [tree.item(f, 'values') for f in tree.get_children()]
        cols = ('ID', 'Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Mail', 'Fecha nacimiento', 'Nivel académico')
        exportar_a_pdf(datos, cols)

    def imprimir():
        imprimir_pdf()

    def volver_a_bienvenida():
        root.destroy()
        pantalla_bienvenida()

    def salir_app():
        root.destroy()

    ttk.Button(extra_btns, text="📄 Exportar a PDF", command=exportar, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🖨️ Imprimir", command=imprimir).pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🏠 Volver a inicio", command=volver_a_bienvenida, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="❌ Salir", command=salir_app, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)

    ttk.Separator(root, orient='horizontal').pack(fill='x', pady=4)
    tk.Label(
        root,
        text="Desarrollado por PRACTICADORES.DEV  |  AcademyGo",
        font=("Segoe UI", 11, "italic"),
        bg="#e9f0fb", fg="#666"
    ).pack(side='bottom', pady=3)

    root.mainloop()

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
        text="© 2025 PRACTICADORES.DEV",
        bg="#375aab",
        fg="#9dc7fb",
        font=("Segoe UI", 13, "italic")
    ).pack(side='bottom', pady=14)

    welcome.mainloop()
