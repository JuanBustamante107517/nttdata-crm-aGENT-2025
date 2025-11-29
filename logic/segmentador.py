"""
Módulo: Segmentador
Responsabilidad: Clasificar clientes en segmentos usando reglas de negocio
"""
from typing import Dict


class Segmentador:
    """
    Clasifica clientes en segmentos según múltiples dimensiones:
    - Datos CRM (gasto, riesgo, sector)
    - Señales sociales (actividad, intereses)
    """
    
    # Definición de segmentos (mínimo 2, aquí usamos 5)
    SEGMENTOS = {
        "VIP_ALTO_VALOR": {
            "descripcion": "Clientes de alto valor con engagement activo",
            "criterios": "Gasto > 5000 AND Riesgo Bajo AND Social Score > 7"
        },
        "RIESGO_FUGA": {
            "descripcion": "Clientes con señales de abandono",
            "criterios": "Riesgo Alto OR (Social Score < 3 AND Gasto > 1000)"
        },
        "EARLY_ADOPTER": {
            "descripcion": "Tech-savvy con alta actividad en redes",
            "criterios": "Sector Tech OR (Intereses incluye IA/Startups) AND Social Score > 7"
        },
        "MASS_MARKET": {
            "descripcion": "Clientes estándar con engagement moderado",
            "criterios": "Gasto < 1000 AND Riesgo Medio AND Social Score 4-7"
        },
        "B2B_ENTERPRISE": {
            "descripcion": "Empresas con alto ticket y ciclo largo",
            "criterios": "Sector B2B OR Gasto > 10000"
        }
    }
    
    @staticmethod
    def segmentar(cliente: Dict, perfil_social: Dict) -> Dict:
        """
        Aplica reglas de negocio para determinar el segmento
        
        Returns:
            {
                "segmento": str,
                "confianza": float,
                "razones": List[str]
            }
        """
        gasto = cliente.get('Gasto_Promedio', 0)
        riesgo = cliente.get('Riesgo_Abandono', 'Medio')
        sector = cliente.get('Sector', '')
        
        from logic.mock_social import MockSocialAPI
        score_social = MockSocialAPI.calcular_score_social(perfil_social)
        
        intereses = perfil_social.get('intereses', [])
        intereses_str = ' '.join(intereses).lower()
        
        razones = []
        
        # REGLA 1: B2B Enterprise (máxima prioridad)
        if sector == "B2B" or gasto > 10000:
            razones.append(f"Sector {sector} con gasto promedio ${gasto:,.0f}")
            return {
                "segmento": "B2B_ENTERPRISE",
                "confianza": 0.95,
                "razones": razones,
                "score_social": score_social
            }
        
        # REGLA 2: Early Adopter
        tech_keywords = ['ia', 'startups', 'tech', 'web3', 'gadgets', 'gaming']
        if sector == "Tecnología" or any(kw in intereses_str for kw in tech_keywords):
            if score_social > 7:
                razones.append(f"Perfil tecnológico con alta actividad social (score: {score_social})")
                razones.append(f"Intereses: {', '.join(intereses[:3])}")
                return {
                    "segmento": "EARLY_ADOPTER",
                    "confianza": 0.88,
                    "razones": razones,
                    "score_social": score_social
                }
        
        # REGLA 3: Riesgo de Fuga (alta prioridad)
        if riesgo == "Alto" or (score_social < 3 and gasto > 1000):
            razones.append(f"Riesgo de abandono: {riesgo}")
            if score_social < 3:
                razones.append(f"Baja actividad social (score: {score_social})")
            return {
                "segmento": "RIESGO_FUGA",
                "confianza": 0.82,
                "razones": razones,
                "score_social": score_social
            }
        
        # REGLA 4: VIP Alto Valor
        if gasto > 5000 and riesgo == "Bajo" and score_social > 7:
            razones.append(f"Alto valor (${gasto:,.0f}) con engagement activo")
            return {
                "segmento": "VIP_ALTO_VALOR",
                "confianza": 0.90,
                "razones": razones,
                "score_social": score_social
            }
        
        # REGLA 5: Mass Market (default)
        razones.append(f"Perfil estándar: Gasto ${gasto:,.0f}, Riesgo {riesgo}")
        razones.append(f"Score social: {score_social}")
        return {
            "segmento": "MASS_MARKET",
            "confianza": 0.70,
            "razones": razones,
            "score_social": score_social
        }
    
    @staticmethod
    def obtener_descripcion_segmento(segmento: str) -> str:
        """Retorna la descripción legible del segmento"""
        return Segmentador.SEGMENTOS.get(segmento, {}).get(
            "descripcion", 
            "Segmento no definido"
        )
