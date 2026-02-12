'use client'

import { useControls, folder } from 'leva'
import { useSceneStore } from '@/store/scene-store'

export default function AdvancedControls() {
  const setAutoRotate = useSceneStore((state) => state.setAutoRotate)
  const toggleGrid = useSceneStore((state) => state.toggleGrid)

  const controls = useControls({
    'Modelo': folder({
      autoRotate: {
        value: true,
        onChange: (v) => setAutoRotate(v)
      },
      rotationSpeed: {
        value: 0.5,
        min: 0,
        max: 2,
        step: 0.1
      }
    }),
    
    'Cámara': folder({
      fov: {
        value: 50,
        min: 20,
        max: 100,
        step: 1
      },
      position: {
        value: { x: 5, y: 3, z: 5 },
        step: 0.5
      }
    }),
    
    'Iluminación': folder({
      ambientIntensity: {
        value: 0.4,
        min: 0,
        max: 2,
        step: 0.1,
        label: 'Luz Ambiental'
      },
      directionalIntensity: {
        value: 1.2,
        min: 0,
        max: 3,
        step: 0.1,
        label: 'Luz Direccional'
      },
      timeOfDay: {
        value: 12,
        min: 0,
        max: 24,
        step: 0.5,
        label: 'Hora del Día'
      }
    }),
    
    'Efectos': folder({
      bloomIntensity: {
        value: 0.3,
        min: 0,
        max: 2,
        step: 0.1,
        label: 'Bloom'
      },
      ssaoIntensity: {
        value: 30,
        min: 0,
        max: 100,
        step: 5,
        label: 'SSAO'
      }
    }),
    
    'Escena': folder({
      showGrid: {
        value: true,
        label: 'Mostrar Grid',
        onChange: () => toggleGrid()
      },
      backgroundColor: {
        value: '#0a0a0a',
        label: 'Fondo'
      }
    })
  })

  return null // Leva se renderiza automáticamente
}
