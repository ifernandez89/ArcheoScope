'use client'

import { useState, useEffect } from 'react'

interface QuetzalcoatlDialogueProps {
  hasCornSeed: boolean
  hasPlantedCorn: boolean
  onClose: () => void
  onRequestSeed: () => void
}

export default function QuetzalcoatlDialogue({ 
  hasCornSeed,
  hasPlantedCorn,
  onClose,
  onRequestSeed
}: QuetzalcoatlDialogueProps) {
  const [currentMessage, setCurrentMessage] = useState('')
  const [showOptions, setShowOptions] = useState(false)

  useEffect(() => {
    if (!hasCornSeed && !hasPlantedCorn) {
      setCurrentMessage('🌽 Viajero de las estrellas... El maíz es el regalo de los dioses a la humanidad. Busca la semilla sagrada y plántala en la tierra fértil.')
      setShowOptions(false)
      onRequestSeed()
      // ✅ Sin auto-close — el usuario cierra cuando quiera
    } else if (hasCornSeed && !hasPlantedCorn) {
      setCurrentMessage('🌱 Veo que has encontrado la semilla sagrada. Ahora debes plantarla en la tierra para completar el ciclo de la vida.')
      setShowOptions(false)
      // ✅ Sin auto-close — el usuario cierra cuando quiera
    } else {
      setCurrentMessage('🌾 ¡Viajero de las estrellas! Has completado el ciclo sagrado del maíz. Los dioses están complacidos. La tormenta cesa y la abundancia fluirá sobre estas tierras.')
      setShowOptions(false)
      // ✅ Sin auto-close — el usuario cierra cuando quiera
    }
  }, [hasCornSeed, hasPlantedCorn, onClose, onRequestSeed])

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 2000,
        animation: 'fadeIn 0.3s ease-out'
      }}
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: 'rgba(20, 40, 20, 0.95)',
          border: '2px solid #7cfc00',
          borderRadius: '12px',
          padding: 'clamp(18px, 5vw, 36px)',
          maxWidth: '600px',
          width: '90%',
          maxHeight: '85vh',
          overflowY: 'auto',
          boxShadow: '0 0 30px rgba(124, 252, 0, 0.6)',
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        {/* Icono de Quetzalcoatl */}
        <div style={{ textAlign: 'center', marginBottom: 'clamp(12px, 3vw, 20px)', fontSize: 'clamp(36px, 9vw, 48px)' }}>
          🐍
        </div>
        
        {/* Nombre */}
        <div
          style={{
            color: '#7cfc00',
            fontSize: 'clamp(18px, 5vw, 22px)',
            fontWeight: 'bold',
            textAlign: 'center',
            marginBottom: 'clamp(12px, 3vw, 20px)',
            fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
            letterSpacing: '3px',
            textShadow: '0 0 10px rgba(124, 252, 0, 0.8)',
          }}
        >
          Quetzalcóatl
        </div>

        {/* Mensaje principal */}
        <div
          style={{
            color: '#ffffff',
            fontSize: 'clamp(14px, 3.5vw, 18px)',
            fontWeight: 'normal',
            textAlign: 'center',
            marginBottom: 'clamp(12px, 3vw, 20px)',
            fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
            letterSpacing: '1px',
            lineHeight: '1.8',
            textShadow: '0 0 5px rgba(124, 252, 0, 0.3)',
          }}
        >
          {currentMessage}
        </div>

        {/* Botón cerrar */}
        <button
          onClick={onClose}
          style={{
            marginTop: '20px',
            padding: '10px 30px',
            fontSize: 'clamp(14px, 3.5vw, 16px)',
            color: '#7cfc00',
            background: 'transparent',
            border: '2px solid #7cfc00',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
            letterSpacing: '2px',
            display: 'block',
            margin: '20px auto 0',
            minHeight: '44px'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#7cfc00'
            e.currentTarget.style.color = '#000000'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'transparent'
            e.currentTarget.style.color = '#7cfc00'
          }}
        >
          Cerrar
        </button>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes scaleIn {
          from {
            opacity: 0;
            transform: scale(0.9);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }
      `}</style>
    </div>
  )
}
