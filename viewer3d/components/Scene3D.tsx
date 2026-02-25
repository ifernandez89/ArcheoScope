'use client'

import { useState, useEffect } from 'react'
import ImmersiveScene from './ImmersiveScene'
import * as THREE from 'three'

export default function Scene3D() {
  const [loadedModel, setLoadedModel] = useState<THREE.Object3D | null>(null)
  const [camera, setCamera] = useState<THREE.Camera | null>(null)
  const [showUfoSelector, setShowUfoSelector] = useState(false)
  const [spaceUfoActive, setSpaceUfoActive] = useState(false)
  const [currentSpaceUfo, setCurrentSpaceUfo] = useState(1)
  const [isGlobeMode, setIsGlobeMode] = useState(true)

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      {/* Escena inmersiva con Globe 3D y modelos */}
      <ImmersiveScene
        onModelLoaded={setLoadedModel}
        onCameraReady={setCamera}
        onModeChange={(mode) => {
          setIsGlobeMode(mode === 'globe')
        }}
        spaceUfoActive={spaceUfoActive}
        spaceUfoNumber={currentSpaceUfo}
      />

      {/* Selector de UFO Espacial - Solo en modo globo */}
      {isGlobeMode && (
        <>
          <button
            onClick={() => setShowUfoSelector(!showUfoSelector)}
            style={{
              position: 'fixed',
              top: '20px',
              left: '20px',
              zIndex: 1002,
              padding: '12px 20px',
              background: spaceUfoActive 
                ? 'rgba(139, 92, 246, 0.9)' 
                : 'rgba(75, 85, 99, 0.7)',
              border: spaceUfoActive
                ? '2px solid rgba(139, 92, 246, 1)'
                : '1px solid rgba(255,255,255,0.3)',
              borderRadius: '8px',
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              transition: 'all 0.2s',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
              backdropFilter: 'blur(10px)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = spaceUfoActive
                ? 'rgba(139, 92, 246, 1)'
                : 'rgba(75, 85, 99, 0.9)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = spaceUfoActive
                ? 'rgba(139, 92, 246, 0.9)'
                : 'rgba(75, 85, 99, 0.7)'
            }}
          >
            ðŸŒ
          </button>

          {/* Selector desplegable de UFOs */}
          {showUfoSelector && (
            <div
              style={{
                position: 'fixed',
                top: '70px',
                left: '20px',
                zIndex: 2000,
                background: 'rgba(0, 0, 0, 0.9)',
                backdropFilter: 'blur(10px)',
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.3)',
                padding: '8px',
                minWidth: '150px'
              }}
            >
              {[1, 2, 3, 4, 5].map(ufoNum => (
                <button
                  key={ufoNum}
                  onClick={() => {
                    setCurrentSpaceUfo(ufoNum)
                    setSpaceUfoActive(true)
                    setShowUfoSelector(false)
                  }}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    background: currentSpaceUfo === ufoNum 
                      ? 'rgba(139, 92, 246, 0.5)' 
                      : 'transparent',
                    border: 'none',
                    borderRadius: '4px',
                    color: 'white',
                    fontSize: '14px',
                    cursor: 'pointer',
                    textAlign: 'center',
                    marginBottom: '4px',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    if (currentSpaceUfo !== ufoNum) {
                      e.currentTarget.style.background = 'rgba(139, 92, 246, 0.3)'
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (currentSpaceUfo !== ufoNum) {
                      e.currentTarget.style.background = 'transparent'
                    }
                  }}
                >
                  ðŸŒ
                </button>
              ))}
              
              {/* Opción para desactivar */}
              <button
                onClick={() => {
                  setSpaceUfoActive(false)
                  setShowUfoSelector(false)
                }}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  background: !spaceUfoActive ? 'rgba(239, 68, 68, 0.5)' : 'transparent',
                  border: 'none',
                  borderRadius: '4px',
                  color: 'white',
                  fontSize: '14px',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => {
                  if (spaceUfoActive) {
                    e.currentTarget.style.background = 'rgba(239, 68, 68, 0.3)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (spaceUfoActive) {
                    e.currentTarget.style.background = 'transparent'
                  }
                }}
              >
                ❌ Desactivar
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
