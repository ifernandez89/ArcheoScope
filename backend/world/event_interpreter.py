"""
EventInterpreter - Convierte output HRM en eventos estructurados

Traduce análisis abstracto del HRM en eventos concretos del mundo
que pueden ser aplicados y narrados.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """Tipos de eventos emergentes"""
    ELECTROMAGNETIC_STORM = "electromagnetic_storm"
    REALITY_FRACTURE = "reality_fracture"
    TEMPORAL_ANOMALY = "temporal_anomaly"
    ENERGY_SURGE = "energy_surge"
    CHAOS_WAVE = "chaos_wave"
    DIMENSIONAL_SHIFT = "dimensional_shift"
    MINOR_DISTURBANCE = "minor_disturbance"
    SEISMIC_ACTIVITY = "seismic_activity"
    ATMOSPHERIC_DISTORTION = "atmospheric_distortion"
    GRAVITATIONAL_ANOMALY = "gravitational_anomaly"


class EventSeverity(Enum):
    """Severidad del evento"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"


@dataclass
class EventEffect:
    """Efecto específico de un evento"""
    type: str  # 'climate', 'visual', 'audio', 'physics'
    parameter: str  # Parámetro a modificar
    value: float  # Valor del efecto
    duration: float  # Duración en segundos


@dataclass
class Event:
    """Evento emergente estructurado"""
    type: EventType
    severity: EventSeverity
    intensity: float  # 0-1
    confidence: float  # 0-1
    affected_zones: List[int]
    affected_regions: List[str]
    duration: float  # segundos
    effects: List[EventEffect]
    narrative_seed: Dict[str, any]
    propagation: Dict[str, any]
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para serialización"""
        return {
            "type": self.type.value,
            "severity": self.severity.value,
            "intensity": self.intensity,
            "confidence": self.confidence,
            "affected_zones": self.affected_zones,
            "affected_regions": self.affected_regions,
            "duration": self.duration,
            "effects": [
                {
                    "type": e.type,
                    "parameter": e.parameter,
                    "value": e.value,
                    "duration": e.duration
                }
                for e in self.effects
            ],
            "narrative_seed": self.narrative_seed,
            "propagation": self.propagation
        }


class EventInterpreter:
    """
    Interpreta output del HRM y genera eventos estructurados
    
    Convierte análisis abstracto en eventos concretos con:
    - Tipo y severidad
    - Efectos específicos (clima, visual, audio, física)
    - Duración y propagación
    - Seed para narrativa
    """
    
    def __init__(self):
        # Mapeo de eventos a efectos
        self.event_effects_map = self._build_effects_map()
        
    def interpret(self, hrm_output: Dict) -> Event:
        """
        Interpreta output del HRM y genera evento
        
        Args:
            hrm_output: Análisis del HRM
            
        Returns:
            Event estructurado
        """
        # Extraer datos del análisis
        event_type_str = hrm_output["emergent_event"]
        instability = hrm_output["instability_level"]
        confidence = hrm_output["confidence"]
        affected_zones = hrm_output["affected_zones"]
        propagation = hrm_output["propagation_vector"]
        
        # Mapear tipo de evento
        event_type = self._map_event_type(event_type_str, instability)
        
        # Calcular severidad
        severity = self._calculate_severity(instability, len(affected_zones))
        
        # Calcular duración
        duration = self._calculate_duration(instability, severity)
        
        # Generar efectos
        effects = self._generate_effects(event_type, instability, duration)
        
        # Obtener regiones afectadas
        affected_regions = self._get_affected_regions(affected_zones)
        
        # Crear seed para narrativa
        narrative_seed = self._create_narrative_seed(
            event_type, 
            severity, 
            affected_regions, 
            propagation
        )
        
        return Event(
            type=event_type,
            severity=severity,
            intensity=instability,
            confidence=confidence,
            affected_zones=affected_zones,
            affected_regions=affected_regions,
            duration=duration,
            effects=effects,
            narrative_seed=narrative_seed,
            propagation=propagation
        )
    
    def _map_event_type(self, event_str: str, instability: float) -> EventType:
        """
        Mapea string de evento a EventType
        """
        mapping = {
            "electromagnetic_storm": EventType.ELECTROMAGNETIC_STORM,
            "reality_fracture": EventType.REALITY_FRACTURE,
            "temporal_anomaly": EventType.TEMPORAL_ANOMALY,
            "energy_surge": EventType.ENERGY_SURGE,
            "chaos_wave": EventType.CHAOS_WAVE,
            "dimensional_shift": EventType.DIMENSIONAL_SHIFT,
            "minor_disturbance": EventType.MINOR_DISTURBANCE
        }
        
        # Agregar variaciones según instabilidad
        if instability > 0.9:
            # Eventos más extremos
            if "storm" in event_str:
                return EventType.ELECTROMAGNETIC_STORM
            elif "fracture" in event_str:
                return EventType.REALITY_FRACTURE
        
        return mapping.get(event_str, EventType.MINOR_DISTURBANCE)
    
    def _calculate_severity(self, instability: float, num_zones: int) -> EventSeverity:
        """
        Calcula severidad del evento
        
        Basado en:
        - Nivel de inestabilidad
        - Número de zonas afectadas
        """
        # Score combinado
        zone_factor = min(1.0, num_zones / 32.0)
        severity_score = (instability * 0.7 + zone_factor * 0.3)
        
        # Clasificar
        if severity_score < 0.2:
            return EventSeverity.MINOR
        elif severity_score < 0.4:
            return EventSeverity.MODERATE
        elif severity_score < 0.6:
            return EventSeverity.MAJOR
        elif severity_score < 0.8:
            return EventSeverity.CRITICAL
        else:
            return EventSeverity.CATASTROPHIC
    
    def _calculate_duration(self, instability: float, severity: EventSeverity) -> float:
        """
        Calcula duración del evento en segundos
        """
        # Duración base según severidad
        base_durations = {
            EventSeverity.MINOR: 30,
            EventSeverity.MODERATE: 60,
            EventSeverity.MAJOR: 120,
            EventSeverity.CRITICAL: 180,
            EventSeverity.CATASTROPHIC: 300
        }
        
        base = base_durations[severity]
        
        # Modificar según instabilidad
        duration = base * (0.5 + instability)
        
        return float(duration)
    
    def _generate_effects(
        self, 
        event_type: EventType, 
        intensity: float, 
        duration: float
    ) -> List[EventEffect]:
        """
        Genera efectos específicos del evento
        """
        effects = []
        
        # Obtener template de efectos
        template = self.event_effects_map.get(event_type, [])
        
        # Generar efectos con intensidad
        for effect_template in template:
            effect = EventEffect(
                type=effect_template["type"],
                parameter=effect_template["parameter"],
                value=effect_template["base_value"] * intensity,
                duration=duration * effect_template.get("duration_factor", 1.0)
            )
            effects.append(effect)
        
        return effects
    
    def _build_effects_map(self) -> Dict[EventType, List[Dict]]:
        """
        Construye mapeo de eventos a efectos
        """
        return {
            EventType.ELECTROMAGNETIC_STORM: [
                {
                    "type": "climate",
                    "parameter": "storm_intensity",
                    "base_value": 1.0,
                    "duration_factor": 1.0
                },
                {
                    "type": "visual",
                    "parameter": "lightning_frequency",
                    "base_value": 0.8,
                    "duration_factor": 1.0
                },
                {
                    "type": "audio",
                    "parameter": "thunder_volume",
                    "base_value": 0.7,
                    "duration_factor": 1.0
                },
                {
                    "type": "visual",
                    "parameter": "sky_darkness",
                    "base_value": 0.6,
                    "duration_factor": 1.0
                }
            ],
            EventType.REALITY_FRACTURE: [
                {
                    "type": "visual",
                    "parameter": "distortion_intensity",
                    "base_value": 0.9,
                    "duration_factor": 0.8
                },
                {
                    "type": "physics",
                    "parameter": "gravity_fluctuation",
                    "base_value": 0.3,
                    "duration_factor": 0.5
                },
                {
                    "type": "audio",
                    "parameter": "reality_hum",
                    "base_value": 0.6,
                    "duration_factor": 1.0
                }
            ],
            EventType.TEMPORAL_ANOMALY: [
                {
                    "type": "physics",
                    "parameter": "time_dilation",
                    "base_value": 0.5,
                    "duration_factor": 0.7
                },
                {
                    "type": "visual",
                    "parameter": "temporal_blur",
                    "base_value": 0.4,
                    "duration_factor": 1.0
                },
                {
                    "type": "audio",
                    "parameter": "time_echo",
                    "base_value": 0.5,
                    "duration_factor": 1.0
                }
            ],
            EventType.ENERGY_SURGE: [
                {
                    "type": "visual",
                    "parameter": "energy_glow",
                    "base_value": 0.8,
                    "duration_factor": 0.5
                },
                {
                    "type": "physics",
                    "parameter": "electromagnetic_field",
                    "base_value": 0.6,
                    "duration_factor": 0.8
                },
                {
                    "type": "audio",
                    "parameter": "energy_hum",
                    "base_value": 0.5,
                    "duration_factor": 1.0
                }
            ],
            EventType.CHAOS_WAVE: [
                {
                    "type": "climate",
                    "parameter": "wind_intensity",
                    "base_value": 0.9,
                    "duration_factor": 1.0
                },
                {
                    "type": "visual",
                    "parameter": "particle_chaos",
                    "base_value": 0.7,
                    "duration_factor": 1.0
                },
                {
                    "type": "physics",
                    "parameter": "turbulence",
                    "base_value": 0.6,
                    "duration_factor": 1.0
                }
            ],
            EventType.DIMENSIONAL_SHIFT: [
                {
                    "type": "visual",
                    "parameter": "dimensional_rift",
                    "base_value": 1.0,
                    "duration_factor": 0.6
                },
                {
                    "type": "physics",
                    "parameter": "spatial_distortion",
                    "base_value": 0.7,
                    "duration_factor": 0.8
                },
                {
                    "type": "audio",
                    "parameter": "dimensional_tear",
                    "base_value": 0.8,
                    "duration_factor": 0.5
                }
            ],
            EventType.MINOR_DISTURBANCE: [
                {
                    "type": "climate",
                    "parameter": "wind_gust",
                    "base_value": 0.3,
                    "duration_factor": 0.5
                },
                {
                    "type": "visual",
                    "parameter": "dust_particles",
                    "base_value": 0.2,
                    "duration_factor": 0.8
                }
            ]
        }
    
    def _get_affected_regions(self, zone_ids: List[int]) -> List[str]:
        """
        Obtiene nombres de regiones afectadas
        """
        regions = set()
        
        for zone_id in zone_ids:
            if 0 <= zone_id <= 7:
                regions.add("norte")
            elif 8 <= zone_id <= 15:
                regions.add("este")
            elif 16 <= zone_id <= 23:
                regions.add("sur")
            elif 24 <= zone_id <= 31:
                regions.add("oeste")
            elif 32 <= zone_id <= 39:
                regions.add("central")
            elif 40 <= zone_id <= 47:
                regions.add("subterranea")
            elif 48 <= zone_id <= 55:
                regions.add("atmosferica")
            elif 56 <= zone_id <= 63:
                regions.add("temporal")
        
        return list(regions)
    
    def _create_narrative_seed(
        self,
        event_type: EventType,
        severity: EventSeverity,
        regions: List[str],
        propagation: Dict
    ) -> Dict:
        """
        Crea seed para generación de narrativa
        
        Información mínima para que el LLM genere texto
        """
        # Descripción corta del evento
        event_descriptions = {
            EventType.ELECTROMAGNETIC_STORM: "tormenta electromagnética",
            EventType.REALITY_FRACTURE: "fractura en la realidad",
            EventType.TEMPORAL_ANOMALY: "anomalía temporal",
            EventType.ENERGY_SURGE: "oleada de energía",
            EventType.CHAOS_WAVE: "onda de caos",
            EventType.DIMENSIONAL_SHIFT: "cambio dimensional",
            EventType.MINOR_DISTURBANCE: "perturbación menor"
        }
        
        # Sensaciones según severidad
        severity_sensations = {
            EventSeverity.MINOR: "una leve sensación extraña",
            EventSeverity.MODERATE: "una perturbación notable",
            EventSeverity.MAJOR: "una fuerza intensa",
            EventSeverity.CRITICAL: "una energía abrumadora",
            EventSeverity.CATASTROPHIC: "un poder devastador"
        }
        
        # Dirección de propagación
        direction_texts = {
            "norte": "desde el norte",
            "este": "desde el este",
            "sur": "desde el sur",
            "oeste": "desde el oeste",
            "central": "desde el centro",
            "atmosferica": "desde arriba",
            "subterranea": "desde abajo",
            "temporal": "desde otra dimensión"
        }
        
        return {
            "event": event_descriptions.get(event_type, "evento desconocido"),
            "severity_text": severity.value,
            "sensation": severity_sensations.get(severity, "algo extraño"),
            "region": regions[0] if regions else "desconocida",
            "direction": direction_texts.get(propagation.get("direction", ""), "de ninguna parte"),
            "intensity_text": self._intensity_to_text(propagation.get("intensity", 0.5)),
            "speed_text": self._speed_to_text(propagation.get("speed", 0.5))
        }
    
    def _intensity_to_text(self, intensity: float) -> str:
        """Convierte intensidad a texto"""
        if intensity < 0.3:
            return "débil"
        elif intensity < 0.6:
            return "moderada"
        elif intensity < 0.8:
            return "fuerte"
        else:
            return "extrema"
    
    def _speed_to_text(self, speed: float) -> str:
        """Convierte velocidad a texto"""
        if speed < 0.3:
            return "lentamente"
        elif speed < 0.6:
            return "a velocidad moderada"
        else:
            return "rápidamente"
