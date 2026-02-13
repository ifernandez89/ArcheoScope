'use client'

import { useRef, useMemo } from 'react'
import * as THREE from 'three'

interface ProceduralTerrainProps {
  size?: number
  segments?: number
  heightScale?: number
  seed?: number
}

// Simplex noise simplificado (para terreno más natural)
function noise2D(x: number, y: number, seed: number = 0): number {
  const X = Math.floor(x) & 255
  const Y = Math.floor(y) & 255
  
  x -= Math.floor(x)
  y -= Math.floor(y)
  
  const u = fade(x)
  const v = fade(y)
  
  const a = hash(X + seed) + Y
  const b = hash(X + 1 + seed) + Y
  
  return lerp(v,
    lerp(u, grad(hash(a), x, y), grad(hash(b), x - 1, y)),
    lerp(u, grad(hash(a + 1), x, y - 1), grad(hash(b + 1), x - 1, y - 1))
  )
}

function fade(t: number): number {
  return t * t * t * (t * (t * 6 - 15) + 10)
}

function lerp(t: number, a: number, b: number): number {
  return a + t * (b - a)
}

function grad(hash: number, x: number, y: number): number {
  const h = hash & 3
  const u = h < 2 ? x : y
  const v = h < 2 ? y : x
  return ((h & 1) ? -u : u) + ((h & 2) ? -v : v)
}

function hash(n: number): number {
  n = (n << 13) ^ n
  return (n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff
}

// Fractal Brownian Motion para terreno más detallado
function fbm(x: number, y: number, octaves: number = 4, seed: number = 0): number {
  let value = 0
  let amplitude = 1
  let frequency = 1
  let maxValue = 0
  
  for (let i = 0; i < octaves; i++) {
    value += noise2D(x * frequency, y * frequency, seed) * amplitude
    maxValue += amplitude
    amplitude *= 0.5
    frequency *= 2
  }
  
  return value / maxValue
}

export default function ProceduralTerrain({
  size = 200,
  segments = 128,
  heightScale = 15,
  seed = 42
}: ProceduralTerrainProps) {
  const meshRef = useRef<THREE.Mesh>(null)

  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(size, size, segments, segments)
    geo.rotateX(-Math.PI / 2)
    
    const positions = geo.attributes.position.array as Float32Array
    const colors = new Float32Array(positions.length)
    
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i]
      const z = positions[i + 2]
      
      // Generar altura con FBM (múltiples octavas de ruido)
      const height = fbm(x * 0.02, z * 0.02, 5, seed) * heightScale
      
      // Agregar montañas más pronunciadas
      const mountainNoise = Math.pow(Math.abs(fbm(x * 0.01, z * 0.01, 3, seed + 100)), 2) * heightScale * 2
      
      // Combinar terreno base con montañas
      positions[i + 1] = height + mountainNoise
      
      // Colorear según altura
      const normalizedHeight = (positions[i + 1] + heightScale) / (heightScale * 3)
      
      if (normalizedHeight < 0.3) {
        // Bajo (verde oscuro)
        colors[i] = 0.2
        colors[i + 1] = 0.4
        colors[i + 2] = 0.1
      } else if (normalizedHeight < 0.6) {
        // Medio (verde claro)
        colors[i] = 0.3
        colors[i + 1] = 0.6
        colors[i + 2] = 0.2
      } else if (normalizedHeight < 0.8) {
        // Alto (marrón)
        colors[i] = 0.5
        colors[i + 1] = 0.4
        colors[i + 2] = 0.3
      } else {
        // Muy alto (gris/nieve)
        colors[i] = 0.8
        colors[i + 1] = 0.8
        colors[i + 2] = 0.85
      }
    }
    
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3))
    geo.computeVertexNormals()
    
    console.log('⛰️ Terreno procedural generado:', {
      size,
      segments,
      heightScale,
      vertices: positions.length / 3
    })
    
    return geo
  }, [size, segments, heightScale, seed])

  return (
    <mesh ref={meshRef} geometry={geometry} receiveShadow>
      <meshStandardMaterial
        vertexColors
        roughness={0.9}
        metalness={0.1}
        flatShading={false}
      />
    </mesh>
  )
}
