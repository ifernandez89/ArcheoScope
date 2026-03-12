'use client'

import { useEffect, useState, useRef } from 'react'

interface SphinxDialogueProps {
  message: string
  onComplete?: () => void
  onClose?: () => void
}

export default function SphinxDialogue({ message, onComplete, onClose }: SphinxDialogueProps) {
  const [opacity, setOpacity] = useState(0)
  const [translateY, setTranslateY] = useState(0)
  const onCompleteRef = useRef(onComplete)
  const onCloseRef = useRef(onClose)

  // Mantener las referencias actualizadas
  useEffect(() => {
    onCompleteRef.current = onComplete
    onCloseRef.current = onClose
  }, [onComplete, onClose])

  useEffect(() => {
    // Fade in
    setTimeout(() => setOpacity(1), 50)

    // Después de 3.5 segundos, empezar a flotar y desaparecer
    const floatTimer = setTimeout(() => {
      setOpacity(0)
      setTranslateY(-30)
    }, 3500)

    // Después de 4 segundos total, notificar que terminó
    const completeTimer = setTimeout(() => {
      if (onCompleteRef.current) {
        onCompleteRef.current()
      }
      if (onCloseRef.current) {
        onCloseRef.current()
      }
    }, 4000)

    return () => {
      clearTimeout(floatTimer)
      clearTimeout(completeTimer)
    }
  }, []) // Sin dependencias - solo se ejecuta una vez al montar

  return (
    <div
      style={{
        position: 'fixed',
        top: '30%',
        left: '50%',
        transform: `translate(-50%, ${translateY}px)`,
        opacity,
        transition: 'opacity 0.5s ease-out, transform 0.5s ease-out',
        pointerEvents: 'none',
        zIndex: 1000,
      }}
    >
      <div
        style={{
          background: 'rgba(20, 20, 40, 0.95)',
          border: '2px solid #ffd700',
          borderRadius: '12px',
          padding: '20px 30px',
          color: '#ffffff',
          fontSize: '24px',
          fontWeight: 'normal',
          textAlign: 'center',
          boxShadow: '0 0 30px rgba(255, 215, 0, 0.6)',
          fontFamily: '"Cinzel", "Trajan Pro", "Times New Roman", serif',
          letterSpacing: '2px',
          textShadow: '0 0 10px rgba(255, 215, 0, 0.5)',
        }}
      >
        {message}
      </div>
    </div>
  )
}
