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
      // ✅ Sin auto-close — el usuario cierra cuando quiera
    } else {
      // Ya le diste el piramidón, mostrar menú de opciones
      setCurrentMessage(sphinxDialogues.menu.text)
      setShowOptions(true)
    }
  }, [pyramidionCollected, hasReceivedPyramidion])

  const handleOptionClick = (optionId: number, response: string) => {
    setSelectedResponse(response)
    setShowOptions(false)
    
    if (onOptionSelected) {
      onOptionSelected(optionId)
    }
    // ✅ Sin auto-close — el usuario cierra cuando quiera
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
          padding: 'clamp(18px, 5vw, 36px)',
          maxWidth: '600px',
          width: '90%',
          maxHeight: '85vh',
          overflowY: 'auto',
          boxShadow: '0 0 30px rgba(255, 215, 0, 0.6)',
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        {/* Icono */}
        <div style={{
          textAlign: 'center',
          marginBottom: 'clamp(8px, 2vw, 14px)',
          fontSize: 'clamp(32px, 8vw, 42px)',
        }}>
          🦁
        </div>

        {/* Nombre */}
        <div style={{
          color: '#ffd700',
          fontSize: 'clamp(18px, 5vw, 22px)',
          fontWeight: 'bold',
          textAlign: 'center',
          marginBottom: 'clamp(12px, 3vw, 20px)',
          fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
          letterSpacing: '3px',
          textShadow: '0 0 12px rgba(255, 215, 0, 0.7)',
        }}>
          La Esfinge
        </div>

        {/* Mensaje principal */}
        <div
          style={{
            color: '#ffffff',
            fontSize: 'clamp(14px, 3.5vw, 18px)',
            fontWeight: 'normal',
            textAlign: 'center',
            marginBottom: showOptions ? 'clamp(16px, 4vw, 25px)' : '0',
            fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
            letterSpacing: '1px',
            lineHeight: '1.8',
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
              gap: 'clamp(10px, 2.5vw, 15px)'
            }}
          >
            {sphinxDialogues.menu.options.map((option) => (
              <button
                key={option.id}
                onClick={() => handleOptionClick(option.id, option.response)}
                style={{
                  padding: 'clamp(12px, 3vw, 15px) clamp(16px, 4vw, 25px)',
                  fontSize: 'clamp(13px, 3.5vw, 18px)',
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
              fontSize: 'clamp(14px, 3.5vw, 16px)',
              color: '#ffd700',
              background: 'transparent',
              border: '2px solid #ffd700',
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
