'use client'

/**
 * AstronomicalInfo - Panel de información astronómica avanzada
 * Muestra coordenadas sexagesimales, estación, precesión, etc.
 */

import { useState } from 'react'
import * as THREE from 'three'
import { formatLatLon, formatAngle, radiansToSexagesimal } from '@/utils/sexagesimal'
import { LUNAR_PHASE_NAMES, LUNAR_PHASE_ICONS } from '@/utils/lunar-system'
import { detectConjunctions } from '@/utils/planetary-orbits'

interface AstronomicalInfoProps {
  location?: { lat: number; lon: number } | null
  solarState?: {
    // Formato actual del sistema
    altitude?: number
    azimuth?: number
    declination: number
    // Formato nuevo del SolarEngine
    solarAltitude?: number
    solarAzimuth?: number
    season?: 'spring' | 'summer' | 'autumn' | 'winter'
    dayOfYear?: number
    precessionAngle?: number
    // FASE 2: Nuevas propiedades
    planets?: Array<{
      position: { x: number, y: number, z: number }
      angle: number
      planet: { name: string, color: string }
    }>
    lunarState?: {
      phase: 'new' | 'waxing_crescent' | 'first_quarter' | 'waxing_gibbous' | 
             'full' | 'waning_gibbous' | 'last_quarter' | 'waning_crescent'
      illumination: number
      age: number
      distance: number
    }
    eclipse?: {
      type: 'solar' | 'lunar'
      magnitude: number
      visibility: 'visible' | 'partial' | 'not_visible'
      phase: 'beginning' | 'maximum' | 'ending' | 'none'
    }
  }
}

const SEASON_ICONS = {
  spring: '🌸',
  summer: '☀️',
  autumn: '🍂',
  winter: '❄️'
}

const SEASON_NAMES = {
  spring: 'Primavera',
  summer: 'Verano',
  autumn: 'Otoño',
  winter: 'Invierno'
}

export default function AstronomicalInfo({ location, solarState }: AstronomicalInfoProps) {
  const [isOpen, setIsOpen] = useState(false)
  
  if (!location || !solarState) return null
  
  // Convertir coordenadas a sexagesimal
  const coordsText = formatLatLon(location.lat, location.lon)
  
  // Convertir ángulos solares - usar formato disponible
  const altitude = solarState.solarAltitude ?? solarState.altitude ?? 0
  const azimuth = solarState.solarAzimuth ?? solarState.azimuth ?? 0
  
  const altitudeSex = radiansToSexagesimal(altitude)
  const azimuthSex = radiansToSexagesimal(azimuth)
  const declinationSex = radiansToSexagesimal(solarState.declination)
  
  // Calcular años de precesión desde J2000 (solo si está disponible)
  const precessionYears = solarState.precessionAngle 
    ? (solarState.precessionAngle / (2 * Math.PI)) * 25772 
    : 0
  
  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      zIndex: 1000,
      pointerEvents: 'auto'
    }}>
      {/* Botón toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          padding: '12px 16px',
          background: 'rgba(102, 126, 234, 0.9)',
          border: '1px solid rgba(255,255,255,0.3)',
          borderRadius: '8px',
          color: 'white',
          fontSize: '14px',
          fontWeight: 'bold',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          transition: 'all 0.2s',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
          marginLeft: 'auto'
        }}
        onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(102, 126, 234, 1)'}
        onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(102, 126, 234, 0.9)'}
      >
        🌌 Astronomía {isOpen ? '▼' : '▲'}
      </button>
      
      {/* Panel de información */}
      {isOpen && (
        <div style={{
          marginTop: '10px',
          padding: '16px',
          background: 'rgba(0, 0, 0, 0.85)',
          border: '1px solid rgba(255,255,255,0.2)',
          borderRadius: '8px',
          color: 'white',
          fontSize: '12px',
          minWidth: '320px',
          maxWidth: '400px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ 
            margin: '0 0 12px 0', 
            fontSize: '14px', 
            fontWeight: 'bold',
            color: '#fbbf24',
            borderBottom: '1px solid rgba(255,255,255,0.2)',
            paddingBottom: '8px'
          }}>
            📍 Información Astronómica
          </h3>
          
          {/* Coordenadas Sexagesimales */}
          <div style={{ marginBottom: '12px' }}>
            <div style={{ 
              fontSize: '11px', 
              color: '#9ca3af',
              marginBottom: '4px',
              fontWeight: 'bold'
            }}>
              Coordenadas (Sistema Babilónico):
            </div>
            <div style={{ 
              fontFamily: 'monospace',
              color: '#60a5fa',
              fontSize: '11px'
            }}>
              {coordsText}
            </div>
          </div>
          
          {/* Estación */}
          {solarState.season && solarState.dayOfYear && (
            <div style={{ marginBottom: '12px' }}>
              <div style={{ 
                fontSize: '11px', 
                color: '#9ca3af',
                marginBottom: '4px',
                fontWeight: 'bold'
              }}>
                Estación del Año:
              </div>
              <div style={{ 
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: '#34d399'
              }}>
                <span style={{ fontSize: '20px' }}>{SEASON_ICONS[solarState.season]}</span>
                <span>{SEASON_NAMES[solarState.season]}</span>
                <span style={{ color: '#9ca3af', fontSize: '11px' }}>
                  (Día {solarState.dayOfYear}/365)
                </span>
              </div>
            </div>
          )}
          
          {/* Posición Solar */}
          <div style={{ marginBottom: '12px' }}>
            <div style={{ 
              fontSize: '11px', 
              color: '#9ca3af',
              marginBottom: '4px',
              fontWeight: 'bold'
            }}>
              Posición Solar:
            </div>
            <div style={{ fontFamily: 'monospace', fontSize: '11px' }}>
              <div style={{ color: '#fbbf24' }}>
                Altura: {altitudeSex.degrees}° {altitudeSex.minutes}' {altitudeSex.seconds}"
              </div>
              <div style={{ color: '#f97316' }}>
                Azimut: {azimuthSex.degrees}° {azimuthSex.minutes}' {azimuthSex.seconds}"
              </div>
              <div style={{ color: '#ec4899' }}>
                Declinación: {declinationSex.degrees}° {declinationSex.minutes}' {declinationSex.seconds}"
              </div>
            </div>
          </div>
          
          {/* Precesión Axial */}
          {solarState.precessionAngle !== undefined && (
            <div style={{ marginBottom: '12px' }}>
              <div style={{ 
                fontSize: '11px', 
                color: '#9ca3af',
                marginBottom: '4px',
                fontWeight: 'bold'
              }}>
                Precesión Axial (Ciclo 25,772 años):
              </div>
              <div style={{ 
                fontFamily: 'monospace',
                color: '#a78bfa',
                fontSize: '11px'
              }}>
                {precessionYears >= 0 ? '+' : ''}{precessionYears.toFixed(1)} años desde J2000
              </div>
              <div style={{ 
                fontSize: '10px',
                color: '#6b7280',
                marginTop: '4px',
                fontStyle: 'italic'
              }}>
                💡 La precesión causa que las constelaciones "se muevan" lentamente
              </div>
            </div>
          )}
          
          {/* Estado Lunar */}
          {solarState.lunarState && (
            <div style={{ marginBottom: '12px' }}>
              <div style={{ 
                fontSize: '11px', 
                color: '#9ca3af',
                marginBottom: '4px',
                fontWeight: 'bold'
              }}>
                Estado Lunar:
              </div>
              <div style={{ 
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                marginBottom: '4px'
              }}>
                <span style={{ fontSize: '18px' }}>
                  {LUNAR_PHASE_ICONS[solarState.lunarState.phase]}
                </span>
                <span style={{ color: '#60a5fa', fontSize: '11px' }}>
                  {LUNAR_PHASE_NAMES[solarState.lunarState.phase]}
                </span>
              </div>
              <div style={{ fontFamily: 'monospace', fontSize: '10px', color: '#9ca3af' }}>
                Iluminación: {(solarState.lunarState.illumination * 100).toFixed(1)}%
                <br />
                Edad: {solarState.lunarState.age.toFixed(1)} días
                <br />
                Distancia: {(solarState.lunarState.distance / 1000).toFixed(0)}k km
              </div>
            </div>
          )}
          
          {/* Eclipses */}
          {solarState.eclipse && solarState.eclipse.magnitude > 0 && (
            <div style={{ marginBottom: '12px' }}>
              <div style={{ 
                fontSize: '11px', 
                color: '#9ca3af',
                marginBottom: '4px',
                fontWeight: 'bold'
              }}>
                🌒 Eclipse Detectado:
              </div>
              <div style={{ 
                padding: '8px',
                background: 'rgba(239, 68, 68, 0.2)',
                borderRadius: '4px',
                border: '1px solid rgba(239, 68, 68, 0.3)'
              }}>
                <div style={{ color: '#fbbf24', fontSize: '11px', fontWeight: 'bold' }}>
                  Eclipse {solarState.eclipse.type === 'solar' ? 'Solar' : 'Lunar'}
                </div>
                <div style={{ fontSize: '10px', color: '#9ca3af', marginTop: '2px' }}>
                  Magnitud: {solarState.eclipse.magnitude.toFixed(2)}
                  <br />
                  Fase: {solarState.eclipse.phase}
                  <br />
                  Visibilidad: {solarState.eclipse.visibility}
                </div>
              </div>
            </div>
          )}
          
          {/* Planetas Visibles */}
          {solarState.planets && solarState.planets.length > 0 && (
            <div style={{ marginBottom: '0' }}>
              <div style={{ 
                fontSize: '11px', 
                color: '#9ca3af',
                marginBottom: '4px',
                fontWeight: 'bold'
              }}>
                Planetas en Órbita:
              </div>
              <div style={{ 
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '4px',
                fontSize: '10px'
              }}>
                {solarState.planets.slice(0, 4).map((planetPos, i) => (
                  <div key={i} style={{ 
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}>
                    <div style={{ 
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      backgroundColor: planetPos.planet.color
                    }} />
                    <span style={{ color: '#9ca3af' }}>
                      {planetPos.planet.name}
                    </span>
                  </div>
                ))}
              </div>
              
              {/* Conjunciones planetarias */}
              {(() => {
                // Convertir formato si es necesario
                const planetsForConjunction = solarState.planets.map(p => ({
                  position: new THREE.Vector3(p.position.x, p.position.y, p.position.z),
                  angle: p.angle,
                  planet: {
                    name: p.planet.name,
                    period: 365, // valor por defecto
                    radius: 1,
                    inclination: 0,
                    eccentricity: 0,
                    color: p.planet.color,
                    size: 1,
                    initialAngle: 0 // valor por defecto
                  }
                }))
                const conjunctions = detectConjunctions(planetsForConjunction)
                return conjunctions.length > 0 && (
                  <div style={{ 
                    marginTop: '8px',
                    padding: '6px',
                    background: 'rgba(34, 197, 94, 0.2)',
                    borderRadius: '4px',
                    border: '1px solid rgba(34, 197, 94, 0.3)'
                  }}>
                    <div style={{ color: '#22c55e', fontSize: '10px', fontWeight: 'bold' }}>
                      ✨ Conjunción: {conjunctions[0].planets.join(' - ')}
                    </div>
                    <div style={{ fontSize: '9px', color: '#9ca3af' }}>
                      Separación: {conjunctions[0].separation.toFixed(1)}°
                    </div>
                  </div>
                )
              })()}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
