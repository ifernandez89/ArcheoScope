/**
 * ArcheoScope - Aplicación del Visor Volumétrico LIDAR
 * Modelado Volumétrico Arqueológico (LIDAR + ArcheoScope)
 */

// Configuración adaptativa
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' ? 'http://localhost:8002' : '/api',
    VOLUMETRIC_API_URL: window.location.hostname === 'localhost' ? 'http://localhost:8002/volumetric' : '/api/volumetric',
    
    // Configuración visual adaptativa
    VISUAL: {
        BACKGROUND_COLOR: 0xf5f5f5,  // Gris claro más suave
        TERRAIN_COLOR: 0x8B7355,     // Color tierra más natural
        CAMERA_DISTANCE_FACTOR: 1.5,  // Factor para posición de cámara
        LIGHT_INTENSITY: 0.8,
        AMBIENT_INTENSITY: 0.4
    }
};

// Variables globales
let selectedSiteId = null;
let currentAnalysisResults = null;
let scene = null;
let camera = null;
let renderer = null;
let controls = null;
let activeLayers = new Set();

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando Visor Volumétrico ArcheoScope...');
    
    initializeEventListeners();
    loadSitesCatalog();
    checkSystemStatus();
});

function initializeEventListeners() {
    console.log('🔧 Configurando event listeners...');
    
    // Botones principales
    document.getElementById('analyzeBtn').addEventListener('click', performVolumetricAnalysis);
    document.getElementById('previewBtn').addEventListener('click', showSitePreview);
    document.getElementById('methodologyBtn').addEventListener('click', showMethodology);
    
    // Checkboxes de configuración
    document.getElementById('includeArcheoScope').addEventListener('change', updateAnalysisConfig);
    document.getElementById('performFusion').addEventListener('change', updateAnalysisConfig);
    document.getElementById('outputFormat').addEventListener('change', updateAnalysisConfig);
}

async function loadSitesCatalog() {
    console.log('📚 Cargando catálogo de sitios LIDAR...');
    
    const catalogLoading = document.getElementById('catalogLoading');
    const catalogStats = document.getElementById('catalogStats');
    const sitesGrid = document.getElementById('sitesGrid');
    
    catalogLoading.classList.add('active');
    
    try {
        const response = await fetch(`${CONFIG.VOLUMETRIC_API_URL}/sites/catalog`);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const catalogData = await response.json();
        
        // Actualizar estadísticas
        document.getElementById('archaeologicalCount').textContent = catalogData.archaeological_compatible with;
        document.getElementById('controlCount').textContent = catalogData.control_sites;
        
        // Mostrar estadísticas
        catalogLoading.classList.remove('active');
        catalogStats.style.display = 'block';
        
        // Renderizar sitios
        renderSitesGrid(catalogData.sites);
        
        console.log(`✅ Catálogo cargado: ${catalogData.total_sites} sitios`);
        
    } catch (error) {
        console.error('❌ Error cargando catálogo:', error);
        catalogLoading.innerHTML = `
            <div style="color: #dc3545; text-align: center;">
                <i class="fas fa-exclamation-triangle"></i><br>
                Error cargando catálogo de sitios<br>
                <small>${error.message}</small>
            </div>
        `;
    }
}

function renderSitesGrid(sites) {
    const sitesGrid = document.getElementById('sitesGrid');
    sitesGrid.innerHTML = '';
    
    Object.entries(sites).forEach(([siteId, site]) => {
        const siteCard = document.createElement('div');
        siteCard.className = 'site-card';
        siteCard.dataset.siteId = siteId;
        
        const siteTypeClass = site.site_type === 'archaeological_compatible with' ? 'archaeological' : 'control';
        const siteTypeIcon = site.site_type === 'archaeological_compatible with' ? '✔️' : '❌';
        const siteTypeText = site.site_type === 'archaeological_compatible with' ? 'Arqueológico Confirmado' : 'Control Negativo';
        
        siteCard.innerHTML = `
            <div class="site-name">${site.name}</div>
            <div class="site-type ${siteTypeClass}">${siteTypeIcon} ${siteTypeText}</div>
            <div class="site-details">
                <div><strong>LIDAR:</strong> ${site.lidar_type}</div>
                <div><strong>Resolución:</strong> ${site.resolution_cm}cm</div>
                <div><strong>Año:</strong> ${site.acquisition_year}</div>
                <div><strong>Fuente:</strong> ${site.official_source}</div>
            </div>
        `;
        
        siteCard.addEventListener('click', () => selectSite(siteId, site));
        sitesGrid.appendChild(siteCard);
    });
}

function selectSite(siteId, siteData) {
    console.log(`🎯 Sitio seleccionado: ${siteData.name}`);
    
    // Actualizar selección visual
    document.querySelectorAll('.site-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    document.querySelector(`[data-site-id="${siteId}"]`).classList.add('selected');
    
    // Actualizar estado global
    selectedSiteId = siteId;
    
    // Habilitar botones
    document.getElementById('analyzeBtn').disabled = false;
    document.getElementById('previewBtn').disabled = false;
    
    // Limpiar resultados anteriores
    hideResults();
    
    // Mostrar información del sitio en el visor
    showSiteInfo(siteData);
}

function showSiteInfo(siteData) {
    const viewerPlaceholder = document.getElementById('viewerPlaceholder');
    
    const siteTypeIcon = siteData.site_type === 'archaeological_compatible with' ? '🏛️' : '🏗️';
    const siteTypeText = siteData.site_type === 'archaeological_compatible with' ? 'Sitio Arqueológico Confirmado' : 'Sitio de Control';
    
    viewerPlaceholder.innerHTML = `
        <div style="text-align: center; max-width: 600px;">
            <div style="font-size: 3em; margin-bottom: 20px;">${siteTypeIcon}</div>
            <h2 style="color: #2a5298; margin-bottom: 15px;">${siteData.name}</h2>
            <div style="background: rgba(255,255,255,0.9); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: left;">
                    <div><strong>Tipo:</strong> ${siteTypeText}</div>
                    <div><strong>LIDAR:</strong> ${siteData.lidar_type}</div>
                    <div><strong>Resolución:</strong> ${siteData.resolution_cm}cm</div>
                    <div><strong>Año:</strong> ${siteData.acquisition_year}</div>
                    <div><strong>Coordenadas:</strong> ${siteData.coordinates[0].toFixed(4)}, ${siteData.coordinates[1].toFixed(4)}</div>
                    <div><strong>Fuente:</strong> ${siteData.official_source}</div>
                </div>
            </div>
            <div style="color: #666; font-size: 0.9em;">
                Presiona "Ejecutar Análisis Volumétrico" para procesar este sitio con el pipeline científico completo
            </div>
        </div>
    `;
}

async function performVolumetricAnalysis() {
    if (!selectedSiteId) {
        alert('Por favor selecciona un sitio del catálogo');
        return;
    }
    
    console.log(`🔬 Iniciando análisis volumétrico para sitio: ${selectedSiteId}`);
    
    const analysisLoading = document.getElementById('analysisLoading');
    const viewerPlaceholder = document.getElementById('viewerPlaceholder');
    const loadingMessage = document.getElementById('loadingMessage');
    
    // Mostrar loading
    viewerPlaceholder.style.display = 'none';
    analysisLoading.classList.add('active');
    
    // Configuración del análisis
    const analysisConfig = {
        site_id: selectedSiteId,
        include_archeoscope: document.getElementById('includeArcheoScope').checked,
        perform_fusion: document.getElementById('performFusion').checked,
        output_format: document.getElementById('outputFormat').value
    };
    
    try {
        // Paso 1: Análisis volumétrico LIDAR
        loadingMessage.textContent = '📊 Procesando datos LIDAR volumétricos...';
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simular procesamiento
        
        // Paso 2: Análisis ArcheoScope (si está habilitado)
        if (analysisConfig.include_archeoscope) {
            loadingMessage.textContent = '🛰️ Ejecutando análisis ArcheoScope paralelo...';
            await new Promise(resolve => setTimeout(resolve, 1500));
        }
        
        // Paso 3: Fusión probabilística (si está habilitada)
        if (analysisConfig.perform_fusion && analysisConfig.include_archeoscope) {
            loadingMessage.textContent = '🧬 Realizando fusión probabilística...';
            await new Promise(resolve => setTimeout(resolve, 1200));
        }
        
        // Paso 4: Generación de modelo 3D
        loadingMessage.textContent = '🎯 Generando modelo 3D interpretado...';
        await new Promise(resolve => setTimeout(resolve, 800));
        
        // Llamada a la API
        const response = await fetch(`${CONFIG.VOLUMETRIC_API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(analysisConfig)
        });
        
        if (!response.ok) {
            throw new Error(`Error en análisis: ${response.status}`);
        }
        
        const analysisResults = await response.json();
        
        // Procesar y mostrar resultados
        currentAnalysisResults = analysisResults;
        showAnalysisResults(analysisResults);
        
        console.log('✅ Análisis volumétrico completado');
        
    } catch (error) {
        console.error('❌ Error en análisis volumétrico:', error);
        
        analysisLoading.classList.remove('active');
        viewerPlaceholder.style.display = 'flex';
        viewerPlaceholder.innerHTML = `
            <div style="text-align: center; color: #dc3545;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3em; margin-bottom: 20px;"></i>
                <div>Error en el análisis volumétrico</div>
                <div style="font-size: 0.9em; margin-top: 10px;">${error.message}</div>
                <button class="btn btn-secondary" onclick="location.reload()" style="margin-top: 15px;">
                    Reintentar
                </button>
            </div>
        `;
    }
}

function showAnalysisResults(results) {
    console.log('📊 Mostrando resultados del análisis volumétrico');
    
    const analysisLoading = document.getElementById('analysisLoading');
    const resultsPanel = document.getElementById('resultsPanel');
    const metricsGrid = document.getElementById('metricsGrid');
    
    // Ocultar loading
    analysisLoading.classList.remove('active');
    
    // Mostrar panel de resultados
    resultsPanel.style.display = 'block';
    
    // Renderizar métricas
    renderMetrics(results);
    
    // Inicializar visor 3D
    if (results.model_3d) {
        initialize3DViewer(results.model_3d);
    }
    
    // Mostrar interpretación científica
    showScientificInterpretation(results);
}

function renderMetrics(results) {
    const metricsGrid = document.getElementById('metricsGrid');
    
    const volumetric = results.volumetric_analysis;
    const fusion = results.fusion_results;
    
    const metrics = [
        {
            label: 'Volumen Positivo',
            value: `${volumetric.positive_volume_m3.toFixed(2)} m³`,
            description: 'Rellenos observados'
        },
        {
            label: 'Volumen Negativo',
            value: `${volumetric.negative_volume_m3.toFixed(2)} m³`,
            description: 'Excavaciones observadas'
        },
        {
            label: 'Resolución LIDAR',
            value: `${results.site_info.resolution_cm}cm`,
            description: 'Precisión geométrica'
        },
        {
            label: 'Año Adquisición',
            value: results.site_info.acquisition_year,
            description: 'Fecha de los datos'
        }
    ];
    
    // Agregar métricas de fusión si están disponibles
    if (fusion) {
        metrics.push(
            {
                label: 'Convergencia',
                value: `${fusion.confidence_statistics.high_confidence_percentage.toFixed(1)}%`,
                description: 'Píxeles con alta confianza'
            },
            {
                label: 'Probabilidad Antrópica',
                value: `${(fusion.anthropic_probability_final.mean * 100).toFixed(1)}%`,
                description: 'Intervención humana observada'
            }
        );
    }
    
    metricsGrid.innerHTML = metrics.map(metric => `
        <div class="metric-card">
            <div class="value">${metric.value}</div>
            <div class="label">${metric.label}</div>
            <div style="font-size: 0.75em; color: #999; margin-top: 5px;">${metric.description}</div>
        </div>
    `).join('');
}

function initialize3DViewer(model3D) {
    console.log('🎯 Inicializando visor 3D...');
    
    const viewerContainer = document.querySelector('.viewer-container');
    const layerControls = document.getElementById('layerControls');
    
    // Crear contenedor del visor 3D
    const canvas = document.createElement('canvas');
    canvas.id = 'threejs-canvas';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    
    // Limpiar contenedor y agregar canvas
    viewerContainer.innerHTML = '';
    viewerContainer.appendChild(canvas);
    
    // Inicializar Three.js
    scene = new THREE.Scene();
    scene.background = new THREE.Color(CONFIG.VISUAL.BACKGROUND_COLOR);
    
    camera = new THREE.PerspectiveCamera(75, viewerContainer.clientWidth / viewerContainer.clientHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
    renderer.setSize(viewerContainer.clientWidth, viewerContainer.clientHeight);
    
    // Controles de cámara
    if (typeof THREE.OrbitControls !== 'undefined') {
        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
    }
    
    // Iluminación adaptativa
    const ambientLight = new THREE.AmbientLight(0x404040, CONFIG.VISUAL.AMBIENT_INTENSITY);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, CONFIG.VISUAL.LIGHT_INTENSITY);
    directionalLight.position.set(10, 10, 5);
    scene.add(directionalLight);
    
    // Crear geometría del modelo
    const modelBounds = create3DModel(model3D);
    
    // Posicionar cámara adaptativamente basada en el modelo
    const maxDimension = Math.max(modelBounds.width, modelBounds.height, modelBounds.depth);
    const cameraDistance = maxDimension * CONFIG.VISUAL.CAMERA_DISTANCE_FACTOR;
    
    camera.position.set(
        cameraDistance * 0.7, 
        cameraDistance * 0.5, 
        cameraDistance * 0.7
    );
    camera.lookAt(modelBounds.center.x, modelBounds.center.y, modelBounds.center.z);
    
    logger.info(`Cámara posicionada adaptativamente: distancia=${cameraDistance.toFixed(1)}, centro=${modelBounds.center.x.toFixed(1)},${modelBounds.center.y.toFixed(1)},${modelBounds.center.z.toFixed(1)}`);
    
    // Mostrar controles de capas
    layerControls.style.display = 'block';
    setupLayerControls(model3D.activatable_layers);
    
    // Iniciar renderizado
    animate();
    
    // Manejar redimensionamiento
    window.addEventListener('resize', onWindowResize);
}

function create3DModel(model3D) {
    console.log('🏗️ Creando modelo 3D adaptativo...');
    
    const vertices = new Float32Array(model3D.vertices.flat());
    const faces = new Uint32Array(model3D.faces.flat());
    
    // Calcular bounds del modelo para posicionamiento adaptativo
    const bounds = {
        min: { x: Infinity, y: Infinity, z: Infinity },
        max: { x: -Infinity, y: -Infinity, z: -Infinity }
    };
    
    for (let i = 0; i < vertices.length; i += 3) {
        bounds.min.x = Math.min(bounds.min.x, vertices[i]);
        bounds.max.x = Math.max(bounds.max.x, vertices[i]);
        bounds.min.y = Math.min(bounds.min.y, vertices[i + 1]);
        bounds.max.y = Math.max(bounds.max.y, vertices[i + 1]);
        bounds.min.z = Math.min(bounds.min.z, vertices[i + 2]);
        bounds.max.z = Math.max(bounds.max.z, vertices[i + 2]);
    }
    
    const modelBounds = {
        width: bounds.max.x - bounds.min.x,
        height: bounds.max.y - bounds.min.y,
        depth: bounds.max.z - bounds.min.z,
        center: {
            x: (bounds.max.x + bounds.min.x) / 2,
            y: (bounds.max.y + bounds.min.y) / 2,
            z: (bounds.max.z + bounds.min.z) / 2
        }
    };
    
    // Crear geometría
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    geometry.setIndex(new THREE.BufferAttribute(faces, 1));
    geometry.computeVertexNormals();
    
    // Material adaptativo basado en datos del modelo
    let materialColor = CONFIG.VISUAL.TERRAIN_COLOR;
    let opacity = 0.8;
    
    // Adaptar color según tipo de sitio si está disponible
    if (model3D.metadata && model3D.metadata.site_type) {
        switch (model3D.metadata.site_type) {
            case 'archaeological_compatible with':
                materialColor = 0x8B4513; // Marrón arqueológico
                break;
            case 'modern_control':
                materialColor = 0x708090; // Gris moderno
                break;
            case 'natural_control':
                materialColor = 0x228B22; // Verde natural
                break;
        }
    }
    
    const material = new THREE.MeshLambertMaterial({
        color: materialColor,
        wireframe: false,
        transparent: true,
        opacity: opacity
    });
    
    // Crear mesh
    const mesh = new THREE.Mesh(geometry, material);
    mesh.name = 'terrain_base';
    scene.add(mesh);
    
    // Agregar atributos de vértice como colores si están disponibles
    if (model3D.vertex_attributes && model3D.vertex_attributes.anthropic_probability) {
        const probabilities = model3D.vertex_attributes.anthropic_probability;
        const colors = new Float32Array(probabilities.length * 3);
        
        for (let i = 0; i < probabilities.length; i++) {
            const prob = probabilities[i];
            // Color mapping adaptativo: azul (bajo) -> verde (medio) -> rojo (alto)
            colors[i * 3] = Math.min(1.0, prob * 1.5); // R
            colors[i * 3 + 1] = Math.sin(prob * Math.PI); // G (pico en 0.5)
            colors[i * 3 + 2] = Math.max(0.0, 1.0 - prob * 1.5); // B
        }
        
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        material.vertexColors = true;
    }
    
    console.log(`Modelo 3D creado: ${vertices.length/3} vértices, bounds: ${modelBounds.width.toFixed(1)}x${modelBounds.height.toFixed(1)}x${modelBounds.depth.toFixed(1)}`);
    
    return modelBounds;
}

function setupLayerControls(activatableLayers) {
    const layerControlsList = document.getElementById('layerControlsList');
    layerControlsList.innerHTML = '';
    
    Object.entries(activatableLayers).forEach(([layerId, layer]) => {
        const layerControl = document.createElement('div');
        layerControl.className = 'layer-control';
        layerControl.dataset.layerId = layerId;
        
        layerControl.innerHTML = `
            <input type="checkbox" id="layer_${layerId}" checked>
            <label for="layer_${layerId}">${layer.name}</label>
        `;
        
        const checkbox = layerControl.querySelector('input');
        checkbox.addEventListener('change', (e) => {
            toggleLayer(layerId, e.target.checked);
        });
        
        layerControlsList.appendChild(layerControl);
        
        // Activar capa por defecto
        activeLayers.add(layerId);
    });
}

function toggleLayer(layerId, enabled) {
    console.log(`🔄 Toggling layer: ${layerId} = ${enabled}`);
    
    if (enabled) {
        activeLayers.add(layerId);
    } else {
        activeLayers.delete(layerId);
    }
    
    // Actualizar visualización del modelo 3D
    updateModelVisualization();
}

function updateModelVisualization() {
    // Actualizar la visualización basada en las capas activas
    const terrainMesh = scene.getObjectByName('terrain_base');
    if (terrainMesh) {
        // Ajustar opacidad y colores basado en capas activas
        let opacity = 0.8;
        let wireframe = false;
        
        if (activeLayers.has('geometry_pure')) {
            wireframe = true;
            opacity = 1.0;
        }
        
        terrainMesh.material.wireframe = wireframe;
        terrainMesh.material.opacity = opacity;
        terrainMesh.material.needsUpdate = true;
    }
}

function animate() {
    requestAnimationFrame(animate);
    
    if (controls) {
        controls.update();
    }
    
    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

function onWindowResize() {
    if (camera && renderer) {
        const viewerContainer = document.querySelector('.viewer-container');
        camera.aspect = viewerContainer.clientWidth / viewerContainer.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(viewerContainer.clientWidth, viewerContainer.clientHeight);
    }
}

function showScientificInterpretation(results) {
    const interpretationDiv = document.getElementById('scientificInterpretation');
    
    const siteInfo = results.site_info;
    const volumetric = results.volumetric_analysis;
    const fusion = results.fusion_results;
    
    let interpretation = `
        <div style="background: #f8f9fa; border-left: 4px solid #2a5298; padding: 15px; border-radius: 4px;">
            <h4 style="color: #2a5298; margin-bottom: 10px;">
                <i class="fas fa-microscope"></i> Interpretación Científica
            </h4>
    `;
    
    // Información del sitio
    interpretation += `
        <div style="margin-bottom: 15px;">
            <strong>Sitio:</strong> ${siteInfo.name}<br>
            <strong>Tipo:</strong> ${siteInfo.site_type === 'archaeological_compatible with' ? '✔️ Arqueológico Confirmado' : '❌ Control Negativo'}<br>
            <strong>Datos LIDAR:</strong> ${siteInfo.lidar_type}, ${siteInfo.resolution_cm}cm, ${siteInfo.acquisition_year}
        </div>
    `;
    
    // Análisis volumétrico
    interpretation += `
        <div style="margin-bottom: 15px;">
            <strong>📊 Análisis Volumétrico LIDAR:</strong><br>
            • Volumen positivo (rellenos): ${volumetric.positive_volume_m3.toFixed(2)} m³<br>
            • Volumen negativo (excavaciones): ${volumetric.negative_volume_m3.toFixed(2)} m³<br>
            • Significancia volumétrica: ${(volumetric.positive_volume_m3 + volumetric.negative_volume_m3) > 1.0 ? 'Significativa' : 'Mínima'}
        </div>
    `;
    
    // Fusión (si está disponible)
    if (fusion) {
        interpretation += `
            <div style="margin-bottom: 15px;">
                <strong>🧬 Fusión Probabilística:</strong><br>
                • Probabilidad antrópica promedio: ${(fusion.anthropic_probability_final.mean * 100).toFixed(1)}%<br>
                • Píxeles con alta confianza: ${fusion.confidence_statistics.high_confidence_percentage.toFixed(1)}%<br>
                • Convergencia de evidencias: ${fusion.confidence_statistics.high_confidence_percentage > 60 ? 'Fuerte' : 'Moderada'}
            </div>
        `;
    }
    
    // Limitaciones
    interpretation += `
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 4px; margin-top: 15px;">
            <strong>⚠️ Limitaciones Científicas:</strong><br>
            • Interpretación basada en datos disponibles<br>
            • Resolución limitada por LIDAR original (${siteInfo.resolution_cm}cm)<br>
            • Análisis espectral sujeto a condiciones atmosféricas<br>
            • Fusión probabilística no garantiza certeza arqueológica
        </div>
    `;
    
    interpretation += '</div>';
    
    interpretationDiv.innerHTML = interpretation;
}

async function showSitePreview() {
    if (!selectedSiteId) {
        alert('Por favor selecciona un sitio del catálogo');
        return;
    }
    
    console.log(`👁️ Mostrando vista previa para sitio: ${selectedSiteId}`);
    
    try {
        const response = await fetch(`${CONFIG.VOLUMETRIC_API_URL}/sites/${selectedSiteId}/preview`);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const previewData = await response.json();
        
        // Mostrar vista previa en modal o panel
        showPreviewModal(previewData);
        
    } catch (error) {
        console.error('❌ Error en vista previa:', error);
        alert(`Error obteniendo vista previa: ${error.message}`);
    }
}

function showPreviewModal(previewData) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.8); z-index: 1000;
        display: flex; align-items: center; justify-content: center;
    `;
    
    const content = document.createElement('div');
    content.style.cssText = `
        background: white; padding: 30px; border-radius: 8px;
        max-width: 500px; width: 90%;
    `;
    
    const siteInfo = previewData.site_info;
    const volumetric = previewData.volumetric_preview;
    
    content.innerHTML = `
        <h3 style="color: #2a5298; margin-bottom: 20px;">
            <i class="fas fa-eye"></i> Vista Previa - ${siteInfo.name}
        </h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
            <div><strong>Tipo:</strong> ${siteInfo.site_type === 'archaeological_compatible with' ? '✔️ Arqueológico' : '❌ Control'}</div>
            <div><strong>LIDAR:</strong> ${siteInfo.lidar_type}</div>
            <div><strong>Resolución:</strong> ${siteInfo.resolution_cm}cm</div>
            <div><strong>Volumen Total:</strong> ${volumetric.total_volume_m3.toFixed(2)} m³</div>
            <div><strong>Pendiente Promedio:</strong> ${volumetric.average_slope_degrees.toFixed(1)}°</div>
            <div><strong>Rugosidad:</strong> ${volumetric.average_roughness.toFixed(3)}</div>
        </div>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
            <strong>Calidad de Datos:</strong> ${volumetric.data_quality.resolution_quality}<br>
            <strong>Significancia Volumétrica:</strong> ${volumetric.data_quality.volume_significance}<br>
            <strong>Complejidad Topográfica:</strong> ${volumetric.data_quality.topographic_complexity}
        </div>
        
        <button class="btn btn-primary" onclick="this.parentElement.parentElement.remove()" style="width: 100%;">
            Cerrar Vista Previa
        </button>
    `;
    
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    // Cerrar al hacer clic fuera
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

async function showMethodology() {
    console.log('📖 Mostrando metodología científica completa...');
    
    try {
        const response = await fetch(`${CONFIG.VOLUMETRIC_API_URL}/methodology`);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const methodology = await response.json();
        
        // Mostrar metodología en modal
        showMethodologyModal(methodology);
        
    } catch (error) {
        console.error('❌ Error obteniendo metodología:', error);
        alert(`Error obteniendo metodología: ${error.message}`);
    }
}

function showMethodologyModal(methodology) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.8); z-index: 1000;
        display: flex; align-items: center; justify-content: center;
        overflow-y: auto; padding: 20px;
    `;
    
    const content = document.createElement('div');
    content.style.cssText = `
        background: white; padding: 30px; border-radius: 8px;
        max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto;
    `;
    
    let methodologyHTML = `
        <h3 style="color: #2a5298; margin-bottom: 20px;">
            <i class="fas fa-microscope"></i> ${methodology.module_name}
        </h3>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
            <h4>🧠 Principio Científico</h4>
            <p style="font-style: italic; margin-top: 10px;">${methodology.scientific_principle}</p>
        </div>
        
        <h4 style="color: #495057; margin-bottom: 15px;">📋 Arquitectura del Pipeline</h4>
    `;
    
    // Pipeline steps
    Object.entries(methodology.pipeline_architecture).forEach(([stepKey, step]) => {
        methodologyHTML += `
            <div style="background: #f8f9fa; border-left: 4px solid #2a5298; padding: 15px; margin-bottom: 10px; border-radius: 4px;">
                <strong>${step.name}</strong><br>
                <span style="color: #666;">${step.description}</span><br>
                <small style="color: #28a745;"><strong>Output:</strong> ${step.output}</small>
            </div>
        `;
    });
    
    // Fusion weights
    methodologyHTML += `
        <h4 style="color: #495057; margin: 20px 0 15px 0;">⚖️ Pesos de Fusión</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
    `;
    
    Object.entries(methodology.fusion_weights).forEach(([key, weight]) => {
        methodologyHTML += `
            <div style="background: #e9ecef; padding: 10px; border-radius: 4px;">
                <strong>${key.replace('_', ' ')}:</strong> ${(weight * 100).toFixed(0)}%
            </div>
        `;
    });
    
    methodologyHTML += '</div>';
    
    // Scientific rules
    methodologyHTML += `
        <h4 style="color: #495057; margin-bottom: 15px;">🔬 Reglas Científicas</h4>
        <ul style="margin-left: 20px; margin-bottom: 20px;">
    `;
    
    methodology.validation_approach.scientific_rules.forEach(rule => {
        methodologyHTML += `<li style="margin-bottom: 5px;">${rule}</li>`;
    });
    
    methodologyHTML += '</ul>';
    
    // Limitations
    methodologyHTML += `
        <h4 style="color: #495057; margin-bottom: 15px;">⚠️ Limitaciones</h4>
        <ul style="margin-left: 20px; margin-bottom: 20px;">
    `;
    
    methodology.limitations.forEach(limitation => {
        methodologyHTML += `<li style="margin-bottom: 5px;">${limitation}</li>`;
    });
    
    methodologyHTML += `
        </ul>
        
        <button class="btn btn-primary" onclick="this.parentElement.parentElement.remove()" style="width: 100%; margin-top: 20px;">
            Cerrar Metodología
        </button>
    `;
    
    content.innerHTML = methodologyHTML;
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    // Cerrar al hacer clic fuera
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

function updateAnalysisConfig() {
    const includeArcheoScope = document.getElementById('includeArcheoScope').checked;
    const performFusion = document.getElementById('performFusion').checked;
    
    // Deshabilitar fusión si ArcheoScope no está incluido
    document.getElementById('performFusion').disabled = !includeArcheoScope;
    
    if (!includeArcheoScope) {
        document.getElementById('performFusion').checked = false;
    }
}

function hideResults() {
    document.getElementById('resultsPanel').style.display = 'none';
    document.getElementById('layerControls').style.display = 'none';
    
    // Limpiar visor 3D
    if (scene) {
        while (scene.children.length > 0) {
            scene.remove(scene.children[0]);
        }
    }
    
    currentAnalysisResults = null;
    activeLayers.clear();
}

async function checkSystemStatus() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/status`);
        if (response.ok) {
            console.log('✅ Sistema ArcheoScope conectado');
        }
    } catch (error) {
        console.warn('⚠️ Sistema ArcheoScope no disponible:', error);
    }
}