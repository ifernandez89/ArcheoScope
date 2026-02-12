'use client'

import { useEffect } from 'react'
import { useEngine } from '@/hooks/useEngine'
import * as THREE from 'three'

export default function EngineDemo() {
  const engine = useEngine()

  useEffect(() => {
    if (!engine) return

    // Ejemplo: Timeline de eventos
    engine.timeline.addEvent({
      time: 2000,
      name: 'camera-intro',
      action: () => {
        console.log('🎬 Ejecutando transición de cámara')
        engine.cameraController.flyTo(
          new THREE.Vector3(3, 2, 3),
          new THREE.Vector3(0, 0, 0),
          1500
        )
      }
    })

    engine.timeline.addEvent({
      time: 5000,
      name: 'lighting-change',
      action: () => {
        console.log('💡 Cambiando hora del día')
        engine.lighting.setTimeOfDay(18) // Atardecer
      }
    })

    // Eventos de interacción
    engine.events.on('click', (event) => {
      console.log('🖱️ Click detectado:', event.target?.name)
    })

    engine.events.on('hover', (event) => {
      console.log('👆 Hover sobre:', event.target?.name)
    })

    // Iniciar timeline
    // engine.timeline.play() // Descomentar para activar

    return () => {
      engine.timeline.clear()
    }
  }, [engine])

  // Update loop
  useEffect(() => {
    if (!engine) return

    let animationId: number

    const animate = () => {
      engine.update()
      animationId = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId)
      }
    }
  }, [engine])

  return null // Este componente no renderiza nada visual
}
