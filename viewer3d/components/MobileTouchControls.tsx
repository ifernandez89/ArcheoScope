'use client'

/**
 * MobileTouchControls — D-pad + botones de rotación para mobile
 * 
 * Simula teclas WASD + Q/R para controlar el avatar en escenas terrestres.
 * Q = rotar izquierda, R = rotar derecha (igual que en PC)
 */

import { useEffect, useRef } from 'react'

interface MobileTouchControlsProps {
  visible?: boolean
}

// Simular keydown/keyup directamente — sin estado React para máxima velocidad
function pressKey(key: string) {
  window.dispatchEvent(new KeyboardEvent('keydown', {
    key, code: `Key${key.toUpperCase()}`, bubbles: true, cancelable: true
  }))
}

function releaseKey(key: string) {
  window.dispatchEvent(new KeyboardEvent('keyup', {
    key, code: `Key${key.toUpperCase()}`, bubbles: true, cancelable: true
  }))
}

// Botón individual — componente puro sin hooks internos
function Btn({
  keyCode,
  label,
  size = 44,
  fontSize = 18,
}: {
  keyCode: string
  label: string
  size?: number
  fontSize?: number
}) {
  const style: React.CSSProperties = {
    width: size,
    height: size,
    borderRadius: '50%',
    background: 'rgba(55, 55, 55, 0.9)',
    border: '2px solid rgba(200, 200, 200, 0.6)',
    color: '#fff',
    fontSize,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    userSelect: 'none',
    WebkitUserSelect: 'none',
    touchAction: 'none',
    boxShadow: '0 2px 8px rgba(0,0,0,0.7)',
    flexShrink: 0,
  }

  return (
    <button
      style={style}
      onPointerDown={(e) => { e.preventDefault(); pressKey(keyCode) }}
      onPointerUp={(e) => { e.preventDefault(); releaseKey(keyCode) }}
      onPointerLeave={(e) => { e.preventDefault(); releaseKey(keyCode) }}
      onPointerCancel={(e) => { e.preventDefault(); releaseKey(keyCode) }}
      onContextMenu={(e) => e.preventDefault()}
    >
      {label}
    </button>
  )
}

export default function MobileTouchControls({ visible = true }: MobileTouchControlsProps) {
  // Limpiar teclas al desmontar
  useEffect(() => {
    return () => {
      ['w', 'a', 's', 'd', 'q', 'r'].forEach(releaseKey)
    }
  }, [])

  if (!visible) return null

  return (
    <div style={{
      position: 'fixed',
      top: 96,
      right: 12,
      zIndex: 1000,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 6,
      background: 'rgba(0,0,0,0.45)',
      borderRadius: '18px',
      padding: '10px 8px',
      backdropFilter: 'blur(6px)',
      border: '1px solid rgba(255,255,255,0.1)',
    }}>

      {/* ROTACIÓN — Q (izq) / R (der) — arriba del D-pad */}
      <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
        <Btn keyCode="q" label="↺" fontSize={20} />
        <span style={{ color: '#999', fontSize: '9px', letterSpacing: '1px', minWidth: 20, textAlign: 'center' }}>ROT</span>
        <Btn keyCode="r" label="↻" fontSize={20} />
      </div>

      {/* Separador */}
      <div style={{ width: '90%', height: 1, background: 'rgba(255,255,255,0.12)' }} />

      {/* D-PAD */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 44px)',
        gridTemplateRows: 'repeat(3, 44px)',
        gap: 4,
      }}>
        {/* Fila 1 */}
        <div />
        <Btn keyCode="w" label="▲" />
        <div />
        {/* Fila 2 */}
        <Btn keyCode="a" label="◀" />
        <div />
        <Btn keyCode="d" label="▶" />
        {/* Fila 3 */}
        <div />
        <Btn keyCode="s" label="▼" />
        <div />
      </div>

    </div>
  )
}
