'use client'

/**
 * EnhancedMoon - Luna mejorada con fases y eclipses
 * Integrada con nuestro sistema lunar avanzado
 */

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface EnhancedMoonProps {
  lunarState?: {
    phase: 'new' | 'waxing_crescent' | 'first_quarter' | 'waxing_gibbous' | 
           'full' | 'waning_gibbous' | 'last_quarter' | 'waning_crescent'
    illumination: number // 0-1
    position: { x: number, y: number, z: number }
    angularSize: number // grados
  }
  eclipse?: {
    type: 'solar' | 'lunar'
    magnitude: number
    phase: 'beginning' | 'maximum' | 'ending' | 'none'
  }
  solarDirection: { x: number, y: number, z: number }
  visible?: boolean
}

export default function EnhancedMoon({ 
  lunarState, 
  eclipse, 
  solarDirection,
  visible = true 
}: EnhancedMoonProps) {
  const moonRef = useRef<THREE.Mesh>(null)
  const moonTexture = useTexture(getAssetPath('/textures/2k_moon.jpg'))
  
  // Calcular posición y tamaño de la luna
  const { position, scale, color } = useMemo(() => {
    if (!lunarState) {
      return { 
        position: [30, 10, 30] as [number, number, number], 
        scale: 1, 
        color: '#ffffff' 
      }
    }
    
    // Posición escalada para visualización
    const pos: [number, number, number] = [
      lunarState.position.x * 50,
      lunarState.position.y * 50 + 15, // Elevar un poco
      lunarState.position.z * 50
    ]
    
    // Tamaño basado en distancia (tamaño angular)
    const baseScale = 2
    const sizeScale = baseScale * (lunarState.angularSize / 0.5) // 0.5° es el tamaño promedio
    
    // Color según eclipse
    let moonColor = '#ffffff'
    if (eclipse && eclipse.type === 'lunar' && eclipse.magnitude > 0) {
      // Eclipse lunar - luna rojiza
      const redness = Math.min(eclipse.magnitude, 1)
      moonColor = `rgb(${255}, ${Math.floor(255 * (1 - redness * 0.7))}, ${Math.floor(255 * (1 - redness * 0.8))})`
    }
    
    return { position: pos, scale: sizeScale, color: moonColor }
  }, [lunarState, eclipse])
  
  // Shader para fases lunares
  const moonMaterial = useMemo(() => {
    const illumination = lunarState?.illumination || 0.5
    
    return new THREE.ShaderMaterial({
      uniforms: {
        moonTexture: { value: moonTexture },
        illumination: { value: illumination },
        sunDirection: { value: new THREE.Vector3(solarDirection.x, solarDirection.y, solarDirection.z) },
        eclipseMagnitude: { value: eclipse?.magnitude || 0 },
        time: { value: 0 }
      },
      vertexShader: `
        varying vec2 vUv;
        varying vec3 vNormal;
        varying vec3 vPosition;
        
        void main() {
          vUv = uv;
          vNormal = normalize(normalMatrix * normal);
          vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform sampler2D moonTexture;
        uniform float illumination;
        uniform vec3 sunDirection;
        uniform float eclipseMagnitude;
        uniform float time;
        
        varying vec2 vUv;
        varying vec3 vNormal;
        varying vec3 vPosition;
        
        void main() {
          vec4 moonColor = texture2D(moonTexture, vUv);
          
          // Calcular iluminación de fase lunar
          float phase = illumination;
          float terminator = (vUv.x - 0.5) * 2.0; // -1 a 1
          float phaseEdge = (phase - 0.5) * 2.0; // -1 a 1
          
          float brightness = 1.0;
          if (phase < 0.5) {
            // Fases menguantes
            brightness = step(terminator, phaseEdge);
          } else {
            // Fases crecientes
            brightness = step(phaseEdge, terminator);
          }
          
          // Eclipse lunar
          if (eclipseMagnitude > 0.0) {
            float eclipseEffect = 1.0 - eclipseMagnitude * 0.8;
            brightness *= eclipseEffect;
            // Tinte rojizo durante eclipse
            moonColor.r *= 1.0 + eclipseMagnitude * 0.3;
            moonColor.g *= 1.0 - eclipseMagnitude * 0.4;
            moonColor.b *= 1.0 - eclipseMagnitude * 0.5;
          }
          
          // Brillo sutil
          float glow = 1.0 + sin(time * 2.0) * 0.1;
          
          gl_FragColor = vec4(moonColor.rgb * brightness * glow, moonColor.a);
        }
      `,
      transparent: true
    })
  }, [moonTexture, lunarState?.illumination, solarDirection, eclipse?.magnitude])
  
  // Actualizar uniforms
  useFrame((state) => {
    if (moonMaterial.uniforms) {
      moonMaterial.uniforms.time.value = state.clock.elapsedTime
      moonMaterial.uniforms.illumination.value = lunarState?.illumination || 0.5
      moonMaterial.uniforms.eclipseMagnitude.value = eclipse?.magnitude || 0
    }
  })
  
  if (!visible || !lunarState) return null
  
  return (
    <mesh
      ref={moonRef}
      position={position}
      scale={scale}
      material={moonMaterial}
    >
      <sphereGeometry args={[1, 32, 32]} />
    </mesh>
  )
}