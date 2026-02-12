'use client'

import { useState } from 'react'

interface AIControlsProps {
  onToggleReactiveBehavior: () => void
  onToggleAutoAnimation: () => void
  onToggleExpressions: () => void
  reactiveBehaviorActive: boolean
  autoAnimationActive: boolean
  expressionsActive: boolean
}

export default function AIControls({
  onToggleReactiveBehavior,
  onToggleAutoAnimation,
  onToggleExpressions,
  reactiveBehaviorActive,
  autoAnimationActive,
  expressionsActive
}: AIControlsProps) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          top: '90px',
          right: '20px',
          width: '50px',
          height: '50px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          border: 'none',
          color: 'white',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
          zIndex: 1000,
          transition: 'transform 0.2s',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
        onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
      >
        🤖
      </button>

      {/* Panel de controles */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          top: '150px',
          right: '20px',
          width: '280px',
          background: 'rgba(0, 0, 0, 0.85)',
          backdropFilter: 'blur(10px)',
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          zIndex: 999
        }}>
          <h3 style={{
            margin: '0 0 15px 0',
            color: 'white',
            fontSize: '18px',
            fontWeight: 'bold'
          }}>
            🤖 Controles IA
          </h3>

          {/* Comportamiento Reactivo */}
          <ControlToggle
            label="Comportamiento Reactivo"
            description="El modelo reacciona a tu proximidad"
            icon="👁️"
            isActive={reactiveBehaviorActive}
            onToggle={onToggleReactiveBehavior}
          />

          {/* Animaciones Automáticas */}
          <ControlToggle
            label="Animaciones Auto"
            description="Movimientos procedurales continuos"
            icon="🎭"
            isActive={autoAnimationActive}
            onToggle={onToggleAutoAnimation}
          />

          {/* Expresiones Faciales */}
          <ControlToggle
            label="Expresiones Faciales"
            description="Micro-expresiones y emociones"
            icon="😊"
            isActive={expressionsActive}
            onToggle={onToggleExpressions}
          />

          {/* Info */}
          <div style={{
            marginTop: '15px',
            padding: '12px',
            background: 'rgba(102, 126, 234, 0.1)',
            border: '1px solid rgba(102, 126, 234, 0.3)',
            borderRadius: '8px'
          }}>
            <div style={{
              color: 'rgba(255,255,255,0.7)',
              fontSize: '12px',
              lineHeight: '1.5'
            }}>
              💡 <strong>Tip:</strong> Acércate al modelo para ver reacciones en tiempo real
            </div>
          </div>
        </div>
      )}
    </>
  )
}

// Componente auxiliar para toggles
function ControlToggle({
  label,
  description,
  icon,
  isActive,
  onToggle
}: {
  label: string
  description: string
  icon: string
  isActive: boolean
  onToggle: () => void
}) {
  return (
    <div style={{
      marginBottom: '15px',
      padding: '12px',
      background: isActive 
        ? 'rgba(102, 126, 234, 0.2)' 
        : 'rgba(255,255,255,0.05)',
      border: isActive 
        ? '2px solid #667eea' 
        : '1px solid rgba(255,255,255,0.1)',
      borderRadius: '8px',
      cursor: 'pointer',
      transition: 'all 0.2s'
    }}
      onClick={onToggle}
      onMouseEnter={(e) => {
        if (!isActive) {
          e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
        }
      }}
      onMouseLeave={(e) => {
        if (!isActive) {
          e.currentTarget.style.background = 'rgba(255,255,255,0.05)'
        }
      }}
    >
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '5px'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <span style={{ fontSize: '20px' }}>{icon}</span>
          <span style={{
            color: 'white',
            fontSize: '14px',
            fontWeight: 'bold'
          }}>
            {label}
          </span>
        </div>
        <div style={{
          width: '40px',
          height: '22px',
          borderRadius: '11px',
          background: isActive ? '#4ade80' : 'rgba(255,255,255,0.2)',
          position: 'relative',
          transition: 'background 0.2s'
        }}>
          <div style={{
            width: '18px',
            height: '18px',
            borderRadius: '50%',
            background: 'white',
            position: 'absolute',
            top: '2px',
            left: isActive ? '20px' : '2px',
            transition: 'left 0.2s',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
          }} />
        </div>
      </div>
      <div style={{
        color: 'rgba(255,255,255,0.6)',
        fontSize: '12px',
        marginLeft: '28px'
      }}>
        {description}
      </div>
    </div>
  )
}
