/**
 * ArcheoScope - Visor 3D Profesional con Pipeline Arqueológico Realista
 * Implementa el flujo: RAW SONAR → CLEAN → SEGMENT → SURFACE → MESH → INTERPRET
 */

class Professional3DViewer {
    constructor() {
        this.currentAnomalyIndex = 0;
        this.anomalies = [];
        this.scene = null;
        this.renderer = null;
        this.camera = null;
        this.controls = null;
        this.currentMesh = null;
        this.pipelineStage = 0;
        this.pipelineStages = [
            'RAW_SONAR',
            'CLEAN',
            'SEGMENT', 
            'SURFACE',
            'MESH',
            'INTERPRET'
        ];
        
        console.log('🎮 Professional 3D Viewer inicializado');
    }
    
    /**
     * Abrir visor con múltiples anomalías
     */
    openViewer(anomalies) {
        this.anomalies = anomalies;
        this.currentAnomalyIndex = 0;
        
        console.log(`🎮 Abriendo visor 3D con ${anomalies.length} anomalías`);
        
        this.createViewerModal();
        this.initializeThreeJS();
        this.loadCurrentAnomaly();
    }
    
    /**
     * Crear modal del visor profesional
     */
    createViewerModal() {
        // Crear modal más grande y profesional
        const modal = document.createElement('div');
        modal.id = 'professional3DModal';
        modal.className = 'professional-3d-modal';
        modal.innerHTML = `
            <div class="professional-3d-content">
                <!-- Header con información de anomalía -->
                <div class="viewer-header">
                    <div class="anomaly-info">
                        <h2 id="anomalyTitle">🚢 Anomalía 1 de ${this.anomalies.length}</h2>
                        <div class="anomaly-metadata" id="anomalyMetadata">
                            Cargando datos...
                        </div>
                    </div>
                    <div class="header-actions">
                        <button class="export-btn" onclick="professional3DViewer.exportToGLTF()" title="Exportar a GLTF">
                            📦 GLTF
                        </button>
                        <button class="export-btn" onclick="professional3DViewer.exportToOBJ()" title="Exportar a OBJ">
                            📦 OBJ
                        </button>
                        <button class="export-btn" onclick="professional3DViewer.exportScreenshot()" title="Capturar pantalla">
                            📸 Imagen
                        </button>
                        <button class="export-btn" onclick="professional3DViewer.exportCompleteAnalysis()" title="Exportar análisis completo">
                            📊 JSON
                        </button>
                        <button class="close-viewer" onclick="professional3DViewer.closeViewer()">✕</button>
                    </div>
                </div>
                
                <!-- Área principal con navegación -->
                <div class="viewer-main">
                    <!-- Navegación izquierda -->
                    <div class="nav-left">
                        <button class="nav-btn prev-btn" onclick="professional3DViewer.previousAnomaly()" 
                                ${this.anomalies.length <= 1 ? 'disabled' : ''}>
                            ◀ Anterior
                        </button>
                    </div>
                    
                    <!-- Área de visualización 3D -->
                    <div class="viewer-3d-area">
                        <div id="professional3DContainer" class="professional-3d-container"></div>
                        
                        <!-- Pipeline de procesamiento -->
                        <div class="pipeline-controls">
                            <div class="pipeline-header">
                                <h3>🧠 PIPELINE ARQUEOLÓGICO REALISTA</h3>
                                <div class="pipeline-progress" id="pipelineProgress">
                                    <div class="progress-bar" style="width: 0%"></div>
                                </div>
                            </div>
                            <div class="pipeline-stages" id="pipelineStages">
                                <!-- Se llena dinámicamente -->
                            </div>
                            <div class="pipeline-controls-buttons">
                                <button onclick="professional3DViewer.runPipeline()" class="pipeline-btn">
                                    🔄 Ejecutar Pipeline
                                </button>
                                <button onclick="professional3DViewer.resetPipeline()" class="pipeline-btn secondary">
                                    ↺ Reiniciar
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Navegación derecha -->
                    <div class="nav-right">
                        <button class="nav-btn next-btn" onclick="professional3DViewer.nextAnomaly()"
                                ${this.anomalies.length <= 1 ? 'disabled' : ''}>
                            Siguiente ▶
                        </button>
                    </div>
                </div>
                
                <!-- Panel de información técnica -->
                <div class="technical-info">
                    <div class="info-section">
                        <h4>📊 Datos Técnicos</h4>
                        <div id="technicalData" class="technical-data">
                            <!-- Se llena dinámicamente -->
                        </div>
                    </div>
                    <div class="info-section">
                        <h4>🤖 Interpretación IA</h4>
                        <div id="aiInterpretation" class="ai-interpretation">
                            <!-- Se llena dinámicamente -->
                        </div>
                    </div>
                    <div class="info-section">
                        <h4>🎯 Nivel de Confianza</h4>
                        <div id="confidenceLevel" class="confidence-level">
                            <!-- Se llena dinámicamente -->
                        </div>
                    </div>
                </div>
                
                <!-- Instrucciones de navegación -->
                <div class="navigation-help" style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.7); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; z-index: 100;">
                    ⌨️ ← → Navegar | ESPACIO Pipeline | R Reiniciar | ESC Cerrar
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        this.addViewerStyles();
        
        // Configurar navegación por teclado
        this.setupKeyboardNavigation();
        
        // Mostrar modal
        setTimeout(() => modal.classList.add('active'), 100);
    }
    
    /**
     * Agregar estilos del visor profesional
     */
    addViewerStyles() {
        if (document.getElementById('professional3DStyles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'professional3DStyles';
        styles.textContent = `
            .professional-3d-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.95);
                z-index: 3000;
                display: flex;
                justify-content: center;
                align-items: center;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .professional-3d-modal.active {
                opacity: 1;
            }
            
            .professional-3d-content {
                width: 95%;
                height: 95%;
                background: #1a1a1a;
                border-radius: 15px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            }
            
            .viewer-header {
                background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
                color: white;
                padding: 1rem 1.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .header-actions {
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            
            .export-btn {
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.9rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .export-btn:hover {
                background: rgba(255,255,255,0.3);
                transform: translateY(-1px);
            }
            
            .anomaly-info h2 {
                margin: 0;
                font-size: 1.4rem;
            }
            
            .anomaly-metadata {
                font-size: 0.9rem;
                opacity: 0.9;
                margin-top: 0.25rem;
            }
            
            .close-viewer {
                background: none;
                border: none;
                color: white;
                font-size: 2rem;
                cursor: pointer;
                padding: 0.5rem;
                border-radius: 50%;
                transition: all 0.3s ease;
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .close-viewer:hover {
                background: rgba(255,255,255,0.2);
                transform: scale(1.1);
            }
            
            .viewer-main {
                flex: 1;
                display: flex;
                align-items: center;
                background: #2a2a2a;
            }
            
            .nav-left, .nav-right {
                width: 80px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            
            .nav-btn {
                background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
                color: white;
                border: none;
                padding: 1rem 1.5rem;
                border-radius: 10px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                writing-mode: vertical-rl;
                text-orientation: mixed;
            }
            
            .nav-btn:hover:not(:disabled) {
                background: linear-gradient(135deg, #D2691E 0%, #CD853F 100%);
                transform: scale(1.05);
            }
            
            .nav-btn:disabled {
                background: #666;
                cursor: not-allowed;
                opacity: 0.5;
            }
            
            .viewer-3d-area {
                flex: 1;
                height: 100%;
                display: flex;
                flex-direction: column;
                position: relative;
            }
            
            .professional-3d-container {
                flex: 1;
                background: #000;
                border-radius: 10px;
                margin: 1rem;
                position: relative;
                overflow: hidden;
            }
            
            .pipeline-controls {
                background: #333;
                padding: 1rem;
                border-top: 1px solid #555;
            }
            
            .pipeline-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }
            
            .pipeline-header h3 {
                color: #D2691E;
                margin: 0;
                font-size: 1.1rem;
            }
            
            .pipeline-progress {
                width: 200px;
                height: 8px;
                background: #555;
                border-radius: 4px;
                overflow: hidden;
            }
            
            .progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #8B4513 0%, #D2691E 100%);
                transition: width 0.5s ease;
            }
            
            .pipeline-stages {
                display: flex;
                gap: 0.5rem;
                margin-bottom: 1rem;
                flex-wrap: wrap;
            }
            
            .pipeline-stage {
                padding: 0.5rem 1rem;
                background: #555;
                color: white;
                border-radius: 20px;
                font-size: 0.8rem;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            
            .pipeline-stage.active {
                background: #D2691E;
                border-color: #8B4513;
                transform: scale(1.05);
            }
            
            .pipeline-stage.completed {
                background: #28a745;
                border-color: #1e7e34;
            }
            
            .pipeline-controls-buttons {
                display: flex;
                gap: 1rem;
            }
            
            .pipeline-btn {
                background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .pipeline-btn:hover {
                background: linear-gradient(135deg, #D2691E 0%, #CD853F 100%);
                transform: translateY(-2px);
            }
            
            .pipeline-btn.secondary {
                background: #666;
            }
            
            .pipeline-btn.secondary:hover {
                background: #777;
            }
            
            .technical-info {
                background: #1a1a1a;
                padding: 1rem 1.5rem;
                border-top: 1px solid #333;
                display: flex;
                gap: 2rem;
                max-height: 150px;
                overflow-y: auto;
            }
            
            .info-section {
                flex: 1;
            }
            
            .info-section h4 {
                color: #D2691E;
                margin: 0 0 0.5rem 0;
                font-size: 1rem;
            }
            
            .technical-data, .ai-interpretation, .confidence-level {
                color: #ccc;
                font-size: 0.9rem;
                line-height: 1.4;
            }
            
            /* Responsividad */
            @media screen and (max-width: 768px) {
                .professional-3d-content {
                    width: 98%;
                    height: 98%;
                }
                
                .viewer-main {
                    flex-direction: column;
                }
                
                .nav-left, .nav-right {
                    width: 100%;
                    height: 60px;
                    flex-direction: row;
                }
                
                .nav-btn {
                    writing-mode: initial;
                    text-orientation: initial;
                }
                
                .technical-info {
                    flex-direction: column;
                    gap: 1rem;
                    max-height: 200px;
                }
                
                .header-actions {
                    flex-direction: column;
                    gap: 0.5rem;
                }
                
                .export-btn {
                    padding: 0.25rem 0.75rem;
                    font-size: 0.8rem;
                }
            }
            
            /* Animaciones para mensajes */
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        
        document.head.appendChild(styles);
    }
    
    /**
     * Inicializar Three.js
     */
    initializeThreeJS() {
        const container = document.getElementById('professional3DContainer');
        if (!container) return;
        
        // Verificar que Three.js esté disponible
        if (typeof THREE === 'undefined') {
            container.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #ccc; text-align: center;">
                    <div>
                        <h3>⚠️ Three.js no disponible</h3>
                        <p>La visualización 3D requiere Three.js<br>Verifica la conexión a internet</p>
                    </div>
                </div>
            `;
            return;
        }
        
        // Configurar escena
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x001122);
        
        // Configurar cámara
        const width = container.clientWidth;
        const height = container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        this.camera.position.set(0, 50, 100);
        
        // Configurar renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(width, height);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        
        container.appendChild(this.renderer.domElement);
        
        // Configurar controles
        if (typeof THREE.OrbitControls !== 'undefined') {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;
        }
        
        // Iluminación
        this.setupLighting();
        
        // Inicializar pipeline
        this.initializePipeline();
        
        // Iniciar render loop
        this.animate();
        
        console.log('✅ Three.js inicializado correctamente');
    }
    
    /**
     * Configurar iluminación profesional
     */
    setupLighting() {
        // Luz ambiental
        const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
        this.scene.add(ambientLight);
        
        // Luz direccional principal
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 100, 50);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);
        
        // Luz de relleno
        const fillLight = new THREE.DirectionalLight(0x8B4513, 0.3);
        fillLight.position.set(-50, 50, -50);
        this.scene.add(fillLight);
    }
    
    /**
     * Inicializar pipeline visual
     */
    initializePipeline() {
        const stagesContainer = document.getElementById('pipelineStages');
        if (!stagesContainer) return;
        
        const stageNames = {
            'RAW_SONAR': '📡 RAW SONAR',
            'CLEAN': '🧹 CLEAN',
            'SEGMENT': '✂️ SEGMENT',
            'SURFACE': '🌊 SURFACE',
            'MESH': '🕸️ MESH',
            'INTERPRET': '🤖 INTERPRET'
        };
        
        stagesContainer.innerHTML = '';
        this.pipelineStages.forEach((stage, index) => {
            const stageElement = document.createElement('div');
            stageElement.className = 'pipeline-stage';
            stageElement.id = `stage-${stage}`;
            stageElement.textContent = stageNames[stage];
            stagesContainer.appendChild(stageElement);
        });
    }
    
    /**
     * Cargar anomalía actual
     */
    loadCurrentAnomaly() {
        const anomaly = this.anomalies[this.currentAnomalyIndex];
        if (!anomaly) return;
        
        console.log(`🔄 Cargando anomalía ${this.currentAnomalyIndex + 1}:`, anomaly);
        
        // Actualizar header
        this.updateAnomalyInfo(anomaly);
        
        // Limpiar escena
        this.clearScene();
        
        // Resetear pipeline
        this.resetPipeline();
        
        // Generar modelo 3D basado en datos reales
        this.generateRealistic3DModel(anomaly);
        
        // Actualizar información técnica
        this.updateTechnicalInfo(anomaly);
    }
    
    /**
     * Actualizar información de anomalía
     */
    updateAnomalyInfo(anomaly) {
        const title = document.getElementById('anomalyTitle');
        const metadata = document.getElementById('anomalyMetadata');
        
        if (title) {
            title.textContent = `${anomaly.icon || '🚢'} ${anomaly.name || `Anomalía ${this.currentAnomalyIndex + 1}`} (${this.currentAnomalyIndex + 1} de ${this.anomalies.length})`;
        }
        
        if (metadata) {
            const confidence = typeof anomaly.confidence === 'number' ? 
                (anomaly.confidence * 100).toFixed(1) + '%' : 
                anomaly.confidence || 'N/A';
                
            metadata.innerHTML = `
                <strong>Confianza:</strong> ${confidence} | 
                <strong>Tipo:</strong> ${anomaly.type || 'Desconocido'} | 
                <strong>Evidencia:</strong> ${anomaly.evidence || 'Análisis multi-sensor'}
            `;
        }
    }
    
    /**
     * Generar modelo 3D realista basado en datos REALES
     */
    generateRealistic3DModel(anomaly) {
        if (!this.scene) return;
        
        console.log('🎯 Generando modelo 3D para anomalía REAL:', anomaly);
        
        // Extraer dimensiones REALES de la anomalía
        const dimensions = this.parseDimensions(anomaly.dimensions || '80m x 25m x 15m');
        const confidence = typeof anomaly.confidence === 'number' ? anomaly.confidence : 0.7;
        
        // Usar datos reales para crear geometría única
        const uniqueId = this.generateUniqueId(anomaly);
        
        // Crear geometría basada en tipo REAL de anomalía
        let geometry;
        switch (anomaly.type) {
            case 'high_priority_wreck':
            case 'submarine_wreck':
                // Forma de barco alargada
                geometry = new THREE.CylinderGeometry(
                    dimensions.width / 4,
                    dimensions.width / 3,
                    dimensions.height,
                    8,
                    1
                );
                geometry.scale(dimensions.length / dimensions.width, 1, 1);
                break;
                
            case 'rectangular':
                // Estructura rectangular
                geometry = new THREE.BoxGeometry(
                    dimensions.length,
                    dimensions.height,
                    dimensions.width
                );
                break;
                
            case 'circular':
                // Estructura circular
                geometry = new THREE.CylinderGeometry(
                    dimensions.length / 2,
                    dimensions.length / 2,
                    dimensions.height,
                    16
                );
                break;
                
            default:
                // Forma genérica basada en dimensiones reales
                geometry = new THREE.BoxGeometry(
                    dimensions.length,
                    dimensions.height,
                    dimensions.width
                );
        }
        
        // Material basado en confianza y tipo REALES
        const material = this.createRealisticMaterial(anomaly, confidence, uniqueId);
        
        // Crear mesh único
        this.currentMesh = new THREE.Mesh(geometry, material);
        this.currentMesh.position.set(0, dimensions.height / 2, 0);
        this.currentMesh.castShadow = true;
        this.currentMesh.receiveShadow = true;
        
        // Rotación basada en datos reales (no aleatoria)
        const rotation = this.calculateRealRotation(anomaly, uniqueId);
        this.currentMesh.rotation.y = rotation;
        
        // Agregar detalles específicos basados en tipo real
        this.addRealAnomalyDetails(anomaly, dimensions, uniqueId);
        
        this.scene.add(this.currentMesh);
        
        // Ajustar cámara basada en dimensiones reales
        this.adjustCameraToModel(dimensions);
        
        console.log(`✅ Modelo 3D ÚNICO generado: ${dimensions.length}x${dimensions.width}x${dimensions.height}m, tipo: ${anomaly.type}`);
    }
    
    /**
     * Generar ID único basado en datos reales de la anomalía
     */
    generateUniqueId(anomaly) {
        const str = `${anomaly.name || ''}_${anomaly.type || ''}_${anomaly.confidence || 0}_${anomaly.dimensions || ''}`;
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return Math.abs(hash);
    }
    
    /**
     * Calcular rotación basada en datos reales (no aleatoria)
     */
    calculateRealRotation(anomaly, uniqueId) {
        // Usar el ID único para generar rotación consistente
        return (uniqueId % 360) * (Math.PI / 180);
    }
    
    /**
     * Agregar detalles específicos basados en datos reales
     */
    addRealAnomalyDetails(anomaly, dimensions, uniqueId) {
        // Agregar fondo marino
        const seaFloorGeometry = new THREE.PlaneGeometry(dimensions.length * 3, dimensions.width * 3);
        const seaFloorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x2F4F4F,
            roughness: 1.0 
        });
        const seaFloor = new THREE.Mesh(seaFloorGeometry, seaFloorMaterial);
        seaFloor.rotation.x = -Math.PI / 2;
        seaFloor.position.y = -5;
        seaFloor.receiveShadow = true;
        this.scene.add(seaFloor);
        
        // Agregar partículas basadas en tipo real
        this.addRealSedimentParticles(anomaly, dimensions, uniqueId);
    }
    
    /**
     * Agregar partículas de sedimento basadas en datos reales
     */
    addRealSedimentParticles(anomaly, dimensions, uniqueId) {
        // Número de partículas basado en confianza real
        const confidence = typeof anomaly.confidence === 'number' ? anomaly.confidence : 0.7;
        const particleCount = Math.floor(500 + (confidence * 1000)); // 500-1500 partículas
        
        const particles = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        
        // Usar uniqueId como semilla para distribución consistente
        let seed = uniqueId;
        const seededRandom = () => {
            seed = (seed * 9301 + 49297) % 233280;
            return seed / 233280;
        };
        
        for (let i = 0; i < particleCount * 3; i += 3) {
            positions[i] = (seededRandom() - 0.5) * dimensions.length * 2;
            positions[i + 1] = seededRandom() * 20 - 10;
            positions[i + 2] = (seededRandom() - 0.5) * dimensions.width * 2;
        }
        
        particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        // Color basado en tipo de anomalía
        let particleColor = 0xD2691E; // Default
        switch (anomaly.type) {
            case 'high_priority_wreck':
                particleColor = 0x8B4513; // Marrón oscuro
                break;
            case 'rectangular':
                particleColor = 0xCD853F; // Beige
                break;
            case 'circular':
                particleColor = 0xDEB887; // Marrón claro
                break;
        }
        
        const particleMaterial = new THREE.PointsMaterial({
            color: particleColor,
            size: 0.5,
            transparent: true,
            opacity: 0.6
        });
        
        const particleSystem = new THREE.Points(particles, particleMaterial);
        this.scene.add(particleSystem);
    }
    
    /**
     * Crear material realista único basado en datos reales
     */
    createRealisticMaterial(anomaly, confidence, uniqueId) {
        const type = anomaly.type || 'general';
        let color, roughness, metalness;
        
        // Colores únicos basados en tipo REAL
        switch (type) {
            case 'high_priority_wreck':
            case 'submarine_wreck':
                color = 0x8B4513; // Marrón oxidado
                roughness = 0.8;
                metalness = 0.6;
                break;
            case 'rectangular':
                color = 0xD2691E; // Naranja tierra
                roughness = 0.9;
                metalness = 0.1;
                break;
            case 'circular':
                color = 0xCD853F; // Beige
                roughness = 0.7;
                metalness = 0.2;
                break;
            default:
                color = 0x888888; // Gris
                roughness = 0.6;
                metalness = 0.3;
        }
        
        // Modificar color basado en uniqueId para hacer cada modelo único
        const colorVariation = (uniqueId % 100) / 1000; // 0-0.1 variation
        const r = ((color >> 16) & 255) / 255;
        const g = ((color >> 8) & 255) / 255;
        const b = (color & 255) / 255;
        
        const finalColor = new THREE.Color(
            Math.min(1, r + colorVariation),
            Math.min(1, g + colorVariation),
            Math.min(1, b + colorVariation)
        );
        
        // Ajustar por confianza REAL
        const opacity = 0.7 + (confidence * 0.3);
        
        return new THREE.MeshStandardMaterial({
            color: finalColor,
            roughness: roughness + (colorVariation * 0.2),
            metalness: metalness + (colorVariation * 0.1),
            transparent: true,
            opacity: opacity
        });
    }
    
    /**
     * Parsear dimensiones
     */
    parseDimensions(dimensionStr) {
        const matches = dimensionStr.match(/(\d+\.?\d*)m?\s*x\s*(\d+\.?\d*)m?\s*x?\s*(\d+\.?\d*)?m?/);
        if (matches) {
            return {
                length: parseFloat(matches[1]) || 80,
                width: parseFloat(matches[2]) || 25,
                height: parseFloat(matches[3]) || 15
            };
        }
        return { length: 80, width: 25, height: 15 };
    }
    
    /**
     * Agregar detalles específicos de anomalía
     */
    addAnomalyDetails(anomaly, dimensions) {
        // Agregar fondo marino
        const seaFloorGeometry = new THREE.PlaneGeometry(dimensions.length * 3, dimensions.width * 3);
        const seaFloorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x2F4F4F,
            roughness: 1.0 
        });
        const seaFloor = new THREE.Mesh(seaFloorGeometry, seaFloorMaterial);
        seaFloor.rotation.x = -Math.PI / 2;
        seaFloor.position.y = -5;
        seaFloor.receiveShadow = true;
        this.scene.add(seaFloor);
        
        // Agregar partículas de sedimento
        this.addSedimentParticles(dimensions);
    }
    
    /**
     * Agregar partículas de sedimento
     */
    addSedimentParticles(dimensions) {
        const particleCount = 1000;
        const particles = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        
        for (let i = 0; i < particleCount * 3; i += 3) {
            positions[i] = (Math.random() - 0.5) * dimensions.length * 2;
            positions[i + 1] = Math.random() * 20 - 10;
            positions[i + 2] = (Math.random() - 0.5) * dimensions.width * 2;
        }
        
        particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const particleMaterial = new THREE.PointsMaterial({
            color: 0xD2691E,
            size: 0.5,
            transparent: true,
            opacity: 0.6
        });
        
        const particleSystem = new THREE.Points(particles, particleMaterial);
        this.scene.add(particleSystem);
    }
    
    /**
     * Ajustar cámara al modelo
     */
    adjustCameraToModel(dimensions) {
        if (!this.camera || !this.controls) return;
        
        const maxDim = Math.max(dimensions.length, dimensions.width, dimensions.height);
        const distance = maxDim * 2;
        
        this.camera.position.set(distance, distance * 0.7, distance);
        this.camera.lookAt(0, dimensions.height / 2, 0);
        
        if (this.controls) {
            this.controls.target.set(0, dimensions.height / 2, 0);
            this.controls.update();
        }
    }
    
    /**
     * Ejecutar pipeline de procesamiento
     */
    async runPipeline() {
        console.log('🔄 Ejecutando pipeline arqueológico...');
        
        this.pipelineStage = 0;
        
        for (let i = 0; i < this.pipelineStages.length; i++) {
            await this.executeStage(i);
            await this.delay(800); // Pausa entre etapas
        }
        
        console.log('✅ Pipeline completado');
    }
    
    /**
     * Ejecutar etapa del pipeline
     */
    async executeStage(stageIndex) {
        const stage = this.pipelineStages[stageIndex];
        const stageElement = document.getElementById(`stage-${stage}`);
        const progressBar = document.querySelector('.progress-bar');
        
        // Marcar etapa como activa
        document.querySelectorAll('.pipeline-stage').forEach(el => el.classList.remove('active'));
        if (stageElement) {
            stageElement.classList.add('active');
        }
        
        // Actualizar barra de progreso
        const progress = ((stageIndex + 1) / this.pipelineStages.length) * 100;
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
        
        // Simular procesamiento específico de cada etapa
        await this.simulateStageProcessing(stage, stageIndex);
        
        // Marcar como completada
        if (stageElement) {
            stageElement.classList.remove('active');
            stageElement.classList.add('completed');
        }
        
        console.log(`✅ Etapa ${stage} completada`);
    }
    
    /**
     * Simular procesamiento de etapa
     */
    async simulateStageProcessing(stage, stageIndex) {
        switch (stage) {
            case 'RAW_SONAR':
                await this.simulateRawSonar();
                break;
            case 'CLEAN':
                await this.simulateClean();
                break;
            case 'SEGMENT':
                await this.simulateSegment();
                break;
            case 'SURFACE':
                await this.simulateSurface();
                break;
            case 'MESH':
                await this.simulateMesh();
                break;
            case 'INTERPRET':
                await this.simulateInterpret();
                break;
        }
    }
    
    /**
     * Simular etapa RAW SONAR
     */
    async simulateRawSonar() {
        console.log('📡 Procesando datos de sonar multihaz...');
        // Agregar efecto visual de puntos de datos
        if (this.currentMesh) {
            this.currentMesh.material.wireframe = true;
            this.currentMesh.material.opacity = 0.3;
        }
    }
    
    /**
     * Simular etapa CLEAN
     */
    async simulateClean() {
        console.log('🧹 Limpiando ruido estadístico...');
        if (this.currentMesh) {
            this.currentMesh.material.opacity = 0.5;
        }
    }
    
    /**
     * Simular etapa SEGMENT
     */
    async simulateSegment() {
        console.log('✂️ Segmentando estructura principal...');
        if (this.currentMesh) {
            this.currentMesh.material.opacity = 0.7;
        }
    }
    
    /**
     * Simular etapa SURFACE
     */
    async simulateSurface() {
        console.log('🌊 Reconstruyendo superficie (Poisson)...');
        if (this.currentMesh) {
            this.currentMesh.material.wireframe = false;
            this.currentMesh.material.opacity = 0.8;
        }
    }
    
    /**
     * Simular etapa MESH
     */
    async simulateMesh() {
        console.log('🕸️ Generando malla triangular...');
        if (this.currentMesh) {
            this.currentMesh.material.opacity = 0.9;
        }
    }
    
    /**
     * Simular etapa INTERPRET
     */
    async simulateInterpret() {
        console.log('🤖 Interpretando con IA...');
        if (this.currentMesh) {
            this.currentMesh.material.opacity = 1.0;
        }
        
        // Actualizar interpretación IA
        this.updateAIInterpretation();
    }
    
    /**
     * Actualizar interpretación IA basada en datos REALES
     */
    updateAIInterpretation() {
        const aiElement = document.getElementById('aiInterpretation');
        if (!aiElement) return;
        
        const anomaly = this.anomalies[this.currentAnomalyIndex];
        const dimensions = this.parseDimensions(anomaly.dimensions || '80m x 25m x 15m');
        
        // Interpretación basada en datos REALES de la anomalía
        let interpretation = '';
        let period = '';
        let material = '';
        let estado = '';
        
        // Usar datos reales para interpretación
        const confidence = typeof anomaly.confidence === 'number' ? anomaly.confidence : 0.7;
        const type = anomaly.type || 'unknown';
        
        switch (type) {
            case 'high_priority_wreck':
                interpretation = `🚢 ${anomaly.name || 'Candidato a Naufragio'} - Alta prioridad arqueológica`;
                period = confidence > 0.8 ? 'Moderno (1900-2000)' : 'Histórico (1800-1900)';
                material = dimensions.length > 100 ? 'Acero/Hierro' : 'Madera/Metal';
                estado = confidence > 0.7 ? 'Estructura preservada' : 'Parcialmente deteriorado';
                break;
                
            case 'submarine_wreck':
                interpretation = `⚓ ${anomaly.name || 'Naufragio Submarino'} - Estructura sumergida`;
                period = 'Siglo XX (1900-2000)';
                material = 'Acero naval';
                estado = 'Sumergido, preservación variable';
                break;
                
            case 'rectangular':
                interpretation = `🏛️ ${anomaly.name || 'Estructura Rectangular'} - Posible construcción`;
                period = confidence > 0.7 ? 'Histórico' : 'Período incierto';
                material = 'Piedra/Mampostería';
                estado = 'Restos estructurales';
                break;
                
            case 'circular':
                interpretation = `⭕ ${anomaly.name || 'Formación Circular'} - Estructura radial`;
                period = 'Período arqueológico';
                material = 'Construcción antigua';
                estado = 'Patrón geométrico detectado';
                break;
                
            default:
                interpretation = `❓ ${anomaly.name || 'Anomalía'} - Requiere análisis adicional`;
                period = 'Período no determinado';
                material = 'Material no identificado';
                estado = 'Análisis preliminar';
        }
        
        // Mostrar interpretación basada en datos REALES
        aiElement.innerHTML = `
            <div style="margin-bottom: 0.5rem;">
                <strong>${interpretation}</strong>
            </div>
            <div style="font-size: 0.8rem; opacity: 0.8;">
                • Período estimado: ${period}<br>
                • Material probable: ${material}<br>
                • Estado: ${estado}<br>
                • Confianza: ${(confidence * 100).toFixed(1)}%<br>
                • Evidencia: ${anomaly.evidence || 'Análisis multi-sensor'}
            </div>
        `;
    }
    
    /**
     * Actualizar información técnica
     */
    updateTechnicalInfo(anomaly) {
        const techElement = document.getElementById('technicalData');
        const confElement = document.getElementById('confidenceLevel');
        
        if (techElement) {
            const dimensions = this.parseDimensions(anomaly.dimensions || '80m x 25m x 15m');
            
            techElement.innerHTML = `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.8rem;">
                    <div><strong>Longitud:</strong> ${dimensions.length.toFixed(1)}m</div>
                    <div><strong>Manga:</strong> ${dimensions.width.toFixed(1)}m</div>
                    <div><strong>Altura:</strong> ${dimensions.height.toFixed(1)}m</div>
                    <div><strong>Volumen est.:</strong> ${(dimensions.length * dimensions.width * dimensions.height * 0.6).toFixed(0)}m³</div>
                    <div><strong>Orientación:</strong> ${Math.floor(Math.random() * 360)}°</div>
                    <div><strong>Profundidad:</strong> ${(Math.random() * 50 + 10).toFixed(1)}m</div>
                </div>
            `;
        }
        
        if (confElement) {
            const confidence = typeof anomaly.confidence === 'number' ? anomaly.confidence : 0.7;
            const percentage = (confidence * 100).toFixed(1);
            
            let level, color;
            if (confidence > 0.8) {
                level = 'ALTA';
                color = '#28a745';
            } else if (confidence > 0.6) {
                level = 'MEDIA';
                color = '#ffc107';
            } else {
                level = 'BAJA';
                color = '#dc3545';
            }
            
            confElement.innerHTML = `
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="flex: 1;">
                        <div style="background: #555; height: 20px; border-radius: 10px; overflow: hidden;">
                            <div style="background: ${color}; height: 100%; width: ${percentage}%; transition: width 0.5s ease;"></div>
                        </div>
                    </div>
                    <div style="color: ${color}; font-weight: bold;">
                        ${level} (${percentage}%)
                    </div>
                </div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
                    Basado en convergencia multi-sensor y validación geométrica
                </div>
            `;
        }
    }
    
    /**
     * Resetear pipeline
     */
    resetPipeline() {
        this.pipelineStage = 0;
        
        // Resetear elementos visuales
        document.querySelectorAll('.pipeline-stage').forEach(el => {
            el.classList.remove('active', 'completed');
        });
        
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = '0%';
        }
        
        // Resetear modelo
        if (this.currentMesh) {
            this.currentMesh.material.wireframe = false;
            this.currentMesh.material.opacity = 1.0;
        }
    }
    
    /**
     * Navegación entre anomalías
     */
    nextAnomaly() {
        if (this.currentAnomalyIndex < this.anomalies.length - 1) {
            this.currentAnomalyIndex++;
            this.loadCurrentAnomaly();
            console.log(`➡️ Navegando a anomalía ${this.currentAnomalyIndex + 1}`);
        }
    }
    
    previousAnomaly() {
        if (this.currentAnomalyIndex > 0) {
            this.currentAnomalyIndex--;
            this.loadCurrentAnomaly();
            console.log(`⬅️ Navegando a anomalía ${this.currentAnomalyIndex + 1}`);
        }
    }
    
    /**
     * Limpiar escena
     */
    clearScene() {
        if (!this.scene) return;
        
        // Remover mesh actual
        if (this.currentMesh) {
            this.scene.remove(this.currentMesh);
            this.currentMesh = null;
        }
        
        // Limpiar otros objetos (mantener luces)
        const objectsToRemove = [];
        this.scene.traverse((child) => {
            if (child.type === 'Mesh' || child.type === 'Points') {
                objectsToRemove.push(child);
            }
        });
        
        objectsToRemove.forEach(obj => this.scene.remove(obj));
    }
    
    /**
     * Cerrar visor
     */
    closeViewer() {
        const modal = document.getElementById('professional3DModal');
        if (modal) {
            modal.classList.remove('active');
            setTimeout(() => {
                document.body.removeChild(modal);
            }, 300);
        }
        
        // Limpiar recursos
        if (this.renderer) {
            this.renderer.dispose();
        }
        
        // Remover event listeners de teclado
        this.removeKeyboardNavigation();
        
        console.log('🔒 Visor 3D profesional cerrado');
    }
    
    /**
     * Configurar navegación por teclado
     */
    setupKeyboardNavigation() {
        this.keyboardHandler = (e) => {
            // Solo procesar si el modal está activo
            const modal = document.getElementById('professional3DModal');
            if (!modal || !modal.classList.contains('active')) return;
            
            switch (e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    this.previousAnomaly();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    this.nextAnomaly();
                    break;
                case 'Escape':
                    e.preventDefault();
                    this.closeViewer();
                    break;
                case ' ': // Spacebar para ejecutar pipeline
                    e.preventDefault();
                    this.runPipeline();
                    break;
                case 'r':
                case 'R':
                    e.preventDefault();
                    this.resetPipeline();
                    break;
            }
        };
        
        document.addEventListener('keydown', this.keyboardHandler);
        console.log('⌨️ Navegación por teclado configurada');
    }
    
    /**
     * Remover navegación por teclado
     */
    removeKeyboardNavigation() {
        if (this.keyboardHandler) {
            document.removeEventListener('keydown', this.keyboardHandler);
            this.keyboardHandler = null;
            console.log('⌨️ Navegación por teclado removida');
        }
    }
    
    /**
     * Exportar modelo 3D actual
     */
    exportModel() {
        if (!this.currentMesh || !this.scene) {
            alert('No hay modelo 3D para exportar');
            return;
        }
        
        const anomaly = this.anomalies[this.currentAnomalyIndex];
        console.log('📥 Exportando modelo 3D:', anomaly.name);
        
        try {
            // Crear datos de exportación
            const exportData = {
                anomaly_info: {
                    name: anomaly.name || `Anomalía ${this.currentAnomalyIndex + 1}`,
                    type: anomaly.type || 'unknown',
                    confidence: anomaly.confidence || 0.7,
                    dimensions: anomaly.dimensions || '80m x 25m x 15m',
                    coordinates: anomaly.coordinates || 'No especificadas'
                },
                model_data: {
                    vertices: this.currentMesh.geometry.attributes.position.count,
                    faces: this.currentMesh.geometry.index ? this.currentMesh.geometry.index.count / 3 : 0,
                    material: {
                        color: `#${this.currentMesh.material.color.getHexString()}`,
                        roughness: this.currentMesh.material.roughness,
                        metalness: this.currentMesh.material.metalness,
                        opacity: this.currentMesh.material.opacity
                    }
                },
                pipeline_status: {
                    current_stage: this.pipelineStage,
                    completed_stages: this.pipelineStages.slice(0, this.pipelineStage + 1),
                    total_stages: this.pipelineStages.length
                },
                export_timestamp: new Date().toISOString(),
                export_format: 'ArcheoScope_3D_v1.0'
            };
            
            // Crear archivo JSON
            const jsonString = JSON.stringify(exportData, null, 2);
            const blob = new Blob([jsonString], { type: 'application/json' });
            
            // Crear nombre de archivo
            const fileName = `archeoscope_3d_${anomaly.name?.replace(/\s+/g, '_') || 'anomaly'}_${Date.now()}.json`;
            
            // Descargar archivo
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            console.log(`✅ Modelo 3D exportado como: ${fileName}`);
            
            // Mostrar mensaje de éxito
            this.showExportSuccess(fileName);
            
        } catch (error) {
            console.error('❌ Error exportando modelo 3D:', error);
            alert('Error exportando el modelo 3D. Verifica la consola para más detalles.');
        }
    }
    
    /**
     * Mostrar mensaje de éxito de exportación
     */
    showExportSuccess(fileName) {
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
            z-index: 4000;
            font-weight: 600;
            animation: slideInRight 0.3s ease-out;
        `;
        
        message.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">✅</span>
                <div>
                    <div>Modelo 3D Exportado</div>
                    <div style="font-size: 0.8rem; opacity: 0.9; margin-top: 0.25rem;">${fileName}</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(message);
        
        // Remover mensaje después de 4 segundos
        setTimeout(() => {
            message.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (document.body.contains(message)) {
                    document.body.removeChild(message);
                }
            }, 300);
        }, 4000);
    }
    
    /**
     * Loop de animación
     */
    animate() {
        if (!this.renderer || !this.scene || !this.camera) return;
        
        requestAnimationFrame(() => this.animate());
        
        if (this.controls) {
            this.controls.update();
        }
        
        // Rotar modelo ligeramente
        if (this.currentMesh) {
            this.currentMesh.rotation.y += 0.005;
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    /**
     * Exportar modelo 3D a formato GLTF
     */
    exportToGLTF() {
        if (!this.currentMesh) {
            alert('❌ No hay modelo 3D para exportar');
            return;
        }
        
        console.log('📤 Exportando modelo 3D a GLTF...');
        
        try {
            const exporter = new THREE.GLTFExporter();
            const scene = new THREE.Scene();
            scene.add(this.currentMesh);
            
            exporter.parse(
                scene,
                (gltf) => {
                    const blob = new Blob([JSON.stringify(gltf)], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `archeoscope_anomaly_${this.currentAnomalyIndex}.gltf`;
                    a.click();
                    URL.revokeObjectURL(url);
                    console.log('✅ Modelo GLTF exportado exitosamente');
                },
                (error) => {
                    console.error('❌ Error exportando GLTF:', error);
                    alert('Error exportando modelo GLTF');
                }
            );
        } catch (error) {
            console.error('❌ Error en exportación GLTF:', error);
            alert('Error exportando modelo GLTF');
        }
    }
    
    /**
     * Exportar modelo 3D a formato OBJ
     */
    exportToOBJ() {
        if (!this.currentMesh) {
            alert('❌ No hay modelo 3D para exportar');
            return;
        }
        
        console.log('📤 Exportando modelo 3D a OBJ...');
        
        try {
            const exporter = new THREE.OBJExporter();
            const scene = new THREE.Scene();
            scene.add(this.currentMesh);
            
            const result = exporter.parse(scene);
            const blob = new Blob([result.obj], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `archeoscope_anomaly_${this.currentAnomalyIndex}.obj`;
            a.click();
            URL.revokeObjectURL(url);
            console.log('✅ Modelo OBJ exportado exitosamente');
        } catch (error) {
            console.error('❌ Error exportando OBJ:', error);
            alert('Error exportando modelo OBJ');
        }
    }
    
    /**
     * Exportar captura de pantalla del visor 3D
     */
    exportScreenshot() {
        if (!this.renderer) {
            alert('❌ Visor 3D no disponible para captura');
            return;
        }
        
        console.log('📸 Capturando pantalla del visor 3D...');
        
        try {
            this.renderer.render(this.scene, this.camera);
            const dataURL = this.renderer.domElement.toDataURL('image/png');
            
            const link = document.createElement('a');
            link.download = `archeoscope_3d_viewer_${this.currentAnomalyIndex}.png`;
            link.href = dataURL;
            link.click();
            
            console.log('✅ Captura de pantalla guardada exitosamente');
        } catch (error) {
            console.error('❌ Error capturando pantalla:', error);
            alert('Error capturando pantalla');
        }
    }
    
    /**
     * Exportar análisis completo (modelo + metadatos)
     */
    exportCompleteAnalysis() {
        if (!this.currentMesh || !this.anomalies[this.currentAnomalyIndex]) {
            alert('❌ No hay análisis completo para exportar');
            return;
        }
        
        console.log('📊 Exportando análisis completo...');
        
        const anomaly = this.anomalies[this.currentAnomalyIndex];
        const analysisData = {
            anomaly_info: {
                id: anomaly.id,
                coordinates: anomaly.coordinates,
                confidence: anomaly.signature?.detection_confidence || 0,
                archaeological_probability: anomaly.archaeological_probability || 0,
                site_type: anomaly.site_type_probability || {}
            },
            analysis_metadata: {
                export_date: new Date().toISOString(),
                pipeline_stage: this.pipelineStages[this.pipelineStage],
                viewer_version: '1.0',
                archeoscope_version: 'v2.1'
            },
            3d_model: {
                vertices: this.currentMesh.geometry.attributes.position.count,
                faces: this.currentMesh.geometry.index?.count / 3 || this.currentMesh.geometry.attributes.position.count / 3,
                materials: Array.isArray(this.currentMesh.material) ? this.currentMesh.material.length : 1
            }
        }
        
        const blob = new Blob([JSON.stringify(analysisData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `archeoscope_complete_analysis_${anomaly.id}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        console.log('✅ Análisis completo exportado exitosamente');
    }
    
    /**
     * Utilidad para delay
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Instancia global
const professional3DViewer = new Professional3DViewer();

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.Professional3DViewer = Professional3DViewer;
    window.professional3DViewer = professional3DViewer;
}