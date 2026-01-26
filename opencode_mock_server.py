#!/usr/bin/env python3
"""
OpenCode Mock Server - ArcheoScope

Servidor simulado de OpenCode/Zen para testing local.
Simula respuestas de validación lógica estructurada.

Uso:
    python opencode_mock_server.py

Luego en .env:
    OPENCODE_ENABLED=true
    OPENCODE_API_URL=http://localhost:8080
"""

from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "OpenCode Mock Server",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint principal de análisis OpenCode.
    
    Simula validación lógica estructurada de candidatos arqueológicos.
    """
    
    try:
        data = request.json
        task = data.get('task', 'unknown')
        analysis_data = data.get('data', {})
        
        logger.info(f"📥 Recibida tarea: {task}")
        
        if task == 'validate_coherence':
            return jsonify(validate_coherence(analysis_data))
        
        elif task == 'explain_archaeological':
            return jsonify(explain_archaeological(analysis_data))
        
        elif task == 'classify_pattern':
            return jsonify(classify_pattern(analysis_data))
        
        else:
            return jsonify({
                "error": f"Unknown task: {task}",
                "supported_tasks": [
                    "validate_coherence",
                    "explain_archaeological",
                    "classify_pattern"
                ]
            }), 400
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

def validate_coherence(data):
    """
    Validar coherencia lógica de un candidato arqueológico.
    
    Simula razonamiento estructurado de OpenCode/Zen.
    """
    
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
    reasoning = generate_reasoning(
        score, convergence, len(instruments), 
        is_coherent, inconsistencies
    )
    
    # Generar recomendaciones
    recommendations = generate_recommendations(
        score, convergence, inconsistencies, environment
    )
    
    # Clasificar patrón
    pattern_type = infer_pattern_type(score, convergence, instruments)
    
    logger.info(f"✅ Validación completada: coherente={is_coherent}, confianza={confidence:.2f}")
    
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
    
    # Generar explicación estructurada
    explanation = {
        "summary": f"Análisis arqueológico de {region} (ID: {candidate_id})",
        "detection_summary": f"Score arqueológico: {score:.3f} basado en {len(evidence)} capas de evidencia",
        "instrumental_analysis": [
            f"- {ev.get('type', 'unknown')}: valor {ev.get('value', 0):.2f}"
            for ev in evidence[:5]  # Top 5
        ],
        "archaeological_interpretation": generate_archaeological_interpretation(score, evidence),
        "confidence_notes": f"Confianza {'alta' if score > 0.7 else 'moderada' if score > 0.5 else 'baja'} en detección",
        "recommendations": [
            "Validación con datos de mayor resolución",
            "Correlación con bases de datos arqueológicas regionales",
            "Análisis de contexto cultural e histórico"
        ],
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"✅ Explicación generada para {region}")
    
    return explanation

def classify_pattern(data):
    """Clasificar tipo de patrón arqueológico."""
    
    geometry = data.get('geometry', 0.0)
    spatial_extent = data.get('spatial_extent', {})
    instruments = data.get('instruments', [])
    
    # Clasificación basada en geometría y extensión
    if geometry > 0.8:
        if 'thermal' in instruments:
            pattern_type = "estructura_compacta"
        else:
            pattern_type = "asentamiento_planificado"
    elif geometry > 0.5:
        if 'sar' in instruments:
            pattern_type = "camino_o_canal"
        else:
            pattern_type = "area_modificada"
    else:
        pattern_type = "anomalia_dispersa"
    
    logger.info(f"✅ Patrón clasificado: {pattern_type}")
    
    return {
        "pattern_type": pattern_type,
        "confidence": 0.7,
        "alternative_classifications": [
            "estructura_subsuperficial",
            "modificacion_paisaje"
        ],
        "timestamp": datetime.now().isoformat()
    }

def generate_reasoning(score, convergence, num_instruments, is_coherent, inconsistencies):
    """Generar razonamiento estructurado."""
    
    if is_coherent:
        return (
            f"Candidato muestra coherencia lógica: score {score:.2f} respaldado por "
            f"{convergence} instrumentos convergentes de {num_instruments} totales. "
            f"Patrón consistente con intervención humana antigua."
        )
    else:
        return (
            f"Candidato presenta inconsistencias lógicas: {len(inconsistencies)} detectadas. "
            f"Score {score:.2f} no está adecuadamente respaldado por evidencia instrumental. "
            f"Revisar calibración o considerar procesos naturales alternativos."
        )

def generate_recommendations(score, convergence, inconsistencies, environment):
    """Generar recomendaciones específicas."""
    
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
    
    if environment == 'unknown':
        recommendations.append("Clasificar ambiente para mejor interpretación")
    
    return recommendations

def infer_pattern_type(score, convergence, instruments):
    """Inferir tipo de patrón basado en características."""
    
    instrument_types = [inst.get('type', '') for inst in instruments]
    
    if 'thermal' in instrument_types and score > 0.7:
        return "estructura_termica"
    elif 'sar' in instrument_types and convergence >= 2:
        return "estructura_geometrica"
    elif 'ndvi' in instrument_types:
        return "anomalia_vegetacion"
    else:
        return "patron_mixto"

def generate_archaeological_interpretation(score, evidence):
    """Generar interpretación arqueológica."""
    
    if score > 0.8:
        return (
            "Patrón altamente consistente con intervención humana antigua. "
            "Múltiples líneas de evidencia convergen en anomalía espacial persistente. "
            "Recomendado para investigación arqueológica prioritaria."
        )
    elif score > 0.6:
        return (
            "Patrón moderadamente consistente con posible actividad humana antigua. "
            "Evidencia sugiere modificación del paisaje, pero requiere validación adicional."
        )
    else:
        return (
            "Patrón débil - puede ser explicado por procesos naturales. "
            "Considerar como candidato de baja prioridad hasta obtener datos adicionales."
        )

if __name__ == '__main__':
    print("=" * 60)
    print("🧠 OpenCode Mock Server - ArcheoScope")
    print("=" * 60)
    print()
    print("Servidor iniciando en http://localhost:8080")
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
    
    app.run(host='0.0.0.0', port=8080, debug=False)
