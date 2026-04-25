'use client'

/**
 * MobileTouchControls — D-pad + botones de rotación para mobile
 * 
 * Simula teclas WASD + Q/E para controlar el avatar en escenas terrestres.
 * Se coloca debajo de la brújula, mismo tamaño aproximado.
 */

import { useCallback, useRef, useEffect } from 'react'

interface MobileTouchControlsProps {
  visible?: boolean
}

export default function MobileTouchControls({ visible = true }: MobileTouchControlsProps) {
  // Refs para tracking de teclas activas (evitar eventos duplicados)
  const activeKeys = useRef<Set<string>>(new Set())

  // Simular keydown/keyup
  const fireKey = useCallback((key: string, down: boolean) => {
    const code = key === ' ' ? 'Space' : `Key${key.toUpperCase()}`
    const eventType = down ? 'keydown' : 'keyup'
    
    // Evitar eventos duplicados
    if (down && activeKeys.current.has(key)) return
    if (!down && !activeKeys.current.has(key)) return
    
    if (down) {
      activeKeys.current.add(key)
    } else {
      activeKeys.current.delete(key)
    }
    
    const ev = new KeyboardEvent(eventType, {
      key,
      code,
      bubbles: true,
      cancelable: true
    })
    window.dispatchEvent(ev)
  }, [])

  // Limpiar todas las teclas al desmontar
  useEffect(() => {
    return () => {
      activeKeys.current.forEach(key => fireKey(key, false))
    }
  }, [fireKey])

  if (!visible) return null

  // Estilos de botones — fondo gris visible siempre
  const btnBase: React.CSSProperties = {
    width: 44,
    height: 44,
    borderRadius: '50%',
    background: 'rgba(60, 60, 60, 0.85)',
    border: '2px solid rgba(180, 180, 180, 0.7)',
    color: '#ffffff',
    fontSize: '18px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    userSelect: 'none',
    WebkitUserSelect: 'none',
    touchAction: 'manipulation',
    boxShadow: '0 2px 6px rgba(0,0,0,0.6)',
  }

  const btnActive: React.CSSProperties = {
    ...btnBase,
    background: 'rgba(74, 158, 255, 0.5)',
    border: '2px solid rgba(74, 158, 255, 0.8)',
  }

  // Componente de botón con touch events
  const ControlButton = ({ 
    keyCode, 
    label, 
    style 
  }: { 
    keyCode: string
    label: string
    style?: React.CSSProperties 
  }) => {
    const pressed = useRef(false)

    const handleStart = useCallback((e: React.TouchEvent | React.MouseEvent) => {
      e.preventDefault()
      if (!pressed.current) {
        pressed.current = true
        fireKey(keyCode, true)
      }
    }, [keyCode])

    const handleEnd = useCallback((e: React.TouchEvent | React.MouseEvent) => {
      e.preventDefault()
      if (pressed.current) {
        pressed.current = false
        fireKey(keyCode, false)
      }
    }, [keyCode])

    return (
      <button
        style={{ ...btnBase, ...style }}
        onTouchStart={handleStart}
        onTouchEnd={handleEnd}
        onTouchCancel={handleEnd}
        onMouseDown={handleStart}
        onMouseUp={handleEnd}
        onMouseLeave={handleEnd}
        onContextMenu={(e) => e.preventDefault()}
      >
        {label}
      </button>
    )
  }

  return (
    <div style={{
      position: 'fixed',
      top: 100,
      right: 16,
      zIndex: 1000,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 8,
      pointerEvents: 'auto',
      background: 'rgba(0,0,0,0.35)',
      borderRadius: '16px',
      padding: '10px 8px',
      backdropFilter: 'blur(4px)',
    }}>
      {/* ROTACIÓN: Q / E — arriba del D-pad */}
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <ControlButton keyCode="q" label="↺" style={{ fontSize: '20px' }} />
        <span style={{ color: '#aaa', fontSize: '9px', letterSpacing: '1px' }}>ROT</span>
        <ControlButton keyCode="e" label="↻" style={{ fontSize: '20px' }} />
      </div>

      {/* Separador */}
      <div style={{ width: '100%', height: 1, background: 'rgba(255,255,255,0.15)' }} />

      {/* D-PAD: Arriba/Abajo/Izq/Der */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 44px)',
        gridTemplateRows: 'repeat(3, 44px)',
        gap: 4,
      }}>
        <div />
        <ControlButton keyCode="w" label="▲" />
        <div />
        <ControlButton keyCode="a" label="◀" />
        <div />
        <ControlButton keyCode="d" label="▶" />
        <div />
        <ControlButton keyCode="s" label="▼" />
        <div />
      </div>
    </div>
  )
}
