import streamlit as st
import pandas as pd
from logic.mock_social import obtener_redes_sociales
from logic.agente_ia import generar_campana_ia

# Configuración de página
st.set_page_config(page_title="CRM Agente IA - NTT DATA", page_icon="🤖")

st.title("🤖 NTT DATA CRM: Agente Inteligente")
st.markdown("Generación automática de campañas basada en **Datos CRM** + **Huella Digital**.")

# 1. Cargar Datos
try:
    df = pd.read_csv("data/clientes.csv")
except:
    st.error("No se encontró data/clientes.csv")
    st.stop()

# 2. Selector de Cliente
cliente_seleccionado = st.selectbox("Selecciona un Cliente del CRM:", df['Nombre'])

# Obtener fila completa del cliente
cliente_data = df[df['Nombre'] == cliente_seleccionado].iloc[0]

# Mostrar ficha técnica
col1, col2 = st.columns(2)
with col1:
    st.info(f"**Sector:** {cliente_data['Sector']}")
with col2:
    st.info(f"**Historial:** {cliente_data['Historial_Compras']}")

# 3. Botón de Acción
if st.button("🚀 ACTIVAR AGENTE DE VENTAS"):
    with st.spinner("🕵️‍♂️ El Agente está investigando redes sociales y diseñando la campaña..."):
        
        # PASO A: Consultar Mock de Redes
        social_info = obtener_redes_sociales(cliente_data['ID'])
        st.success(f"Huella Digital encontrada en {social_info['red']}!")
        with st.expander("Ver datos ocultos de redes sociales"):
            st.json(social_info)
            
        # PASO B: Llamar a la IA
        resultado = generar_campana_ia(cliente_data, social_info)
        
        # 4. Mostrar Resultados
        st.divider()
        st.subheader(f"📢 Campaña Generada: {resultado.get('asunto', 'Error')}")
        
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.metric(label="Segmento", value=resultado.get('segmento', 'N/A'))
            st.write(f"**Producto:** {resultado.get('producto_sugerido', 'N/A')}")
            
        with c2:
            st.markdown("### 📧 Vista Previa del Correo")
            st.info(resultado.get('mensaje', 'Sin mensaje'))