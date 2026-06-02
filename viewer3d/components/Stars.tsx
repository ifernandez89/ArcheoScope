'use client'

import { useMemo, useRef, useEffect, useState } from 'react'
import * as THREE from 'three'
import { useFrame } from '@react-three/fiber'
import { Html } from '@react-three/drei'
import { BRIGHT_STARS, raDecToXYZ, spectralColor } from '@/data/bright-stars'
import { CONSTELLATION_LINES } from '@/data/constellations'

/**
 * Estrellas optimizadas para Mobile GPU:
 *  - Capa base: 80k (fondo galáctico), tamaño reducido (2.5) y opacidad baja (0.6).
 *  - Capa brillante: 3k con Twinkle Shader y full opacity.
 *  - Capa real: 148 estrellas escaladas por magnitud real.
 *  - Constelaciones: Líneas con gradiente y labels adaptativos.
 */
export default function Stars() {
  const [isMobile, setIsMobile] = useState(false)
  
  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768)
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])

  const layers = useMemo(() => {
    // ── Capa base: fondo galáctico procedural (Optimizado para fillrate) ─────
    const baseCount = 80000
    const basePos   = new Float32Array(baseCount * 3)
    const baseCol   = new Float32Array(baseCount * 3)

    for (let i = 0; i < baseCount; i++) {
      const i3    = i * 3
      const theta = Math.random() * Math.PI * 2
      const phi   = Math.acos(2 * Math.random() - 1)
      const r = i < baseCount * 0.2
        ? 500  + Math.random() * 5500
        : 6000 + Math.random() * 14000

      basePos[i3]     = r * Math.sin(phi) * Math.cos(theta)
      basePos[i3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      basePos[i3 + 2] = r * Math.cos(phi)

      const color = new THREE.Color()
      const t = Math.random()
      if      (t < 0.12) color.setHSL(0.60, 0.9, 0.92)
      else if (t < 0.28) color.setHSL(0.58, 0.5, 0.90)
      else if (t < 0.50) color.setHSL(0.13, 0.4, 0.92)
      else if (t < 0.65) color.setHSL(0.07, 0.6, 0.88)
      else if (t < 0.72) color.setHSL(0.02, 0.8, 0.82)
      else               color.setHSL(0.00, 0.0, 0.88 + Math.random() * 0.12)

      baseCol[i3]     = color.r
      baseCol[i3 + 1] = color.g
      baseCol[i3 + 2] = color.b
    }

    const baseGeo = new THREE.BufferGeometry()
    baseGeo.setAttribute('position', new THREE.BufferAttribute(basePos, 3))
    baseGeo.setAttribute('color',    new THREE.BufferAttribute(baseCol, 3))
    const baseMat = new THREE.PointsMaterial({
      size: 2.5, // Reducido de 4.0 para mobile fillrate
      vertexColors: true,
      transparent: true,
      opacity: 0.6, // Reducido de 0.9 para profundidad
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })

    // ── Capa brillante: 3000 estrellas con TWINKLE SHADER ─────────────────
    const brightCount = 3000
    const brightPos   = new Float32Array(brightCount * 3)
    const brightCol   = new Float32Array(brightCount * 3)
    const brightRand  = new Float32Array(brightCount) // Para el parpadeo

    for (let i = 0; i < brightCount; i++) {
      const i3    = i * 3
      const theta = Math.random() * Math.PI * 2
      const phi   = Math.acos(2 * Math.random() - 1)
      const r     = 3000 + Math.random() * 15000

      brightPos[i3]     = r * Math.sin(phi) * Math.cos(theta)
      brightPos[i3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      brightPos[i3 + 2] = r * Math.cos(phi)

      const color = new THREE.Color()
      const t = Math.random()
      if   (t < 0.3) color.setHSL(0.60, 1.0, 1.0)
      else if (t < 0.6) color.setHSL(0.13, 0.6, 1.0)
      else           color.setHSL(0.00, 0.0, 1.0)

      brightCol[i3]     = color.r
      brightCol[i3 + 1] = color.g
      brightCol[i3 + 2] = color.b
      brightRand[i]     = Math.random()
    }

    const brightGeo = new THREE.BufferGeometry()
    brightGeo.setAttribute('position', new THREE.BufferAttribute(brightPos, 3))
    brightGeo.setAttribute('color',    new THREE.BufferAttribute(brightCol, 3))
    brightGeo.setAttribute('aRandom',  new THREE.BufferAttribute(brightRand, 1))

    const brightMat = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uBaseSize: { value: 10.0 } // Entre 8 y 12
      },
      vertexShader: `
        attribute float aRandom;
        varying float vRandom;
        varying vec3 vColor;
        uniform float uTime;
        uniform float uBaseSize;
        void main() {
          vRandom = aRandom;
          vColor = color;
          vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
          float twinkle = 1.0 + sin(uTime * 3.0 + aRandom * 10.0) * 0.2;
          gl_PointSize = uBaseSize * (300.0 / -mvPosition.z) * twinkle;
          gl_Position = projectionMatrix * mvPosition;
        }
      `,
      fragmentShader: `
        varying float vRandom;
        varying vec3 vColor;
        void main() {
          float dist = distance(gl_PointCoord, vec2(0.5));
          if (dist > 0.5) discard;
          float alpha = 1.0 - smoothstep(0.4, 0.5, dist);
          gl_FragColor = vec4(vColor, alpha);
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    })

    // ── Capa real: catálogo Yale Bright Star (Escalado por magnitud) ──────
    const R = 8000
    const realCount = BRIGHT_STARS.length
    const realPos   = new Float32Array(realCount * 3)
    const realCol   = new Float32Array(realCount * 3)
    const realSize  = new Float32Array(realCount)

    const starPositions = new Map<string, THREE.Vector3>()

    BRIGHT_STARS.forEach((star, i) => {
      const i3 = i * 3
      const [x, y, z] = raDecToXYZ(star.ra, star.dec, R)
      realPos[i3]     = x
      realPos[i3 + 1] = y
      realPos[i3 + 2] = z
      
      const [r, g, b] = spectralColor(star.type)
      realCol[i3]     = r
      realCol[i3 + 1] = g
      realCol[i3 + 2] = b
      
      // size = 14 - magnitude * 1.8 (Sugerencia del usuario)
      realSize[i] = Math.max(2.0, 14.0 - star.mag * 1.8)
      
      if (star.name) starPositions.set(star.name, new THREE.Vector3(x, y, z))
    })

    const realGeo = new THREE.BufferGeometry()
    realGeo.setAttribute('position', new THREE.BufferAttribute(realPos, 3))
    realGeo.setAttribute('color',    new THREE.BufferAttribute(realCol, 3))
    realGeo.setAttribute('size',     new THREE.BufferAttribute(realSize, 1))
    
    const realMat = new THREE.PointsMaterial({
      size: 1.0, // Se usará como multiplicador si usáramos shader, o lo manejamos así:
      vertexColors: true,
      transparent: true,
      opacity: 1.0,
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })
    // Como PointsMaterial no soporta tamaños por vértice nativamente sin shader, 
    // usaremos un shader simple para la capa real también para máxima calidad.
    const realShaderMat = new THREE.ShaderMaterial({
      uniforms: { uTime: { value: 0 } },
      vertexShader: `
        attribute float size;
        varying vec3 vColor;
        void main() {
          vColor = color;
          vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
          gl_PointSize = size * (300.0 / -mvPosition.z);
          gl_Position = projectionMatrix * mvPosition;
        }
      `,
      fragmentShader: `
        varying vec3 vColor;
        void main() {
          float dist = distance(gl_PointCoord, vec2(0.5));
          if (dist > 0.5) discard;
          gl_FragColor = vec4(vColor, 1.0 - smoothstep(0.3, 0.5, dist));
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    })

    return { baseGeo, baseMat, brightGeo, brightMat, realGeo, realShaderMat, starPositions }
  }, [])

  const brightMatRef = useRef<THREE.ShaderMaterial>(null)
  useFrame((state) => {
    if (layers.brightMat instanceof THREE.ShaderMaterial) {
      layers.brightMat.uniforms.uTime.value = state.clock.elapsedTime
    }
    if (layers.realShaderMat instanceof THREE.ShaderMaterial) {
      layers.realShaderMat.uniforms.uTime.value = state.clock.elapsedTime
    }
  })

  // Constelaciones con GRADIENT LINES
  const constellationLines = useMemo(() => {
    const lines: { points: Float32Array, colors: Float32Array }[] = []
    CONSTELLATION_LINES.forEach(constellation => {
      const pts: number[] = []
      const cols: number[] = []
      const baseColor = new THREE.Color(constellation.color)
      
      constellation.stars.forEach(([nameA, nameB]) => {
        const posA = layers.starPositions.get(nameA)
        const posB = layers.starPositions.get(nameB)
        if (posA && posB) {
          pts.push(posA.x, posA.y, posA.z, posB.x, posB.y, posB.z)
          // Gradiente: inicio 0.9, fin 0.2
          cols.push(baseColor.r, baseColor.g, baseColor.b, 0.9)
          cols.push(baseColor.r, baseColor.g, baseColor.b, 0.2)
        }
      })
      if (pts.length > 0) {
        lines.push({ 
          points: new Float32Array(pts), 
          colors: new Float32Array(cols) 
        })
      }
    })
    return lines
  }, [layers.starPositions])

  const constellationCenters = useMemo(() => {
    const centers: { name: string, position: THREE.Vector3, color: string }[] = []
    CONSTELLATION_LINES.forEach(constellation => {
      const positions: THREE.Vector3[] = []
      constellation.stars.forEach(([nameA, nameB]) => {
        const posA = layers.starPositions.get(nameA)
        const posB = layers.starPositions.get(nameB)
        if (posA) positions.push(posA)
        if (posB) positions.push(posB)
      })
      if (positions.length > 0) {
        const center = new THREE.Vector3()
        positions.forEach(p => center.add(p))
        center.divideScalar(positions.length)
        centers.push({ name: constellation.name, position: center, color: constellation.color })
      }
    })
    return centers
  }, [layers.starPositions])

  return (
    <group renderOrder={-1}>
      <points geometry={layers.baseGeo}   material={layers.baseMat} />
      <points geometry={layers.brightGeo} material={layers.brightMat} />
      <points geometry={layers.realGeo}   material={layers.realShaderMat} />
      
      {/* Líneas de constelaciones con gradiente */}
      {constellationLines.map((line, i) => (
        <lineSegments key={`const-${i}`}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={line.points.length / 3} array={line.points} itemSize={3} />
            <bufferAttribute attach="attributes-color" count={line.colors.length / 4} array={line.colors} itemSize={4} />
          </bufferGeometry>
          <lineBasicMaterial 
            vertexColors 
            transparent 
            blending={THREE.AdditiveBlending} 
            depthWrite={false} 
          />
        </lineSegments>
      ))}

      {/* Labels adaptativos */}
      {constellationCenters.map((c, i) => (
        <Html 
          key={`label-${i}`} 
          position={c.position} 
          center 
          sprite 
          occlude={false}
          distanceFactor={isMobile ? 12000 : 8000} // Implementa distanceFade de forma efectiva
        >
          <div style={{
            color: c.color,
            fontSize: isMobile ? '22px' : '35px',
            fontFamily: 'monospace',
            letterSpacing: '4px',
            textTransform: 'uppercase',
            opacity: 0.8,
            textShadow: `0 0 15px ${c.color}`,
            pointerEvents: 'none',
            whiteSpace: 'nowrap',
            userSelect: 'none',
            fontWeight: 'bold',
            transition: 'font-size 0.3s ease',
          }}>
            {c.name}
          </div>
        </Html>
      ))}
    </group>
  )
}
