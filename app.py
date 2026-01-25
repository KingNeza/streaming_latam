import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Reg-Track LatAm", layout="wide")

# --- ESTÉTICA "THE PUDDING" (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Lora:ital,wght@0,700;1,400&display=swap');

    /* General */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #2c3e50;
    }

    h1, h2, h3 {
        font-family: 'Lora', serif !important;
        font-weight: 700;
        color: #1a1a1a;
    }

    /* Estilo de Tarjetas de Métricas */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-top: 3px solid #000;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* Sidebar */
    .stSidebar {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }

    /* Botones y Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (CONTROLES DINÁMICOS) ---
with st.sidebar:
    st.markdown("## ⚙️ Ajustes de Ponderación")
    st.write("Modifica la importancia de cada factor en el Índice de Rigidez Digital (IRD).")
    
    w_tax = st.slider("Importancia de Impuestos", 0.0, 1.0, 0.4)
    w_content = st.slider("Importancia de Cuota Contenido", 0.0, 1.0, 0.3)
    w_punitive = st.slider("Importancia de Poder Punitivo", 0.0, 1.0, 0.3)
    
    st.divider()
    st.markdown("### Filtros")
    paises_sel = st.multiselect("Países a comparar", ["México", "Colombia", "Argentina"], default=["México", "Colombia", "Argentina"])

# --- DATASET ---
raw_data = {
    "País": ["México", "Colombia", "Argentina"],
    "Impuestos (%)": [16, 19, 21],
    "Cuota Contenido (%)": [30, 15, 10],
    "Poder Punitivo (1-10)": [9, 4, 6],
    "Facilidad Operativa (1-10)": [4, 8, 5]
}

df = pd.DataFrame(raw_data)
df = df[df['País'].isin(paises_sel)]

# Cálculo dinámico basado en la Sidebar
df['IRD Index'] = (
    (df['Impuestos (%)'] * w_tax) + 
    (df['Cuota Contenido (%)'] * w_content) + 
    (df['Poder Punitivo (1-10)'] * 3 * w_punitive) # Factor 3 para normalizar el impacto
).round(2)

# --- HEADER ---
st.title("The Digital Borderline")
st.markdown("""
*Un análisis sobre la soberanía digital y las barreras de entrada para plataformas de streaming en América Latina.* **Contexto Actualizado: 2026**
""")
st.divider()

# --- KPI METRICS ---
cols = st.columns(len(df))
for i, row in enumerate(df.itertuples()):
    with cols[i]:
        st.metric(label=f"Índice IRD {row.País}", value=row[6])

# --- VISUALIZACIONES PRINCIPALES ---
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
    st.markdown("### El Perfil del Riesgo")
    categories = ['Impuestos (%)', 'Cuota Contenido (%)', 'Poder Punitivo (1-10)', 'Facilidad Operativa (1-10)']
    
    fig_radar = go.Figure()
    for i in range(len(df)):
        fig_radar.add_trace(go.Scatterpolar(
            r=[df.iloc[i][c] for c in categories],
            theta=categories,
            fill='toself',
            name=df.iloc[i]['País'],
            line=dict(width=2)
        ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 35], gridcolor="#e0e0e0"),
            bgcolor="white"
        ),
        font=dict(family="Inter", size=12),
        margin=dict(t=40, b=40, l=40, r=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.markdown("### Resumen Normativo")
    for i, row in df.iterrows():
        with st.expander(f"Lectura técnica: {row['País']}"):
            if row['País'] == "México":
                st.write("**⚠️ Alerta SAT:** El Art. 30-B permite la desconexión digital inmediata por incumplimiento fiscal.")
            elif row['País'] == "Colombia":
                st.write("**🎬 Incentivo:** Reembolsos de hasta el 40% a través de FFC (Fondo Fílmico Colombia).")
            else:
                st.write("**💸 Presión:** La suma de IVA + Impuesto PAIS + Tasas INCAA la convierte en la región más cara de operar.")

# --- SECCIÓN REFERENCIAS ---
st.divider()
st.markdown("### 📚 Actores Clave y Fuentes")
tab_ref = st.tabs(["Estructura Legal", "Entidades de Control"])

with tab_ref[0]:
    st.table(df[['País', 'Impuestos (%)', 'Cuota Contenido (%)', 'IRD Index']])

with tab_ref[1]:
    st.markdown("""
    - **México:** Agencia de Transformación Digital (Nueva 2026), SAT.
    - **Colombia:** Comisión de Regulación de Comunicaciones (CRC), MinTIC.
    - **Argentina:** ENACOM, AFIP, INCAA.
    """)

st.caption("Tipografía: Lora & Inter via Google Fonts. Diseño inspirado en The Pudding (2026).")