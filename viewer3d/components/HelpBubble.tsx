'use client'

import { useState, useEffect } from 'react'
import { isHelpEnabled } from '@/systems/helpSystem'

export interface HelpTip {
  icon: string
  title: string
  tip: string
}

interface HelpBubbleProps {
  tip: HelpTip
  /** Posición en pantalla (px desde top-left). Si no se pasa, se centra en pantalla */
  screenX?: number
  screenY?: number
  /** Forzar visibilidad (para testing) */
  forceVisible?: boolean
}

/**
 * Botón flotante de ayuda + diálogo desplegable.
 * Se muestra cuando el jugador está cerca de un objeto con tip registrado.
 */
export default function HelpBubble({ tip, screenX, screenY, forceVisible }: HelpBubbleProps) {
  const [open, setOpen] = useState(false)
  const [helpOn, setHelpOn] = useState(true)
  const [pulse, setPulse] = useState(false)

  useEffect(() => {
    setHelpOn(isHelpEnabled())
    const handler = (e: Event) => {
      setHelpOn((e as CustomEvent).detail.enabled)
    }
    window.addEventListener('help-toggle', handler)
    return () => window.removeEventListener('help-toggle', handler)
  }, [])

  // Pulso de entrada al aparecer
  useEffect(() => {
    setPulse(true)
    const t = setTimeout(() => setPulse(false), 600)
    return () => clearTimeout(t)
  }, [tip])

  if (!helpOn && !forceVisible) return null

  // Posición del botón
  const btnStyle: React.CSSProperties = screenX !== undefined && screenY !== undefined
    ? {
        position: 'fixed',
        left: `${screenX}px`,
        top: `${screenY}px`,
        transform: 'translate(-50%, -50%)',
        zIndex: 500,
      }
    : {
        position: 'fixed',
        bottom: '120px',
        right: '24px',
        zIndex: 500,
      }

  return (
    <>
      <style>{`
        @keyframes helpPop {
          0%   { transform: translate(-50%,-50%) scale(0.5); opacity: 0 }
          60%  { transform: translate(-50%,-50%) scale(1.15); opacity: 1 }
          100% { transform: translate(-50%,-50%) scale(1); opacity: 1 }
        }
        @keyframes helpPulse {
          0%,100% { box-shadow: 0 0 0 0 rgba(251,191,36,0.7), 0 4px 16px rgba(0,0,0,0.5) }
          50%     { box-shadow: 0 0 0 10px rgba(251,191,36,0), 0 4px 16px rgba(0,0,0,0.5) }
        }
        @keyframes helpIdle {
          0%,100% { box-shadow: 0 0 0 0 rgba(251,191,36,0.4), 0 4px 16px rgba(0,0,0,0.5) }
          50%     { box-shadow: 0 0 0 6px rgba(251,191,36,0), 0 4px 16px rgba(0,0,0,0.5) }
        }
        @keyframes dialogSlide {
          from { opacity: 0; transform: translateY(8px) scale(0.97) }
          to   { opacity: 1; transform: translateY(0) scale(1) }
        }
      `}</style>

      {/* Botón de ayuda */}
      <div style={btnStyle}>
        <button
          onClick={() => setOpen(o => !o)}
          title={`Ayuda: ${tip.title}`}
          style={{
            width: '48px', height: '48px', borderRadius: '50%',
            background: open
              ? 'linear-gradient(135deg, #fbbf24, #f59e0b)'
              : 'linear-gradient(135deg, #1e293b, #0f172a)',
            border: `2.5px solid ${open ? '#fbbf24' : 'rgba(251,191,36,0.7)'}`,
            cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '22px', color: '#fff',
            animation: pulse
              ? 'helpPop 0.6s ease-out, helpPulse 1.2s ease-in-out 0.6s 2'
              : 'helpIdle 2.5s ease-in-out infinite',
            WebkitTapHighlightColor: 'transparent',
            touchAction: 'manipulation',
            transition: 'background 0.2s, border-color 0.2s',
          }}
        >
          {open ? '✕' : '?'}
        </button>
      </div>

      {/* Diálogo de ayuda */}
      {open && (
        <div style={{
          position: 'fixed',
          ...(screenX !== undefined && screenY !== undefined
            ? { left: `${screenX}px`, top: `${screenY - 70}px`, transform: 'translate(-50%, -100%)' }
            : { bottom: '180px', right: '16px' }
          ),
          zIndex: 501,
          maxWidth: '260px', width: 'max-content',
          background: 'linear-gradient(135deg, rgba(15,23,42,0.97), rgba(30,41,59,0.97))',
          border: '1.5px solid rgba(251,191,36,0.4)',
          borderRadius: '14px',
          padding: '14px 16px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.6), 0 0 20px rgba(251,191,36,0.08)',
          animation: 'dialogSlide 0.2s ease-out',
          pointerEvents: 'auto',
        }}>
          {/* Header */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <span style={{ fontSize: '20px' }}>{tip.icon}</span>
            <span style={{
              fontSize: '13px', fontWeight: 'bold', color: '#fbbf24',
              letterSpacing: '1px', textTransform: 'uppercase',
            }}>
              {tip.title}
            </span>
          </div>
          {/* Tip */}
          <p style={{
            margin: 0, fontSize: '13px', color: 'rgba(255,255,255,0.8)',
            lineHeight: '1.6',
          }}>
            {tip.tip}
          </p>
          {/* Flecha decorativa */}
          <div style={{
            position: 'absolute', bottom: '-8px', right: '20px',
            width: 0, height: 0,
            borderLeft: '8px solid transparent',
            borderRight: '8px solid transparent',
            borderTop: '8px solid rgba(251,191,36,0.4)',
          }} />
        </div>
      )}
    </>
  )
}
