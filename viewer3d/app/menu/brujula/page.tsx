'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState, useRef, useCallback } from 'react'

// ─── Helpers ─────────────────────────────────────────────────────────────────

function getCardinalDirection(degrees: number): string {
  const n = ((degrees % 360) + 360) % 360
  if (n >= 337.5 || n < 22.5)   return 'N'
  if (n < 67.5)                  return 'NE'
  if (n < 112.5)                 return 'E'
  if (n < 157.5)                 return 'SE'
  if (n < 202.5)                 return 'S'
  if (n < 247.5)                 return 'SO'
  if (n < 292.5)                 return 'O'
  return 'NO'
}

function getCardinalLabel(dir: string): string {
  const labels: Record<string, string> = {
    N: 'Norte', NE: 'Noreste', E: 'Este', SE: 'Sureste',
    S: 'Sur', SO: 'Suroeste', O: 'Oeste', NO: 'Noroeste',
  }
  return labels[dir] || dir
}

// ─── Componente principal ─────────────────────────────────────────────────────

export default function BrujulaPage() {
  const router = useRouter()
  const [heading, setHeading]         = useState<number | null>(null)
  const [permission, setPermission]   = useState<'unknown' | 'granted' | 'denied' | 'unsupported'>('unknown')
  const [calibrating, setCalibrating] = useState(false)
  const [accuracy, setAccuracy]       = useState<number | null>(null)
  const smoothRef = useRef<number | null>(null)

  // ─── Suavizado exponencial (igual que el juego usa transition: 0.1s) ───────
  const smooth = useCallback((raw: number) => {
    if (smoothRef.current === null) {
      smoothRef.current = raw
      return raw
    }
    // Manejar wrap-around 359°→0°
    let prev = smoothRef.current
    let diff = raw - prev
    if (diff > 180)  diff -= 360
    if (diff < -180) diff += 360
    const alpha = 0.15  // factor de suavizado (0=sin cambio, 1=sin suavizado)
    smoothRef.current = ((prev + diff * alpha) + 360) % 360
    return smoothRef.current
  }, [])

  // Ref para el handler activo — permite removerlo correctamente al desmontar
  const handlerRef = useRef<((e: DeviceOrientationEvent) => void) | null>(null)

  const attachListeners = useCallback(() => {
    if (typeof window === 'undefined') return

    if (!window.DeviceOrientationEvent) {
      setPermission('unsupported')
      return
    }

    const handler = (e: DeviceOrientationEvent) => {
      let raw: number | null = null

      if ((e as any).webkitCompassHeading !== undefined) {
        // iOS — webkitCompassHeading ya es el rumbo magnético real (0=Norte, CW)
        raw = (e as any).webkitCompassHeading
        const acc = (e as any).webkitCompassAccuracy
        if (acc !== undefined && acc >= 0) setAccuracy(acc)
      } else if (e.alpha !== null) {
        // Android — alpha es la rotación del dispositivo; invertir para obtener rumbo
        raw = (360 - e.alpha) % 360
      }

      if (raw !== null) {
        setHeading(smooth(raw))
      }
    }

    handlerRef.current = handler
    // deviceorientationabsolute da el norte magnético real en Android (más preciso)
    window.addEventListener('deviceorientationabsolute', handler as EventListener, true)
    window.addEventListener('deviceorientation', handler as EventListener, true)
    setPermission('granted')
  }, [smooth])

  // ─── Iniciar brújula (llamado por botón en iOS) ───────────────────────────
  const startCompass = useCallback(async () => {
    if (typeof window === 'undefined') return

    // iOS requiere requestPermission() explícito (gesto del usuario)
    if (typeof (DeviceOrientationEvent as any).requestPermission === 'function') {
      try {
        const result = await (DeviceOrientationEvent as any).requestPermission()
        if (result !== 'granted') {
          setPermission('denied')
          return
        }
      } catch {
        setPermission('denied')
        return
      }
    }

    attachListeners()
  }, [attachListeners])

  useEffect(() => {
    if (typeof window === 'undefined') return
    // Android: no requiere permiso explícito — iniciar automáticamente
    if (typeof (DeviceOrientationEvent as any).requestPermission !== 'function') {
      attachListeners()
    }
    // iOS: esperar tap del usuario (botón "Activar brújula")

    return () => {
      // Cleanup correcto: remover siempre el handler al desmontar
      if (handlerRef.current) {
        window.removeEventListener('deviceorientationabsolute', handlerRef.current as EventListener, true)
        window.removeEventListener('deviceorientation', handlerRef.current as EventListener, true)
        handlerRef.current = null
      }
    }
  }, [attachListeners])

  const cardinal = heading !== null ? getCardinalDirection(heading) : null
  const cardinalLabel = cardinal ? getCardinalLabel(cardinal) : null

  // ─── Colores por dirección ────────────────────────────────────────────────
  const dirColor: Record<string, string> = {
    N: '#ef4444', NE: '#f97316', E: '#fbbf24', SE: '#a3e635',
    S: '#22c55e', SO: '#38bdf8', O: '#818cf8', NO: '#c084fc',
  }
  const needleColor = cardinal ? (dirColor[cardinal] || '#ffffff') : '#ffffff'

  return (
    <main style={{
      width: '100vw', minHeight: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'flex-start',
      background: 'linear-gradient(160deg, #050510 0%, #0a0f2e 50%, #050510 100%)',
      color: '#fff', padding: '28px 16px 40px',
      overflowY: 'auto', boxSizing: 'border-box',
    }}>

      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <h1 style={{
          fontSize: 'clamp(22px, 7vw, 32px)', letterSpacing: '6px',
          margin: 0, fontFamily: 'Archeoscope, serif', color: '#a5f3fc',
        }}>
          BRÚJULA
        </h1>
        <p style={{
          fontSize: '11px', color: 'rgba(255,255,255,0.3)',
          letterSpacing: '2px', margin: '6px 0 0',
        }}>
          ORIENTACIÓN MAGNÉTICA EN TIEMPO REAL
        </p>
      </div>

      {/* ── Estado: sin permiso iOS ── */}
      {permission === 'unknown' && typeof window !== 'undefined' && typeof (DeviceOrientationEvent as any).requestPermission === 'function' && (
        <div style={{ textAlign: 'center', maxWidth: '300px' }}>
          <div style={{ fontSize: '64px', marginBottom: '20px' }}>🧭</div>
          <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '15px', lineHeight: '1.7', marginBottom: '24px' }}>
            Para usar la brújula, el dispositivo necesita acceso al sensor de orientación.
          </p>
          <button
            onClick={startCompass}
            style={{
              padding: '16px 40px', fontSize: '16px', fontWeight: 'bold',
              color: '#fff', background: 'rgba(165,243,252,0.1)',
              border: '1.5px solid rgba(165,243,252,0.4)', borderRadius: '12px',
              cursor: 'pointer', letterSpacing: '2px', textTransform: 'uppercase',
              WebkitTapHighlightColor: 'transparent',
            }}
          >
            Activar brújula
          </button>
        </div>
      )}

      {/* ── Estado: denegado ── */}
      {permission === 'denied' && (
        <div style={{
          background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)',
          borderRadius: '16px', padding: '24px', textAlign: 'center', maxWidth: '300px',
        }}>
          <div style={{ fontSize: '36px', marginBottom: '12px' }}>⚠️</div>
          <p style={{ color: '#fca5a5', fontSize: '14px', lineHeight: '1.7' }}>
            Permiso denegado. Habilitá el acceso al sensor de movimiento en Ajustes → Safari → Sensor de movimiento y orientación.
          </p>
        </div>
      )}

      {/* ── Estado: no soportado ── */}
      {permission === 'unsupported' && (
        <div style={{
          background: 'rgba(251,191,36,0.08)', border: '1px solid rgba(251,191,36,0.3)',
          borderRadius: '16px', padding: '24px', textAlign: 'center', maxWidth: '300px',
        }}>
          <div style={{ fontSize: '36px', marginBottom: '12px' }}>📵</div>
          <p style={{ color: '#fde68a', fontSize: '14px', lineHeight: '1.7' }}>
            Este dispositivo no tiene sensor de orientación disponible.
          </p>
        </div>
      )}

      {/* ── Brújula activa ── */}
      {(permission === 'granted' || (permission === 'unknown' && typeof window !== 'undefined' && typeof (DeviceOrientationEvent as any).requestPermission !== 'function')) && (
        <>
          {/* Heading grande */}
          <div style={{ textAlign: 'center', marginBottom: '28px' }}>
            <div style={{
              fontSize: 'clamp(56px, 18vw, 80px)', fontWeight: '200',
              letterSpacing: '-2px', lineHeight: 1,
              color: heading !== null ? needleColor : 'rgba(255,255,255,0.2)',
              transition: 'color 0.3s ease',
              fontVariantNumeric: 'tabular-nums',
            }}>
              {heading !== null ? `${Math.round(heading)}°` : '---°'}
            </div>
            <div style={{
              fontSize: 'clamp(18px, 5vw, 24px)', fontWeight: 'bold',
              color: heading !== null ? needleColor : 'rgba(255,255,255,0.2)',
              letterSpacing: '3px', marginTop: '4px',
              transition: 'color 0.3s ease',
            }}>
              {cardinalLabel || '···'}
            </div>
          </div>

          {/* ── Disco de brújula ── */}
          <div style={{ position: 'relative', width: '260px', height: '260px', marginBottom: '28px' }}>

            {/* Anillo exterior decorativo */}
            <div style={{
              position: 'absolute', inset: 0, borderRadius: '50%',
              background: 'linear-gradient(135deg, rgba(245,240,230,0.06) 0%, rgba(20,20,40,0.9) 100%)',
              border: '2px solid rgba(139,115,85,0.5)',
              boxShadow: '0 0 40px rgba(165,243,252,0.06), inset 0 0 30px rgba(0,0,0,0.5)',
            }} />

            {/* Marcas de grados — rotan con el heading */}
            <div style={{
              position: 'absolute', inset: 0, borderRadius: '50%',
              transform: heading !== null ? `rotate(${-heading}deg)` : 'rotate(0deg)',
              transition: 'transform 0.08s linear',
            }}>
              {Array.from({ length: 72 }).map((_, i) => {
                const angle = i * 5
                const isCardinal = angle % 90 === 0
                const isMajor = angle % 45 === 0
                const isMed = angle % 10 === 0
                const h = isCardinal ? 14 : isMajor ? 10 : isMed ? 7 : 4
                const w = isCardinal ? 2.5 : isMed ? 1.5 : 1
                const dist = 118  // radio desde centro
                const rad = (angle - 90) * Math.PI / 180
                const x = 130 + dist * Math.cos(rad)
                const y = 130 + dist * Math.sin(rad)
                return (
                  <div key={angle} style={{
                    position: 'absolute',
                    width: `${w}px`, height: `${h}px`,
                    background: isCardinal ? '#ef4444' : isMajor ? 'rgba(255,255,255,0.7)' : 'rgba(255,255,255,0.3)',
                    left: `${x}px`, top: `${y}px`,
                    transform: `translate(-50%, -50%) rotate(${angle}deg)`,
                    transformOrigin: 'center bottom',
                    borderRadius: '1px',
                  }} />
                )
              })}

              {/* Letras cardinales */}
              {[
                { label: 'N', angle: 0,   color: '#ef4444', size: '18px', weight: 'bold' },
                { label: 'E', angle: 90,  color: '#e2e8f0', size: '14px', weight: 'bold' },
                { label: 'S', angle: 180, color: '#e2e8f0', size: '14px', weight: 'bold' },
                { label: 'O', angle: 270, color: '#e2e8f0', size: '14px', weight: 'bold' },
                { label: 'NE', angle: 45,  color: 'rgba(255,255,255,0.45)', size: '10px', weight: 'normal' },
                { label: 'SE', angle: 135, color: 'rgba(255,255,255,0.45)', size: '10px', weight: 'normal' },
                { label: 'SO', angle: 225, color: 'rgba(255,255,255,0.45)', size: '10px', weight: 'normal' },
                { label: 'NO', angle: 315, color: 'rgba(255,255,255,0.45)', size: '10px', weight: 'normal' },
              ].map(({ label, angle, color, size, weight }) => {
                const rad = (angle - 90) * Math.PI / 180
                const dist = 100
                const x = 130 + dist * Math.cos(rad)
                const y = 130 + dist * Math.sin(rad)
                return (
                  <div key={label} style={{
                    position: 'absolute', left: `${x}px`, top: `${y}px`,
                    transform: 'translate(-50%, -50%)',
                    color, fontSize: size, fontWeight: weight,
                    fontFamily: '"Cinzel", "Trajan Pro", serif',
                    textShadow: '0 1px 3px rgba(0,0,0,0.8)',
                    userSelect: 'none',
                  }}>
                    {label}
                  </div>
                )
              })}
            </div>

            {/* Aguja — FIJA, siempre apunta arriba (norte) */}
            <div style={{ position: 'absolute', inset: 0 }}>
              {/* Mitad norte — roja */}
              <svg style={{
                position: 'absolute', top: '18px', left: '50%',
                transform: 'translateX(-50%)',
                width: '18px', height: '112px',
                filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.6))',
              }} viewBox="0 0 18 112">
                <path d="M 9 0 L 15 108 L 9 96 L 3 108 Z" fill="#ef4444" stroke="#8b1a2e" strokeWidth="0.8" />
                <path d="M 9 0 L 11 108 L 9 96 L 7 108 Z" fill="#ff6b6b" opacity="0.5" />
              </svg>
              {/* Mitad sur — blanca */}
              <svg style={{
                position: 'absolute', bottom: '18px', left: '50%',
                transform: 'translateX(-50%) rotate(180deg)',
                width: '18px', height: '112px',
                filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.6))',
              }} viewBox="0 0 18 112">
                <path d="M 9 0 L 15 108 L 9 96 L 3 108 Z" fill="rgba(255,255,255,0.85)" stroke="#999" strokeWidth="0.8" />
              </svg>
              {/* Pivote central */}
              <div style={{
                position: 'absolute', top: '50%', left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '14px', height: '14px', borderRadius: '50%',
                background: 'radial-gradient(circle at 35% 35%, #ffd700, #b8860b)',
                border: '2px solid #8b7355',
                boxShadow: '0 2px 6px rgba(0,0,0,0.6)',
                zIndex: 10,
              }} />
            </div>

            {/* Indicador de dirección actual (triángulo arriba) */}
            <div style={{
              position: 'absolute', top: '-10px', left: '50%',
              transform: 'translateX(-50%)',
              width: 0, height: 0,
              borderLeft: '8px solid transparent',
              borderRight: '8px solid transparent',
              borderBottom: `12px solid ${needleColor}`,
              filter: `drop-shadow(0 0 6px ${needleColor})`,
              transition: 'border-bottom-color 0.3s ease',
            }} />
          </div>

          {/* ── Info cards ── */}
          <div style={{
            display: 'grid', gridTemplateColumns: '1fr 1fr',
            gap: '10px', width: '100%', maxWidth: '300px', marginBottom: '20px',
          }}>
            <div style={{
              padding: '14px 12px', textAlign: 'center',
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px',
            }}>
              <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.35)', letterSpacing: '1px', marginBottom: '6px' }}>RUMBO</div>
              <div style={{ fontSize: '22px', fontWeight: 'bold', color: needleColor, fontVariantNumeric: 'tabular-nums' }}>
                {heading !== null ? `${Math.round(heading)}°` : '---'}
              </div>
            </div>
            <div style={{
              padding: '14px 12px', textAlign: 'center',
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px',
            }}>
              <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.35)', letterSpacing: '1px', marginBottom: '6px' }}>DIRECCIÓN</div>
              <div style={{ fontSize: '22px', fontWeight: 'bold', color: needleColor }}>
                {cardinal || '---'}
              </div>
            </div>
            {accuracy !== null && (
              <div style={{
                gridColumn: '1 / -1',
                padding: '10px 12px', textAlign: 'center',
                background: accuracy < 20 ? 'rgba(34,197,94,0.06)' : accuracy < 45 ? 'rgba(251,191,36,0.06)' : 'rgba(239,68,68,0.06)',
                border: `1px solid ${accuracy < 20 ? 'rgba(34,197,94,0.2)' : accuracy < 45 ? 'rgba(251,191,36,0.2)' : 'rgba(239,68,68,0.2)'}`,
                borderRadius: '12px',
              }}>
                <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.35)', letterSpacing: '1px', marginBottom: '4px' }}>PRECISIÓN DEL SENSOR</div>
                <div style={{
                  fontSize: '15px', fontWeight: 'bold',
                  color: accuracy < 20 ? '#22c55e' : accuracy < 45 ? '#fbbf24' : '#ef4444',
                }}>
                  {accuracy < 20 ? '🟢 Alta' : accuracy < 45 ? '🟡 Media' : '🔴 Baja'} · ±{Math.round(accuracy)}°
                </div>
              </div>
            )}
          </div>

          {/* ── Tip de calibración ── */}
          <div style={{
            maxWidth: '300px', width: '100%',
            padding: '14px 16px',
            background: 'rgba(165,243,252,0.04)',
            border: '1px solid rgba(165,243,252,0.12)',
            borderRadius: '12px', marginBottom: '8px',
          }}>
            <div style={{ fontSize: '10px', color: 'rgba(165,243,252,0.5)', letterSpacing: '2px', marginBottom: '8px' }}>
              💡 CALIBRACIÓN
            </div>
            <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)', lineHeight: '1.7', margin: 0 }}>
              Si la brújula parece imprecisa, mové el dispositivo en forma de "8" en el aire durante unos segundos para recalibrar el magnetómetro.
            </p>
          </div>

          {/* ── Nota de precisión ── */}
          <div style={{
            maxWidth: '300px', width: '100%',
            padding: '12px 16px',
            background: 'rgba(255,255,255,0.02)',
            border: '1px solid rgba(255,255,255,0.06)',
            borderRadius: '12px',
          }}>
            <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.25)', letterSpacing: '2px', marginBottom: '6px' }}>
              ℹ️ PRECISIÓN
            </div>
            <p style={{ fontSize: '12px', color: 'rgba(255,255,255,0.3)', lineHeight: '1.7', margin: 0 }}>
              Precisión típica ±5–10°. Puede verse afectada por metales, imanes o fundas magnéticas cercanas al dispositivo.
            </p>
          </div>
        </>
      )}

      {/* Volver */}
      <button
        onClick={() => router.push('/menu')}
        className="btn-responsive"
        style={{ marginTop: '32px' }}
        onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#fff' }}
        onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)' }}
      >
        Volver
      </button>
    </main>
  )
}
