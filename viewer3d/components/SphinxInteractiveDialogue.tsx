'use client'

import { useState, useEffect } from 'react'
import sphinxDialogues from '@/data/sphinxDialogues.json'

interface SphinxInteractiveDialogueProps {
  pyramidionCollected: boolean
  hasReceivedPyramidion: boolean
  onClose: () => void
  onOptionSelected?: (optionId: number) => void
}

export default function SphinxInteractiveDialogue({ 
  pyramidionCollected, 
  hasReceivedPyramidion,
  onClose,
  onOptionSelected 
}: SphinxInteractiveDialogueProps) {
  const [currentMessage, setCurrentMessage] = useState('')
  const [showOptions, setShowOptions] = useState(false)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)

  useEffect(() => {
    // Determinar qué mensaje mostrar
    if (!pyramidionCollected) {
      // Antes de recoger el piramidón
      setCurrentMessage(sphinxDialogues.initial.text)
      setShowOptions(false)
    } else if (pyramidionCollected && !hasReceivedPyramidion) {
      // Primera vez que hablas después de recoger el piramidón
      setCurrentMessage(sphinxDialogues.gratitude.text)
      setShowOptions(false)
      
      // Después de 3 segundos, cerrar automáticamente
      setTimeout(() => {
        onClose()
      }, 3000)
    } else {
      // Ya le diste el piramidón, mostrar menú de opciones
      setCurrentMessage(sphinxDialogues.menu.text)
      setShowOptions(true)
    }
  }, [pyramidionCollected, hasReceivedPyramidion, onClose])

  const handleOptionClick = (optionId: number, response: string) => {
    setSelectedResponse(response)
    setShowOptions(false)
    
    if (onOptionSelected) {
      onOptionSelected(optionId)
    }

    // Después de 4 segundos, cerrar el diálogo
    setTimeout(() => {
      onClose()
    }, 4000)
  }

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
          background: 'rgba(20, 20, 40, 0.95)',
          border: '2px solid #ffd700',
          borderRadius: '12px',
          padding: '30px 40px',
          maxWidth: '600px',
          width: '90%',
          boxShadow: '0 0 30px rgba(255, 215, 0, 0.6)',
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        {/* Mensaje principal */}
        <div
          style={{
            color: '#ffffff',
            fontSize: '24px',
            fontWeight: 'normal',
            textAlign: 'center',
            marginBottom: showOptions ? '30px' : '0',
            fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
            letterSpacing: '2px',
            textShadow: '0 0 10px rgba(255, 215, 0, 0.5)',
          }}
        >
          {selectedResponse || currentMessage}
        </div>

        {/* Opciones interactivas */}
        {showOptions && !selectedResponse && (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '15px'
            }}
          >
            {sphinxDialogues.menu.options.map((option) => (
              <button
                key={option.id}
                onClick={() => handleOptionClick(option.id, option.response)}
                style={{
                  padding: '15px 25px',
                  fontSize: '18px',
                  color: '#ffd700',
                  background: 'rgba(255, 215, 0, 0.1)',
                  border: '2px solid #ffd700',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
                  letterSpacing: '1px',
                  textAlign: 'left'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 215, 0, 0.3)'
                  e.currentTarget.style.transform = 'translateX(10px)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 215, 0, 0.1)'
                  e.currentTarget.style.transform = 'translateX(0)'
                }}
              >
                {option.id}. {option.label}
              </button>
            ))}
          </div>
        )}

        {/* Botón cerrar (solo si no hay opciones o ya se seleccionó una) */}
        {(!showOptions || selectedResponse) && (
          <button
            onClick={onClose}
            style={{
              marginTop: '20px',
              padding: '10px 30px',
              fontSize: '16px',
              color: '#ffd700',
              background: 'transparent',
              border: '2px solid #ffd700',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
              letterSpacing: '2px',
              display: 'block',
              margin: '20px auto 0'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#ffd700'
              e.currentTarget.style.color = '#000000'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = '#ffd700'
            }}
          >
            Cerrar
          </button>
        )}
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
