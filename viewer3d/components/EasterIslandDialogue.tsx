'use client'

import { useState, useEffect } from 'react'
import { Html } from '@react-three/drei'
import * as THREE from 'three'

/**
 * Sistema de diálogo entre Moai y Atlante
 * Conversación sobre la red energética planetaria y los cristales del tiempo
 */

interface DialogueLine {
  speaker: 'moai' | 'atlante'
  text: string
}

const DIALOGUE: DialogueLine[] = [
  {
    speaker: "moai",
    text: "La resonancia de la Tierra ha cambiado. El pulso ya no coincide con el ciclo estelar."
  },
  {
    speaker: "atlante",
    text: "Lo detecté también. Los cristales del tiempo están fuera de fase."
  },
  {
    speaker: "moai",
    text: "Si la red permanece inestable, la distorsión crecerá."
  },
  {
    speaker: "atlante",
    text: "Los nodos deben realinearse: Giza, Teotihuacan, Puma Punku… y este."
  },
  {
    speaker: "moai",
    text: "La ingeniería antigua fue diseñada para resistir ciclos largos."
  },
  {
    speaker: "atlante",
    text: "Pero incluso la ingeniería eterna falla si los guardianes olvidan su propósito."
  },
  {
    speaker: "moai",
    text: "Entonces el viajero deberá restaurar la red."
  },
  {
    speaker: "atlante",
    text: "Antes de que el tiempo se fracture."
  }
]

interface EasterIslandDialogueProps {
  moaiPosition: THREE.Vector3
  atlantePosition: THREE.Vector3
  enabled?: boolean
}

export default function EasterIslandDialogue({ 
  moaiPosition, 
  atlantePosition,
  enabled = true 
}: EasterIslandDialogueProps) {
  const [currentLineIndex, setCurrentLineIndex] = useState(0)
  const [visible, setVisible] = useState(false)
  
  useEffect(() => {
    if (!enabled) return
    
    // Esperar 3 segundos antes de empezar
    const startDelay = setTimeout(() => {
      setVisible(true)
    }, 3000)
    
    return () => clearTimeout(startDelay)
  }, [enabled])
  
  useEffect(() => {
    if (!visible || !enabled) return
    
    // Cambiar de línea cada 12 segundos (más pausado)
    const interval = setInterval(() => {
      setCurrentLineIndex((prev) => (prev + 1) % DIALOGUE.length)
    }, 12000)
    
    return () => clearInterval(interval)
  }, [visible, enabled])
  
  if (!visible || !enabled) return null
  
  const currentLine = DIALOGUE[currentLineIndex]
  const position = currentLine.speaker === 'moai' ? moaiPosition : atlantePosition
  
  return (
    <Html
      position={[position.x, position.y + 8, position.z]}
      center
      distanceFactor={10}
      style={{
        pointerEvents: 'none',
        userSelect: 'none'
      }}
    >
      <div
        style={{
          background: currentLine.speaker === 'moai' 
            ? 'rgba(139, 115, 85, 0.95)' 
            : 'rgba(70, 130, 180, 0.95)',
          color: 'white',
          padding: '16px 20px',
          borderRadius: '16px',
          maxWidth: '320px',
          fontSize: '14px',
          lineHeight: '1.5',
          fontFamily: 'system-ui, -apple-system, sans-serif',
          boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          border: currentLine.speaker === 'moai'
            ? '2px solid rgba(205, 133, 63, 0.6)'
            : '2px solid rgba(100, 149, 237, 0.6)',
          position: 'relative',
          animation: 'fadeInScale 0.5s ease-out',
          backdropFilter: 'blur(4px)'
        }}
      >
        {/* Texto del diálogo */}
        <div style={{
          fontSize: '13px',
          opacity: 0.95
        }}>
          {currentLine.text}
        </div>
        
        {/* Triángulo apuntando hacia abajo */}
        <div style={{
          position: 'absolute',
          bottom: '-10px',
          left: '50%',
          transform: 'translateX(-50%)',
          width: 0,
          height: 0,
          borderLeft: '10px solid transparent',
          borderRight: '10px solid transparent',
          borderTop: currentLine.speaker === 'moai'
            ? '10px solid rgba(139, 115, 85, 0.95)'
            : '10px solid rgba(70, 130, 180, 0.95)'
        }} />
      </div>
      
      <style jsx>{`
        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: scale(0.8) translateY(10px);
          }
          to {
            opacity: 1;
            transform: scale(1) translateY(0);
          }
        }
      `}</style>
    </Html>
  )
}
