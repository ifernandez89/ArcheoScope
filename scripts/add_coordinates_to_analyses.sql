-- Agregar columnas de coordenadas a archaeological_candidate_analyses
-- Para poder consultar análisis por ubicación geográfica

ALTER TABLE archaeological_candidate_analyses
ADD COLUMN IF NOT EXISTS latitude DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS longitude DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS lat_min DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS lat_max DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS lon_min DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS lon_max DOUBLE PRECISION;

-- Crear índice espacial para búsquedas eficientes
CREATE INDEX IF NOT EXISTS idx_analyses_coordinates 
ON archaeological_candidate_analyses(latitude, longitude);

-- Comentarios
COMMENT ON COLUMN archaeological_candidate_analyses.latitude IS 'Latitud del centro del área analizada';
COMMENT ON COLUMN archaeological_candidate_analyses.longitude IS 'Longitud del centro del área analizada';
COMMENT ON COLUMN archaeological_candidate_analyses.lat_min IS 'Latitud mínima del bounding box';
COMMENT ON COLUMN archaeological_candidate_analyses.lat_max IS 'Latitud máxima del bounding box';
COMMENT ON COLUMN archaeological_candidate_analyses.lon_min IS 'Longitud mínima del bounding box';
COMMENT ON COLUMN archaeological_candidate_analyses.lon_max IS 'Longitud máxima del bounding box';
