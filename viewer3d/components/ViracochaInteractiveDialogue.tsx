'use client'

import { useState, useEffect } from 'react'

interface ViracochaInteractiveDialogueProps {
  missionCompleted: boolean
  allMissionsCompleted: boolean
  magnaBowlReturned: boolean      // true = ya devolvió la fuente y Viracocha agradeció
  onClose: () => void
  onLendMagnaBowl?: () => void
}

const ACCENT = '#ffd700'

const OPTIONS = [
  { id: 1, label: '¿Qué debo hacer?' },
  { id: 2, label: '¿Qué es la Fuente Magna?' },
  { id: 3, label: '¿Me prestas la Fuente Magna?' },
]

const RESPONSES: Record<number, (allDone: boolean) => string> = {
  1: () => 'Debes completar las cinco misiones sagradas para demostrar tu valía. Solo entonces serás digno de portar la Fuente Magna en tu viaje a Göbekli Tepe.',
  2: () => 'La Fuente Magna es un recipiente sagrado de más de 5000 años. Sus inscripciones invocan a la diosa Nia. Fue creada para canalizar energías cósmicas en rituales de alineación planetaria.',
  3: () => 'Has demostrado ser digno, viajero. Los cinco nodos sagrados resuenan con tu energía. Toma la Fuente Magna y úsala sabiamente en Göbekli Tepe. Que los antiguos guíen tu camino.',
}

// Mensaje de agradecimiento — se muestra la primera vez que devuelve la fuente
const THANKS_MESSAGE = '¡Gracias, viajero! La Fuente Magna regresa a su lugar sagrado. Los antiguos te bendicen. Completa las cinco misiones sagradas y regresa. Solo entonces serás digno de portarla en tu viaje a Göbekli Tepe.'

export default function ViracochaInteractiveDialogue({
  missionCompleted,
  allMissionsCompleted,
  magnaBowlReturned,
  onClose,
  onLendMagnaBowl
}: ViracochaInteractiveDialogueProps) {
  // Si magnaBowlReturned es FALSE → mostrar agradecimiento (primera vez que devuelve)
  // Si magnaBowlReturned es TRUE → mostrar opciones (ya agradeció antes)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(
    !magnaBowlReturned ? THANKS_MESSAGE : null
  )
  const [showOptions, setShowOptions] = useState(magnaBowlReturned)

  // Si es el agradecimiento, cerrar automáticamente después de 6s
  useEffect(() => {
    if (!magnaBowlReturned) {
      const timer = setTimeout(() => onClose(), 6000)
      return () => clearTimeout(timer)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleOption = (id: number) => {
    const response = RESPONSES[id]()
    setSelectedResponse(response)
    setShowOptions(false)

    // Opción 3: Prestar la Fuente Magna (siempre positivo porque el diálogo solo aparece con 5 misiones completas)
    if (id === 3 && onLendMagnaBowl) {
      setTimeout(() => { 
        onLendMagnaBowl()
        onClose() 
      }, 5000) // Dar tiempo para leer el mensaje
      return
    }
    
    // Para otras opciones, cerrar después de 5s
    setTimeout(() => onClose(), 5000)
  }

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
          border: `2px solid ${ACCENT}`,
          borderRadius: '12px',
          padding: '30px 40px',
          maxWidth: '620px',
          width: '90%',
          boxShadow: `0 0 30px rgba(255, 215, 0, 0.6)`,
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        {/* Icono */}
        <div style={{ textAlign: 'center', marginBottom: '15px', fontSize: '42px' }}>🗿</div>

        {/* Nombre */}
        <div style={{
          color: ACCENT,
          fontSize: '22px',
          fontWeight: 'bold',
          textAlign: 'center',
          marginBottom: '20px',
          fontFamily: '"Cinzel", "Trajan Pro", serif',
          letterSpacing: '3px',
          textShadow: `0 0 10px rgba(255, 215, 0, 0.8)`,
        }}>
          Viracocha
        </div>

        {/* Mensaje */}
        <div style={{
          color: '#ffffff',
          fontSize: '18px',
          textAlign: 'center',
          marginBottom: showOptions && !selectedResponse ? '25px' : '0',
          fontFamily: '"Cinzel", serif',
          letterSpacing: '1px',
          lineHeight: '1.6',
          textShadow: `0 0 5px rgba(255, 215, 0, 0.3)`,
        }}>
          {selectedResponse || '¿Qué deseas saber, viajero?'}
        </div>

        {/* Opciones */}
        {showOptions && !selectedResponse && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {OPTIONS.map((opt) => {
              const isLend = opt.id === 3
              
              return (
                <button
                  key={opt.id}
                  onClick={() => handleOption(opt.id)}
                  style={{
                    padding: '14px 22px', fontSize: '16px',
                    color: isLend ? '#00ff88' : ACCENT,
                    background: isLend ? 'rgba(0,255,136,0.1)' : `rgba(255,215,0,0.1)`,
                    border: `2px solid ${isLend ? '#00ff88' : ACCENT}`,
                    borderRadius: '8px', 
                    cursor: 'pointer',
                    fontFamily: '"Cinzel", serif', letterSpacing: '1px',
                    textAlign: 'left', transition: 'all 0.3s ease',
                    fontWeight: isLend ? 'bold' : 'normal'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = isLend ? 'rgba(0,255,136,0.3)' : 'rgba(255,215,0,0.3)'
                    e.currentTarget.style.transform = 'translateX(8px)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = isLend ? 'rgba(0,255,136,0.1)' : 'rgba(255,215,0,0.1)'
                    e.currentTarget.style.transform = 'translateX(0)'
                  }}
                >
                  {opt.id}. {opt.label}
                  {isLend && ' ✨'}
                </button>
              )
            })}
          </div>
        )}

        {/* Botón cerrar */}
        {(!showOptions || selectedResponse) && (
          <button
            onClick={onClose}
            style={{
              marginTop: '20px', padding: '10px 30px', fontSize: '16px',
              color: ACCENT, background: 'transparent',
              border: `2px solid ${ACCENT}`, borderRadius: '8px',
              cursor: 'pointer', fontFamily: '"Cinzel", serif',
              letterSpacing: '2px', display: 'block', margin: '20px auto 0',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => { e.currentTarget.style.background = ACCENT; e.currentTarget.style.color = '#000' }}
            onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = ACCENT }}
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
