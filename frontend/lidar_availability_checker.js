/**
 * Sistema de verificación de disponibilidad real de LiDAR
 * Verifica si hay datos LiDAR reales disponibles en coordenadas específicas
 */

class LiDARAvailabilityChecker {
    constructor() {
        // Base de datos de regiones con cobertura LiDAR real conocida
        this.lidarCoverageRegions = [
            // Estados Unidos - Cobertura sistemática
            {
                name: "Estados Unidos Continental",
                bounds: { latMin: 24.0, latMax: 49.0, lonMin: -125.0, lonMax: -66.0 },
                coverage: "systematic",
                resolution: "1-3m",
                source: "USGS 3DEP, NOAA",
                availability: 0.95
            },
            
            // Europa Occidental - Cobertura alta
            {
                name: "Europa Occidental",
                bounds: { latMin: 35.0, latMax: 71.0, lonMin: -10.0, lonMax: 30.0 },
                coverage: "high",
                resolution: "0.5-2m",
                source: "National mapping agencies",
                availability: 0.85
            },
            
            // Reino Unido - Cobertura completa
            {
                name: "Reino Unido",
                bounds: { latMin: 49.5, latMax: 61.0, lonMin: -8.0, lonMax: 2.0 },
                coverage: "complete",
                resolution: "0.25-1m",
                source: "Environment Agency, Ordnance Survey",
                availability: 0.98
            },
            
            // Países Bajos - Cobertura completa
            {
                name: "Países Bajos",
                bounds: { latMin: 50.5, latMax: 54.0, lonMin: 3.0, lonMax: 7.5 },
                coverage: "complete",
                resolution: "0.5m",
                source: "AHN (Actueel Hoogtebestand Nederland)",
                availability: 1.0
            },
            
            // Dinamarca - Cobertura completa
            {
                name: "Dinamarca",
                bounds: { latMin: 54.0, latMax: 58.0, lonMin: 8.0, lonMax: 15.5 },
                coverage: "complete",
                resolution: "0.4m",
                source: "Danish Agency for Data Supply",
                availability: 0.99
            },
            
            // Australia - Cobertura parcial
            {
                name: "Australia Oriental",
                bounds: { latMin: -44.0, latMax: -10.0, lonMin: 110.0, lonMax: 155.0 },
                coverage: "partial",
                resolution: "1-5m",
                source: "Geoscience Australia",
                availability: 0.60
            },
            
            // Canadá - Cobertura parcial
            {
                name: "Canadá Sur",
                bounds: { latMin: 42.0, latMax: 60.0, lonMin: -141.0, lonMax: -52.0 },
                coverage: "partial",
                resolution: "1-2m",
                source: "Natural Resources Canada",
                availability: 0.45
            },
            
            // Japón - Cobertura alta
            {
                name: "Japón",
                bounds: { latMin: 24.0, latMax: 46.0, lonMin: 123.0, lonMax: 146.0 },
                coverage: "high",
                resolution: "1m",
                source: "GSI Japan",
                availability: 0.80
            },
            
            // Singapur - Cobertura completa
            {
                name: "Singapur",
                bounds: { latMin: 1.15, latMax: 1.48, lonMin: 103.6, lonMax: 104.0 },
                coverage: "complete",
                resolution: "0.5m",
                source: "Singapore Land Authority",
                availability: 1.0
            },
            
            // Nueva Zelanda - Cobertura alta
            {
                name: "Nueva Zelanda",
                bounds: { latMin: -47.5, latMax: -34.0, lonMin: 166.0, lonMax: 179.0 },
                coverage: "high",
                resolution: "1m",
                source: "LINZ",
                availability: 0.75
            }
        ];
        
        // Sitios arqueológicos específicos con LiDAR conocido
        this.archaeologicalLidarSites = [
            {
                name: "Angkor Wat, Camboya",
                coords: { lat: 13.4125, lon: 103.8670 },
                radius: 0.5, // 50km radius
                coverage: "archaeological_survey",
                resolution: "0.5m",
                source: "Khmer Archaeology LiDAR Consortium",
                availability: 1.0
            },
            {
                name: "Caracol, Belice",
                coords: { lat: 16.7622, lon: -89.1167 },
                radius: 0.2,
                coverage: "archaeological_survey",
                resolution: "1m",
                source: "PACUNAM LiDAR Initiative",
                availability: 1.0
            },
            {
                name: "Tikal, Guatemala",
                coords: { lat: 17.2222, lon: -89.6236 },
                radius: 0.3,
                coverage: "archaeological_survey",
                resolution: "1m",
                source: "PACUNAM LiDAR Initiative",
                availability: 1.0
            },
            {
                name: "Stonehenge, Reino Unido",
                coords: { lat: 51.1789, lon: -1.8262 },
                radius: 0.1,
                coverage: "archaeological_survey",
                resolution: "0.25m",
                source: "English Heritage",
                availability: 1.0
            }
        ];
    }
    
    /**
     * Verificar disponibilidad de LiDAR en coordenadas específicas
     */
    checkLiDARAvailability(lat, lon) {
        console.log(`🔍 Verificando disponibilidad de LiDAR en: ${lat.toFixed(6)}, ${lon.toFixed(6)}`);
        
        // 1. Verificar sitios arqueológicos específicos
        for (const site of this.archaeologicalLidarSites) {
            const distance = this.calculateDistance(lat, lon, site.coords.lat, site.coords.lon);
            if (distance <= site.radius) {
                console.log(`✅ LiDAR arqueológico encontrado: ${site.name}`);
                return {
                    available: true,
                    type: 'archaeological_survey',
                    source: site.source,
                    resolution: site.resolution,
                    coverage: site.coverage,
                    confidence: site.availability,
                    details: `Sitio arqueológico con LiDAR: ${site.name}`
                };
            }
        }
        
        // 2. Verificar cobertura regional sistemática
        for (const region of this.lidarCoverageRegions) {
            if (this.isInBounds(lat, lon, region.bounds)) {
                console.log(`✅ LiDAR regional encontrado: ${region.name}`);
                return {
                    available: true,
                    type: 'systematic_coverage',
                    source: region.source,
                    resolution: region.resolution,
                    coverage: region.coverage,
                    confidence: region.availability,
                    details: `Cobertura sistemática: ${region.name}`
                };
            }
        }
        
        // 3. No hay cobertura LiDAR conocida
        console.log(`❌ No hay LiDAR disponible en esta ubicación`);
        return {
            available: false,
            type: 'none',
            source: 'N/A',
            resolution: 'N/A',
            coverage: 'none',
            confidence: 0.0,
            details: 'Sin cobertura LiDAR conocida en esta región'
        };
    }
    
    /**
     * Verificar si las coordenadas están dentro de los límites
     */
    isInBounds(lat, lon, bounds) {
        return lat >= bounds.latMin && lat <= bounds.latMax && 
               lon >= bounds.lonMin && lon <= bounds.lonMax;
    }
    
    /**
     * Calcular distancia entre dos puntos (aproximación simple)
     */
    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Radio de la Tierra en km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c / 111; // Convertir a grados aproximadamente
    }
    
    /**
     * Generar etiqueta apropiada para datos LiDAR
     */
    generateLiDARLabel(availability) {
        if (!availability.available) {
            return "LiDAR-No-Disponible";
        }
        
        switch (availability.type) {
            case 'archaeological_survey':
                return `LiDAR-Arqueológico (${availability.resolution})`;
            case 'systematic_coverage':
                return `LiDAR-Sistemático (${availability.resolution})`;
            default:
                return `LiDAR-${availability.coverage}`;
        }
    }
    
    /**
     * Obtener descripción detallada de disponibilidad
     */
    getAvailabilityDescription(availability) {
        if (!availability.available) {
            return "Sin datos LiDAR reales disponibles en esta ubicación";
        }
        
        return `${availability.details} - Resolución: ${availability.resolution} - Fuente: ${availability.source}`;
    }
}

// Instancia global del verificador
window.lidarChecker = new LiDARAvailabilityChecker();
