#!/usr/bin/env python3
"""
Guardado de resultados TIMT en base de datos.
"""

import logging
import json
import math
from typing import Any
from territorial_inferential_tomography import TerritorialInferentialTomographyResult

logger = logging.getLogger(__name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calcular distancia en km entre dos puntos (Haversine)."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

async def save_timt_result_to_db(db_pool, result: TerritorialInferentialTomographyResult, request_data: dict):
    """
    Guardar resultado TIMT completo en base de datos.
    
    Args:
        db_pool: Pool de conexiones asyncpg
        result: Resultado TIMT completo
        request_data: Datos de la solicitud original
    """
    
    if not db_pool:
        logger.warning("⚠️ DB pool not available, skipping save")
        return None
    
    try:
        async with db_pool.acquire() as conn:
            async with conn.transaction():
                
                # 1. Guardar análisis TIMT principal
                timt_id = await conn.fetchval("""
                    INSERT INTO timt_analyses (
                        analysis_id, lat_min, lat_max, lon_min, lon_max,
                        center_lat, center_lon, region_name, analysis_objective,
                        analysis_radius_km, resolution_m,
                        territorial_coherence_score, scientific_rigor_score,
                        analysis_timestamp, scientific_output
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
                    RETURNING id
                """,
                    result.analysis_id,
                    result.territory_bounds.lat_min,
                    result.territory_bounds.lat_max,
                    result.territory_bounds.lon_min,
                    result.territory_bounds.lon_max,
                    (result.territory_bounds.lat_min + result.territory_bounds.lat_max) / 2,
                    (result.territory_bounds.lon_min + result.territory_bounds.lon_max) / 2,
                    request_data.get('region_name', 'Unknown'),
                    result.territorial_context.analysis_objective.value,
                    request_data.get('analysis_radius_km', 5.0),
                    request_data.get('resolution_m'),
                    result.territorial_coherence_score,
                    result.scientific_rigor_score,
                    result.analysis_timestamp,
                    json.dumps(result.scientific_output)
                )
                
                logger.info(f"✅ TIMT analysis saved: ID={timt_id}")
                
                # 2. Guardar TCP (Territorial Context Profile)
                tcp = result.territorial_context
                tcp_id = await conn.fetchval("""
                    INSERT INTO tcp_profiles (
                        timt_analysis_id, tcp_id,
                        dominant_lithology, geological_age, tectonic_context,
                        hydrographic_features_count, water_availability,
                        external_sites_count, nearest_site_distance_km,
                        human_traces_count,
                        preservation_potential, historical_biome,
                        priority_instruments, recommended_resolution_m
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                    RETURNING id
                """,
                    timt_id,
                    tcp.tcp_id,
                    tcp.geological_context.dominant_lithology.value if tcp.geological_context else 'unknown',
                    tcp.geological_context.geological_age.value if tcp.geological_context else 'unknown',
                    f"fault_density_{tcp.geological_context.fault_density:.1f}" if tcp.geological_context else 'unknown',  # Usar fault_density en lugar de tectonic_context
                    len(tcp.hydrographic_features),
                    f"{result.tomographic_profile.water_availability.settlement_viability:.2f}" if result.tomographic_profile.water_availability else 'unknown',
                    len(tcp.external_archaeological_sites),
                    min([calculate_distance((request_data.get('center_lat') or (result.territory_bounds.lat_min + result.territory_bounds.lat_max)/2),
                                          (request_data.get('center_lon') or (result.territory_bounds.lon_min + result.territory_bounds.lon_max)/2),
                                          s.latitude, s.longitude) for s in tcp.external_archaeological_sites]) if tcp.external_archaeological_sites else None,
                    len(tcp.known_human_traces),
                    tcp.preservation_potential.value,
                    tcp.historical_biome.value,
                    tcp.instrumental_strategy.priority_instruments if tcp.instrumental_strategy else [],
                    tcp.instrumental_strategy.recommended_resolution_m if tcp.instrumental_strategy else None
                )
                
                logger.info(f"✅ TCP saved: ID={tcp_id}")
                
                # 3. Guardar hipótesis territoriales
                for hypothesis in tcp.territorial_hypotheses:
                    # Buscar validación correspondiente
                    validation = next(
                        (v for v in result.hypothesis_validations if v.hypothesis_id == hypothesis.hypothesis_id),
                        None
                    )
                    
                    await conn.execute("""
                        INSERT INTO territorial_hypotheses (
                            tcp_profile_id, hypothesis_type, hypothesis_explanation,
                            plausibility_score, recommended_instruments,
                            validation_status, supporting_evidence_score,
                            contradicting_evidence_score, validation_confidence,
                            validation_explanation
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    """,
                        tcp_id,
                        hypothesis.hypothesis_type,  # Ya es string, no .value
                        hypothesis.hypothesis_explanation,
                        hypothesis.plausibility_score,
                        hypothesis.recommended_instruments,
                        validation.overall_evidence_level.value if validation else 'insufficient',  # Usar overall_evidence_level
                        # Calcular scores de evidencia desde los atributos reales
                        (validation.sensorial_evidence + validation.geological_evidence + 
                         validation.hydrographic_evidence + validation.archaeological_evidence + 
                         validation.human_traces_evidence) / 5.0 if validation else 0.0,  # Promedio como supporting
                        len(validation.contradictions) / 10.0 if validation else 0.0,  # Contradicciones normalizadas
                        validation.confidence_score if validation else 0.0,  # Usar confidence_score
                        validation.validation_explanation if validation else ''
                    )
                
                logger.info(f"✅ {len(tcp.territorial_hypotheses)} hypotheses saved")
                
                # 4. Guardar ETP (Environmental Tomographic Profile)
                etp = result.tomographic_profile
                etp_id = await conn.fetchval("""
                    INSERT INTO etp_profiles (
                        timt_analysis_id, territory_id, resolution_m,
                        ess_superficial, ess_subsuperficial, ess_volumetrico, ess_temporal,
                        coherencia_3d, persistencia_temporal, densidad_arqueologica_m3,
                        geological_compatibility_score, water_availability_score,
                        external_consistency_score,
                        confidence_level, recommended_action, narrative_explanation
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
                    RETURNING id
                """,
                    timt_id,
                    etp.territory_id,
                    etp.resolution_m,
                    etp.ess_superficial,
                    0.0,  # ess_subsuperficial no existe en ETP
                    etp.ess_volumetrico,
                    etp.ess_temporal,
                    etp.coherencia_3d,
                    etp.persistencia_temporal,
                    etp.densidad_arqueologica_m3,
                    etp.geological_compatibility.gcs_score if etp.geological_compatibility else None,
                    etp.water_availability.settlement_viability if etp.water_availability else None,
                    etp.external_consistency.ecs_score if etp.external_consistency else None,
                    etp.get_confidence_level(),
                    etp.get_archaeological_recommendation(),  # Usar método correcto
                    etp.narrative_explanation
                )
                
                logger.info(f"✅ ETP saved: ID={etp_id}")
                
                # 5. Guardar anomalías volumétricas (si existen)
                if hasattr(etp, 'volumetric_anomalies') and etp.volumetric_anomalies:
                    for anomaly in etp.volumetric_anomalies:
                        # Calcular volumen desde extent_3d
                        volume_m3 = anomaly.extent_3d[0] * anomaly.extent_3d[1] * anomaly.extent_3d[2]
                        depth_min = anomaly.center_3d[2] - anomaly.extent_3d[2] / 2
                        depth_max = anomaly.center_3d[2] + anomaly.extent_3d[2] / 2
                        
                        await conn.execute("""
                            INSERT INTO volumetric_anomalies (
                                etp_profile_id, center_x, center_y, center_z,
                                volume_m3, depth_min_m, depth_max_m,
                                anomaly_type, archaeological_type,
                                temporal_range_start, temporal_range_end,
                                confidence, instruments_supporting
                            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                        """,
                            etp_id,
                            anomaly.center_3d[0],
                            anomaly.center_3d[1],
                            anomaly.center_3d[2],
                            volume_m3,
                            depth_min,
                            depth_max,
                            'volumetric',  # Tipo genérico
                            anomaly.archaeological_type,
                            anomaly.temporal_range[0],
                            anomaly.temporal_range[1],
                            anomaly.confidence,
                            anomaly.instruments_supporting
                        )
                    
                    logger.info(f"✅ {len(etp.volumetric_anomalies)} volumetric anomalies saved")
                
                # 6. Guardar reporte de transparencia
                tr = result.transparency_report
                
                # Calcular conteos de hipótesis por nivel de evidencia
                strong_evidence = len([h for h in result.hypothesis_validations if h.overall_evidence_level.value == 'strong'])
                moderate_evidence = len([h for h in result.hypothesis_validations if h.overall_evidence_level.value == 'moderate'])
                weak_evidence = len([h for h in result.hypothesis_validations if h.overall_evidence_level.value == 'weak'])
                insufficient_evidence = len([h for h in result.hypothesis_validations if h.overall_evidence_level.value == 'insufficient'])
                
                await conn.execute("""
                    INSERT INTO transparency_reports (
                        timt_analysis_id, analysis_process, key_decisions,
                        known_limitations, system_boundaries,
                        hypotheses_evaluated, hypotheses_validated,
                        hypotheses_rejected, hypotheses_uncertain, hypotheses_discarded,
                        validation_recommendations, future_work_suggestions
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                """,
                    timt_id,
                    tr.analysis_process,
                    tr.decisions_made,
                    tr.system_limitations,
                    tr.cannot_affirm,  # Usar cannot_affirm en lugar de system_boundaries
                    len(result.hypothesis_validations),
                    strong_evidence,  # Evidencia fuerte como "validadas"
                    weak_evidence + insufficient_evidence,  # Evidencia débil/insuficiente como "rechazadas"
                    moderate_evidence,  # Evidencia moderada como "inciertas"
                    len(tr.hypotheses_discarded),
                    tr.validation_recommendations,
                    tr.future_work_suggestions
                )
                
                logger.info(f"✅ Transparency report saved")
                
                # 7. Guardar comunicación multinivel
                await conn.execute("""
                    INSERT INTO multilevel_communications (
                        timt_analysis_id,
                        level1_what_measured, level2_why_measured,
                        level3_what_inferred, level4_what_cannot_affirm,
                        executive_summary, technical_summary,
                        academic_summary, educational_summary
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """,
                    timt_id,
                    result.general_summary[:1000] if result.general_summary else '',  # Level 1
                    result.technical_summary[:1000] if result.technical_summary else '',  # Level 2
                    result.academic_summary[:1000] if result.academic_summary else '',  # Level 3
                    ', '.join(tr.cannot_affirm[:5]),  # Level 4
                    result.institutional_summary if result.institutional_summary else '',
                    result.technical_summary if result.technical_summary else '',
                    result.academic_summary if result.academic_summary else '',
                    result.general_summary if result.general_summary else ''
                )
                
                logger.info(f"✅ Multilevel communication saved")
                
                # 8. Guardar TAMBIÉN en tabla antigua para compatibilidad con endpoints existentes
                print("[BD] Guardando en tabla antigua para compatibilidad...", flush=True)
                
                # Generar candidate_id único basado en el analysis_id
                candidate_id = f"TIMT_{result.analysis_id}"
                
                await conn.execute("""
                    INSERT INTO archaeological_candidate_analyses (
                        candidate_id, candidate_name, region,
                        archaeological_probability, anomaly_score,
                        result_type, recommended_action,
                        environment_type, confidence_level,
                        latitude, longitude,
                        lat_min, lat_max, lon_min, lon_max,
                        scientific_explanation, explanation_type
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
                """,
                    candidate_id,
                    request_data.get('region_name', 'Unknown'),
                    f"TIMT Analysis {result.analysis_id}",
                    result.tomographic_profile.densidad_arqueologica_m3,
                    result.tomographic_profile.ess_superficial,
                    'positive_candidate' if result.tomographic_profile.densidad_arqueologica_m3 > 0.5 else 'uncertain',
                    result.tomographic_profile.get_archaeological_recommendation(),
                    result.territorial_context.historical_biome.value,
                    result.scientific_rigor_score,
                    (result.territory_bounds.lat_min + result.territory_bounds.lat_max) / 2,
                    (result.territory_bounds.lon_min + result.territory_bounds.lon_max) / 2,
                    result.territory_bounds.lat_min,
                    result.territory_bounds.lat_max,
                    result.territory_bounds.lon_min,
                    result.territory_bounds.lon_max,
                    result.academic_summary[:1000] if result.academic_summary else '',
                    'timt_analysis'
                )
                
                logger.info(f"✅ Saved to legacy table for compatibility")
                
                logger.info(f"🎉 TIMT result completely saved to database: {result.analysis_id}")
                
                return timt_id
                
    except Exception as e:
        logger.error(f"❌ Error saving TIMT result to DB: {e}", exc_info=True)
        return None
