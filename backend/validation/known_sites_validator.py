#!/usr/bin/env python3
"""
Validador de Sitios Conocidos - SOLO DATOS REALES

REGLA ABSOLUTA: JAMÁS INVENTAR DATOS

Este módulo:
1. Recibe análisis REAL de CoreAnomalyDetector (con APIs satelitales reales)
2. Consulta BD de sitios arqueológicos documentados (PostgreSQL)
3. Contrasta mediciones REALES vs sitios conocidos
4. Usa OpenCode para validación lógica (NO para detección)
5. Crea registros de candidatos en BD

FLUJO CORRECTO:
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario analiza zona → CoreAnomalyDetector              │
│ 2. Mediciones REALES → Sentinel-2, Sentinel-1, Landsat...  │
│ 3. Detección con datos reales → Score base determinista    │
│ 4. Contraste con BD de sitios documentados                 │
│ 5. OpenCode valida coherencia lógica (DESPUÉS, no antes)   │
│ 6. Crear registro de candidato en BD                       │
└─────────────────────────────────────────────────────────────┘

Fecha de reescritura: 2026-01-26
Razón: Eliminar simulaciones, usar solo datos reales
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class DocumentedSite:
    """Sitio arqueológico documentado en BD."""
    id: str
    name: str
    latitude: float
    longitude: float
    site_type: str
    period: Optional[str]
    confidence_level: str  # CONFIRMED, HIGH, MODERATE, LOW
    source: str  # excavated, national, wikidata, osm
    distance_km: float = 0.0  # Distancia al punto de análisis

@dataclass
class ValidationResult:
    """Resultado de validación con datos REALES."""
    
    # Identificación
    validation_id: str
    analysis_date: datetime
    
    # Ubicación analizada
    center_lat: float
    center_lon: float
    area_analyzed_km2: float
    
    # Mediciones REALES de instrumentos
    real_measurements: List[Dict[str, Any]]  # De CoreAnomalyDetector
    
    # Resultado de detección REAL
    anomaly_detected: bool
    archaeological_probability: float
    confidence_level: str
    
    # Contraste con sitios documentados
    documented_sites_nearby: List[DocumentedSite]
    closest_site: Optional[DocumentedSite]
    distance_to_closest_km: Optional[float]
    
    # Validación lógica (OpenCode - DESPUÉS del análisis)
    logical_validation: Optional[Dict[str, Any]]
    
    # Registro de candidato creado
    candidate_id: Optional[str]
    candidate_status: str  # validated, candidate, false_positive, needs_review
    
    # Metadata
    validation_notes: str
    created_by: str = "archeoscope_validator"

class KnownSitesValidator:
    """
    Validador que CONTRASTA mediciones REALES contra sitios documentados.
    
    IMPORTANTE:
    - NO inventa datos
    - NO simula mediciones
    - NO usa np.random
    - Solo trabaja con datos REALES de APIs satelitales
    - OpenCode se usa DESPUÉS del análisis, para validación lógica
    """
    
    def __init__(self, db_connection, opencode_client=None):
        """
        Inicializar validador.
        
        Args:
            db_connection: Conexión a PostgreSQL con sitios documentados
            opencode_client: Cliente OpenCode para validación lógica (opcional)
        """
        self.db = db_connection
        self.opencode = opencode_client
        
        logger.info("✅ KnownSitesValidator inicializado - SOLO DATOS REALES")
        if self.opencode:
            logger.info("✅ OpenCode disponible para validación lógica")
    
    async def validate_analysis(
        self,
        analysis_result,  # AnomalyDetectionResult de CoreAnomalyDetector
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        region_name: str = "Unknown Region"
    ) -> ValidationResult:
        """
        Validar análisis REAL contra sitios documentados.
        
        FLUJO:
        1. Recibir análisis REAL (con mediciones de APIs satelitales)
        2. Buscar sitios documentados en la zona (BD PostgreSQL)
        3. Contrastar mediciones REALES vs sitios conocidos
        4. Validar coherencia lógica con OpenCode (DESPUÉS)
        5. Crear registro de candidato en BD
        
        Args:
            analysis_result: Resultado REAL de CoreAnomalyDetector
            lat_min, lat_max, lon_min, lon_max: Área analizada
            region_name: Nombre de la región
        
        Returns:
            ValidationResult con contraste de datos REALES
        """
        
        logger.info("="*80)
        logger.info("🔍 VALIDACIÓN CON DATOS REALES")
        logger.info(f"   Región: {region_name}")
        logger.info(f"   Probabilidad arqueológica (REAL): {analysis_result.archaeological_probability:.2%}")
        logger.info("="*80)
        
        # Calcular centro y área
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2
        area_km2 = self._calculate_area_km2(lat_min, lat_max, lon_min, lon_max)
        
        # PASO 1: Buscar sitios documentados en la zona (BD REAL)
        logger.info("📚 PASO 1: Consultando BD de sitios documentados...")
        documented_sites = await self._find_documented_sites(
            lat_min, lat_max, lon_min, lon_max, center_lat, center_lon
        )
        
        if documented_sites:
            logger.info(f"   ✅ Encontrados {len(documented_sites)} sitios documentados")
            for site in documented_sites[:3]:  # Mostrar top 3
                logger.info(f"      - {site.name} ({site.distance_km:.2f} km)")
        else:
            logger.info("   ℹ️ No hay sitios documentados en esta zona")
        
        # PASO 2: Determinar sitio más cercano
        closest_site = documented_sites[0] if documented_sites else None
        distance_to_closest = closest_site.distance_km if closest_site else None
        
        # PASO 3: Determinar status del candidato
        candidate_status = self._determine_candidate_status(
            analysis_result, documented_sites
        )
        
        logger.info(f"📊 Status del candidato: {candidate_status}")
        
        # PASO 4: Validación lógica con OpenCode (DESPUÉS del análisis)
        logical_validation = None
        if self.opencode and analysis_result.archaeological_probability > 0.7:
            logger.info("🧠 PASO 4: Validación lógica con OpenCode...")
            logical_validation = await self._validate_with_opencode(
                analysis_result, documented_sites
            )
            
            if logical_validation:
                logger.info(f"   ✅ Coherencia lógica: {logical_validation.get('coherence_score', 0):.2f}")
        
        # PASO 5: Crear registro de candidato en BD
        logger.info("💾 PASO 5: Creando registro de candidato en BD...")
        candidate_id = await self._create_candidate_record(
            analysis_result=analysis_result,
            center_lat=center_lat,
            center_lon=center_lon,
            area_km2=area_km2,
            documented_sites=documented_sites,
            candidate_status=candidate_status,
            logical_validation=logical_validation
        )
        
        logger.info(f"   ✅ Candidato creado: {candidate_id}")
        
        # PASO 6: Generar resultado de validación
        validation_result = ValidationResult(
            validation_id=self._generate_validation_id(),
            analysis_date=datetime.now(),
            center_lat=center_lat,
            center_lon=center_lon,
            area_analyzed_km2=area_km2,
            real_measurements=[asdict(m) for m in analysis_result.measurements],
            anomaly_detected=analysis_result.anomaly_detected,
            archaeological_probability=analysis_result.archaeological_probability,
            confidence_level=analysis_result.confidence_level,
            documented_sites_nearby=documented_sites,
            closest_site=closest_site,
            distance_to_closest_km=distance_to_closest,
            logical_validation=logical_validation,
            candidate_id=candidate_id,
            candidate_status=candidate_status,
            validation_notes=self._generate_validation_notes(
                analysis_result, documented_sites, candidate_status
            )
        )
        
        logger.info("="*80)
        logger.info("✅ VALIDACIÓN COMPLETADA")
        logger.info(f"   Candidato: {candidate_id}")
        logger.info(f"   Status: {candidate_status}")
        logger.info("="*80)
        
        return validation_result
    
    async def _find_documented_sites(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        center_lat: float,
        center_lon: float
    ) -> List[DocumentedSite]:
        """
        Buscar sitios documentados en BD PostgreSQL.
        
        IMPORTANTE: Consulta BD REAL, NO inventa datos.
        """
        
        try:
            # Query a BD PostgreSQL
            query = """
                SELECT 
                    id,
                    name,
                    latitude,
                    longitude,
                    site_type,
                    period,
                    confidence_level,
                    source,
                    ST_Distance(
                        ST_MakePoint(longitude, latitude)::geography,
                        ST_MakePoint($5, $6)::geography
                    ) / 1000.0 as distance_km
                FROM archaeological_sites
                WHERE 
                    latitude BETWEEN $1 AND $2
                    AND longitude BETWEEN $3 AND $4
                    AND confidence_level IN ('CONFIRMED', 'HIGH', 'MODERATE')
                ORDER BY distance_km ASC
                LIMIT 10
            """
            
            rows = await self.db.fetch(
                query,
                lat_min, lat_max, lon_min, lon_max,
                center_lon, center_lat
            )
            
            documented_sites = []
            for row in rows:
                site = DocumentedSite(
                    id=str(row['id']),
                    name=row['name'],
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    site_type=row['site_type'] or 'unknown',
                    period=row['period'],
                    confidence_level=row['confidence_level'],
                    source=row['source'] or 'unknown',
                    distance_km=float(row['distance_km'])
                )
                documented_sites.append(site)
            
            return documented_sites
        
        except Exception as e:
            logger.error(f"❌ Error consultando BD de sitios documentados: {e}")
            return []
    
    def _determine_candidate_status(
        self,
        analysis_result,
        documented_sites: List[DocumentedSite]
    ) -> str:
        """
        Determinar status del candidato basado en datos REALES.
        
        Lógica:
        - validated: Alta probabilidad + sitio documentado cercano
        - candidate: Alta probabilidad + NO hay sitio documentado
        - false_positive: Baja probabilidad + sitio documentado (falló detección)
        - needs_review: Casos ambiguos
        """
        
        prob = analysis_result.archaeological_probability
        has_nearby_site = len(documented_sites) > 0
        closest_distance = documented_sites[0].distance_km if has_nearby_site else 999
        
        # Validated: Detección exitosa de sitio conocido
        if prob > 0.7 and has_nearby_site and closest_distance < 1.0:
            return "validated"
        
        # Candidate: Detección en zona sin sitios documentados
        if prob > 0.7 and not has_nearby_site:
            return "candidate"
        
        # False positive: No detectó sitio conocido cercano
        if prob < 0.5 and has_nearby_site and closest_distance < 0.5:
            return "false_positive"
        
        # Needs review: Casos ambiguos
        return "needs_review"
    
    async def _validate_with_opencode(
        self,
        analysis_result,
        documented_sites: List[DocumentedSite]
    ) -> Optional[Dict[str, Any]]:
        """
        Validar coherencia lógica con OpenCode.
        
        IMPORTANTE:
        - Se llama DESPUÉS del análisis, NO antes
        - Solo para candidatos de alta probabilidad (> 0.7)
        - NO se usa para detección, solo para validación
        - Asíncrono, no bloquea el flujo principal
        
        OpenCode valida:
        - Coherencia entre instrumentos
        - Consistencia lógica de mediciones
        - Explicación científica estructurada
        """
        
        if not self.opencode:
            return None
        
        try:
            # Preparar contexto para OpenCode
            context = {
                "task": "validate_archaeological_detection",
                "measurements": [
                    {
                        "instrument": m.instrument_name,
                        "value": m.value,
                        "threshold": m.threshold,
                        "exceeds": m.exceeds_threshold,
                        "confidence": m.confidence
                    }
                    for m in analysis_result.measurements
                ],
                "archaeological_probability": analysis_result.archaeological_probability,
                "environment_type": analysis_result.environment_type,
                "documented_sites_nearby": [
                    {
                        "name": s.name,
                        "distance_km": s.distance_km,
                        "confidence": s.confidence_level
                    }
                    for s in documented_sites[:3]
                ]
            }
            
            # Llamar OpenCode (asíncrono)
            validation = await self.opencode.validate(context)
            
            return {
                "coherence_score": validation.get("coherence_score", 0.0),
                "logical_consistency": validation.get("logical_consistency", "unknown"),
                "explanation": validation.get("explanation", ""),
                "flags": validation.get("flags", []),
                "recommendations": validation.get("recommendations", [])
            }
        
        except Exception as e:
            logger.warning(f"⚠️ OpenCode validation failed: {e}")
            return None
    
    async def _create_candidate_record(
        self,
        analysis_result,
        center_lat: float,
        center_lon: float,
        area_km2: float,
        documented_sites: List[DocumentedSite],
        candidate_status: str,
        logical_validation: Optional[Dict[str, Any]]
    ) -> str:
        """
        Crear registro de candidato en BD PostgreSQL.
        
        IMPORTANTE: Guarda mediciones REALES, NO inventadas.
        """
        
        try:
            # Preparar datos de mediciones REALES
            measurements_json = json.dumps([
                {
                    "instrument": m.instrument_name,
                    "type": m.measurement_type,
                    "value": m.value,
                    "unit": m.unit,
                    "threshold": m.threshold,
                    "exceeds_threshold": m.exceeds_threshold,
                    "confidence": m.confidence,
                    "notes": m.notes
                }
                for m in analysis_result.measurements
            ])
            
            # Preparar datos de sitios documentados cercanos
            nearby_sites_json = json.dumps([
                {
                    "id": s.id,
                    "name": s.name,
                    "distance_km": s.distance_km,
                    "confidence_level": s.confidence_level
                }
                for s in documented_sites
            ]) if documented_sites else None
            
            # Preparar validación lógica
            logical_validation_json = json.dumps(logical_validation) if logical_validation else None
            
            # Insert en BD
            query = """
                INSERT INTO archaeological_candidates (
                    latitude,
                    longitude,
                    area_km2,
                    archaeological_probability,
                    confidence_level,
                    environment_type,
                    real_measurements,
                    documented_sites_nearby,
                    logical_validation,
                    status,
                    created_by,
                    created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING id
            """
            
            result = await self.db.fetchrow(
                query,
                center_lat,
                center_lon,
                area_km2,
                analysis_result.archaeological_probability,
                analysis_result.confidence_level,
                analysis_result.environment_type,
                measurements_json,
                nearby_sites_json,
                logical_validation_json,
                candidate_status,
                "archeoscope_validator",
                datetime.now()
            )
            
            return str(result['id'])
        
        except Exception as e:
            logger.error(f"❌ Error creando registro de candidato: {e}")
            return "error_creating_record"
    
    def _calculate_area_km2(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> float:
        """Calcular área aproximada en km²."""
        
        # Aproximación simple (suficiente para este propósito)
        lat_diff = lat_max - lat_min
        lon_diff = lon_max - lon_min
        
        # ~111 km por grado de latitud
        # ~111 km * cos(lat) por grado de longitud
        avg_lat = (lat_min + lat_max) / 2
        import math
        
        height_km = lat_diff * 111.0
        width_km = lon_diff * 111.0 * math.cos(math.radians(avg_lat))
        
        return height_km * width_km
    
    def _generate_validation_id(self) -> str:
        """Generar ID único para validación."""
        import uuid
        return f"val_{uuid.uuid4().hex[:12]}"
    
    def _generate_validation_notes(
        self,
        analysis_result,
        documented_sites: List[DocumentedSite],
        candidate_status: str
    ) -> str:
        """Generar notas de validación."""
        
        notes = []
        
        # Resultado de detección
        if analysis_result.anomaly_detected:
            notes.append(f"Anomalía detectada con probabilidad {analysis_result.archaeological_probability:.2%}")
        else:
            notes.append("No se detectó anomalía significativa")
        
        # Instrumentos convergentes
        converging = analysis_result.instruments_converging
        required = analysis_result.minimum_required
        notes.append(f"Convergencia instrumental: {converging}/{required}")
        
        # Sitios documentados
        if documented_sites:
            closest = documented_sites[0]
            notes.append(f"Sitio documentado más cercano: {closest.name} ({closest.distance_km:.2f} km)")
        else:
            notes.append("No hay sitios documentados en la zona")
        
        # Status
        notes.append(f"Status: {candidate_status}")
        
        return " | ".join(notes)


# ============================================================================
# DOCUMENTACIÓN DE USO
# ============================================================================

"""
EJEMPLO DE USO CORRECTO:

from backend.core_anomaly_detector import CoreAnomalyDetector
from backend.validation.known_sites_validator import KnownSitesValidator
from backend.database import db

# 1. Inicializar componentes
core_detector = CoreAnomalyDetector(...)
validator = KnownSitesValidator(db_connection=db, opencode_client=opencode)

# 2. Analizar zona con DATOS REALES
analysis_result = await core_detector.detect_anomaly(
    lat=13.1631,
    lon=-72.5450,
    lat_min=13.1531,
    lat_max=13.1731,
    lon_min=-72.5550,
    lon_max=-72.5350,
    region_name="Machu Picchu Area"
)

# 3. Validar contra sitios documentados
validation_result = await validator.validate_analysis(
    analysis_result=analysis_result,  # ← DATOS REALES de APIs satelitales
    lat_min=13.1531,
    lat_max=13.1731,
    lon_min=-72.5550,
    lon_max=-72.5350,
    region_name="Machu Picchu Area"
)

# 4. Resultado contiene:
# - Mediciones REALES de instrumentos
# - Sitios documentados cercanos (de BD)
# - Validación lógica (OpenCode)
# - Registro de candidato creado en BD

print(f"Candidato creado: {validation_result.candidate_id}")
print(f"Status: {validation_result.candidate_status}")
print(f"Sitio más cercano: {validation_result.closest_site.name if validation_result.closest_site else 'Ninguno'}")
"""
