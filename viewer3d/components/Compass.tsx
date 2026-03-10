'use client'

interface CompassProps {
  rotation: number // Rotación de la cámara en grados
  solarAzimuth?: number // Opcional, para referencia
}

/**
 * 🧭 Brújula que apunta al norte real
 * - Muestra la rotación actual de la cámara/personaje
 * - Siempre apunta al norte geográfico (0°)
 * - Funciona en modo órbita y avatar
 */
export default function Compass({ rotation, solarAzimuth }: CompassProps) {
  return (
    <div
      style={{
        position: 'fixed',
        top: '70px',
        right: '20px',
        width: '65px',
        height: '65px',
        zIndex: 100,
        pointerEvents: 'none',
      }}
    >
      {/* Círculo exterior - estilo vintage */}
      <div
        style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, rgba(245, 240, 230, 0.98) 0%, rgba(220, 210, 195, 0.98) 100%)',
          border: '3px solid #8b7355',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.6), inset 0 2px 4px rgba(255, 255, 255, 0.4), inset 0 -2px 4px rgba(0, 0, 0, 0.2)',
        }}
      />

      {/* Rosa de los vientos - fondo decorativo */}
      <div
        style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          borderRadius: '50%',
          background: `
            radial-gradient(circle at center, transparent 20%, rgba(139, 115, 85, 0.1) 20%, rgba(139, 115, 85, 0.1) 22%, transparent 22%),
            conic-gradient(from 0deg, 
              rgba(139, 115, 85, 0.15) 0deg, transparent 5deg,
              transparent 40deg, rgba(139, 115, 85, 0.15) 45deg,
              rgba(139, 115, 85, 0.15) 90deg, transparent 95deg,
              transparent 130deg, rgba(139, 115, 85, 0.15) 135deg,
              rgba(139, 115, 85, 0.15) 180deg, transparent 185deg,
              transparent 220deg, rgba(139, 115, 85, 0.15) 225deg,
              rgba(139, 115, 85, 0.15) 270deg, transparent 275deg,
              transparent 310deg, rgba(139, 115, 85, 0.15) 315deg,
              rgba(139, 115, 85, 0.15) 360deg
            )
          `,
        }}
      />

      {/* Marcas cardinales - ROTAN con la cámara */}
      <div 
        style={{ 
          position: 'absolute', 
          width: '100%', 
          height: '100%',
          transition: 'transform 0.1s linear',
          transform: `rotate(${-rotation}deg)` // Contra-rotar para que el norte siempre esté arriba
        }}
      >
        <div style={{ position: 'absolute', top: '3px', left: '50%', transform: 'translateX(-50%)', color: '#c41e3a', fontSize: '13px', fontWeight: 'bold', fontFamily: '"Cinzel", "Trajan Pro", serif', textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)' }}>N</div>
        <div style={{ position: 'absolute', right: '3px', top: '50%', transform: 'translateY(-50%)', color: '#2c2416', fontSize: '11px', fontWeight: 'bold', fontFamily: '"Cinzel", "Trajan Pro", serif', textShadow: '0 1px 1px rgba(255, 255, 255, 0.3)' }}>E</div>
        <div style={{ position: 'absolute', bottom: '3px', left: '50%', transform: 'translateX(-50%)', color: '#2c2416', fontSize: '11px', fontWeight: 'bold', fontFamily: '"Cinzel", "Trajan Pro", serif', textShadow: '0 1px 1px rgba(255, 255, 255, 0.3)' }}>S</div>
        <div style={{ position: 'absolute', left: '3px', top: '50%', transform: 'translateY(-50%)', color: '#2c2416', fontSize: '11px', fontWeight: 'bold', fontFamily: '"Cinzel", "Trajan Pro", serif', textShadow: '0 1px 1px rgba(255, 255, 255, 0.3)' }}>O</div>
      </div>

      {/* Marcas de grados - ROTAN con la cámara */}
      <div 
        style={{ 
          position: 'absolute', 
          width: '100%', 
          height: '100%',
          transition: 'transform 0.1s linear',
          transform: `rotate(${-rotation}deg)`
        }}
      >
        {Array.from({ length: 36 }).map((_, i) => {
          const angle = i * 10
          const isCardinal = angle % 90 === 0
          const isIntercardinal = angle % 45 === 0 && !isCardinal
          return (
            <div
              key={angle}
              style={{
                position: 'absolute',
                width: isCardinal ? '1.5px' : isIntercardinal ? '1px' : '0.8px',
                height: isCardinal ? '7px' : isIntercardinal ? '5px' : '3px',
                background: isCardinal ? '#c41e3a' : '#8b7355',
                top: '50%',
                left: '50%',
                transformOrigin: `${isCardinal ? '0.75px' : isIntercardinal ? '0.5px' : '0.4px'} 0px`,
                transform: `translate(-50%, -50%) rotate(${angle}deg) translateY(-29px)`,
                opacity: isCardinal ? 1 : isIntercardinal ? 0.8 : 0.5,
              }}
            />
          )
        })}
      </div>

      {/* Aguja - FIJA apuntando al norte (arriba) */}
      <div style={{ position: 'absolute', width: '100%', height: '100%' }}>
        <svg style={{ position: 'absolute', top: '6px', left: '50%', transform: 'translateX(-50%)', width: '13px', height: '26px', filter: 'drop-shadow(0 2px 3px rgba(0, 0, 0, 0.4))' }} viewBox="0 0 16 32">
          <path d="M 8 0 L 12 28 L 8 24 L 4 28 Z" fill="#c41e3a" stroke="#8b1a2e" strokeWidth="0.5" />
          <path d="M 8 0 L 10 28 L 8 24 L 6 28 Z" fill="#e63946" opacity="0.6" />
        </svg>
        <svg style={{ position: 'absolute', bottom: '6px', left: '50%', transform: 'translateX(-50%) rotate(180deg)', width: '13px', height: '26px', filter: 'drop-shadow(0 2px 3px rgba(0, 0, 0, 0.4))' }} viewBox="0 0 16 32">
          <path d="M 8 0 L 12 28 L 8 24 L 4 28 Z" fill="#e8e8e8" stroke="#999999" strokeWidth="0.5" />
          <path d="M 8 0 L 10 28 L 8 24 L 6 28 Z" fill="#ffffff" opacity="0.7" />
        </svg>
        <div style={{ position: 'absolute', width: '8px', height: '8px', borderRadius: '50%', background: 'radial-gradient(circle at 30% 30%, #ffd700 0%, #daa520 50%, #b8860b 100%)', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', border: '1.5px solid #8b7355', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.5)' }} />
      </div>

      {/* Rumbo actual (hacia dónde miras) */}
      <div style={{ position: 'absolute', bottom: '-20px', left: '50%', transform: 'translateX(-50%)', color: '#e8e8e8', fontSize: '10px', fontFamily: '"Courier New", monospace', fontWeight: 'bold', background: 'rgba(44, 36, 22, 0.9)', padding: '2px 6px', borderRadius: '3px', border: '1px solid #8b7355', whiteSpace: 'nowrap', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.5)' }}>
        {Math.round(rotation)}° {getCardinalDirection(rotation)}
      </div>
    </div>
  )
}

/**
 * Obtener dirección cardinal
 */
function getCardinalDirection(degrees: number): string {
  const normalized = ((degrees % 360) + 360) % 360
  
  if (normalized >= 337.5 || normalized < 22.5) return 'N'
  if (normalized >= 22.5 && normalized < 67.5) return 'NE'
  if (normalized >= 67.5 && normalized < 112.5) return 'E'
  if (normalized >= 112.5 && normalized < 157.5) return 'SE'
  if (normalized >= 157.5 && normalized < 202.5) return 'S'
  if (normalized >= 202.5 && normalized < 247.5) return 'SO'
  if (normalized >= 247.5 && normalized < 292.5) return 'O'
  if (normalized >= 292.5 && normalized < 337.5) return 'NO'
  
  return 'N'
}
