'use client'

/**
 * CosmicEntity - Entidades que revelan su relación con el cosmos
 * No son solo objetos 3D, son puntos de memoria que reaccionan al sol
 */

import { useRef, useEffect, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface CosmicEntityProps {
  children: React.ReactNode
  solarDirection?: THREE.Vector3
  isDay?: boolean
  showSolarAxis?: boolean
}

export default function CosmicEntity({ 
  children, 
  solarDirection = new THREE.Vector3(0, 1, 0),
  isDay = true,
  showSolarAxis = true
}: CosmicEntityProps) {
  const groupRef = useRef<THREE.Group>(null)
  // Usar state para almacenar las referencias de los objetos 3D
  const [solarAxis, setSolarAxis] = useState<THREE.Line | null>(null)
  const [shadowProjection, setShadowProjection] = useState<THREE.Mesh | null>(null)
  const [aura, setAura] = useState<THREE.Mesh | null>(null)
  
  // Crear eje solar (línea desde entidad hacia el sol)
  useEffect(() => {
    if (!groupRef.current || !showSolarAxis) return
    
    // Configurar el grupo para que esté en una capa diferente (capa 1)
    groupRef.current.layers.set(1)
    
    // Geometría de línea
    const points = [
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(0, 50, 0) // Será actualizado dinámicamente
    ]
    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    
    // Material etéreo
    const material = new THREE.LineBasicMaterial({
      color: 0xffd700,
      transparent: true,
      opacity: 0,
      linewidth: 1
    })
    
    const line = new THREE.Line(geometry, material)
    line.name = 'SolarAxis'
    line.raycast = () => {} // No bloquear raycast
    groupRef.current.add(line)
    setSolarAxis(line)
    
    // Proyección de sombra en el suelo (disco)
    const shadowGeometry = new THREE.CircleGeometry(1.5, 32)
    const shadowMaterial = new THREE.MeshBasicMaterial({
      color: 0x000000,
      transparent: true,
      opacity: 0,
      side: THREE.DoubleSide
    })
    const shadowMesh = new THREE.Mesh(shadowGeometry, shadowMaterial)
    shadowMesh.rotation.x = -Math.PI / 2
    shadowMesh.position.y = 0.01
    shadowMesh.name = 'ShadowProjection'
    shadowMesh.raycast = () => {} // No bloquear raycast
    groupRef.current.add(shadowMesh)
    setShadowProjection(shadowMesh)
    
    // Aura cósmica (esfera sutil)
    const auraGeometry = new THREE.SphereGeometry(2.5, 32, 32)
    const auraMaterial = new THREE.MeshBasicMaterial({
      color: 0xffd700,
      transparent: true,
      opacity: 0,
      side: THREE.BackSide,
      blending: THREE.AdditiveBlending
    })
    const auraMesh = new THREE.Mesh(auraGeometry, auraMaterial)
    auraMesh.name = 'CosmicAura'
    auraMesh.raycast = () => {} // No bloquear raycast
    groupRef.current.add(auraMesh)
    setAura(auraMesh)
    
    return () => {
      if (groupRef.current) {
        groupRef.current.remove(line)
        groupRef.current.remove(shadowMesh)
        groupRef.current.remove(auraMesh)
      }
      geometry.dispose()
      material.dispose()
      shadowGeometry.dispose()
      shadowMaterial.dispose()
      auraGeometry.dispose()
      auraMaterial.dispose()
    }
  }, [showSolarAxis])
  
  // Actualizar relación con el sol cada frame
  useFrame((state) => {
    if (!groupRef.current) return
    
    const time = state.clock.elapsedTime
    
    // Actualizar eje solar
    if (solarAxis && showSolarAxis) {
      const line = solarAxis
      const material = line.material as THREE.LineBasicMaterial
      const geometry = line.geometry as THREE.BufferGeometry
      
      // Dirección hacia el sol (extendida)
      const solarPoint = solarDirection.clone().multiplyScalar(50)
      const positions = geometry.attributes.position.array as Float32Array
      positions[3] = solarPoint.x
      positions[4] = solarPoint.y
      positions[5] = solarPoint.z
      geometry.attributes.position.needsUpdate = true
      
      // Opacidad según hora del día (más sutil, revelación gradual)
      const targetOpacity = isDay ? 0.08 : 0.03 // Reducido de 0.15/0.05 a 0.08/0.03
      material.opacity += (targetOpacity - material.opacity) * 0.02
      
      // Color según altura solar
      const sunHeight = solarDirection.y
      if (sunHeight < 0.3) {
        // Amanecer/atardecer: dorado intenso
        material.color.lerp(new THREE.Color(0xffa500), 0.05)
      } else {
        // Mediodía: dorado suave
        material.color.lerp(new THREE.Color(0xffd700), 0.05)
      }
    }
    
    // Actualizar proyección de sombra
    if (shadowProjection) {
      const shadow = shadowProjection
      const material = shadow.material as THREE.MeshBasicMaterial
      
      // Mantener sombra invisible
      material.opacity = 0
    }
    
    // Actualizar aura cósmica
    if (aura) {
      const auraMesh = aura
      const material = auraMesh.material as THREE.MeshBasicMaterial
      
      // Pulso lento
      const pulse = Math.sin(time * 0.3) * 0.5 + 0.5
      const baseScale = 1 + pulse * 0.1
      aura.scale.setScalar(baseScale)
      
      // Opacidad según alineación con el sol (más sutil)
      const alignment = Math.max(0, solarDirection.y)
      const targetOpacity = isDay ? alignment * 0.04 : 0.01 // Reducido de 0.08 a 0.04
      material.opacity += (targetOpacity - material.opacity) * 0.02
      
      // Color según hora
      if (solarDirection.y < 0.3 && solarDirection.y > -0.1) {
        // Amanecer/atardecer: naranja
        material.color.lerp(new THREE.Color(0xff6b35), 0.05)
      } else if (isDay) {
        // Día: dorado
        material.color.lerp(new THREE.Color(0xffd700), 0.05)
      } else {
        // Noche: azul profundo
        material.color.lerp(new THREE.Color(0x4a5899), 0.05)
      }
      
      // Rotación lenta
      aura.rotation.y += 0.001
    }
  })
  
  return (
    <group ref={groupRef} raycast={() => {}}>
      {children}
    </group>
  )
}
