/**
 * Cliente Frontend para HRM-World Engine
 * 
 * Ejemplo de integración con Three.js
 */

// ============================================================================
// TIPOS
// ============================================================================

interface WorldState {
    player_position: [number, number, number];
    player_velocity: [number, number, number];
    climate_state: {
        temperature: number;
        humidity: number;
        pressure: number;
    };
    biome_type: string;
    time_of_day: number;
    active_npcs: any[];
    active_anomalies: any[];
    terrain_elevation: number;
    weather_intensity: number;
    player_zone: number;
}

interface WorldEvent {
    type: string;
    severity: string;
    intensity: number;
    confidence: number;
    affected_zones: number[];
    affected_regions: string[];
    duration: number;
    effects: EventEffect[];
}

interface EventEffect {
    type: string;  // 'climate', 'visual', 'audio', 'physics'
    parameter: string;
    value: number;
    duration: number;
}

interface WorldUpdateResponse {
    event: WorldEvent;
    narrative: string;
    analysis: {
        instability: number;
        confidence: number;
        affected_zones: number;
        world_shift: string;
    };
    metrics: {
        entropy: number;
        anomaly_score: number;
        player_disruption: number;
    };
    processing_time: number;
}

// ============================================================================
// CLIENTE API REST
// ============================================================================

class WorldEngineClient {
    private baseUrl: string;
    private ws: WebSocket | null = null;
    private eventCallbacks: ((data: any) => void)[] = [];

    constructor(baseUrl: string = 'http://localhost:8003') {
        this.baseUrl = baseUrl;
    }

    /**
     * Actualizar estado del mundo
     */
    async updateWorld(state: WorldState): Promise<WorldUpdateResponse> {
        const response = await fetch(`${this.baseUrl}/world/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(state),
        });

        if (!response.ok) {
            throw new Error(`Error updating world: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Inyectar acción del jugador
     */
    async injectPlayerAction(intensity: number, zone: number = 32): Promise<any> {
        const response = await fetch(`${this.baseUrl}/world/action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action_intensity: intensity,
                player_zone: zone,
            }),
        });

        if (!response.ok) {
            throw new Error(`Error injecting action: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Obtener estado del mundo
     */
    async getWorldStatus(): Promise<any> {
        const response = await fetch(`${this.baseUrl}/world/status`);

        if (!response.ok) {
            throw new Error(`Error getting status: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Obtener historial de eventos
     */
    async getEventHistory(limit: number = 10): Promise<any[]> {
        const response = await fetch(`${this.baseUrl}/world/history?limit=${limit}`);

        if (!response.ok) {
            throw new Error(`Error getting history: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Obtener estadísticas
     */
    async getStatistics(): Promise<any> {
        const response = await fetch(`${this.baseUrl}/world/statistics`);

        if (!response.ok) {
            throw new Error(`Error getting statistics: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Configurar motor
     */
    async configure(config: {
        hrm_cycles?: number;
        enable_propagation?: boolean;
        propagation_steps?: number;
        enable_cascade?: boolean;
    }): Promise<any> {
        const response = await fetch(`${this.baseUrl}/world/configure`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config),
        });

        if (!response.ok) {
            throw new Error(`Error configuring: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Conectar WebSocket para eventos en tiempo real
     */
    connectWebSocket(onEvent: (data: any) => void): void {
        const wsUrl = this.baseUrl.replace('http', 'ws') + '/world/ws';
        
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('✅ WebSocket conectado');
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'event') {
                // Evento del mundo
                onEvent(data.data);
                
                // Notificar callbacks
                this.eventCallbacks.forEach(cb => cb(data.data));
            } else if (data.type === 'status') {
                console.log('Estado inicial:', data.data);
            }
        };

        this.ws.onerror = (error) => {
            console.error('❌ WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('⚠️ WebSocket cerrado');
        };
    }

    /**
     * Agregar callback para eventos
     */
    onEvent(callback: (data: any) => void): void {
        this.eventCallbacks.push(callback);
    }

    /**
     * Desconectar WebSocket
     */
    disconnectWebSocket(): void {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
}

// ============================================================================
// INTEGRACIÓN CON THREE.JS
// ============================================================================

class WorldEffectsManager {
    private scene: any; // THREE.Scene
    private camera: any; // THREE.Camera
    private activeEffects: Map<string, any> = new Map();

    constructor(scene: any, camera: any) {
        this.scene = scene;
        this.camera = camera;
    }

    /**
     * Aplicar efectos de un evento
     */
    applyEventEffects(event: WorldEvent): void {
        console.log(`Aplicando efectos de evento: ${event.type}`);

        event.effects.forEach(effect => {
            switch (effect.type) {
                case 'climate':
                    this.applyClimateEffect(effect);
                    break;
                case 'visual':
                    this.applyVisualEffect(effect);
                    break;
                case 'audio':
                    this.applyAudioEffect(effect);
                    break;
                case 'physics':
                    this.applyPhysicsEffect(effect);
                    break;
            }
        });

        // Programar limpieza después de la duración
        setTimeout(() => {
            this.clearEventEffects(event);
        }, event.duration * 1000);
    }

    private applyClimateEffect(effect: EventEffect): void {
        console.log(`Clima: ${effect.parameter} = ${effect.value}`);
        
        // Ejemplo: Modificar fog según intensidad de tormenta
        if (effect.parameter === 'storm_intensity') {
            // this.scene.fog.density = effect.value * 0.01;
        }
    }

    private applyVisualEffect(effect: EventEffect): void {
        console.log(`Visual: ${effect.parameter} = ${effect.value}`);
        
        // Ejemplo: Rayos
        if (effect.parameter === 'lightning_frequency') {
            this.startLightningEffect(effect.value);
        }
        
        // Ejemplo: Oscurecer cielo
        if (effect.parameter === 'sky_darkness') {
            // Modificar intensidad de luz ambiental
            // this.scene.ambientLight.intensity = 1.0 - effect.value;
        }
    }

    private applyAudioEffect(effect: EventEffect): void {
        console.log(`Audio: ${effect.parameter} = ${effect.value}`);
        
        // Ejemplo: Truenos
        if (effect.parameter === 'thunder_volume') {
            // Reproducir sonido de trueno con volumen
            // this.audioManager.play('thunder', effect.value);
        }
    }

    private applyPhysicsEffect(effect: EventEffect): void {
        console.log(`Física: ${effect.parameter} = ${effect.value}`);
        
        // Ejemplo: Fluctuación de gravedad
        if (effect.parameter === 'gravity_fluctuation') {
            // Modificar gravedad del mundo
            // this.physicsWorld.gravity.y = -9.8 * (1.0 + effect.value);
        }
    }

    private startLightningEffect(frequency: number): void {
        // Crear efecto de rayos
        const interval = 1000 / frequency; // ms entre rayos
        
        const lightningInterval = setInterval(() => {
            // Flash de luz
            // const flash = new THREE.PointLight(0xffffff, 10, 100);
            // this.scene.add(flash);
            
            setTimeout(() => {
                // this.scene.remove(flash);
            }, 100);
        }, interval);

        this.activeEffects.set('lightning', lightningInterval);
    }

    private clearEventEffects(event: WorldEvent): void {
        console.log(`Limpiando efectos de evento: ${event.type}`);
        
        // Limpiar efectos activos
        this.activeEffects.forEach((effect, key) => {
            if (typeof effect === 'number') {
                clearInterval(effect);
            }
        });
        
        this.activeEffects.clear();
    }
}

// ============================================================================
// EJEMPLO DE USO
// ============================================================================

async function main() {
    // Inicializar cliente
    const client = new WorldEngineClient('http://localhost:8003');

    // Conectar WebSocket
    client.connectWebSocket((eventData) => {
        console.log('🌍 Nuevo evento del mundo:', eventData);
        
        // Aplicar efectos visuales
        // effectsManager.applyEventEffects(eventData.event);
        
        // Mostrar narrativa
        console.log('📖 Narrativa:', eventData.narrative);
    });

    // Crear estado del mundo desde Three.js
    const worldState: WorldState = {
        player_position: [0, 0, 0],
        player_velocity: [1, 0, 1],
        climate_state: {
            temperature: 0.5,
            humidity: 0.6,
            pressure: 0.7,
        },
        biome_type: 'desert',
        time_of_day: 14.5,
        active_npcs: [],
        active_anomalies: [],
        terrain_elevation: 100.0,
        weather_intensity: 0.3,
        player_zone: 32,
    };

    // Actualizar mundo cada 5 segundos
    setInterval(async () => {
        try {
            const result = await client.updateWorld(worldState);
            
            console.log('Evento:', result.event.type);
            console.log('Narrativa:', result.narrative);
            console.log('Inestabilidad:', result.analysis.instability);
            
            // Aplicar efectos
            // effectsManager.applyEventEffects(result.event);
            
        } catch (error) {
            console.error('Error actualizando mundo:', error);
        }
    }, 5000);

    // Inyectar acción del jugador cuando interactúa
    document.addEventListener('keydown', async (event) => {
        if (event.key === 'e') {
            // Acción intensa
            try {
                const result = await client.injectPlayerAction(0.8, 32);
                console.log('Impacto de acción:', result);
            } catch (error) {
                console.error('Error inyectando acción:', error);
            }
        }
    });

    // Obtener estadísticas cada 30 segundos
    setInterval(async () => {
        try {
            const stats = await client.getStatistics();
            console.log('📊 Estadísticas:', stats);
        } catch (error) {
            console.error('Error obteniendo estadísticas:', error);
        }
    }, 30000);
}

// Exportar para uso en módulos
export { WorldEngineClient, WorldEffectsManager, WorldState, WorldEvent };

// Ejecutar si es script standalone
if (typeof window !== 'undefined') {
    // main();
}
