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
      // Primera vez - pedir que plante la semilla
      setCurrentMessage('🌽 Viajero de las estrellas... El maíz es el regalo de los dioses a la humanidad. Busca la semilla sagrada y plántala en la tierra fértil.')
      setShowOptions(false)
      onRequestSeed()
      
      setTimeout(() => {
        onClose()
      }, 5000)
    } else if (hasCornSeed && !hasPlantedCorn) {
      // Tiene la semilla pero no la ha plantado
      setCurrentMessage('🌱 Veo que has encontrado la semilla sagrada. Ahora debes plantarla en la tierra para completar el ciclo de la vida.')
      setShowOptions(false)
      
      setTimeout(() => {
        onClose()
      }, 4000)
    } else {
      // Ya plantó el maíz - agradecimiento
      setCurrentMessage('🌾 ¡Viajero de las estrellas! Has completado el ciclo sagrado del maíz. Los dioses están complacidos. La tormenta cesa y la abundancia fluirá sobre estas tierras.')
      setShowOptions(false)
      setTimeout(() => {
        onClose()
      }, 6000)
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
          padding: '30px 40px',
          maxWidth: '600px',
          width: '90%',
          boxShadow: '0 0 30px rgba(124, 252, 0, 0.6)',
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        {/* Icono de Quetzalcoatl */}
        <div style={{ textAlign: 'center', marginBottom: '20px', fontSize: '48px' }}>
          🐍
        </div>
        
        {/* Nombre */}
        <div
          style={{
            color: '#7cfc00',
            fontSize: '28px',
            fontWeight: 'bold',
            textAlign: 'center',
            marginBottom: '20px',
            fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
            letterSpacing: '3px',
            textShadow: '0 0 10px rgba(124, 252, 0, 0.8)',
          }}
        >
        </div>

        {/* Mensaje principal */}
        <div
          style={{
            color: '#ffffff',
            fontSize: '20px',
            fontWeight: 'normal',
            textAlign: 'center',
            marginBottom: '20px',
            fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
            letterSpacing: '1px',
            lineHeight: '1.6',
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
            fontSize: '16px',
            color: '#7cfc00',
            background: 'transparent',
            border: '2px solid #7cfc00',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
            letterSpacing: '2px',
            display: 'block',
            margin: '20px auto 0'
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
