-- ============================================================================
-- TABLAS PARA SISTEMA TIMT (Territorial Inferential Multi-modal Tomography)
-- ============================================================================

-- Tabla para análisis TIMT completos
CREATE TABLE IF NOT EXISTS timt_analyses (
    id SERIAL PRIMARY KEY,
    analysis_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Coordenadas del territorio
    lat_min DECIMAL(10, 6) NOT NULL,
    lat_max DECIMAL(10, 6) NOT NULL,
    lon_min DECIMAL(10, 6) NOT NULL,
    lon_max DECIMAL(10, 6) NOT NULL,
    center_lat DECIMAL(10, 6),
    center_lon DECIMAL(10, 6),
    
    -- Metadatos
    region_name VARCHAR(500),
    analysis_objective VARCHAR(100),
    analysis_radius_km DECIMAL(10, 2),
    resolution_m DECIMAL(10, 2),
    
    -- Métricas finales
    territorial_coherence_score DECIMAL(5, 4),
    scientific_rigor_score DECIMAL(5, 4),
    
    -- Timestamps
    analysis_timestamp TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Índices para búsqueda
    CONSTRAINT timt_analyses_bounds_check CHECK (lat_min < lat_max AND lon_min < lon_max)
);

CREATE INDEX IF NOT EXISTS idx_timt_analyses_coords ON timt_analyses(center_lat, center_lon);
CREATE INDEX IF NOT EXISTS idx_timt_analyses_timestamp ON timt_analyses(analysis_timestamp DESC);

-- Tabla para TCP (Territorial Context Profile)
CREATE TABLE IF NOT EXISTS tcp_profiles (
    id SERIAL PRIMARY KEY,
    timt_analysis_id INTEGER REFERENCES timt_analyses(id) ON DELETE CASCADE,
    tcp_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Contexto geológico
    dominant_lithology VARCHAR(100),
    geological_age VARCHAR(100),
    tectonic_context VARCHAR(200),
    
    -- Contexto hidrográfico
    hydrographic_features_count INTEGER DEFAULT 0,
    water_availability VARCHAR(50),
    
    -- Contexto arqueológico externo
    external_sites_count INTEGER DEFAULT 0,
    nearest_site_distance_km DECIMAL(10, 2),
    
    -- Contexto humano
    human_traces_count INTEGER DEFAULT 0,
    
    -- Potencial de preservación
    preservation_potential VARCHAR(50),
    historical_biome VARCHAR(100),
    
    -- Estrategia instrumental
    priority_instruments TEXT[], -- Array de instrumentos
    recommended_resolution_m DECIMAL(10, 2),
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tcp_timt_analysis ON tcp_profiles(timt_analysis_id);

-- Tabla para hipótesis territoriales
CREATE TABLE IF NOT EXISTS territorial_hypotheses (
    id SERIAL PRIMARY KEY,
    tcp_profile_id INTEGER REFERENCES tcp_profiles(id) ON DELETE CASCADE,
    
    -- Hipótesis
    hypothesis_type VARCHAR(100) NOT NULL,
    hypothesis_explanation TEXT,
    plausibility_score DECIMAL(5, 4),
    
    -- Instrumentos recomendados
    recommended_instruments TEXT[],
    
    -- Validación
    validation_status VARCHAR(50), -- 'validated', 'rejected', 'uncertain'
    supporting_evidence_score DECIMAL(5, 4),
    contradicting_evidence_score DECIMAL(5, 4),
    validation_confidence DECIMAL(5, 4),
    validation_explanation TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hypotheses_tcp ON territorial_hypotheses(tcp_profile_id);
CREATE INDEX IF NOT EXISTS idx_hypotheses_validation ON territorial_hypotheses(validation_status);

-- Tabla para ETP (Environmental Tomographic Profile)
CREATE TABLE IF NOT EXISTS etp_profiles (
    id SERIAL PRIMARY KEY,
    timt_analysis_id INTEGER REFERENCES timt_analyses(id) ON DELETE CASCADE,
    territory_id VARCHAR(255) NOT NULL,
    
    -- Resolución
    resolution_m DECIMAL(10, 2),
    
    -- Métricas ESS
    ess_superficial DECIMAL(5, 4),
    ess_subsuperficial DECIMAL(5, 4),
    ess_volumetrico DECIMAL(5, 4),
    ess_temporal DECIMAL(5, 4),
    
    -- Métricas 3D/4D
    coherencia_3d DECIMAL(5, 4),
    persistencia_temporal DECIMAL(5, 4),
    densidad_arqueologica_m3 DECIMAL(10, 6),
    
    -- Scores de compatibilidad
    geological_compatibility_score DECIMAL(5, 4),
    water_availability_score DECIMAL(5, 4),
    external_consistency_score DECIMAL(5, 4),
    
    -- Nivel de confianza
    confidence_level VARCHAR(50),
    
    -- Recomendación
    recommended_action VARCHAR(100),
    
    -- Narrativa
    narrative_explanation TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_etp_timt_analysis ON etp_profiles(timt_analysis_id);
CREATE INDEX IF NOT EXISTS idx_etp_ess_volumetrico ON etp_profiles(ess_volumetrico DESC);

-- Tabla para anomalías volumétricas
CREATE TABLE IF NOT EXISTS volumetric_anomalies (
    id SERIAL PRIMARY KEY,
    etp_profile_id INTEGER REFERENCES etp_profiles(id) ON DELETE CASCADE,
    
    -- Posición 3D
    center_x DECIMAL(10, 2),
    center_y DECIMAL(10, 2),
    center_z DECIMAL(10, 2),
    
    -- Dimensiones
    volume_m3 DECIMAL(15, 2),
    depth_min_m DECIMAL(10, 2),
    depth_max_m DECIMAL(10, 2),
    
    -- Clasificación
    anomaly_type VARCHAR(100),
    archaeological_type VARCHAR(100),
    
    -- Temporal
    temporal_range_start INTEGER, -- años
    temporal_range_end INTEGER,
    
    -- Confianza
    confidence DECIMAL(5, 4),
    
    -- Instrumentos
    instruments_supporting TEXT[],
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_anomalies_etp ON volumetric_anomalies(etp_profile_id);
CREATE INDEX IF NOT EXISTS idx_anomalies_confidence ON volumetric_anomalies(confidence DESC);

-- Tabla para reporte de transparencia
CREATE TABLE IF NOT EXISTS transparency_reports (
    id SERIAL PRIMARY KEY,
    timt_analysis_id INTEGER REFERENCES timt_analyses(id) ON DELETE CASCADE,
    
    -- Proceso
    analysis_process TEXT[],
    
    -- Decisiones
    key_decisions TEXT[],
    
    -- Limitaciones
    known_limitations TEXT[],
    system_boundaries TEXT[],
    
    -- Hipótesis
    hypotheses_evaluated INTEGER,
    hypotheses_validated INTEGER,
    hypotheses_rejected INTEGER,
    hypotheses_uncertain INTEGER,
    hypotheses_discarded INTEGER,
    
    -- Recomendaciones
    validation_recommendations TEXT[],
    future_work_suggestions TEXT[],
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transparency_timt ON transparency_reports(timt_analysis_id);

-- Tabla para comunicación multinivel
CREATE TABLE IF NOT EXISTS multilevel_communications (
    id SERIAL PRIMARY KEY,
    timt_analysis_id INTEGER REFERENCES timt_analyses(id) ON DELETE CASCADE,
    
    -- 4 niveles de comunicación
    level1_what_measured TEXT,
    level2_why_measured TEXT,
    level3_what_inferred TEXT,
    level4_what_cannot_affirm TEXT,
    
    -- Resúmenes por audiencia
    executive_summary TEXT,
    technical_summary TEXT,
    academic_summary TEXT,
    educational_summary TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_communications_timt ON multilevel_communications(timt_analysis_id);

-- Vista consolidada para consultas rápidas
CREATE OR REPLACE VIEW timt_analyses_complete AS
SELECT 
    ta.id,
    ta.analysis_id,
    ta.region_name,
    ta.center_lat,
    ta.center_lon,
    ta.territorial_coherence_score,
    ta.scientific_rigor_score,
    ta.analysis_timestamp,
    
    -- TCP
    tcp.tcp_id,
    tcp.dominant_lithology,
    tcp.preservation_potential,
    tcp.external_sites_count,
    
    -- ETP
    etp.ess_volumetrico,
    etp.coherencia_3d,
    etp.confidence_level,
    etp.recommended_action,
    
    -- Hipótesis
    COUNT(DISTINCT th.id) as total_hypotheses,
    COUNT(DISTINCT CASE WHEN th.validation_status = 'validated' THEN th.id END) as validated_hypotheses,
    
    -- Anomalías
    COUNT(DISTINCT va.id) as volumetric_anomalies_count
    
FROM timt_analyses ta
LEFT JOIN tcp_profiles tcp ON tcp.timt_analysis_id = ta.id
LEFT JOIN etp_profiles etp ON etp.timt_analysis_id = ta.id
LEFT JOIN territorial_hypotheses th ON th.tcp_profile_id = tcp.id
LEFT JOIN volumetric_anomalies va ON va.etp_profile_id = etp.id
GROUP BY ta.id, tcp.id, etp.id;

-- Comentarios
COMMENT ON TABLE timt_analyses IS 'Análisis completos del sistema TIMT con 3 capas (TCP + ETP + Validación)';
COMMENT ON TABLE tcp_profiles IS 'Perfiles de Contexto Territorial - CAPA 0: Contexto antes de medir';
COMMENT ON TABLE territorial_hypotheses IS 'Hipótesis territoriales generadas y validadas';
COMMENT ON TABLE etp_profiles IS 'Perfiles Tomográficos Ambientales - CAPA 1: Tomografía 3D/4D';
COMMENT ON TABLE volumetric_anomalies IS 'Anomalías volumétricas detectadas en el análisis tomográfico';
COMMENT ON TABLE transparency_reports IS 'Reportes de transparencia - CAPA 3: Límites epistémicos';
COMMENT ON TABLE multilevel_communications IS 'Comunicación multinivel (4 niveles) para diferentes audiencias';
