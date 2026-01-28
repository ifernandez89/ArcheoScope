-- Arreglar el campo updatedAt para que tenga un default
ALTER TABLE archaeological_sites 
ALTER COLUMN "updatedAt" SET DEFAULT CURRENT_TIMESTAMP;

-- Verificar
SELECT column_name, column_default 
FROM information_schema.columns 
WHERE table_name = 'archaeological_sites' 
AND column_name IN ('id', 'createdAt', 'updatedAt');
