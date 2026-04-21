'use client'

import { useState } from 'react'

interface AkhenatonDialogueProps {
  onClose: () => void
  hasSeenGeoglyphs?: boolean // Desbloquea la 4ta pregunta
}

const ACCENT = '#e8c97a'

const OPTIONS = [
  { id: 1, label: '¿Quién construyó realmente esta red?' },
  { id: 2, label: '¿Por qué estoy aquí?' },
  { id: 3, label: '¿Qué ocurre si la red no se restaura?' },
]

const RESPONSES: Record<number, string> = {
  1: `Los hombres creen que cada civilización levantó sus monumentos por separado.\n\nPero las piedras recuerdan otra historia.\n\nCulturas separadas por océanos… separadas por milenios… levantaron estructuras con la misma geometría. Los mismos alineamientos. Las mismas proporciones. Las mismas orientaciones hacia las estrellas.\n\nNadie sabe quién transmitió ese conocimiento.\n\nAlgunos guardianes lo llaman…\n\nLa Primera Señal.`,
  2: `Tu llegada no es un accidente.\n\nTu nave porta la marca de una antigua orden.\n\nArcheoscope.\n\nExploradores de mundos… buscadores de estructuras imposibles.\n\nHace poco tiempo, sus sensores detectaron algo que no debería existir. Una resonancia artificial proveniente de este planeta. Un pulso… demasiado preciso para ser natural.\n\nLa red despertó… y respondió a tu llegada.`,
  3: `La red mantiene el equilibrio entre cielo y tierra.\n\nCuando sus nodos están alineados… el mundo respira en armonía.\n\nPero ahora… algo está fuera de fase.\n\nLos antiguos lo llamaban…\n\nLa Distorsión.\n\nCuando la red colapsa… las órbitas comienzan a desviarse. Las resonancias del planeta cambian. Y el tiempo mismo se vuelve inestable.\n\nSi la distorsión crece… la historia de este mundo podría reiniciarse.\n\nComo si nunca hubiera existido.`,
  4: `Entonces comienzas a ver la red.\n\nLos antiguos no solo construyeron monumentos.\n\nDibujaron señales visibles desde el cielo.\n\nGeoglifos en los desiertos. Patrones en las montañas. Geometría grabada en piedra.\n\nCada símbolo es parte de un mapa mayor.\n\nUna geometría planetaria.\n\nUn lenguaje que solo puede leerse…\n\ndesde las estrellas.`,
}

export default function AkhenatonDialogue({ onClose, hasSeenGeoglyphs = false }: AkhenatonDialogueProps) {
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)
  const [showOptions, setShowOptions] = useState(true)

  const options = hasSeenGeoglyphs
    ? [...OPTIONS, { id: 4, label: 'He visto símbolos que conectan los nodos.' }]
    : OPTIONS

  const handleOption = (id: number) => {
    setSelectedResponse(RESPONSES[id])
    setShowOptions(false)
    setTimeout(() => onClose(), 8000)
  }

  const handleBack = () => {
    setSelectedResponse(null)
    setShowOptions(true)
  }

  return (
    <div
      style={{
        position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
        background: 'rgba(0, 0, 0, 0.80)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 2000, animation: 'fadeIn 0.3s ease-out'
      }}
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: 'rgba(18, 12, 6, 0.97)',
          border: `2px solid ${ACCENT}`,
          borderRadius: '12px',
          padding: '32px 44px',
          maxWidth: '640px',
          width: '92%',
          boxShadow: `0 0 40px rgba(232, 201, 122, 0.4)`,
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        {/* Icono */}
        <div style={{ textAlign: 'center', marginBottom: '10px', fontSize: '44px' }}>𓂀</div>

        {/* Nombre */}
        <div style={{
          color: ACCENT,
          fontSize: '22px',
          fontWeight: 'bold',
          textAlign: 'center',
          marginBottom: '22px',
          fontFamily: '"Cinzel", serif',
          letterSpacing: '4px',
          textShadow: `0 0 12px rgba(232, 201, 122, 0.7)`,
        }}>
          Akhenaton
        </div>

        {/* Respuesta seleccionada */}
        {selectedResponse && (
          <div style={{
            color: '#f0e8d0',
            fontSize: '16px',
            textAlign: 'center',
            fontFamily: '"Cinzel", serif',
            letterSpacing: '0.5px',
            lineHeight: '1.9',
            whiteSpace: 'pre-line',
            textShadow: `0 0 6px rgba(232, 201, 122, 0.2)`,
            marginBottom: '24px',
          }}>
            {selectedResponse}
          </div>
        )}

        {/* Opciones */}
        {showOptions && !selectedResponse && (
          <>
            <div style={{
              color: 'rgba(240, 232, 208, 0.7)',
              fontSize: '15px',
              textAlign: 'center',
              fontFamily: '"Cinzel", serif',
              marginBottom: '20px',
              letterSpacing: '1px',
            }}>
              ¿Qué deseas saber, viajero?
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {options.map((opt) => (
                <button
                  key={opt.id}
                  onClick={() => handleOption(opt.id)}
                  style={{
                    padding: '14px 22px',
                    fontSize: '15px',
                    color: opt.id === 4 ? '#88ddff' : ACCENT,
                    background: opt.id === 4 ? 'rgba(136, 221, 255, 0.08)' : `rgba(232, 201, 122, 0.08)`,
                    border: `1px solid ${opt.id === 4 ? 'rgba(136,221,255,0.4)' : 'rgba(232,201,122,0.4)'}`,
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontFamily: '"Cinzel", serif',
                    letterSpacing: '0.5px',
                    textAlign: 'left',
                    transition: 'all 0.25s ease',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = opt.id === 4 ? 'rgba(136,221,255,0.2)' : 'rgba(232,201,122,0.2)'
                    e.currentTarget.style.transform = 'translateX(8px)'
                    e.currentTarget.style.borderColor = opt.id === 4 ? '#88ddff' : ACCENT
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = opt.id === 4 ? 'rgba(136,221,255,0.08)' : 'rgba(232,201,122,0.08)'
                    e.currentTarget.style.transform = 'translateX(0)'
                    e.currentTarget.style.borderColor = opt.id === 4 ? 'rgba(136,221,255,0.4)' : 'rgba(232,201,122,0.4)'
                  }}
                >
                  {opt.id === 4 && '✦ '}{opt.label}
                </button>
              ))}
            </div>
          </>
        )}

        {/* Botones inferiores */}
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', marginTop: '24px' }}>
          {selectedResponse && (
            <button
              onClick={handleBack}
              style={{
                padding: '10px 24px', fontSize: '14px',
                color: 'rgba(232,201,122,0.6)', background: 'transparent',
                border: `1px solid rgba(232,201,122,0.3)`, borderRadius: '8px',
                cursor: 'pointer', fontFamily: '"Cinzel", serif', letterSpacing: '1px',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => { e.currentTarget.style.borderColor = ACCENT; e.currentTarget.style.color = ACCENT }}
              onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(232,201,122,0.3)'; e.currentTarget.style.color = 'rgba(232,201,122,0.6)' }}
            >
              ← Volver
            </button>
          )}
          <button
            onClick={onClose}
            style={{
              padding: '10px 28px', fontSize: '14px',
              color: ACCENT, background: 'transparent',
              border: `1px solid ${ACCENT}`, borderRadius: '8px',
              cursor: 'pointer', fontFamily: '"Cinzel", serif', letterSpacing: '2px',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => { e.currentTarget.style.background = ACCENT; e.currentTarget.style.color = '#000' }}
            onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = ACCENT }}
          >
            Cerrar
          </button>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes scaleIn { from { opacity: 0; transform: scale(0.92); } to { opacity: 1; transform: scale(1); } }
      `}</style>
    </div>
  )
}
