import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Auditoría Infraestructura", layout="centered")

st.title("🧾 Cuestionario - Auditoría Física: Infraestructura")
st.subheader("Universidad Autónoma Juan Misael Saracho - Laboratorio de Redes")

# Preguntas del cuestionario
preguntas = {
    "¿El cableado estructurado está canalizado?": None,
    "¿Hay UPS o planta eléctrica de respaldo?": None,
    "¿Existen suficientes tomas eléctricas?": None,
    "¿Las conexiones están etiquetadas correctamente?": None,
    "¿Se realiza mantenimiento preventivo periódico?": None
}

# Formulario
with st.form("cuestionario_form"):
    respuestas = {}
    for pregunta in preguntas:
        respuesta = st.radio(pregunta, ["Sí", "No"], key=pregunta)
        respuestas[pregunta] = respuesta

    submitted = st.form_submit_button("Enviar Respuestas")

# Procesar resultados
if submitted:
    st.success("✅ Respuestas registradas correctamente.")

    # Crear DataFrame
    df = pd.DataFrame(respuestas.items(), columns=["Pregunta", "Respuesta"])

    # Mostrar tabla
    st.write("### 🗂️ Resumen de respuestas")
    st.dataframe(df)

    # Estadísticas
    conteo = df["Respuesta"].value_counts()
    st.write("### 📊 Resultados estadísticos")
    st.write(conteo)

    # Gráfico de barras
    fig, ax = plt.subplots()
    colores = ['green' if r == 'Sí' else 'red' for r in conteo.index]
    conteo.plot(kind="bar", color=colores, ax=ax)
    ax.set_title("Respuestas del Cuestionario de Infraestructura")
    ax.set_ylabel("Cantidad")
    ax.set_xlabel("Respuesta")
    st.pyplot(fig)

    # Guardar resultados
    df.to_csv("respuestas_infraestructura.csv", index=False)
    st.success("📁 Archivo CSV generado: respuestas_infraestructura.csv")
