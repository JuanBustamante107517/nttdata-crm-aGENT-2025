"""
Módulo: Output Generator
Responsabilidad: Exportar resultados en HTML, JSON y CSV
"""
import json
import os
from datetime import datetime
from typing import Dict


class OutputGenerator:
    """Genera archivos de salida en múltiples formatos"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generar_json(self, resultado: Dict, nombre_archivo: str = None) -> str:
        """Exporta resultado completo a JSON"""
        if not nombre_archivo:
            cliente_nombre = resultado['cliente']['nombre'].replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"campana_{cliente_nombre}_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, nombre_archivo)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def generar_html(self, resultado: Dict, nombre_archivo: str = None) -> str:
        """Genera visualización HTML profesional"""
        if not nombre_archivo:
            cliente_nombre = resultado['cliente']['nombre'].replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"campana_{cliente_nombre}_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, nombre_archivo)
        
        html = self._template_html(resultado)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath
    
    def generar_csv(self, resultados_multiples: list, nombre_archivo: str = "resultados.csv") -> str:
        """Genera CSV consolidado de múltiples ejecuciones"""
        import csv
        
        filepath = os.path.join(self.output_dir, nombre_archivo)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Headers
            writer.writerow([
                'Timestamp',
                'Cliente',
                'Sector',
                'Segmento',
                'Confianza',
                'Campaña',
                'Canal',
                'Descuento',
                'Open Rate Esperado',
                'CTR Esperado',
                'Conversión Esperada'
            ])
            
            # Datos
            for resultado in resultados_multiples:
                writer.writerow([
                    resultado['metadata']['timestamp'],
                    resultado['cliente']['nombre'],
                    resultado['cliente']['sector'],
                    resultado['segmentacion']['segmento'],
                    f"{resultado['segmentacion']['confianza']:.2f}",
                    resultado['campana']['nombre'],
                    resultado['campana']['canal'],
                    f"{resultado['campana']['descuento']*100:.0f}%",
                    resultado['campana']['metricas_esperadas']['open_rate_esperado'],
                    resultado['campana']['metricas_esperadas']['ctr_esperado'],
                    resultado['campana']['metricas_esperadas']['conversion_esperada']
                ])
        
        return filepath
    
    def _template_html(self, resultado: Dict) -> str:
        """Template HTML con diseño profesional"""
        cliente = resultado['cliente']
        segmentacion = resultado['segmentacion']
        campana = resultado['campana']
        metadata = resultado['metadata']
        
        # Generar lista de razones
        razones_html = "".join([
            f"<li>{razon}</li>" for razon in segmentacion['razones']
        ])
        
        # Generar log
        log_html = ""
        for entrada in resultado.get('log_estados', [])[:10]:  # Últimas 10 entradas
            log_html += f"""
            <div class="log-entry">
                <span class="log-time">{entrada['timestamp'].split('T')[1].split('.')[0]}</span>
                <span class="log-estado">{entrada['estado'].upper()}</span>
                <span class="log-msg">{entrada['mensaje']}</span>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campaña - {cliente['nombre']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .section h2 {{
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 15px;
        }}
        .badge {{
            display: inline-block;
            padding: 6px 12px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin-right: 10px;
        }}
        .metric {{
            display: inline-block;
            margin: 10px 15px 10px 0;
        }}
        .metric-label {{
            color: #6c757d;
            font-size: 0.9em;
            display: block;
        }}
        .metric-value {{
            color: #212529;
            font-size: 1.3em;
            font-weight: bold;
        }}
        .campana-preview {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-top: 15px;
        }}
        .campana-asunto {{
            font-size: 1.2em;
            font-weight: bold;
            color: #212529;
            margin-bottom: 10px;
        }}
        .campana-mensaje {{
            line-height: 1.6;
            color: #495057;
            white-space: pre-line;
        }}
        .cta-button {{
            display: inline-block;
            margin-top: 15px;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
        }}
        ul {{ margin-left: 20px; line-height: 1.8; }}
        .log-section {{
            background: #212529;
            color: #00ff00;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            max-height: 300px;
            overflow-y: auto;
        }}
        .log-entry {{
            margin-bottom: 5px;
        }}
        .log-time {{ color: #6c757d; }}
        .log-estado {{ color: #ffc107; font-weight: bold; }}
        .log-msg {{ color: #00ff00; }}
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Campaña Generada</h1>
            <p>Agente Inteligente CRM - NTT DATA Hackathon</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generado: {metadata['timestamp']}</p>
        </div>
        
        <div class="content">
            <!-- SECCIÓN CLIENTE -->
            <div class="section">
                <h2>👤 Perfil del Cliente</h2>
                <p><strong>Nombre:</strong> {cliente['nombre']}</p>
                <p><strong>Sector:</strong> <span class="badge">{cliente['sector']}</span></p>
                <p><strong>Gasto Promedio:</strong> ${cliente['gasto_promedio']:,.2f}</p>
                <p><strong>Riesgo de Abandono:</strong> {cliente['riesgo']}</p>
            </div>
            
            <!-- SECCIÓN SEGMENTACIÓN -->
            <div class="section">
                <h2>🎯 Segmentación Inteligente</h2>
                <p><strong>Segmento Asignado:</strong> <span class="badge">{segmentacion['segmento'].replace('_', ' ')}</span></p>
                <p><strong>Nivel de Confianza:</strong> {segmentacion['confianza']*100:.1f}%</p>
                <p><strong>Score Social:</strong> {segmentacion['score_social']}/10</p>
                <p style="margin-top: 15px;"><strong>Razones de Segmentación:</strong></p>
                <ul>
                    {razones_html}
                </ul>
            </div>
            
            <!-- SECCIÓN CAMPAÑA -->
            <div class="section">
                <h2>📧 Campaña Seleccionada</h2>
                <p><strong>Nombre:</strong> {campana['nombre']}</p>
                <p><strong>Canal:</strong> <span class="badge">{campana['canal']}</span></p>
                <p><strong>Descuento Aplicado:</strong> {campana['descuento']*100:.0f}%</p>
                
                <div class="campana-preview">
                    <div class="campana-asunto">✉️ {campana['asunto']}</div>
                    <div class="campana-mensaje">{campana['mensaje']}</div>
                    <a href="#" class="cta-button">{campana['cta']}</a>
                </div>
            </div>
            
            <!-- MÉTRICAS ESPERADAS -->
            <div class="section">
                <h2>📊 Métricas Esperadas</h2>
                <div class="metric">
                    <span class="metric-label">Open Rate</span>
                    <span class="metric-value">{campana['metricas_esperadas']['open_rate_esperado']}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">CTR</span>
                    <span class="metric-value">{campana['metricas_esperadas']['ctr_esperado']}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Conversión</span>
                    <span class="metric-value">{campana['metricas_esperadas']['conversion_esperada']}</span>
                </div>
            </div>
            
            <!-- LOG DE EJECUCIÓN -->
            <div class="section">
                <h2>📝 Log de Ejecución del Agente</h2>
                <div class="log-section">
                    {log_html}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 Generado automáticamente por el Agente CRM Inteligente</p>
            <p>NTT DATA GenAI Hackathon 2025</p>
        </div>
    </div>
</body>
</html>
"""
        return html