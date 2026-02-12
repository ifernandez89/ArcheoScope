'use client'

import { useState, useEffect } from 'react'
import { useEngine } from '@/hooks/useEngine'
import type { SceneDefinition } from '@/experience/scene-system'

interface SceneNavigatorProps {
  scenes: SceneDefinition[]
  currentSceneId: string | null
  onSceneChange: (sceneId: string) => void
  isTransitioning: boolean
}

export default function SceneNavigator({
  scenes,
  currentSceneId,
  onSceneChange,
  isTransitioning
}: SceneNavigatorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [loadingProgress, setLoadingProgress] = useState(0)

  const currentScene = scenes.find(s => s.id === currentSceneId)
  const currentIndex = scenes.findIndex(s => s.id === currentSceneId)

  const handlePrevious = () => {
    if (currentIndex > 0 && !isTransitioning) {
      onSceneChange(scenes[currentIndex - 1].id)
    }
  }

  const handleNext = () => {
    if (currentIndex < scenes.length - 1 && !isTransitioning) {
      onSceneChange(scenes[currentIndex + 1].id)
    }
  }

  return (
    <>
      {/* Botón flotante para abrir navegador */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '20px',
          left: '20px',
          width: '50px',
          height: '50px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
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
        🎬
      </button>

      {/* Panel de navegación */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '80px',
          left: '20px',
          width: '320px',
          maxHeight: '500px',
          background: 'rgba(0, 0, 0, 0.85)',
          backdropFilter: 'blur(10px)',
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          zIndex: 999,
          overflowY: 'auto'
        }}>
          <h3 style={{
            margin: '0 0 15px 0',
            color: 'white',
            fontSize: '18px',
            fontWeight: 'bold'
          }}>
            🎬 Navegador de Escenas
          </h3>

          {/* Escena actual */}
          {currentScene && (
            <div style={{
              background: 'rgba(102, 126, 234, 0.2)',
              border: '2px solid #667eea',
              borderRadius: '8px',
              padding: '12px',
              marginBottom: '15px'
            }}>
              <div style={{
                color: '#667eea',
                fontSize: '12px',
                fontWeight: 'bold',
                marginBottom: '5px'
              }}>
                ESCENA ACTUAL
              </div>
              <div style={{
                color: 'white',
                fontSize: '16px',
                fontWeight: 'bold',
                marginBottom: '5px'
              }}>
                {currentScene.name}
              </div>
              <div style={{
                color: 'rgba(255,255,255,0.7)',
                fontSize: '13px'
              }}>
                {currentScene.description}
              </div>
            </div>
          )}

          {/* Barra de progreso durante transición */}
          {isTransitioning && (
            <div style={{
              marginBottom: '15px'
            }}>
              <div style={{
                color: 'rgba(255,255,255,0.7)',
                fontSize: '12px',
                marginBottom: '5px'
              }}>
                Cargando escena... {Math.round(loadingProgress)}%
              </div>
              <div style={{
                width: '100%',
                height: '4px',
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '2px',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${loadingProgress}%`,
                  height: '100%',
                  background: 'linear-gradient(90deg, #667eea, #764ba2)',
                  transition: 'width 0.3s'
                }} />
              </div>
            </div>
          )}

          {/* Controles de navegación */}
          <div style={{
            display: 'flex',
            gap: '10px',
            marginBottom: '20px'
          }}>
            <button
              onClick={handlePrevious}
              disabled={currentIndex === 0 || isTransitioning}
              style={{
                flex: 1,
                padding: '10px',
                background: currentIndex === 0 || isTransitioning 
                  ? 'rgba(255,255,255,0.1)' 
                  : 'rgba(102, 126, 234, 0.3)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '6px',
                color: 'white',
                cursor: currentIndex === 0 || isTransitioning ? 'not-allowed' : 'pointer',
                fontSize: '14px',
                fontWeight: 'bold',
                opacity: currentIndex === 0 || isTransitioning ? 0.5 : 1
              }}
            >
              ← Anterior
            </button>
            <button
              onClick={handleNext}
              disabled={currentIndex === scenes.length - 1 || isTransitioning}
              style={{
                flex: 1,
                padding: '10px',
                background: currentIndex === scenes.length - 1 || isTransitioning 
                  ? 'rgba(255,255,255,0.1)' 
                  : 'rgba(102, 126, 234, 0.3)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '6px',
                color: 'white',
                cursor: currentIndex === scenes.length - 1 || isTransitioning ? 'not-allowed' : 'pointer',
                fontSize: '14px',
                fontWeight: 'bold',
                opacity: currentIndex === scenes.length - 1 || isTransitioning ? 0.5 : 1
              }}
            >
              Siguiente →
            </button>
          </div>

          {/* Lista de todas las escenas */}
          <div style={{
            color: 'rgba(255,255,255,0.7)',
            fontSize: '12px',
            fontWeight: 'bold',
            marginBottom: '10px'
          }}>
            TODAS LAS ESCENAS ({scenes.length})
          </div>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}>
            {scenes.map((scene, index) => (
              <button
                key={scene.id}
                onClick={() => !isTransitioning && onSceneChange(scene.id)}
                disabled={isTransitioning}
                style={{
                  padding: '12px',
                  background: scene.id === currentSceneId 
                    ? 'rgba(102, 126, 234, 0.3)' 
                    : 'rgba(255,255,255,0.05)',
                  border: scene.id === currentSceneId 
                    ? '2px solid #667eea' 
                    : '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '6px',
                  color: 'white',
                  cursor: isTransitioning ? 'not-allowed' : 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.2s',
                  opacity: isTransitioning ? 0.5 : 1
                }}
                onMouseEnter={(e) => {
                  if (!isTransitioning && scene.id !== currentSceneId) {
                    e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (scene.id !== currentSceneId) {
                    e.currentTarget.style.background = 'rgba(255,255,255,0.05)'
                  }
                }}
              >
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px'
                }}>
                  <span style={{ fontSize: '20px' }}>
                    {index === 0 ? '🎬' : 
                     index === scenes.length - 1 ? '🎉' : 
                     scene.models.length > 1 ? '🌍' : '🗿'}
                  </span>
                  <div style={{ flex: 1 }}>
                    <div style={{
                      fontSize: '14px',
                      fontWeight: 'bold',
                      marginBottom: '3px'
                    }}>
                      {scene.name}
                    </div>
                    <div style={{
                      fontSize: '11px',
                      color: 'rgba(255,255,255,0.6)'
                    }}>
                      {scene.description}
                    </div>
                  </div>
                  {scene.id === currentSceneId && (
                    <span style={{
                      fontSize: '16px',
                      color: '#667eea'
                    }}>
                      ✓
                    </span>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  )
}
