-- Clasificar los últimos 55 registros con environmentType UNKNOWN
-- Basándose en las coordenadas y el terreno

-- Sitios agregados manualmente que necesitan environmentType

UPDATE archaeological_sites
SET "environmentType" = 
    CASE
        -- Perú - Andes (montaña)
        WHEN latitude BETWEEN -18 AND -3 AND longitude BETWEEN -82 AND -70 
             AND latitude < -10 THEN 'MOUNTAIN'::"EnvironmentType"
        
        -- Perú - Costa (desierto)
        WHEN latitude BETWEEN -18 AND -3 AND longitude BETWEEN -82 AND -70 
             AND latitude >= -10 THEN 'DESERT'::"EnvironmentType"
        
        -- Colombia - San Agustín (montaña/bosque)
        WHEN latitude BETWEEN 1 AND 3 AND longitude BETWEEN -77 AND -75 THEN 'MOUNTAIN'::"EnvironmentType"
        
        -- Brasil - Amazonía (bosque)
        WHEN latitude BETWEEN -5 AND -3 AND longitude BETWEEN -62 AND -60 THEN 'FOREST'::"EnvironmentType"
        
        -- Myanmar - Bagan (semi-árido)
        WHEN latitude BETWEEN 21 AND 22 AND longitude BETWEEN 94 AND 95 THEN 'SEMI_ARID'::"EnvironmentType"
        
        -- Isla de Pascua (costero)
        WHEN latitude BETWEEN -28 AND -27 AND longitude BETWEEN -110 AND -109 THEN 'COASTAL'::"EnvironmentType"
        
        -- Default: clasificar por latitud
        WHEN latitude > 60 THEN 'FOREST'::"EnvironmentType"  -- Norte
        WHEN latitude < -30 THEN 'GRASSLAND'::"EnvironmentType"  -- Sur
        WHEN ABS(latitude) < 30 AND longitude BETWEEN -20 AND 60 THEN 'DESERT'::"EnvironmentType"  -- Trópicos secos
        ELSE 'FOREST'::"EnvironmentType"  -- Default
    END
WHERE "environmentType" = 'UNKNOWN';
