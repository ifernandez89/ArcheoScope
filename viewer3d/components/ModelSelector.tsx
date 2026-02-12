'use client'

import { useState } from 'react'
import { getAssetPath } from '@/lib/paths'

interface Model {
  id: string
  name: string
  path: string
  thumbnail?: string
}

const AVAILABLE_MODELS: Model[] = [
  {
    id: 'warrior',
    name: 'Warrior',
    path: getAssetPath('/warrior.glb'),
    thumbnail: '⚔️'
  },
  {
    id: 'moai',
    name: 'Moai (Rapa Nui)',
    path: getAssetPath('/moai.glb'),
    thumbnail: '🗿'
  },
  {
    id: 'sphinx',
    name: 'Sphinx',
    path: getAssetPath('/sphinx.glb'),
    thumbnail: '🦁'
  },
  {
    id: 'sphinxWithBase',
    name: 'Sphinx con Base',
    path: getAssetPath('/sphinxWithBase.glb'),
    thumbnail: '🏛️'
  }
]

interface ModelSelectorProps {
  onModelChange: (modelPath: string) => void
  currentModel: string
}

export default function ModelSelector({ onModelChange, currentModel }: ModelSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div style={{
      position: 'fixed',
      bottom: '100px',
      right: '20px',
      zIndex: 1000
    }}>
      {/* Botón principal */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          padding: '12px 20px',
          background: 'rgba(102, 126, 234, 0.9)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '8px',
          color: '#fff',
          cursor: 'pointer',
          fontSize: '14px',
          fontWeight: 'bold',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          transition: 'all 0.2s',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'rgba(102, 126, 234, 1)'
          e.currentTarget.style.transform = 'translateY(-2px)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'rgba(102, 126, 234, 0.9)'
          e.currentTarget.style.transform = 'translateY(0)'
        }}
      >
        <span>📦</span>
        <span>Modelos</span>
        <span style={{ 
          fontSize: '10px',
          opacity: 0.8
        }}>
          {isOpen ? '▲' : '▼'}
        </span>
      </button>

      {/* Panel de modelos */}
      {isOpen && (
        <div style={{
          position: 'absolute',
          bottom: '60px',
          right: 0,
          minWidth: '250px',
          background: 'rgba(10, 10, 10, 0.95)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '12px',
          padding: '12px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)'
        }}>
          <div style={{
            fontSize: '12px',
            color: '#888',
            marginBottom: '12px',
            textTransform: 'uppercase',
            letterSpacing: '1px'
          }}>
            Seleccionar Modelo
          </div>

          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}>
            {AVAILABLE_MODELS.map((model) => (
              <button
                key={model.id}
                onClick={() => {
                  onModelChange(model.path)
                  setIsOpen(false)
                }}
                style={{
                  padding: '12px',
                  background: currentModel === model.path 
                    ? 'rgba(102, 126, 234, 0.3)' 
                    : 'rgba(255, 255, 255, 0.05)',
                  border: currentModel === model.path
                    ? '1px solid rgba(102, 126, 234, 0.5)'
                    : '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  color: '#fff',
                  cursor: 'pointer',
                  fontSize: '14px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  transition: 'all 0.2s',
                  textAlign: 'left'
                }}
                onMouseEnter={(e) => {
                  if (currentModel !== model.path) {
                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (currentModel !== model.path) {
                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)'
                  }
                }}
              >
                <span style={{ fontSize: '24px' }}>
                  {model.thumbnail}
                </span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 'bold' }}>
                    {model.name}
                  </div>
                  <div style={{ 
                    fontSize: '11px', 
                    color: '#888',
                    marginTop: '2px'
                  }}>
                    {model.path}
                  </div>
                </div>
                {currentModel === model.path && (
                  <span style={{ color: '#4ade80' }}>✓</span>
                )}
              </button>
            ))}
          </div>

          <div style={{
            marginTop: '12px',
            paddingTop: '12px',
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            fontSize: '11px',
            color: '#666',
            textAlign: 'center'
          }}>
            {AVAILABLE_MODELS.length} modelo(s) disponible(s)
          </div>
        </div>
      )}
    </div>
  )
}
