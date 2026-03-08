'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

interface InGameMenuProps {
  isOpen: boolean
  onClose: () => void
}

export default function InGameMenu({ isOpen, onClose }: InGameMenuProps) {
  const router = useRouter()

  // Cerrar con ESC
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }
    window.addEventListener('keydown', handleEsc)
    return () => window.removeEventListener('keydown', handleEsc)
  }, [isOpen, onClose])

  if (!isOpen) return null

  const menuOptions = [
    { label: 'Continuar', action: () => onClose() },
    { label: 'Audio', action: () => router.push('/menu/audio') },
    { label: 'Video', action: () => router.push('/menu/video') },
    { label: 'Información', action: () => router.push('/menu/info') },
    { label: 'Menú Principal', action: () => router.push('/menu') }
  ]

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        background: 'rgba(0, 0, 0, 0.85)',
        backdropFilter: 'blur(10px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
        animation: 'fadeIn 0.2s ease-out'
      }}
      onClick={onClose}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '20px',
          alignItems: 'center'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <h1 style={{
          color: '#ffffff',
          fontSize: '48px',
          margin: '0 0 20px 0',
          letterSpacing: '4px',
          textTransform: 'uppercase'
        }}>
          Menú
        </h1>

        {menuOptions.map((option) => (
          <button
            key={option.label}
            onClick={option.action}
            style={{
              padding: '20px 80px',
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#ffffff',
              background: 'transparent',
              border: '2px solid #ffffff',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              fontFamily: 'inherit',
              letterSpacing: '2px',
              textTransform: 'uppercase',
              minWidth: '350px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#ffffff'
              e.currentTarget.style.color = '#000000'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = '#ffffff'
            }}
          >
            {option.label}
          </button>
        ))}

        <div style={{
          color: '#888888',
          fontSize: '14px',
          marginTop: '20px',
          letterSpacing: '1px'
        }}>
          Presiona ESC o M para cerrar
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }
      `}</style>
    </div>
  )
}
