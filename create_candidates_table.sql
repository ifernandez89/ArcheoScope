-- ArcheoScope - Tabla de Candidatas Arqueológicas Enriquecidas
-- Almacena candidatas generadas por el sistema multi-instrumental

-- Enum para estado de análisis
CREATE TYPE candidate_status AS ENUM (
    'pending',           -- Pendiente de análisis
    'analyzing',         -- En proceso de análisis
    'analyzed',          -- Análisis completado
    'field_validated',   -- Validada en campo
    'rejected',          -- Rechazada
    'archived'           -- Archivada
);

-- Enum para acción recomendada
CREATE TYPE recommended_action AS ENUM (
    'field_validation',  -- Validación de campo prioritaria
    'detailed_analysis', -- Análisis detallado requerido
    'monitor',           -- Monitorear cambios temporales
    'discard'            -- Descartar (baja probabilidad)
);

-- Tabla principal de candidatas
CREATE TABLE IF NOT EXISTS archaeological_candidates (
    -- Identificación
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id VARCHAR(50) UNIQUE NOT NULL,  -- CND_HZ_000001
    zone_id VARCHAR(50) NOT NULL,              -- HZ_000001
    
    -- Ubicación
    center_lat DOUBLE PRECISION NOT NULL,
    center_lon DOUBLE PRECISION NOT NULL,
    area_km2 DOUBLE PRECISION NOT NULL,
    
    -- Scoring multi-instrumental
    multi_instrumental_score DOUBLE PRECISION NOT NULL,  -- 0-1
    convergence_count INTEGER NOT NULL,                  -- Cuántos instrumentos detectan
    convergence_ratio DOUBLE PRECISION NOT NULL,         -- 0-1
    
    -- Recomendación y estado
    recommended_action recommended_action NOT NULL,
    status candidate_status DEFAULT 'pending',
    
    -- Persistencia temporal
    temporal_persistence BOOLEAN DEFAULT false,
    temporal_years INTEGER DEFAULT 0,
    
    -- Señales instrumentales (JSONB para flexibilidad)
    signals JSONB NOT NULL,
    
    -- Metadata de generación
    strategy VARCHAR(20),                      -- buffer, gradient, gaps
    generation_date TIMESTAMP DEFAULT NOW(),
    
    -- Región de origen
    region_bounds JSONB,                       -- {lat_min, lat_max, lon_min, lon_max}
    
    -- Análisis y validación
    analysis_date TIMESTAMP,
    analysis_results JSONB,
    field_validation_date TIMESTAMP,
    field_validation_results JSONB,
    
    -- Notas y observaciones
    notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices para búsquedas eficientes
CREATE INDEX idx_candidates_lat_lon ON archaeological_candidates (center_lat, center_lon);

CREATE INDEX idx_candidates_score ON archaeological_candidates (multi_instrumental_score DESC);
CREATE INDEX idx_candidates_status ON archaeological_candidates (status);
CREATE INDEX idx_candidates_action ON archaeological_candidates (recommended_action);
CREATE INDEX idx_candidates_convergence ON archaeological_candidates (convergence_ratio DESC);
CREATE INDEX idx_candidates_temporal ON archaeological_candidates (temporal_persistence, temporal_years DESC);
CREATE INDEX idx_candidates_generation_date ON archaeological_candidates (generation_date DESC);

-- Índice GIN para búsquedas en JSONB
CREATE INDEX idx_candidates_signals ON archaeological_candidates USING GIN (signals);
CREATE INDEX idx_candidates_analysis ON archaeological_candidates USING GIN (analysis_results);

-- Trigger para actualizar updated_at
CREATE OR REPLACE FUNCTION update_candidates_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_candidates_updated_at
    BEFORE UPDATE ON archaeological_candidates
    FOR EACH ROW
    EXECUTE FUNCTION update_candidates_updated_at();

-- Vista para candidatas prioritarias
CREATE OR REPLACE VIEW priority_candidates AS
SELECT 
    id,
    candidate_id,
    zone_id,
    center_lat,
    center_lon,
    area_km2,
    multi_instrumental_score,
    convergence_count,
    convergence_ratio,
    recommended_action,
    status,
    temporal_persistence,
    temporal_years,
    generation_date,
    -- Extraer instrumentos detectados
    (
        SELECT COUNT(*)
        FROM jsonb_each(signals)
        WHERE (value->>'detected')::boolean = true
    ) as instruments_detected
FROM archaeological_candidates
WHERE 
    status = 'pending'
    AND recommended_action IN ('field_validation', 'detailed_analysis')
ORDER BY 
    multi_instrumental_score DESC,
    convergence_ratio DESC;

-- Vista para estadísticas de candidatas
CREATE OR REPLACE VIEW candidates_statistics AS
SELECT 
    COUNT(*) as total_candidates,
    COUNT(*) FILTER (WHERE status = 'pending') as pending,
    COUNT(*) FILTER (WHERE status = 'analyzing') as analyzing,
    COUNT(*) FILTER (WHERE status = 'analyzed') as analyzed,
    COUNT(*) FILTER (WHERE status = 'field_validated') as field_validated,
    COUNT(*) FILTER (WHERE status = 'rejected') as rejected,
    COUNT(*) FILTER (WHERE recommended_action = 'field_validation') as field_validation_priority,
    COUNT(*) FILTER (WHERE recommended_action = 'detailed_analysis') as detailed_analysis,
    COUNT(*) FILTER (WHERE temporal_persistence = true) as with_temporal_persistence,
    AVG(multi_instrumental_score) as avg_score,
    AVG(convergence_ratio) as avg_convergence,
    AVG(temporal_years) FILTER (WHERE temporal_persistence = true) as avg_temporal_years
FROM archaeological_candidates;

-- Comentarios para documentación
COMMENT ON TABLE archaeological_candidates IS 'Candidatas arqueológicas enriquecidas con señales multi-instrumentales';
COMMENT ON COLUMN archaeological_candidates.multi_instrumental_score IS 'Score combinado de todos los instrumentos (0-1)';
COMMENT ON COLUMN archaeological_candidates.convergence_ratio IS 'Ratio de instrumentos que detectan anomalía (0-1)';
COMMENT ON COLUMN archaeological_candidates.temporal_persistence IS 'Si la anomalía persiste temporalmente (lo humano persiste, lo natural fluctúa)';
COMMENT ON COLUMN archaeological_candidates.signals IS 'Señales de cada instrumento en formato JSON';

-- Grants (ajustar según usuarios de tu BD)
-- GRANT SELECT, INSERT, UPDATE ON archaeological_candidates TO archeoscope_user;
-- GRANT SELECT ON priority_candidates TO archeoscope_user;
-- GRANT SELECT ON candidates_statistics TO archeoscope_user;

-- Mensaje de éxito
DO $$
BEGIN
    RAISE NOTICE '✅ Tabla archaeological_candidates creada exitosamente';
    RAISE NOTICE '✅ Índices creados para búsquedas eficientes';
    RAISE NOTICE '✅ Vistas priority_candidates y candidates_statistics disponibles';
END $$;
