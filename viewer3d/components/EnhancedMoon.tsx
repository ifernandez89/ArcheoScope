'use client'

/**
 * EnhancedMoon - Luna mejorada con fases y eclipses
 * Integrada con nuestro sistema lunar avanzado y optimizaciones para mobile
 */

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface EnhancedMoonProps {
  lunarState?: {
    phase: string
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
  const halo1Ref = useRef<THREE.Mesh>(null)
  const halo2Ref = useRef<THREE.Mesh>(null)
  
  const moonTexture = useTexture(getAssetPath('/textures/2k_moon.jpg'))
  
  const { position, scale, sunDir } = useMemo(() => {
    const sDir = new THREE.Vector3(solarDirection.x, solarDirection.y, solarDirection.z).normalize()
    
    if (!lunarState) {
      return { 
        position: new THREE.Vector3(30, 10, 30), 
        scale: 1, 
        sunDir: sDir
      }
    }
    
    const pos = new THREE.Vector3(
      lunarState.position.x * 50,
      lunarState.position.y * 50 + 15,
      lunarState.position.z * 50
    )
    
    const baseScale = 2
    const sizeScale = baseScale * (lunarState.angularSize / 0.5)
    
    return { position: pos, scale: sizeScale, sunDir: sDir }
  }, [lunarState, solarDirection])
  
  // Shader de Luna con Terminador Realista
  const moonMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        moonTexture: { value: moonTexture },
        sunDirection: { value: sunDir },
        eclipseMagnitude: { value: eclipse?.magnitude || 0 },
        time: { value: 0 }
      },
      vertexShader: `
        varying vec2 vUv;
        varying vec3 vNormal;
        varying vec3 vViewPosition;
        varying vec3 vWorldNormal;
        
        void main() {
          vUv = uv;
          vNormal = normalize(normalMatrix * normal);
          vWorldNormal = normalize((modelMatrix * vec4(normal, 0.0)).xyz);
          vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
          vViewPosition = -mvPosition.xyz;
          gl_Position = projectionMatrix * mvPosition;
        }
      `,
      fragmentShader: `
        uniform sampler2D moonTexture;
        uniform vec3 sunDirection;
        uniform float eclipseMagnitude;
        uniform float time;
        
        varying vec2 vUv;
        varying vec3 vNormal;
        varying vec3 vWorldNormal;
        
        void main() {
          vec4 texColor = texture2D(moonTexture, vUv);
          
          // Terminador realista: dot product entre normal de la superficie y dirección del sol
          // Invertimos sunDirection porque es la dirección HACIA el sol
          float NdotL = dot(vWorldNormal, sunDirection);
          
          // Suavizado del terminador para realismo
          float terminator = smoothstep(-0.05, 0.05, NdotL);
          
          // Luz cenicienta (Earthshine) - luz sutil en la parte oscura
          float earthshine = 0.05;
          float finalLighting = max(terminator, earthshine);
          
          vec3 finalColor = texColor.rgb * finalLighting;
          
          // Efecto de Eclipse Lunar
          if (eclipseMagnitude > 0.0) {
            vec3 bloodMoon = vec3(0.6, 0.2, 0.1);
            finalColor = mix(finalColor, finalColor * bloodMoon * 2.0, eclipseMagnitude);
          }
          
          gl_FragColor = vec4(finalColor, 1.0);
        }
      `
    })
  }, [moonTexture, sunDir, eclipse?.magnitude])

  // Shader para Halo Lunar (Dispersión Atmosférica)
  const createHaloMaterial = (opacity: number) => {
    return new THREE.ShaderMaterial({
      uniforms: {
        color: { value: new THREE.Color('#ffffff') },
        opacity: { value: opacity }
      },
      vertexShader: `
        varying vec3 vNormal;
        void main() {
          vNormal = normalize(normalMatrix * normal);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        varying vec3 vNormal;
        uniform vec3 color;
        uniform float opacity;
        void main() {
          float intensity = pow(0.6 - dot(vNormal, vec3(0, 0, 1.0)), 2.0);
          gl_FragColor = vec4(color, intensity * opacity);
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending,
      side: THREE.BackSide,
      depthWrite: false
    })
  }

  const halo1Mat = useMemo(() => createHaloMaterial(0.06), [])
  const halo2Mat = useMemo(() => createHaloMaterial(0.03), [])

  useFrame((state) => {
    if (moonMaterial.uniforms) {
      moonMaterial.uniforms.time.value = state.clock.elapsedTime
      moonMaterial.uniforms.sunDirection.value.copy(sunDir)
    }
    // Orientar halos hacia la cámara
    if (halo1Ref.current) halo1Ref.current.lookAt(state.camera.position)
    if (halo2Ref.current) halo2Ref.current.lookAt(state.camera.position)
  })
  
  if (!visible || !lunarState) return null
  
  return (
    <group position={position} scale={scale}>
      {/* Cuerpo Lunar */}
      <mesh ref={moonRef} material={moonMaterial}>
        <sphereGeometry args={[1, 64, 64]} />
      </mesh>
      
      {/* Halo Lunar Capa 1 (Cercana) */}
      <mesh ref={halo1Ref} scale={1.2}>
        <planeGeometry args={[2.5, 2.5]} />
        <primitive object={halo1Mat} attach="material" />
      </mesh>
      
      {/* Halo Lunar Capa 2 (Extendida) */}
      <mesh ref={halo2Ref} scale={1.5}>
        <planeGeometry args={[3, 3]} />
        <primitive object={halo2Mat} attach="material" />
      </mesh>
    </group>
  )
}