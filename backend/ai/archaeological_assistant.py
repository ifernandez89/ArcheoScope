#!/usr/bin/env python3
"""
Asistente IA arqueológico para ArcheoScope usando OpenRouter/Ollama.

Especializado en explicar anomalías espaciales desde perspectiva arqueológica
con razonamiento científico riguroso.
"""

import requests
import json
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env.local')

logger = logging.getLogger(__name__)

@dataclass
class ArchaeologicalExplanation:
    """Explicación arqueológica estructurada."""
    explanation: str
    archaeological_interpretation: str
    confidence_assessment: str
    methodological_notes: str
    recommendations: List[str]
    limitations: str
    scientific_reasoning: str

class ArchaeologicalAssistant:
    """
    Asistente IA especializado en arqueología remota.
    
    Usa OpenRouter (Gemini 3 Preview) o Ollama para generar explicaciones 
    científicamente rigurosas de anomalías espaciales desde perspectiva arqueológica.
    """
    
    def __init__(self):
        """Inicializar asistente arqueológico con configuración desde .env.local"""
        
        # Leer configuración desde .env.local
        self.ollama_enabled = os.getenv('OLLAMA_ENABLED', 'false').lower() == 'true'
        self.openrouter_enabled = os.getenv('OPENROUTER_ENABLED', 'true').lower() == 'true'
        
        # Configuración OpenRouter
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.openrouter_model = os.getenv('OPENROUTER_MODEL', 'google/gemini-3.0-flash-preview-01-2025')
        
        # Configuración Ollama (fallback)
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'phi4-mini-reasoning')
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        
        # Timeouts
        self.ai_timeout = int(os.getenv('AI_TIMEOUT_SECONDS', '30'))
        self.max_tokens = int(os.getenv('AI_MAX_TOKENS', '300'))
        
        # Verificar disponibilidad
        self.is_available = self._check_availability()
        
        logger.info(f"ArchaeologicalAssistant inicializado:")
        logger.info(f"  - OpenRouter: {'✅' if self.openrouter_enabled else '❌'} ({self.openrouter_model})")
        logger.info(f"  - Ollama: {'✅' if self.ollama_enabled else '❌'} ({self.ollama_model})")
        logger.info(f"  - Disponible: {'✅' if self.is_available else '❌'}")
        
        # Prompt base arqueológico
        self.base_prompt = """Eres un especialista en arqueología remota y análisis espacial científico. 

Tu rol es analizar anomalías detectadas por sensores remotos desde una perspectiva arqueológica rigurosa.

PRINCIPIOS FUNDAMENTALES:
1. NUNCA afirmes "encontramos una ciudad" o "esto es un templo"
2. SIEMPRE usa lenguaje científico: "área con firma espacial consistente con intervención humana antigua"
3. Distingue entre: anomalías detectadas vs interpretaciones arqueológicas
4. Considera procesos naturales alternativos ANTES de sugerir origen antrópico
5. Evalúa persistencia temporal y coherencia geométrica como indicadores clave

METODOLOGÍA:
- Analiza patrones espaciales no explicables por procesos naturales actuales
- Evalúa coherencia entre múltiples tipos de datos (vegetación, térmico, SAR, etc.)
- Considera contexto geográfico y arqueológico regional
- Proporciona razonamiento paso a paso

FORMATO DE RESPUESTA:
- Explicación clara del patrón detectado
- Interpretación arqueológica cautelosa
- Evaluación de confianza y limitaciones
- Recomendaciones para investigación adicional"""
        
        logger.info(f"ArchaeologicalAssistant inicializado: modelo={self.openrouter_model if self.openrouter_enabled else self.ollama_model}, "
                   f"disponible={self.is_available}")
    
    def _check_availability(self) -> bool:
        """Verificar disponibilidad de IA (OpenRouter primero, luego Ollama)."""
        
        # Prioridad 1: OpenRouter
        if self.openrouter_enabled and self.openrouter_api_key:
            try:
                # Test simple con OpenRouter
                headers = {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json"
                }
                
                test_payload = {
                    "model": self.openrouter_model,
                    "messages": [{"role": "user", "content": "Test"}],
                    "max_tokens": 10
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=test_payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ OpenRouter disponible con {self.openrouter_model}")
                    return True
                else:
                    logger.warning(f"OpenRouter error: {response.status_code}")
                    
            except Exception as e:
                logger.warning(f"Error conectando con OpenRouter: {e}")
        
        # Prioridad 2: Ollama (fallback)
        if self.ollama_enabled:
            try:
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    available_models = [model['name'] for model in models]
                    
                    # Buscar phi4-mini-reasoning con cualquier tag
                    phi4_models = [m for m in available_models if 'phi4-mini-reasoning' in m]
                    
                    if phi4_models:
                        # Usar el primer modelo phi4 encontrado
                        self.ollama_model = phi4_models[0]
                        logger.info(f"✅ Ollama disponible con {self.ollama_model}")
                        return True
                    else:
                        logger.warning(f"Modelo phi4-mini-reasoning no encontrado. "
                                     f"Disponibles: {available_models}")
                        return False
                else:
                    logger.warning(f"Ollama no responde: {response.status_code}")
                    return False
                    
            except Exception as e:
                logger.warning(f"Error conectando con Ollama: {e}")
        
        logger.warning("❌ Ningún proveedor de IA disponible")
        return False
    
    def explain_archaeological_anomalies(self, 
                                       anomalies: List[Dict[str, Any]], 
                                       rule_evaluations: Dict[str, Any],
                                       context: Dict[str, Any]) -> ArchaeologicalExplanation:
        """
        Explicar anomalías desde perspectiva arqueológica.
        
        Args:
            anomalies: Lista de anomalías detectadas
            rule_evaluations: Evaluaciones de reglas arqueológicas
            context: Contexto geográfico y metodológico
            
        Returns:
            Explicación arqueológica estructurada
        """
        
        if not self.is_available:
            return self._fallback_explanation(anomalies, rule_evaluations, context)
        
        # Construir prompt específico
        prompt = self._build_archaeological_prompt(anomalies, rule_evaluations, context)
        
        try:
            # Llamar al modelo
            response = self._call_ai_model(prompt)
            
            # Parsear respuesta
            return self._parse_archaeological_response(response, anomalies, context)
            
        except Exception as e:
            logger.error(f"Error en explicación arqueológica: {e}")
            return self._fallback_explanation(anomalies, rule_evaluations, context)
    
    def _build_archaeological_prompt(self, 
                                   anomalies: List[Dict[str, Any]], 
                                   rule_evaluations: Dict[str, Any],
                                   context: Dict[str, Any]) -> str:
        """Construir prompt arqueológico específico."""
        
        # Información del contexto
        region_info = f"""
CONTEXTO REGIONAL:
- Región: {context.get('region_name', 'Desconocida')}
- Área: {context.get('area_km2', 0):,.0f} km²
- Coordenadas: {context.get('coordinates', 'No especificadas')}
- Tipo de paisaje: {context.get('landscape_type', 'Mixto')}
"""
        
        # Resumen de anomalías
        anomaly_summary = "ANOMALÍAS DETECTADAS:\n"
        for i, anomaly in enumerate(anomalies, 1):
            anomaly_summary += f"""
{i}. Tipo: {anomaly.get('type', 'Desconocido')}
   - Probabilidad arqueológica: {anomaly.get('archaeological_probability', 0):.2f}
   - Coherencia geométrica: {anomaly.get('geometric_coherence', 0):.2f}
   - Persistencia temporal: {anomaly.get('temporal_persistence', 0):.2f}
   - Píxeles afectados: {anomaly.get('affected_pixels', 0):,}
   - Características: {', '.join(anomaly.get('suspected_features', []))}
"""
        
        # Evaluaciones de reglas
        rules_summary = "EVALUACIONES DE REGLAS:\n"
        for rule_name, evaluation in rule_evaluations.items():
            if hasattr(evaluation, 'result'):
                rules_summary += f"""
- {rule_name}: {evaluation.result.value}
  Probabilidad arqueológica: {evaluation.archaeological_probability:.2f}
  Violaciones: {', '.join(evaluation.rule_violations) if evaluation.rule_violations else 'Ninguna'}
"""
        
        # Prompt completo
        full_prompt = f"""{self.base_prompt}

{region_info}

{anomaly_summary}

{rules_summary}

TAREA:
Analiza estos hallazgos desde una perspectiva arqueológica científica. Proporciona:

1. EXPLICACIÓN CLARA: ¿Qué patrones espaciales se detectaron?
2. INTERPRETACIÓN ARQUEOLÓGICA: ¿Qué podrían indicar estos patrones? (cauteloso)
3. RAZONAMIENTO CIENTÍFICO: ¿Por qué estos patrones son significativos?
4. EVALUACIÓN DE CONFIANZA: ¿Qué tan confiables son estas interpretaciones?
5. LIMITACIONES: ¿Qué no podemos concluir con certeza?
6. RECOMENDACIONES: ¿Qué investigación adicional se necesita?

Recuerda: Nunca afirmes descubrimientos definitivos. Usa lenguaje científico cauteloso."""
        
        return full_prompt
    
    def _call_ai_model(self, prompt: str) -> str:
        """Llamar al modelo de IA (OpenRouter primero, luego Ollama)."""
        
        # Prioridad 1: OpenRouter
        if self.openrouter_enabled and self.openrouter_api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.openrouter_model,
                    "messages": [
                        {
                            "role": "system", 
                            "content": "Eres un arqueólogo experto especializado en teledetección arqueológica. Proporciona análisis científicos rigurosos y explicaciones claras sobre anomalías espaciales."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "max_tokens": self.max_tokens,
                    "temperature": 0.3,  # Más determinista para análisis científico
                    "top_p": 0.9
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.ai_timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    logger.info(f"✅ Respuesta de OpenRouter ({self.openrouter_model})")
                    return content
                else:
                    logger.warning(f"OpenRouter error: {response.status_code}")
                    
            except Exception as e:
                logger.warning(f"Error con OpenRouter: {e}")
        
        # Prioridad 2: Ollama (fallback)
        if self.ollama_enabled:
            try:
                payload = {
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "num_predict": 1000
                    }
                }
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ Respuesta de Ollama ({self.ollama_model})")
                    return result.get('response', '')
                else:
                    raise Exception(f"Ollama error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                logger.warning(f"Error con Ollama: {e}")
        
        raise Exception("Ningún proveedor de IA disponible")
    
    def _parse_archaeological_response(self, 
                                     response: str, 
                                     anomalies: List[Dict[str, Any]], 
                                     context: Dict[str, Any]) -> ArchaeologicalExplanation:
        """Parsear respuesta del modelo en estructura arqueológica."""
        
        # Extraer secciones de la respuesta
        sections = self._extract_response_sections(response)
        
        # Generar recomendaciones específicas
        recommendations = self._generate_archaeological_recommendations(anomalies, context)
        
        return ArchaeologicalExplanation(
            explanation=sections.get('explanation', response[:500] + "..."),
            archaeological_interpretation=sections.get('interpretation', 
                "Análisis requiere datos adicionales para interpretación arqueológica definitiva."),
            confidence_assessment=sections.get('confidence', 
                "Confianza moderada - requiere validación con métodos adicionales."),
            methodological_notes=sections.get('methodology', 
                "Análisis basado en detección de anomalías espaciales multiespectrales."),
            recommendations=recommendations,
            limitations=sections.get('limitations', 
                "Interpretación basada en sensores remotos - requiere validación de campo."),
            scientific_reasoning=sections.get('reasoning', 
                "Patrones detectados muestran persistencia espacial y coherencia geométrica.")
        )
    
    def _extract_response_sections(self, response: str) -> Dict[str, str]:
        """Extraer secciones estructuradas de la respuesta."""
        
        sections = {}
        current_section = 'explanation'
        current_text = []
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Detectar nuevas secciones
            if any(keyword in line.lower() for keyword in ['interpretación', 'interpretation']):
                sections[current_section] = '\n'.join(current_text)
                current_section = 'interpretation'
                current_text = []
            elif any(keyword in line.lower() for keyword in ['confianza', 'confidence']):
                sections[current_section] = '\n'.join(current_text)
                current_section = 'confidence'
                current_text = []
            elif any(keyword in line.lower() for keyword in ['limitaciones', 'limitations']):
                sections[current_section] = '\n'.join(current_text)
                current_section = 'limitations'
                current_text = []
            elif any(keyword in line.lower() for keyword in ['razonamiento', 'reasoning']):
                sections[current_section] = '\n'.join(current_text)
                current_section = 'reasoning'
                current_text = []
            else:
                if line:  # Solo añadir líneas no vacías
                    current_text.append(line)
        
        # Añadir última sección
        sections[current_section] = '\n'.join(current_text)
        
        return sections
    
    def _generate_archaeological_recommendations(self, 
                                              anomalies: List[Dict[str, Any]], 
                                              context: Dict[str, Any]) -> List[str]:
        """Generar recomendaciones arqueológicas específicas."""
        
        recommendations = []
        
        # Recomendaciones basadas en tipos de anomalías
        has_vegetation_anomalies = any('vegetation' in str(a.get('type', '')) for a in anomalies)
        has_thermal_anomalies = any('thermal' in str(a.get('type', '')) for a in anomalies)
        has_geometric_patterns = any(a.get('geometric_coherence', 0) > 0.5 for a in anomalies)
        
        if has_vegetation_anomalies:
            recommendations.append(
                "Análisis multitemporal de índices de vegetación para confirmar persistencia de patrones"
            )
        
        if has_thermal_anomalies:
            recommendations.append(
                "Adquisición de datos térmicos nocturnos adicionales para validar inercia térmica diferencial"
            )
        
        if has_geometric_patterns:
            recommendations.append(
                "Investigación geofísica (GPR, magnetometría) para validar estructuras subsuperficiales"
            )
        
        # Recomendaciones generales
        recommendations.extend([
            "Análisis de contexto arqueológico regional para evaluar plausibilidad cultural",
            "Adquisición de datos de mayor resolución espacial para análisis detallado",
            "Correlación con bases de datos arqueológicas existentes"
        ])
        
        return recommendations
    
    def _fallback_explanation(self, 
                            anomalies: List[Dict[str, Any]], 
                            rule_evaluations: Dict[str, Any],
                            context: Dict[str, Any]) -> ArchaeologicalExplanation:
        """Generar explicación de respaldo cuando IA no está disponible."""
        
        # Análisis determinista básico
        total_anomalies = len(anomalies)
        high_prob_anomalies = sum(1 for a in anomalies if a.get('archaeological_probability', 0) > 0.6)
        
        if high_prob_anomalies > 0:
            explanation = (f"Se detectaron {total_anomalies} anomalías espaciales, "
                         f"de las cuales {high_prob_anomalies} muestran alta probabilidad "
                         f"de origen antrópico basado en criterios de persistencia espacial "
                         f"y coherencia geométrica.")
            
            interpretation = ("Las anomalías detectadas muestran patrones no explicables "
                            "completamente por procesos naturales actuales. La coherencia "
                            "geométrica y persistencia espacial sugieren posible intervención "
                            "humana antigua, aunque se requiere validación adicional.")
            
            confidence = "Confianza moderada basada en análisis determinista"
        else:
            explanation = (f"Se detectaron {total_anomalies} anomalías espaciales menores. "
                         f"Los patrones observados son consistentes con variabilidad natural "
                         f"o procesos geológicos/ecológicos actuales.")
            
            interpretation = ("Las anomalías detectadas no muestran características "
                            "distintivas de intervención humana antigua. Los patrones "
                            "son explicables por procesos naturales conocidos.")
            
            confidence = "Alta confianza en explicación por procesos naturales"
        
        return ArchaeologicalExplanation(
            explanation=explanation,
            archaeological_interpretation=interpretation,
            confidence_assessment=confidence,
            methodological_notes="Análisis determinista - IA no disponible",
            recommendations=[
                "Análisis con datos de mayor resolución",
                "Validación con métodos geofísicos",
                "Consulta con arqueólogos regionales"
            ],
            limitations="Análisis limitado por ausencia de IA especializada",
            scientific_reasoning="Basado en criterios de persistencia espacial y coherencia geométrica"
        )
    
    def explain_batch_archaeological_analysis(self, 
                                            spatial_anomalies: List[Dict[str, Any]], 
                                            rule_contradictions: List[Dict[str, Any]], 
                                            context: Dict[str, Any]) -> ArchaeologicalExplanation:
        """
        Explicar análisis arqueológico por lotes.
        
        Args:
            spatial_anomalies: Anomalías espaciales detectadas
            rule_contradictions: Contradicciones de reglas arqueológicas
            context: Contexto del análisis
            
        Returns:
            Explicación arqueológica integrada
        """
        
        # Combinar anomalías y contradicciones
        all_anomalies = spatial_anomalies + [
            {
                'type': f"rule_violation_{c.get('rule', 'unknown')}",
                'archaeological_probability': c.get('archaeological_probability', 0.5),
                'geometric_coherence': c.get('geometric_coherence', 0.0),
                'temporal_persistence': c.get('temporal_persistence', 0.0),
                'affected_pixels': c.get('pixels', 0),
                'suspected_features': [c.get('rule', 'unknown_violation')]
            }
            for c in rule_contradictions
        ]
        
        # Crear evaluaciones simuladas para compatibilidad
        mock_evaluations = {
            f"rule_{i}": type('MockEval', (), {
                'result': type('MockResult', (), {'value': 'anomalous'})(),
                'archaeological_probability': anomaly.get('archaeological_probability', 0.5),
                'rule_violations': anomaly.get('suspected_features', [])
            })()
            for i, anomaly in enumerate(all_anomalies)
        }
        
        return self.explain_archaeological_anomalies(all_anomalies, mock_evaluations, context)