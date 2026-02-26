'use client'

/**
 * AmbientAudio - Drone atmosférico independiente del modo de cámara
 * Funciona tanto en modo órbita como en modo avatar/exploración
 */

import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { AtmosphericSound } from '@/engines/AtmosphericSound'

export default function AmbientAudio() {
  const soundRef = useRef<AtmosphericSound | null>(null)
  const initializedRef = useRef(false)
  const timeRef = useRef(0)

  // Inicializar en primera interacción del usuario
  useEffect(() => {
    const init = async () => {
      if (initializedRef.current) return
      initializedRef.current = true

      const sound = new AtmosphericSound()
      await sound.initialize()
      sound.setEnabled(true)
      soundRef.current = sound
      console.log('🔊 AmbientAudio: drone atmosférico activo')
    }

    // Intentar en primer click/touch (requiere gesto del usuario)
    const handleInteraction = () => {
      init()
      window.removeEventListener('click', handleInteraction)
      window.removeEventListener('keydown', handleInteraction)
      window.removeEventListener('touchstart', handleInteraction)
    }

    window.addEventListener('click', handleInteraction)
    window.addEventListener('keydown', handleInteraction)
    window.addEventListener('touchstart', handleInteraction)

    return () => {
      window.removeEventListener('click', handleInteraction)
      window.removeEventListener('keydown', handleInteraction)
      window.removeEventListener('touchstart', handleInteraction)
      soundRef.current?.dispose()
    }
  }, [])

  // Actualizar cada frame con valores por defecto (mediodía, viento suave)
  useFrame((_, delta) => {
    if (!soundRef.current) return
    timeRef.current += delta
    // solarAltitude: 0 = horizonte, PI/2 = cenit — usamos valor fijo de mediodía
    soundRef.current.update(delta, Math.PI / 4, 0.4)
  })

  return null
}
