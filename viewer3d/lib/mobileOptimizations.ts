/**
 * Mobile Optimizations — Utilidades para optimizar rendimiento en móvil
 * 
 * Estas funciones detectan mobile y ajustan parámetros gráficos
 * para mantener FPS fluido sin sacrificar demasiada calidad visual.
 */

/**
 * Detectar si estamos en un dispositivo móvil
 */
export function isMobileDevice(): boolean {
  if (typeof window === 'undefined') return false
  return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
}

/**
 * Obtener segmentos óptimos para esferas según plataforma
 * - PC: 64 segmentos (alta calidad)
 * - Mobile: 24 segmentos (suficiente para pantallas pequeñas)
 */
export function getSphereSegments(quality: 'low' | 'medium' | 'high' = 'medium'): number {
  const isMobile = isMobileDevice()
  
  if (isMobile) {
    // Mobile: menos polígonos
    switch (quality) {
      case 'low': return 16
      case 'medium': return 24
      case 'high': return 32
    }
  } else {
    // PC: más polígonos
    switch (quality) {
      case 'low': return 32
      case 'medium': return 48
      case 'high': return 64
    }
  }
}

/**
 * Obtener pixelRatio óptimo para el dispositivo
 * - Mobile: máximo 1.3 (ahorra GPU significativamente)
 * - PC: devicePixelRatio completo o según preset
 */
export function getOptimalPixelRatio(presetRatio: number = 1.0): number {
  if (typeof window === 'undefined') return presetRatio
  
  const isMobile = isMobileDevice()
  
  if (isMobile) {
    // En mobile, limitar a 1.3 máximo
    return Math.min(window.devicePixelRatio, 1.3)
  }
  
  // En PC, usar el ratio del preset o devicePixelRatio
  return presetRatio === 1.0 ? window.devicePixelRatio : presetRatio
}

/**
 * Obtener cantidad de partículas según plataforma
 */
export function getParticleCount(baseCount: number): number {
  const isMobile = isMobileDevice()
  return isMobile ? Math.floor(baseCount * 0.4) : baseCount
}

/**
 * Obtener distancia de renderizado según plataforma
 */
export function getRenderDistance(baseDistance: number): number {
  const isMobile = isMobileDevice()
  return isMobile ? baseDistance * 0.6 : baseDistance
}

/**
 * Obtener configuración de sombras según plataforma
 */
export function getShadowConfig(): { enabled: boolean; mapSize: number } {
  const isMobile = isMobileDevice()
  
  if (isMobile) {
    return { enabled: false, mapSize: 512 }
  }
  
  return { enabled: true, mapSize: 2048 }
}
