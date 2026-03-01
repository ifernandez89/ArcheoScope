// Archaeological Sites - Sitios arqueológicos con coordenadas reales
import type { ArchaeologicalSite } from '@/geo/coordinate-system'

export const ARCHAEOLOGICAL_SITES: ArchaeologicalSite[] = [
  // Océano Pacífico
  {
    id: 'pacific-ocean-test',
    name: 'Océano Pacífico',
    description: 'Zona abierta del Océano Pacífico para probar el sistema de agua realista',
    coordinates: {
      latitude: 8.7783,
      longitude: -144.8885,
      altitude: 0
    },
    culture: 'Natural',
    period: 'Moderno',
    discovered: 2026
  },

  // Antártida
  {
    id: 'antarctica',
    name: 'Antártida',
    description: 'Continente helado en el extremo sur del planeta',
    coordinates: {
      latitude: -75.2509,
      longitude: 0.0714,
      altitude: 2835
    },
    culture: 'Natural',
    period: 'Moderno',
    discovered: 1820
  },

  // Bolivia
  {
    id: 'puma-punku',
    name: 'Puma Punku - Tiwanaku',
    description: 'Complejo megalítico con bloques de andesita y diorita de precisión extraordinaria. Parte del sitio de Tiwanaku, Patrimonio de la Humanidad.',
    coordinates: {
      latitude: -16.56164569638123,
      longitude: -68.67952141492464,
      altitude: 3840
    },
    modelPath: '/puma_punku_block.glb',
    culture: 'Tiwanaku',
    period: 'Período Tiwanaku',
    discovered: 500
  },

  // Egipto
  {
    id: 'giza-pyramid',
    name: 'Pirámides de Giza',
    description: 'Las pirámides más famosas de Egipto, incluyendo la Gran Pirámide de Keops',
    coordinates: {
      latitude: 29.9792,
      longitude: 31.1342,
      altitude: 146
    },
    culture: 'Egipcia',
    period: 'Reino Antiguo',
    discovered: -2560
  },

  // Isla de Pascua
  {
    id: 'rapa-nui-ahu-tongariki',
    name: 'Isla de Pascua - Ahu Tongariki',
    description: 'Plataforma ceremonial con 15 moai, el ahu más grande de Rapa Nui',
    coordinates: {
      latitude: -27.1254,
      longitude: -109.2778,
      altitude: 10
    },
    modelPath: '/moai.glb',
    culture: 'Rapa Nui',
    period: 'Período Medio',
    discovered: 1400
  },

  // México - Teotihuacán
  {
    id: 'teotihuacan',
    name: 'Teotihuacán',
    description: 'Ciudad prehispánica con las pirámides del Sol y la Luna',
    coordinates: {
      latitude: 19.6925,
      longitude: -98.8438,
      altitude: 2300
    },
    culture: 'Teotihuacana',
    period: 'Período Clásico',
    discovered: -100
  },

  // México - Tres Zapotes
  {
    id: 'tres-zapotes',
    name: 'Tres Zapotes',
    description: 'Importante sitio arqueológico olmeca en Veracruz, México. Conocido por sus cabezas colosales y estelas.',
    coordinates: {
      latitude: 18.4667,
      longitude: -95.4500,
      altitude: 50
    },
    culture: 'Olmeca',
    period: 'Período Preclásico',
    discovered: -1200
  }
]

// Sitios por región
export const SITES_BY_REGION = {
  americas: ['puma-punku', 'rapa-nui-ahu-tongariki', 'teotihuacan', 'tres-zapotes'],
  africa: ['giza-pyramid'],
  oceania: ['pacific-ocean-test'],
  antarctica: ['antarctica']
}

// Sitios por cultura
export const SITES_BY_CULTURE = {
  tiwanaku: ['puma-punku'],
  egipcia: ['giza-pyramid'],
  rapaui: ['rapa-nui-ahu-tongariki'],
  teotihuacana: ['teotihuacan'],
  olmeca: ['tres-zapotes']
}
