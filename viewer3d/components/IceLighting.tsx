'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface IceLightingProps {
  sunPosition?: [number, number, number]
  enableShadows?: boolean
}

export default function IceLighting({ 
  sunPosition = [30, 40, 30],
  enableShadows = true 
}: IceLightingProps) {
  const sunRef = useRef<THREE.DirectionalLight>(null)
  
  // Animación sutil de intensidad para simular reflejos de hielo
  useFrame((state) => {
    if (sunRef.current) {
      const time = state.clock.getElapsedTime()
      sunRef.current.intensity = 2.0 + Math.sin(time * 0.5) * 0.3
    }
  })
  
  return (
    <>
      {/* Sol directo - más brillante para reflejos en hielo */}
      <directionalLight
        ref={sunRef}
        position={sunPosition}
        intensity={2.0}
        color="#f0f8ff"
        castShadow={enableShadows}
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={100}
        shadow-camera-left={-50}
        shadow-camera-right={50}
        shadow-camera-top={50}
        shadow-camera-bottom={-50}
        shadow-bias={-0.0001}
      />
      
      {/* Luz hemisférica fría */}
      <hemisphereLight
        color="#d0e8f2"
        groundColor="#b8d4e8"
        intensity={1.5}
      />
      
      {/* Luz ambiental azulada */}
      <ambientLight color="#c8e0f0" intensity={0.8} />
      
      {/* Luz de relleno para reducir sombras duras */}
      <directionalLight
        position={[-20, 20, -20]}
        intensity={0.6}
        color="#e8f4f8"
      />
      
      {/* Luz de reflejo del hielo desde abajo */}
      <pointLight
        position={[0, 2, 0]}
        intensity={0.4}
        color="#ffffff"
        distance={30}
      />
    </>
  )
}
