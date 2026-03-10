'use client'

import { useEffect, useRef } from 'react'

interface SphinxDialogueProps {
  onClose: () => void
}

/**
 * 💬 Diálogo de la Esfinge
 * Componente UI que se renderiza fuera del Canvas
 * Se cierra automáticamente después de 4 segundos
 */
export default function SphinxDialogue({ onClose }: SphinxDialogueProps) {
  const onCloseRef = useRef(onClose)
  
  // Actualizar la referencia cuando cambie
  useEffect(() => {
    onCloseRef.current = onClose
  }, [onClose])
  
  // Cerrar automáticamente después de 3 segundos
  useEffect(() => {
    const timer = setTimeout(() => {
      onCloseRef.current()
    }, 3000)
    
    return () => clearTimeout(timer)
  }, []) // Array vacío para que solo se ejecute una vez
  
  return (
    <div
      style={{
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 2000,
        background: 'rgba(0, 0, 0, 0.95)',
        backdropFilter: 'blur(10px)',
        padding: '40px 60px',
        borderRadius: '12px',
        border: '2px solid #d4a574',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.8)',
        maxWidth: '500px',
        animation: 'fadeIn 0.3s ease-out'
      }}
    >
      <div style={{
        color: '#ffffff',
        fontSize: '18px',
        textAlign: 'center',
        lineHeight: '1.6'
      }}>
        ¿Qué quieres?
      </div>
      
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translate(-50%, -45%); }
          to { opacity: 1; transform: translate(-50%, -50%); }
        }
      `}</style>
    </div>
  )
}
