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

    profesion = st.sidebar
