'use client'

import { useMemo, useState, useRef, useEffect, useCallback, Suspense } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useGLTF, Html } from '@react-three/drei'
import { getAssetPath } from '@/lib/paths'
import SelectableObject from './SelectableObject'

// 🚀 PRECARGAR TODOS LOS MODELOS INMEDIATAMENTE
useGLTF.preload(getAssetPath('/sphinx_base.glb'))
useGLTF.preload(getAssetPath('/ramses2.glb'))
useGLTF.preload(getAssetPath('/hatshepsut.glb'))
useGLTF.preload(getAssetPath('/akenaton.glb'))
useGLTF.preload(getAssetPath('/momia.glb'))
useGLTF.preload(getAssetPath('/escab.glb'))
useGLTF.preload(getAssetPath('/piramidon.glb'))

interface GizaSceneProps {
  avatarPositionRef: React.MutableRefObject<THREE.Vector3>
  onSphinxClick?: () => void
  onPyramidionCollect?: () => void
  pyramidionCollected?: boolean
  pyramidionOnTop?: boolean
  onMummyMoved?: () => void
  onScarabCollect?: () => void
  scarabDiscovered?: boolean
  scarabCollected?: boolean
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
export default function GizaScene({ avatarPositionRef, onSphinxClick, onPyramidionCollect, pyramidionCollected, pyramidionOnTop, onMummyMoved, onScarabCollect, scarabDiscovered, scarabCollected }: GizaSceneProps) {
  console.log('🔶 GizaScene RENDER - pyramidionCollected:', pyramidionCollected, 'pyramidionOnTop:', pyramidionOnTop)
  
  // Usar ref para nivel de inundación (evita re-renders cada frame)
  const floodLevelRef = useRef(0)
  const [isFlooding, setIsFlooding] = useState(false)
  const [fadeToBlack, setFadeToBlack] = useState(false)
  
  // 🎼 Activar arquitectura de Giza
  useEffect(() => {
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const harmonia = getHarmoniaMundi()
      if (harmonia.isEnabled()) {
        harmonia.activateArchitecture('giza')
        console.log('🏛️ Arquitectura de Giza activada')
      }
    })
    
    return () => {
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        const harmonia = getHarmoniaMundi()
        harmonia.deactivateArchitecture('giza')
      })
    }
  }, [])
  
  // Iniciar inundación cuando se recoge el escarabajo
  useEffect(() => {
    if (scarabCollected && !isFlooding) {
      console.log('🌊 Escarabajo recogido - Iniciando inundación...')
      setIsFlooding(true)
    }
  }, [scarabCollected, isFlooding])
  
  // Animación de inundación progresiva
  useFrame((state, delta) => {
    if (isFlooding && !fadeToBlack) {
      // Subir agua lentamente (1m por segundo - más rápido)
      floodLevelRef.current = Math.min(floodLevelRef.current + delta * 1.0, 100)
      
      // Verificar si el agua alcanzó la nave del usuario
      const avatarY = avatarPositionRef.current.y
      
      if (floodLevelRef.current >= avatarY) {
        // ¡El agua alcanzó al jugador!
        console.log('🌊 El agua ha alcanzado al jugador - Game Over')
        setFadeToBlack(true) // Marcar para evitar múltiples redirecciones
        
        // Limpiar estados para forzar nueva partida
        if (typeof window !== 'undefined') {
          // Limpiar sessionStorage
          sessionStorage.clear()
          
          // Limpiar flag de sesión activa para ocultar "Continuar"
          sessionStorage.removeItem('game_session_active')
          
          // Redirigir inmediatamente al menú
          const basePath = window.location.pathname.includes('/ArcheoScope') ? '/ArcheoScope' : ''
          window.location.href = basePath + '/menu'
        }
      }
    }
  })
  
  return (
    <Suspense fallback={<LoadingGiza />}>
      <group name="giza-complex">
        {/* 🌫️ Niebla desértica amarillenta */}
        <fog attach="fog" args={['#e8d5b7', 50, 400]} />
        
        {/* 🏜️ Terreno desértico con dunas suaves */}
        <DesertTerrain />
        
        {/* 🔺 Gran Pirámide de Keops (Khufu) - CON PUNTA PLANA */}
        <GreatPyramid 
          position={[0, 0, 0]}
          rotation={[0, Math.PI / 4, 0]} // Rotación 45° para alinear caras con cardinales
        />
        
        {/* 👑 Akhenaton - Dentro de la pirámide (cámara del rey) - MOVIBLE */}
        <MovablePharao 
          id="giza-akhenaton"
          model="akenaton.glb"
          initialPosition={[0, 0, 0]} // Centro de la pirámide, a nivel del suelo
          rotation={[0, 0, 0]} // De pie, mirando al norte
          scale={6}
        />
        
        {/* 🏺 Momia - Fuera de la pirámide hacia el oeste - MOVIBLE */}
        <MovableMummy 
          id="giza-momia"
          model="momia.glb"
          initialPosition={[-72, 0, -2]} // 2 metros más al oeste, a nivel del piso
          rotation={[-Math.PI / 2, 0, 0]} // Acostada boca arriba
          scale={0.125}
          onMove={onMummyMoved}
        />
        
        {/* 🪲 Escarabajo - Aparece cuando se mueve la momia */}
        {scarabDiscovered && !scarabCollected && (
          <Scarab 
            position={[-72, 1, -2]} // Encima de donde estaba la momia
            onCollect={onScarabCollect}
          />
        )}
        
        {/* 🔶 Piramidión - En el suelo frente a la esfinge */}
        {!pyramidionCollected && (
          <Pyramidion 
            position={[100, 0.5, 35]} // 15m delante de la esfinge, 50cm sobre el suelo
            rotation={[0, 0, 0]}
            onCollect={onPyramidionCollect}
          />
        )}
        
        {/* 🔶 Piramidón en la punta - VISIBLE después de entregarlo a la Esfinge */}
        {pyramidionOnTop && (
          <PyramidionOnTop 
            position={[0, 45.48, 0]} // En la punta de la pirámide
            rotation={[0, 0, 0]}
          />
        )}
        
        {/* 🦁 La Gran Esfinge - Al este de la pirámide, mirando al Este */}
        <Sphinx 
          position={[100, 5, 50]}
          rotation={[0, Math.PI / 2, 0]} // Mira hacia el Este (salida del sol)
          onClick={onSphinxClick}
        />
        
        {/* 👑 Estatuas de faraones - Frente a la pirámide, mirando al sur */}
        {/* Ramsés II - Lado oeste, CAÍDO de lado */}
        <PharaoStatue 
          model="ramses2.glb"
          position={[-20, 0, -50]} // Oeste de la pirámide, frente sur
          rotation={[0, 0, Math.PI / 2]} // Rotado 90° en Z para que caiga de lado
          scale={8}
        />
        
        {/* Hatshepsut - Lado este */}
        <PharaoStatue 
          model="hatshepsut.glb"
          position={[20, 0, -50]} // Este de la pirámide, frente sur
          rotation={[0, Math.PI, 0]} // Mirando al sur (rotada 180° para enfrentar a Ramsés)
          scale={8}
        />
        
        {/* 🏛️ Templo del Valle de Kefrén - Debajo de la pirámide */}
        <ValleyTemple 
          position={[0, -5, 0]} // Justo debajo de la pirámide, 5m bajo la arena
        />
        
        {/* 🪨 Piedras dispersas del desierto */}
        <DesertRocks />
        
        {/* 🌊 INUNDACIÓN - Plano de agua que sube progresivamente */}
        {isFlooding && (
          <FloodWater levelRef={floodLevelRef} />
        )}
      </group>
    </Suspense>
  )
}

/**
 * 🔄 Loading placeholder para Giza
 */
function LoadingGiza() {
  return (
    <Html center>
      <div style={{
        color: 'white',
        fontSize: '24px',
        textAlign: 'center',
        padding: '20px',
        background: 'rgba(0,0,0,0.7)',
        borderRadius: '10px'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>🏜️</div>
        <div>Cargando Giza...</div>
      </div>
    </Html>
  )
}

/**
 * 🔺 Gran Pirámide de Keops - CON PUNTA PLANA
 * La más grande y precisa - Actualmente sin piramidón
 */
function GreatPyramid({ position, rotation }: { 
  position: [number, number, number]
  rotation: [number, number, number]
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
  const scale = 20
  
  return (
    <group position={position} rotation={rotation} onClick={onClick} onPointerOver={() => document.body.style.cursor = 'pointer'} onPointerOut={() => document.body.style.cursor = 'default'}>
      <primitive 
        object={scene}
        scale={[scale, scale, scale]}
        castShadow
        receiveShadow
      />
    </group>
  )
}

/**
 * 👑 Estatua de Faraón
 * Estatuas monumentales de faraones egipcios
 */
function PharaoStatue({ model, position, rotation, scale }: { 
  model: string
  position: [number, number, number]
  rotation: [number, number, number]
  scale: number
}) {
  const { scene } = useGLTF(getAssetPath(`/${model}`))
  
  return (
    <group position={position} rotation={rotation}>
      <primitive 
        object={scene}
        scale={[scale, scale, scale]}
        castShadow
        receiveShadow
      />
    </group>
  )
}

/**
 * 🌊 Agua de inundación - Plano que sube progresivamente
 */
function FloodWater({ levelRef }: { levelRef: React.MutableRefObject<number> }) {
  const waterRef = useRef<THREE.Mesh>(null)
  
  // Animación de ondulación del agua y actualización de posición
  useFrame((state) => {
    if (waterRef.current) {
      // Actualizar posición Y basada en el ref
      waterRef.current.position.y = levelRef.current
      
      if (waterRef.current.material) {
        const time = state.clock.getElapsedTime()
        const material = waterRef.current.material as THREE.MeshStandardMaterial
        // Ondulación sutil
        material.opacity = 0.6 + Math.sin(time * 0.5) * 0.1
      }
    }
  })
  
  return (
    <mesh ref={waterRef} position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[1000, 1000, 50, 50]} />
      <meshStandardMaterial
        color="#1e3a5f"
        transparent
        opacity={0.6}
        metalness={0.8}
        roughness={0.2}
        envMapIntensity={1}
      />
    </mesh>
  )
}

/**
 * 👑 Faraón Movible - Wrapper para hacer estatuas seleccionables y movibles
 * Usa SelectableObject para permitir click y movimiento como los bloques H
 */
function MovablePharao({ id, model, initialPosition, rotation, scale }: {
  id: string
  model: string
  initialPosition: [number, number, number]
  rotation: [number, number, number]
  scale: number
}) {
  const [pos, setPos] = useState<[number, number, number]>(initialPosition)
  
  return (
    <SelectableObject id={id} position={pos} onMove={setPos}>
      <PharaoStatue 
        model={model}
        position={[0, 0, 0]} // Posición relativa al SelectableObject
        rotation={rotation}
        scale={scale}
      />
    </SelectableObject>
  )
}

/**
 * 🏺 Momia Movible - Detecta cuando se mueve para revelar el escarabajo
 */
function MovableMummy({ id, model, initialPosition, rotation, scale, onMove }: {
  id: string
  model: string
  initialPosition: [number, number, number]
  rotation: [number, number, number]
  scale: number
  onMove?: () => void
}) {
  const [pos, setPos] = useState<[number, number, number]>(initialPosition)
  const [hasMoved, setHasMoved] = useState(false)
  
  const handleMove = useCallback((newPos: [number, number, number]) => {
    setPos(newPos)
    if (!hasMoved) {
      setHasMoved(true)
      if (onMove) {
        onMove()
        console.log('🏺 Momia movida! Escarabajo revelado')
      }
    }
  }, [hasMoved, onMove])
  
  return (
    <SelectableObject id={id} position={pos} onMove={handleMove}>
      <PharaoStatue 
        model={model}
        position={[0, 0, 0]}
        rotation={rotation}
        scale={scale}
      />
    </SelectableObject>
  )
}

/**
 * 🪲 Escarabajo - Item coleccionable que aparece bajo la momia
 */
function Scarab({ position, onCollect }: {
  position: [number, number, number]
  onCollect?: () => void
}) {
  const { scene } = useGLTF(getAssetPath('/escab.glb'))
  const [isHovered, setIsHovered] = useState(false)
  const [isDisappearing, setIsDisappearing] = useState(false)
  const disappearTimer = useRef(0)
  
  // Cache de meshes para evitar traverse cada frame
  const cachedMeshes = useRef<THREE.Mesh[]>([])
  const meshesCached = useRef(false)
  
  const scale = 0.5
  
  // Calcular offset Y para que esté en el suelo
  const yOffset = useMemo(() => {
    const box = new THREE.Box3().setFromObject(scene)
    const minY = box.min.y
    return -minY * scale
  }, [scene, scale])
  
  // Animación de desaparición
  useFrame((state, delta) => {
    if (isDisappearing && scene) {
      disappearTimer.current += delta
      
      const progress = Math.min(disappearTimer.current / 1.0, 1)
      scene.scale.setScalar(scale * (1 + progress * 0.5))
      
      // Cache meshes solo una vez
      if (!meshesCached.current) {
        cachedMeshes.current = []
        scene.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            cachedMeshes.current.push(child as THREE.Mesh)
          }
        })
        meshesCached.current = true
      }
      
      // Aplicar fade a meshes cacheados
      for (const mesh of cachedMeshes.current) {
        if (mesh.material) {
          const material = mesh.material as THREE.MeshStandardMaterial
          material.transparent = true
          material.opacity = 1 - progress
        }
      }
      
      if (progress >= 1 && onCollect) {
        onCollect()
      }
    }
  })
  
  const handleClick = (e: any) => {
    if (onCollect && !isDisappearing) {
      e.stopPropagation()
      setIsDisappearing(true)
      console.log('🪲 Escarabajo recogido!')
    }
  }
  
  return (
    <group 
      position={[position[0], position[1] + yOffset, position[2]]} 
      onClick={handleClick}
      onPointerOver={() => onCollect && !isDisappearing && setIsHovered(true)}
      onPointerOut={() => setIsHovered(false)}
    >
      <primitive 
        object={scene}
        scale={[scale, scale, scale]}
        castShadow
        receiveShadow
      />
      
      {isHovered && onCollect && !isDisappearing && (
        <mesh>
          <sphereGeometry args={[1, 16, 16]} />
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

/**
 * 🔶 Piramidón en la punta de la pirámide
 * Versión especial que CLONA la escena para ser independiente del piramidión del suelo
 */
function PyramidionOnTop({ position, rotation }: { 
  position: [number, number, number]
  rotation: [number, number, number]
}) {
  const { scene } = useGLTF(getAssetPath('/piramidon.glb'))
  
  // CLONAR la escena para que sea independiente
  const clonedScene = useMemo(() => {
    const cloned = scene.clone(true)
    // Asegurar que los materiales sean visibles
    cloned.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        if (mesh.material) {
          // Clonar material para independencia
          mesh.material = (mesh.material as THREE.Material).clone()
          const mat = mesh.material as THREE.MeshStandardMaterial
          mat.transparent = false
          mat.opacity = 1
          mat.needsUpdate = true
        }
      }
    })
    return cloned
  }, [scene])
  
  const scale = 4
  
  // NO usar yOffset - la posición Y=46.6 es la correcta y se aplica directamente
  
  return (
    <group 
      position={position} 
      rotation={rotation}
    >
      <primitive 
        object={clonedScene}
        scale={[scale, scale, scale]}
        castShadow
        receiveShadow
      />
    </group>
  )
}

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
  
  // Cache de meshes para evitar traverse cada frame
  const cachedMeshes = useRef<THREE.Mesh[]>([])
  const meshesCached = useRef(false)
  
  // Aplicar opacidad inicial (solo una vez)
  useEffect(() => {
    scene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        if (mesh.material) {
          const mat = mesh.material as THREE.MeshStandardMaterial
          mat.transparent = true
          mat.opacity = opacity
          mat.needsUpdate = true
        }
      }
    })
  }, [scene, opacity])
  
  const scale = 4
  
  // NO usar yOffset - la posición Y viene directamente del prop
  // El modelo se posiciona exactamente donde se indica
  
  // Animación de desaparición
  useFrame((state, delta) => {
    if (isDisappearing && scene) {
      disappearTimer.current += delta
      
      const progress = Math.min(disappearTimer.current / 1.0, 1)
      scene.scale.setScalar(scale * (1 + progress * 0.5))
      
      // Cache meshes solo una vez
      if (!meshesCached.current) {
        cachedMeshes.current = []
        scene.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            cachedMeshes.current.push(child as THREE.Mesh)
          }
        })
        meshesCached.current = true
      }
      
      // Aplicar fade a meshes cacheados
      for (const mesh of cachedMeshes.current) {
        if (mesh.material) {
          const material = mesh.material as THREE.MeshStandardMaterial
          material.transparent = true
          material.opacity = 1 - progress
        }
      }
      
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
      position={position} 
      rotation={rotation}
      onClick={handleClick}
      onPointerOver={() => onCollect && !isDisappearing && setIsHovered(true)}
      onPointerOut={() => setIsHovered(false)}
    >
      <primitive 
        object={scene}
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
