-- Agregar analysis_id a measurements para vincular mediciones con análisis específicos
-- Esto permite consultar exactamente qué instrumentos se usaron en cada análisis

ALTER TABLE measurements
ADD COLUMN IF NOT EXISTS analysis_id INTEGER;

-- Crear índice para búsquedas eficientes
CREATE INDEX IF NOT EXISTS idx_measurements_analysis_id 
ON measurements(analysis_id);

-- Comentario
COMMENT ON COLUMN measurements.analysis_id IS 'ID del análisis al que pertenece esta medición (INTEGER, no UUID)';
