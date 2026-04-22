import streamlit as st
import pandas as pd
import os

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="Buscador de Plazas SERUMS 2026-I", 
    layout="wide", 
    page_icon="🏥"
)

# 2. Estilos CSS: Colores con alto contraste y tonos oscuros para títulos
st.markdown("""
    <style>
        /* Fondo general calmante */
        .stApp {
            background-color: #F8FAFC; 
        }
        
        /* Título Principal y Subtítulos (Azul Oscuro para visibilidad) */
        h1, h2, h3 {
            color: #0F172A !important; 
            font-weight: 800 !important;
        }

        /* Estilo de las tarjetas de resultados */
        .tarjeta-establecimiento {
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border-left: 8px solid #1E293B; 
            color: #1E293B !important;
        }

        /* Asegurar que todos los textos sean oscuros */
        .tarjeta-establecimiento p, .tarjeta-establecimiento strong {
            color: #334155 !important;
        }

        .titulo-centro {
            color: #0F172A; 
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 12px;
        }

        .badge {
            background-color: #F1F5F9; 
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 700;
            color: #0F172A !important;
            margin-right: 8px;
            border: 1px solid #CBD5E1;
            display: inline-block;
            margin-top: 5px;
        }

        /* Sección de Apoyo Yape en el Sidebar */
        .sidebar-yape {
            background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: white !important;
            margin-top: 20px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .sidebar-yape h3 {
            color: white !important;
            margin-top: 0;
            font-size: 1.2rem;
        }
        .sidebar-yape p {
            font-size: 14px;
            line-height: 1.4;
            margin-bottom: 0;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Buscador de Plazas SERUMS 2026-I")
st.markdown("Busca y filtra las plazas disponibles con total claridad. Los datos incluyen coordenadas exactas.")

# 3. Función para cargar datos
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel('Plazas_Ofertadas_con_Mapas.xlsx')
        return df.fillna("NO ESPECIFICA")
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel: {e}")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    # 4. Filtros en la barra lateral
    st.sidebar.header("🔍 Filtros de Búsqueda")

    profesion = st.sidebar.selectbox("1. Profesión", options=["Todos"] + sorted(list(df['PROFESIÓN'].unique())))
    institucion = st.sidebar.selectbox("2. Institución", options=["Todos"] + sorted(list(df['INSTITUCIÓN'].unique())))
    departamento = st.sidebar.selectbox("3. Departamento", options=["Todos"] + sorted(list(df['DEPARTAMENTO'].unique())))

    prov_opts = sorted(list(df[df['DEPARTAMENTO'] == departamento]['PROVINCIA'].unique())) if departamento != "Todos" else sorted(list(df['PROVINCIA'].unique()))
    provincia = st.sidebar.selectbox("4. Provincia", options=["Todos"] + prov_opts)

    dist_opts = sorted(list(df[df['PROVINCIA'] == provincia]['DISTRITO'].unique())) if provincia != "Todos" else sorted(list(df['DISTRITO'].unique()))
    distrito = st.sidebar.selectbox("5. Distrito", options=["Todos"] + dist_opts)

    categoria = st.sidebar.selectbox("6. Categoría", options=["Todos"] + sorted(list(df['CATEGORÍA'].unique())))
    zaf = st.sidebar.selectbox("7. Bono ZAF", options=["Todos", "SI", "NO"])
    ze = st.sidebar.selectbox("8. Bono ZE", options=["Todos", "SI", "NO"])

    # --- NUEVA UBICACIÓN DEL QR DE YAPE (SIEMPRE VISIBLE EN EL SIDEBAR) ---
    st.sidebar.markdown("---") # Línea divisoria visual
    st.sidebar.markdown("""
        <div class="sidebar-yape">
            <h3>💜 ¡Apoya el proyecto!</h3>
            <p>Si esta herramienta te ayudó a encontrar tu plaza, invítame un café.</p>
        </div>
    """, unsafe_allow_html=True)

    qr_path = "image_2c6c57.jpeg"
    if os.path.exists(qr_path):
        # Muestra la imagen directamente en el sidebar
        st.sidebar.image(qr_path, use_container_width=True)
    else:
        st.sidebar.info("Imagen del QR no detectada. Verifica el nombre en GitHub.")
    # ----------------------------------------------------------------------

    # 5. Filtrado
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

    # 6. Resultados
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
            <a href="{row['Link Google Maps']}" target="_blank" style="background-color:#0F172A; color:white; padding:12px 24px; text-decoration:none; border-radius:8px; font-weight:bold; display:inline-block; margin-top:10px;">
                🗺️ Ver ubicación exacta
            </a>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)

else:
    st.warning("No se pudo cargar la base de datos.")
