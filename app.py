import streamlit as st
import pandas as pd
import os

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="Buscador de Plazas SERUMS 2026-I", 
    layout="wide", 
    page_icon="🏥"
)

# 2. Estilos CSS: Colores calmantes y corrección de legibilidad (texto oscuro)
st.markdown("""
    <style>
        /* Fondo general calmante (Alice Blue) */
        .stApp {
            background-color: #F0F8FF; 
        }
        /* Estilo de las tarjetas de resultados */
        .tarjeta-establecimiento {
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 20px;
            border-left: 8px solid #8FBC8F; /* Verde suave */
            color: #333333 !important; /* Fuerza el texto a gris oscuro para legibilidad */
        }
        /* Asegurar que todos los textos dentro de la tarjeta sean oscuros */
        .tarjeta-establecimiento p, .tarjeta-establecimiento strong, .tarjeta-establecimiento div {
            color: #333333 !important;
        }
        .titulo-centro {
            color: #2F4F4F; /* Gris azulado oscuro */
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 12px;
        }
        .badge {
            background-color: #E6E6FA; /* Lavanda */
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: bold;
            color: #483D8B !important;
            margin-right: 8px;
            display: inline-block;
            margin-top: 5px;
        }
        /* Sección de Apoyo llamativa y colorida */
        .seccion-yape {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 35px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            margin-top: 50px;
            border: 2px solid #FFFFFF;
        }
        .yape-text {
            font-size: 28px;
            font-weight: bold;
            color: #7A288A; /* Color morado Yape */
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Buscador de Plazas SERUMS 2026-I")
st.markdown("Busca y filtra las plazas disponibles de forma sencilla. Los datos incluyen coordenadas exactas para Google Maps.")

# 3. Función para cargar datos desde el Excel
@st.cache_data
def cargar_datos():
    try:
        # Asegúrate de que este nombre coincida con tu archivo en GitHub
        df = pd.read_excel('Plazas_Ofertadas_con_Mapas.xlsx')
        return df.fillna("NO ESPECIFICA")
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel: {e}")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    # 4. Barra lateral con filtros mejorados
    st.sidebar.header("🔍 Filtros de Búsqueda")

    profesion = st.sidebar.selectbox("1. Profesión", options=["Todos"] + sorted(list(df['PROFESIÓN'].unique())))
    institucion = st.sidebar.selectbox("2. Institución", options=["Todos"] + sorted(list(df['INSTITUCIÓN'].unique())))
    departamento = st.sidebar.selectbox("3. Departamento", options=["Todos"] + sorted(list(df['DEPARTAMENTO'].unique())))

    # Filtros dependientes para Provincia y Distrito
    if departamento != "Todos":
        prov_opts = sorted(list(df[df['DEPARTAMENTO'] == departamento]['PROVINCIA'].unique()))
    else:
        prov_opts = sorted(list(df['PROVINCIA'].unique()))
    provincia = st.sidebar.selectbox("4. Provincia", options=["Todos"] + prov_opts)

    if provincia != "Todos":
        dist_opts = sorted(list(df[df['PROVINCIA'] == provincia]['DISTRITO'].unique()))
    else:
        dist_opts = sorted(list(df['DISTRITO'].unique()))
    distrito = st.sidebar.selectbox("5. Distrito", options=["Todos"] + dist_opts)

    # Filtros adicionales
    categoria = st.sidebar.selectbox("6. Categoría", options=["Todos"] + sorted(list(df['CATEGORÍA'].unique())))
    zaf = st.sidebar.selectbox("7. Bono ZAF", options=["Todos", "SI", "NO"])
    ze = st.sidebar.selectbox("8. Bono ZE", options=["Todos", "SI", "NO"])

    # 5. Lógica de Filtrado
    df_filtrado = df.copy()
    if profesion != "Todos": df_filtrado = df_filtrado[df_filtrado['PROFESIÓN'] == profesion]
    if institucion != "Todos": df_filtrado = df_filtrado[df_filtrado['INSTITUCIÓN'] == institucion]
    if departamento != "Todos": df_filtrado = df_filtrado[df_filtrado['DEPARTAMENTO'] == departamento]
    if provincia != "Todos": df_filtrado = df_filtrado[df_filtrado['PROVINCIA'] == provincia]
    if distrito != "Todos": df_filtrado = df_filtrado[df_filtrado['DISTRITO'] == distrito]
    if categoria != "Todos": df_filtrado = df_filtrado[df_filtrado['CATEGORÍA'] == categoria]
    if zaf != "Todos": df_filtrado = df_filtrado[df_filtrado['ZAF (*)'] == zaf]
    if ze != "Todos": df_filtrado = df_filtrado[df_filtrado['ZE (**)'] == ze]

    st.subheader(f"📍 {len(df_filtrado)} plazas encontradas")

    # 6. Mostrar resultados en tarjetas legibles
    for index, row in df_filtrado.iterrows():
        n_plazas = row.get('N° PLAZAS', 1)
        
        html_card = f"""
        <div class="tarjeta-establecimiento">
            <div class="titulo-centro">🏥 {row['NOMBRE DE ESTABLECIMIENTO']}</div>
            <p><strong>Ubicación:</strong> {row['DEPARTAMENTO']} > {row['PROVINCIA']} > {row['DISTRITO']}</p>
            <p><strong>Detalles:</strong> {row['INSTITUCIÓN']} | Categoría {row['CATEGORÍA']}</p>
            <div>
                <span class="badge">👥 Plazas: {n_plazas}</span>
                <span class="badge">💰 ZAF: {row['ZAF (*)']}</span>
                <span class="badge">🔥 ZE: {row['ZE (**)']}</span>
            </div>
            <br>
            <a href="{row['Link Google Maps']}" target="_blank" style="background-color:#4682B4; color:white; padding:10px 20px; text-decoration:none; border-radius:8px; font-weight:bold; display:inline-block; margin-top:10px;">
                🗺️ Ver ubicación exacta
            </a>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)

    # 7. Sección de Apoyo / Yape
    st.markdown("""
        <div class="seccion-yape">
            <p class="yape-text">💜 ¿Te sirvió la herramienta?</p>
            <p style="font-size: 18px; color: #444;">Puedes apoyar este proyecto escaneando el QR de Yape para seguir mejorando la plataforma.</p>
        </div>
    """, unsafe_allow_html=True)

    # Mostrar QR con manejo de errores y nombre de archivo corregido
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        qr_path = "image_2c6c57.jpeg"
        if os.path.exists(qr_path):
            st.image(qr_path, caption="¡Muchas gracias por tu apoyo!", use_container_width=True)
        else:
            st.info("Sube tu imagen 'image_2c6c57.jpeg' a GitHub para visualizar el QR de apoyo.")
else:
    st.warning("No se encontró información. Verifica que el archivo Excel esté en el repositorio.")
