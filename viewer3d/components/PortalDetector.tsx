'use client'

import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface PortalDetectorProps {
  avatarPositionRef: React.RefObject<THREE.Vector3>
  portalPosition: [number, number, number]
  portalRotation: [number, number, number]
  portalScale: number
  onPortalEnter: () => void
  enabled: boolean
}

export default function PortalDetector({
  avatarPositionRef,
  portalPosition,
  portalRotation,
  portalScale,
  onPortalEnter,
  enabled
}: PortalDetectorProps) {
  const hasEnteredRef = useRef(false)
  const cooldownRef = useRef(0)
  
  // Vector reutilizable para evitar crear en cada frame
  const portalPosVec = useRef(new THREE.Vector3())

  useFrame((_, delta) => {
    if (!enabled || !avatarPositionRef.current) return

    // Cooldown para evitar múltiples activaciones
    if (cooldownRef.current > 0) {
      cooldownRef.current -= delta
      return
    }

    const avatarPos = avatarPositionRef.current
    portalPosVec.current.set(portalPosition[0], portalPosition[1], portalPosition[2])

    // Calcular distancia al portal
    const distance = avatarPos.distanceTo(portalPosVec.current)

    // Radio de detección basado en el tamaño del portal
    const detectionRadius = portalScale * 2

    // Si el avatar está dentro del radio del portal
    if (distance < detectionRadius && !hasEnteredRef.current) {
      console.log('🌀 ¡Portal atravesado! Teletransportando al Lago Titicaca...')
      hasEnteredRef.current = true
      cooldownRef.current = 5 // 5 segundos de cooldown
      onPortalEnter()
      
      // Reset después de un tiempo
      setTimeout(() => {
        hasEnteredRef.current = false
      }, 6000)
    } else if (distance > detectionRadius * 1.5) {
      // Reset si se aleja lo suficiente
      hasEnteredRef.current = false
    }
  })

  return null
}
