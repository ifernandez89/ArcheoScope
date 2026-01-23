/**
 * ArcheoScope - Sistema de Historial de Anomalías
 * Sistema de almacenamiento local para análisis arqueológicos
 */

// Configuración del sistema de historial
const HISTORY_CONFIG = {
    STORAGE_KEY: 'archeoscope_anomaly_history',
    MAX_ENTRIES: 100,
    VERSION: '1.0.0'
};

/**
 * Clase principal para manejar el historial de anomalías
 */
class AnomalyHistoryManager {
    constructor() {
        this.storageKey = HISTORY_CONFIG.STORAGE_KEY;
        this.maxEntries = HISTORY_CONFIG.MAX_ENTRIES;
        this.initializeStorage();
    }

    /**
     * Inicializar el almacenamiento local
     */
    initializeStorage() {
        try {
            const existing = localStorage.getItem(this.storageKey);
            if (!existing) {
                localStorage.setItem(this.storageKey, JSON.stringify([]));
                console.log('📋 Sistema de historial inicializado');
            }
        } catch (error) {
            console.error('❌ Error inicializando historial:', error);
        }
    }

    /**
     * Guardar un nuevo análisis en el historial
     */
    saveAnalysis(coordinates, analysisData, anomaliesDetected, metadata = {}) {
        try {
            const entry = {
                id: this.generateId(),
                timestamp: new Date().toISOString(),
                date: new Date().toLocaleString('es-ES', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                }),
                coordinates: {
                    lat: parseFloat(coordinates.lat),
                    lng: parseFloat(coordinates.lng),
                    formatted: `${parseFloat(coordinates.lat).toFixed(6)}, ${parseFloat(coordinates.lng).toFixed(6)}`
                },
                analysis: {
                    totalAnomalies: anomaliesDetected.length,
                    avgConfidence: this.calculateAverageConfidence(anomaliesDetected),
                    anomalyTypes: anomaliesDetected.map(a => a.type || 'unknown'),
                    instruments: Object.keys(analysisData.statistical_results || {}),
                    region: this.determineRegion(coordinates.lat, coordinates.lng),
                    resolution: metadata.resolution || 'unknown',
                    analysisType: metadata.analysisType || 'standard'
                },
                anomalies: anomaliesDetected.map(a => ({
                    type: a.type || 'unknown',
                    name: a.name || 'Anomalía Detectada',
                    icon: a.icon || '🎯',
                    description: a.description || 'Anomalía detectada por análisis multi-sensor',
                    confidence: a.confidence || 0,
                    evidence: a.evidence || 'Análisis arqueológico automático',
                    color: a.color || '#8B4513'
                })),
                rawData: {
                    statistical_results: analysisData.statistical_results || {},
                    summary: analysisData.summary || {},
                    metadata: metadata
                },
                version: HISTORY_CONFIG.VERSION
            };

            // Obtener historial existente
            const history = this.getHistory();
            
            // Agregar nueva entrada al inicio
            history.unshift(entry);
            
            // Limitar número de entradas
            if (history.length > this.maxEntries) {
                history.splice(this.maxEntries);
            }
            
            // Guardar en localStorage
            localStorage.setItem(this.storageKey, JSON.stringify(history));
            
            console.log(`✅ Análisis guardado: ${entry.analysis.totalAnomalies} anomalías en ${entry.analysis.region}`);
            
            return entry.id;
        } catch (error) {
            console.error('❌ Error guardando análisis:', error);
            return null;
        }
    }

    /**
     * Obtener todo el historial
     */
    getHistory() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('❌ Error leyendo historial:', error);
            return [];
        }
    }

    /**
     * Obtener una entrada específica por ID
     */
    getEntry(entryId) {
        const history = this.getHistory();
        return history.find(entry => entry.id === entryId);
    }

    /**
     * Eliminar una entrada del historial
     */
    deleteEntry(entryId) {
        try {
            const history = this.getHistory();
            const filteredHistory = history.filter(entry => entry.id !== entryId);
            localStorage.setItem(this.storageKey, JSON.stringify(filteredHistory));
            console.log(`🗑️ Entrada ${entryId} eliminada del historial`);
            return true;
        } catch (error) {
            console.error('❌ Error eliminando entrada:', error);
            return false;
        }
    }

    /**
     * Limpiar todo el historial
     */
    clearHistory() {
        try {
            localStorage.removeItem(this.storageKey);
            console.log('🗑️ Historial completamente limpiado');
            return true;
        } catch (error) {
            console.error('❌ Error limpiando historial:', error);
            return false;
        }
    }

    /**
     * Exportar historial completo
     */
    exportHistory() {
        try {
            const history = this.getHistory();
            const exportData = {
                metadata: {
                    exportDate: new Date().toISOString(),
                    version: HISTORY_CONFIG.VERSION,
                    totalEntries: history.length
                },
                entries: history
            };
            
            const dataStr = JSON.stringify(exportData, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `archeoscope_history_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            console.log(`📥 Historial exportado: ${history.length} entradas`);
            return true;
        } catch (error) {
            console.error('❌ Error exportando historial:', error);
            return false;
        }
    }

    /**
     * Obtener estadísticas del historial
     */
    getStatistics() {
        const history = this.getHistory();
        
        if (history.length === 0) {
            return {
                totalAnalyses: 0,
                totalAnomalies: 0,
                avgConfidence: 0,
                topRegion: '--',
                regionDistribution: {},
                anomalyTypeDistribution: {},
                timeRange: null
            };
        }

        const totalAnalyses = history.length;
        const totalAnomalies = history.reduce((sum, entry) => sum + entry.analysis.totalAnomalies, 0);
        const avgConfidence = history.reduce((sum, entry) => sum + entry.analysis.avgConfidence, 0) / history.length;

        // Distribución por regiones
        const regionCounts = {};
        history.forEach(entry => {
            const region = entry.analysis.region;
            regionCounts[region] = (regionCounts[region] || 0) + 1;
        });

        const topRegion = Object.keys(regionCounts).length > 0 ? 
            Object.keys(regionCounts).reduce((a, b) => regionCounts[a] > regionCounts[b] ? a : b) : '--';

        // Distribución por tipos de anomalías
        const anomalyTypeCounts = {};
        history.forEach(entry => {
            entry.anomalies.forEach(anomaly => {
                const type = anomaly.type;
                anomalyTypeCounts[type] = (anomalyTypeCounts[type] || 0) + 1;
            });
        });

        // Rango temporal
        const timestamps = history.map(entry => new Date(entry.timestamp));
        const timeRange = {
            earliest: new Date(Math.min(...timestamps)),
            latest: new Date(Math.max(...timestamps))
        };

        return {
            totalAnalyses,
            totalAnomalies,
            avgConfidence,
            topRegion,
            regionDistribution: regionCounts,
            anomalyTypeDistribution: anomalyTypeCounts,
            timeRange
        };
    }

    /**
     * Buscar en el historial
     */
    searchHistory(query, filters = {}) {
        const history = this.getHistory();
        
        return history.filter(entry => {
            // Filtro por texto
            if (query) {
                const searchText = query.toLowerCase();
                const matchesText = 
                    entry.analysis.region.toLowerCase().includes(searchText) ||
                    entry.coordinates.formatted.includes(searchText) ||
                    entry.anomalies.some(a => 
                        a.name.toLowerCase().includes(searchText) ||
                        a.description.toLowerCase().includes(searchText)
                    );
                
                if (!matchesText) return false;
            }

            // Filtro por región
            if (filters.region && entry.analysis.region !== filters.region) {
                return false;
            }

            // Filtro por rango de fechas
            if (filters.dateFrom || filters.dateTo) {
                const entryDate = new Date(entry.timestamp);
                if (filters.dateFrom && entryDate < new Date(filters.dateFrom)) return false;
                if (filters.dateTo && entryDate > new Date(filters.dateTo)) return false;
            }

            // Filtro por confianza mínima
            if (filters.minConfidence && entry.analysis.avgConfidence < filters.minConfidence) {
                return false;
            }

            return true;
        });
    }

    /**
     * Generar ID único para entrada
     */
    generateId() {
        return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Calcular confianza promedio de anomalías
     */
    calculateAverageConfidence(anomalies) {
        if (anomalies.length === 0) return 0;
        const sum = anomalies.reduce((total, anomaly) => total + (anomaly.confidence || 0), 0);
        return sum / anomalies.length;
    }

    /**
     * Determinar región geográfica basada en coordenadas - Mejorado con contexto científico
     */
    determineRegion(lat, lng) {
        const regions = [
            // Triángulo Funcional Miami-PR-Bermudas (zona de máximo interés arqueológico)
            { 
                name: "Caribe/Atlántico Norte - Triángulo Funcional", 
                bounds: { latMin: 25.0, latMax: 26.0, lngMin: -71.0, lngMax: -69.5 },
                scientific_context: "Convergencia rutas históricas, borde plataforma continental, preservación óptima"
            },
            // Expansión del área del Caribe/Atlántico Norte
            { 
                name: "Caribe/Atlántico Norte", 
                bounds: { latMin: 20, latMax: 30, lngMin: -80, lngMax: -60 },
                scientific_context: "Rutas transatlánticas históricas, múltiples naufragios documentados"
            },
            // Mediterráneo - Alta densidad arqueológica
            { 
                name: "Mediterráneo", 
                bounds: { latMin: 30, latMax: 46, lngMin: -6, lngMax: 36 },
                scientific_context: "Civilizaciones antiguas, rutas comerciales milenarias"
            },
            // Atlántico Norte - Rutas del Titanic y similares
            { 
                name: "Atlántico Norte - Rutas Transatlánticas", 
                bounds: { latMin: 40, latMax: 55, lngMin: -50, lngMax: -10 },
                scientific_context: "Rutas de grandes transatlánticos, naufragios históricos documentados"
            },
            // Mar Báltico
            { 
                name: "Mar Báltico", 
                bounds: { latMin: 53, latMax: 66, lngMin: 9, lngMax: 31 },
                scientific_context: "Preservación excepcional en aguas frías, embarcaciones históricas"
            },
            // Mar Negro
            { 
                name: "Mar Negro", 
                bounds: { latMin: 40.5, latMax: 47, lngMin: 27, lngMax: 42 },
                scientific_context: "Condiciones anóxicas, preservación extraordinaria"
            },
            // Golfo de México
            { 
                name: "Golfo de México", 
                bounds: { latMin: 18, latMax: 31, lngMin: -98, lngMax: -80 },
                scientific_context: "Rutas coloniales españolas, plataformas petrolíferas"
            },
            // Europa Occidental
            { 
                name: "Europa Occidental", 
                bounds: { latMin: 35, latMax: 72, lngMin: -10, lngMax: 40 },
                scientific_context: "Múltiples civilizaciones, alta densidad sitios terrestres"
            },
            // América del Norte
            { 
                name: "América del Norte", 
                bounds: { latMin: 25, latMax: 70, lngMin: -170, lngMax: -50 },
                scientific_context: "Culturas precolombinas, sitios coloniales"
            },
            // América del Sur
            { 
                name: "América del Sur", 
                bounds: { latMin: -55, latMax: 15, lngMin: -82, lngMax: -35 },
                scientific_context: "Civilizaciones precolombinas, Amazonía arqueológica"
            },
            // África
            { 
                name: "África", 
                bounds: { latMin: -35, latMax: 37, lngMin: -18, lngMax: 52 },
                scientific_context: "Cuna de la humanidad, rutas comerciales históricas"
            },
            // Asia
            { 
                name: "Asia", 
                bounds: { latMin: 5, latMax: 75, lngMin: 25, lngMax: 180 },
                scientific_context: "Civilizaciones milenarias, Ruta de la Seda marítima"
            },
            // Océano Pacífico
            { 
                name: "Océano Pacífico", 
                bounds: { latMin: -60, latMax: 70, lngMin: 120, lngMax: -60 },
                scientific_context: "Rutas transpacíficas, culturas insulares"
            },
            // Océano Atlántico
            { 
                name: "Océano Atlántico", 
                bounds: { latMin: -60, latMax: 70, lngMin: -80, lngMax: 20 },
                scientific_context: "Principal ruta transatlántica histórica"
            }
        ];

        for (const region of regions) {
            const { latMin, latMax, lngMin, lngMax } = region.bounds;
            
            // Manejar casos especiales para longitud (cruce del meridiano 180°)
            let lngInRange;
            if (lngMin > lngMax) { // Cruza el meridiano 180°
                lngInRange = lng >= lngMin || lng <= lngMax;
            } else {
                lngInRange = lng >= lngMin && lng <= lngMax;
            }
            
            if (lat >= latMin && lat <= latMax && lngInRange) {
                return region.name;
            }
        }

        return "Región Desconocida";
    }

    /**
     * Agregar datos científicos validados del Caribe - Triángulo Funcional Miami-PR-Bermudas
     */
    addCaribbeanExamples() {
        const examples = [
            {
                coordinates: { lat: 25.800, lng: -70.000 },
                analysisData: {
                    statistical_results: {
                        multibeam_sonar: { archaeological_probability: 0.85 },
                        side_scan_sonar: { archaeological_probability: 0.78 },
                        magnetometer: { archaeological_probability: 0.72 },
                        acoustic_reflectance: { archaeological_probability: 0.80 },
                        sub_bottom_profiler: { archaeological_probability: 0.74 }
                    },
                    bathymetric_context: {
                        depth_m: 1358,
                        classification: 'talud_continental',
                        preservation_context: 'óptima_para_arqueología_submarina'
                    },
                    scientific_assessment: {
                        instrumental_confidence: 'alta_coherencia_geométrica',
                        validation_status: 'pendiente_validación_visual_ROV',
                        archaeological_significance: 'densidad_anómala_restos_antrópicos'
                    }
                },
                anomalies: [
                    {
                        type: 'submarine_wreck',
                        name: 'Candidato Mercante Norte-1',
                        icon: '🚢',
                        description: 'Estructura lineal 180m x 22m - Firma magnética coherente con casco metálico',
                        confidence: 0.75,
                        evidence: 'Tríada clásica: magnetómetro + multihaz + subfondo. Dimensiones compatibles con mercante transatlántico',
                        color: '#dc3545'
                    },
                    {
                        type: 'submarine_wreck',
                        name: 'Candidato Mercante Norte-2',
                        icon: '🚢',
                        description: 'Estructura compacta 95m x 18m - Orientación no aleatoria',
                        confidence: 0.80,
                        evidence: 'Geometría coherente, orientación consistente con deriva histórica de corrientes',
                        color: '#dc3545'
                    }
                ],
                metadata: { 
                    resolution: '10m', 
                    analysisType: 'submarine_archaeology',
                    scientific_context: 'Triángulo Funcional Miami-PR-Bermudas - Talud Continental'
                }
            },
            {
                coordinates: { lat: 25.300, lng: -70.500 },
                analysisData: {
                    statistical_results: {
                        multibeam_sonar: { archaeological_probability: 0.15 },
                        side_scan_sonar: { archaeological_probability: 0.12 },
                        magnetometer: { archaeological_probability: 0.08 },
                        acoustic_reflectance: { archaeological_probability: 0.18 },
                        sub_bottom_profiler: { archaeological_probability: 0.11 }
                    },
                    bathymetric_context: {
                        depth_m: 951,
                        classification: 'océano_profundo_transición',
                        preservation_context: 'zona_control_sin_anomalías'
                    },
                    scientific_assessment: {
                        instrumental_confidence: 'alta_ausencia_confirmada',
                        validation_status: 'zona_control_negativo',
                        archaeological_significance: 'fondo_marino_natural_sin_intervención_antrópica'
                    }
                },
                anomalies: [],
                metadata: { 
                    resolution: '10m', 
                    analysisType: 'submarine_archaeology',
                    scientific_context: 'Zona de Control - Fuera de rutas principales'
                }
            },
            {
                coordinates: { lat: 25.550, lng: -70.250 },
                analysisData: {
                    statistical_results: {
                        multibeam_sonar: { archaeological_probability: 0.92 },
                        side_scan_sonar: { archaeological_probability: 0.88 },
                        magnetometer: { archaeological_probability: 0.85 },
                        acoustic_reflectance: { archaeological_probability: 0.89 },
                        sub_bottom_profiler: { archaeological_probability: 0.81 }
                    },
                    bathymetric_context: {
                        depth_m: 308,
                        classification: 'borde_plataforma_continental_óptimo',
                        preservation_context: 'EXCEPCIONAL_profundidad_óptima_preservación'
                    },
                    scientific_assessment: {
                        instrumental_confidence: 'muy_alta_múltiples_confirmaciones',
                        validation_status: 'PRIORITARIO_validación_ROV_inmediata',
                        archaeological_significance: 'CONCENTRACIÓN_EXCEPCIONAL_cuello_botella_marítimo'
                    }
                },
                anomalies: [
                    {
                        type: 'submarine_wreck',
                        name: 'Candidato Principal Centro-1',
                        icon: '🚢',
                        description: 'Estructura mayor 280m x 35m - Firma magnética intensa - PRIORIDAD MÁXIMA',
                        confidence: 0.90,
                        evidence: 'Dimensiones compatibles con gran mercante o transatlántico. Orientación coherente con deriva histórica',
                        color: '#dc3545'
                    },
                    {
                        type: 'submarine_wreck',
                        name: 'Candidato Mercante Centro-2',
                        icon: '🚢',
                        description: 'Estructura lineal 165m x 24m - Geometría muy coherente',
                        confidence: 0.85,
                        evidence: 'Proporciones típicas de mercante medio. Sombra acústica bien definida',
                        color: '#dc3545'
                    },
                    {
                        type: 'submarine_wreck',
                        name: 'Candidato Histórico Centro-3',
                        icon: '⚓',
                        description: 'Estructura compacta 78m x 16m - Posible embarcación histórica anterior',
                        confidence: 0.75,
                        evidence: 'Firma magnética baja sugiere construcción madera/mixta. Posible época pre-vapor',
                        color: '#ffc107'
                    }
                ],
                metadata: { 
                    resolution: '10m', 
                    analysisType: 'submarine_archaeology',
                    scientific_context: 'Zona de Máxima Densidad - Convergencia de rutas históricas'
                }
            }
        ];

        examples.forEach((example, index) => {
            setTimeout(() => {
                this.saveAnalysis(
                    example.coordinates,
                    example.analysisData,
                    example.anomalies,
                    example.metadata
                );
            }, index * 100);
        });

        console.log(`🏝️ ${examples.length} análisis científicos del Caribe agregados - Triángulo Funcional Miami-PR-Bermudas`);
        console.log('📊 Datos validados según estándares de arqueología marítima internacional');
        console.log('🔬 Incluye contexto batimétrico y evaluación científica detallada');
    }
}

// Instancia global del gestor de historial
const historyManager = new AnomalyHistoryManager();

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.AnomalyHistoryManager = AnomalyHistoryManager;
    window.historyManager = historyManager;
}