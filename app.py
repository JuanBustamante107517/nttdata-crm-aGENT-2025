"""
CRM INTELIGENTE - NTT DATA HACKATHON GENAI 2025
Aplicación Web: Agente Autónomo para Campañas de Marketing
"""
import streamlit as st
import pandas as pd

import json
from datetime import datetime
import sys
import os

from dotenv import load_dotenv
load_dotenv()


# Configurar path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.data_loader import DataLoader
from logic.agente_orchestrator import AgenteOrchestrator
from logic.output_generator import OutputGenerator

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="CRM Inteligente - NTT DATA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS PERSONALIZADOS ====================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .log-container {
        background: #212529;
        color: #00ff00;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🤖 CRM INTELIGENTE</h1>
    <h3>Agente Autónomo de Marketing con IA</h3>
    <p>NTT DATA - GenAI Hackathon 2025</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR - CONFIGURACIÓN ====================
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/artificial-intelligence.png", width=100)
    st.title("⚙️ Configuración")
    
    st.markdown("---")
    st.subheader("🤖 Modo del Agente")
    
    # Toggle para GenAI
    usar_genai = st.checkbox(
        "🧠 Usar GenAI (Experimental)",
        value=False,
        help="Mejora mensajes con GPT-3.5. Requiere OPENAI_API_KEY en .env"
    )
    
    if usar_genai:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            st.success("✅ API Key detectada")
        else:
            st.warning("⚠️ No se encontró OPENAI_API_KEY. Se usará modo determinístico.")
            st.info("Para habilitar GenAI:\n1. Crea archivo `.env`\n2. Agrega: `OPENAI_API_KEY=sk-...`")
    else:
        st.info("Modo determinístico: Usa templates y reglas de negocio")
    
    st.markdown("---")
    st.subheader("📊 Acerca del Sistema")
    st.info("""
    **Flujo del Agente:**
    1. 🔍 INGESTA - Cargar datos
    2. 👤 PERFIL - Consultar redes sociales
    3. 🎯 SEGMENTO - Clasificar cliente
    4. 📧 CAMPAÑA - Generar mensaje
    5. 💾 SALIDA - Exportar resultados
    """)
    
    st.markdown("---")
    st.subheader("📈 Estadísticas")
    
    # Cargar datos para stats
    try:
        loader = DataLoader()
        df = loader.cargar_clientes()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Clientes", len(df))
        with col2:
            st.metric("Sectores", df['Sector'].nunique())
        
        # Distribución por riesgo
        st.markdown("**Distribución por Riesgo:**")
        riesgo_counts = df['Riesgo_Abandono'].value_counts()
        for riesgo, count in riesgo_counts.items():
            st.write(f"- {riesgo}: {count}")
            
    except Exception as e:
        st.error(f"Error cargando stats: {e}")
    
    st.markdown("---")
    st.caption("🔒 Datos 100% simulados - Demo educativo")

# ==================== MAIN CONTENT ====================

# Inicializar session state
if 'resultados_historicos' not in st.session_state:
    st.session_state.resultados_historicos = []

# ==================== SECCIÓN 1: SELECCIÓN DE CLIENTE ====================
st.header("1️⃣ Selección de Cliente")

try:
    loader = DataLoader()
    df_clientes = loader.cargar_clientes()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Modo de selección
        modo = st.radio(
            "Modo de ejecución:",
            ["🎯 Cliente Individual", "📦 Procesamiento Batch (Todos)"],
            horizontal=True
        )
        
        if modo == "🎯 Cliente Individual":
            cliente_seleccionado = st.selectbox(
                "Selecciona un cliente:",
                df_clientes['Nombre'].tolist(),
                index=0
            )
            clientes_a_procesar = [cliente_seleccionado]
        else:
            st.info(f"Se procesarán {len(df_clientes)} clientes automáticamente")
            clientes_a_procesar = df_clientes['Nombre'].tolist()
    
    with col2:
        st.markdown("### 📋 Preview")
        if modo == "🎯 Cliente Individual":
            cliente_data = df_clientes[df_clientes['Nombre'] == cliente_seleccionado].iloc[0]
            st.write(f"**ID:** {cliente_data['ID']}")
            st.write(f"**Sector:** {cliente_data['Sector']}")
            st.write(f"**Gasto:** ${cliente_data['Gasto_Promedio']:,.0f}")
            st.write(f"**Riesgo:** {cliente_data['Riesgo_Abandono']}")
        else:
            st.write(f"**Total:** {len(clientes_a_procesar)}")
            st.write(f"**Sectores:** {df_clientes['Sector'].nunique()}")
    
except Exception as e:
    st.error(f"❌ Error cargando datos: {e}")
    st.stop()

st.markdown("---")

# ==================== SECCIÓN 2: EJECUCIÓN DEL AGENTE ====================
st.header("2️⃣ Ejecutar Agente Inteligente")

col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])

with col_btn1:
    ejecutar = st.button("🚀 ACTIVAR AGENTE", use_container_width=True)

with col_btn2:
    if st.button("🗑️ Limpiar Historial", use_container_width=True):
        st.session_state.resultados_historicos = []
        st.rerun()

with col_btn3:
    if st.button("📊 Ver Historial", use_container_width=True):
        if st.session_state.resultados_historicos:
            st.session_state.mostrar_historial = True
        else:
            st.warning("No hay historial disponible")

# ==================== EJECUCIÓN ====================
if ejecutar:
    output_gen = OutputGenerator()
    resultados_batch = []
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, cliente_nombre in enumerate(clientes_a_procesar):
        # Actualizar progress
        progreso = (idx + 1) / len(clientes_a_procesar)
        progress_bar.progress(progreso)
        status_text.text(f"Procesando {idx + 1}/{len(clientes_a_procesar)}: {cliente_nombre}")
        
        # Contenedor para este cliente
        with st.expander(f"📍 Cliente: {cliente_nombre}", expanded=(len(clientes_a_procesar) == 1)):
            
            # Ejecutar agente
            agente = AgenteOrchestrator(usar_genai=usar_genai)
            
            with st.spinner("🤖 El agente está trabajando..."):
                resultado_ejecucion = agente.ejecutar_pipeline(cliente_nombre)
            
            if resultado_ejecucion['exito']:
                resultado = resultado_ejecucion['resultado']
                
                # Agregar a historial
                st.session_state.resultados_historicos.append(resultado)
                resultados_batch.append(resultado)
                
                st.success(f"✅ Campaña generada para {cliente_nombre}")
                
                # Tabs para organizar info
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumen", "📧 Campaña", "📝 Log", "💾 Exportar"])
                
                with tab1:
                    # Métricas principales
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Segmento", 
                            resultado['segmentacion']['segmento'].replace('_', ' ')
                        )
                    with col2:
                        st.metric(
                            "Confianza", 
                            f"{resultado['segmentacion']['confianza']*100:.0f}%"
                        )
                    with col3:
                        st.metric(
                            "Score Social", 
                            f"{resultado['segmentacion']['score_social']:.1f}/10"
                        )
                    with col4:
                        st.metric(
                            "Canal", 
                            resultado['campana']['canal']
                        )
                    
                    # Razones de segmentación
                    st.markdown("**🎯 Razones de Segmentación:**")
                    for razon in resultado['segmentacion']['razones']:
                        st.write(f"- {razon}")
                    
                    # Métricas esperadas
                    st.markdown("**📈 Métricas Esperadas:**")
                    col1, col2, col3 = st.columns(3)
                    metricas = resultado['campana']['metricas_esperadas']
                    with col1:
                        st.info(f"**Open Rate:** {metricas['open_rate_esperado']}")
                    with col2:
                        st.info(f"**CTR:** {metricas['ctr_esperado']}")
                    with col3:
                        st.info(f"**Conversión:** {metricas['conversion_esperada']}")
                
                with tab2:
                    # Preview de la campaña
                    st.subheader(f"📧 {resultado['campana']['nombre']}")
                    
                    # Indicador de IA
                    if resultado['campana'].get('mejorado_con_ia', False):
                        st.success("🤖 Mensaje mejorado con IA Generativa")
                        if 'asunto_original' in resultado['campana']:
                            with st.expander("Ver comparación de asuntos"):
                                st.write("**Original:**", resultado['campana']['asunto_original'])
                                st.write("**Mejorado con IA:**", resultado['campana']['asunto'])
                    else:
                        st.info("📝 Mensaje generado con templates determinísticos")
                    
                    st.markdown(f"**Asunto:** {resultado['campana']['asunto']}")
                    
                    st.markdown("---")
                    
                    st.markdown("**Mensaje:**")
                    st.text_area(
                        "Preview",
                        value=resultado['campana']['mensaje'],
                        height=300,
                        disabled=True
                    )
                    
                    # Comparación si hay versión original
                    if resultado['campana'].get('mensaje_original'):
                        with st.expander("🔍 Ver mensaje original vs mejorado"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Original (Template):**")
                                st.text(resultado['campana']['mensaje_original'][:200] + "...")
                            with col2:
                                st.markdown("**Mejorado (IA):**")
                                st.text(resultado['campana']['mensaje'][:200] + "...")
                    
                    st.markdown(f"**CTA:** `{resultado['campana']['cta']}`")
                    
                    # Manejar descuento (puede venir como 'descuento' o 'descuento_aplicado')
                    descuento = resultado['campana'].get('descuento_aplicado', 
                                                          resultado['campana'].get('descuento', 0))
                    if descuento > 0:
                        st.success(f"🎁 Descuento aplicado: {descuento*100:.0f}%")
                
                with tab3:
                    # Log de ejecución
                    st.markdown("**Log del Agente:**")
                    log_text = agente.obtener_log_legible()
                    st.code(log_text, language='log')
                
                with tab4:
                    # Botones de exportación
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # JSON
                        json_str = json.dumps(resultado, indent=2, ensure_ascii=False)
                        st.download_button(
                            label="📥 Descargar JSON",
                            data=json_str,
                            file_name=f"campana_{cliente_nombre.replace(' ', '_')}.json",
                            mime="application/json"
                        )
                    
                    with col2:
                        # HTML
                        html_path = output_gen.generar_html(resultado)
                        with open(html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        st.download_button(
                            label="📥 Descargar HTML",
                            data=html_content,
                            file_name=f"campana_{cliente_nombre.replace(' ', '_')}.html",
                            mime="text/html"
                        )
                    
                    st.info(f"✅ Archivos guardados en carpeta 'output/'")
            
            else:
                st.error(f"❌ Error procesando {cliente_nombre}: {resultado_ejecucion['error']}")
    
    # Si fue batch, generar CSV consolidado
    if len(resultados_batch) > 1:
        st.markdown("---")
        st.subheader("📊 Reporte Consolidado (Batch)")
        
        csv_path = output_gen.generar_csv(resultados_batch)
        
        # Mostrar tabla resumen
        df_resumen = pd.DataFrame([
            {
                'Cliente': r['cliente']['nombre'],
                'Segmento': r['segmentacion']['segmento'],
                'Confianza': f"{r['segmentacion']['confianza']:.2f}",
                'Campaña': r['campana']['nombre'],
                'Canal': r['campana']['canal'],
                'Descuento': f"{r['campana']['descuento']*100:.0f}%"
            }
            for r in resultados_batch
        ])
        
        st.dataframe(df_resumen, use_container_width=True)
        
        # Descargar CSV
        with open(csv_path, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        
        st.download_button(
            label="📥 Descargar CSV Consolidado",
            data=csv_content,
            file_name="resultados_batch.csv",
            mime="text/csv"
        )
    
    progress_bar.empty()
    status_text.empty()
    st.balloons()

# ==================== SECCIÓN 3: HISTORIAL ====================
if st.session_state.resultados_historicos and st.session_state.get('mostrar_historial', False):
    st.markdown("---")
    st.header("📚 Historial de Ejecuciones")
    
    for idx, resultado in enumerate(reversed(st.session_state.resultados_historicos[-10:])):  # Últimos 10
        with st.expander(
            f"🕐 {resultado['metadata']['timestamp']} - {resultado['cliente']['nombre']}"
        ):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Segmento:** {resultado['segmentacion']['segmento']}")
            with col2:
                st.write(f"**Campaña:** {resultado['campana']['nombre']}")
            with col3:
                st.write(f"**Canal:** {resultado['campana']['canal']}")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 2rem;'>
    <p><strong>🤖 CRM Inteligente - Agente Autónomo</strong></p>
    <p>NTT DATA GenAI Hackathon 2025</p>
    <p style='font-size: 0.85em;'>
        Datos 100% simulados • Sin scraping real • Demo educativo<br>
        Arquitectura FSM: INGESTA → PERFIL → SEGMENTO → CAMPAÑA → SALIDA
    </p>
</div>
""", unsafe_allow_html=True)
=======
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
