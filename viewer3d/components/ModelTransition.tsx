'use client'

import { useState, useEffect } from 'react'

interface ModelTransitionProps {
  modelName: string
}

export default function ModelTransition({ modelName }: ModelTransitionProps) {
  const [show, setShow] = useState(false)
  const [displayName, setDisplayName] = useState('')

  useEffect(() => {
    // Extraer nombre del modelo del path
    const name = modelName.split('/').pop()?.replace('.glb', '') || ''
    const formattedName = name.charAt(0).toUpperCase() + name.slice(1)
    
    setDisplayName(formattedName)
    setShow(true)

    const timer = setTimeout(() => {
      setShow(false)
    }, 2000)

    return () => clearTimeout(timer)
  }, [modelName])

  if (!show) return null

  return (
    <>
      <style jsx>{`
        @keyframes fadeInOut {
          0% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.9);
          }
          20% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
          }
          80% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
          }
          100% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.9);
          }
        }
        
        @keyframes shimmer {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(100%);
          }
        }
        
        .transition-container {
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          padding: 24px 48px;
          background: rgba(10, 10, 10, 0.95);
          backdrop-filter: blur(20px);
          border: 2px solid rgba(102, 126, 234, 0.5);
          border-radius: 16px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
          z-index: 2000;
          animation: fadeInOut 2s ease-in-out;
          pointer-events: none;
        }
        
        .progress-bar {
          margin-top: 16px;
          height: 3px;
          background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
          border-radius: 2px;
          animation: shimmer 1.5s infinite;
        }
      `}</style>

      <div className="transition-container">
        <div style={{
          fontSize: '14px',
          color: '#888',
          marginBottom: '8px',
          textAlign: 'center',
          textTransform: 'uppercase',
          letterSpacing: '2px'
        }}>
          Cargando Modelo
        </div>

        <div style={{
          fontSize: '32px',
          fontWeight: 'bold',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          textAlign: 'center'
        }}>
          {displayName}
        </div>

        <div className="progress-bar" />
      </div>
    </>
  )
}
