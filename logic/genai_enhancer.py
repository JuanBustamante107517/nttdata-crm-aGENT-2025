"""
Módulo OPCIONAL: GenAI Enhancer
Mejora las campañas usando IA generativa si hay API key disponible
"""
import os
from typing import Dict, Optional


class GenAIEnhancer:
    """
    Mejora campañas con GenAI si está disponible.
    Si no hay API key, usa fallback a templates.
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.disponible = self.api_key is not None
        
        if self.disponible:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                self.disponible = False
                print("⚠️ OpenAI no instalado. Usando modo determinístico.")
    
    def mejorar_mensaje(
        self, 
        mensaje_base: str,
        cliente: Dict,
        perfil_social: Dict,
        segmento: str
    ) -> Dict:
        """
        Intenta mejorar el mensaje con GenAI.
        Si falla, retorna el mensaje base.
        """
        if not self.disponible:
            return {
                "mensaje": mensaje_base,
                "mejorado_con_ia": False,
                "metodo": "template"
            }
        
        try:
            # Prompt embebido (como requiere el hackathon)
            prompt = f"""
Eres un experto en marketing B2C/B2B. Mejora este mensaje de campaña haciéndolo más persuasivo y personalizado.

CONTEXTO DEL CLIENTE:
- Nombre: {cliente['Nombre']}
- Sector: {cliente['Sector']}
- Segmento: {segmento}
- Intereses en redes: {', '.join(perfil_social.get('intereses', [])[:3])}
- Tono detectado: {perfil_social.get('tono', 'neutral')}

MENSAJE BASE:
{mensaje_base}

INSTRUCCIONES:
1. Mantén la estructura general pero mejora el copywriting
2. Usa el tono detectado del cliente
3. Incluye referencias sutiles a sus intereses
4. Máximo 200 palabras
5. Mantén saltos de línea para legibilidad

MENSAJE MEJORADO:
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5",
                messages=[
                    {"role": "system", "content": "Eres un copywriter experto en marketing digital."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            mensaje_mejorado = response.choices[0].message.content.strip()
            
            return {
                "mensaje": mensaje_mejorado,
                "mejorado_con_ia": True,
                "metodo": "gpt-3.5",
                "mensaje_original": mensaje_base
            }
            
        except Exception as e:
            print(f"⚠️ Error en GenAI (usando fallback): {e}")
            return {
                "mensaje": mensaje_base,
                "mejorado_con_ia": False,
                "metodo": "template_fallback",
                "error": str(e)
            }
    
    def generar_asunto_alternativo(
        self,
        asunto_base: str,
        cliente: Dict
    ) -> Optional[str]:
        """
        Genera un asunto más atractivo con IA
        """
        if not self.disponible:
            return None
        
        try:
            prompt = f"""
Mejora este asunto de email para {cliente['Nombre']} del sector {cliente['Sector']}:

"{asunto_base}"

Reglas:
- Máximo 50 caracteres
- Incluir emoji relevante
- Hacerlo más urgente/atractivo
- Solo devuelve el asunto, nada más

Asunto mejorado:
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=30
            )
            
            return response.choices[0].message.content.strip().strip('"')
            
        except:
            return None
