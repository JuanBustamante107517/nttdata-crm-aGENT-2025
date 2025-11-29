import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

# Configurar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generar_campana_ia(cliente, info_social):
    """
    Función que actúa como el Agente Inteligente.
    Toma datos del CSV y datos Mock de redes, y genera una campaña.
    """
    
    # 1. El Prompt (Instrucciones al Agente)
    prompt = f"""
    Eres un experto en Marketing Digital. Genera una campaña de ventas personalizada.
    
    PERFIL DEL CLIENTE (CRM):
    - Nombre: {cliente['Nombre']}
    - Edad: {cliente['Edad']}
    - Sector: {cliente['Sector']}
    - Historial: {cliente['Historial_Compras']}
    
    HUELLA DIGITAL (REDES SOCIALES):
    - Red Favorita: {info_social['red']}
    - Intereses Detectados: {", ".join(info_social['intereses'])}
    - Última Actividad: "{info_social['ultimo_post']}"
    
    TAREA:
    1. Analiza el perfil y decide qué producto venderle.
    2. Redacta un asunto de correo atractivo (máx 50 caracteres).
    3. Escribe el cuerpo del mensaje (corto y persuasivo).
    
    SALIDA (FORMATO JSON ÚNICAMENTE):
    {{
        "segmento": "Ej: Early Adopter",
        "producto_sugerido": "...",
        "asunto": "...",
        "mensaje": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # O gpt-4 si tienes acceso
            messages=[
                {"role": "system", "content": "Responde siempre en formato JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "error": f"Error del Agente: {str(e)}",
            "segmento": "Error",
            "producto_sugerido": "N/A",
            "asunto": "Error",
            "mensaje": "No se pudo conectar con la IA."
        }