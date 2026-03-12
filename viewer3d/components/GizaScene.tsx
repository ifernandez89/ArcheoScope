'use client'

import { useMemo, useState, useRef, useEffect, useCallback } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useGLTF } from '@react-three/drei'
import { getAssetPath } from '@/lib/paths'

interface GizaSceneProps {
  avatarPositionRef: React.MutableRefObject<THREE.Vector3>
  onSphinxClick?: () => void
  onPyramidionCollect?: () => void
  pyramidionCollected?: boolean
  pyramidionOnTop?: boolean
}

/**
 * 🏜️ Escena de Giza - Gran Pirámide y Esfinge
 * 
 * Características astronómicas reales:
 * - Alineación cardinal casi perfecta (~0.05° de error)
 * - Cada cara mira exactamente: Norte, Sur, Este, Oeste
 * - Orientación basada en observaciones estelares de 2500 a.C.
 * 
 * Escala adaptada para juego:
 * - Gran Pirámide (Keops): 138m base × 88m altura (60% escala real)
 * - Esfinge: 73m largo × 20m alto (escala real)
 * 
 * Ambiente desértico realista:
 * - Arena color ocre/beige (#d9c8a3, #cdb68e, #bfa77f)
 * - Dunas suaves con ruido Perlin
 * - Niebla amarillenta atmosférica
 * - Piedras dispersas
 */
export default function GizaScene({ avatarPositionRef, onSphinxClick, onPyramidionCollect, pyramidionCollected, pyramidionOnTop }: GizaSceneProps) {
  console.log('🔶 GizaScene RENDER - pyramidionCollected:', pyramidionCollected, 'pyramidionOnTop:', pyramidionOnTop)
  
  return (
    <group name="giza-complex">
        {/* 🌫️ Niebla desértica amarillenta */}
        <fog attach="fog" args={['#e8d5b7', 50, 400]} />
        
        {/* 🏜️ Terreno desértico con dunas suaves */}
        <DesertTerrain />
        
        {/* 🔺 Gran Pirámide de Keops (Khufu) - CON PUNTA PLANA */}
        <GreatPyramid 
          position={[0, 0, 0]}
          rotation={[0, Math.PI / 4, 0]} // Rotación 45° para alinear caras con cardinales
          pyramidionCollected={pyramidionOnTop || false}
        />
        
        {/* 🔶 Piramidión - Frente a la esfinge (50cm delante) */}
        {!pyramidionCollected && (
          <>
            {/* Piramidón flotante en la punta de la pirámide - INVISIBLE */}
            <Pyramidion 
              position={[0, 44, 0]} // En la punta de la pirámide (altura 44m)
              rotation={[0, 0, 0]}
              onCollect={undefined} // NO clickeable
              opacity={0}
            />
            {/* Piramidón en el suelo */}
            <Pyramidion 
              position={[100, 0, 35]} // 15m delante de la esfinge, en el suelo
              rotation={[0, 0, 0]}
              onCollect={onPyramidionCollect}
            />
          </>
        )}
        
        {/* 🔶 Piramidón en la punta - VISIBLE después de entregarlo a la Esfinge */}
        {pyramidionOnTop && (
          <Pyramidion 
            position={[0, 44, 0]} // En la punta de la pirámide
            rotation={[0, 0, 0]}
            onCollect={undefined} // NO clickeable
            opacity={1}
          />
        )}
        
        {/* 🦁 La Gran Esfinge - Al este de la pirámide, mirando al Este */}
        <Sphinx 
          position={[100, 5, 50]}
          rotation={[0, Math.PI / 2, 0]} // Mira hacia el Este (salida del sol)
          onClick={onSphinxClick}
        />
        
        {/* 🏛️ Templo del Valle de Kefrén - Debajo de la pirámide */}
        <ValleyTemple 
          position={[0, -5, 0]} // Justo debajo de la pirámide, 5m bajo la arena
        />
        
        {/* 🪨 Piedras dispersas del desierto */}
        <DesertRocks />
      </group>
  )
}

/**
 * 🔺 Gran Pirámide de Keops - CON PUNTA PLANA
 * La más grande y precisa - Actualmente sin piramidón
 */
function GreatPyramid({ position, rotation, pyramidionCollected }: { 
  position: [number, number, number]
  rotation: [number, number, number]
  pyramidionCollected: boolean
}) {
  const baseSize = 69 // Reducido a la mitad (30% de 230m real)
  const height = 44 // Reducido a la mitad (30% de 146m real)
  const topSize = 4 // Reducido a la mitad - Tamaño de la plataforma superior (punta plana)
  
  // Geometría de tronco de pirámide (pirámide con punta cortada)
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    
    // Vértices del tronco de pirámide
    const halfBase = baseSize / 2
    const halfTop = topSize / 2
    
    // 8 vértices: 4 en la base, 4 en la parte superior
    const vertices = new Float32Array([
      // Base (y = 0)
      -halfBase, 0, -halfBase,  // 0
       halfBase, 0, -halfBase,  // 1
       halfBase, 0,  halfBase,  // 2
      -halfBase, 0,  halfBase,  // 3
      
      // Top (y = height)
      -halfTop, height, -halfTop,  // 4
       halfTop, height, -halfTop,  // 5
       halfTop, height,  halfTop,  // 6
      -halfTop, height,  halfTop,  // 7
    ])
    
    // Índices para las caras (triángulos)
    const indices = new Uint16Array([
      // Base (mirando hacia abajo)
      0, 2, 1,  0, 3, 2,
      
      // Top (mirando hacia arriba)
      4, 5, 6,  4, 6, 7,
      
      // Cara Norte (frente)
      0, 1, 5,  0, 5, 4,
      
      // Cara Este (derecha)
      1, 2, 6,  1, 6, 5,
      
      // Cara Sur (atrás)
      2, 3, 7,  2, 7, 6,
      
      // Cara Oeste (izquierda)
      3, 0, 4,  3, 4, 7,
    ])
    
    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    geo.setIndex(new THREE.BufferAttribute(indices, 1))
    geo.computeVertexNormals()
    
    // Rotar para alinear caras con cardinales
    geo.rotateY(Math.PI / 4)
    
    return geo
  }, [baseSize, height, topSize])
  
  return (
    <group position={position} rotation={rotation}>
      <mesh geometry={geometry} castShadow receiveShadow>
        <meshStandardMaterial
          color="#d4a574" // Caliza amarillenta (núcleo expuesto)
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>
      
      {/* 🔶 Piramidón en la punta - Solo visible si fue recolectado */}
      {pyramidionCollected && (
        <Pyramidion 
          position={[0, height, 0]} // En la punta de la pirámide
          rotation={[0, 0, 0]}
          onCollect={undefined} // No clickeable cuando está en la pirámide
        />
      )}
    </group>
  )
}

/**
 * 🦁 La Gran Esfinge
 * Dimensiones reales: 73m largo × 20m alto × 19m ancho
 * Tallada en roca caliza natural
 * Mira hacia el Este (salida del sol en equinoccio)
 */
function Sphinx({ position, rotation, onClick }: { position: [number, number, number], rotation: [number, number, number], onClick?: () => void }) {
  const { scene } = useGLTF(getAssetPath('/sphinx_base.glb'))
  
  // Clonar la escena para evitar problemas de reutilización
  const clonedScene = useMemo(() => scene.clone(), [scene])
  
  // La Esfinge real mide 73m de largo × 20m de alto
  // Escala proporcional a la pirámide (60% escala real)
  // Escala del modelo: ajustar según el tamaño del .glb original
  const scale = 20 // Ajustar según necesidad
  
  return (
    <group position={position} rotation={rotation} onClick={onClick} onPointerOver={() => document.body.style.cursor = 'pointer'} onPointerOut={() => document.body.style.cursor = 'default'}>
      <primitive 
        object={clonedScene}
        scale={[scale, scale, scale]}
        castShadow
        receiveShadow
      />
    </group>
  )
}

// Precargar modelo
useGLTF.preload(getAssetPath('/sphinx_base.glb'))

/**
 * 🔶 Piramidón - Capstone de la Gran Pirámide
 * Objeto seleccionable en el piso, al costado de la pirámide
 * Modelo: piramidon.glb
 */
function Pyramidion({ position, rotation, onCollect, opacity = 1 }: { 
  position: [number, number, number]
  rotation: [number, number, number]
  onCollect?: () => void
  opacity?: number
}) {
  const { scene } = useGLTF(getAssetPath('/piramidon.glb'))
  const [isHovered, setIsHovered] = useState(false)
  const [isDisappearing, setIsDisappearing] = useState(false)
  const disappearTimer = useRef(0)
  
  // Clonar la escena para evitar problemas de reutilización
  const clonedScene = useMemo(() => scene.clone(), [scene])
  
  // Aplicar opacidad inicial
  useEffect(() => {
    clonedScene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        if (mesh.material) {
          // Clonar el material para evitar afectar otras instancias
          const material = (mesh.material as THREE.MeshStandardMaterial).clone()
          material.transparent = true
          material.opacity = opacity
          material.needsUpdate = true
          mesh.material = material
        }
      }
    })
  }, [clonedScene, opacity])
  
  // Escala del piramidón - Aumentado al doble
  const scale = 4 // Duplicado de 2 a 4
  
  // Calcular el offset Y para que la base esté exactamente en el suelo
  const yOffset = useMemo(() => {
    const box = new THREE.Box3().setFromObject(clonedScene)
    const minY = box.min.y
    // Retornar el offset necesario para que minY * scale esté en 0
    return -minY * scale
  }, [clonedScene, scale])
  
  // Animación de desaparición
  useFrame((state, delta) => {
    if (isDisappearing && clonedScene) {
      disappearTimer.current += delta
      
      // Fade out y escala hacia arriba
      const progress = Math.min(disappearTimer.current / 1.0, 1) // 1 segundo
      clonedScene.scale.setScalar(scale * (1 + progress * 0.5)) // Crece un poco
      
      // Fade out de todos los materiales
      clonedScene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh
          if (mesh.material) {
            const material = mesh.material as THREE.MeshStandardMaterial
            material.transparent = true
            material.opacity = 1 - progress
          }
        }
      })
      
      // Llamar callback cuando termine
      if (progress >= 1 && onCollect) {
        onCollect()
      }
    }
  })
  
  const handleClick = (e: any) => {
    if (onCollect && !isDisappearing) {
      e.stopPropagation()
      setIsDisappearing(true)
      console.log('🔶 Piramidón recogido! Desapareciendo...')
    }
  }
  
  return (
    <group 
      position={[position[0], position[1] + yOffset, position[2]]} 
      rotation={rotation}
      onClick={handleClick}
      onPointerOver={() => onCollect && !isDisappearing && setIsHovered(true)}
      onPointerOut={() => setIsHovered(false)}
    >
      <primitive 
        object={clonedScene}
        scale={[scale, scale, scale]}
        castShadow
        receiveShadow
      />
      
      {/* Outline cuando está hover */}
      {isHovered && onCollect && !isDisappearing && (
        <mesh>
          <sphereGeometry args={[2, 16, 16]} />
          <meshBasicMaterial
            color="#ffff00"
            wireframe
            transparent
            opacity={0.3}
          />
        </mesh>
      )}
    </group>
  )
}

// Precargar modelo del piramidón
useGLTF.preload(getAssetPath('/piramidon.glb'))

/**
 * 🏜️ Terreno desértico con dunas suaves
 * Usa ruido Perlin para generar ondulaciones naturales
 */
function DesertTerrain() {
  const geometry = useMemo(() => {
    const size = 500 // Tamaño del terreno
    const segments = 100 // Resolución
    const geo = new THREE.PlaneGeometry(size, size, segments, segments)
    
    // Aplicar ruido Perlin para dunas suaves
    const positions = geo.attributes.position
    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i)
      const z = positions.getY(i) // En PlaneGeometry, Y es Z en el mundo
      
      // Ruido Perlin simplificado (ondulaciones suaves)
      const noise1 = Math.sin(x * 0.002) * Math.cos(z * 0.002) * 2
      const noise2 = Math.sin(x * 0.005 + 10) * Math.cos(z * 0.005 + 10) * 1
      const noise3 = Math.sin(x * 0.01 + 20) * Math.cos(z * 0.01 + 20) * 0.5
      
      const height = noise1 + noise2 + noise3
      positions.setZ(i, height)
    }
    
    geo.computeVertexNormals()
    geo.rotateX(-Math.PI / 2) // Horizontal
    return geo
  }, [])
  
  return (
    <mesh geometry={geometry} receiveShadow position={[0, -0.5, 0]}>
      <meshStandardMaterial
        color="#d9c8a3" // Arena ocre/beige real de Giza
        roughness={0.95}
        metalness={0.05}
      />
    </mesh>
  )
}

/**
 * 🪨 Piedras dispersas del desierto
 * Pequeñas rocas distribuidas aleatoriamente
 */
function DesertRocks() {
  const rocks = useMemo(() => {
    const rockArray: JSX.Element[] = []
    const rockCount = 30 // Pocas piedras, realista
    
    for (let i = 0; i < rockCount; i++) {
      // Distribución aleatoria pero no cerca de la pirámide
      const angle = Math.random() * Math.PI * 2
      const distance = 80 + Math.random() * 150 // Entre 80m y 230m de distancia
      const x = Math.cos(angle) * distance
      const z = Math.sin(angle) * distance
      
      // Tamaño variable de rocas
      const size = 0.5 + Math.random() * 2
      const height = size * (0.5 + Math.random() * 0.5)
      
      rockArray.push(
        <mesh
          key={i}
          position={[x, height / 2, z]}
          rotation={[
            Math.random() * 0.3,
            Math.random() * Math.PI * 2,
            Math.random() * 0.3
          ]}
          castShadow
        >
          <boxGeometry args={[size, height, size * 0.8]} />
          <meshStandardMaterial
            color={new THREE.Color().setHSL(0.08, 0.15, 0.4 + Math.random() * 0.2)}
            roughness={0.9}
          />
        </mesh>
      )
    }
    
    return rockArray
  }, [])
  
  return <>{rocks}</>
}

/**
 * 🏛️ Templo del Valle de Kefrén
 * Estructura megalítica junto a la Esfinge
 * Construido proceduralmente con geometría básica
 * 
 * Dimensiones: 30m × 30m × 8m altura
 * Materiales: Granito oscuro (muros), Alabastro (piso)
 * Arquitectura: Planta cuadrada con sala de columnas
 */
function ValleyTemple({ position }: { position: [number, number, number] }) {
  return (
    <group position={position}>
      {/* 🏺 Piso de alabastro (blanco crema) */}
      <mesh position={[0, 0.25, 0]} receiveShadow>
        <boxGeometry args={[30, 0.5, 30]} />
        <meshStandardMaterial
          color="#f5f5dc" // Alabastro blanco crema
          roughness={0.3}
          metalness={0.1}
        />
      </mesh>
      
      {/* 🧱 Muros exteriores de granito oscuro */}
      {/* Muro Norte */}
      <mesh position={[0, 4, -15]} castShadow receiveShadow>
        <boxGeometry args={[30, 8, 1]} />
        <meshStandardMaterial
          color="#3b3b3b" // Granito oscuro
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>
      
      {/* Muro Sur */}
      <mesh position={[0, 4, 15]} castShadow receiveShadow>
        <boxGeometry args={[30, 8, 1]} />
        <meshStandardMaterial
          color="#3b3b3b"
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>
      
      {/* Muro Este */}
      <mesh position={[15, 4, 0]} castShadow receiveShadow>
        <boxGeometry args={[1, 8, 30]} />
        <meshStandardMaterial
          color="#3b3b3b"
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>
      
      {/* Muro Oeste (con entrada) */}
      <mesh position={[-15, 4, 0]} castShadow receiveShadow>
        <boxGeometry args={[1, 8, 30]} />
        <meshStandardMaterial
          color="#3b3b3b"
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>
      
      {/* 🏛️ Columnas cuadradas de granito (8 columnas) */}
      {/* Fila frontal */}
      <Column position={[-8, 3, -8]} />
      <Column position={[0, 3, -8]} />
      <Column position={[8, 3, -8]} />
      
      {/* Fila central */}
      <Column position={[-8, 3, 0]} />
      <Column position={[8, 3, 0]} />
      
      {/* Fila posterior */}
      <Column position={[-8, 3, 8]} />
      <Column position={[0, 3, 8]} />
      <Column position={[8, 3, 8]} />
      
      {/* 🗿 Altar central */}
      <mesh position={[0, 0.75, 0]} castShadow receiveShadow>
        <boxGeometry args={[4, 1.5, 4]} />
        <meshStandardMaterial
          color="#6f6f6f" // Piedra gris
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>
      
      {/* ☀️ Abertura en el techo para luz (simulada con luz puntual) */}
      <pointLight
        position={[0, 7, 0]}
        intensity={2}
        distance={20}
        color="#ffd700"
        castShadow
      />
      
      {/* 🌫️ Luz ambiental tenue interior */}
      <ambientLight intensity={0.2} />
    </group>
  )
}

/**
 * Columna cuadrada individual
 */
function Column({ position }: { position: [number, number, number] }) {
  return (
    <mesh position={position} castShadow receiveShadow>
      <boxGeometry args={[1.5, 6, 1.5]} />
      <meshStandardMaterial
        color="#3b3b3b" // Granito oscuro
        roughness={0.8}
        metalness={0.2}
      />
    </mesh>
  )
}
