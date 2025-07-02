import tkinter as tk
from tkinter import ttk, messagebox
import smtplib
from email.mime.text import MIMEText
from curso_crud import obtener_familias, obtener_cursos_finalizados
from alumno_crud import obtener_alumnos
from database import conectar

def abrir_busqueda_avanzada(parent=None):
    ventana = tk.Toplevel(parent)
    ventana.title("Búsqueda Avanzada de Alumnos")
    ventana.geometry("950x550")
    ventana.configure(bg="#eaf3fc")

    filtros_frame = ttk.LabelFrame(ventana, text="Filtros de Búsqueda")
    filtros_frame.pack(fill="x", padx=18, pady=10)

    tk.Label(filtros_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=3)
    nombre_entry = ttk.Entry(filtros_frame)
    nombre_entry.grid(row=0, column=1, padx=5, pady=3)

    tk.Label(filtros_frame, text="Apellidos:").grid(row=0, column=2, padx=5, pady=3)
    apellidos_entry = ttk.Entry(filtros_frame)
    apellidos_entry.grid(row=0, column=3, padx=5, pady=3)

    tk.Label(filtros_frame, text="Fecha nacimiento >=") \
        .grid(row=1, column=0, padx=5, pady=3)
    fecha_nac_entry = ttk.Entry(filtros_frame)
    fecha_nac_entry.grid(row=1, column=1, padx=5, pady=3)

    tk.Label(filtros_frame, text="Familia profesional:").grid(row=1, column=2, padx=5, pady=3)
    familias = obtener_familias()
    familias_opc = [""] + [f"{f[0]} - {f[1]}" for f in familias]
    familia_combo = ttk.Combobox(filtros_frame, values=familias_opc, state="readonly")
    familia_combo.grid(row=1, column=3, padx=5, pady=3)

    tk.Label(filtros_frame, text="Finalizó curso desde:").grid(row=2, column=0, padx=5, pady=3)
    fecha_fin_entry = ttk.Entry(filtros_frame)
    fecha_fin_entry.grid(row=2, column=1, padx=5, pady=3)

    # Tabla de resultados
    cols = ("ID", "Nombre", "Apellidos", "Email", "Fecha Nacimiento", "Familia", "Fecha Fin Curso")
    tree = ttk.Treeview(ventana, columns=cols, show="headings", selectmode="extended", height=14)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=120 if c not in ("Email", "Familia") else 170, anchor="center")
    tree.pack(fill="both", padx=18, pady=12, expand=True)

    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    scrollbar.place(in_=tree, relx=1.0, rely=0, relheight=1.0, anchor='ne')
    tree.configure(yscrollcommand=scrollbar.set)

    def buscar():
        # Montar consulta filtrando por todos los campos
        conn = conectar()
        cur = conn.cursor()
        sql = """
            SELECT a.id, a.nombre, a.apellidos, a.mail, a.f_nacimiento,
                   f.nombre_fam, cf.fecha_fin
            FROM alumnos a
            LEFT JOIN cursos_fin cf ON a.id = cf.alumno_id
            LEFT JOIN cursos c ON cf.curso_id = c.id
            LEFT JOIN fam_prof f ON c.fam_curso = f.id
            WHERE 1=1
        """
        params = []
        if nombre_entry.get():
            sql += " AND a.nombre LIKE %s"
            params.append(f"%{nombre_entry.get()}%")
        if apellidos_entry.get():
            sql += " AND a.apellidos LIKE %s"
            params.append(f"%{apellidos_entry.get()}%")
        if fecha_nac_entry.get():
            sql += " AND a.f_nacimiento >= %s"
            params.append(fecha_nac_entry.get())
        if familia_combo.get():
            fam_id = familia_combo.get().split(" - ")[0]
            sql += " AND f.id = %s"
            params.append(fam_id)
        if fecha_fin_entry.get():
            sql += " AND cf.fecha_fin >= %s"
            params.append(fecha_fin_entry.get())

        sql += " GROUP BY a.id"
        cur.execute(sql, params)
        resultados = cur.fetchall()
        cur.close()
        conn.close()

        for i in tree.get_children():
            tree.delete(i)
        for row in resultados:
            tree.insert("", "end", values=row)

    def enviar_emails():
        seleccionados = tree.selection()
        if not seleccionados:
            messagebox.showinfo("Selecciona", "Selecciona los alumnos a los que enviar email.")
            return
        emails = []
        for sel in seleccionados:
            data = tree.item(sel, "values")
            if data[3]:
                emails.append(data[3])
        if not emails:
            messagebox.showinfo("Sin emails", "No hay emails válidos seleccionados.")
            return
        # Pedir asunto y cuerpo del mensaje
        win = tk.Toplevel(ventana)
        win.title("Enviar email")
        tk.Label(win, text="Asunto:").pack()
        asunto_entry = ttk.Entry(win, width=50)
        asunto_entry.pack(padx=7, pady=2)
        tk.Label(win, text="Mensaje:").pack()
        cuerpo_text = tk.Text(win, width=60, height=10)
        cuerpo_text.pack(padx=7, pady=2)
        def enviar():
            asunto = asunto_entry.get()
            cuerpo = cuerpo_text.get("1.0", "end").strip()
            if not asunto or not cuerpo:
                messagebox.showwarning("Faltan datos", "Pon asunto y mensaje")
                return
            # Envío SMTP (sólo ejemplo, cambia los datos de acceso)
            try:
                smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp.login('TU_EMAIL@gmail.com', 'TU_CONTRASEÑA')
                for email in emails:
                    msg = MIMEText(cuerpo)
                    msg['Subject'] = asunto
                    msg['From'] = 'TU_EMAIL@gmail.com'
                    msg['To'] = email
                    smtp.sendmail('TU_EMAIL@gmail.com', email, msg.as_string())
                smtp.quit()
                messagebox.showinfo("Éxito", f"Enviados a {len(emails)} destinatarios.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo enviar: {e}")

        ttk.Button(win, text="Enviar", command=enviar).pack(pady=6)

    botones = ttk.Frame(ventana)
    botones.pack(pady=4)
    ttk.Button(botones, text="Buscar", command=buscar).pack(side="left", padx=6, ipadx=6, ipady=2)
    ttk.Button(botones, text="Enviar Email a Seleccionados", command=enviar_emails).pack(side="left", padx=6, ipadx=6, ipady=2)
    ttk.Button(botones, text="Cerrar", command=ventana.destroy).pack(side="left", padx=6, ipadx=6, ipady=2)
