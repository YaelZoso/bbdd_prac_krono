from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import platform
from tkinter import messagebox

def exportar_a_pdf(datos, cols, pdf_path="alumnos_exportados.pdf"):
    if not datos:
        messagebox.showwarning("Sin datos", "No hay alumnos para exportar.")
        return False

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Logo en la cabecera (opcional: pon la ruta si quieres el logo)
    # from reportlab.platypus import Image as RLImage
    # try:
    #     img = RLImage('academygo.png', width=70, height=70)
    #     img.drawOn(c, 40, height - 100)
    # except Exception: pass

    c.setFont("Helvetica-Bold", 22)
    c.drawString(140, height - 60, "Listado de Alumnos")
    c.setFont("Helvetica", 13)

    # Encabezados
    y = height - 100
    x_offsets = [40, 110, 210, 320, 410, 530, 650, 770]
    for i, col in enumerate(cols):
        c.drawString(x_offsets[i], y, str(col))
    y -= 25
    c.setFont("Helvetica", 11)

    for alumno in datos:
        for i, campo in enumerate(alumno):
            c.drawString(x_offsets[i], y, str(campo))
        y -= 22
        if y < 60:
            c.showPage()
            y = height - 60
            c.setFont("Helvetica", 11)
    c.save()
    messagebox.showinfo("Exportación PDF", f"PDF generado correctamente:\n{pdf_path}")
    return True

def imprimir_pdf(pdf_path="alumnos_exportados.pdf"):
    if not os.path.exists(pdf_path):
        messagebox.showwarning("No hay PDF", "Primero exporta a PDF antes de imprimir.")
        return
    if platform.system() == "Windows":
        try:
            os.startfile(pdf_path, "print")
            messagebox.showinfo("Imprimir", "Enviado a la impresora predeterminada.")
        except Exception as e:
            messagebox.showerror("Error de impresión", f"No se pudo imprimir:\n{e}")
    else:
        try:
            os.system(f"lp '{pdf_path}'")
            messagebox.showinfo("Imprimir", "Enviado a la impresora predeterminada.")
        except Exception as e:
            messagebox.showerror("Error de impresión", f"No se pudo imprimir:\n{e}")
