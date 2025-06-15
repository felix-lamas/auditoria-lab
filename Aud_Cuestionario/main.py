# main.py

import smtplib
from email.message import EmailMessage

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
from cuestionarios import cuestionarios
from exportar_pdf import generar_pdf

st.set_page_config(page_title="Auditoría Informática", layout="wide")

st.title("🧾 Sistema de Auditoría Física Informática")
st.subheader("Universidad Autónoma Juan Misael Saracho - Laboratorio de Redes")


seccion = st.sidebar.selectbox("Selecciona una categoría para auditar", list(cuestionarios.keys()))


st.sidebar.markdown("### Datos del Auditor")
nombre_auditor = st.sidebar.text_input("Nombre completo")
fecha = st.sidebar.date_input("Fecha de auditoría", datetime.date.today())

if nombre_auditor.strip() == "":
    st.warning("⚠️ Debes ingresar tu nombre para comenzar.")
    st.stop()


st.markdown(f"## Formulario: {seccion}")
respuestas = {}

with st.form("formulario_auditoria"):
    for idx, item in enumerate(cuestionarios[seccion]):
        pregunta = item["pregunta"]
        tipo = item["tipo"]

        if tipo == "si_no":
            respuesta = st.radio(pregunta, ["Sí", "No"], key=f"{seccion}_{idx}")
        elif tipo == "numero":
            respuesta = st.number_input(pregunta, min_value=0, step=1, key=f"{seccion}_{idx}")
        elif tipo == "escala":
            respuesta = st.slider(pregunta, 1, 5, key=f"{seccion}_{idx}")
        elif tipo == "multiple":
            respuesta = st.selectbox(pregunta, item["opciones"], key=f"{seccion}_{idx}")
        elif tipo == "texto":
            respuesta = st.text_area(pregunta, key=f"{seccion}_{idx}")
        else:
            respuesta = "No definido"

        respuestas[pregunta] = respuesta

    enviado = st.form_submit_button("Enviar respuestas")


def enviar_correo(nombre_auditor, seccion, fecha_str, csv_path, pdf_path):
    emisor = "felix99.lamas@gmail.com"
    receptor = "felix99.lamas@gmail.com"  
    asunto = f"📝 Respuestas - {nombre_auditor} - {seccion}"
    cuerpo = f"Adjunto las respuestas del cuestionario {seccion} realizadas por {nombre_auditor} el {fecha_str}."

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = emisor
    msg["To"] = receptor
    msg.set_content(cuerpo)

    with open(csv_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=os.path.basename(csv_path))

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(emisor, "zsts ydef fljf dojr")  
        smtp.send_message(msg)

if enviado:
    st.success("✅ Respuestas registradas correctamente.")
    
    df = pd.DataFrame(list(respuestas.items()), columns=["Pregunta", "Respuesta"])

    
    os.makedirs("resultados/csv", exist_ok=True)
    os.makedirs("resultados/pdf", exist_ok=True)

    
    fecha_str = fecha.strftime("%Y-%m-%d")
    nombre_base = f"{seccion}_{nombre_auditor.replace(' ', '_')}_{fecha_str}"

    
    csv_path = f"resultados/csv/{nombre_base}.csv"
    contador = 1
    while os.path.exists(csv_path):
        contador += 1
        csv_path = f"resultados/csv/{nombre_base}_v{contador}.csv"
    
    df.to_csv(csv_path, index=False)
    st.success(f"📁 Respuestas guardadas en: `{csv_path}`")


    st.write("### 🗂️ Resumen de respuestas")
    st.dataframe(df)

    
    st.write("### 📊 Estadísticas y visualización")
    if df["Respuesta"].isin(["Sí", "No"]).any():
        respuestas_binarias = df[df["Respuesta"].isin(["Sí", "No"])]
        conteo = respuestas_binarias["Respuesta"].value_counts()

        fig, ax = plt.subplots()
        colores = ['green' if val == 'Sí' else 'red' for val in conteo.index]
        conteo.plot(kind="bar", color=colores, ax=ax)
        ax.set_title("Respuestas Sí / No")
        st.pyplot(fig)

    
    pdf_path = f"resultados/pdf/{nombre_base}.pdf"
    contador_pdf = 1
    while os.path.exists(pdf_path):
        contador_pdf += 1
        pdf_path = f"resultados/pdf/{nombre_base}_v{contador_pdf}.pdf"

    
    generar_pdf(nombre_auditor, seccion, fecha_str, respuestas, pdf_path)
    st.success(f"📄 Informe PDF generado: `{pdf_path}`")

    
    enviar_correo(nombre_auditor, seccion, fecha_str, csv_path, pdf_path)
    st.success("📧 Correo enviado con los archivos adjuntos.")
