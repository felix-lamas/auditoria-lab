from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.alias_nb_pages()

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Informe de Auditoría Física Informática", ln=True, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(0, 10, "Universidad Autónoma Juan Misael Saracho - Laboratorio de Redes", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

    def add_auditor_info(self, nombre, seccion, fecha_str):
        self.set_font("Helvetica", "", 11)
        self.cell(0, 10, f"Auditor: {nombre}", ln=True)
        self.cell(0, 10, f"Sección auditada: {seccion}", ln=True)
        self.cell(0, 10, f"Fecha: {fecha_str}", ln=True)
        self.ln(5)

    def add_respuestas(self, respuestas):
        self.set_font("Helvetica", "", 10)
        for i, (pregunta, respuesta) in enumerate(respuestas.items(), start=1):
            self.multi_cell(0, 8, f"{i}. {pregunta}\n   Respuesta: {respuesta}")
            self.ln(1)

def generar_pdf(nombre, seccion, fecha_str, respuestas, archivo_salida):
    pdf = PDF()
    pdf.add_page()
    pdf.add_auditor_info(nombre, seccion, fecha_str)
    pdf.add_respuestas(respuestas)
    pdf.output(archivo_salida)
