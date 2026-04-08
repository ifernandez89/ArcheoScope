'use client'

import { useState, useEffect } from 'react'
import { isMissionCompleted } from '@/types/missionState'

interface ViracochaInteractiveDialogueProps {
  missionCompleted: boolean       // misión de puma punku completada
  allMissionsCompleted: boolean   // las 5 misiones completas
  magnaBowlReturned: boolean      // fuente magna ya fue devuelta
  onClose: () => void
  onLendMagnaBowl?: () => void    // callback cuando presta la fuente magna
}

const ACCENT = '#ffd700'

const OPTIONS = [
  { id: 1, label: '¿Qué debo hacer?' },
  { id: 2, label: '¿Qué es la Fuente Magna?' },
  { id: 3, label: '¿Me prestas la Fuente Magna?' },
]

const RESPONSES: Record<number, (allDone: boolean) => string> = {
  1: () => 'El cosmos aguarda tu despertar. Cinco nodos de energía duermen en la Tierra — Puma Punku, Giza, Teotihuacán, Veracruz, Rapa Nui. Cuando todos vibren en armonía, el portal se abrirá.',
  2: () => 'La Fuente Magna es un recipiente sagrado de más de 5000 años. Sus inscripciones proto-sumerias invocan a la diosa Nia. Fue creada para canalizar energías cósmicas en rituales de alineación planetaria.',
  3: (allDone) => allDone
    ? 'Has demostrado ser digno, viajero. Los cinco nodos resuenan. Toma la Fuente Magna — llévala al lugar donde el tiempo comenzó.'
    : 'Aún no, viajero. La Fuente Magna solo puede ser portada por quien ha despertado los cinco nodos de la Tierra. Completa tu misión y regresa.',
}

export default function ViracochaInteractiveDialogue({
  missionCompleted,
  allMissionsCompleted,
  magnaBowlReturned,
  onClose,
  onLendMagnaBowl
}: ViracochaInteractiveDialogueProps) {
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)
  const [showOptions, setShowOptions] = useState(true)

  // Mensaje inicial según estado
  const initialMessage = magnaBowlReturned
    ? 'Viajero... ¿Qué deseas saber?'
    : 'Gracias por devolver la Fuente Magna a su lugar sagrado. Los antiguos te bendicen.'

  useEffect(() => {
    // Si la fuente no fue devuelta aún, mostrar agradecimiento y cerrar
    if (!magnaBowlReturned) {
      setShowOptions(false)
      setTimeout(() => onClose(), 5000)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleOption = (id: number) => {
    const response = RESPONSES[id](allMissionsCompleted)
    setSelectedResponse(response)
    setShowOptions(false)

    // Si presta la fuente magna y todas las misiones están completas
    if (id === 3 && allMissionsCompleted && onLendMagnaBowl) {
      setTimeout(() => {
        onLendMagnaBowl()
        onClose()
      }, 4000)
      return
    }

    setTimeout(() => onClose(), 5000)
  }

  return (
    <div
      style={{
        position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
        background: 'rgba(0,0,0,0.75)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 2000, animation: 'fadeIn 0.3s ease-out'
      }}
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: 'rgba(10, 8, 25, 0.97)',
          border: `2px solid ${ACCENT}`,
          borderRadius: '12px',
          padding: '30px 40px',
          maxWidth: '620px',
          width: '90%',
          boxShadow: `0 0 40px rgba(255,215,0,0.4)`,
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        {/* Icono */}
        <div style={{ textAlign: 'center', fontSize: '42px', marginBottom: '12px' }}>🗿</div>

        {/* Nombre */}
        <div style={{
          color: ACCENT, fontSize: '20px', fontWeight: 'bold',
          textAlign: 'center', marginBottom: '18px',
          fontFamily: '"Cinzel", serif', letterSpacing: '3px',
          textShadow: `0 0 10px rgba(255,215,0,0.8)`
        }}>
          Viracocha
        </div>

        {/* Mensaje */}
        <div style={{
          color: '#fff', fontSize: '17px', textAlign: 'center',
          marginBottom: showOptions && !selectedResponse ? '24px' : '0',
          fontFamily: '"Cinzel", serif', lineHeight: '1.6',
          textShadow: `0 0 5px rgba(255,215,0,0.2)`
        }}>
          {selectedResponse || initialMessage}
        </div>

        {/* Opciones */}
        {showOptions && !selectedResponse && magnaBowlReturned && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '8px' }}>
            {OPTIONS.map((opt) => (
              <button
                key={opt.id}
                onClick={() => handleOption(opt.id)}
                style={{
                  padding: '13px 20px', fontSize: '15px',
                  color: opt.id === 3 && allMissionsCompleted ? '#00ff88' : ACCENT,
                  background: opt.id === 3 && allMissionsCompleted
                    ? 'rgba(0,255,136,0.08)' : `rgba(255,215,0,0.08)`,
                  border: `2px solid ${opt.id === 3 && allMissionsCompleted ? '#00ff88' : ACCENT}`,
                  borderRadius: '8px', cursor: 'pointer',
                  fontFamily: '"Cinzel", serif', letterSpacing: '1px',
                  textAlign: 'left', transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = opt.id === 3 && allMissionsCompleted
                    ? 'rgba(0,255,136,0.25)' : 'rgba(255,215,0,0.2)'
                  e.currentTarget.style.transform = 'translateX(6px)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = opt.id === 3 && allMissionsCompleted
                    ? 'rgba(0,255,136,0.08)' : 'rgba(255,215,0,0.08)'
                  e.currentTarget.style.transform = 'translateX(0)'
                }}
              >
                {opt.id}. {opt.label}
                {opt.id === 3 && allMissionsCompleted && ' ✨'}
              </button>
            ))}
          </div>
        )}

        {/* Botón cerrar */}
        {(!showOptions || selectedResponse) && (
          <button
            onClick={onClose}
            style={{
              marginTop: '20px', padding: '10px 30px', fontSize: '14px',
              color: ACCENT, background: 'transparent',
              border: `2px solid ${ACCENT}`, borderRadius: '8px',
              cursor: 'pointer', fontFamily: '"Cinzel", serif',
              letterSpacing: '2px', display: 'block', margin: '20px auto 0',
              transition: 'all 0.2s'
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
