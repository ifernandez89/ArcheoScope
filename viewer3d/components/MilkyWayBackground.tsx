'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * MilkyWayBackground - Banda galáctica optimizada
 * Usa mezcla aditiva y opacidad reducida para integrarse mejor con las estrellas
 */
export default function MilkyWayBackground() {
  const sphereRef = useRef<THREE.Mesh>(null)

  const milkyWayTexture = useTexture(getAssetPath('/textures/2k_stars_milky_way.jpg'), (texture) => {
    texture.mapping = THREE.UVMapping
    texture.colorSpace = THREE.SRGBColorSpace
  })

  // Shader para crear una banda suave y profunda
  const milkyWayMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        uTexture: { value: milkyWayTexture },
        uOpacity: { value: 0.15 }
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform sampler2D uTexture;
        uniform float uOpacity;
        varying vec2 vUv;
        void main() {
          vec4 texColor = texture2D(uTexture, vUv);
          // Suavizar los bordes de la banda galáctica para realismo
          float softBand = smoothstep(0.0, 0.4, vUv.y) * smoothstep(1.0, 0.6, vUv.y);
          gl_FragColor = vec4(texColor.rgb, texColor.r * uOpacity * softBand);
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending,
      side: THREE.BackSide,
      depthWrite: false,
      depthTest: false
    })
  }, [milkyWayTexture])

  useFrame((_, delta) => {
    if (sphereRef.current) {
      sphereRef.current.rotation.y += delta * 0.0005
    }
  })

  return (
    <mesh ref={sphereRef} renderOrder={-2} material={milkyWayMaterial}>
      <sphereGeometry args={[22000, 64, 64]} />
    </mesh>
  )
}
