'use client'

import { useEffect, useRef, useMemo } from 'react'
import { useFrame, useLoader } from '@react-three/fiber'
import { SVGLoader } from 'three/examples/jsm/loaders/SVGLoader.js'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface GeoglyphProps {
  svgPath: string
  position: [number, number, number]
  size?: number
  color?: string
  opacity?: number
  vertical?: boolean
}

export default function Geoglyph({
  svgPath,
  position,
  size = 18,
  color = '#c8a96e',
  opacity = 0.7,
  vertical = false
}: GeoglyphProps) {
  const data = useLoader(SVGLoader, getAssetPath(svgPath))

  const geometry = useMemo(() => {
    if (!data) return null

    const points: THREE.Vector3[] = []

    data.paths.forEach((path) => {
      const subPaths = path.subPaths
      // Filtrar el rectángulo de fondo: un solo subpath con ≤5 puntos (M0,0 L w,0 L w,h L 0,h Z)
      if (subPaths.length === 1 && subPaths[0].getPoints(0).length <= 5) {
        const pts = subPaths[0].getPoints(0)
        const xs = pts.map(p => p.x)
        const ys = pts.map(p => p.y)
        const w = Math.max(...xs) - Math.min(...xs)
        const h = Math.max(...ys) - Math.min(...ys)
        // Si el rectángulo es grande (>100 unidades) probablemente es el fondo
        if (w > 100 && h > 100) return
      }

      subPaths.forEach((subPath) => {
        const pts = subPath.getPoints(12)
        for (let i = 0; i < pts.length - 1; i++) {
          points.push(new THREE.Vector3(pts[i].x, pts[i].y, 0))
          points.push(new THREE.Vector3(pts[i + 1].x, pts[i + 1].y, 0))
        }
      })
    })

    if (points.length === 0) return null

    // Calcular bounding box para centrar y escalar
    const box = new THREE.Box3()
    points.forEach(p => box.expandByPoint(p))
    const center = box.getCenter(new THREE.Vector3())
    const boxSize = box.getSize(new THREE.Vector3())
    const maxDim = Math.max(boxSize.x, boxSize.y)
    const scaleFactor = maxDim > 0 ? size / maxDim : 1

    // Centrar y escalar
    const scaled = points.map(p =>
      new THREE.Vector3(
        (p.x - center.x) * scaleFactor,
        (p.y - center.y) * scaleFactor,
        0
      )
    )

    const geo = new THREE.BufferGeometry()
    const positions = new Float32Array(scaled.length * 3)
    scaled.forEach((p, i) => {
      positions[i * 3]     = p.x
      positions[i * 3 + 1] = p.y
      positions[i * 3 + 2] = p.z
    })
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geo
  }, [data, size])

  if (!geometry) return null

  return (
    <group
      position={position}
      rotation={vertical
        ? [0, 0, Math.PI]           // vertical: parado, mirando al frente
        : [-Math.PI / 2, 0, Math.PI] // horizontal: en el suelo
      }
    >
      <lineSegments geometry={geometry}>
        <lineBasicMaterial
          color={color}
          transparent
          opacity={opacity}
          depthWrite={false}
        />
      </lineSegments>
    </group>
  )
}
