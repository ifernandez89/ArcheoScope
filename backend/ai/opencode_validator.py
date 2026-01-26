#!/usr/bin/env python3
"""
OpenCode/Zen Validator - ArcheoScope

Validador lógico post-scoring usando OpenCode/Zen para:
- Validar coherencia de candidatos arqueológicos
- Generar explicaciones estructuradas y auditables
- Detectar inconsistencias en evidencia multi-instrumental
- Clasificar semánticamente patrones

FILOSOFÍA:
- Se ejecuta DESPUÉS del scoring determinista
- Es OPCIONAL y puede fallar sin afectar el análisis
- Nunca en loops críticos
- Siempre cacheable (determinista)
"""

import requests
import json
import hashlib
import logging
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

logger = logging.getLogger(__name__)

@dataclass
class OpenCodeValidation:
    """Resultado de validación OpenCode."""
    is_coherent: bool
    confidence_score: float
    validation_reasoning: str
    detected_inconsistencies: List[str]
    pattern_classification: Optional[str]
    recommended_actions: List[str]
    false_positive_risk: float
    timestamp: str

class OpenCodeValidator:
    """
    Validador cognitivo usando OpenCode/Zen.
    
    Arquitectura:
    [ Instrumentos ] → [ Scoring ] → [ OpenCode ] → [ Candidato validado ]
                                         ↑
                                    OPCIONAL
    """
    
    def __init__(self):
        """Inicializar validador OpenCode."""
        
        # Configuración desde .env
        self.enabled = os.getenv('OPENCODE_ENABLED', 'false').lower() == 'true'
        self.api_url = os.getenv('OPENCODE_API_URL', 'http://localhost:8080')
        self.timeout = int(os.getenv('OPENCODE_TIMEOUT', '30'))
        self.min_score = float(os.getenv('OPENCODE_MIN_SCORE', '0.75'))
        self.max_tokens = int(os.getenv('OPENCODE_MAX_TOKENS', '500'))
        
        # Caché en memoria
        self.cache = {}
        
        # Caché persistente
        self.cache_file = Path(__file__).parent.parent.parent / 'cache' / 'opencode_validations.json'
        self._load_cache()
        
        # Verificar disponibilidad
        self.is_available = self._check_availability()
        
        logger.info(f"OpenCodeValidator inicializado:")
        logger.info(f"  - Enabled: {'✅' if self.enabled else '❌'}")
        logger.info(f"  - API URL: {self.api_url}")
        logger.info(f"  - Min score: {self.min_score}")
        logger.info(f"  - Available: {'✅' if self.is_available else '❌'}")
        logger.info(f"  - Cache: {len(self.cache)} entradas")
    
    def _check_availability(self) -> bool:
        """Verificar si OpenCode está disponible."""
        
        if not self.enabled:
            logger.info("OpenCode deshabilitado en configuración")
            return False
        
        try:
            # Test simple de conectividad
            response = requests.get(
                f"{self.api_url}/health",
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info(f"✅ OpenCode disponible en {self.api_url}")
                return True
            else:
                logger.warning(f"⚠️ OpenCode respondió con status {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            logger.warning(f"⚠️ OpenCode no accesible en {self.api_url}")
            return False
        except requests.exceptions.Timeout:
            logger.warning(f"⚠️ OpenCode timeout en {self.api_url}")
            return False
        except Exception as e:
            logger.warning(f"⚠️ Error verificando OpenCode: {e}")
            return False
    
    def should_validate(self, candidate: Dict[str, Any]) -> bool:
        """
        Decidir si un candidato debe validarse con OpenCode.
        
        Criterios:
        - Score > threshold configurado
        - OpenCode habilitado y disponible
        - No está en caché
        """
        if not self.enabled or not self.is_available:
            return False
        
        score = candidate.get('archaeological_probability', 0.0)
        if score < self.min_score:
            return False
        
        # Verificar caché
        cache_key = self._hash_candidate(candidate)
        if cache_key in self.cache:
            logger.debug(f"Candidato ya validado (caché): {cache_key[:8]}")
            return False
        
        return True
    
    def validate_candidate(self, candidate: Dict[str, Any]) -> Optional[OpenCodeValidation]:
        """
        Validar coherencia lógica de un candidato arqueológico.
        
        Args:
            candidate: Candidato con scores e instrumentos
            
        Returns:
            Validación OpenCode o None si no aplica/falla
        """
        
        if not self.should_validate(candidate):
            return None
        
        # Verificar caché primero
        cache_key = self._hash_candidate(candidate)
        if cache_key in self.cache:
            logger.info(f"✅ Validación desde caché: {cache_key[:8]}")
            return self._deserialize_validation(self.cache[cache_key])
        
        try:
            logger.info(f"🧠 Validando candidato con OpenCode...")
            
            # Preparar datos para OpenCode
            validation_data = self._prepare_validation_data(candidate)
            
            # Llamar a OpenCode
            result = self._call_opencode(
                task="validate_coherence",
                data=validation_data
            )
            
            # Parsear resultado
            validation = self._parse_validation_result(result, candidate)
            
            # Guardar en caché
            self.cache[cache_key] = self._serialize_validation(validation)
            self._save_cache()
            
            logger.info(f"✅ Validación completada: coherente={'✅' if validation.is_coherent else '❌'}")
            
            return validation
            
        except Exception as e:
            logger.error(f"❌ Error en validación OpenCode: {e}")
            return None
    
    def explain_evidence(self, candidate: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generar explicación estructurada de evidencia arqueológica.
        
        Args:
            candidate: Candidato completo
            
        Returns:
            Explicación estructurada o None si falla
        """
        
        if not self.enabled or not self.is_available:
            return None
        
        try:
            logger.info(f"📝 Generando explicación con OpenCode...")
            
            # Preparar datos
            explanation_data = self._prepare_explanation_data(candidate)
            
            # Llamar a OpenCode
            result = self._call_opencode(
                task="explain_archaeological",
                data=explanation_data
            )
            
            logger.info(f"✅ Explicación generada")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error generando explicación: {e}")
            return None
    
    def classify_pattern(self, candidate: Dict[str, Any]) -> Optional[str]:
        """
        Clasificar tipo de patrón arqueológico.
        
        Args:
            candidate: Candidato con patrón espacial
            
        Returns:
            Tipo de patrón (asentamiento/camino/estructura/etc) o None
        """
        
        if not self.enabled or not self.is_available:
            return None
        
        try:
            logger.info(f"🔍 Clasificando patrón con OpenCode...")
            
            # Preparar datos
            pattern_data = self._prepare_pattern_data(candidate)
            
            # Llamar a OpenCode
            result = self._call_opencode(
                task="classify_pattern",
                data=pattern_data
            )
            
            pattern_type = result.get('pattern_type', 'unknown')
            logger.info(f"✅ Patrón clasificado: {pattern_type}")
            
            return pattern_type
            
        except Exception as e:
            logger.error(f"❌ Error clasificando patrón: {e}")
            return None
    
    def _call_opencode(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Llamar a OpenCode API.
        
        Args:
            task: Tipo de tarea (validate_coherence/explain_archaeological/classify_pattern)
            data: Datos para análisis
            
        Returns:
            Resultado de OpenCode
        """
        
        payload = {
            "task": task,
            "data": data,
            "max_tokens": self.max_tokens,
            "temperature": 0.1  # Muy determinista
        }
        
        response = requests.post(
            f"{self.api_url}/analyze",
            json=payload,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenCode error: HTTP {response.status_code}")
        
        return response.json()
    
    def _prepare_validation_data(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Preparar datos para validación de coherencia."""
        
        return {
            "score": candidate.get('archaeological_probability', 0.0),
            "instruments": [
                {
                    "type": inst.get('type', 'unknown'),
                    "value": inst.get('value', 0.0),
                    "confidence": inst.get('confidence', 'unknown')
                }
                for inst in candidate.get('evidence_layers', [])
            ],
            "convergence": candidate.get('instruments_converging', 0),
            "environment": candidate.get('environment_type', 'unknown'),
            "temporal_data": candidate.get('temporal_persistence', {})
        }
    
    def _prepare_explanation_data(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Preparar datos para explicación."""
        
        return {
            "candidate_id": candidate.get('id', 'unknown'),
            "region": candidate.get('region_name', 'unknown'),
            "score": candidate.get('archaeological_probability', 0.0),
            "evidence": candidate.get('evidence_layers', []),
            "context": candidate.get('spatial_context', {})
        }
    
    def _prepare_pattern_data(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Preparar datos para clasificación de patrón."""
        
        return {
            "geometry": candidate.get('geometric_coherence', 0.0),
            "spatial_extent": candidate.get('spatial_context', {}),
            "instruments": [inst.get('type') for inst in candidate.get('evidence_layers', [])]
        }
    
    def _parse_validation_result(self, result: Dict[str, Any], candidate: Dict[str, Any]) -> OpenCodeValidation:
        """Parsear resultado de validación OpenCode."""
        
        return OpenCodeValidation(
            is_coherent=result.get('is_coherent', True),
            confidence_score=result.get('confidence', 0.5),
            validation_reasoning=result.get('reasoning', 'No reasoning provided'),
            detected_inconsistencies=result.get('inconsistencies', []),
            pattern_classification=result.get('pattern_type'),
            recommended_actions=result.get('recommendations', []),
            false_positive_risk=result.get('false_positive_risk', 0.5),
            timestamp=datetime.now().isoformat()
        )
    
    def _hash_candidate(self, candidate: Dict[str, Any]) -> str:
        """Generar hash determinista del candidato para caché."""
        
        key_data = {
            "coords": candidate.get('spatial_context', {}),
            "score": round(candidate.get('archaeological_probability', 0.0), 3),
            "instruments": sorted([
                inst.get('type', 'unknown') 
                for inst in candidate.get('evidence_layers', [])
            ])
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def _serialize_validation(self, validation: OpenCodeValidation) -> Dict[str, Any]:
        """Serializar validación para caché."""
        
        return {
            "is_coherent": validation.is_coherent,
            "confidence_score": validation.confidence_score,
            "validation_reasoning": validation.validation_reasoning,
            "detected_inconsistencies": validation.detected_inconsistencies,
            "pattern_classification": validation.pattern_classification,
            "recommended_actions": validation.recommended_actions,
            "false_positive_risk": validation.false_positive_risk,
            "timestamp": validation.timestamp
        }
    
    def _deserialize_validation(self, data: Dict[str, Any]) -> OpenCodeValidation:
        """Deserializar validación desde caché."""
        
        return OpenCodeValidation(**data)
    
    def _load_cache(self):
        """Cargar caché desde disco."""
        
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
                logger.info(f"✅ Caché cargado: {len(self.cache)} entradas")
            except Exception as e:
                logger.warning(f"⚠️ Error cargando caché: {e}")
                self.cache = {}
        else:
            self.cache = {}
    
    def _save_cache(self):
        """Guardar caché a disco."""
        
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
            logger.debug(f"💾 Caché guardado: {len(self.cache)} entradas")
        except Exception as e:
            logger.warning(f"⚠️ Error guardando caché: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de caché."""
        
        return {
            "total_entries": len(self.cache),
            "cache_file": str(self.cache_file),
            "cache_exists": self.cache_file.exists(),
            "enabled": self.enabled,
            "available": self.is_available
        }
