#!/usr/bin/env python3
"""
OpenCode Mock Server Simple - ArcheoScope

Servidor simulado de OpenCode/Zen usando solo stdlib (sin Flask).
Simula respuestas de validación lógica estructurada.

Uso:
    python opencode_mock_server_simple.py

Luego en .env:
    OPENCODE_ENABLED=true
    OPENCODE_API_URL=http://localhost:8080
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenCodeHandler(BaseHTTPRequestHandler):
    """Handler para requests de OpenCode."""
    
    def log_message(self, format, *args):
        """Override para logging personalizado."""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def do_GET(self):
        """Handle GET requests."""
        
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "service": "OpenCode Mock Server",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response).encode())
            logger.info("✅ Health check OK")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests."""
        
        if self.path == '/analyze':
            try:
                # Leer body
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                data = json.loads(body.decode())
                
                task = data.get('task', 'unknown')
                analysis_data = data.get('data', {})
                
                logger.info(f"📥 Tarea recibida: {task}")
                
                # Procesar según task
                if task == 'validate_coherence':
                    result = validate_coherence(analysis_data)
                elif task == 'explain_archaeological':
                    result = explain_archaeological(analysis_data)
                elif task == 'classify_pattern':
                    result = classify_pattern(analysis_data)
                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error = {
                        "error": f"Unknown task: {task}",
                        "supported_tasks": [
                            "validate_coherence",
                            "explain_archaeological",
                            "classify_pattern"
                        ]
                    }
                    self.wfile.write(json.dumps(error).encode())
                    return
                
                # Enviar respuesta exitosa
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
                logger.info(f"✅ Respuesta enviada para {task}")
                
            except Exception as e:
                logger.error(f"❌ Error: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error = {"error": str(e)}
                self.wfile.write(json.dumps(error).encode())
        else:
            self.send_response(404)
            self.end_headers()

def validate_coherence(data):
    """Validar coherencia lógica de un candidato arqueológico."""
    
    score = data.get('score', 0.0)
    instruments = data.get('instruments', [])
    convergence = data.get('convergence', 0)
    environment = data.get('environment', 'unknown')
    
    # Lógica de validación simulada
    is_coherent = True
    inconsistencies = []
    confidence = 0.8
    false_positive_risk = 0.2
    
    # Regla 1: Score alto requiere múltiples instrumentos
    if score > 0.8 and convergence < 2:
        is_coherent = False
        inconsistencies.append(
            "Score alto (>0.8) con baja convergencia instrumental (<2) - posible falso positivo"
        )
        false_positive_risk += 0.3
    
    # Regla 2: Convergencia alta debe reflejarse en score
    if convergence >= 3 and score < 0.6:
        inconsistencies.append(
            "Alta convergencia instrumental pero score bajo - revisar calibración"
        )
        confidence -= 0.2
    
    # Regla 3: Ambiente desconocido reduce confianza
    if environment == 'unknown':
        inconsistencies.append(
            "Ambiente no clasificado - dificulta interpretación arqueológica"
        )
        confidence -= 0.1
    
    # Regla 4: Instrumentos de baja confianza
    low_confidence_instruments = [
        inst for inst in instruments 
        if inst.get('confidence') == 'low'
    ]
    if len(low_confidence_instruments) > len(instruments) / 2:
        inconsistencies.append(
            f"Mayoría de instrumentos con baja confianza ({len(low_confidence_instruments)}/{len(instruments)})"
        )
        confidence -= 0.15
    
    # Ajustar confianza final
    confidence = max(0.1, min(1.0, confidence))
    false_positive_risk = max(0.0, min(1.0, false_positive_risk))
    
    # Generar razonamiento
    if is_coherent:
        reasoning = (
            f"Candidato muestra coherencia lógica: score {score:.2f} respaldado por "
            f"{convergence} instrumentos convergentes de {len(instruments)} totales. "
            f"Patrón consistente con intervención humana antigua."
        )
    else:
        reasoning = (
            f"Candidato presenta inconsistencias lógicas: {len(inconsistencies)} detectadas. "
            f"Score {score:.2f} no está adecuadamente respaldado por evidencia instrumental. "
            f"Revisar calibración o considerar procesos naturales alternativos."
        )
    
    # Generar recomendaciones
    recommendations = []
    if score > 0.8:
        recommendations.append("Candidato fuerte - proceder con investigación detallada")
    elif score > 0.6:
        recommendations.append("Candidato moderado - adquirir datos adicionales")
    else:
        recommendations.append("Candidato débil - considerar como baja prioridad")
    
    if convergence < 2:
        recommendations.append("Aumentar número de instrumentos para mayor confianza")
    
    if len(inconsistencies) > 0:
        recommendations.append("Resolver inconsistencias detectadas antes de proceder")
    
    # Clasificar patrón
    instrument_types = [inst.get('type', '') for inst in instruments]
    if 'thermal' in instrument_types and score > 0.7:
        pattern_type = "estructura_termica"
    elif 'sar' in instrument_types and convergence >= 2:
        pattern_type = "estructura_geometrica"
    elif 'ndvi' in instrument_types:
        pattern_type = "anomalia_vegetacion"
    else:
        pattern_type = "patron_mixto"
    
    logger.info(f"   Coherente: {is_coherent}, Confianza: {confidence:.2f}")
    
    return {
        "is_coherent": is_coherent,
        "confidence": confidence,
        "reasoning": reasoning,
        "inconsistencies": inconsistencies,
        "pattern_type": pattern_type,
        "recommendations": recommendations,
        "false_positive_risk": false_positive_risk,
        "analysis_metadata": {
            "task": "validate_coherence",
            "timestamp": datetime.now().isoformat(),
            "model": "opencode_mock_v1.0"
        }
    }

def explain_archaeological(data):
    """Generar explicación arqueológica estructurada."""
    
    candidate_id = data.get('candidate_id', 'unknown')
    region = data.get('region', 'unknown')
    score = data.get('score', 0.0)
    evidence = data.get('evidence', [])
    
    return {
        "summary": f"Análisis arqueológico de {region} (ID: {candidate_id})",
        "detection_summary": f"Score arqueológico: {score:.3f} basado en {len(evidence)} capas de evidencia",
        "instrumental_analysis": [
            f"- {ev.get('type', 'unknown')}: valor {ev.get('value', 0):.2f}"
            for ev in evidence[:5]
        ],
        "archaeological_interpretation": (
            f"Patrón {'altamente' if score > 0.8 else 'moderadamente' if score > 0.6 else 'débilmente'} "
            f"consistente con intervención humana antigua."
        ),
        "confidence_notes": f"Confianza {'alta' if score > 0.7 else 'moderada' if score > 0.5 else 'baja'} en detección",
        "recommendations": [
            "Validación con datos de mayor resolución",
            "Correlación con bases de datos arqueológicas regionales"
        ],
        "timestamp": datetime.now().isoformat()
    }

def classify_pattern(data):
    """Clasificar tipo de patrón arqueológico."""
    
    geometry = data.get('geometry', 0.0)
    instruments = data.get('instruments', [])
    
    if geometry > 0.8:
        pattern_type = "estructura_compacta"
    elif geometry > 0.5:
        pattern_type = "area_modificada"
    else:
        pattern_type = "anomalia_dispersa"
    
    return {
        "pattern_type": pattern_type,
        "confidence": 0.7,
        "alternative_classifications": ["estructura_subsuperficial", "modificacion_paisaje"],
        "timestamp": datetime.now().isoformat()
    }

def run_server(port=8080):
    """Iniciar servidor."""
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, OpenCodeHandler)
    
    print("=" * 60)
    print("🧠 OpenCode Mock Server - ArcheoScope")
    print("=" * 60)
    print()
    print(f"Servidor corriendo en http://localhost:{port}")
    print()
    print("Endpoints disponibles:")
    print("  - GET  /health  → Health check")
    print("  - POST /analyze → Análisis OpenCode")
    print()
    print("Tasks soportados:")
    print("  - validate_coherence")
    print("  - explain_archaeological")
    print("  - classify_pattern")
    print()
    print("Para habilitar en ArcheoScope:")
    print("  1. Edita .env:")
    print("     OPENCODE_ENABLED=true")
    print("     OPENCODE_API_URL=http://localhost:8080")
    print("  2. Reinicia el backend")
    print()
    print("Presiona Ctrl+C para detener")
    print("=" * 60)
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
