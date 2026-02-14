'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import { sunVertexShader, sunFragmentShader, coronaFragmentShader } from '@/shaders/sunShader'

/**
 * Sol - Plasma turbulento con fotosfera viva
 * 
 * CARACTERÍSTICAS NASA-STYLE:
 * - Noise fractal 3D animado
 * - Alto contraste (zonas oscuras + brillos intensos)
 * - Granulación visible
 * - Bordes irregulares
 * - Corona asimétrica
 * - Movimiento lento y turbulento
 * 
 * FOTOSFERA VIVA (NUEVO):
 * - 3 capas orgánicas con movimiento líquido
 * - Respiración asíncrona (cada capa con su propio ritmo)
 * - Rotación multi-eje independiente (X, Y, Z)
 * - Contra-rotación entre capas (efecto turbulento)
 * - Presión térmica contenida
 * - Piel energética que se expande y contrae
 * - Opacidad variable (simula flujo de plasma)
 * - Movimiento caótico natural (no sincronizado)
 * 
 * FILOSOFÍA:
 * - No llamaradas explosivas
 * - Sino presión térmica contenida
 * - Una estrella viva
 * - Fuego bajo tensión
 * 
 * ESCALA ARTÍSTICA:
 * - Tamaño: 15x el radio de la Tierra (comprimido del real 109x)
 * - Posición: Centro del sistema (0, 0, 0)
 * - Intensidad lumínica alta, escala visual moderada
 */
export default function Sun() {
  const sunCoreRef = useRef<THREE.Mesh>(null)
  const sunCoronaRef = useRef<THREE.Mesh>(null)
  const sunGlowRef = useRef<THREE.Mesh>(null)
  const photosphereLayer1Ref = useRef<THREE.Mesh>(null)
  const photosphereLayer2Ref = useRef<THREE.Mesh>(null)
  const photosphereLayer3Ref = useRef<THREE.Mesh>(null)
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
  
  // Animación - Turbulencia interna MUY lenta + Fotosfera orgánica
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
    
    // 🔥 FOTOSFERA VIVA - Capa 1: Movimiento líquido lento (rotación multi-eje)
    if (photosphereLayer1Ref.current) {
      const flow1 = Math.sin(time * 0.15) * 0.008 + 1.0
      const pulse1 = Math.sin(time * 0.12 + 1.2) * 0.006
      photosphereLayer1Ref.current.scale.setScalar(1.02 * flow1 + pulse1)
      
      // Rotación orgánica en múltiples ejes (como plasma turbulento)
      photosphereLayer1Ref.current.rotation.x += 0.00003
      photosphereLayer1Ref.current.rotation.y += 0.0001
      photosphereLayer1Ref.current.rotation.z += 0.00005
      
      // Opacidad respirando
      const material1 = photosphereLayer1Ref.current.material as THREE.MeshBasicMaterial
      material1.opacity = 0.15 + Math.sin(time * 0.18) * 0.05
    }
    
    // 🌊 FOTOSFERA VIVA - Capa 2: Presión térmica contenida (rotación inversa)
    if (photosphereLayer2Ref.current) {
      const flow2 = Math.sin(time * 0.11 + 2.5) * 0.012 + 1.0
      const pulse2 = Math.cos(time * 0.09) * 0.008
      photosphereLayer2Ref.current.scale.setScalar(1.05 * flow2 + pulse2)
      
      // Rotación caótica inversa (contra-rotación para efecto líquido)
      photosphereLayer2Ref.current.rotation.x -= 0.00004
      photosphereLayer2Ref.current.rotation.y -= 0.00008
      photosphereLayer2Ref.current.rotation.z += 0.00006
      
      // Opacidad respirando (desfasada)
      const material2 = photosphereLayer2Ref.current.material as THREE.MeshBasicMaterial
      material2.opacity = 0.12 + Math.cos(time * 0.14 + 1.5) * 0.04
    }
    
    // ✨ FOTOSFERA VIVA - Capa 3: Piel energética exterior (rotación diagonal)
    if (photosphereLayer3Ref.current) {
      const flow3 = Math.cos(time * 0.08 + 4.0) * 0.015 + 1.0
      const pulse3 = Math.sin(time * 0.13 + 3.0) * 0.01
      photosphereLayer3Ref.current.scale.setScalar(1.08 * flow3 + pulse3)
      
      // Rotación diagonal lenta (movimiento más complejo)
      photosphereLayer3Ref.current.rotation.x += 0.00007
      photosphereLayer3Ref.current.rotation.y += 0.00012
      photosphereLayer3Ref.current.rotation.z -= 0.00004
      
      // Opacidad respirando (más sutil)
      const material3 = photosphereLayer3Ref.current.material as THREE.MeshBasicMaterial
      material3.opacity = 0.08 + Math.sin(time * 0.1 + 2.8) * 0.03
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
      
      {/* 2️⃣ FOTOSFERA VIVA - Capa 1: Movimiento líquido (casi pegada) */}
      <mesh ref={photosphereLayer1Ref} scale={1.02}>
        <sphereGeometry args={[sunRadius, 128, 128]} />
        <meshBasicMaterial
          color="#ffcc44"
          transparent
          opacity={0.15}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.FrontSide}
        />
      </mesh>
      
      {/* 3️⃣ FOTOSFERA VIVA - Capa 2: Presión térmica contenida */}
      <mesh ref={photosphereLayer2Ref} scale={1.05}>
        <sphereGeometry args={[sunRadius, 96, 96]} />
        <meshBasicMaterial
          color="#ffaa33"
          transparent
          opacity={0.12}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.FrontSide}
        />
      </mesh>
      
      {/* 4️⃣ FOTOSFERA VIVA - Capa 3: Piel energética exterior */}
      <mesh ref={photosphereLayer3Ref} scale={1.08}>
        <sphereGeometry args={[sunRadius, 64, 64]} />
        <meshBasicMaterial
          color="#ff9922"
          transparent
          opacity={0.08}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* 5️⃣ CORONA IRREGULAR - Borde violento con erupciones */}
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
      
      {/* 6️⃣ GLOW INTENSO - Fuego exterior */}
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
      
      {/* 7️⃣ LUZ DIRECCIONAL - Fuente de luz real */}
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
      
      {/* 8️⃣ LUZ PUNTUAL - Iluminación ambiental */}
      <pointLight
        color="#ffaa55"
        intensity={0.64}
        distance={400}
        decay={2}
      />
    </group>
  )
}
