'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import { sunVertexShader, sunFragmentShader, coronaFragmentShader } from '@/shaders/sunShader'

/**
 * Sol - Plasma turbulento con estructura procedural
 * 
 * CARACTERÍSTICAS NASA-STYLE:
 * - Noise fractal 3D animado
 * - Alto contraste (zonas oscuras + brillos intensos)
 * - Granulación visible
 * - Bordes irregulares
 * - Corona asimétrica
 * - Movimiento lento y turbulento
 * 
 * ESCALA ARTÍSTICA:
 * - Tamaño: 4x el diámetro de la Tierra (reducido para no invadir)
 * - Distancia: 35x el diámetro terrestre
 * - Intensidad lumínica alta, escala visual moderada
 */
export default function Sun() {
  const sunCoreRef = useRef<THREE.Mesh>(null)
  const sunCoronaRef = useRef<THREE.Mesh>(null)
  const sunGlowRef = useRef<THREE.Mesh>(null)
  const directionalLightRef = useRef<THREE.DirectionalLight>(null)
  
  // Cargar textura del Sol
  const sunTexture = useTexture(getAssetPath('/textures/8k_sun.jpg'), (texture) => {
    console.log('☀️ Textura del Sol cargada')
  })
  
  // SISTEMA HÍBRIDO PROFESIONAL - SOL EN EL CENTRO
  // Sol en el origen (0,0,0)
  // Tierra orbita a 100 unidades del Sol
  const earthRadius = 1
  const sunRadius = earthRadius * 15      // Comprimido (real sería 109)
  
  // Posición del Sol - EN EL CENTRO
  const sunPosition: [number, number, number] = [0, 0, 0]
  
  // Uniforms para shaders
  const sunUniforms = useMemo(() => ({
    sunTexture: { value: sunTexture },
    time: { value: 0 },
    intensity: { value: 1.5 }
  }), [sunTexture])
  
  const coronaUniforms = useMemo(() => ({
    time: { value: 0 },
    opacity: { value: 0.125 } // Mitad de 0.25
  }), [])
  
  // Animación - Turbulencia interna MUY lenta
  useFrame((state) => {
    const time = state.clock.elapsedTime
    
    // Actualizar uniforms de tiempo
    sunUniforms.time.value = time
    coronaUniforms.time.value = time
    
    // Rotación casi imperceptible del núcleo (masivo y pesado)
    if (sunCoreRef.current) {
      sunCoreRef.current.rotation.y += 0.00005 // Más lento
    }
    
    // Corona "respirando" muy sutilmente (erupciones)
    if (sunCoronaRef.current) {
      const breathe = Math.sin(time * 0.08) * 0.015 + 1.0
      sunCoronaRef.current.scale.setScalar(1.15 * breathe)
    }
    
    // Actualizar luz direccional
    if (directionalLightRef.current) {
      directionalLightRef.current.position.copy(new THREE.Vector3(...sunPosition))
      directionalLightRef.current.target.position.set(0, 0, 0)
      directionalLightRef.current.target.updateMatrixWorld()
    }
  })
  
  return (
    <group position={sunPosition}>
      {/* 1️⃣ NÚCLEO - Shader procedural con protuberancias */}
      <mesh ref={sunCoreRef}>
        <sphereGeometry args={[sunRadius, 256, 256]} />
        <shaderMaterial
          vertexShader={sunVertexShader}
          fragmentShader={sunFragmentShader}
          uniforms={{
            ...sunUniforms,
            time: sunUniforms.time
          }}
          side={THREE.FrontSide}
        />
      </mesh>
      
      {/* 2️⃣ CORONA IRREGULAR - Borde violento con erupciones */}
      <mesh ref={sunCoronaRef} scale={1.15}>
        <sphereGeometry args={[sunRadius, 64, 64]} />
        <shaderMaterial
          vertexShader={sunVertexShader}
          fragmentShader={coronaFragmentShader}
          uniforms={{
            time: coronaUniforms.time,
            opacity: { value: 0.08 }
          }}
          transparent
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* 3️⃣ GLOW INTENSO - Fuego exterior */}
      <mesh ref={sunGlowRef} scale={1.35}>
        <sphereGeometry args={[sunRadius, 32, 32]} />
        <meshBasicMaterial
          color="#ff9933"
          transparent
          opacity={0.05}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* 4️⃣ LUZ DIRECCIONAL - Fuente de luz real */}
      <directionalLight
        ref={directionalLightRef}
        color="#fff8e7"
        intensity={0.96}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={250}
        shadow-camera-left={-60}
        shadow-camera-right={60}
        shadow-camera-top={60}
        shadow-camera-bottom={-60}
      />
      
      {/* 5️⃣ LUZ PUNTUAL - Iluminación ambiental */}
      <pointLight
        color="#ffaa55"
        intensity={0.64}
        distance={400}
        decay={2}
      />
    </group>
  )
}
