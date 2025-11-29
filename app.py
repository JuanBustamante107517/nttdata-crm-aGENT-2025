import streamlit as st
import pandas as pd
from logic.mock_social import obtener_redes_sociales
from logic.agente_ia import generar_campana_ia
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="CRM Agente IA - NTT DATA", page_icon="🤖", layout="centered")

# CSS personalizado
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🤖 NTT DATA: CRM Inteligente")
st.markdown("Generación de campañas autónomas mediante **GenAI** y **Señales Sociales**.")
st.markdown("---")

# 1. CARGAR DATOS
try:
    df = pd.read_csv("data/clientes.csv")
except:
    st.error("⚠️ Error: No se encontró el archivo 'data/clientes.csv'.")
    st.stop()

# 2. SELECTOR DE CLIENTE
col_sel, col_info = st.columns([1, 2])
with col_sel:
    st.subheader("👤 Cliente")
    cliente_seleccionado = st.selectbox("Seleccionar perfil:", df['Nombre'])
    cliente_data = df[df['Nombre'] == cliente_seleccionado].iloc[0]
    st.info(f"**ID:** {cliente_data['ID']}\n\n**Edad:** {cliente_data['Edad']}")

with col_info:
    st.subheader("📊 Datos del CRM")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Sector:**\n{cliente_data['Sector']}")
    with c2:
        st.markdown(f"**Historial:**\n{cliente_data['Historial_Compras']}")

# 3. EL AGENTE EN ACCIÓN
st.markdown("---")
st.subheader("🚀 Agente de Marketing Autónomo")

if st.button("GENERAR CAMPAÑA (ACTIVAR AGENTE)"):
    
    # 1. INGESTA
    social_info = obtener_redes_sociales(cliente_data['ID'])
    
    # LOOP VISUAL
    with st.status("🧠 El Agente está razonando...", expanded=True) as status:
        st.write("✅ Paso 1: Ingesta de datos CRM completada.")
        time.sleep(0.5)
        st.write(f"✅ Paso 2: Análisis de Huella Digital ({social_info['red']}).")
        st.json(social_info, expanded=False)
        time.sleep(0.5)
        st.write("🔄 Paso 3: Cruzando historial con productos de retail...")
        time.sleep(0.8)
        
        # 2. LLAMADA AL CEREBRO
        resultado = generar_campana_ia(cliente_data, social_info)
        
        status.update(label="✅ ¡Estrategia definida!", state="complete", expanded=False)

        # 3. RESULTADOS FINALES
        st.divider()
        st.subheader(f"📢 Campaña: {resultado.get('asunto', 'Sin Asunto')}")
        
        col_res1, col_res2 = st.columns([1, 2])
        with col_res1:
            st.success(f"**Segmento:**\n{resultado.get('segmento', 'N/A')}")
            st.info(f"**Producto:**\n{resultado.get('producto_sugerido', 'N/A')}")
        
        with col_res2:
            tab1, tab2 = st.tabs(["📧 Vista Previa (HTML)", "⚙️ JSON"])
            
            with tab1:
                # --- LINK INTELIGENTE LA CURACAO ---
                producto_ia = resultado.get('producto_sugerido', 'Tecnología')
                busqueda_url = producto_ia.replace(" ", "+")
                link_tienda = f"https://www.lacuracao.pe/catalogsearch/result/?q={busqueda_url}"

                email_html = f"""
                <div style="font-family: Arial, sans-serif; border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
                    <h3 style="color: #2c3e50;">{resultado.get('asunto', '...')}</h3>
                    <hr style="border: 0; border-top: 1px solid #ccc;">
                    <p style="font-size: 16px; color: #555;">
                        {resultado.get('mensaje', '...').replace(chr(10), '<br>')}
                    </p>
                    <div style="text-align: center; margin-top: 25px;">
                        <a href="{link_tienda}" target="_blank" style="background-color: #ffcc00; color: #000; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; border: 1px solid #e6b800;">
                            Ver Ofertas de {producto_ia} 🛒
                        </a>
                    </div>
                    <p style="font-size: 12px; color: #999; text-align: center; margin-top: 20px;">
                        Enviado automáticamente por NTT DATA GenAI Agent
                    </p>
                </div>
                """
                st.markdown(email_html, unsafe_allow_html=True)
                st.caption(f"📍 Link generado: {link_tienda}")
            
            with tab2:
                st.json(resultado)