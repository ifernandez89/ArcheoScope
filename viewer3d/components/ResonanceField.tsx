/**
 * ResonanceField - Campo de resonancia visible
 * Muestra visualmente una zona de anomalía
 */

'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface ResonanceFieldProps {
  position: [number, number, number]
  radius: number
  intensity: number
  color?: string
  type?: 'gravity' | 'mass' | 'spatial' | 'temporal'
}

export default function ResonanceField({
  position,
  radius,
  intensity,
  color = '#4a9eff',
  type = 'spatial'
}: ResonanceFieldProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  const innerMeshRef = useRef<THREE.Mesh>(null)
  
  // Colores según tipo de anomalía
  const typeColors = {
    gravity: '#9d4edd',    // Púrpura
    mass: '#ff6b6b',       // Rojo
    spatial: '#4a9eff',    // Azul
    temporal: '#06ffa5'    // Verde cyan
  }
  
  const fieldColor = typeColors[type] || color
  
  // Shader personalizado OPTIMIZADO - MÁS SIMPLE
  const fieldShader = useMemo(() => ({
    uniforms: {
      time: { value: 0 },
      intensity: { value: intensity },
      color: { value: new THREE.Color(fieldColor) }
    },
    vertexShader: `
      varying vec3 vNormal;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform float time;
      uniform float intensity;
      uniform vec3 color;
      
      varying vec3 vNormal;
      
      void main() {
        // Fresnel muy simple
        vec3 viewDirection = normalize(cameraPosition - vNormal);
        float fresnel = pow(1.0 - abs(dot(viewDirection, vNormal)), 1.5);
        
        // Pulsación simple
        float pulse = sin(time) * 0.15 + 0.85;
        
        vec3 finalColor = color * fresnel * pulse * intensity;
        float alpha = (fresnel * 0.4 + 0.1) * intensity;
        
        gl_FragColor = vec4(finalColor, alpha);
      }
    `
  }), [fieldColor, intensity])
  
  // Animación
  useFrame((state) => {
    if (meshRef.current) {
      const material = meshRef.current.material as THREE.ShaderMaterial
      material.uniforms.time.value = state.clock.elapsedTime
      
      // Rotación sutil
      meshRef.current.rotation.y += 0.001
    }
    
    if (innerMeshRef.current) {
      // Núcleo pulsante
      const scale = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1
      innerMeshRef.current.scale.setScalar(scale)
      innerMeshRef.current.rotation.y -= 0.002
    }
  })
  
  return (
    <group position={position}>
      {/* Campo exterior (esfera transparente) - MUY OPTIMIZADO */}
      <mesh ref={meshRef}>
        <sphereGeometry args={[radius, 16, 16]} />
        <shaderMaterial
          vertexShader={fieldShader.vertexShader}
          fragmentShader={fieldShader.fragmentShader}
          uniforms={fieldShader.uniforms}
          transparent
          side={THREE.FrontSide}
          depthWrite={false}
        />
      </mesh>
      
      {/* Núcleo interior - MÁS SIMPLE */}
      <mesh ref={innerMeshRef}>
        <sphereGeometry args={[radius * 0.08, 6, 6]} />
        <meshBasicMaterial
          color={fieldColor}
          transparent
          opacity={0.6}
        />
      </mesh>
      
      {/* Solo 1 anillo */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[radius * 0.7, radius * 0.01, 6, 24]} />
        <meshBasicMaterial
          color={fieldColor}
          transparent
          opacity={0.25}
        />
      </mesh>
    </group>
  )
}
