-- Agregar columnas faltantes a archaeological_candidate_analyses
-- Para soportar los nuevos endpoints de consulta

-- Agregar anomaly_score (score de anomalía detectada)
ALTER TABLE archaeological_candidate_analyses 
ADD COLUMN IF NOT EXISTS anomaly_score DOUBLE PRECISION DEFAULT 0.0;

-- Agregar recommended_action (acción recomendada del pipeline)
ALTER TABLE archaeological_candidate_analyses 
ADD COLUMN IF NOT EXISTS recommended_action VARCHAR(50) DEFAULT 'no_action';

-- Agregar environment_type (tipo de ambiente detectado)
ALTER TABLE archaeological_candidate_analyses 
ADD COLUMN IF NOT EXISTS environment_type VARCHAR(50);

-- Agregar confidence_level (nivel de confianza del análisis)
ALTER TABLE archaeological_candidate_analyses 
ADD COLUMN IF NOT EXISTS confidence_level DOUBLE PRECISION DEFAULT 0.0;

-- Comentarios para documentación
COMMENT ON COLUMN archaeological_candidate_analyses.anomaly_score IS 'Score de anomalía detectada (0.0-1.0)';
COMMENT ON COLUMN archaeological_candidate_analyses.recommended_action IS 'Acción recomendada: no_action, further_analysis, priority_investigation';
COMMENT ON COLUMN archaeological_candidate_analyses.environment_type IS 'Tipo de ambiente: desert, tropical_forest, polar_ice, etc.';
COMMENT ON COLUMN archaeological_candidate_analyses.confidence_level IS 'Nivel de confianza del análisis (0.0-1.0)';
