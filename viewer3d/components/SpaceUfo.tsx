'use client'

import { useRef, useState, useEffect } from 'react'
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

    const raycaster = new THREE.Raycaster()
    raycaster.setFromCamera(new THREE.Vector2(mousePosition.x, mousePosition.y), camera)

    const targetPosition = raycaster.ray.origin.clone().add(
      raycaster.ray.direction.multiplyScalar(10)
    )
    ufoRef.current.position.lerp(targetPosition, 0.1)

    if (ufoNumber !== 1 && ufoNumber !== 5) {
      ufoRef.current.lookAt(ufoRef.current.position.clone().add(raycaster.ray.direction))
    }
    if (ufoNumber === 1) ufoRef.current.rotation.y += 0.01
    if (ufoNumber === 5) ufoRef.current.rotation.y += 0.005

    // Escala dinámica según distancia a planetas
    let minDist = Infinity
    threeScene.traverse((obj) => {
      if (obj instanceof THREE.Mesh && obj.geometry instanceof THREE.SphereGeometry) {
        const d = ufoRef.current!.position.distanceTo(obj.getWorldPosition(new THREE.Vector3()))
        if (d < minDist) minDist = d
      }
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
      const dir = ufoRef.current.position.clone().normalize()
      sunLightRef.current.position.copy(dir.multiplyScalar(-50))
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
