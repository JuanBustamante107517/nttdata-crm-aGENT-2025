import streamlit as st
import pandas as pd
from logic.mock_social import obtener_redes_sociales
from logic.agente_ia import generar_campana_ia
import time # Importamos esto para simular el tiempo de "pensado"

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="CRM Agente IA - NTT DATA", page_icon="🤖", layout="centered")

# CSS personalizado para que se vea más profesional (Hackathon style)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        padding: 10px;
    }
    .metric-container {
        border: 1px solid #e6e6e6;
        padding: 10px;
        border-radius: 5px;
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

# 2. SELECTOR DE CLIENTE (SIDEBAR O MAIN)
col_sel, col_info = st.columns([1, 2])

with col_sel:
    st.subheader("👤 Cliente")
    cliente_seleccionado = st.selectbox("Seleccionar perfil:", df['Nombre'])
    
    # Obtener datos del cliente
    cliente_data = df[df['Nombre'] == cliente_seleccionado].iloc[0]
    
    # Mostrar ficha rápida
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
    
    # AQUI ESTA LA PARTE NUEVA QUE IMPRESIONA A LOS JUECES
    # Usamos un contenedor vacío para reportar el estatus en tiempo real
    
    # 1. INGESTA Y ENRIQUECIMIENTO
    social_info = obtener_redes_sociales(cliente_data['ID'])
    
    # Mostramos el "Loop de Decisiones" visualmente
    with st.status("🧠 El Agente está razonando...", expanded=True) as status:
        st.write("✅ Paso 1: Ingesta de datos CRM completada.")
        time.sleep(0.5) # Simulación visual
        st.write(f"✅ Paso 2: Análisis de Huella Digital ({social_info['red']}).")
        st.json(social_info, expanded=False)
        time.sleep(0.5)
        st.write("🔄 Paso 3: Cruzando historial de compras con intereses detectados...")
        time.sleep(0.8)
        
        # 2. LLAMADA A LA IA (EL CEREBRO)
        resultado = generar_campana_ia(cliente_data, social_info)
        
        if "error" in resultado:
            status.update(label="❌ Error en el proceso", state="error")
            st.error(resultado["error"])
            st.error("💡 REVISA TU API KEY EN EL ARCHIVO .ENV")
        else:
            status.update(label="✅ ¡Estrategia definida exitosamente!", state="complete", expanded=False)

            # 3. RESULTADOS FINALES (VISUALIZACIÓN)
            st.divider()
            st.subheader(f"📢 Campaña: {resultado.get('asunto', 'Sin Asunto')}")
            
            # Métricas clave
            col_res1, col_res2 = st.columns([1, 2])
            with col_res1:
                st.success(f"**Segmento:**\n{resultado.get('segmento', 'N/A')}")
                st.info(f"**Producto Sugerido:**\n{resultado.get('producto_sugerido', 'N/A')}")
            
            with col_res2:
                # Pestañas para ver Email renderizado vs JSON puro
                tab1, tab2 = st.tabs(["📧 Vista Previa (HTML)", "⚙️ Datos JSON (Backend)"])
                
                with tab1:
                    email_html = f"""
                    <div style="font-family: Arial, sans-serif; border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
                        <h3 style="color: #2c3e50;">{resultado.get('asunto', '...')}</h3>
                        <hr style="border: 0; border-top: 1px solid #ccc;">
                        <p style="font-size: 16px; color: #555; line-height: 1.5;">
                            {resultado.get('mensaje', '...').replace(chr(10), '<br>')}
                        </p>
                        <div style="text-align: center; margin-top: 25px;">
                            <a href="#" style="background-color: #007bff; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                                Ver Oferta Exclusiva
                            </a>
                        </div>
                        <p style="font-size: 12px; color: #999; text-align: center; margin-top: 20px;">
                            Enviado automáticamente por NTT DATA GenAI Agent
                        </p>
                    </div>
                    """
                    st.markdown(email_html, unsafe_allow_html=True)
                
                with tab2:
                    st.json(resultado)