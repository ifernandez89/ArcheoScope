-- ============================================================================
-- Tabla: known_archaeological_sites
-- ============================================================================
-- 
-- Almacena sitios arqueológicos conocidos como ANCLAS CONTEXTUALES.
-- 
-- NO requiere mediciones satelitales, solo metadata básica:
-- - Nombre, tipo, ambiente, terreno, coordenadas, confianza
-- 
-- Uso: Validación contextual, filtros de plausibilidad, control negativo
-- ============================================================================

CREATE TABLE IF NOT EXISTS known_archaeological_sites (
    id SERIAL PRIMARY KEY,
    
    -- Identificación
    name VARCHAR(255) NOT NULL,
    site_type VARCHAR(50),              -- temple, city, settlement, tomb, fortress, ceremonial
    
    -- Contexto ambiental
    environment VARCHAR(50),             -- arid, semi_arid, plateau, mountain, coastal, forest, grassland
    terrain VARCHAR(50),                 -- plateau, valley, coastal, desert, mountain, etc.
    
    -- Ubicación
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    
    -- Metadata
    confidence_level VARCHAR(20),        -- HIGH, MEDIUM, LOW
    has_documented_cavities BOOLEAN DEFAULT FALSE,
    notes TEXT,
    
    -- Auditoría
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_confidence CHECK (confidence_level IN ('HIGH', 'MEDIUM', 'LOW')),
    CONSTRAINT chk_lat CHECK (lat BETWEEN -90 AND 90),
    CONSTRAINT chk_lon CHECK (lon BETWEEN -180 AND 180)
);

-- Índices para búsquedas eficientes
CREATE INDEX IF NOT EXISTS idx_known_sites_coords ON known_archaeological_sites (lat, lon);
CREATE INDEX IF NOT EXISTS idx_known_sites_env ON known_archaeological_sites (environment);
CREATE INDEX IF NOT EXISTS idx_known_sites_type ON known_archaeological_sites (site_type);
CREATE INDEX IF NOT EXISTS idx_known_sites_confidence ON known_archaeological_sites (confidence_level);

-- Índice geoespacial (si PostGIS está disponible)
-- CREATE INDEX IF NOT EXISTS idx_known_sites_geom ON known_archaeological_sites USING GIST (ST_MakePoint(lon, lat));

-- Comentarios
COMMENT ON TABLE known_archaeological_sites IS 'Sitios arqueológicos conocidos usados como anclas contextuales para validación';
COMMENT ON COLUMN known_archaeological_sites.name IS 'Nombre del sitio arqueológico';
COMMENT ON COLUMN known_archaeological_sites.site_type IS 'Tipo de sitio: temple, city, settlement, tomb, fortress, ceremonial';
COMMENT ON COLUMN known_archaeological_sites.environment IS 'Tipo de ambiente: arid, semi_arid, plateau, mountain, coastal, forest, grassland';
COMMENT ON COLUMN known_archaeological_sites.terrain IS 'Tipo de terreno específico';
COMMENT ON COLUMN known_archaeological_sites.has_documented_cavities IS 'Si el sitio tiene cavidades/estructuras subterráneas documentadas';
COMMENT ON COLUMN known_archaeological_sites.confidence_level IS 'Nivel de confianza en la identificación del sitio';

-- ============================================================================
-- Datos de ejemplo (sitios conocidos del Medio Oriente y Norte de África)
-- ============================================================================

INSERT INTO known_archaeological_sites 
(name, site_type, environment, terrain, lat, lon, confidence_level, has_documented_cavities, notes)
VALUES
-- Egipto
('Giza Pyramids', 'ceremonial', 'arid', 'plateau', 29.9792, 31.1342, 'HIGH', true, 'Pirámides con cámaras internas documentadas'),
('Valley of the Kings', 'tomb', 'arid', 'valley', 25.7402, 32.6014, 'HIGH', true, 'Tumbas excavadas en roca'),
('Abu Simbel', 'temple', 'arid', 'desert', 22.3372, 31.6258, 'HIGH', true, 'Templos excavados en roca'),
('Karnak', 'temple', 'arid', 'plateau', 25.7188, 32.6573, 'HIGH', false, 'Complejo de templos superficiales'),

-- Jordania
('Petra', 'city', 'arid', 'plateau', 30.3285, 35.4444, 'HIGH', true, 'Ciudad excavada en roca con tumbas'),
('Jerash', 'city', 'semi_arid', 'plateau', 32.2719, 35.8906, 'HIGH', false, 'Ciudad romana superficial'),
('Umm Qais', 'settlement', 'semi_arid', 'plateau', 32.6525, 35.6844, 'HIGH', false, 'Asentamiento romano'),

-- Siria
('Palmyra', 'city', 'arid', 'desert', 34.5561, 38.2692, 'HIGH', false, 'Ciudad oasis en desierto'),
('Bosra', 'city', 'semi_arid', 'plateau', 32.5189, 36.4822, 'HIGH', false, 'Ciudad romana'),

-- Irak
('Babylon', 'city', 'semi_arid', 'valley', 32.5355, 44.4275, 'HIGH', false, 'Ciudad mesopotámica'),
('Ur', 'city', 'arid', 'desert', 30.9625, 46.1031, 'HIGH', false, 'Ciudad sumeria'),

-- Perú
('Machu Picchu', 'city', 'mountain', 'mountain', -13.1631, -72.5450, 'HIGH', false, 'Ciudad inca en montaña'),
('Nazca Lines', 'ceremonial', 'arid', 'desert', -14.7390, -75.1300, 'HIGH', false, 'Geoglifos en desierto'),
('Caral', 'city', 'arid', 'valley', -10.8939, -77.5208, 'HIGH', false, 'Ciudad pre-cerámica'),

-- México
('Teotihuacan', 'city', 'semi_arid', 'plateau', 19.6925, -98.8438, 'HIGH', true, 'Pirámides con túneles'),
('Chichen Itza', 'city', 'semi_arid', 'plateau', 20.6843, -88.5678, 'HIGH', true, 'Pirámides con cenotes'),
('Palenque', 'city', 'forest', 'mountain', 17.4839, -92.0458, 'HIGH', true, 'Templos con criptas'),

-- Grecia
('Delphi', 'ceremonial', 'mountain', 'mountain', 38.4824, 22.5010, 'HIGH', false, 'Santuario en montaña'),
('Mycenae', 'city', 'semi_arid', 'plateau', 37.7308, 22.7567, 'HIGH', true, 'Ciudad con tumbas'),

-- Turquía
('Ephesus', 'city', 'coastal', 'coastal', 37.9395, 27.3408, 'HIGH', false, 'Ciudad costera'),
('Göbekli Tepe', 'ceremonial', 'semi_arid', 'plateau', 37.2233, 38.9225, 'HIGH', false, 'Templo neolítico'),

-- China
('Terracotta Army', 'tomb', 'semi_arid', 'plateau', 34.3848, 109.2785, 'HIGH', true, 'Mausoleo con cámaras subterráneas'),

-- Camboya
('Angkor Wat', 'temple', 'forest', 'plateau', 13.4125, 103.8670, 'HIGH', false, 'Complejo de templos'),

-- India
('Ajanta Caves', 'temple', 'semi_arid', 'mountain', 20.5519, 75.7033, 'HIGH', true, 'Templos excavados en roca'),
('Ellora Caves', 'temple', 'semi_arid', 'mountain', 20.0269, 75.1792, 'HIGH', true, 'Templos excavados en roca')

ON CONFLICT DO NOTHING;

-- ============================================================================
-- Verificación
-- ============================================================================

-- Contar sitios por ambiente
SELECT 
    environment,
    COUNT(*) as site_count,
    SUM(CASE WHEN has_documented_cavities THEN 1 ELSE 0 END) as with_cavities,
    SUM(CASE WHEN confidence_level = 'HIGH' THEN 1 ELSE 0 END) as high_confidence
FROM known_archaeological_sites
GROUP BY environment
ORDER BY site_count DESC;

-- Mostrar distribución geográfica
SELECT 
    CASE 
        WHEN lat > 30 THEN 'Northern'
        WHEN lat > 0 THEN 'Equatorial North'
        WHEN lat > -30 THEN 'Equatorial South'
        ELSE 'Southern'
    END as region,
    COUNT(*) as site_count
FROM known_archaeological_sites
GROUP BY region
ORDER BY site_count DESC;

-- Sitios con cavidades documentadas
SELECT name, site_type, environment, has_documented_cavities
FROM known_archaeological_sites
WHERE has_documented_cavities = true
ORDER BY environment, name;

COMMIT;
