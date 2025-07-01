import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from alumno_crud import agregar_alumno, obtener_alumnos, actualizar_alumno, borrar_alumno
from pdf_export import exportar_a_pdf, imprimir_pdf
import platform

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
        root.state('zoomed')  # Compatible con Windows
    else:
        root.attributes('-zoomed', True)  # Compatible con Linux/macOS

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

    # Botones PDF/Imprimir (debajo de la tabla)
    extra_btns = ttk.Frame(frame)
    extra_btns.grid(row=1, column=1, pady=(14,0), sticky='w')

    def exportar():
        datos = [tree.item(f, 'values') for f in tree.get_children()]
        cols = ('ID', 'Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Mail', 'Fecha nacimiento', 'Nivel académico')
        exportar_a_pdf(datos, cols)

    def imprimir():
        imprimir_pdf()

    ttk.Button(extra_btns, text="📄 Exportar a PDF", command=exportar, style='Accent.TButton').pack(side='left', padx=6, ipadx=4, ipady=3)
    ttk.Button(extra_btns, text="🖨️ Imprimir", command=imprimir).pack(side='left', padx=6, ipadx=4, ipady=3)

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

    logo_img = Image.open("academygo.png")
    screen_width = welcome.winfo_screenwidth()
    screen_height = welcome.winfo_screenheight()
    logo_size = min(int(screen_height * 0.33), 350)
    logo_img = logo_img.resize((logo_size, logo_size), Image.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(welcome, image=logo_tk, bg="#375aab")
    logo_label.image = logo_tk
    logo_label.pack(pady=int(screen_height * 0.08))

    tk.Label(
        welcome,
        text="AcademyGo",
        bg="#375aab",
        fg="white",
        font=("Segoe UI", 48, "bold")
    ).pack(pady=10)

    tk.Label(
        welcome,
        text="PRACTICADORES.DEV",
        bg="#375aab",
        fg="#c7e0fa",
        font=("Segoe UI", 22, "italic")
    ).pack(pady=6)

    botones = tk.Frame(welcome, bg="#375aab")
    botones.pack(pady=40)

    def comenzar():
        welcome.destroy()
        crear_interfaz()

    style = ttk.Style(welcome)
    style.theme_use('clam')
    style.configure('Big.TButton', font=('Segoe UI', 19, 'bold'), foreground="white", background="#416bce", padding=14)
    style.map('Big.TButton', background=[('active', '#2b488a')])

    ttk.Button(
        botones, text="Comenzar", command=comenzar, style='Big.TButton'
    ).pack(side='left', padx=30, ipadx=8, ipady=8)

    ttk.Button(
        botones, text="Salir", command=welcome.quit, style='Big.TButton'
    ).pack(side='left', padx=30, ipadx=8, ipady=8)

    tk.Label(
        welcome,
        text="© 2025 PRACTICADORES.DEV",
        bg="#375aab",
        fg="#9dc7fb",
        font=("Segoe UI", 14, "italic")
    ).pack(side='bottom', pady=20)

    welcome.mainloop()
