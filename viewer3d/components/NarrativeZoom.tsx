'use client'

import { useRef, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * Sistema de Zoom Narrativo con Escalas Segmentadas
 * 
 * FILOSOFÍA:
 * No es un simple alejamiento de cámara.
 * Es una revelación progresiva del cosmos.
 * Cada nivel tiene su propia escala coherente.
 * 
 * NIVELES:
 * 0 - Mundo: Solo Tierra y Luna (escala planetaria)
 * 1 - Contexto Orbital: Órbita lunar visible, plano orbital sutil
 * 2 - Aparición Solar: Sol distante, órbita terrestre, plano eclíptico
 * 3 - Sistema Interno: Venus y Marte (si están cerca angularmente)
 * 
 * ESCALAS SEGMENTADAS:
 * - Modo Planetario: Tierra-Luna (0-50 unidades de cámara)
 * - Transición: Interpolación suave (50-100 unidades)
 * - Modo Solar: Sistema interno (100+ unidades)
 */

export type ZoomLevel = 'mundo' | 'orbital' | 'solar' | 'sistema'
export type ScaleMode = 'planetary' | 'transition' | 'solar'

interface NarrativeZoomState {
  level: ZoomLevel
  scaleMode: ScaleMode
  progress: number // 0-1 dentro del nivel actual
  cameraDistance: number
  transitionFactor: number // 0-1 para interpolación de escalas
}

export function useNarrativeZoom(): NarrativeZoomState {
  const { camera } = useThree()
  const stateRef = useRef<NarrativeZoomState>({
    level: 'mundo',
    scaleMode: 'planetary',
    progress: 0,
    cameraDistance: 0,
    transitionFactor: 0
  })
  
  useFrame(() => {
    // Calcular distancia de cámara desde origen
    const distance = camera.position.length()
    stateRef.current.cameraDistance = distance
    
    // Determinar nivel y modo según distancia
    // AJUSTADO para sistema híbrido (Tierra a 100 del Sol)
    if (distance < 50) {
      // Nivel 0: Mundo (escala planetaria pura)
      stateRef.current.level = 'mundo'
      stateRef.current.scaleMode = 'planetary'
      stateRef.current.progress = distance / 50
      stateRef.current.transitionFactor = 0
    } else if (distance < 100) {
      // Nivel 1: Contexto Orbital (transición de escala)
      stateRef.current.level = 'orbital'
      stateRef.current.scaleMode = 'transition'
      stateRef.current.progress = (distance - 50) / 50
      stateRef.current.transitionFactor = stateRef.current.progress
    } else if (distance < 200) {
      // Nivel 2: Aparición Solar (escala solar)
      stateRef.current.level = 'solar'
      stateRef.current.scaleMode = 'solar'
      stateRef.current.progress = (distance - 100) / 100
      stateRef.current.transitionFactor = 1
    } else {
      // Nivel 3: Sistema Interno (escala solar expandida)
      stateRef.current.level = 'sistema'
      stateRef.current.scaleMode = 'solar'
      stateRef.current.progress = Math.min((distance - 200) / 100, 1)
      stateRef.current.transitionFactor = 1
    }
  })
  
  return stateRef.current
}

/**
 * Plano Orbital - Disco sutil que aparece en nivel orbital
 */
export function OrbitalPlane({ visible, radius = 15 }: { visible: boolean, radius?: number }) {
  const planeRef = useRef<THREE.Mesh>(null)
  
  useFrame(() => {
    if (planeRef.current) {
      const targetOpacity = visible ? 0.03 : 0
      const currentOpacity = (planeRef.current.material as THREE.MeshBasicMaterial).opacity
      const newOpacity = THREE.MathUtils.lerp(currentOpacity, targetOpacity, 0.03)
      ;(planeRef.current.material as THREE.MeshBasicMaterial).opacity = newOpacity
      
      // Rotación muy lenta para dar sensación de movimiento
      planeRef.current.rotation.z += 0.0001
    }
  })
  
  return (
    <mesh ref={planeRef} rotation={[-Math.PI / 2, 0, 0]}>
      <ringGeometry args={[radius * 0.5, radius, 64]} />
      <meshBasicMaterial
        color="#2a4a6a"
        transparent
        opacity={0}
        side={THREE.DoubleSide}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </mesh>
  )
}
