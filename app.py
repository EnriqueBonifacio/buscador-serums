import streamlit as st
import pandas as pd
import os

# 1. Configuración de página
st.set_page_config(
    page_title="Buscador SERUMS 2026-I", 
    layout="wide", 
    page_icon="🏥"
)

# 2. Estilos de Alto Contraste y Mejor Legibilidad
st.markdown("""
    <style>
        .stApp { background-color: #F8FAFC; }
        
        h1, h2, h3 { color: #0F172A !important; font-weight: 800 !important; }

        .tarjeta-establecimiento {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 15px;
            border-left: 8px solid #1E293B;
            color: #1E293B !important;
        }

        .titulo-centro {
            color: #0F172A; 
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 8px;
        }

        .badge {
            background-color: #F1F5F9; 
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            color: #0F172A !important;
            border: 1px solid #CBD5E1;
            display: inline-block;
            margin-right: 5px;
            margin-top: 5px;
        }

        /* Sidebar Yape - Muy visible */
        .sidebar-yape {
            background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            color: white !important;
            margin-bottom: 10px;
        }
        
        /* Bottom Yape - Llamativo */
        .bottom-yape {
            background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            color: white !important;
            margin-top: 40px;
            margin-bottom: 20px;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        .bottom-yape h2 { color: white !important; margin-bottom: 10px; }

        .stButton>button {
            width: 100%;
            background-color: #0F172A;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Buscador de Plazas SERUMS 2026-I")
st.markdown("Filtra entre las plazas disponibles. **Puedes escribir dentro de los filtros para buscar más rápido.**")

# 3. Carga de datos con Caché
@st.cache_data
def cargar_datos_optimizados():
    try:
        df = pd.read_excel('Plazas_Ofertadas_con_Mapas.xlsx')
        return df.fillna("NO ESPECIFICA")
    except:
        return pd.DataFrame()

df = cargar_datos_optimizados()

if not df.empty:
    # 4. Sidebar: Filtros interactivos
    st.sidebar.header("🔍 Filtros")

    profesion = st.sidebar.selectbox("1. Profesión", options=["Todos"] + sorted(df['PROFESIÓN'].unique().tolist()))
    institucion = st.sidebar.selectbox("2. Institución", options=["Todos"] + sorted(df['INSTITUCIÓN'].unique().tolist()))
    departamento = st.sidebar.selectbox("3. Departamento", options=["Todos"] + sorted(df['DEPARTAMENTO'].unique().tolist()))

    if departamento != "Todos":
        provincias = sorted(df[df['DEPARTAMENTO'] == departamento]['PROVINCIA'].unique().tolist())
    else:
        provincias = sorted(df['PROVINCIA'].unique().tolist())
    provincia = st.sidebar.selectbox("4. Provincia", options=["Todos"] + provincias)

    if provincia != "Todos":
        distritos = sorted(df[df['PROVINCIA'] == provincia]['DISTRITO'].unique().tolist())
    else:
        distritos = sorted(df['DISTRITO'].unique().tolist())
    distrito = st.sidebar.selectbox("5. Distrito", options=["Todos"] + distritos)

    # NUEVO FILTRO: Grado de Dificultad
    dificultad_opciones = sorted(df['GRADO DE DIFICULTAD'].unique().tolist()) if 'GRADO DE DIFICULTAD' in df.columns else []
    dificultad = st.sidebar.selectbox("6. Grado de Dificultad", options=["Todos"] + dificultad_opciones)

    categoria = st.sidebar.selectbox("7. Categoría", options=["Todos"] + sorted(df['CATEGORÍA'].unique().tolist()))
    zaf = st.sidebar.selectbox("8. Bono ZAF", options=["Todos", "SI", "NO"])
    ze = st.sidebar.selectbox("9. Bono ZE", options=["Todos", "SI", "NO"])

    # Apoyo Yape en el Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-yape"><h3>💜 ¡Apoya el proyecto!</h3><p>Escanea para seguir mejorando</p></div>', unsafe_allow_html=True)
    
    qr_path = "image_2c6c57.jpeg"
    if os.path.exists(qr_path):
        st.sidebar.image(qr_path, use_container_width=True)

    # 5. Lógica de Filtrado
    mask = pd.Series([True] * len(df))
    if profesion != "Todos": mask &= (df['PROFESIÓN'] == profesion)
    if institucion != "Todos": mask &= (df['INSTITUCIÓN'] == institucion)
    if departamento != "Todos": mask &= (df['DEPARTAMENTO'] == departamento)
    if provincia != "Todos": mask &= (df['PROVINCIA'] == provincia)
    if distrito != "Todos": mask &= (df['DISTRITO'] == distrito)
    if dificultad != "Todos": mask &= (df['GRADO DE DIFICULTAD'] == dificultad)
    if categoria != "Todos": mask &= (df['CATEGORÍA'] == categoria)
    if zaf != "Todos": mask &= (df['ZAF (*)'] == zaf)
    if ze != "Todos": mask &= (df['ZE (**)'] == ze)
    
    df_filtrado = df[mask]

    st.subheader(f"📍 {len(df_filtrado)} plazas encontradas")

    # 6. Motor de Fluidez (Paginación)
    estado_filtros_actual = f"{profesion}{institucion}{departamento}{provincia}{distrito}{dificultad}{categoria}{zaf}{ze}"
    
    if 'estado_filtros' not in st.session_state or st.session_state.estado_filtros != estado_filtros_actual:
        st.session_state.estado_filtros = estado_filtros_actual
        st.session_state.items_mostrar = 50 

    df_display = df_filtrado.head(st.session_state.items_mostrar)

    for _, row in df_display.iterrows():
        val_dificultad = row.get('GRADO DE DIFICULTAD', 'N/A')
        html_card = f"""
        <div class="tarjeta-establecimiento">
            <div class="titulo-centro">🏥 {row['NOMBRE DE ESTABLECIMIENTO']}</div>
            <p><strong>Ubicación:</strong> {row['DEPARTAMENTO']} > {row['PROVINCIA']} > {row['DISTRITO']}</p>
            <p><strong>Detalles:</strong> {row['INSTITUCIÓN']} | Cat: {row['CATEGORÍA']}</p>
            <div>
                <span class="badge">👥 Plazas: {row.get('N° PLAZAS', 1)}</span>
                <span class="badge">📊 Dificultad: {val_dificultad}</span>
                <span class="badge">💰 ZAF: {row['ZAF (*)']}</span>
                <span class="badge">🔥 ZE: {row['ZE (**)']}</span>
            </div>
            <br>
            <a href="{row['Link Google Maps']}" target="_blank" style="background-color:#0F172A; color:white; padding:8px 16px; text-decoration:none; border-radius:6px; font-weight:bold; display:inline-block; margin-top:8px;">
                🗺️ Ver en Google Maps
            </a>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)

    if len(df_filtrado) > st.session_state.items_mostrar:
        if st.button(f"Ver más resultados (Mostrando {st.session_state.items_mostrar} de {len(df_filtrado)})"):
            st.session_state.items_mostrar += 50
            st.rerun()

    # APOYO YAPE AL FINAL
    st.markdown("---")
    st.markdown("""
        <div class="bottom-yape">
            <h2>💜 ¿Te sirvió el buscador?</h2>
            <p style="font-size: 18px;">Si esta herramienta te ahorró estrés, apóyanos escaneando el QR para mantener el proyecto activo.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if os.path.exists(qr_path):
            st.image(qr_path, caption="¡Muchas gracias!", use_container_width=True)

else:
    st.warning("No se encontró el archivo de datos.")
