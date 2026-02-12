'use client'

import { useState } from 'react'

interface ModelInfoProps {
  modelPath: string
  vertices?: number
  triangles?: number
  animations?: number
}

const MODEL_DESCRIPTIONS: Record<string, { title: string; description: string; origin: string }> = {
  'moai': {
    title: 'Moai de Rapa Nui',
    description: 'Estatuas monolíticas talladas por el pueblo Rapa Nui en la Isla de Pascua entre 1250 y 1500 d.C.',
    origin: 'Isla de Pascua, Chile'
  },
  'sphinx': {
    title: 'Esfinge de Giza',
    description: 'Monumento icónico del antiguo Egipto con cuerpo de león y cabeza humana, construido durante el reinado de Kefrén.',
    origin: 'Giza, Egipto'
  },
  'sphinxWithBase': {
    title: 'Esfinge con Base',
    description: 'Representación completa de la Esfinge de Giza incluyendo su plataforma base.',
    origin: 'Giza, Egipto'
  },
  'warrior': {
    title: 'Guerrero',
    description: 'Modelo de prueba de un guerrero para demostración del visualizador 3D.',
    origin: 'Modelo de Prueba'
  }
}

export default function ModelInfo({ modelPath, vertices, triangles, animations }: ModelInfoProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  
  const modelKey = modelPath.split('/').pop()?.replace('.glb', '') || ''
  const info = MODEL_DESCRIPTIONS[modelKey] || {
    title: modelKey,
    description: 'Modelo 3D',
    origin: 'Desconocido'
  }

  return (
    <div style={{
      position: 'fixed',
      top: '100px',
      right: '20px',
      width: isExpanded ? '320px' : '60px',
      background: 'rgba(10, 10, 10, 0.9)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '12px',
      padding: isExpanded ? '16px' : '12px',
      transition: 'all 0.3s ease',
      zIndex: 1000,
      cursor: 'pointer'
    }}
    onClick={() => setIsExpanded(!isExpanded)}
    >
      {!isExpanded ? (
        <div style={{
          fontSize: '24px',
          textAlign: 'center'
        }}>
          ℹ️
        </div>
      ) : (
        <div>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '12px'
          }}>
            <h3 style={{
              fontSize: '16px',
              fontWeight: 'bold',
              color: '#fff',
              margin: 0
            }}>
              {info.title}
            </h3>
            <span style={{ fontSize: '20px' }}>✕</span>
          </div>

          <div style={{
            fontSize: '13px',
            color: '#ccc',
            lineHeight: '1.5',
            marginBottom: '12px'
          }}>
            {info.description}
          </div>

          <div style={{
            paddingTop: '12px',
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            fontSize: '12px',
            color: '#888'
          }}>
            <div style={{ marginBottom: '6px' }}>
              <span style={{ color: '#667eea' }}>📍</span> {info.origin}
            </div>
            
            {vertices && (
              <div style={{ marginBottom: '6px' }}>
                <span style={{ color: '#4ade80' }}>▲</span> {vertices.toLocaleString()} vértices
              </div>
            )}
            
            {triangles && (
              <div style={{ marginBottom: '6px' }}>
                <span style={{ color: '#60a5fa' }}>◆</span> {triangles.toLocaleString()} triángulos
              </div>
            )}
            
            {animations !== undefined && animations > 0 && (
              <div>
                <span style={{ color: '#f59e0b' }}>🎬</span> {animations} animación(es)
              </div>
            )}
          </div>

          <div style={{
            marginTop: '12px',
            paddingTop: '12px',
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            fontSize: '11px',
            color: '#666',
            textAlign: 'center'
          }}>
            Click para cerrar
          </div>
        </div>
      )}
    </div>
  )
}
