'use client'

/**
 * CelestialOverlay — Visualización de convergencias planetarias reales
 *
 * Dos partes:
 *  1. <CelestialOverlay3D>  — vive DENTRO del Canvas (líneas 3D + cálculo)
 *  2. <CelestialOverlayHUD> — vive FUERA del Canvas (panel HTML)
 *
 * Comunicación: evento DOM personalizado "celestial-convergence"
 */

import { useRef, useEffect, useState, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { SolarEngine } from '@/engines/SolarEngine'
import { calculateAllPlanets } from '@/utils/planetary-orbits'

// ── Config ───────────────────────────────────────────────────────────────────

const CONVERGENCE_THRESHOLD = 10   // grados (más estricto para convergencias reales)
const UPDATE_INTERVAL       = 2.0  // segundos entre recálculos
const TIME_SCALE            = 3600 // 1 seg real = 1 hora simulada
const VISUAL_SCALE          = 200

// ── Tipos ────────────────────────────────────────────────────────────────────

export interface Convergence {
  a: string
  b: string
  angle: number
  intensity: number // 0-1
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function auToScene(x: number, y: number, z: number): THREE.Vector3 {
  return new THREE.Vector3(x * VISUAL_SCALE, z * VISUAL_SCALE, y * VISUAL_SCALE)
}

// Vectores reutilizables para cálculos
const _dirA = new THREE.Vector3()
const _dirB = new THREE.Vector3()

function geocentricAngle(earth: THREE.Vector3, a: THREE.Vector3, b: THREE.Vector3): number {
  _dirA.copy(a).sub(earth).normalize()
  _dirB.copy(b).sub(earth).normalize()
  const dot = Math.max(-1, Math.min(1, _dirA.dot(_dirB)))
  return THREE.MathUtils.radToDeg(Math.acos(dot))
}

// ── Parte 3D (dentro del Canvas) ─────────────────────────────────────────────

interface LineData { from: THREE.Vector3; to: THREE.Vector3; intensity: number }

export function CelestialOverlay3D() {
  const solarEngineRef = useRef<SolarEngine>(new SolarEngine(0, 0))
  const startTimeRef = useRef(new Date())
  const elapsed = useRef(0)
  const [lines, setLines] = useState<LineData[]>([])
  
  // Geometría y material reutilizables
  const lineMaterial = useMemo(() => new THREE.LineBasicMaterial({
    color: '#00aaff',
    transparent: true,
    opacity: 0.55,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  }), [])

  useFrame((_, delta) => {
    elapsed.current += delta
    if (elapsed.current < UPDATE_INTERVAL) return
    elapsed.current = 0

    // Usar nuestro sistema planetario actualizado
    const solarEngine = solarEngineRef.current
    const solarState = solarEngine.update(delta)
    const timeInDays = (solarState.simulatedTime.getTime() - startTimeRef.current.getTime()) / (1000 * 60 * 60 * 24)
    
    // Calcular posiciones usando nuestro sistema
    const allPlanets = calculateAllPlanets(timeInDays, VISUAL_SCALE)
    
    // Filtrar solo los planetas que queremos mostrar convergencias
    const planets = [
      { name: 'Mercurio', pos: allPlanets.find(p => p.planet.name === 'Mercurio')?.position || new THREE.Vector3() },
      { name: 'Venus', pos: allPlanets.find(p => p.planet.name === 'Venus')?.position || new THREE.Vector3() },
      { name: 'Marte', pos: allPlanets.find(p => p.planet.name === 'Marte')?.position || new THREE.Vector3() },
    ]
    
    // Tierra como punto de referencia
    const earth = allPlanets.find(p => p.planet.name === 'Tierra')?.position || new THREE.Vector3()

    const newLines: LineData[] = []
    const convergences: Convergence[] = []

    for (let i = 0; i < planets.length; i++) {
      for (let j = i + 1; j < planets.length; j++) {
        const angle = geocentricAngle(earth, planets[i].pos, planets[j].pos)
        if (angle <= CONVERGENCE_THRESHOLD) {
          const intensity = 1 - angle / CONVERGENCE_THRESHOLD
          // Copiar posiciones en lugar de clonar
          newLines.push({ 
            from: new THREE.Vector3().copy(planets[i].pos), 
            to: new THREE.Vector3().copy(planets[j].pos), 
            intensity 
          })
          convergences.push({ a: planets[i].name, b: planets[j].name, angle, intensity })
        }
      }
    }

    setLines(newLines)

    // Notificar al HUD via evento DOM
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('celestial-convergence', { detail: convergences }))
    }
  })

  // Memoizar las líneas para evitar recrear en cada render
  const lineObjects = useMemo(() => {
    return lines.map((l, i) => {
      const geo = new THREE.BufferGeometry().setFromPoints([l.from, l.to])
      const mat = lineMaterial.clone()
      mat.opacity = l.intensity * 0.55
      return new THREE.Line(geo, mat)
    })
  }, [lines, lineMaterial])

  return (
    <group>
      {lineObjects.map((line, i) => (
        <primitive key={i} object={line} />
      ))}
    </group>
  )
}

// ── Parte HTML (fuera del Canvas) ─────────────────────────────────────────────

export function CelestialOverlayHUD() {
  const [convergences, setConvergences] = useState<Convergence[]>([])

  useEffect(() => {
    const handler = (e: Event) => {
      setConvergences((e as CustomEvent<Convergence[]>).detail)
    }
    window.addEventListener('celestial-convergence', handler)
    return () => window.removeEventListener('celestial-convergence', handler)
  }, [])

  if (convergences.length === 0) return null

  const strongest = convergences.reduce((a, b) => a.intensity > b.intensity ? a : b)

  return (
    <div style={{
      position: 'absolute',
      top: '50%',
      right: '24px',
      transform: 'translateY(-50%)',
      zIndex: 3000,
      display: 'flex',
      flexDirection: 'column',
      gap: '8px',
      pointerEvents: 'none',
    }}>
      {/* Título */}
      <div style={{
        background: 'rgba(0, 10, 30, 0.85)',
        border: `1px solid rgba(0, 170, 255, ${0.3 + strongest.intensity * 0.5})`,
        borderRadius: '8px',
        padding: '10px 14px',
        color: '#00aaff',
        fontSize: '11px',
        letterSpacing: '0.12em',
        textTransform: 'uppercase',
        textAlign: 'center',
        textShadow: `0 0 8px rgba(0,170,255,${strongest.intensity})`,
        boxShadow: `0 0 16px rgba(0,170,255,${strongest.intensity * 0.3})`,
      }}>
        ✦ Convergencia Celeste
      </div>

      {convergences.map((c, i) => (
        <div key={i} style={{
          background: 'rgba(0, 10, 30, 0.75)',
          border: '1px solid rgba(0, 170, 255, 0.2)',
          borderRadius: '6px',
          padding: '8px 12px',
          color: 'rgba(200, 230, 255, 0.9)',
          fontSize: '12px',
          lineHeight: '1.5',
        }}>
          <div style={{ color: '#00aaff', fontWeight: 600, marginBottom: '2px' }}>
            {c.a} — {c.b}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px' }}>
            <span style={{ color: 'rgba(150,200,255,0.7)', fontSize: '11px' }}>
              {c.angle.toFixed(1)}° separación
            </span>
            <span style={{ color: `rgba(0,170,255,${0.5 + c.intensity * 0.5})`, fontSize: '11px' }}>
              {Math.round(c.intensity * 100)}% resonancia
            </span>
          </div>
          <div style={{
            marginTop: '5px', height: '2px',
            background: 'rgba(0,170,255,0.15)', borderRadius: '1px', overflow: 'hidden',
          }}>
            <div style={{
              height: '100%',
              width: `${c.intensity * 100}%`,
              background: `rgba(0,170,255,${0.6 + c.intensity * 0.4})`,
              boxShadow: `0 0 6px rgba(0,170,255,${c.intensity})`,
              transition: 'width 1s ease',
            }} />
          </div>
        </div>
      ))}
    </div>
  )
}
