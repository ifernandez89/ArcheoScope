// Biome Detector - Detecta el bioma basado en coordenadas geográficas

export type BiomeType = 'ice' | 'volcanic' | 'desert' | 'forest' | 'ocean' | 'default'

export interface BiomeInfo {
  type: BiomeType
  name: string
  description: string
  temperature: number // -50 a 50 °C
  humidity: number // 0 a 100%
}

export function detectBiome(lat: number, lon: number): BiomeInfo {
  const absLat = Math.abs(lat)
  
  // HIELO - Regiones polares y glaciares
  // Ártico (lat > 66.5) y Antártico (lat < -66.5)
  if (absLat > 66.5) {
    return {
      type: 'ice',
      name: lat > 0 ? 'Ártico' : 'Antártico',
      description: 'Región polar con hielo permanente',
      temperature: -30,
      humidity: 20
    }
  }
  
  // Islandia (lat entre 63-67, lon entre -25 y -13)
  // IMPORTANTE: Evaluar ANTES de Groenlandia porque está dentro de su rango
  if (lat > 63 && lat < 67 && lon > -25 && lon < -13) {
    return {
      type: 'ice',
      name: 'Islandia',
      description: 'Glaciares volcánicos',
      temperature: -5,
      humidity: 70
    }
  }
  
  // Groenlandia (lat > 60, lon entre -73 y -12)
  if (lat > 60 && lon > -73 && lon < -12) {
    return {
      type: 'ice',
      name: 'Groenlandia',
      description: 'Capa de hielo continental',
      temperature: -20,
      humidity: 30
    }
  }
  
  // Patagonia glaciar (lat < -45, lon entre -75 y -65)
  if (lat < -45 && lon > -75 && lon < -65) {
    return {
      type: 'ice',
      name: 'Patagonia Glaciar',
      description: 'Campos de hielo patagónicos',
      temperature: 0,
      humidity: 60
    }
  }
  
  // Himalaya y Tibet (lat entre 27-36, lon entre 75-105)
  if (lat > 27 && lat < 36 && lon > 75 && lon < 105) {
    return {
      type: 'ice',
      name: 'Himalaya',
      description: 'Glaciares de alta montaña',
      temperature: -10,
      humidity: 40
    }
  }
  
  // Alaska glaciar (lat > 58, lon entre -170 y -130)
  if (lat > 58 && lon > -170 && lon < -130) {
    return {
      type: 'ice',
      name: 'Alaska Glaciar',
      description: 'Glaciares alpinos',
      temperature: -15,
      humidity: 50
    }
  }
  
  // VOLCÁNICO - Zonas volcánicas activas
  // Islandia ya cubierta arriba como hielo
  
  // Hawái (lat entre 18-22, lon entre -161 y -154)
  if (lat > 18 && lat < 22 && lon > -161 && lon < -154) {
    return {
      type: 'volcanic',
      name: 'Hawái',
      description: 'Islas volcánicas activas',
      temperature: 25,
      humidity: 70
    }
  }
  
  // DESIERTO - Regiones áridas
  // Atacama (lat entre -27 y -18, lon entre -71 y -68)
  // IMPORTANTE: Evaluar ANTES de Andes Volcánicos porque está dentro de su rango
  if (lat > -27 && lat < -18 && lon > -71 && lon < -68) {
    return {
      type: 'desert',
      name: 'Atacama',
      description: 'Desierto más árido del mundo',
      temperature: 20,
      humidity: 5
    }
  }
  
  // Cinturón de Fuego del Pacífico - Andes (solo zonas muy volcánicas)
  // Excluir Machu Picchu y zonas arqueológicas
  if (lat < -15 && lat > -45 && lon > -80 && lon < -65) {
    // Excluir Machu Picchu (lat -13.16, lon -72.54)
    if (!(lat > -14 && lat < -12 && lon > -73 && lon < -71)) {
      return {
        type: 'volcanic',
        name: 'Andes Volcánicos',
        description: 'Cadena volcánica andina',
        temperature: 15,
        humidity: 50
      }
    }
  }
  
  // Japón (lat entre 30-46, lon entre 128-146)
  if (lat > 30 && lat < 46 && lon > 128 && lon < 146) {
    return {
      type: 'volcanic',
      name: 'Arco Volcánico Japonés',
      description: 'Islas volcánicas',
      temperature: 18,
      humidity: 65
    }
  }
  
  // DESIERTO - Regiones áridas
  // Sahara (lat entre 15-35, lon entre -15 y 40)
  if (lat > 15 && lat < 35 && lon > -15 && lon < 40) {
    return {
      type: 'desert',
      name: 'Sahara',
      description: 'Desierto cálido',
      temperature: 35,
      humidity: 10
    }
  }
  
  // OCÉANO - Océano abierto
  // Océano Pacífico - LA ZONA MÁS GRANDE DEL PLANETA
  // Longitud < -70 (excluyendo costas de América)
  if (lon < -70) {
    // Excluir toda América (lon > -120 es costa oeste, lon < -30 es costa este)
    // América del Norte: lat > 10, lon entre -170 y -50
    const isNorthAmerica = lat > 10 && lon > -170 && lon < -50
    
    // América Central: lat entre 7 y 23, lon entre -120 y -77
    const isCentralAmerica = lat > 7 && lat < 23 && lon > -120 && lon < -77
    
    // América del Sur: lat < 15, lon entre -82 y -34
    const isSouthAmerica = lat < 15 && lon > -82 && lon < -34
    
    // Patagonia: lat < -35, lon entre -75 y -53
    const isPatagonia = lat < -35 && lon > -75 && lon < -53
    
    // Si NO es ninguna parte de América, es océano
    if (!isNorthAmerica && !isCentralAmerica && !isSouthAmerica && !isPatagonia) {
      return {
        type: 'ocean',
        name: 'Océano Pacífico',
        description: 'Océano abierto',
        temperature: 20,
        humidity: 100
      }
    }
  }
  
  // Océano Pacífico occidental (lon > 140)
  if (lon > 140 && absLat < 50) {
    return {
      type: 'ocean',
      name: 'Océano Pacífico',
      description: 'Océano abierto',
      temperature: 20,
      humidity: 100
    }
  }
  
  // Océano Atlántico central
  if (lon > -50 && lon < -10 && absLat < 40) {
    return {
      type: 'ocean',
      name: 'Océano Atlántico',
      description: 'Océano abierto',
      temperature: 18,
      humidity: 100
    }
  }
  
  // Océano Índico
  if (lon > 40 && lon < 100 && lat < 0 && lat > -40) {
    return {
      type: 'ocean',
      name: 'Océano Índico',
      description: 'Océano abierto',
      temperature: 22,
      humidity: 100
    }
  }
  
  // DEFAULT - Terreno genérico
  return {
    type: 'default',
    name: 'Terreno Genérico',
    description: 'Paisaje variado',
    temperature: 20,
    humidity: 50
  }
}

// Helper para verificar si es región helada
export function isIcyRegion(lat: number, lon: number): boolean {
  return detectBiome(lat, lon).type === 'ice'
}

// Helper para obtener color del cielo según bioma
export function getSkyColorForBiome(biome: BiomeType, isDay: boolean): string {
  if (!isDay) return '#0a0a1a' // Noche oscura para todos
  
  switch (biome) {
    case 'ice':
      return '#b8d4e8' // Azul pálido helado
    case 'volcanic':
      return '#87ceeb' // Azul cielo (igual que default)
    case 'desert':
      return '#a8c8e8' // Azul cielo suave (menos amarillo)
    case 'ocean':
      return '#4a90e2' // Azul océano
    case 'forest':
      return '#87ceeb' // Azul cielo
    default:
      return '#87ceeb' // Azul cielo estándar
  }
}

// Helper para obtener color de niebla según bioma
export function getFogColorForBiome(biome: BiomeType): string {
  switch (biome) {
    case 'ice':
      return '#d0e8f2' // Niebla blanca-azulada
    case 'volcanic':
      return '#8b7355' // Niebla gris-marrón
    case 'desert':
      return '#f4e4c1' // Niebla amarillenta
    case 'ocean':
      return '#7fb3d5' // Niebla azul
    default:
      return '#87ceeb'
  }
}
