-- Habilitar extensiones UUID para PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Verificar que funcionan
SELECT gen_random_uuid();
