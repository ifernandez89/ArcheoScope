'use client'

import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface WaterCollisionDetectorProps {
  avatarPositionRef: React.RefObject<THREE.Vector3>
  waterLevel: number
  location?: { lat: number; lon: number } | null
  onWaterTouch: (location: { lat: number; lon: number }) => void
}

export default function WaterCollisionDetector({
  avatarPositionRef,
  waterLevel,
  location,
  onWaterTouch
}: WaterCollisionDetectorProps) {
  const hasTriggeredRef = useRef(false)
  const cooldownRef = useRef(0)

  useFrame((state, delta) => {
    // Verificar si estamos en el Lago Titicaca PRIMERO
    if (!location) {
      console.log('❌ No hay location')
      return
    }

    const isInTiticaca =
      location.lat > -16.5 &&
      location.lat < -15.5 &&
      location.lon > -70 &&
      location.lon < -68.5

    if (!isInTiticaca) {
      hasTriggeredRef.current = false
      return
    }

    // Obtener posición actual del avatar
    if (!avatarPositionRef.current) {
      console.log('❌ No hay avatarPositionRef')
      return
    }
    const avatarPosition = avatarPositionRef.current

    // Cooldown para evitar triggers múltiples
    if (cooldownRef.current > 0) {
      cooldownRef.current -= delta
      console.log('⏳ Cooldown activo:', cooldownRef.current.toFixed(2))
      return
    }

    // Detectar si el avatar toca el agua (PRECISO - solo al tocar)
    const touchThreshold = 2.0 // Reducido a 2.0 para ser más preciso
    const distanceToWater = Math.abs(avatarPosition.y - waterLevel)

    // Debug log CONSTANTE para ver qué está pasando
    console.log('🌊 Water Detector:', {
      avatarY: avatarPosition.y.toFixed(2),
      waterLevel,
      distance: distanceToWater.toFixed(2),
      threshold: touchThreshold,
      hasTriggered: hasTriggeredRef.current,
      cooldown: cooldownRef.current.toFixed(2),
      willTrigger: distanceToWater < touchThreshold && !hasTriggeredRef.current,
      isInTiticaca
    })

    if (distanceToWater < touchThreshold && !hasTriggeredRef.current) {
      // ¡Tocó el agua!
      console.log('🎉🎉🎉 ITEM DESCUBIERTO! Magna Bowl encontrado en Lago Titicaca')
      hasTriggeredRef.current = true
      cooldownRef.current = 20 // Cooldown de 20 segundos para evitar activaciones múltiples
      onWaterTouch(location)
    }

    // Reset si se aleja del agua
    if (distanceToWater > 10) {
      if (hasTriggeredRef.current) {
        console.log('🔄 Reset - Avatar se alejó del agua')
      }
      hasTriggeredRef.current = false
    }
  })

  return null // Componente invisible
}
