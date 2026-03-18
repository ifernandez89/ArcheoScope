'use client'

/**
 * EarthquakeEffect - Simula un terremoto:
 * - Shake de cámara con ruido senoidal multicapa
 * - Partículas de polvo que suben del suelo
 * - Intensidad variable (ondas P y S)
 * 
 * IMPORTANTE: Limpia la rotación de cámara al desmontarse
 */

import { useRef, useMemo, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Vector3, BufferGeometry, BufferAttribute, PointsMaterial, AdditiveBlending } from 'three'

export default function EarthquakeEffect() {
  const { camera } = useThree()
  const originRef = useRef(new Vector3())
  const timeRef = useRef(0)
  const dustRef = useRef<any>(null)

  // Guardar posición original de la cámara una sola vez
  const initialized = useRef(false)

  // Cleanup: resetear rotación de cámara al desmontar
  useEffect(() => {
    return () => {
      camera.rotation.z = 0
    }
  }, [camera])

  // Partículas de polvo
  const dustGeometry = useMemo(() => {
    const geo = new BufferGeometry()
    const count = 800
    const positions = new Float32Array(count * 3)
    const velocities = new Float32Array(count * 3)

    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      // Distribuir en el suelo alrededor del jugador
      positions[i3]     = (Math.random() - 0.5) * 80
      positions[i3 + 1] = Math.random() * 0.5  // Empiezan casi en el suelo
      positions[i3 + 2] = (Math.random() - 0.5) * 80
      // Velocidad vertical aleatoria
      velocities[i3 + 1] = 0.02 + Math.random() * 0.06
    }

    geo.setAttribute('position', new BufferAttribute(positions, 3))
    geo.setAttribute('velocity', new BufferAttribute(velocities, 3))
    return geo
  }, [])

  const dustMaterial = useMemo(() => new PointsMaterial({
    size: 0.4,
    color: '#c8a96e',
    transparent: true,
    opacity: 0.6,
    sizeAttenuation: true,
    depthWrite: false,
    blending: AdditiveBlending
  }), [])

  useFrame((_, delta) => {
    timeRef.current += delta

    // Guardar posición base de la cámara la primera vez
    if (!initialized.current) {
      originRef.current.copy(camera.position)
      initialized.current = true
    }

    const t = timeRef.current

    // Shake multicapa: onda principal + réplicas + vibración fina
    // REDUCIDO DRÁSTICAMENTE para evitar mareos (amplitud reducida 90%)
    const shakeX = Math.sin(t * 25) * 0.03 + Math.sin(t * 17.3) * 0.015
    const shakeY = Math.sin(t * 19.7) * 0.012 + Math.sin(t * 31) * 0.006
    const shakeZ = Math.sin(t * 22.1) * 0.025 + Math.sin(t * 13.5) * 0.01

    // Aplicar shake relativo a la posición actual (velocidad reducida 75%)
    camera.position.x += shakeX * delta * 2
    camera.position.y += shakeY * delta * 2
    camera.position.z += shakeZ * delta * 2

    // Leve rotación de cámara para sensación de inestabilidad (reducida 50%)
    camera.rotation.z = Math.sin(t * 18) * 0.004

    // Animar partículas de polvo
    if (dustRef.current) {
      const positions = dustRef.current.geometry.attributes.position.array as Float32Array
      const velocities = dustRef.current.geometry.attributes.velocity.array as Float32Array

      for (let i = 0; i < positions.length; i += 3) {
        // Mover hacia arriba
        positions[i + 1] += velocities[i + 1]
        // Sacudir horizontalmente
        positions[i]     += Math.sin(t * 10 + i) * 0.02
        positions[i + 2] += Math.cos(t * 8  + i) * 0.02

        // Reset cuando llegan muy alto
        if (positions[i + 1] > 12) {
          positions[i]     = (Math.random() - 0.5) * 80
          positions[i + 1] = 0
          positions[i + 2] = (Math.random() - 0.5) * 80
        }
      }
      dustRef.current.geometry.attributes.position.needsUpdate = true
    }
  })

  return (
    <points ref={dustRef} geometry={dustGeometry} material={dustMaterial} />
  )
}
