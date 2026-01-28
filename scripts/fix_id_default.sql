-- Arreglar el campo id para que genere UUIDs automáticamente
ALTER TABLE archaeological_sites 
ALTER COLUMN id SET DEFAULT gen_random_uuid()::text;

-- Verificar
\d archaeological_sites
