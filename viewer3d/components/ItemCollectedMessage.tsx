'use client'

import { useEffect } from 'react'

interface ItemCollectedMessageProps {
  onClose: () => void
}

export default function ItemCollectedMessage({ onClose }: ItemCollectedMessageProps) {
  useEffect(() => {
    // Auto-cerrar después de 3 segundos
    const timer = setTimeout(() => {
      onClose()
    }, 3000)

    return () => clearTimeout(timer)
  }, [onClose])

  return (
    <div
      style={{
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        padding: '30px 60px',
        borderRadius: '12px',
        border: '2px solid rgba(255, 215, 0, 0.5)',
        boxShadow: '0 0 30px rgba(255, 215, 0, 0.3)',
        zIndex: 10000,
        animation: 'fadeInScale 0.3s ease-out'
      }}
    >
      <div
        style={{
          fontSize: '1.5rem',
          fontWeight: 'bold',
          color: '#ffd700',
          textAlign: 'center',
          textShadow: '0 0 10px rgba(255, 215, 0, 0.5)'
        }}
      >
        ¡Adquiriste un nuevo item!
      </div>

      <style jsx>{`
        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.8);
          }
          to {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
          }
        }
      `}</style>
    </div>
  )
}
