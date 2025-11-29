"""
Módulo: Generador de Campañas
Responsabilidad: Seleccionar y personalizar plantillas de campañas
"""
from typing import Dict, List
import random


class GeneradorCampanas:
    """
    Gestiona 3+ plantillas de campañas y las personaliza
    según el segmento y perfil del cliente
    """
    
    # Plantillas de campañas (mínimo 3, aquí 5)
    PLANTILLAS = {
        "UPGRADE_PREMIUM": {
            "nombre": "Upgrade Premium",
            "segmentos_target": ["VIP_ALTO_VALOR", "EARLY_ADOPTER"],
            "canal": "email",
            "asunto_template": "🚀 {nombre}, accede a funciones exclusivas",
            "mensaje_template": """
Hola {nombre},

Hemos notado tu interés en {interes_principal}. 

Como cliente {segmento}, tienes acceso prioritario a nuestro plan Premium con:
✅ {beneficio_1}
✅ {beneficio_2}
✅ Soporte 24/7 personalizado

Activa tu upgrade con 30% de descuento hasta fin de mes.

[Activar Premium]

Saludos,
Equipo CRM Inteligente
            """,
            "cta": "Activar Premium",
            "descuento": 0.30
        },
        
        "RETENCION_URGENTE": {
            "nombre": "Retención con Oferta Especial",
            "segmentos_target": ["RIESGO_FUGA"],
            "canal": "sms",
            "asunto_template": "⚠️ {nombre}, te extrañamos",
            "mensaje_template": """
Hola {nombre},

Notamos que llevas tiempo sin interactuar con nosotros.

Como gesto de aprecio, te ofrecemos:
🎁 {beneficio_1}
🎁 Asesoría gratuita personalizada

Tu satisfacción es nuestra prioridad.

[Reclama tu oferta]

Equipo CRM
            """,
            "cta": "Reclama tu oferta",
            "descuento": 0.40
        },
        
        "EDUCACION_ONBOARDING": {
            "nombre": "Onboarding Educativo",
            "segmentos_target": ["MASS_MARKET", "EARLY_ADOPTER"],
            "canal": "email",
            "asunto_template": "📚 {nombre}, guía para aprovechar {producto}",
            "mensaje_template": """
Hola {nombre},

¿Sabías que el 80% de nuestros clientes en {sector} aumentan su productividad con {producto}?

Te compartimos:
📖 Guía práctica en 5 pasos
🎥 Video tutorial exclusivo
💬 Acceso a comunidad de usuarios

Empieza hoy y transforma tu {objetivo}.

[Ver guía completa]

Equipo de Éxito del Cliente
            """,
            "cta": "Ver guía completa",
            "descuento": 0.0
        },
        
        "CROSS_SELL": {
            "nombre": "Cross-Sell Inteligente",
            "segmentos_target": ["VIP_ALTO_VALOR", "B2B_ENTERPRISE"],
            "canal": "email",
            "asunto_template": "💡 {nombre}, complementa tu {producto_actual}",
            "mensaje_template": """
Hola {nombre},

Basado en tu historial de {historial}, identificamos una oportunidad:

{producto_nuevo} se integra perfectamente con tu configuración actual y te permitirá:
⚡ {beneficio_1}
⚡ {beneficio_2}

Clientes como tú reportan ROI del 150% en 3 meses.

[Solicitar demo]

Saludos,
{ejecutivo_cuenta}
            """,
            "cta": "Solicitar demo",
            "descuento": 0.15
        },
        
        "SOCIAL_ENGAGEMENT": {
            "nombre": "Engagement en Redes",
            "segmentos_target": ["EARLY_ADOPTER", "MASS_MARKET"],
            "canal": "dm_instagram",
            "asunto_template": "👋 {nombre}, vimos tu post sobre {tema}",
            "mensaje_template": """
Hola {nombre}! 👋

Nos encantó tu reciente post sobre {tema}.

Tenemos algo que podría interesarte:
{producto} está diseñado para personas como tú que buscan {objetivo}.

¿Te gustaría conocer más? Te regalamos 20% de descuento.

[Más info]

— Equipo Social Media
            """,
            "cta": "Más info",
            "descuento": 0.20
        }
    }
    
    @staticmethod
    def seleccionar_campana(segmento: str, perfil_social: Dict) -> str:
        """
        Selecciona la mejor campaña según el segmento
        Si hay múltiples opciones, prioriza por score social
        """
        candidatas = []
        
        for nombre_campana, config in GeneradorCampanas.PLANTILLAS.items():
            if segmento in config['segmentos_target']:
                candidatas.append(nombre_campana)
        
        # Si no hay match, usar educación como fallback
        if not candidatas:
            return "EDUCACION_ONBOARDING"
        
        # Si hay múltiples, elegir según nivel de actividad
        score = perfil_social.get('engagement_promedio', 5)
        
        if score > 7 and "SOCIAL_ENGAGEMENT" in candidatas:
            return "SOCIAL_ENGAGEMENT"
        
        return candidatas[0]
    
    @staticmethod
    def personalizar_campana(
        nombre_campana: str,
        cliente: Dict,
        perfil_social: Dict,
        segmento: str
    ) -> Dict:
        """
        Genera la campaña final con datos reales del cliente
        """
        plantilla = GeneradorCampanas.PLANTILLAS[nombre_campana]
        
        # Extraer datos
        nombre = cliente.get('Nombre', 'Cliente')
        sector = cliente.get('Sector', 'tu sector')
        historial = cliente.get('Historial_Compras', 'compras anteriores')
        
        intereses = perfil_social.get('intereses', ['tecnología'])
        interes_principal = intereses[0] if intereses else 'nuestros productos'
        
        # Generar beneficios dinámicos según segmento
        beneficios = GeneradorCampanas._generar_beneficios(segmento, sector)
        
        # Reemplazar variables en plantilla
        asunto = plantilla['asunto_template'].format(
            nombre=nombre,
            tema=interes_principal,
            producto="nuestra solución"
        )
        
        mensaje = plantilla['mensaje_template'].format(
            nombre=nombre,
            interes_principal=interes_principal,
            segmento=segmento.replace('_', ' ').title(),
            beneficio_1=beneficios[0],
            beneficio_2=beneficios[1] if len(beneficios) > 1 else "Acceso prioritario",
            sector=sector,
            historial=historial.split(',')[0] if ',' in historial else historial,
            producto="nuestra plataforma",
            producto_actual="herramientas actuales",
            producto_nuevo="Módulo Analytics Pro",
            objetivo="eficiencia operativa",
            tema=interes_principal,
            ejecutivo_cuenta="Juan Pérez, Account Manager"
        )
        
        # Retornar con AMBOS campos para compatibilidad
        return {
            "nombre_campana": plantilla['nombre'],
            "nombre": plantilla['nombre'],
            "canal": plantilla['canal'],
            "asunto": asunto,
            "mensaje": mensaje.strip(),
            "cta": plantilla['cta'],
            "descuento": plantilla['descuento'],
            "descuento_aplicado": plantilla['descuento'],  # Duplicado para compatibilidad
            "metricas_esperadas": GeneradorCampanas._estimar_metricas(
                segmento, 
                plantilla['canal']
            )
        }
    
    @staticmethod
    def _generar_beneficios(segmento: str, sector: str) -> List[str]:
        """Genera beneficios contextuales según segmento"""
        mapa_beneficios = {
            "VIP_ALTO_VALOR": [
                "Gerente de cuenta dedicado",
                "Acceso anticipado a nuevas features",
                "Reportes personalizados mensuales"
            ],
            "RIESGO_FUGA": [
                "50% de descuento en renovación",
                "3 meses gratis de soporte premium",
                "Migración asistida sin costo"
            ],
            "EARLY_ADOPTER": [
                "Beta access a funciones experimentales",
                "Sesiones de feedback con el equipo de producto",
                "Certificación gratuita"
            ],
            "B2B_ENTERPRISE": [
                "SLA del 99.9% garantizado",
                "Integración con tu ERP sin costo",
                "Capacitación on-site para tu equipo"
            ],
            "MASS_MARKET": [
                "Tutoriales paso a paso",
                "Comunidad de usuarios activa",
                "Plantillas prediseñadas"
            ]
        }
        
        return mapa_beneficios.get(segmento, ["Soporte dedicado", "Recursos exclusivos"])
    
    @staticmethod
    def _estimar_metricas(segmento: str, canal: str) -> Dict:
        """
        Simula métricas esperadas de la campaña
        En producción, usaría modelos ML entrenados
        """
        # Tasas base por segmento
        tasas_base = {
            "VIP_ALTO_VALOR": {"open_rate": 0.45, "ctr": 0.12, "conversion": 0.08},
            "EARLY_ADOPTER": {"open_rate": 0.52, "ctr": 0.18, "conversion": 0.06},
            "RIESGO_FUGA": {"open_rate": 0.35, "ctr": 0.08, "conversion": 0.15},
            "B2B_ENTERPRISE": {"open_rate": 0.38, "ctr": 0.10, "conversion": 0.05},
            "MASS_MARKET": {"open_rate": 0.28, "ctr": 0.06, "conversion": 0.03}
        }
        
        metricas = tasas_base.get(segmento, {"open_rate": 0.30, "ctr": 0.07, "conversion": 0.04})
        
        # Ajustar por canal
        if canal == "sms":
            metricas["open_rate"] = 0.98  # SMS tiene apertura casi garantizada
        elif canal == "dm_instagram":
            metricas["ctr"] *= 1.3  # Redes sociales tienen mayor engagement
        
        return {
            "open_rate_esperado": f"{metricas['open_rate']*100:.1f}%",
            "ctr_esperado": f"{metricas['ctr']*100:.1f}%",
            "conversion_esperada": f"{metricas['conversion']*100:.1f}%"
        }


# Ejemplo de uso
if __name__ == "__main__":
    cliente_test = {
        'Nombre': 'Carlos Ruiz',
        'Sector': 'Tecnología',
        'Historial_Compras': 'Laptops, Monitores'
    }
    
    perfil_test = {
        'intereses': ['IA', 'Startups'],
        'engagement_promedio': 8.5
    }
    
    campana_elegida = GeneradorCampanas.seleccionar_campana("EARLY_ADOPTER", perfil_test)
    print(f"Campaña seleccionada: {campana_elegida}\n")
    
    resultado = GeneradorCampanas.personalizar_campana(
        campana_elegida,
        cliente_test,
        perfil_test,
        "EARLY_ADOPTER"
    )
    
    print(f"Asunto: {resultado['asunto']}")
    print(f"Canal: {resultado['canal']}")
    print(f"\nMensaje:\n{resultado['mensaje']}")