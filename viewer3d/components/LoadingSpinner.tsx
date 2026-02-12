'use client'

import { Html, useProgress } from '@react-three/drei'

export default function LoadingSpinner() {
  const { progress } = useProgress()
  
  return (
    <Html center>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '1rem',
        color: '#ffffff',
        fontFamily: 'monospace'
      }}>
        <div style={{
          width: '60px',
          height: '60px',
          border: '4px solid rgba(255, 255, 255, 0.1)',
          borderTop: '4px solid #ffffff',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
        <div style={{ fontSize: '14px' }}>
          Cargando modelo... {progress.toFixed(0)}%
        </div>
        <style jsx>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    </Html>
  )
}
