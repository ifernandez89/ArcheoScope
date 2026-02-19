/**
 * Tests para biome-detector
 * Testea: Detección de biomas, helpers, casos edge
 */

import { describe, it, expect } from 'vitest'
import { 
  detectBiome, 
  isIcyRegion, 
  getSkyColorForBiome, 
  getFogColorForBiome,
  type BiomeType 
} from './biome-detector'

describe('BiomeDetector - Regiones polares', () => {
  it('debe detectar Ártico (lat > 66.5)', () => {
    const biome = detectBiome(70, 0)
    expect(biome.type).toBe('ice')
    expect(biome.name).toBe('Ártico')
    expect(biome.temperature).toBe(-30)
  })

  it('debe detectar Antártico (lat < -66.5)', () => {
    const biome = detectBiome(-70, 0)
    expect(biome.type).toBe('ice')
    expect(biome.name).toBe('Antártico')
    expect(biome.temperature).toBe(-30)
  })

  it('debe detectar límite exacto polar (66.5)', () => {
    const biomeJustAbove = detectBiome(66.6, 0)
    const biomeJustBelow = detectBiome(66.4, 0)
    
    expect(biomeJustAbove.type).toBe('ice')
    expect(biomeJustBelow.type).not.toBe('ice')
  })
})

describe('BiomeDetector - Regiones glaciares específicas', () => {
  it('debe detectar Groenlandia', () => {
    const biome = detectBiome(65, -40)
    expect(biome.type).toBe('ice')
    expect(biome.name).toBe('Groenlandia')
    expect(biome.temperature).toBe(-20)
  })

  it('debe detectar Islandia', () => {
    // Islandia: lat entre 63-67, lon entre -25 y -13
    // Groenlandia: lat > 60, lon entre -73 y -12
    // Usar coordenadas que NO caigan en Groenlandia (lon < -12 para Groenlandia)
    // Islandia termina en -13, así que usar -15 para estar seguro en Islandia
    const biome = detectBiome(64.5, -18)
    expect(biome.type).toBe('ice')
    expect(biome.name).toBe('Islandia')
    expect(biome.temperature).toBe(-5)
  })

  it('debe detectar Patagonia Glaciar', () => {
    const biome = detectBiome(-50, -70)
    expect(biome.type).toBe('ice')
    expect(biome.name).toBe('Patagonia Glaciar')
    expect(biome.temperature).toBe(0)
  })

  it('debe detectar Himalaya', () => {
    const biome = detectBiome(30, 85)
    expect(biome.type).toBe('ice')
    expect(biome.name).toBe('Himalaya')
    expect(biome.temperature).toBe(-10)
  })

  it('debe detectar Alaska Glaciar', () => {
    const biome = detectBiome(60, -150)
    expect(biome.type).toBe('ice')
    expect(biome.name).toBe('Alaska Glaciar')
    expect(biome.temperature).toBe(-15)
  })
})

describe('BiomeDetector - Regiones volcánicas', () => {
  it('debe detectar Hawái', () => {
    const biome = detectBiome(20, -157)
    expect(biome.type).toBe('volcanic')
    expect(biome.name).toBe('Hawái')
    expect(biome.temperature).toBe(25)
  })

  it('debe detectar Andes Volcánicos', () => {
    // Andes: lat < -15 y lat > -45, lon > -80 y lon < -65
    // Atacama: lat > -27 y lat < -18, lon > -71 y lon < -68
    // Usar coordenadas fuera del rango de Atacama
    const biome = detectBiome(-30, -70)
    expect(biome.type).toBe('volcanic')
    expect(biome.name).toBe('Andes Volcánicos')
  })

  it('NO debe detectar Machu Picchu como volcánico', () => {
    // Machu Picchu: -13.16, -72.54
    const biome = detectBiome(-13.16, -72.54)
    expect(biome.type).not.toBe('volcanic')
  })

  it('debe detectar Arco Volcánico Japonés', () => {
    const biome = detectBiome(35, 138)
    expect(biome.type).toBe('volcanic')
    expect(biome.name).toBe('Arco Volcánico Japonés')
    expect(biome.temperature).toBe(18)
  })
})

describe('BiomeDetector - Regiones desérticas', () => {
  it('debe detectar Sahara', () => {
    const biome = detectBiome(25, 10)
    expect(biome.type).toBe('desert')
    expect(biome.name).toBe('Sahara')
    expect(biome.temperature).toBe(35)
    expect(biome.humidity).toBe(10)
  })

  it('debe detectar Atacama', () => {
    // Atacama: lat entre -27 y -18, lon entre -71 y -68
    const biome = detectBiome(-22, -69.5)
    expect(biome.type).toBe('desert')
    expect(biome.name).toBe('Atacama')
    expect(biome.temperature).toBe(20)
    expect(biome.humidity).toBe(5)
  })
})

describe('BiomeDetector - Océano', () => {
  it('debe detectar Océano Pacífico', () => {
    const biome = detectBiome(0, 170)
    expect(biome.type).toBe('ocean')
    expect(biome.name).toBe('Océano Pacífico')
    expect(biome.humidity).toBe(100)
  })

  it('debe detectar océano en coordenadas extremas', () => {
    const biome = detectBiome(-10, -170)
    expect(biome.type).toBe('ocean')
  })
})

describe('BiomeDetector - Terreno por defecto', () => {
  it('debe retornar default para coordenadas genéricas', () => {
    const biome = detectBiome(40, -100)
    expect(biome.type).toBe('default')
    expect(biome.name).toBe('Terreno Genérico')
  })

  it('debe retornar default para Europa central', () => {
    const biome = detectBiome(50, 10)
    expect(biome.type).toBe('default')
  })
})

describe('BiomeDetector - Helper isIcyRegion', () => {
  it('debe retornar true para regiones heladas', () => {
    expect(isIcyRegion(70, 0)).toBe(true) // Ártico
    expect(isIcyRegion(-70, 0)).toBe(true) // Antártico
    expect(isIcyRegion(65, -40)).toBe(true) // Groenlandia
    expect(isIcyRegion(30, 85)).toBe(true) // Himalaya
  })

  it('debe retornar false para regiones no heladas', () => {
    expect(isIcyRegion(25, 10)).toBe(false) // Sahara
    expect(isIcyRegion(20, -157)).toBe(false) // Hawái
    expect(isIcyRegion(0, 0)).toBe(false) // Ecuador
  })
})

describe('BiomeDetector - Helper getSkyColorForBiome', () => {
  it('debe retornar colores correctos para día', () => {
    expect(getSkyColorForBiome('ice', true)).toBe('#b8d4e8')
    expect(getSkyColorForBiome('volcanic', true)).toBe('#d4a574')
    expect(getSkyColorForBiome('desert', true)).toBe('#e8d4b8')
    expect(getSkyColorForBiome('ocean', true)).toBe('#4a90e2')
    expect(getSkyColorForBiome('forest', true)).toBe('#87ceeb')
    expect(getSkyColorForBiome('default', true)).toBe('#87ceeb')
  })

  it('debe retornar color oscuro para noche en todos los biomas', () => {
    const nightColor = '#0a0a1a'
    
    expect(getSkyColorForBiome('ice', false)).toBe(nightColor)
    expect(getSkyColorForBiome('volcanic', false)).toBe(nightColor)
    expect(getSkyColorForBiome('desert', false)).toBe(nightColor)
    expect(getSkyColorForBiome('ocean', false)).toBe(nightColor)
    expect(getSkyColorForBiome('default', false)).toBe(nightColor)
  })
})

describe('BiomeDetector - Helper getFogColorForBiome', () => {
  it('debe retornar colores de niebla correctos', () => {
    expect(getFogColorForBiome('ice')).toBe('#d0e8f2')
    expect(getFogColorForBiome('volcanic')).toBe('#8b7355')
    expect(getFogColorForBiome('desert')).toBe('#f4e4c1')
    expect(getFogColorForBiome('ocean')).toBe('#7fb3d5')
    expect(getFogColorForBiome('default')).toBe('#87ceeb')
  })
})

describe('BiomeDetector - Casos edge', () => {
  it('debe manejar coordenadas en límites de longitud', () => {
    const biome180 = detectBiome(0, 180)
    const biomeNeg180 = detectBiome(0, -180)
    
    expect(biome180.type).toBeDefined()
    expect(biomeNeg180.type).toBeDefined()
  })

  it('debe manejar coordenadas en ecuador', () => {
    const biome = detectBiome(0, 0)
    expect(biome.type).toBeDefined()
  })

  it('debe manejar coordenadas en polos exactos', () => {
    const northPole = detectBiome(90, 0)
    const southPole = detectBiome(-90, 0)
    
    expect(northPole.type).toBe('ice')
    expect(southPole.type).toBe('ice')
  })

  it('debe retornar propiedades válidas para todos los biomas', () => {
    const testCoords = [
      [70, 0], [-70, 0], [25, 10], [20, -157], [0, 170], [40, -100]
    ]
    
    testCoords.forEach(([lat, lon]) => {
      const biome = detectBiome(lat, lon)
      
      expect(biome.type).toBeDefined()
      expect(biome.name).toBeDefined()
      expect(biome.description).toBeDefined()
      expect(typeof biome.temperature).toBe('number')
      expect(typeof biome.humidity).toBe('number')
      expect(biome.humidity).toBeGreaterThanOrEqual(0)
      expect(biome.humidity).toBeLessThanOrEqual(100)
    })
  })
})
