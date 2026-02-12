// Predefined Scenes for Archaeological Models
import * as THREE from 'three'
import type { SceneDefinition } from '@/experience/scene-system'

export const ARCHAEOLOGICAL_SCENES: SceneDefinition[] = [
  {
    id: 'intro',
    name: 'Introducción',
    description: 'Bienvenida al tour arqueológico virtual',
    models: [],
    camera: {
      position: new THREE.Vector3(8, 5, 8),
      target: new THREE.Vector3(0, 0, 0),
      fov: 50,
      transition: {
        duration: 2000,
        easing: 'easeInOut'
      }
    },
    lighting: {
      timeOfDay: 12,
      ambient: { intensity: 0.5, color: '#ffffff' }
    },
    duration: 5000,
    autoPlay: true,
    onEnter: () => {
      console.log('🎬 Bienvenido al tour arqueológico')
    }
  },

  {
    id: 'moai-scene',
    name: 'Moai de Rapa Nui',
    description: 'Estatuas monolíticas de la Isla de Pascua',
    models: [
      {
        id: 'moai',
        path: '/moai.glb',
        position: new THREE.Vector3(0, 0, 0),
        scale: 1
      }
    ],
    camera: {
      position: new THREE.Vector3(5, 3, 5),
      target: new THREE.Vector3(0, 1, 0),
      fov: 50,
      transition: {
        duration: 2500,
        easing: 'easeInOut'
      }
    },
    lighting: {
      timeOfDay: 14,
      ambient: { intensity: 0.4, color: '#ffffff' },
      directional: { intensity: 1.2, position: [10, 10, 5] }
    },
    audio: {
      background: '/audio/ocean-waves.mp3',
      narration: '/audio/moai-narration.mp3',
      volume: 0.7,
      loop: true
    },
    duration: 15000,
    autoPlay: false,
    onEnter: () => {
      console.log('🗿 Explorando Moai de Rapa Nui')
    }
  },

  {
    id: 'sphinx-scene',
    name: 'Esfinge de Giza',
    description: 'Monumento icónico del antiguo Egipto',
    models: [
      {
        id: 'sphinx',
        path: '/sphinxWithBase.glb',
        position: new THREE.Vector3(0, 0, 0),
        scale: 1
      }
    ],
    camera: {
      position: new THREE.Vector3(6, 4, 6),
      target: new THREE.Vector3(0, 1.5, 0),
      fov: 45,
      transition: {
        duration: 3000,
        easing: 'easeInOut'
      }
    },
    lighting: {
      timeOfDay: 16,
      ambient: { intensity: 0.5, color: '#fff5e6' },
      directional: { intensity: 1.5, position: [8, 12, 4] }
    },
    audio: {
      background: '/audio/desert-wind.mp3',
      narration: '/audio/sphinx-narration.mp3',
      volume: 0.6,
      loop: true
    },
    duration: 15000,
    autoPlay: false,
    onEnter: () => {
      console.log('🦁 Explorando la Esfinge de Giza')
    }
  },

  {
    id: 'warrior-scene',
    name: 'Guerrero Antiguo',
    description: 'Representación de un guerrero histórico',
    models: [
      {
        id: 'warrior',
        path: '/warrior.glb',
        position: new THREE.Vector3(0, 0, 0),
        scale: 1,
        animation: 'idle'
      }
    ],
    camera: {
      position: new THREE.Vector3(4, 2, 4),
      target: new THREE.Vector3(0, 1, 0),
      fov: 55,
      transition: {
        duration: 2000,
        easing: 'easeOut'
      }
    },
    lighting: {
      timeOfDay: 10,
      ambient: { intensity: 0.6, color: '#ffffff' },
      directional: { intensity: 1.0, position: [5, 8, 3] }
    },
    audio: {
      background: '/audio/ambient-battle.mp3',
      volume: 0.5,
      loop: true
    },
    duration: 12000,
    autoPlay: false,
    onEnter: () => {
      console.log('⚔️ Explorando Guerrero Antiguo')
    }
  },

  {
    id: 'comparison-scene',
    name: 'Comparación Cultural',
    description: 'Moai y Esfinge lado a lado',
    models: [
      {
        id: 'moai',
        path: '/moai.glb',
        position: new THREE.Vector3(-3, 0, 0),
        scale: 0.8
      },
      {
        id: 'sphinx',
        path: '/sphinx.glb',
        position: new THREE.Vector3(3, 0, 0),
        scale: 0.8
      }
    ],
    camera: {
      position: new THREE.Vector3(0, 4, 10),
      target: new THREE.Vector3(0, 1, 0),
      fov: 60,
      transition: {
        duration: 3500,
        easing: 'easeInOut'
      }
    },
    lighting: {
      timeOfDay: 12,
      ambient: { intensity: 0.5, color: '#ffffff' },
      directional: { intensity: 1.3, position: [0, 10, 5] }
    },
    duration: 20000,
    autoPlay: false,
    onEnter: () => {
      console.log('🌍 Comparando culturas: Rapa Nui vs Egipto')
    }
  },

  {
    id: 'finale',
    name: 'Final del Tour',
    description: 'Conclusión del recorrido arqueológico',
    models: [],
    camera: {
      position: new THREE.Vector3(10, 6, 10),
      target: new THREE.Vector3(0, 0, 0),
      fov: 50,
      transition: {
        duration: 3000,
        easing: 'easeOut'
      }
    },
    lighting: {
      timeOfDay: 18,
      ambient: { intensity: 0.6, color: '#ffd4a3' }
    },
    duration: 5000,
    onEnter: () => {
      console.log('🎬 Fin del tour arqueológico')
    },
    onExit: () => {
      console.log('👋 Gracias por visitar')
    }
  }
]

// Escenas por categoría
export const SCENE_CATEGORIES = {
  intro: ['intro'],
  individual: ['moai-scene', 'sphinx-scene', 'warrior-scene'],
  comparison: ['comparison-scene'],
  finale: ['finale']
}

// Orden del tour completo
export const TOUR_ORDER = [
  'intro',
  'moai-scene',
  'sphinx-scene',
  'warrior-scene',
  'comparison-scene',
  'finale'
]
