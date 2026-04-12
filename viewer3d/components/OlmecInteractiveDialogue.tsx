'use client'

import { useState, useEffect } from 'react'

interface OlmecInteractiveDialogueProps {
  hasStoodUp: boolean
  hasJadeMask?: boolean
  missionCompleted?: boolean
  onClose: () => void
  onEnterCave?: () => void
  onDeliverJade?: () => void
}

const OLMEC_OPTIONS = [
  {
    id: 1,
    label: '¿Qué necesitas de mí?',
    response: 'Viajero... En las profundidades del Mictlán yace el Jade del Aliento, una piedra que guarda el soplo de vida de los antiguos. Atraviesa la cueva y tráemelo.'
  },
  {
    id: 2,
    label: '¿Qué hay dentro de la cueva?',
    response: 'La cueva es un lugar de prueba para el espíritu. Antiguos la usaban como portal entre el mundo de los vivos y el de los muertos. Solo los valientes se atreven a cruzar.'
  },
  {
    id: 3,
    label: '¿Quién es Mictlantecuhtli?',
    response: 'Mictlantecuhtli gobierna el Mictlán, el nivel más profundo del mundo de los muertos. Su rostro es un cráneo descarnado, y su dominio se extiende por las nueve capas del inframundo. No lo busques... a menos que estés preparado.'
  }
]

const OLMEC_OPTIONS_COMPLETED = [
  {
    id: 1,
    label: '¿Qué es la Máscara de Jade?',
    response: 'La Máscara de Jade representa el aliento de vida. El jade era más valioso que el oro, simbolizaba la eternidad, el agua y la vegetación. Los gobernantes la usaban para comunicarse con los dioses y asegurar su paso al más allá.'
  },
  {
    id: 2,
    label: '¿Qué hay dentro de la cueva?',
    response: 'La cueva es un lugar de prueba para el espíritu. Antiguos la usaban como portal entre el mundo de los vivos y el de los muertos. Solo los valientes se atreven a cruzar.'
  },
  {
    id: 3,
    label: '¿Quién es Mictlantecuhtli?',
    response: 'Mictlantecuhtli gobierna el Mictlán, el nivel más profundo del mundo de los muertos. Su rostro es un cráneo descarnado, y su dominio se extiende por las nueve capas del inframundo. No lo busques... a menos que estés preparado.'
  }
]

export default function OlmecInteractiveDialogue({ 
  hasStoodUp,
  hasJadeMask,
  missionCompleted,
  onClose,
  onEnterCave,
  onDeliverJade
}: OlmecInteractiveDialogueProps) {
  const [currentMessage, setCurrentMessage] = useState('')
  const [showOptions, setShowOptions] = useState(false)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)

  useEffect(() => {
    if (!hasStoodUp) {
      setCurrentMessage('Gracias, viajero de las estrellas... Dormia desde hace milenios. Te saludo desde el principio de los tiempos.')
      setShowOptions(false)
      setTimeout(() => onClose(), 5000)
    } else if (hasJadeMask) {
      setCurrentMessage('Siento la energia del Jade del Aliento... ¿Me lo entregas, viajero?')
      setShowOptions(true)
    } else {
      setCurrentMessage('¿Que deseas?')
      setShowOptions(true)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasStoodUp, hasJadeMask])

  const handleOptionClick = (optionId: number, response: string) => {
    setSelectedResponse(response)
    setShowOptions(false)

    // Si eligió la opción 1 y la misión NO está completada, activar cueva después de mostrar respuesta
    if (optionId === 1 && onEnterCave && !missionCompleted) {
      setTimeout(() => {
        if (onEnterCave) onEnterCave()
      }, 3000) // Dar tiempo a leer la respuesta
      setTimeout(() => onClose(), 5000)
      return
    }

    setTimeout(() => onClose(), 5000)
  }

  const accentColor = '#c8860a'

  return (
    <div
      style={{
        position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
        background: 'rgba(0, 0, 0, 0.75)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 2000, animation: 'fadeIn 0.3s ease-out'
      }}
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: 'rgba(20, 15, 10, 0.95)',
          border: `2px solid ${accentColor}`,
          borderRadius: '12px',
          padding: '30px 40px',
          maxWidth: '620px',
          width: '90%',
          boxShadow: `0 0 30px rgba(200, 134, 10, 0.6)`,
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        {/* Icono */}
        <div style={{ textAlign: 'center', marginBottom: '15px', fontSize: '42px' }}></div>

        {/* Título */}
        <div style={{
          color: accentColor, fontSize: '22px', fontWeight: 'bold',
          textAlign: 'center', marginBottom: '20px',
          fontFamily: '"Cinzel", serif', letterSpacing: '3px',
          textShadow: `0 0 10px rgba(200, 134, 10, 0.8)`,
        }}>
        </div>

        {/* Mensaje */}
        <div style={{
          color: '#fff', fontSize: '18px', textAlign: 'center',
          marginBottom: showOptions ? '25px' : '0',
          fontFamily: '"Cinzel", serif', letterSpacing: '1px',
          lineHeight: '1.6', textShadow: `0 0 5px rgba(200, 134, 10, 0.3)`,
        }}>
          {selectedResponse || currentMessage}
        </div>

        {/* Opciones */}
        {showOptions && !selectedResponse && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {/* Opción especial: entregar jade */}
            {hasJadeMask && (
              <button
                onClick={() => {
                  setSelectedResponse('Gracias, viajero... El Jade del Aliento regresa a su lugar sagrado. Los antiguos te bendicen.')
                  setShowOptions(false)
                  if (onDeliverJade) onDeliverJade()
                  setTimeout(() => onClose(), 6000)
                }}
                style={{
                  padding: '14px 22px', fontSize: '16px',
                  color: '#00ff88',
                  background: 'rgba(0, 255, 136, 0.1)',
                  border: '2px solid #00ff88',
                  borderRadius: '8px', cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  fontFamily: '"Cinzel", serif', letterSpacing: '1px',
                  textAlign: 'left', fontWeight: 'bold'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.background = 'rgba(0,255,136,0.3)'; e.currentTarget.style.transform = 'translateX(8px)' }}
                onMouseLeave={(e) => { e.currentTarget.style.background = 'rgba(0,255,136,0.1)'; e.currentTarget.style.transform = 'translateX(0)' }}
              >
                Entregar la Mascara de Jade
              </button>
            )}
            {!hasJadeMask && (missionCompleted ? OLMEC_OPTIONS_COMPLETED : OLMEC_OPTIONS).map((opt) => (
              <button
                key={opt.id}
                onClick={() => handleOptionClick(opt.id, opt.response)}
                style={{
                  padding: '14px 22px', fontSize: '16px',
                  color: accentColor,
                  background: `rgba(200, 134, 10, 0.1)`,
                  border: `2px solid ${accentColor}`,
                  borderRadius: '8px', cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  fontFamily: '"Cinzel", serif', letterSpacing: '1px',
                  textAlign: 'left'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(200, 134, 10, 0.3)'
                  e.currentTarget.style.transform = 'translateX(8px)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(200, 134, 10, 0.1)'
                  e.currentTarget.style.transform = 'translateX(0)'
                }}
              >
                {opt.id}. {opt.label}
              </button>
            ))}
          </div>
        )}

        {/* Botón cerrar */}
        {(!showOptions || selectedResponse) && (
          <button
            onClick={onClose}
            style={{
              marginTop: '20px', padding: '10px 30px', fontSize: '15px',
              color: accentColor, background: 'transparent',
              border: `2px solid ${accentColor}`, borderRadius: '8px',
              cursor: 'pointer', fontFamily: '"Cinzel", serif',
              letterSpacing: '2px', display: 'block', margin: '20px auto 0',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => { e.currentTarget.style.background = accentColor; e.currentTarget.style.color = '#000' }}
            onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = accentColor }}
          >
            Cerrar
          </button>
        )}
      </div>

      <style jsx>{`
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes scaleIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
      `}</style>
    </div>
  )
}
