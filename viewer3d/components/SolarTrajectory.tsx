'use client'

/**
 * SolarTrajectory - Visualización de la trayectoria solar del día
 * Muestra el arco completo del sol, ejes cardinales y eje axial terrestre
 */

import { useRef, useEffect, useMemo, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface SolarTrajectoryProps {
  solarAltitude: number
  solarAzimuth: number
  declination: number
  latitude: number
  isDay: boolean
  visible?: boolean
}

export default function SolarTrajectory({
  solarAltitude,
  solarAzimuth,
  declination,
  latitude,
  isDay,
  visible = true
}: SolarTrajectoryProps) {
  const groupRef = useRef<THREE.Group>(null)
  const [trajectory, setTrajectory] = useState<THREE.Line | null>(null)
  const [currentPos, setCurrentPos] = useState<THREE.Mesh | null>(null)
  
  // Crear geometría de la trayectoria solar
  useEffect(() => {
    if (!groupRef.current || !visible) return
    
    const group = groupRef.current
    
    // Configurar el grupo para que esté en una capa diferente (capa 1)
    group.layers.set(1)
    
    // Limpiar geometrías anteriores
    while (group.children.length > 0) {
      const child = group.children[0]
      group.remove(child)
      if (child instanceof THREE.Mesh || child instanceof THREE.Line) {
        child.geometry.dispose()
        if (Array.isArray(child.material)) {
          child.material.forEach(m => m.dispose())
        } else {
          child.material.dispose()
        }
      }
    }
    
    // 1. ARCO DE TRAYECTORIA SOLAR
    const points: THREE.Vector3[] = []
    const numPoints = 100
    
    // Calcular puntos del arco solar para todo el día
    for (let i = 0; i < numPoints; i++) {
      const hourAngle = ((i / numPoints) * 24 - 12) / 12 * Math.PI
      
      // Altura solar en este punto
      const alt = Math.asin(
        Math.sin(latitude) * Math.sin(declination) +
        Math.cos(latitude) * Math.cos(declination) * Math.cos(hourAngle)
      )
      
      // Azimut solar en este punto
      const az = Math.atan2(
        -Math.sin(hourAngle),
        Math.tan(declination) * Math.cos(latitude) -
        Math.sin(latitude) * Math.cos(hourAngle)
      )
      
      // Solo puntos sobre el horizonte
      if (alt > 0) {
        const radius = 40
        const x = radius * Math.cos(alt) * Math.sin(az)
        const y = radius * Math.sin(alt)
        const z = radius * Math.cos(alt) * Math.cos(az)
        points.push(new THREE.Vector3(x, y, z))
      }
    }
    
    if (points.length > 1) {
      const trajectoryGeometry = new THREE.BufferGeometry().setFromPoints(points)
      const trajectoryMaterial = new THREE.LineBasicMaterial({
        color: 0xffd700,
        transparent: true,
        opacity: 0.15, // Reducido de 0.3 a 0.15 (50% más sutil)
        linewidth: 1 // Reducido de 2 a 1
      })
      const trajectoryLine = new THREE.Line(trajectoryGeometry, trajectoryMaterial)
      trajectoryLine.name = 'SolarTrajectory'
      trajectoryLine.raycast = () => {} // No bloquear raycast
      group.add(trajectoryLine)
      setTrajectory(trajectoryLine)
    }
    
    // 2. POSICIÓN ACTUAL DEL SOL
    const currentRadius = 40
    const currentX = currentRadius * Math.cos(solarAltitude) * Math.sin(solarAzimuth)
    const currentY = currentRadius * Math.sin(solarAltitude)
    const currentZ = currentRadius * Math.cos(solarAltitude) * Math.cos(solarAzimuth)
    
    const sunMarkerGeometry = new THREE.SphereGeometry(0.8, 16, 16)
    const sunMarkerMaterial = new THREE.MeshBasicMaterial({
      color: 0xffaa00,
      transparent: true,
      opacity: 0.5 // Reducido de 0.8 a 0.5 (más sutil)
    })
    const sunMarker = new THREE.Mesh(sunMarkerGeometry, sunMarkerMaterial)
    sunMarker.position.set(currentX, currentY, currentZ)
    sunMarker.name = 'CurrentSunPosition'
    sunMarker.raycast = () => {} // No bloquear raycast
    group.add(sunMarker)
    setCurrentPos(sunMarker)
    
    // 3. EJES CARDINALES (N-S, E-O)
    const cardinalMaterial = new THREE.LineBasicMaterial({
      color: 0x4a90e2,
      transparent: true,
      opacity: 0.08, // Reducido de 0.2 a 0.08 (ultra sutil)
      linewidth: 1
    })
    
    // Norte-Sur
    const nsPoints = [
      new THREE.Vector3(0, 0, -50),
      new THREE.Vector3(0, 0, 50)
    ]
    const nsGeometry = new THREE.BufferGeometry().setFromPoints(nsPoints)
    const nsLine = new THREE.Line(nsGeometry, cardinalMaterial)
    nsLine.name = 'NorthSouth'
    nsLine.raycast = () => {} // No bloquear raycast
    group.add(nsLine)
    
    // Este-Oeste
    const ewPoints = [
      new THREE.Vector3(-50, 0, 0),
      new THREE.Vector3(50, 0, 0)
    ]
    const ewGeometry = new THREE.BufferGeometry().setFromPoints(ewPoints)
    const ewLine = new THREE.Line(ewGeometry, cardinalMaterial.clone())
    ewLine.name = 'EastWest'
    ewLine.raycast = () => {} // No bloquear raycast
    group.add(ewLine)
    
    // 4. EJE AXIAL TERRESTRE (inclinado 23.44°)
    const axialTilt = 23.44 * Math.PI / 180
    const axialPoints = [
      new THREE.Vector3(0, -30, 0),
      new THREE.Vector3(0, 30, 0)
    ]
    const axialGeometry = new THREE.BufferGeometry().setFromPoints(axialPoints)
    const axialMaterial = new THREE.LineBasicMaterial({
      color: 0x00ff88,
      transparent: true,
      opacity: 0.12, // Reducido de 0.25 a 0.12 (más sutil)
      linewidth: 1 // Reducido de 2 a 1
    })
    const axialLine = new THREE.Line(axialGeometry, axialMaterial)
    axialLine.rotation.z = axialTilt
    axialLine.name = 'EarthAxis'
    axialLine.raycast = () => {} // No bloquear raycast
    group.add(axialLine)
    
    // 5. CÍRCULO DE HORIZONTE (invisible)
    const horizonPoints: THREE.Vector3[] = []
    for (let i = 0; i <= 64; i++) {
      const angle = (i / 64) * Math.PI * 2
      horizonPoints.push(new THREE.Vector3(
        Math.cos(angle) * 45,
        0.1,
        Math.sin(angle) * 45
      ))
    }
    const horizonGeometry = new THREE.BufferGeometry().setFromPoints(horizonPoints)
    const horizonMaterial = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0, // Invisible
      linewidth: 1
    })
    const horizonLine = new THREE.Line(horizonGeometry, horizonMaterial)
    horizonLine.name = 'Horizon'
    horizonLine.raycast = () => {} // No bloquear raycast
    group.add(horizonLine)
    
    return () => {
      // Cleanup
      while (group.children.length > 0) {
        const child = group.children[0]
        group.remove(child)
        if (child instanceof THREE.Mesh || child instanceof THREE.Line) {
          child.geometry.dispose()
          if (Array.isArray(child.material)) {
            child.material.forEach(m => m.dispose())
          } else {
            child.material.dispose()
          }
        }
      }
    }
  }, [solarAltitude, solarAzimuth, declination, latitude, visible])
  
  // Animar opacidad según hora del día (revelación gradual)
  useFrame((state) => {
    if (!groupRef.current) return
    
    const time = state.clock.elapsedTime
    
    // Revelación sutil: las líneas aparecen y desaparecen lentamente
    const revealCycle = Math.sin(time * 0.1) * 0.5 + 0.5 // Ciclo lento 0-1
    const targetOpacity = isDay && visible ? revealCycle * 0.3 : 0 // Máximo 30% de opacidad
    
    groupRef.current.children.forEach(child => {
      if (child instanceof THREE.Line) {
        const material = child.material as THREE.LineBasicMaterial
        const baseName = child.name
        
        // Diferentes velocidades de revelación según el elemento
        let multiplier = 1
        if (baseName === 'SolarTrajectory') multiplier = 0.8
        if (baseName === 'NorthSouth' || baseName === 'EastWest') multiplier = 0.4
        if (baseName === 'EarthAxis') multiplier = 0.6
        
        material.opacity += (targetOpacity * multiplier - material.opacity) * 0.02
      } else if (child instanceof THREE.Mesh && child.name === 'CurrentSunPosition') {
        const material = child.material as THREE.MeshBasicMaterial
        material.opacity += (targetOpacity * 0.5 - material.opacity) * 0.05
        
        // Pulso muy sutil
        const pulse = Math.sin(state.clock.elapsedTime * 1.5) * 0.08 + 1
        child.scale.setScalar(pulse)
      }
    })
  })
  
  return <group ref={groupRef} raycast={() => {}} />
}
