/**
 * Tests para ArcheoEngine
 * Testea: Singleton, búsqueda de sitios, cálculo de distancias, caché
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { ArcheoEngine } from './ArcheoEngine'

// Mock del JSON de sitios
vi.mock('../data/archaeological-sites.json', () => ({
  default: {
    sites: [
      {
        id: 'machu-picchu',
        name: 'Machu Picchu',
        lat: -13.163,
        lon: -72.545,
        model: 'machu-picchu.glb',
        description: 'Ciudadela inca',
        period: 'Siglo XV',
        culture: 'Inca'
      },
      {
        id: 'giza',
        name: 'Pirámides de Giza',
        lat: 29.979,
        lon: 31.134,
        model: 'giza.glb',
        description: 'Pirámides egipcias',
        period: 'c. 2580-2560 a.C.',
        culture: 'Egipcia'
      },
      {
        id: 'stonehenge',
        name: 'Stonehenge',
        lat: 51.179,
        lon: -1.826,
        model: 'stonehenge.glb',
        description: 'Monumento megalítico',
        period: 'c. 3000-2000 a.C.',
        culture: 'Neolítica'
      },
      {
        id: 'chichen-itza',
        name: 'Chichén Itzá',
        lat: 20.683,
        lon: -88.568,
        model: 'chichen-itza.glb',
        description: 'Ciudad maya',
        period: 'c. 600-1200 d.C.',
        culture: 'Maya'
      }
    ]
  }
}))

describe('ArcheoEngine - Singleton', () => {
  it('debe retornar la misma instancia', () => {
    const instance1 = ArcheoEngine.getInstance()
    const instance2 = ArcheoEngine.getInstance()
    
    expect(instance1).toBe(instance2)
  })

  it('debe cargar sitios al inicializar', () => {
    const engine = ArcheoEngine.getInstance()
    const sites = engine.getAllSites()
    
    expect(sites.length).toBeGreaterThan(0)
  })
})

describe('ArcheoEngine - getAllSites', () => {
  it('debe retornar todos los sitios', () => {
    const engine = ArcheoEngine.getInstance()
    const sites = engine.getAllSites()
    
    expect(Array.isArray(sites)).toBe(true)
    expect(sites.length).toBe(4)
  })

  it('debe retornar sitios con estructura correcta', () => {
    const engine = ArcheoEngine.getInstance()
    const sites = engine.getAllSites()
    
    sites.forEach(site => {
      expect(site).toHaveProperty('id')
      expect(site).toHaveProperty('name')
      expect(site).toHaveProperty('lat')
      expect(site).toHaveProperty('lon')
      expect(site).toHaveProperty('model')
      expect(site).toHaveProperty('description')
      expect(site).toHaveProperty('period')
      expect(site).toHaveProperty('culture')
    })
  })
})

describe('ArcheoEngine - getSiteById', () => {
  it('debe encontrar sitio por ID válido', () => {
    const engine = ArcheoEngine.getInstance()
    
    const machuPicchu = engine.getSiteById('machu-picchu')
    expect(machuPicchu).toBeDefined()
    expect(machuPicchu?.name).toBe('Machu Picchu')
    expect(machuPicchu?.culture).toBe('Inca')
  })

  it('debe retornar undefined para ID inválido', () => {
    const engine = ArcheoEngine.getInstance()
    
    const notFound = engine.getSiteById('atlantis')
    expect(notFound).toBeUndefined()
  })

  it('debe encontrar todos los sitios mock por ID', () => {
    const engine = ArcheoEngine.getInstance()
    
    expect(engine.getSiteById('machu-picchu')).toBeDefined()
    expect(engine.getSiteById('giza')).toBeDefined()
    expect(engine.getSiteById('stonehenge')).toBeDefined()
    expect(engine.getSiteById('chichen-itza')).toBeDefined()
  })
})

describe('ArcheoEngine - getNearestSites', () => {
  it('debe encontrar sitios cercanos a Machu Picchu', () => {
    const engine = ArcheoEngine.getInstance()
    
    // Coordenadas cerca de Machu Picchu
    const nearest = engine.getNearestSites(-13.0, -72.0, 100)
    
    expect(nearest.length).toBeGreaterThan(0)
    expect(nearest[0].id).toBe('machu-picchu')
  })

  it('debe ordenar sitios por distancia', () => {
    const engine = ArcheoEngine.getInstance()
    
    // Desde un punto central
    const nearest = engine.getNearestSites(0, 0, 20000)
    
    // Verificar que están ordenados (cada uno más lejos que el anterior)
    for (let i = 1; i < nearest.length; i++) {
      const dist1 = calculateTestDistance(0, 0, nearest[i-1].lat, nearest[i-1].lon)
      const dist2 = calculateTestDistance(0, 0, nearest[i].lat, nearest[i].lon)
      expect(dist2).toBeGreaterThanOrEqual(dist1)
    }
  })

  it('debe respetar maxDistance', () => {
    const engine = ArcheoEngine.getInstance()
    
    // Buscar con distancia muy pequeña
    const nearest = engine.getNearestSites(0, 0, 10)
    
    // No debería encontrar ningún sitio (todos están lejos)
    expect(nearest.length).toBe(0)
  })

  it('debe retornar array vacío si no hay sitios cercanos', () => {
    const engine = ArcheoEngine.getInstance()
    
    // Coordenadas en medio del océano Pacífico
    const nearest = engine.getNearestSites(0, -170, 100)
    
    expect(Array.isArray(nearest)).toBe(true)
    expect(nearest.length).toBe(0)
  })

  it('debe usar maxDistance por defecto de 1000km', () => {
    const engine = ArcheoEngine.getInstance()
    
    // Sin especificar maxDistance
    const nearest = engine.getNearestSites(-13.0, -72.0)
    
    expect(Array.isArray(nearest)).toBe(true)
  })
})

describe('ArcheoEngine - getModelForSite', () => {
  it('debe retornar el path del modelo', () => {
    const engine = ArcheoEngine.getInstance()
    const site = engine.getSiteById('machu-picchu')!
    
    const modelPath = engine.getModelForSite(site)
    expect(modelPath).toBe('machu-picchu.glb')
  })

  it('debe retornar modelos correctos para todos los sitios', () => {
    const engine = ArcheoEngine.getInstance()
    
    const machuPicchu = engine.getSiteById('machu-picchu')!
    const giza = engine.getSiteById('giza')!
    
    expect(engine.getModelForSite(machuPicchu)).toBe('machu-picchu.glb')
    expect(engine.getModelForSite(giza)).toBe('giza.glb')
  })
})

describe('ArcheoEngine - Caché de modelos', () => {
  let engine: ArcheoEngine

  beforeEach(() => {
    engine = ArcheoEngine.getInstance()
  })

  it('debe cachear un modelo', () => {
    const mockModel = { geometry: {}, material: {} }
    
    engine.cacheModel('test.glb', mockModel)
    const cached = engine.getCachedModel('test.glb')
    
    expect(cached).toBe(mockModel)
  })

  it('debe retornar undefined para modelo no cacheado', () => {
    const cached = engine.getCachedModel('not-cached.glb')
    expect(cached).toBeUndefined()
  })

  it('debe sobrescribir modelo cacheado', () => {
    const model1 = { id: 1 }
    const model2 = { id: 2 }
    
    engine.cacheModel('test.glb', model1)
    engine.cacheModel('test.glb', model2)
    
    const cached = engine.getCachedModel('test.glb')
    expect(cached).toBe(model2)
  })

  it('debe mantener múltiples modelos en caché', () => {
    const model1 = { id: 1 }
    const model2 = { id: 2 }
    
    engine.cacheModel('model1.glb', model1)
    engine.cacheModel('model2.glb', model2)
    
    expect(engine.getCachedModel('model1.glb')).toBe(model1)
    expect(engine.getCachedModel('model2.glb')).toBe(model2)
  })
})

describe('ArcheoEngine - getSitesByCulture', () => {
  it('debe encontrar sitios por cultura exacta', () => {
    const engine = ArcheoEngine.getInstance()
    
    const incaSites = engine.getSitesByCulture('Inca')
    expect(incaSites.length).toBe(1)
    expect(incaSites[0].id).toBe('machu-picchu')
  })

  it('debe ser case-insensitive', () => {
    const engine = ArcheoEngine.getInstance()
    
    const incaSites1 = engine.getSitesByCulture('inca')
    const incaSites2 = engine.getSitesByCulture('INCA')
    
    expect(incaSites1.length).toBe(1)
    expect(incaSites2.length).toBe(1)
  })

  it('debe encontrar por substring', () => {
    const engine = ArcheoEngine.getInstance()
    
    const sites = engine.getSitesByCulture('inc')
    expect(sites.length).toBeGreaterThan(0)
  })

  it('debe retornar array vacío si no encuentra', () => {
    const engine = ArcheoEngine.getInstance()
    
    const sites = engine.getSitesByCulture('Atlantis')
    expect(sites.length).toBe(0)
  })
})

describe('ArcheoEngine - getSitesByPeriod', () => {
  it('debe encontrar sitios por período', () => {
    const engine = ArcheoEngine.getInstance()
    
    const sites = engine.getSitesByPeriod('Siglo XV')
    expect(sites.length).toBe(1)
    expect(sites[0].id).toBe('machu-picchu')
  })

  it('debe ser case-insensitive', () => {
    const engine = ArcheoEngine.getInstance()
    
    const sites1 = engine.getSitesByPeriod('siglo xv')
    const sites2 = engine.getSitesByPeriod('SIGLO XV')
    
    expect(sites1.length).toBe(1)
    expect(sites2.length).toBe(1)
  })

  it('debe encontrar por substring', () => {
    const engine = ArcheoEngine.getInstance()
    
    const sites = engine.getSitesByPeriod('a.C.')
    expect(sites.length).toBeGreaterThan(0)
  })

  it('debe retornar array vacío si no encuentra', () => {
    const engine = ArcheoEngine.getInstance()
    
    const sites = engine.getSitesByPeriod('Futuro')
    expect(sites.length).toBe(0)
  })
})

describe('ArcheoEngine - Cálculo de distancias (Haversine)', () => {
  it('debe calcular distancia 0 para mismo punto', () => {
    const engine = ArcheoEngine.getInstance()
    
    const sites = engine.getNearestSites(-13.163, -72.545, 1)
    expect(sites.length).toBeGreaterThan(0)
    expect(sites[0].id).toBe('machu-picchu')
  })

  it('debe calcular distancias razonables', () => {
    const engine = ArcheoEngine.getInstance()
    
    // Machu Picchu a Giza debería ser > 10,000 km
    const nearest = engine.getNearestSites(-13.163, -72.545, 20000)
    
    // Machu Picchu debe estar primero (distancia 0)
    expect(nearest[0].id).toBe('machu-picchu')
  })
})

// Helper para tests
function calculateTestDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2)
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  
  return R * c
}
