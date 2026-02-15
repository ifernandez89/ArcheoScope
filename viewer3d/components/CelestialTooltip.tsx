'use client'

import { useState } from 'react'
import { Html } from '@react-three/drei'

interface CelestialTooltipProps {
  name: string
  symbol: string
  type: string
  data: {
    orbitalPeriod?: string
    day?: string
    diameter: string
    temperature?: string
    atmosphere?: string
    moons?: string
    funFact: string
  }
  position: [number, number, number]
  color: string
}

export default function CelestialTooltip({
  name,
  symbol,
  type,
  data,
  position,
  color
}: CelestialTooltipProps) {
  const [isHovered, setIsHovered] = useState(false)
  
  return (
    <Html position={position} center>
      <div
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        style={{
          position: 'relative',
          pointerEvents: 'auto',
          cursor: 'pointer'
        }}
      >
        {/* Etiqueta siempre visible */}
        <div style={{
          color,
          fontSize: '11px',
          fontWeight: 'bold',
          textShadow: '0 0 4px rgba(0,0,0,0.9)',
          whiteSpace: 'nowrap',
          userSelect: 'none'
        }}>
          {symbol} {name}
        </div>
        
        {/* Tooltip en hover */}
        {isHovered && (
          <div style={{
            position: 'absolute',
            top: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(0, 0, 0, 0.95)',
            backdropFilter: 'blur(10px)',
            padding: '12px 16px',
            borderRadius: '8px',
            border: `2px solid ${color}`,
            minWidth: '220px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
            animation: 'fadeIn 0.2s ease-in-out',
            zIndex: 1000
          }}>
            {/* Título */}
            <div style={{
              fontSize: '14px',
              fontWeight: 'bold',
              color,
              marginBottom: '8px',
              borderBottom: `1px solid ${color}40`,
              paddingBottom: '6px'
            }}>
              {name}
            </div>
            
            {/* Tipo */}
            <div style={{
              fontSize: '10px',
              color: '#888',
              marginBottom: '8px'
            }}>
              {type}
            </div>
            
            {/* Datos clave */}
            <div style={{
              fontSize: '11px',
              color: '#fff',
              lineHeight: '1.6'
            }}>
              {data.orbitalPeriod && (
                <div>🪐 Año: {data.orbitalPeriod}</div>
              )}
              {data.day && (
                <div>☀️ Día: {data.day}</div>
              )}
              {data.temperature && (
                <div>🌡️ Temp: {data.temperature}</div>
              )}
              <div>📏 Diámetro: {data.diameter}</div>
              {data.moons && (
                <div>🌙 Lunas: {data.moons}</div>
              )}
              {data.atmosphere && (
                <div>💨 Atmósfera: {data.atmosphere}</div>
              )}
            </div>
            
            {/* Dato curioso */}
            <div style={{
              marginTop: '10px',
              paddingTop: '8px',
              borderTop: `1px solid ${color}40`,
              fontSize: '10px',
              color: '#fbbf24',
              fontStyle: 'italic'
            }}>
              ✨ {data.funFact}
            </div>
          </div>
        )}
      </div>
      
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateX(-50%) translateY(-5px); }
          to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }
      `}</style>
    </Html>
  )
}
