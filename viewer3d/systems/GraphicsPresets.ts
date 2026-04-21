/**
 * GraphicsPresets - Presets de calidad gráfica
 * 
 * CRÍTICO: Medir antes de optimizar
 * Si LOW es fluido y HIGH no → problema en pipeline gráfico
 */

import { loggers } from '@/core/Logger'

export type QualityPreset = 'LOW' | 'MEDIUM' | 'HIGH' | 'ULTRA'

export interface GraphicsConfig {
  // Shadows
  shadows: boolean
  shadowMapSize: number
  shadowCascades: number
  
  // Post-processing
  bloom: boolean
  ssao: boolean
  ssr: boolean
  dof: boolean
  motionBlur: boolean
  volumetrics: boolean
  
  // Rendering
  antialias: boolean
  pixelRatio: number
  maxLights: number
  
  // LOD
  lodBias: number
  maxDrawDistance: number
  
  // Instancing
  maxInstancesPerMesh: number
  
  // Culling
  frustumCulling: boolean
  occlusionCulling: boolean
}

export const GRAPHICS_PRESETS: Record<QualityPreset, GraphicsConfig> = {
  LOW: {
    // Shadows
    shadows: false,
    shadowMapSize: 512,
    shadowCascades: 1,
    
    // Post-processing (TODO DESACTIVADO)
    bloom: false,
    ssao: false,
    ssr: false,
    dof: false,
    motionBlur: false,
    volumetrics: false,
    
    // Rendering
    antialias: false,
    pixelRatio: 0.75,
    maxLights: 2,
    
    // LOD
    lodBias: 2.0, // Más agresivo
    maxDrawDistance: 1000,
    
    // Instancing
    maxInstancesPerMesh: 5000,
    
    // Culling
    frustumCulling: true,
    occlusionCulling: false
  },
  
  MEDIUM: {
    // Shadows
    shadows: true,
    shadowMapSize: 1024,
    shadowCascades: 2,
    
    // Post-processing (MÍNIMO)
    bloom: false,
    ssao: false,
    ssr: false,
    dof: false,
    motionBlur: false,
    volumetrics: false,
    
    // Rendering
    antialias: true,
    pixelRatio: 1.0,
    maxLights: 4,
    
    // LOD
    lodBias: 1.5,
    maxDrawDistance: 2000,
    
    // Instancing
    maxInstancesPerMesh: 10000,
    
    // Culling
    frustumCulling: true,
    occlusionCulling: false
  },
  
  HIGH: {
    // Shadows
    shadows: true,
    shadowMapSize: 2048,
    shadowCascades: 3,
    
    // Post-processing (SELECTIVO)
    bloom: true,
    ssao: true,
    ssr: false,
    dof: false,
    motionBlur: false,
    volumetrics: false,
    
    // Rendering
    antialias: true,
    pixelRatio: 1.0,
    maxLights: 8,
    
    // LOD
    lodBias: 1.0,
    maxDrawDistance: 3000,
    
    // Instancing
    maxInstancesPerMesh: 15000,
    
    // Culling
    frustumCulling: true,
    occlusionCulling: true
  },
  
  ULTRA: {
    // Shadows
    shadows: true,
    shadowMapSize: 4096,
    shadowCascades: 4,
    
    // Post-processing (TODO)
    bloom: true,
    ssao: true,
    ssr: true,
    dof: true,
    motionBlur: true,
    volumetrics: true,
    
    // Rendering
    antialias: true,
    pixelRatio: 1.0, // Se sobreescribe en cliente con window.devicePixelRatio
    maxLights: 16,
    
    // LOD
    lodBias: 0.5,
    maxDrawDistance: 5000,
    
    // Instancing
    maxInstancesPerMesh: 20000,
    
    // Culling
    frustumCulling: true,
    occlusionCulling: true
  }
}

export class GraphicsPresetManager {
  private static instance: GraphicsPresetManager
  private currentPreset: QualityPreset = 'MEDIUM'
  private config: GraphicsConfig = GRAPHICS_PRESETS.MEDIUM
  
  private constructor() {
    loggers.performance.info('GraphicsPresetManager inicializado')
    this.detectOptimalPreset()
  }
  
  static getInstance(): GraphicsPresetManager {
    if (!GraphicsPresetManager.instance) {
      GraphicsPresetManager.instance = new GraphicsPresetManager()
    }
    return GraphicsPresetManager.instance
  }
  
  /**
   * Detectar preset óptimo según hardware
   */
  private detectOptimalPreset(): void {
    try {
      // Detectar GPU
      const canvas = document.createElement('canvas')
      const gl = canvas.getContext('webgl2') || canvas.getContext('webgl')
      
      if (!gl) {
        this.setPreset('MEDIUM')
        return
      }
      
      const debugInfo = gl.getExtension('WEBGL_debug_renderer_info')
      const renderer = debugInfo
        ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
        : 'Unknown'
      
      loggers.performance.info('GPU detectada:', renderer)
      
      // Heurística simple
      const rendererStr = String(renderer).toLowerCase()
      if (rendererStr.includes('intel')) {
        this.setPreset('LOW')
      } else if (rendererStr.includes('gtx') || rendererStr.includes('rtx') || rendererStr.includes('nvidia')) {
        this.setPreset('HIGH')
      } else if (rendererStr.includes('amd') || rendererStr.includes('radeon')) {
        this.setPreset('MEDIUM')
      } else {
        this.setPreset('MEDIUM')
      }
    } catch (error) {
      loggers.performance.warn('No se pudo detectar GPU, usando preset MEDIUM')
      this.setPreset('MEDIUM')
    }
  }
  
  /**
   * Establecer preset
   */
  setPreset(preset: QualityPreset): void {
    this.currentPreset = preset
    this.config = GRAPHICS_PRESETS[preset]
    
    loggers.performance.info(`Graphics preset: ${preset}`, this.config)
  }
  
  /**
   * Obtener preset actual
   */
  getPreset(): QualityPreset {
    return this.currentPreset
  }
  
  /**
   * Obtener configuración
   */
  getConfig(): GraphicsConfig {
    return { ...this.config }
  }
  
  /**
   * Configuración custom
   */
  setCustomConfig(config: Partial<GraphicsConfig>): void {
    this.config = { ...this.config, ...config }
    loggers.performance.info('Custom config aplicada')
  }
}

export default GraphicsPresetManager.getInstance()
