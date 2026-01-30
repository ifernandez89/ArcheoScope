/**
 * ArcheoScope Interactive Map - Lupa Arqueológica Multi-Sensor
 * Visualización avanzada de los 10 instrumentos arqueológicos integrados
 */

class ArcheoScopeInteractiveMap {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.map = null;
        this.layers = {};
        this.instruments = {};
        this.currentAnalysis = null;
        this.isAnalyzing = false;
        this.tempMarker = null; // Marcador temporal para coordenadas ingresadas manualmente
        
        // Configuración de instrumentos
        this.instrumentConfig = {
            // Instrumentos Base (5)
            'ndvi_vegetation': {
                name: '📡 Sentinel-2/Landsat',
                type: 'optical',
                color: '#2E8B57',
                description: 'NDVI y análisis multiespectral',
                priority: 1
            },
            'thermal_lst': {
                name: '🌡️ MODIS/Landsat Térmico',
                type: 'thermal',
                color: '#FF4500',
                description: 'Temperatura superficial y anomalías térmicas',
                priority: 2
            },
            'sar_backscatter': {
                name: '📊 Sentinel-1 SAR',
                type: 'radar',
                color: '#4169E1',
                description: 'Backscatter SAR banda C',
                priority: 3
            },
            'surface_roughness': {
                name: '🌊 Scatterometer',
                type: 'roughness',
                color: '#20B2AA',
                description: 'Rugosidad superficial',
                priority: 4
            },
            'soil_salinity': {
                name: '🧂 SMOS Salinidad',
                type: 'salinity',
                color: '#DDA0DD',
                description: 'Salinidad superficial del suelo',
                priority: 5
            },
            'seismic_resonance': {
                name: '📳 IRIS Sísmico',
                type: 'seismic',
                color: '#8B4513',
                description: 'Resonancia sísmica pasiva',
                priority: 6
            },
            
            // Instrumentos Mejorados (5)
            'elevation_dem': {
                name: '🏔️ OpenTopography DEM',
                type: 'elevation',
                color: '#8B4513',
                description: 'Micro-relieve y alteraciones topográficas',
                priority: 7,
                enhanced: true,
                value: 'CRÍTICO'
            },
            'sar_l_band': {
                name: '📡 ASF PALSAR L-band',
                type: 'radar_enhanced',
                color: '#FF6347',
                description: 'Penetración bajo vegetación densa',
                priority: 8,
                enhanced: true,
                value: 'CRÍTICO'
            },
            'icesat2_profiles': {
                name: '📏 ICESat-2 Láser',
                type: 'laser',
                color: '#00CED1',
                description: 'Perfiles láser precisión centimétrica',
                priority: 9,
                enhanced: true,
                value: 'REVOLUCIONARIO'
            },
            'vegetation_height': {
                name: '🌳 GEDI Vegetación 3D',
                type: 'lidar',
                color: '#32CD32',
                description: 'Estructura 3D de vegetación',
                priority: 10,
                enhanced: true,
                value: 'ALTO'
            },
            'soil_moisture': {
                name: '💧 SMAP Humedad',
                type: 'moisture',
                color: '#1E90FF',
                description: 'Humedad del suelo y drenaje',
                priority: 11,
                enhanced: true,
                value: 'COMPLEMENTARIO'
            }
        };
        
        this.init();
    }
    
    init() {
        this.createMapContainer();
        this.createInstrumentPanel();
        this.createAnalysisPanel();
        this.createResultsPanel();
        this.initializeMap();
        this.setupEventListeners();
    }
    
    createMapContainer() {
        this.container.innerHTML = `
            <div class="archeoscope-container">
                <!-- Header -->
                <div class="archeoscope-header">
                    <h1>🏺 ArcheoScope - Lupa Arqueológica Multi-Sensor</h1>
                    <div class="status-indicators">
                        <span class="status-item">
                            <span class="status-dot active"></span>
                            10 Instrumentos Activos
                        </span>
                        <span class="status-item">
                            <span class="status-dot enhanced"></span>
                            5 Mejorados Integrados
                        </span>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="archeoscope-main">
                    <!-- Left Panel - Instruments -->
                    <div class="instruments-panel">
                        <h3>🛰️ Instrumentos Arqueológicos</h3>
                        <div class="instruments-list" id="instrumentsList"></div>
                        
                        <h3>🎯 Análisis Rápido</h3>
                        <div class="quick-analysis">
                            <button id="quickAnalysisBtn" class="btn-primary">
                                🔍 Análisis Automático
                            </button>
                            <div class="coordinates-input">
                                <input type="text" id="coordsInput" placeholder="Lat, Lon (ej: -76.75, -110.09)">
                                <button id="analyzeBtn" class="btn-secondary">Analizar</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Center - Map -->
                    <div class="map-container">
                        <div id="archaeoMap" class="map"></div>
                        <div class="map-controls">
                            <button id="layerToggle" class="map-btn">🗂️ Capas</button>
                            <button id="instrumentToggle" class="map-btn">🛰️ Instrumentos</button>
                            <button id="resultsToggle" class="map-btn">📊 Resultados</button>
                        </div>
                        
                        <!-- Loading Overlay -->
                        <div id="analysisOverlay" class="analysis-overlay hidden">
                            <div class="analysis-spinner">
                                <div class="spinner"></div>
                                <p>Analizando con 10 instrumentos...</p>
                                <div class="progress-bar">
                                    <div class="progress-fill" id="progressFill"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Right Panel - Results -->
                    <div class="results-panel">
                        <h3>📊 Resultados Multi-Sensor</h3>
                        <div id="resultsContent" class="results-content">
                            <p class="placeholder">Selecciona una región para análisis arqueológico</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    createInstrumentPanel() {
        const instrumentsList = document.getElementById('instrumentsList');
        
        Object.entries(this.instrumentConfig).forEach(([key, config]) => {
            const instrumentItem = document.createElement('div');
            instrumentItem.className = `instrument-item ${config.enhanced ? 'enhanced' : 'base'}`;
            instrumentItem.innerHTML = `
                <div class="instrument-header">
                    <span class="instrument-name">${config.name}</span>
                    ${config.enhanced ? `<span class="value-badge ${config.value.toLowerCase()}">${config.value}</span>` : ''}
                </div>
                <div class="instrument-description">${config.description}</div>
                <div class="instrument-controls">
                    <label class="toggle-switch">
                        <input type="checkbox" id="toggle_${key}" checked>
                        <span class="slider"></span>
                    </label>
                    <span class="instrument-status" id="status_${key}">Activo</span>
                </div>
            `;
            
            instrumentsList.appendChild(instrumentItem);
            
            // Event listener para toggle
            document.getElementById(`toggle_${key}`).addEventListener('change', (e) => {
                this.toggleInstrument(key, e.target.checked);
            });
        });
    }
    
    createAnalysisPanel() {
        // Ya creado en createMapContainer
    }
    
    createResultsPanel() {
        // Ya creado en createMapContainer
    }
    
    initializeMap() {
        // Inicializar mapa simple (sin dependencias externas)
        const mapElement = document.getElementById('archaeoMap');
        mapElement.innerHTML = `
            <div class="simple-map">
                <div class="map-grid" id="mapGrid"></div>
                <div class="map-overlay">
                    <div class="coordinates-display" id="coordsDisplay">
                        Lat: 0.000, Lon: 0.000
                    </div>
                </div>
            </div>
        `;
        
        this.createMapGrid();
        this.setupMapInteraction();
    }
    
    createMapGrid() {
        const mapGrid = document.getElementById('mapGrid');
        const gridSize = 20; // 20x20 grid
        
        for (let i = 0; i < gridSize * gridSize; i++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            cell.dataset.index = i;
            mapGrid.appendChild(cell);
        }
    }
    
    setupMapInteraction() {
        const mapGrid = document.getElementById('mapGrid');
        const coordsDisplay = document.getElementById('coordsDisplay');
        
        mapGrid.addEventListener('mousemove', (e) => {
            if (e.target.classList.contains('grid-cell')) {
                const index = parseInt(e.target.dataset.index);
                const row = Math.floor(index / 20);
                const col = index % 20;
                
                // Simular coordenadas
                const lat = (90 - (row * 9)).toFixed(3);
                const lon = (-180 + (col * 18)).toFixed(3);
                
                coordsDisplay.textContent = `Lat: ${lat}, Lon: ${lon}`;
            }
        });
        
        mapGrid.addEventListener('click', (e) => {
            if (e.target.classList.contains('grid-cell')) {
                this.selectMapCell(e.target);
            }
        });
    }
    
    selectMapCell(cell) {
        // Limpiar selección anterior
        document.querySelectorAll('.grid-cell.selected').forEach(c => {
            c.classList.remove('selected');
        });
        
        // Seleccionar nueva celda
        cell.classList.add('selected');
        
        // Extraer coordenadas
        const index = parseInt(cell.dataset.index);
        const row = Math.floor(index / 20);
        const col = index % 20;
        
        const lat = (90 - (row * 9)).toFixed(3);
        const lon = (-180 + (col * 18)).toFixed(3);
        
        // Actualizar input de coordenadas
        document.getElementById('coordsInput').value = `${lat}, ${lon}`;
        
        // Análisis automático si está habilitado
        if (document.getElementById('quickAnalysisBtn').classList.contains('active')) {
            this.analyzeRegion(lat, lon);
        }
    }
    
    setupEventListeners() {
        // Botón de análisis automático
        document.getElementById('quickAnalysisBtn').addEventListener('click', () => {
            this.toggleQuickAnalysis();
        });
        
        // Botón de análisis manual
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            const coords = document.getElementById('coordsInput').value;
            if (coords) {
                const [lat, lon] = coords.split(',').map(s => parseFloat(s.trim()));
                
                // Validar coordenadas
                if (isNaN(lat) || isNaN(lon)) {
                    alert('❌ Coordenadas inválidas. Formato: Lat, Lon (ej: -13.15, -72.55)');
                    return;
                }
                
                if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
                    alert('❌ Coordenadas fuera de rango. Lat: -90 a 90, Lon: -180 a 180');
                    return;
                }
                
                // CENTRAR EL MAPA en las coordenadas ingresadas
                console.log(`📍 Centrando mapa en: ${lat}, ${lon}`);
                this.map.setView([lat, lon], 13); // Zoom 13 para ver detalles
                
                // Agregar marcador temporal en la ubicación
                if (this.tempMarker) {
                    this.map.removeLayer(this.tempMarker);
                }
                this.tempMarker = L.marker([lat, lon], {
                    icon: L.divIcon({
                        className: 'temp-marker',
                        html: '<div style="background: #ff4444; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(255,68,68,0.5);"></div>',
                        iconSize: [20, 20]
                    })
                }).addTo(this.map);
                
                // Analizar región después de centrar
                setTimeout(() => {
                    this.analyzeRegion(lat, lon);
                }, 500); // Pequeño delay para que se vea el centrado
            } else {
                alert('⚠️ Por favor ingresa coordenadas (Lat, Lon)');
            }
        });
        
        // Soporte para Enter en el campo de coordenadas
        document.getElementById('coordsInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.getElementById('analyzeBtn').click();
            }
        });
        
        // Controles del mapa
        document.getElementById('layerToggle').addEventListener('click', () => {
            this.toggleLayerPanel();
        });
        
        document.getElementById('instrumentToggle').addEventListener('click', () => {
            this.toggleInstrumentPanel();
        });
        
        document.getElementById('resultsToggle').addEventListener('click', () => {
            this.toggleResultsPanel();
        });
    }
    
    toggleQuickAnalysis() {
        const btn = document.getElementById('quickAnalysisBtn');
        btn.classList.toggle('active');
        
        if (btn.classList.contains('active')) {
            btn.innerHTML = '🎯 Modo Automático ON';
            btn.style.backgroundColor = '#28a745';
        } else {
            btn.innerHTML = '🔍 Análisis Automático';
            btn.style.backgroundColor = '#007bff';
        }
    }
    
    toggleInstrument(instrumentKey, enabled) {
        const statusElement = document.getElementById(`status_${instrumentKey}`);
        
        if (enabled) {
            statusElement.textContent = 'Activo';
            statusElement.className = 'instrument-status active';
        } else {
            statusElement.textContent = 'Inactivo';
            statusElement.className = 'instrument-status inactive';
        }
        
        this.instruments[instrumentKey] = enabled;
    }
    
    async analyzeRegion(lat, lon) {
        if (this.isAnalyzing) return;
        
        this.isAnalyzing = true;
        this.showAnalysisOverlay();
        
        try {
            // Simular análisis con progreso
            await this.simulateAnalysisProgress();
            
            // Llamar a la API real
            const results = await this.callArcheoScopeAPI(lat, lon);
            
            // Mostrar resultados
            this.displayResults(results);
            
            // Actualizar visualización del mapa
            this.updateMapVisualization(results);
            
        } catch (error) {
            console.error('Error en análisis:', error);
            this.showError('Error ejecutando análisis arqueológico');
        } finally {
            this.isAnalyzing = false;
            this.hideAnalysisOverlay();
        }
    }
    
    async simulateAnalysisProgress() {
        const progressFill = document.getElementById('progressFill');
        const steps = [
            'Inicializando instrumentos...',
            'Cargando datos Sentinel-2...',
            'Procesando MODIS térmico...',
            'Analizando SAR Sentinel-1...',
            'Evaluando OpenTopography DEM...',
            'Procesando PALSAR L-band...',
            'Analizando ICESat-2...',
            'Evaluando GEDI vegetación...',
            'Procesando SMAP humedad...',
            'Integrando resultados...'
        ];
        
        for (let i = 0; i < steps.length; i++) {
            const progress = ((i + 1) / steps.length) * 100;
            progressFill.style.width = `${progress}%`;
            
            const overlay = document.querySelector('.analysis-spinner p');
            overlay.textContent = steps[i];
            
            await new Promise(resolve => setTimeout(resolve, 300));
        }
    }
    
    async callArcheoScopeAPI(lat, lon) {
        const response = await fetch('http://localhost:8003/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                lat_min: lat - 0.01,
                lat_max: lat + 0.01,
                lon_min: lon - 0.01,
                lon_max: lon + 0.01,
                resolution_m: 200,
                layers_to_analyze: Object.keys(this.instrumentConfig).filter(key => 
                    this.instruments[key] !== false
                ),
                active_rules: ['all'],
                region_name: `Interactive Analysis ${lat.toFixed(3)}, ${lon.toFixed(3)}`,
                include_explainability: true,
                include_validation_metrics: true
            })
        });
        
        if (!response.ok) {
            let errorMessage = `API Error: ${response.status}`;
            switch (response.status) {
                case 404:
                    errorMessage = '🔍 Servicio no encontrado (404) - Verifica que el backend esté ejecutándose en puerto 8003';
                    break;
                case 500:
                    errorMessage = '⚠️ Error interno del servidor (500) - Problema en el análisis arqueológico';
                    break;
                case 503:
                    errorMessage = '🔧 Servicio no disponible (503) - Backend temporalmente inaccesible';
                    break;
                case 429:
                    errorMessage = '⏳ Demasiadas solicitudes (429) - Espera un momento antes de intentar de nuevo';
                    break;
                default:
                    errorMessage = `❌ Error de conexión (${response.status}) - Problema de comunicación con el servidor`;
            }
            throw new Error(errorMessage);
        }
        
        return await response.json();
    }
    
    displayResults(results) {
        const resultsContent = document.getElementById('resultsContent');
        
        // Extraer datos clave
        const stats = results.statistical_results || {};
        const archaeological = results.physics_results || {};
        const regionInfo = results.region_info || {};
        
        // Calcular probabilidad promedio
        const probabilities = Object.values(stats).map(s => s.archaeological_probability || 0);
        const avgProbability = probabilities.length > 0 ? 
            probabilities.reduce((a, b) => a + b, 0) / probabilities.length : 0;
        
        resultsContent.innerHTML = `
            <div class="results-summary">
                <h4>📍 ${regionInfo.name || 'Análisis Arqueológico'}</h4>
                <div class="key-metrics">
                    <div class="metric">
                        <span class="metric-label">Probabilidad Arqueológica</span>
                        <span class="metric-value ${this.getProbabilityClass(avgProbability)}">
                            ${(avgProbability * 100).toFixed(1)}%
                        </span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Área Analizada</span>
                        <span class="metric-value">${(regionInfo.area_km2 || 0).toFixed(2)} km²</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Resolución</span>
                        <span class="metric-value">${regionInfo.resolution_m || 200}m</span>
                    </div>
                </div>
            </div>
            
            <div class="instruments-results">
                <h4>🛰️ Resultados por Instrumento</h4>
                ${this.generateInstrumentResults(stats)}
            </div>
            
            <div class="archaeological-evaluation">
                <h4>🏛️ Evaluación Arqueológica</h4>
                ${this.generateArchaeologicalEvaluation(archaeological)}
            </div>
            
            <div class="interpretation">
                <h4>💡 Interpretación</h4>
                <p>${this.generateInterpretation(avgProbability, stats)}</p>
            </div>
        `;
    }
    
    generateInstrumentResults(stats) {
        let html = '<div class="instrument-results-grid">';
        
        Object.entries(this.instrumentConfig).forEach(([key, config]) => {
            const result = stats[key];
            if (result) {
                const prob = result.archaeological_probability || 0;
                const coherence = result.geometric_coherence || 0;
                
                html += `
                    <div class="instrument-result ${config.enhanced ? 'enhanced' : 'base'}">
                        <div class="instrument-result-header">
                            <span class="instrument-name">${config.name}</span>
                            ${config.enhanced ? `<span class="enhanced-badge">✨</span>` : ''}
                        </div>
                        <div class="instrument-metrics">
                            <div class="metric-small">
                                <span>Probabilidad:</span>
                                <span class="${this.getProbabilityClass(prob)}">${(prob * 100).toFixed(1)}%</span>
                            </div>
                            <div class="metric-small">
                                <span>Coherencia:</span>
                                <span>${(coherence * 100).toFixed(1)}%</span>
                            </div>
                        </div>
                        <div class="probability-bar">
                            <div class="probability-fill ${this.getProbabilityClass(prob)}" 
                                 style="width: ${prob * 100}%"></div>
                        </div>
                    </div>
                `;
            }
        });
        
        html += '</div>';
        return html;
    }
    
    generateArchaeologicalEvaluation(archaeological) {
        const evaluations = archaeological.evaluations || {};
        const integrated = archaeological.integrated_analysis || {};
        
        let html = '<div class="evaluation-results">';
        
        if (integrated.integrated_score !== undefined) {
            html += `
                <div class="integrated-score">
                    <span class="score-label">Score Integrado:</span>
                    <span class="score-value ${this.getProbabilityClass(integrated.integrated_score)}">
                        ${(integrated.integrated_score * 100).toFixed(1)}%
                    </span>
                </div>
                <div class="classification">
                    <span class="classification-label">Clasificación:</span>
                    <span class="classification-value">${integrated.classification || 'N/A'}</span>
                </div>
            `;
        }
        
        Object.entries(evaluations).forEach(([ruleName, evaluation]) => {
            const prob = evaluation.archaeological_probability || 0;
            const confidence = evaluation.confidence || 0;
            
            html += `
                <div class="rule-evaluation">
                    <div class="rule-name">${ruleName.replace(/_/g, ' ')}</div>
                    <div class="rule-metrics">
                        <span>Prob: ${(prob * 100).toFixed(1)}%</span>
                        <span>Conf: ${(confidence * 100).toFixed(1)}%</span>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        return html;
    }
    
    generateInterpretation(avgProbability, stats) {
        if (avgProbability > 0.6) {
            return "🔴 ALTA probabilidad arqueológica detectada. Múltiples instrumentos convergen en anomalías significativas. Recomendado: investigación detallada.";
        } else if (avgProbability > 0.3) {
            return "🟡 MODERADA probabilidad arqueológica. Algunos instrumentos detectan patrones anómalos. Considerar análisis complementario.";
        } else if (avgProbability > 0.1) {
            return "🟢 BAJA probabilidad arqueológica. Patrones principalmente naturales con algunas anomalías menores.";
        } else {
            return "⚪ Muy baja probabilidad arqueológica. Patrones consistentes con procesos naturales.";
        }
    }
    
    getProbabilityClass(probability) {
        if (probability > 0.6) return 'high';
        if (probability > 0.3) return 'moderate';
        if (probability > 0.1) return 'low';
        return 'very-low';
    }
    
    updateMapVisualization(results) {
        const stats = results.statistical_results || {};
        const anomalyMap = results.anomaly_map || {};
        
        // Actualizar celdas del mapa con resultados
        const gridCells = document.querySelectorAll('.grid-cell');
        
        // Simular distribución de anomalías
        const anomalyPercentage = anomalyMap.statistics?.spatial_anomaly_percentage || 0;
        const numAnomalyCells = Math.floor((anomalyPercentage / 100) * gridCells.length);
        
        // Limpiar visualización anterior
        gridCells.forEach(cell => {
            cell.classList.remove('anomaly', 'high-prob', 'moderate-prob', 'low-prob');
        });
        
        // Aplicar visualización de anomalías
        for (let i = 0; i < numAnomalyCells; i++) {
            const randomIndex = Math.floor(Math.random() * gridCells.length);
            const cell = gridCells[randomIndex];
            
            const probability = Math.random();
            cell.classList.add('anomaly');
            
            if (probability > 0.6) {
                cell.classList.add('high-prob');
            } else if (probability > 0.3) {
                cell.classList.add('moderate-prob');
            } else {
                cell.classList.add('low-prob');
            }
        }
    }
    
    showAnalysisOverlay() {
        document.getElementById('analysisOverlay').classList.remove('hidden');
    }
    
    hideAnalysisOverlay() {
        document.getElementById('analysisOverlay').classList.add('hidden');
    }
    
    showError(message) {
        const resultsContent = document.getElementById('resultsContent');
        resultsContent.innerHTML = `
            <div class="error-message">
                <h4>❌ Error</h4>
                <p>${message}</p>
            </div>
        `;
    }
    
    toggleLayerPanel() {
        // Implementar toggle de panel de capas
        console.log('Toggle layer panel');
    }
    
    toggleInstrumentPanel() {
        const panel = document.querySelector('.instruments-panel');
        panel.classList.toggle('collapsed');
    }
    
    toggleResultsPanel() {
        const panel = document.querySelector('.results-panel');
        panel.classList.toggle('collapsed');
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.archeoScope = new ArcheoScopeInteractiveMap('archeoScopeContainer');
});
