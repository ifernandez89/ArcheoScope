-- Corregir tipo de analysis_id de UUID a INTEGER

-- Eliminar columna existente
ALTER TABLE measurements DROP COLUMN IF EXISTS analysis_id;

-- Recrear como INTEGER
ALTER TABLE measurements ADD COLUMN analysis_id INTEGER;

-- Recrear índice
CREATE INDEX IF NOT EXISTS idx_measurements_analysis_id 
ON measurements(analysis_id);

-- Comentario
COMMENT ON COLUMN measurements.analysis_id IS 'ID del análisis al que pertenece esta medición (INTEGER)';
