#!/usr/bin/env python3
"""
Sistema de Calibración Científica - ArcheoScope
===============================================

Sistema de calibración con controles negativos y positivos.

FILOSOFÍA:
- No empezar por lo "interesante"
- Empezar por lugares que fijan la escala
- Calibrar honestidad, no hallazgos

CONTROLES:
1. PISO (control negativo) - Debe dar bajo
2. TECHO (control positivo) - Debe dar alto
3. INTERMEDIO (validación) - Debe distinguir
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ControlType(Enum):
    """Tipos de control de calibración."""
    NEGATIVE = "negative"      # Piso - debe dar bajo
    POSITIVE = "positive"      # Techo - debe dar alto
    VALIDATION = "validation"  # Intermedio - debe distinguir


class AnalysisMode(Enum):
    """Modos de análisis."""
    HYPOTHESIS_DRIVEN = "hypothesis_driven"
    EXPLORATORY = "exploratory"
    VALIDATION = "validation"


class AnalysisObjective(Enum):
    """Objetivos de análisis."""
    CALIBRATION = "calibration"      # Optimiza honestidad
    DISCOVERY = "discovery"          # Optimiza hallazgos
    MONITORING = "monitoring"        # Optimiza cambios


class AnalysisDepth(Enum):
    """Profundidad de análisis."""
    SURFACE = "surface"
    MULTILAYER = "multilayer"
    DEEP = "deep"


class TemporalWindowType(Enum):
    """Tipo de ventana temporal."""
    SHORT = "short"    # 2-3 años
    MEDIUM = "medium"  # 3-5 años
    LONG = "long"      # 5+ años


class SpatialWindowType(Enum):
    """Tipo de ventana espacial."""
    POINT = "point"      # < 1 km
    LOCAL = "local"      # 1-5 km
    BBOX = "bbox"        # 5-20 km
    REGIONAL = "regional" # > 20 km


class InstrumentPolicy(Enum):
    """Política de instrumentos."""
    MAX_AVAILABLE = "max_available"  # Todos los disponibles
    CORE_ONLY = "core_only"          # Solo núcleo (Sentinel-2, Landsat, SAR)
    MINIMAL = "minimal"              # Mínimo viable


class NormalizationType(Enum):
    """Tipo de normalización."""
    ROBUST = "robust"      # Robusta (mediana, IQR)
    STANDARD = "standard"  # Estándar (media, std)
    MINMAX = "minmax"      # Min-Max


class ESSMode(Enum):
    """Modo de cálculo ESS."""
    CONSERVATIVE = "conservative"  # Conservador (evita falsos positivos)
    BALANCED = "balanced"          # Balanceado
    SENSITIVE = "sensitive"        # Sensible (detecta señales débiles)


@dataclass
class TemporalWindow:
    """Ventana temporal de análisis."""
    type: TemporalWindowType
    years: int


@dataclass
class SpatialWindow:
    """Ventana espacial de análisis."""
    type: SpatialWindowType
    size_km: float


@dataclass
class AnomalyDetectionConfig:
    """Configuración de detección de anomalías."""
    enabled: bool
    sensitivity: str  # "low", "medium", "high"


@dataclass
class CalibrationRequest:
    """Solicitud de calibración canónica."""
    
    # Parámetros principales
    mode: AnalysisMode
    objective: AnalysisObjective
    analysis_depth: AnalysisDepth
    
    # Ventanas
    temporal_window: TemporalWindow
    spatial_window: SpatialWindow
    
    # Configuración técnica
    resolution_m: float
    instrument_policy: InstrumentPolicy
    normalization: NormalizationType
    ess_mode: ESSMode
    
    # Detección de anomalías
    anomaly_detection: AnomalyDetectionConfig
    
    @classmethod
    def create_canonical(cls) -> 'CalibrationRequest':
        """
        Crear solicitud canónica de calibración.
        
        PLANTILLA CANÓNICA - NO ADAPTAR
        """
        return cls(
            mode=AnalysisMode.HYPOTHESIS_DRIVEN,
            objective=AnalysisObjective.CALIBRATION,
            analysis_depth=AnalysisDepth.MULTILAYER,
            temporal_window=TemporalWindow(
                type=TemporalWindowType.LONG,
                years=5
            ),
            spatial_window=SpatialWindow(
                type=SpatialWindowType.BBOX,
                size_km=15.0
            ),
            resolution_m=150.0,
            instrument_policy=InstrumentPolicy.MAX_AVAILABLE,
            normalization=NormalizationType.ROBUST,
            ess_mode=ESSMode.CONSERVATIVE,
            anomaly_detection=AnomalyDetectionConfig(
                enabled=True,
                sensitivity="low"
            )
        )
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario."""
        return {
            "mode": self.mode.value,
            "objective": self.objective.value,
            "analysis_depth": self.analysis_depth.value,
            "temporal_window": {
                "type": self.temporal_window.type.value,
                "years": self.temporal_window.years
            },
            "spatial_window": {
                "type": self.spatial_window.type.value,
                "size_km": self.spatial_window.size_km
            },
            "resolution_m": self.resolution_m,
            "instrument_policy": self.instrument_policy.value,
            "normalization": self.normalization.value,
            "ess_mode": self.ess_mode.value,
            "anomaly_detection": {
                "enabled": self.anomaly_detection.enabled,
                "sensitivity": self.anomaly_detection.sensitivity
            }
        }


@dataclass
class CalibrationSite:
    """Sitio de calibración."""
    
    site_id: str
    name: str
    control_type: ControlType
    
    # Coordenadas
    lat: float
    lon: float
    
    # Contexto
    geological_context: str
    archaeological_context: str
    why_chosen: str
    
    # Expectativas
    expected_ess_vol: Tuple[float, float]  # (min, max)
    expected_ess_temp: Tuple[float, float]
    expected_coherence: Tuple[float, float]
    
    # Justificación
    justification: str


# ============================================================================
# CATÁLOGO DE SITIOS DE CALIBRACIÓN
# ============================================================================

CALIBRATION_SITES = {
    
    # ========================================================================
    # A. PISO (Control Negativo)
    # ========================================================================
    
    "pampa_argentina": CalibrationSite(
        site_id="neg_001",
        name="Pampa Argentina - Control Negativo",
        control_type=ControlType.NEGATIVE,
        lat=-35.150,
        lon=-61.800,
        geological_context="Planicie sedimentaria homogénea. Loess cuaternario.",
        archaeological_context="Uso agrícola continuo. Sin evidencia arqueológica profunda.",
        why_chosen="Geología homogénea + uso agrícola continuo + sin memoria enterrada",
        expected_ess_vol=(0.0, 0.30),
        expected_ess_temp=(0.0, 0.30),
        expected_coherence=(0.65, 1.0),
        justification="Si acá da anomalías → algo está mal. Debe ser PISO."
    ),
    
    "gran_llanura_usa": CalibrationSite(
        site_id="neg_002",
        name="Gran Llanura USA - Control Negativo",
        control_type=ControlType.NEGATIVE,
        lat=40.0,
        lon=-100.0,
        geological_context="Planicie aluvial estable. Sedimentos recientes.",
        archaeological_context="Agricultura intensiva moderna. Sin ocupación prehispánica significativa.",
        why_chosen="Planicie estable + agricultura moderna + sin historia profunda",
        expected_ess_vol=(0.0, 0.25),
        expected_ess_temp=(0.0, 0.25),
        expected_coherence=(0.70, 1.0),
        justification="Control negativo secundario. Debe confirmar PISO."
    ),
    
    # ========================================================================
    # B. TECHO (Control Positivo)
    # ========================================================================
    
    "giza_egipto": CalibrationSite(
        site_id="pos_001",
        name="Giza - Control Positivo",
        control_type=ControlType.POSITIVE,
        lat=29.9792,
        lon=31.1342,
        geological_context="Meseta calcárea. Roca madre estable.",
        archaeological_context="Pirámides de Giza. Estructuras masivas conocidas.",
        why_chosen="Estructuras masivas conocidas + contraste brutal + preservación perfecta",
        expected_ess_vol=(0.70, 0.90),
        expected_ess_temp=(0.65, 0.85),
        expected_coherence=(0.40, 0.60),
        justification="Si acá NO da alto → sistema no detecta. Debe ser TECHO."
    ),
    
    "machu_picchu": CalibrationSite(
        site_id="pos_002",
        name="Machu Picchu - Control Positivo",
        control_type=ControlType.POSITIVE,
        lat=-13.1631,
        lon=-72.5450,
        geological_context="Montaña granítica. Terraza artificial.",
        archaeological_context="Ciudad inca conocida. Estructuras de piedra masivas.",
        why_chosen="Estructuras conocidas + terraza artificial + contraste topográfico",
        expected_ess_vol=(0.65, 0.85),
        expected_ess_temp=(0.60, 0.80),
        expected_coherence=(0.35, 0.55),
        justification="Control positivo secundario. Debe confirmar TECHO."
    ),
    
    # ========================================================================
    # C. INTERMEDIO (Validación)
    # ========================================================================
    
    "veracruz_laguna": CalibrationSite(
        site_id="val_001",
        name="Veracruz Laguna - Validación",
        control_type=ControlType.VALIDATION,
        lat=20.58,
        lon=-96.92,
        geological_context="Laguna costera colmatada. Sedimentos recientes.",
        archaeological_context="Zona de transición. Posible ocupación costera prehispánica.",
        why_chosen="Transición agua/tierra + contraste moderado + señal real",
        expected_ess_vol=(0.40, 0.55),
        expected_ess_temp=(0.40, 0.55),
        expected_coherence=(0.50, 0.65),
        justification="Debe distinguir entre PISO y TECHO. Señal moderada real."
    ),
    
    "altiplano_andino": CalibrationSite(
        site_id="val_002",
        name="Altiplano Andino - Validación",
        control_type=ControlType.VALIDATION,
        lat=-16.5,
        lon=-68.7,
        geological_context="Altiplano volcánico. Terrazas agrícolas.",
        archaeological_context="Zona Tiwanaku. Terrazas y sistemas hidráulicos.",
        why_chosen="Terrazas agrícolas + sistemas hidráulicos + señal moderada-alta",
        expected_ess_vol=(0.50, 0.65),
        expected_ess_temp=(0.45, 0.60),
        expected_coherence=(0.45, 0.60),
        justification="Debe detectar estructuras agrícolas. Señal moderada-alta."
    )
}


class CalibrationSystem:
    """Sistema de calibración científica."""
    
    def __init__(self):
        """Inicializar sistema de calibración."""
        self.canonical_request = CalibrationRequest.create_canonical()
        logger.info("🎯 CalibrationSystem inicializado")
        logger.info("   📊 Modo: Calibración científica")
        logger.info("   🎯 Objetivo: Honestidad, no hallazgos")
    
    def get_canonical_request(self) -> CalibrationRequest:
        """Obtener solicitud canónica de calibración."""
        return self.canonical_request
    
    def get_calibration_site(self, site_id: str) -> CalibrationSite:
        """Obtener sitio de calibración."""
        for site in CALIBRATION_SITES.values():
            if site.site_id == site_id:
                return site
        raise ValueError(f"Sitio '{site_id}' no encontrado")
    
    def list_calibration_sites(self, control_type: Optional[ControlType] = None) -> List[CalibrationSite]:
        """Listar sitios de calibración."""
        sites = list(CALIBRATION_SITES.values())
        if control_type:
            sites = [s for s in sites if s.control_type == control_type]
        return sites
    
    def validate_result(self, site: CalibrationSite, ess_vol: float, 
                       ess_temp: float, coherence: float) -> Dict:
        """
        Validar resultado contra expectativas.
        
        Args:
            site: Sitio de calibración
            ess_vol: ESS volumétrico obtenido
            ess_temp: ESS temporal obtenido
            coherence: Coherencia obtenida
            
        Returns:
            Diccionario con validación
        """
        
        # Validar ESS volumétrico
        ess_vol_ok = site.expected_ess_vol[0] <= ess_vol <= site.expected_ess_vol[1]
        
        # Validar ESS temporal
        ess_temp_ok = site.expected_ess_temp[0] <= ess_temp <= site.expected_ess_temp[1]
        
        # Validar coherencia
        coherence_ok = site.expected_coherence[0] <= coherence <= site.expected_coherence[1]
        
        # Resultado general
        all_ok = ess_vol_ok and ess_temp_ok and coherence_ok
        
        # Interpretación
        if site.control_type == ControlType.NEGATIVE:
            if all_ok:
                interpretation = "✅ PISO CORRECTO - Sistema no inventa anomalías"
            else:
                interpretation = "❌ PISO INCORRECTO - Sistema inventa anomalías donde no hay"
        
        elif site.control_type == ControlType.POSITIVE:
            if all_ok:
                interpretation = "✅ TECHO CORRECTO - Sistema detecta estructuras conocidas"
            else:
                interpretation = "❌ TECHO INCORRECTO - Sistema no detecta estructuras conocidas"
        
        else:  # VALIDATION
            if all_ok:
                interpretation = "✅ VALIDACIÓN CORRECTA - Sistema distingue señal moderada"
            else:
                interpretation = "⚠️ VALIDACIÓN FUERA DE RANGO - Revisar calibración"
        
        return {
            "site_id": site.site_id,
            "site_name": site.name,
            "control_type": site.control_type.value,
            "validation": {
                "ess_volumetrico": {
                    "obtained": ess_vol,
                    "expected": site.expected_ess_vol,
                    "ok": ess_vol_ok
                },
                "ess_temporal": {
                    "obtained": ess_temp,
                    "expected": site.expected_ess_temp,
                    "ok": ess_temp_ok
                },
                "coherencia": {
                    "obtained": coherence,
                    "expected": site.expected_coherence,
                    "ok": coherence_ok
                }
            },
            "all_ok": all_ok,
            "interpretation": interpretation
        }
    
    def print_calibration_protocol(self):
        """Imprimir protocolo de calibración."""
        print("="*80)
        print("🎯 PROTOCOLO DE CALIBRACIÓN CIENTÍFICA - ArcheoScope")
        print("="*80)
        print()
        
        print("📋 SOLICITUD CANÓNICA:")
        print("-"*80)
        request_dict = self.canonical_request.to_dict()
        for key, value in request_dict.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")
        print()
        
        print("📍 SITIOS DE CALIBRACIÓN:")
        print("-"*80)
        
        # Controles negativos
        print("\n🟢 A. PISO (Control Negativo) - Debe dar BAJO")
        for site in self.list_calibration_sites(ControlType.NEGATIVE):
            print(f"\n  📍 {site.name}")
            print(f"     Coords: {site.lat:.4f}, {site.lon:.4f}")
            print(f"     Por qué: {site.why_chosen}")
            print(f"     Esperado ESS Vol: {site.expected_ess_vol[0]:.2f}-{site.expected_ess_vol[1]:.2f}")
            print(f"     Justificación: {site.justification}")
        
        # Controles positivos
        print("\n🔴 B. TECHO (Control Positivo) - Debe dar ALTO")
        for site in self.list_calibration_sites(ControlType.POSITIVE):
            print(f"\n  📍 {site.name}")
            print(f"     Coords: {site.lat:.4f}, {site.lon:.4f}")
            print(f"     Por qué: {site.why_chosen}")
            print(f"     Esperado ESS Vol: {site.expected_ess_vol[0]:.2f}-{site.expected_ess_vol[1]:.2f}")
            print(f"     Justificación: {site.justification}")
        
        # Validación
        print("\n🟡 C. INTERMEDIO (Validación) - Debe DISTINGUIR")
        for site in self.list_calibration_sites(ControlType.VALIDATION):
            print(f"\n  📍 {site.name}")
            print(f"     Coords: {site.lat:.4f}, {site.lon:.4f}")
            print(f"     Por qué: {site.why_chosen}")
            print(f"     Esperado ESS Vol: {site.expected_ess_vol[0]:.2f}-{site.expected_ess_vol[1]:.2f}")
            print(f"     Justificación: {site.justification}")
        
        print()
        print("="*80)


if __name__ == "__main__":
    # Test del sistema de calibración
    cal_system = CalibrationSystem()
    cal_system.print_calibration_protocol()
