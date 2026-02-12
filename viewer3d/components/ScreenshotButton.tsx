'use client'

import { useState } from 'react'

export default function ScreenshotButton() {
  const [capturing, setCapturing] = useState(false)

  const captureScreenshot = () => {
    setCapturing(true)

    try {
      // Buscar el canvas de Three.js
      const canvas = document.querySelector('canvas')
      
      if (!canvas) {
        console.error('Canvas not found')
        setCapturing(false)
        return
      }

      // Convert to blob and download
      canvas.toBlob((blob) => {
        if (blob) {
          const url = URL.createObjectURL(blob)
          const link = document.createElement('a')
          const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
          link.download = `creador3d-screenshot-${timestamp}.png`
          link.href = url
          link.click()
          URL.revokeObjectURL(url)
          
          // Show success message
          setTimeout(() => setCapturing(false), 1000)
        }
      }, 'image/png')
    } catch (error) {
      console.error('Error capturing screenshot:', error)
      setCapturing(false)
    }
  }

  return (
    <button
      onClick={captureScreenshot}
      disabled={capturing}
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        padding: '14px 20px',
        background: capturing 
          ? 'rgba(74, 222, 128, 0.9)' 
          : 'rgba(59, 130, 246, 0.9)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        borderRadius: '8px',
        color: '#fff',
        cursor: capturing ? 'not-allowed' : 'pointer',
        fontSize: '14px',
        fontWeight: 'bold',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        transition: 'all 0.2s',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
        zIndex: 1000
      }}
      onMouseEnter={(e) => {
        if (!capturing) {
          e.currentTarget.style.background = 'rgba(59, 130, 246, 1)'
          e.currentTarget.style.transform = 'translateY(-2px)'
        }
      }}
      onMouseLeave={(e) => {
        if (!capturing) {
          e.currentTarget.style.background = 'rgba(59, 130, 246, 0.9)'
          e.currentTarget.style.transform = 'translateY(0)'
        }
      }}
    >
      <span style={{ fontSize: '18px' }}>
        {capturing ? '✓' : '📸'}
      </span>
      <span>
        {capturing ? 'Capturado!' : 'Screenshot'}
      </span>
    </button>
  )
}
