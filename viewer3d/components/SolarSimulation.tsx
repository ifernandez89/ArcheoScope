'use client'

import { useRef, useEffect } from 'react'
import * as THREE from 'three'
import { loggers } from '@/core/Logger'

/** Simulación solar real basada en coordenadas geográficas y hora actual */
export default function SolarSimulation({ lat, lon }: { lat: number; lon: number }) {
  const lightRef = useRef<THREE.DirectionalLight>(null)

  useEffect(() => {
    if (!lightRef.current) return

    const now = new Date()
    const dayOfYear = Math.floor((now.getTime() - new Date(now.getFullYear(), 0, 0).getTime()) / 86400000)
    const hour = now.getHours() + now.getMinutes() / 60

    const declination = 23.45 * Math.sin((360 / 365) * (dayOfYear - 81) * Math.PI / 180)
    const hourAngle = 15 * (hour - 12)

    const altitude = Math.asin(
      Math.sin(lat * Math.PI / 180) * Math.sin(declination * Math.PI / 180) +
      Math.cos(lat * Math.PI / 180) * Math.cos(declination * Math.PI / 180) * Math.cos(hourAngle * Math.PI / 180)
    ) * 180 / Math.PI

    const distance = 15
    const x = distance * Math.cos(altitude * Math.PI / 180) * Math.sin(hourAngle * Math.PI / 180)
    const y = distance * Math.sin(altitude * Math.PI / 180)
    const z = distance * Math.cos(altitude * Math.PI / 180) * Math.cos(hourAngle * Math.PI / 180)

    lightRef.current.position.set(x, Math.max(y, 2), z)
    lightRef.current.intensity = Math.max(0.3, Math.sin(altitude * Math.PI / 180) * 1.5)
    lightRef.current.color.set(altitude > 0 ? (altitude < 15 ? '#ff9966' : '#ffffff') : '#1a1a2e')

    loggers.world.debug('Simulación solar:', { lat: lat.toFixed(2), lon: lon.toFixed(2), altitude: altitude.toFixed(2) })
  }, [lat, lon])

  return (
    <>
      <ambientLight intensity={0.2} />
      <directionalLight ref={lightRef} castShadow shadow-mapSize-width={2048} shadow-mapSize-height={2048} />
      <hemisphereLight args={['#87ceeb', '#654321', 0.2]} />
    </>
  )
}
