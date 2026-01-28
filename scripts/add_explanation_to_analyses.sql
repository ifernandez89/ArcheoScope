-- Agregar campo de explicación científica a archaeological_candidate_analyses
-- Para guardar la explicación determinística en lenguaje natural

ALTER TABLE archaeological_candidate_analyses
ADD COLUMN IF NOT EXISTS scientific_explanation TEXT,
ADD COLUMN IF NOT EXISTS explanation_type VARCHAR(50) DEFAULT 'deterministic';

-- Comentarios
COMMENT ON COLUMN archaeological_candidate_analyses.scientific_explanation IS 'Explicación científica en lenguaje natural del resultado del análisis';
COMMENT ON COLUMN archaeological_candidate_analyses.explanation_type IS 'Tipo de explicación: deterministic, ai_assisted, hybrid';
