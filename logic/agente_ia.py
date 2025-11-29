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
        # --- MODO RESCATE (PRODUCTOS REALES DE LA CURACAO) ---
        print(f"⚠️ Usando respaldo retail. Error: {e}")
        
        # Extraemos el primer nombre para personalizar
        nombre = str(cliente['Nombre']).split()[0]
        
        # AQUÍ ESTÁ EL CAMBIO CLAVE:
        # Fíjate que ahora dice "Laptop Gamer", "iPhone", etc.
        # Si en tu código dice "Asesoría Personalizada", ¡CÁMBIALO POR ESTO!
        respuestas_backup = [
            {
                "segmento": "Gamer Entusiasta",
                "producto_sugerido": "Laptop Gamer",  # <--- ESTO ES LO QUE BUSCA EL BOTÓN
                "asunto": f"¡{nombre}, sube de nivel con esta oferta!",
                "mensaje": "Sabemos que te gusta la tecnología. Esta Laptop con tarjeta gráfica RTX es lo que necesitas."
            },
            {
                "segmento": "Tech Lover",
                "producto_sugerido": "iPhone 15",
                "asunto": "Tecnología de punta en tus manos",
                "mensaje": "Renueva tu equipo con lo último de Apple. Disponible ahora en tienda."
            },
            {
                "segmento": "Home Cinema",
                "producto_sugerido": "Smart TV 4K",
                "asunto": "Cine en casa para ti",
                "mensaje": "Disfruta de tus series favoritas con la mejor resolución del mercado."
            }
        ]
        
        return random.choice(respuestas_backup)