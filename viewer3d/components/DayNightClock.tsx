'use client'

/**
 * DayNightClock - Reloj visual que muestra la hora del día
 * Muestra un círculo con el sol/luna moviéndose alrededor
 */

import { useMemo } from 'react'

interface DayNightClockProps {
  solarAltitude: number  // Altura del sol en radianes (-π/2 a π/2)
  solarAzimuth: number   // Azimut del sol en radianes
  isDay: boolean
}

export default function DayNightClock({ solarAltitude, solarAzimuth, isDay }: DayNightClockProps) {
  // Calcular posición del sol/luna en el círculo
  const { x, y, icon, timeLabel } = useMemo(() => {
    // Convertir altitud a posición en círculo (0° = horizonte este, 90° = cenit, 180° = horizonte oeste)
    // Normalizar altitud de -90° a 90° a un rango de 0 a 1
    const normalizedAltitude = (solarAltitude + Math.PI / 2) / Math.PI
    
    // Calcular ángulo en el círculo (0° = este/derecha, 90° = arriba, 180° = oeste/izquierda)
    // El azimut va de 0 (norte) a 2π, necesitamos rotarlo 90° para que este sea 0°
    const angle = solarAzimuth - Math.PI / 2
    
    // Radio del círculo (más pequeño cuando está cerca del horizonte)
    const radius = 35 * normalizedAltitude
    
    // Posición x,y en el círculo
    const posX = 40 + Math.cos(angle) * radius
    const posY = 40 - Math.sin(angle) * radius
    
    // Determinar icono
    const displayIcon = isDay ? '☀️' : '🌙'
    
    // Calcular hora aproximada (basado en altitud)
    // Amanecer ~6am (altitud = 0°), Mediodía ~12pm (altitud = 90°), Atardecer ~6pm (altitud = 0°)
    let hour = 0
    if (solarAltitude >= 0) {
      // Día: de 6am a 6pm
      hour = 6 + (solarAltitude / (Math.PI / 2)) * 6
    } else {
      // Noche: de 6pm a 6am
      hour = 18 + ((solarAltitude + Math.PI / 2) / (Math.PI / 2)) * 12
      if (hour >= 24) hour -= 24
    }
    
    const hourInt = Math.floor(hour)
    const minutes = Math.floor((hour - hourInt) * 60)
    const timeStr = `${hourInt.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
    
    return { x: posX, y: posY, icon: displayIcon, timeLabel: timeStr }
  }, [solarAltitude, solarAzimuth, isDay])
  
  return (
    <div style={{
      position: 'fixed',
      top: '80px',
      right: '20px',
      zIndex: 1000,
      width: '72px',
      height: '72px',
      pointerEvents: 'none'
    }}>
      {/* Círculo exterior */}
      <svg width="72" height="72" style={{ position: 'absolute' }}>
        {/* Fondo del cielo */}
        <circle
          cx="36"
          cy="36"
          r="34"
          fill={isDay ? 'rgba(135, 206, 235, 0.3)' : 'rgba(25, 25, 112, 0.3)'}
          stroke={isDay ? 'rgba(255, 215, 0, 0.6)' : 'rgba(192, 192, 192, 0.6)'}
          strokeWidth="2"
        />
        
        {/* Línea del horizonte */}
        <line
          x1="2"
          y1="36"
          x2="70"
          y2="36"
          stroke="rgba(255, 255, 255, 0.4)"
          strokeWidth="1"
          strokeDasharray="2,2"
        />
        
        {/* Marcadores cardinales */}
        <text x="36" y="10" textAnchor="middle" fill="rgba(255,255,255,0.5)" fontSize="8">N</text>
        <text x="63" y="39" textAnchor="middle" fill="rgba(255,255,255,0.5)" fontSize="8">E</text>
        <text x="36" y="68" textAnchor="middle" fill="rgba(255,255,255,0.5)" fontSize="8">S</text>
        <text x="9" y="39" textAnchor="middle" fill="rgba(255,255,255,0.5)" fontSize="8">O</text>
        
        {/* Trayectoria del sol/luna */}
        <circle
          cx={x * 0.9}
          cy={y * 0.9}
          r="5"
          fill={isDay ? '#FFD700' : '#C0C0C0'}
          stroke={isDay ? '#FFA500' : '#A0A0A0'}
          strokeWidth="1"
        />
      </svg>
      
      {/* Icono del sol/luna */}
      <div style={{
        position: 'absolute',
        left: `${x * 0.9 - 7}px`,
        top: `${y * 0.9 - 7}px`,
        fontSize: '14px',
        textShadow: '0 0 4px rgba(0,0,0,0.5)',
        pointerEvents: 'none'
      }}>
        {icon}
      </div>
    </div>
  )
}
