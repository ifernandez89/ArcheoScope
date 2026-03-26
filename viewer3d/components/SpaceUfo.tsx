'use client'

import { useRef, useState, useEffect, useMemo } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * SpaceUfo - OVNI controlado por mouse en la escena del espacio.
 * Escala dinámicamente según proximidad a planetas.
 */
export default function SpaceUfo({ ufoNumber = 1 }: { ufoNumber?: number }) {
  const ufoRef = useRef<THREE.Group>(null)
  const sunLightRef = useRef<THREE.DirectionalLight>(null)
  const { camera, size, scene: threeScene } = useThree()
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const { scene } = useGLTF(getAssetPath(`/ufo_${ufoNumber}.glb`))
  
  // Objetos reutilizables para evitar crear en cada frame
  const raycaster = useMemo(() => new THREE.Raycaster(), [])
  const mouseVec = useMemo(() => new THREE.Vector2(), [])
  const tempVec = useMemo(() => new THREE.Vector3(), [])
  const targetPos = useMemo(() => new THREE.Vector3(), [])
  const lookAtPos = useMemo(() => new THREE.Vector3(), [])
  const dirVec = useMemo(() => new THREE.Vector3(), [])
  
  // Cache de planetas (esferas) para evitar traverse cada frame
  const cachedPlanets = useRef<THREE.Mesh[]>([])
  const planetsCached = useRef(false)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: (e.clientX / size.width) * 2 - 1,
        y: -(e.clientY / size.height) * 2 + 1
      })
    }
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [size])

  useFrame(() => {
    if (!ufoRef.current) return

    mouseVec.set(mousePosition.x, mousePosition.y)
    raycaster.setFromCamera(mouseVec, camera)

    targetPos.copy(raycaster.ray.origin).add(
      tempVec.copy(raycaster.ray.direction).multiplyScalar(10)
    )
    ufoRef.current.position.lerp(targetPos, 0.1)

    if (ufoNumber !== 1 && ufoNumber !== 5) {
      lookAtPos.copy(ufoRef.current.position).add(raycaster.ray.direction)
      ufoRef.current.lookAt(lookAtPos)
    }
    if (ufoNumber === 1) ufoRef.current.rotation.y += 0.01
    if (ufoNumber === 5) ufoRef.current.rotation.y += 0.005

    // Cachear planetas una sola vez
    if (!planetsCached.current) {
      cachedPlanets.current = []
      threeScene.traverse((obj) => {
        if (obj instanceof THREE.Mesh && obj.geometry instanceof THREE.SphereGeometry) {
          cachedPlanets.current.push(obj)
        }
      })
      planetsCached.current = true
    }

    // Escala dinámica según distancia a planetas cacheados
    let minDist = Infinity
    cachedPlanets.current.forEach(planet => {
      const d = ufoRef.current!.position.distanceTo(planet.getWorldPosition(tempVec))
      if (d < minDist) minDist = d
    })

    const normalScale = 1.14
    const minScale = 0.0285
    let targetScale = normalScale
    if (minDist < 50) {
      const t = Math.max(0, Math.min(1, (50 - minDist) / 45))
      targetScale = normalScale - t * (normalScale - minScale)
    }
    const newScale = ufoRef.current.scale.x + (targetScale - ufoRef.current.scale.x) * 0.05
    ufoRef.current.scale.setScalar(newScale)

    // Luz solar apuntando desde el Sol hacia el OVNI
    if (sunLightRef.current) {
      dirVec.copy(ufoRef.current.position).normalize().multiplyScalar(-50)
      sunLightRef.current.position.copy(dirVec)
    }
  })

  return (
    <group ref={ufoRef} position={[0, 0, 10]}>
      <primitive object={scene} scale={1.37} />
      <directionalLight ref={sunLightRef} intensity={2.5} color="#fff5e6" castShadow
        shadow-mapSize-width={1024} shadow-mapSize-height={1024} />
      <ambientLight intensity={0.2} />
      <pointLight position={[10, 10, 10]} intensity={0.3} color="#ffffff" />
    </group>
  )
}
