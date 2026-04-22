import streamlit as st
import pandas as pd
import base64

# 1. Configuración inicial de la página
st.set_page_config(page_title="Buscador de Plazas SERUMS 2026-I", layout="wide", page_icon="🏥")

# 2. Estilos CSS para colores amigables, calmantes y responsivos
st.markdown("""
    <style>
        /* Fondo general calmante (Alice Blue) */
        .stApp {
            background-color: #F0F8FF; 
        }
        /* Estilo de las tarjetas de resultados */
        .tarjeta-establecimiento {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 15px;
            border-left: 6px solid #8FBC8F; /* Dark Sea Green - Calmante */
        }
        .titulo-centro {
            color: #2F4F4F; /* Dark Slate Gray */
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .badge {
            background-color: #E6E6FA; /* Lavender */
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            color: #483D8B;
            margin-right: 5px;
        }
        /* Sección de Apoyo Colorida */
        .seccion-yape {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            margin-top: 40px;
            color: #333;
        }
        .yape-text {
            font-size: 24px;
            font-weight: bold;
            color: #7A288A; /* Color morado Yape */
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Buscador de Plazas SERUMS 2026-I")
st.markdown("Encuentra tu plaza ideal filtrando por ubicación, profesión y beneficios. Diseñado para ayudarte a tomar la mejor decisión con calma y claridad.")

# 3. Cargar los datos
# Asegúrate de que el archivo Excel consolidado esté en la misma carpeta
@st.cache_data
def cargar_datos():
    # Cambia esto por el nombre exacto de tu archivo final
    df = pd.read_excel('Plazas_Ofertadas_con_Mapas.xlsx')
    # Rellenar valores nulos para evitar errores en los filtros
    return df.fillna("NO ESPECIFICA")

df = cargar_datos()

# 4. Creación de Filtros en la barra lateral o en columnas
st.sidebar.header("🔍 Filtros de Búsqueda")

profesion = st.sidebar.selectbox("1. Profesión", options=["Todos"] + list(df['PROFESIÓN'].unique()))
institucion = st.sidebar.selectbox("2. Institución", options=["Todos"] + list(df['INSTITUCIÓN'].unique()))
departamento = st.sidebar.selectbox("3. Departamento", options=["Todos"] + list(df['DEPARTAMENTO'].unique()))

# Filtrado dinámico de Provincia basado en el Departamento
provincias_filtradas = df[df['DEPARTAMENTO'] == departamento]['PROVINCIA'].unique() if departamento != "Todos" else df['PROVINCIA'].unique()
provincia = st.sidebar.selectbox("4. Provincia", options=["Todos"] + list(provincias_filtradas))

# Filtrado dinámico de Distrito
distritos_filtrados = df[(df['PROVINCIA'] == provincia)]['DISTRITO'].unique() if provincia != "Todos" else df['DISTRITO'].unique()
distrito = st.sidebar.selectbox("5. Distrito", options=["Todos"] + list(distritos_filtrados))

# Para el grado de dificultad asumimos que existe la columna. Si no, quita este filtro.
if 'GRADO DE DIFICULTAD' in df.columns:
    dificultad = st.sidebar.selectbox("6. Grado de Dificultad", options=["Todos"] + list(df['GRADO DE DIFICULTAD'].unique()))
else:
    dificultad = "Todos"

categoria = st.sidebar.selectbox("7. Categoría", options=["Todos"] + list(df['CATEGORÍA'].unique()))
zaf = st.sidebar.selectbox("8. Bono ZAF", options=["Todos", "SI", "NO"])
ze = st.sidebar.selectbox("9. Bono ZE", options=["Todos", "SI", "NO"])

# 5. Aplicar Filtros al DataFrame
df_filtrado = df.copy()
if profesion != "Todos": df_filtrado = df_filtrado[df_filtrado['PROFESIÓN'] == profesion]
if institucion != "Todos": df_filtrado = df_filtrado[df_filtrado['INSTITUCIÓN'] == institucion]
if departamento != "Todos": df_filtrado = df_filtrado[df_filtrado['DEPARTAMENTO'] == departamento]
if provincia != "Todos": df_filtrado = df_filtrado[df_filtrado['PROVINCIA'] == provincia]
if distrito != "Todos": df_filtrado = df_filtrado[df_filtrado['DISTRITO'] == distrito]
if dificultad != "Todos" and 'GRADO DE DIFICULTAD' in df.columns: df_filtrado = df_filtrado[df_filtrado['GRADO DE DIFICULTAD'] == dificultad]
if categoria != "Todos": df_filtrado = df_filtrado[df_filtrado['CATEGORÍA'] == categoria]
if zaf != "Todos": df_filtrado = df_filtrado[df_filtrado['ZAF (*)'] == zaf]
if ze != "Todos": df_filtrado = df_filtrado[df_filtrado['ZE (**)'] == ze]

st.subheader(f"Resultados encontrados: {len(df_filtrado)} plazas")

# 6. Mostrar los Resultados como Tarjetas
for index, row in df_filtrado.iterrows():
    # Construir la tarjeta en HTML
    html_tarjeta = f"""
    <div class="tarjeta-establecimiento">
        <div class="titulo-centro">📍 {row['NOMBRE DE ESTABLECIMIENTO']}</div>
        <p><strong>Ubicación:</strong> {row['DEPARTAMENTO']} - {row['PROVINCIA']} - {row['DISTRITO']}</p>
        <p><strong>Institución:</strong> {row['INSTITUCIÓN']} | <strong>Categoría:</strong> {row['CATEGORÍA']}</p>
        <div>
            <span class="badge">N° Plazas: {row.get('N° PLAZAS', 1)}</span>
            <span class="badge">ZAF: {row['ZAF (*)']}</span>
            <span class="badge">ZE: {row['ZE (**)']}</span>
        </div>
        <br>
        <a href="{row['Link Google Maps']}" target="_blank" style="background-color:#4682B4; color:white; padding:8px 15px; text-decoration:none; border-radius:5px; font-weight:bold;">
            🗺️ Ver en Google Maps
        </a>
    </div>
    """
    st.markdown(html_tarjeta, unsafe_allow_html=True)

# 7. Sección Colorida de Apoyo / Yape
st.markdown("""
    <div class="seccion-yape">
        <p class="yape-text">💜 ¡Apoya este proyecto con Yape!</p>
        <p style="font-size: 16px;">Si esta herramienta te ayudó a encontrar tu plaza ideal, puedes invitarme un café.</p>
    </div>
""", unsafe_allow_html=True)

# Mostrar la imagen del QR (Asegúrate de tener la imagen 'image_2c6c57.jpg' en la misma carpeta)
try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("image_2c6c57.jpg", caption="¡Escanea para apoyar!", use_column_width=True)
except FileNotFoundError:
    st.warning("Coloca tu imagen 'image_2c6c57.jpg' en la misma carpeta para que aparezca el QR.")
