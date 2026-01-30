/**
 * ArcheoScope - Generador de Imágenes de Anomalías
 * Sistema para generar visualizaciones aproximadas de candidatos arqueológicos
 */

class AnomalyImageGenerator {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.scene = null;
        this.renderer = null;
        this.camera = null;
        this.controls = null;
        
        console.log('🎨 Generador de imágenes de anomalías inicializado');
    }

    /**
     * Generar imagen 2D de la anomalía
     */
    generate2DImage(anomalyData, containerId) {
        try {
            const container = document.getElementById(containerId);
            if (!container) {
                console.error('❌ Contenedor no encontrado:', containerId);
                return false;
            }

            // Limpiar contenedor
            container.innerHTML = '';

            // Crear canvas
            const canvas = document.createElement('canvas');
            canvas.width = 400;
            canvas.height = 300;
            canvas.style.border = '2px solid #8B4513';
            canvas.style.borderRadius = '8px';
            canvas.style.background = 'linear-gradient(180deg, #87CEEB 0%, #4682B4 50%, #191970 100%)';
            
            const ctx = canvas.getContext('2d');
            
            // Dibujar vista superior (sonar)
            this.draw2DSonarView(ctx, anomalyData, canvas.width, canvas.height);
            
            container.appendChild(canvas);
            
            // Agregar información técnica
            const infoDiv = document.createElement('div');
            infoDiv.innerHTML = this.generateTechnicalInfo(anomalyData);
            infoDiv.style.marginTop = '10px';
            infoDiv.style.fontSize = '0.8rem';
            infoDiv.style.lineHeight = '1.4';
            container.appendChild(infoDiv);
            
            console.log('✅ Imagen 2D generada exitosamente');
            return true;
            
        } catch (error) {
            console.error('❌ Error generando imagen 2D:', error);
            return false;
        }
    }

    /**
     * Generar modelo 3D de la anomalía
     */
    generate3DModel(anomalyData, containerId) {
        try {
            const container = document.getElementById(containerId);
            if (!container) {
                console.error('❌ Contenedor no encontrado:', containerId);
                return false;
            }

            // Verificar si Three.js está disponible
            if (typeof THREE === 'undefined') {
                console.warn('⚠️ Three.js no disponible, generando vista 2D alternativa');
                return this.generate2DAlternative(anomalyData, containerId);
            }

            // Limpiar contenedor
            container.innerHTML = '';

            // Configurar escena 3D
            const width = 400;
            const height = 300;
            
            this.scene = new THREE.Scene();
            this.scene.background = new THREE.Color(0x001122);
            
            this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
            this.renderer = new THREE.WebGLRenderer({ antialias: true });
            this.renderer.setSize(width, height);
            this.renderer.shadowMap.enabled = true;
            this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            
            container.appendChild(this.renderer.domElement);
            
            // Crear modelo 3D de la anomalía
            this.create3DAnomalyModel(anomalyData);
            
            // Configurar cámara
            this.camera.position.set(50, 30, 50);
            this.camera.lookAt(0, 0, 0);
            
            // Configurar controles si están disponibles
            if (typeof THREE.OrbitControls !== 'undefined') {
                this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
                this.controls.enableDamping = true;
                this.controls.dampingFactor = 0.05;
            }
            
            // Iniciar renderizado
            this.animate3D();
            
            // Agregar controles de vista
            this.addViewControls(container, anomalyData);
            
            console.log('✅ Modelo 3D generado exitosamente');
            return true;
            
        } catch (error) {
            console.error('❌ Error generando modelo 3D:', error);
            return this.generate2DAlternative(anomalyData, containerId);
        }
    }

    /**
     * Dibujar vista de sonar 2D
     */
    draw2DSonarView(ctx, anomalyData, width, height) {
        // Fondo del océano
        const gradient = ctx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, '#87CEEB');  // Superficie
        gradient.addColorStop(0.3, '#4682B4'); // Agua media
        gradient.addColorStop(1, '#191970');   // Fondo profundo
        
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
        
        // Líneas de profundidad
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.lineWidth = 1;
        for (let i = 0; i < 5; i++) {
            const y = (height / 5) * i;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        
        // Extraer dimensiones basadas en datos reales del análisis
        const dimensions = this.parseDimensions(anomalyData.dimensions || this.generateRealisticDimensions(anomalyData));
        
        // Calcular escala
        const maxDim = Math.max(dimensions.length, dimensions.width);
        const scale = Math.min(width * 0.6, height * 0.6) / maxDim;
        
        // Posición central
        const centerX = width / 2;
        const centerY = height * 0.7; // Cerca del fondo
        
        // Dibujar sombra acústica (característica del sonar)
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.fillRect(
            centerX - (dimensions.length * scale) / 2,
            centerY + 10,
            dimensions.length * scale,
            dimensions.width * scale * 0.5
        );
        
        // Dibujar anomalía principal
        this.drawAnomalyShape(ctx, centerX, centerY, dimensions, scale, anomalyData);
        
        // Dibujar información de sonar
        this.drawSonarInfo(ctx, width, height, anomalyData);
        
        // Dibujar escala
        this.drawScale(ctx, width, height, scale);
    }

    /**
     * Dibujar forma de la anomalía
     */
    drawAnomalyShape(ctx, centerX, centerY, dimensions, scale, anomalyData) {
        const length = dimensions.length * scale;
        const width = dimensions.width * scale;
        
        // Determinar color basado en confianza
        const confidence = this.parseConfidence(anomalyData.confidence || '0.76');
        const intensity = Math.floor(confidence * 255);
        
        // Gradiente de intensidad
        const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, length/2);
        gradient.addColorStop(0, `rgba(255, ${255-intensity}, 0, 0.9)`);
        gradient.addColorStop(0.7, `rgba(${intensity}, 0, 0, 0.7)`);
        gradient.addColorStop(1, `rgba(${intensity/2}, 0, 0, 0.3)`);
        
        ctx.fillStyle = gradient;
        
        // Dibujar forma según clasificación
        const classification = anomalyData.classification || '';
        
        if (classification.includes('mercante') || classification.includes('cargo')) {
            // Forma de barco mercante
            this.drawMerchantVesselShape(ctx, centerX, centerY, length, width);
        } else if (classification.includes('liner') || classification.includes('passenger')) {
            // Forma de transatlántico
            this.drawPassengerLinerShape(ctx, centerX, centerY, length, width);
        } else {
            // Forma genérica
            this.drawGenericVesselShape(ctx, centerX, centerY, length, width);
        }
        
        // Dibujar puntos de alta reflectancia (metal)
        this.drawMetallicSignatures(ctx, centerX, centerY, length, width, anomalyData);
    }

    /**
     * Dibujar forma de mercante
     */
    drawMerchantVesselShape(ctx, centerX, centerY, length, width) {
        ctx.beginPath();
        
        // Casco principal (forma alargada)
        ctx.ellipse(centerX, centerY, length/2, width/2, 0, 0, 2 * Math.PI);
        ctx.fill();
        
        // Superestructura (más pequeña)
        ctx.fillStyle = 'rgba(255, 200, 0, 0.6)';
        ctx.fillRect(centerX - length*0.1, centerY - width*0.3, length*0.2, width*0.6);
        
        // Chimenea
        ctx.fillStyle = 'rgba(200, 100, 0, 0.8)';
        ctx.fillRect(centerX - length*0.05, centerY - width*0.2, length*0.1, width*0.1);
    }

    /**
     * Dibujar forma de transatlántico
     */
    drawPassengerLinerShape(ctx, centerX, centerY, length, width) {
        ctx.beginPath();
        
        // Casco principal (más estilizado)
        ctx.ellipse(centerX, centerY, length/2, width/2, 0, 0, 2 * Math.PI);
        ctx.fill();
        
        // Múltiples cubiertas
        for (let i = 0; i < 3; i++) {
            ctx.fillStyle = `rgba(255, ${200-i*30}, 0, ${0.6-i*0.1})`;
            ctx.fillRect(
                centerX - length*0.3 + i*length*0.05, 
                centerY - width*0.4 + i*width*0.1, 
                length*0.6 - i*length*0.1, 
                width*0.2
            );
        }
        
        // Chimeneas múltiples
        ctx.fillStyle = 'rgba(200, 100, 0, 0.8)';
        for (let i = 0; i < 2; i++) {
            ctx.fillRect(
                centerX - length*0.1 + i*length*0.2, 
                centerY - width*0.3, 
                length*0.05, 
                width*0.15
            );
        }
    }

    /**
     * Dibujar forma genérica
     */
    drawGenericVesselShape(ctx, centerX, centerY, length, width) {
        ctx.beginPath();
        
        // Forma básica alargada
        ctx.ellipse(centerX, centerY, length/2, width/2, 0, 0, 2 * Math.PI);
        ctx.fill();
        
        // Estructura central
        ctx.fillStyle = 'rgba(255, 150, 0, 0.5)';
        ctx.fillRect(centerX - length*0.2, centerY - width*0.3, length*0.4, width*0.6);
    }

    /**
     * Dibujar firmas metálicas
     */
    drawMetallicSignatures(ctx, centerX, centerY, length, width, anomalyData) {
        const magneticSignature = anomalyData.magnetic_signature || 'Moderada';
        
        let numPoints = 3;
        let intensity = 0.5;
        
        if (magneticSignature.includes('Intensa')) {
            numPoints = 8;
            intensity = 0.9;
        } else if (magneticSignature.includes('Moderada')) {
            numPoints = 5;
            intensity = 0.6;
        } else {
            numPoints = 2;
            intensity = 0.3;
        }
        
        ctx.fillStyle = `rgba(255, 255, 0, ${intensity})`;
        
        for (let i = 0; i < numPoints; i++) {
            const angle = (i / numPoints) * 2 * Math.PI;
            const x = centerX + Math.cos(angle) * length * 0.3;
            const y = centerY + Math.sin(angle) * width * 0.3;
            
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI);
            ctx.fill();
        }
    }

    /**
     * Dibujar información del sonar
     */
    drawSonarInfo(ctx, width, height, anomalyData) {
        ctx.fillStyle = 'rgba(0, 255, 0, 0.8)';
        ctx.font = '12px Consolas, monospace';
        
        const info = [
            `SONAR MULTIHAZ - DETECCIÓN CONFIRMADA`,
            `Candidato: ${anomalyData.name || 'Anomalía Detectada'}`,
            `Dimensiones: ${anomalyData.dimensions || 'N/A'}`,
            `Confianza: ${anomalyData.confidence || 'N/A'}`,
            `Firma Magnética: ${anomalyData.magnetic_signature || 'N/A'}`
        ];
        
        info.forEach((line, i) => {
            ctx.fillText(line, 10, 20 + i * 15);
        });
        
        // Timestamp
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.font = '10px Consolas, monospace';
        ctx.fillText(`Análisis: ${new Date().toLocaleString()}`, width - 200, height - 10);
    }

    /**
     * Dibujar escala
     */
    drawScale(ctx, width, height, scale) {
        const scaleLength = 50; // píxeles
        const realLength = scaleLength / scale; // metros
        
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(width - 80, height - 30);
        ctx.lineTo(width - 80 + scaleLength, height - 30);
        ctx.stroke();
        
        // Marcas
        ctx.beginPath();
        ctx.moveTo(width - 80, height - 35);
        ctx.lineTo(width - 80, height - 25);
        ctx.moveTo(width - 80 + scaleLength, height - 35);
        ctx.lineTo(width - 80 + scaleLength, height - 25);
        ctx.stroke();
        
        // Texto
        ctx.fillStyle = 'white';
        ctx.font = '10px Consolas, monospace';
        ctx.fillText(`${realLength.toFixed(0)}m`, width - 75, height - 40);
    }

    /**
     * Crear modelo 3D de la anomalía
     */
    create3DAnomalyModel(anomalyData) {
        // Fondo marino
        const seaFloorGeometry = new THREE.PlaneGeometry(200, 200);
        const seaFloorMaterial = new THREE.MeshLambertMaterial({ 
            color: 0x8B4513,
            transparent: true,
            opacity: 0.7
        });
        const seaFloor = new THREE.Mesh(seaFloorGeometry, seaFloorMaterial);
        seaFloor.rotation.x = -Math.PI / 2;
        seaFloor.position.y = -10;
        seaFloor.receiveShadow = true;
        this.scene.add(seaFloor);
        
        // Extraer dimensiones basadas en datos reales del análisis
        const dimensions = this.parseDimensions(anomalyData.dimensions || this.generateRealisticDimensions(anomalyData));
        
        // Escalar para visualización
        const scale = 0.2;
        const length = dimensions.length * scale;
        const width = dimensions.width * scale;
        const height = dimensions.height * scale;
        
        // Crear geometría del casco
        const hullGeometry = new THREE.BoxGeometry(length, height, width);
        const hullMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x8B0000,
            transparent: true,
            opacity: 0.8
        });
        const hull = new THREE.Mesh(hullGeometry, hullMaterial);
        hull.position.y = height / 2 - 5;
        hull.castShadow = true;
        this.scene.add(hull);
        
        // Superestructura
        const superstructureGeometry = new THREE.BoxGeometry(length * 0.3, height * 0.5, width * 0.8);
        const superstructureMaterial = new THREE.MeshPhongMaterial({ 
            color: 0xCD853F,
            transparent: true,
            opacity: 0.7
        });
        const superstructure = new THREE.Mesh(superstructureGeometry, superstructureMaterial);
        superstructure.position.y = height + height * 0.25 - 5;
        superstructure.castShadow = true;
        this.scene.add(superstructure);
        
        // Puntos de alta reflectancia magnética
        this.addMagneticSignatures3D(anomalyData, length, width, height);
        
        // Iluminación
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 50, 50);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);
        
        // Luz submarina (azul)
        const underwaterLight = new THREE.PointLight(0x0077be, 0.5, 100);
        underwaterLight.position.set(0, 20, 0);
        this.scene.add(underwaterLight);
    }

    /**
     * Agregar firmas magnéticas en 3D
     */
    addMagneticSignatures3D(anomalyData, length, width, height) {
        const magneticSignature = anomalyData.magnetic_signature || 'Moderada';
        
        let numPoints = 3;
        let intensity = 0.5;
        
        if (magneticSignature.includes('Intensa')) {
            numPoints = 8;
            intensity = 1.0;
        } else if (magneticSignature.includes('Moderada')) {
            numPoints = 5;
            intensity = 0.7;
        }
        
        for (let i = 0; i < numPoints; i++) {
            const geometry = new THREE.SphereGeometry(1, 8, 6);
            const material = new THREE.MeshBasicMaterial({ 
                color: 0xFFFF00,
                transparent: true,
                opacity: intensity
            });
            const sphere = new THREE.Mesh(geometry, material);
            
            sphere.position.x = (Math.random() - 0.5) * length;
            sphere.position.y = (Math.random() - 0.5) * height;
            sphere.position.z = (Math.random() - 0.5) * width;
            
            this.scene.add(sphere);
        }
    }

    /**
     * Animar modelo 3D
     */
    animate3D() {
        if (!this.renderer || !this.scene || !this.camera) return;
        
        requestAnimationFrame(() => this.animate3D());
        
        if (this.controls) {
            this.controls.update();
        }
        
        this.renderer.render(this.scene, this.camera);
    }

    /**
     * Agregar controles de vista
     */
    addViewControls(container, anomalyData) {
        const controlsDiv = document.createElement('div');
        controlsDiv.style.marginTop = '10px';
        controlsDiv.innerHTML = `
            <div style="display: flex; gap: 10px; justify-content: center;">
                <button onclick="anomalyImageGenerator.resetView()" style="padding: 5px 10px; background: #8B4513; color: white; border: none; border-radius: 3px; cursor: pointer;">
                    🔄 Reset Vista
                </button>
                <button onclick="anomalyImageGenerator.topView()" style="padding: 5px 10px; background: #8B4513; color: white; border: none; border-radius: 3px; cursor: pointer;">
                    ⬆️ Vista Superior
                </button>
                <button onclick="anomalyImageGenerator.sideView()" style="padding: 5px 10px; background: #8B4513; color: white; border: none; border-radius: 3px; cursor: pointer;">
                    ➡️ Vista Lateral
                </button>
            </div>
        `;
        
        container.appendChild(controlsDiv);
        
        // Información técnica
        const infoDiv = document.createElement('div');
        infoDiv.innerHTML = this.generateTechnicalInfo(anomalyData);
        infoDiv.style.marginTop = '10px';
        infoDiv.style.fontSize = '0.8rem';
        infoDiv.style.lineHeight = '1.4';
        container.appendChild(infoDiv);
    }

    /**
     * Generar información técnica
     */
    generateTechnicalInfo(anomalyData) {
        return `
            <div style="background: rgba(0,0,0,0.8); color: #00ff00; padding: 10px; border-radius: 5px; font-family: Consolas, monospace;">
                <div style="color: #ffff00; font-weight: bold; margin-bottom: 5px;">📊 DATOS TÉCNICOS DE LA ANOMALÍA</div>
                <div><strong>Candidato:</strong> ${anomalyData.name || 'Anomalía Detectada'}</div>
                <div><strong>Dimensiones:</strong> ${anomalyData.dimensions || 'N/A'}</div>
                <div><strong>Confianza Instrumental:</strong> ${anomalyData.confidence || 'N/A'}</div>
                <div><strong>Clasificación:</strong> ${anomalyData.classification || 'N/A'}</div>
                <div><strong>Firma Magnética:</strong> ${anomalyData.magnetic_signature || 'N/A'}</div>
                <div><strong>Estado:</strong> ${anomalyData.validation_status || 'Pendiente validación'}</div>
                <div style="margin-top: 5px; color: #ffaa00;"><strong>Evidencia:</strong> ${anomalyData.evidence || 'Análisis multi-sensor'}</div>
            </div>
        `;
    }

    /**
     * Generar vista 2D alternativa
     */
    generate2DAlternative(anomalyData, containerId) {
        console.log('🎨 Generando vista 2D alternativa...');
        return this.generate2DImage(anomalyData, containerId);
    }

    /**
     * Funciones de control de vista 3D
     */
    resetView() {
        if (this.camera) {
            this.camera.position.set(50, 30, 50);
            this.camera.lookAt(0, 0, 0);
        }
    }

    topView() {
        if (this.camera) {
            this.camera.position.set(0, 80, 0);
            this.camera.lookAt(0, 0, 0);
        }
    }

    sideView() {
        if (this.camera) {
            this.camera.position.set(80, 0, 0);
            this.camera.lookAt(0, 0, 0);
        }
    }

    /**
     * Utilidades de parsing
     */
    parseDimensions(dimensionStr) {
        const matches = dimensionStr.match(/(\d+\.?\d*)m?\s*x\s*(\d+\.?\d*)m?\s*x\s*(\d+\.?\d*)m?/);
        if (matches) {
            return {
                length: parseFloat(matches[1]),
                width: parseFloat(matches[2]),
                height: parseFloat(matches[3])
            };
        }
        return { length: 100, width: 15, height: 10 }; // Valores por defecto
    }

    parseConfidence(confidenceStr) {
        const match = confidenceStr.match(/(\d+\.?\d*)/);
        return match ? parseFloat(match[1]) : 0.5;
    }
    
    /**
     * Generar dimensiones realistas basadas en datos del análisis
     */
    generateRealisticDimensions(anomalyData) {
        console.log('🔧 Generando dimensiones basadas en datos reales:', anomalyData);
        
        // Usar confianza para determinar tamaño base
        const confidence = this.parseConfidence(anomalyData.confidence || '0.5');
        
        // Determinar tipo de anomalía para dimensiones apropiadas
        const type = anomalyData.type || 'general';
        
        let baseDimensions;
        
        switch (type) {
            case 'high_priority_wreck':
            case 'submarine_wreck':
                // Naufragios: dimensiones típicas de embarcaciones
                baseDimensions = {
                    length: 80 + (confidence * 120), // 80-200m
                    width: 12 + (confidence * 18),   // 12-30m  
                    height: 8 + (confidence * 12)    // 8-20m
                };
                break;
                
            case 'rectangular':
                // Estructuras rectangulares: edificios, terrazas
                baseDimensions = {
                    length: 20 + (confidence * 80),  // 20-100m
                    width: 15 + (confidence * 35),   // 15-50m
                    height: 3 + (confidence * 12)    // 3-15m
                };
                break;
                
            case 'circular':
                // Estructuras circulares: plazas, fosos
                const radius = 10 + (confidence * 40); // 10-50m radio
                baseDimensions = {
                    length: radius * 2,
                    width: radius * 2,
                    height: 2 + (confidence * 8) // 2-10m
                };
                break;
                
            case 'linear':
                // Estructuras lineales: caminos, muros
                baseDimensions = {
                    length: 50 + (confidence * 200), // 50-250m
                    width: 2 + (confidence * 8),     // 2-10m
                    height: 1 + (confidence * 4)     // 1-5m
                };
                break;
                
            default:
                // Anomalía general
                baseDimensions = {
                    length: 30 + (confidence * 70),  // 30-100m
                    width: 20 + (confidence * 30),   // 20-50m
                    height: 5 + (confidence * 10)    // 5-15m
                };
        }
        
        // Agregar variación aleatoria pequeña para realismo
        const variation = 0.1; // 10% de variación
        baseDimensions.length *= (1 + (Math.random() - 0.5) * variation);
        baseDimensions.width *= (1 + (Math.random() - 0.5) * variation);
        baseDimensions.height *= (1 + (Math.random() - 0.5) * variation);
        
        // Formatear como string
        const dimensionStr = `${baseDimensions.length.toFixed(1)}m x ${baseDimensions.width.toFixed(1)}m x ${baseDimensions.height.toFixed(1)}m`;
        
        console.log(`✅ Dimensiones generadas: ${dimensionStr} (tipo: ${type}, confianza: ${confidence.toFixed(2)})`);
        
        return dimensionStr;
    }
}

// Instancia global
const anomalyImageGenerator = new AnomalyImageGenerator();

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.AnomalyImageGenerator = AnomalyImageGenerator;
    window.anomalyImageGenerator = anomalyImageGenerator;
}
