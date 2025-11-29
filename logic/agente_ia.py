import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import random

# Cargar variables
load_dotenv()

# --- TU LLAVE REAL ---
api_key = "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"

client = OpenAI(api_key=api_key)

def generar_campana_ia(cliente, info_social):
    """
    Agente usando GPT-3.5-Turbo.
    Incluye sistema de respaldo anti-caídas.
    """
    
    # 1. El Prompt
    prompt = f"""
    Eres un Agente Experto en Marketing.
    CLIENTE: {cliente['Nombre']}, Sector: {cliente['Sector']}
    INTERESES: {", ".join(info_social['intereses'])}
    
    TAREA: Generar campaña de venta en JSON.
    
    FORMATO JSON ESPERADO:
    {{
        "segmento": "...",
        "producto_sugerido": "...",
        "asunto": "...",
        "mensaje": "..."
    }}
    """

    try:
        # --- INTENTO DE CONEXIÓN REAL ---
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Responde solo en JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Limpieza y retorno
        contenido = response.choices[0].message.content
        if "```json" in contenido:
            contenido = contenido.replace("```json", "").replace("```", "")
        return json.loads(contenido)

    except Exception as e:
        # --- MODO RESCATE (SI FALLA) ---
        print(f"⚠️ Alerta: Usando respuesta de respaldo. Error: {e}")
        
        nombre_cliente = cliente['Nombre']
        sector_cliente = cliente['Sector']
        
        # Generamos una respuesta simulada segura
        respuestas_backup = [
            {
                "segmento": "Usuario Digital",
                "producto_sugerido": "Servicio Cloud Premium",
                "asunto": f"Oportunidad exclusiva para {nombre_cliente}",
                "mensaje": f"Tenemos una solución personalizada para el sector {sector_cliente} con un 20% de descuento."
            },
            {
                "segmento": "Cliente VIP",
                "producto_sugerido": "Asesoría Personalizada",
                "asunto": "Propuesta de valor única",
                "mensaje": "Basado en tu historial reciente, hemos seleccionado los mejores productos para optimizar tu negocio."
            }
        ]
        
        return random.choice(respuestas_backup)