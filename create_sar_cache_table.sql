-- Tabla de cache para datos SAR
-- Evita re-descargar datos satelitales costosos

CREATE TABLE IF NOT EXISTS sar_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identificación de la región
    lat_min DECIMAL(10, 6) NOT NULL,
    lat_max DECIMAL(10, 6) NOT NULL,
    lon_min DECIMAL(10, 6) NOT NULL,
    lon_max DECIMAL(10, 6) NOT NULL,
    
    -- Hash único de la región (para búsqueda rápida)
    region_hash VARCHAR(64) NOT NULL UNIQUE,
    
    -- Datos SAR
    vv_mean DECIMAL(10, 4),
    vh_mean DECIMAL(10, 4),
    vv_vh_ratio DECIMAL(10, 4),
    backscatter_std DECIMAL(10, 4),
    
    -- Metadatos
    source VARCHAR(100) NOT NULL,
    acquisition_date TIMESTAMP NOT NULL,
    resolution_m INTEGER NOT NULL,
    scene_id VARCHAR(200),
    
    -- Control
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,  -- Cache expira después de X días
    
    -- Índices para búsqueda rápida
    CONSTRAINT sar_cache_region_check CHECK (
        lat_min < lat_max AND lon_min < lon_max
    )
);

-- Índice para búsqueda por hash
CREATE INDEX IF NOT EXISTS idx_sar_cache_hash ON sar_cache(region_hash);

-- Índice para búsqueda por región
CREATE INDEX IF NOT EXISTS idx_sar_cache_region ON sar_cache(lat_min, lat_max, lon_min, lon_max);

-- Índice para limpieza de cache expirado
CREATE INDEX IF NOT EXISTS idx_sar_cache_expires ON sar_cache(expires_at);

-- Comentarios
COMMENT ON TABLE sar_cache IS 'Cache de datos SAR para evitar re-descargas costosas';
COMMENT ON COLUMN sar_cache.region_hash IS 'MD5 hash de lat_min,lat_max,lon_min,lon_max para búsqueda rápida';
COMMENT ON COLUMN sar_cache.expires_at IS 'Fecha de expiración del cache (NULL = no expira)';
