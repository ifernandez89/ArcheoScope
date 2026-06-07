'use client'

import { useEffect, useState } from 'react'
import type { DiscoveryToast as ToastData } from '@/systems/discoveryToasts'

interface DiscoveryToastProps {
  toast: ToastData | null
  onDismiss: () => void
}

/**
 * Toast de descubrimiento — minimalista, no intrusivo.
 * Aparece abajo-centro, se desvanece solo tras 7s, también se puede tocar para cerrar.
 */
export default function DiscoveryToast({ toast, onDismiss }: DiscoveryToastProps) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (!toast) return
    setVisible(true)
    const fadeTimer = setTimeout(() => setVisible(false), 6500)
    const removeTimer = setTimeout(() => onDismiss(), 7000)
    // ⛑️ Timeout de seguridad: fuerza dismiss si algo falla (ej: re-render congelado)
    const safetyTimer = setTimeout(() => {
      setVisible(false)
      onDismiss()
    }, 8500)
    return () => {
      clearTimeout(fadeTimer)
      clearTimeout(removeTimer)
      clearTimeout(safetyTimer)
    }
  }, [toast]) // eslint-disable-line react-hooks/exhaustive-deps
  // Nota: onDismiss excluido intencionalmente para evitar re-triggers por cambio de referencia

  if (!toast) return null

  return (
    <div
      onClick={() => { setVisible(false); setTimeout(onDismiss, 300) }}
      style={{
        position: 'fixed',
        bottom: '28px',
        left: '50%',
        transform: `translateX(-50%) translateY(${visible ? '0' : '12px'})`,
        opacity: visible ? 1 : 0,
        transition: 'opacity 0.4s ease, transform 0.4s ease',
        zIndex: 1500,
        maxWidth: 'min(420px, 88vw)',
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '12px 18px',
        background: 'rgba(10, 12, 24, 0.85)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        border: '1px solid rgba(167, 139, 250, 0.25)',
        borderRadius: '14px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
        cursor: 'pointer',
        pointerEvents: 'auto',
      }}
    >
      <span style={{ fontSize: '22px', flexShrink: 0 }}>{toast.icon}</span>
      <span style={{
        fontSize: 'clamp(13px, 3vw, 14px)',
        color: 'rgba(255, 255, 255, 0.85)',
        lineHeight: 1.45,
        fontFamily: 'var(--font-inter), sans-serif',
      }}>
        {toast.text}
      </span>
    </div>
  )
}
