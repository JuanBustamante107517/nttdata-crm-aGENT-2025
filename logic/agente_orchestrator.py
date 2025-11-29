"""
Módulo: Agente Orchestrator (FSM)
Responsabilidad: Coordinar el flujo completo del agente autónomo
"""
from enum import Enum
from typing import Dict, List
from datetime import datetime
import logging

from logic.data_loader import DataLoader
from logic.mock_social import MockSocialAPI
from logic.segmentador import Segmentador
from logic.campanas import GeneradorCampanas


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EstadoAgente(Enum):
    """Estados de la FSM del agente"""
    INACTIVO = "inactivo"
    INGESTA = "ingesta"
    PERFIL = "perfil"
    SEGMENTO = "segmento"
    CAMPANA = "campana"
    SALIDA = "salida"
    COMPLETADO = "completado"
    ERROR = "error"


class AgenteOrchestrator:
    """
    Finite State Machine que ejecuta el loop autónomo:
    INGESTA → PERFIL → SEGMENTO → CAMPAÑA → SALIDA
    """
    
    def __init__(self, usar_genai: bool = False):
        self.estado_actual = EstadoAgente.INACTIVO
        self.log_ejecucion = []
        self.resultados = {}
        self.data_loader = DataLoader()
        self.usar_genai = usar_genai
        
        # Inicializar GenAI solo si se solicita
        if usar_genai:
            try:
                from logic.genai_enhancer import GenAIEnhancer
                self.genai = GenAIEnhancer()
                if self.genai.disponible:
                    logger.info("✅ GenAI habilitado")
                else:
                    logger.info("⚠️ GenAI solicitado pero no disponible, usando templates")
                    self.usar_genai = False
            except ImportError:
                logger.info("⚠️ GenAI no disponible, usando modo determinístico")
                self.usar_genai = False
        
    def log_estado(self, estado: EstadoAgente, mensaje: str, datos: Dict = None):
        """Registra cada transición de estado"""
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "estado": estado.value,
            "mensaje": mensaje,
            "datos": datos or {}
        }
        self.log_ejecucion.append(entrada)
        logger.info(f"[{estado.value.upper()}] {mensaje}")
    
    def ejecutar_pipeline(self, cliente_nombre: str) -> Dict:
        """
        Punto de entrada principal
        Ejecuta todo el flujo sin intervención manual
        """
        try:
            self.log_estado(EstadoAgente.INACTIVO, f"Iniciando pipeline para {cliente_nombre}")
            
            # ESTADO 1: INGESTA
            cliente_data = self._estado_ingesta(cliente_nombre)
            
            # ESTADO 2: PERFIL
            perfil_social = self._estado_perfil(cliente_data)
            
            # ESTADO 3: SEGMENTO
            segmentacion = self._estado_segmento(cliente_data, perfil_social)
            
            # ESTADO 4: CAMPAÑA
            campana = self._estado_campana(cliente_data, perfil_social, segmentacion)
            
            # ESTADO 5: SALIDA
            resultado_final = self._estado_salida(cliente_data, segmentacion, campana)
            
            self.estado_actual = EstadoAgente.COMPLETADO
            self.log_estado(
                EstadoAgente.COMPLETADO, 
                "Pipeline ejecutado exitosamente",
                {"duracion_total": len(self.log_ejecucion)}
            )
            
            return {
                "exito": True,
                "resultado": resultado_final,
                "log": self.log_ejecucion
            }
            
        except Exception as e:
            self.estado_actual = EstadoAgente.ERROR
            self.log_estado(EstadoAgente.ERROR, f"Error crítico: {str(e)}")
            logger.error(f"Pipeline falló: {e}", exc_info=True)
            
            return {
                "exito": False,
                "error": str(e),
                "log": self.log_ejecucion
            }
    
    def _estado_ingesta(self, cliente_nombre: str) -> Dict:
        """ESTADO 1: Cargar datos del cliente desde CSV"""
        self.estado_actual = EstadoAgente.INGESTA
        self.log_estado(EstadoAgente.INGESTA, f"Cargando datos de {cliente_nombre}")
        
        try:
            cliente = self.data_loader.obtener_cliente_por_nombre(cliente_nombre)
            
            self.log_estado(
                EstadoAgente.INGESTA,
                f"Cliente encontrado: {cliente['Nombre']}",
                {
                    "id": cliente['ID'],
                    "sector": cliente['Sector'],
                    "gasto": cliente['Gasto_Promedio']
                }
            )
            
            return cliente
            
        except Exception as e:
            raise ValueError(f"Error en ingesta: {e}")
    
    def _estado_perfil(self, cliente: Dict) -> Dict:
        """ESTADO 2: Consultar API social (mock)"""
        self.estado_actual = EstadoAgente.PERFIL
        self.log_estado(
            EstadoAgente.PERFIL,
            f"Consultando perfil social del cliente ID {cliente['ID']}"
        )
        
        perfil = MockSocialAPI.obtener_perfil_social(cliente['ID'])
        score = MockSocialAPI.calcular_score_social(perfil)
        
        self.log_estado(
            EstadoAgente.PERFIL,
            f"Perfil obtenido de {perfil['red_principal']}",
            {
                "red": perfil['red_principal'],
                "score_social": score,
                "nivel_actividad": perfil['nivel_actividad'],
                "intereses": perfil['intereses'][:3]
            }
        )
        
        return perfil
    
    def _estado_segmento(self, cliente: Dict, perfil: Dict) -> Dict:
        """ESTADO 3: Aplicar reglas de segmentación"""
        self.estado_actual = EstadoAgente.SEGMENTO
        self.log_estado(EstadoAgente.SEGMENTO, "Ejecutando motor de segmentación")
        
        segmentacion = Segmentador.segmentar(cliente, perfil)
        descripcion = Segmentador.obtener_descripcion_segmento(segmentacion['segmento'])
        
        self.log_estado(
            EstadoAgente.SEGMENTO,
            f"Cliente asignado a: {segmentacion['segmento']}",
            {
                "segmento": segmentacion['segmento'],
                "confianza": segmentacion['confianza'],
                "descripcion": descripcion,
                "razones": segmentacion['razones']
            }
        )
        
        return segmentacion
    
    def _estado_campana(self, cliente: Dict, perfil: Dict, segmentacion: Dict) -> Dict:
        """ESTADO 4: Generar campaña personalizada"""
        self.estado_actual = EstadoAgente.CAMPANA
        self.log_estado(EstadoAgente.CAMPANA, "Generando campaña personalizada")
        
        # Seleccionar mejor campaña
        nombre_campana = GeneradorCampanas.seleccionar_campana(
            segmentacion['segmento'],
            perfil
        )
        
        self.log_estado(
            EstadoAgente.CAMPANA,
            f"Campaña seleccionada: {nombre_campana}"
        )
        
        # Personalizar con datos reales
        campana = GeneradorCampanas.personalizar_campana(
            nombre_campana,
            cliente,
            perfil,
            segmentacion['segmento']
        )
        
        # OPCIONAL: Mejorar con GenAI si está disponible
        if self.usar_genai and hasattr(self, 'genai'):
            self.log_estado(
                EstadoAgente.CAMPANA,
                "Mejorando mensaje con GenAI..."
            )
            
            mejora = self.genai.mejorar_mensaje(
                campana['mensaje'],
                cliente,
                perfil,
                segmentacion['segmento']
            )
            
            if mejora['mejorado_con_ia']:
                campana['mensaje'] = mejora['mensaje']
                campana['mensaje_original'] = mejora['mensaje_original']
                campana['mejorado_con_ia'] = True
                
                # Intentar mejorar asunto también
                asunto_mejorado = self.genai.generar_asunto_alternativo(
                    campana['asunto'],
                    cliente
                )
                if asunto_mejorado:
                    campana['asunto_original'] = campana['asunto']
                    campana['asunto'] = asunto_mejorado
                
                self.log_estado(
                    EstadoAgente.CAMPANA,
                    "Mensaje mejorado con IA generativa"
                )
            else:
                campana['mejorado_con_ia'] = False
        else:
            campana['mejorado_con_ia'] = False
        
        self.log_estado(
            EstadoAgente.CAMPANA,
            "Campaña personalizada generada",
            {
                "nombre": campana.get('nombre', campana.get('nombre_campana', 'N/A')),
                "canal": campana['canal'],
                "asunto": campana['asunto'],
                "descuento": f"{campana.get('descuento_aplicado', campana.get('descuento', 0))*100:.0f}%",
                "con_ia": campana.get('mejorado_con_ia', False)
            }
        )
        
        return campana
    
    def _estado_salida(self, cliente: Dict, segmentacion: Dict, campana: Dict) -> Dict:
        """ESTADO 5: Consolidar resultados finales"""
        self.estado_actual = EstadoAgente.SALIDA
        self.log_estado(EstadoAgente.SALIDA, "Preparando salida estructurada")
        
        resultado = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "cliente_id": cliente['ID'],
                "cliente_nombre": cliente['Nombre'],
                "estados_ejecutados": len(self.log_ejecucion)
            },
            "cliente": {
                "nombre": cliente['Nombre'],
                "sector": cliente['Sector'],
                "gasto_promedio": cliente['Gasto_Promedio'],
                "riesgo": cliente['Riesgo_Abandono']
            },
            "segmentacion": {
                "segmento": segmentacion['segmento'],
                "confianza": segmentacion['confianza'],
                "razones": segmentacion['razones'],
                "score_social": segmentacion['score_social']
            },
            "campana": {
                "nombre": campana['nombre_campana'],
                "canal": campana['canal'],
                "asunto": campana['asunto'],
                "mensaje": campana['mensaje'],
                "cta": campana['cta'],
                "descuento": campana['descuento_aplicado'],
                "metricas_esperadas": campana['metricas_esperadas']
            },
            "log_estados": self.log_ejecucion
        }
        
        self.resultados = resultado
        self.log_estado(EstadoAgente.SALIDA, "Resultado final consolidado")
        
        return resultado
    
    def obtener_log_legible(self) -> str:
        """Retorna el log en formato legible para UI"""
        lineas = []
        for entrada in self.log_ejecucion:
            timestamp = entrada['timestamp'].split('T')[1].split('.')[0]
            estado = entrada['estado'].upper()
            mensaje = entrada['mensaje']
            lineas.append(f"[{timestamp}] {estado:15} | {mensaje}")
        
        return "\n".join(lineas)


# Ejemplo de uso
if __name__ == "__main__":
    agente = AgenteOrchestrator()
    
    resultado = agente.ejecutar_pipeline("Carlos Ruiz")
    
    if resultado['exito']:
        print("✅ Pipeline ejecutado con éxito\n")
        print(f"Segmento: {resultado['resultado']['segmentacion']['segmento']}")
        print(f"Campaña: {resultado['resultado']['campana']['nombre']}")
        print(f"\n--- LOG DE EJECUCIÓN ---")
        print(agente.obtener_log_legible())
    else:
        print(f"❌ Error: {resultado['error']}")