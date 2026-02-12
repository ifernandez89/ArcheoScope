// Archaeological Sites - Sitios arqueológicos con coordenadas reales
import type { ArchaeologicalSite } from '@/geo/coordinate-system'

export const ARCHAEOLOGICAL_SITES: ArchaeologicalSite[] = [
  // Egipto
  {
    id: 'giza-sphinx',
    name: 'Gran Esfinge de Giza',
    description: 'Monumento icónico del antiguo Egipto, construido durante el reinado de Kefrén (c. 2558-2532 a.C.)',
    coordinates: {
      latitude: 29.9753,
      longitude: 31.1376,
      altitude: 60
    },
    modelPath: '/sphinxWithBase.glb',
    culture: 'Egipcia',
    period: 'Reino Antiguo',
    discovered: -2500
  },
  {
    id: 'giza-pyramid',
    name: 'Gran Pirámide de Giza',
    description: 'La más grande de las tres pirámides de Giza, construida como tumba del faraón Keops',
    coordinates: {
      latitude: 29.9792,
      longitude: 31.1342,
      altitude: 146
    },
    culture: 'Egipcia',
    period: 'Reino Antiguo',
    discovered: -2560
  },
  {
    id: 'karnak',
    name: 'Templo de Karnak',
    description: 'Complejo de templos más grande de Egipto, dedicado principalmente a Amón-Ra',
    coordinates: {
      latitude: 25.7188,
      longitude: 32.6573,
      altitude: 75
    },
    culture: 'Egipcia',
    period: 'Reino Nuevo',
    discovered: -1400
  },

  // Isla de Pascua
  {
    id: 'rapa-nui-ahu-tongariki',
    name: 'Ahu Tongariki',
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
  {
    id: 'rapa-nui-rano-raraku',
    name: 'Rano Raraku',
    description: 'Cantera volcánica donde se tallaron la mayoría de los moai',
    coordinates: {
      latitude: -27.1247,
      longitude: -109.2897,
      altitude: 150
    },
    modelPath: '/moai.glb',
    culture: 'Rapa Nui',
    period: 'Período Medio',
    discovered: 1200
  },

  // Perú
  {
    id: 'machu-picchu',
    name: 'Machu Picchu',
    description: 'Ciudad inca del siglo XV, una de las Siete Maravillas del Mundo Moderno',
    coordinates: {
      latitude: -13.1631,
      longitude: -72.5450,
      altitude: 2430
    },
    culture: 'Inca',
    period: 'Imperio Inca',
    discovered: 1450
  },
  {
    id: 'nazca-lines',
    name: 'Líneas de Nazca',
    description: 'Geoglifos gigantes en el desierto de Nazca, Patrimonio de la Humanidad',
    coordinates: {
      latitude: -14.7390,
      longitude: -75.1300,
      altitude: 520
    },
    culture: 'Nazca',
    period: 'Período Intermedio Temprano',
    discovered: -200
  },
  {
    id: 'sacsayhuaman',
    name: 'Sacsayhuamán',
    description: 'Fortaleza inca con enormes bloques de piedra perfectamente ensamblados',
    coordinates: {
      latitude: -13.5084,
      longitude: -71.9826,
      altitude: 3701
    },
    culture: 'Inca',
    period: 'Imperio Inca',
    discovered: 1440
  },

  // México
  {
    id: 'chichen-itza',
    name: 'Chichén Itzá',
    description: 'Ciudad maya con la famosa pirámide de Kukulkán (El Castillo)',
    coordinates: {
      latitude: 20.6843,
      longitude: -88.5678,
      altitude: 25
    },
    culture: 'Maya',
    period: 'Período Clásico Terminal',
    discovered: 600
  },
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

  // Reino Unido
  {
    id: 'stonehenge',
    name: 'Stonehenge',
    description: 'Monumento megalítico prehistórico, Patrimonio de la Humanidad',
    coordinates: {
      latitude: 51.1789,
      longitude: -1.8262,
      altitude: 100
    },
    culture: 'Neolítica',
    period: 'Neolítico',
    discovered: -3000
  },

  // Grecia
  {
    id: 'parthenon',
    name: 'Partenón',
    description: 'Templo dedicado a Atenea en la Acrópolis de Atenas',
    coordinates: {
      latitude: 37.9715,
      longitude: 23.7267,
      altitude: 156
    },
    culture: 'Griega',
    period: 'Período Clásico',
    discovered: -447
  },

  // Italia
  {
    id: 'colosseum',
    name: 'Coliseo Romano',
    description: 'Anfiteatro más grande del Imperio Romano',
    coordinates: {
      latitude: 41.8902,
      longitude: 12.4922,
      altitude: 25
    },
    culture: 'Romana',
    period: 'Imperio Romano',
    discovered: 80
  },

  // Jordania
  {
    id: 'petra',
    name: 'Petra',
    description: 'Ciudad nabatea tallada en roca, una de las Siete Maravillas',
    coordinates: {
      latitude: 30.3285,
      longitude: 35.4444,
      altitude: 810
    },
    culture: 'Nabatea',
    period: 'Período Helenístico',
    discovered: -312
  },

  // Camboya
  {
    id: 'angkor-wat',
    name: 'Angkor Wat',
    description: 'Complejo de templos más grande del mundo, Patrimonio de la Humanidad',
    coordinates: {
      latitude: 13.4125,
      longitude: 103.8670,
      altitude: 65
    },
    culture: 'Jemer',
    period: 'Imperio Jemer',
    discovered: 1113
  },

  // China
  {
    id: 'great-wall',
    name: 'Gran Muralla China',
    description: 'Sistema de fortificaciones más largo del mundo',
    coordinates: {
      latitude: 40.4319,
      longitude: 116.5704,
      altitude: 1000
    },
    culture: 'China',
    period: 'Dinastías Varias',
    discovered: -700
  },

  // India
  {
    id: 'taj-mahal',
    name: 'Taj Mahal',
    description: 'Mausoleo de mármol blanco, símbolo del amor eterno',
    coordinates: {
      latitude: 27.1751,
      longitude: 78.0421,
      altitude: 171
    },
    culture: 'Mogol',
    period: 'Imperio Mogol',
    discovered: 1653
  }
]

// Sitios por región
export const SITES_BY_REGION = {
  africa: ['giza-sphinx', 'giza-pyramid', 'karnak'],
  americas: ['rapa-nui-ahu-tongariki', 'rapa-nui-rano-raraku', 'machu-picchu', 'nazca-lines', 'sacsayhuaman', 'chichen-itza', 'teotihuacan'],
  europe: ['stonehenge', 'parthenon', 'colosseum'],
  asia: ['petra', 'angkor-wat', 'great-wall', 'taj-mahal']
}

// Sitios por cultura
export const SITES_BY_CULTURE = {
  egipcia: ['giza-sphinx', 'giza-pyramid', 'karnak'],
  rapaui: ['rapa-nui-ahu-tongariki', 'rapa-nui-rano-raraku'],
  inca: ['machu-picchu', 'sacsayhuaman'],
  maya: ['chichen-itza'],
  griega: ['parthenon'],
  romana: ['colosseum']
}
