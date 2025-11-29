"""
Módulo: Mock Social API
Responsabilidad: Simular señales de redes sociales sin scraping real
"""
import random
from typing import Dict, List


class MockSocialAPI:
    """
    API simulada que retorna señales sociales ficticias
    En producción, esto conectaría con Meta Graph API, Twitter API, etc.
    """
    
    # Base de datos ficticia de perfiles sociales
    MOCK_DATABASE = {
        1: {  # Carlos Ruiz - Tech Early Adopter
            "red_principal": "Twitter/X",
            "intereses": ["IA", "Startups", "Gaming", "Web3", "Gadgets"],
            "ultimo_post": "Increíble lo nuevo de Claude 4 #AIRevolution",
            "nivel_actividad": "Alto",
            "tono": "Técnico y entusiasta",
            "engagement_promedio": 8.5,
            "horario_activo": "20:00-23:00"
        },
        2: {  # Maria Gomez - Wellness
            "red_principal": "Instagram",
            "intereses": ["Yoga", "Nutrición", "Mindfulness", "Viajes"],
            "ultimo_post": "🧘‍♀️ Rutina matutina para empezar con energía",
            "nivel_actividad": "Medio",
            "tono": "Inspiracional y positivo",
            "engagement_promedio": 6.2,
            "horario_activo": "07:00-09:00"
        },
        3: {  # Empresa Tech SAC - B2B
            "red_principal": "LinkedIn",
            "intereses": ["Cloud Computing", "Ciberseguridad", "DevOps", "Automatización"],
            "ultimo_post": "Buscamos proveedores de infraestructura híbrida. Abierto a propuestas.",
            "nivel_actividad": "Muy Alto",
            "tono": "Profesional y directo",
            "engagement_promedio": 12.4,
            "horario_activo": "09:00-18:00"
        },
        4: {  # Juan Perez - Ejecutivo Senior
            "red_principal": "Facebook",
            "intereses": ["Economía", "Golf", "Vinos Premium", "Inversiones"],
            "ultimo_post": "Análisis del mercado bursátil esta semana",
            "nivel_actividad": "Bajo",
            "tono": "Conservador y formal",
            "engagement_promedio": 3.1,
            "horario_activo": "12:00-14:00"
        },
        5: {  # Ana Torres - GenZ Student
            "red_principal": "TikTok",
            "intereses": ["Study hacks", "Moda low-cost", "K-pop", "DIY"],
            "ultimo_post": "📚 Cómo aprobé todos mis exámenes con este método",
            "nivel_actividad": "Alto",
            "tono": "Informal y creativo",
            "engagement_promedio": 9.7,
            "horario_activo": "21:00-00:00"
        },
        6: {  # Roberto Silva - Retail Manager
            "red_principal": "LinkedIn",
            "intereses": ["Retail Tech", "CX", "Gestión de equipos", "E-commerce"],
            "ultimo_post": "Cómo implementamos un sistema POS que aumentó ventas 30%",
            "nivel_actividad": "Medio",
            "tono": "Práctico y orientado a resultados",
            "engagement_promedio": 5.8,
            "horario_activo": "10:00-17:00"
        },
        7: {  # Laura Vega - Marketer Digital
            "red_principal": "Instagram",
            "intereses": ["Marketing Digital", "SEO", "Branding", "Creatividad"],
            "ultimo_post": "5 tendencias de marketing que dominarán 2025",
            "nivel_actividad": "Alto",
            "tono": "Educativo y trendy",
            "engagement_promedio": 7.9,
            "horario_activo": "15:00-19:00"
        },
        8: {  # Pedro Morales - Industrial
            "red_principal": "LinkedIn",
            "intereses": ["Manufactura 4.0", "IoT Industrial", "Eficiencia operativa"],
            "ultimo_post": "Nuestra planta redujo tiempos de producción con sensores IoT",
            "nivel_actividad": "Bajo",
            "tono": "Técnico y conservador",
            "engagement_promedio": 4.2,
            "horario_activo": "08:00-16:00"
        }
    }
    
    @staticmethod
    def obtener_perfil_social(cliente_id: int) -> Dict:
        """
        Simula una llamada a API de redes sociales
        En producción: requests.get("https://graph.facebook.com/...")
        """
        
        # Simular latencia de red
        import time
        time.sleep(0.3)  # 300ms de delay simulado
        
        perfil = MockSocialAPI.MOCK_DATABASE.get(
            cliente_id,
            {
                "red_principal": "N/A",
                "intereses": ["General"],
                "ultimo_post": "Sin actividad reciente",
                "nivel_actividad": "Desconocido",
                "tono": "Neutral",
                "engagement_promedio": 0.0,
                "horario_activo": "N/A"
            }
        )
        
        # Agregar timestamp de consulta
        from datetime import datetime
        perfil["fecha_consulta"] = datetime.now().isoformat()
        
        return perfil
    
    @staticmethod
    def calcular_score_social(perfil: Dict) -> float:
        """
        Calcula un score de 0-10 basado en la actividad social
        Usado para priorizar campañas
        """
        scores = {
            "Muy Alto": 10,
            "Alto": 8,
            "Medio": 5,
            "Bajo": 2,
            "Desconocido": 0
        }
        
        base_score = scores.get(perfil.get("nivel_actividad", "Desconocido"), 0)
        engagement = perfil.get("engagement_promedio", 0)
        
        # Score ponderado
        final_score = (base_score * 0.6) + (engagement * 0.4)
        
        return round(final_score, 2)


# Ejemplo de uso
if __name__ == "__main__":
    api = MockSocialAPI()
    
    for cliente_id in [1, 2, 3]:
        perfil = api.obtener_perfil_social(cliente_id)
        score = api.calcular_score_social(perfil)
        print(f"\nCliente {cliente_id}:")
        print(f"  Red: {perfil['red_principal']}")
        print(f"  Intereses: {perfil['intereses']}")
        print(f"  Score Social: {score}/10")