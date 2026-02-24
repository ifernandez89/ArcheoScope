'use client'

import { useState } from 'react'

interface AudioControlProps {
  onEnable: () => Promise<void>
  enabled: boolean
  masterVolume: number
  onVolumeChange: (volume: number) => void
}

export default function AudioControl({ 
  onEnable, 
  enabled, 
  masterVolume, 
  onVolumeChange 
}: AudioControlProps) {
  const [isEnabling, setIsEnabling] = useState(false)
  const [showVolume, setShowVolume] = useState(false)

  const handleEnable = async () => {
    setIsEnabling(true)
    try {
      await onEnable()
    } catch (error) {
      console.error('Error habilitando audio:', error)
    } finally {
      setIsEnabling(false)
    }
  }

  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      right: '20px',
      zIndex: 1002,
      display: 'flex',
      flexDirection: 'column',
      gap: '8px',
      alignItems: 'flex-end'
    }}>
      {!enabled ? (
        <button
          onClick={handleEnable}
          disabled={isEnabling}
          style={{
            padding: '12px 24px',
            background: isEnabling ? 'rgba(75, 85, 99, 0.7)' : 'rgba(139, 92, 246, 0.9)',
            border: '1px solid rgba(255,255,255,0.3)',
            borderRadius: '8px',
            color: 'white',
            fontSize: '14px',
            fontWeight: 'bold',
            cursor: isEnabling ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            transition: 'all 0.2s',
            boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
          }}
          onMouseEnter={(e) => {
            if (!isEnabling) {
              e.currentTarget.style.background = 'rgba(139, 92, 246, 1)'
            }
          }}
          onMouseLeave={(e) => {
            if (!isEnabling) {
              e.currentTarget.style.background = 'rgba(139, 92, 246, 0.9)'
            }
          }}
        >
          {isEnabling ? '⏳ Habilitando...' : '🔊 Habilitar Audio'}
        </button>
      ) : (
        <>
          <button
            onClick={() => setShowVolume(!showVolume)}
            style={{
              padding: '12px 24px',
              background: 'rgba(34, 197, 94, 0.9)',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '8px',
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.2s',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(34, 197, 94, 1)'}
            onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(34, 197, 94, 0.9)'}
          >
            🔊 Audio: ON
          </button>

          {showVolume && (
            <div style={{
              background: 'rgba(0, 0, 0, 0.9)',
              backdropFilter: 'blur(10px)',
              padding: '16px',
              borderRadius: '8px',
              border: '1px solid rgba(255,255,255,0.2)',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
              minWidth: '200px'
            }}>
              <div style={{
                color: 'white',
                fontSize: '12px',
                fontWeight: 'bold',
                marginBottom: '4px'
              }}>
                Volumen Master
              </div>
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.01"
                value={masterVolume}
                onChange={(e) => onVolumeChange(parseFloat(e.target.value))}
                style={{
                  width: '100%',
                  cursor: 'pointer'
                }}
              />
              <div style={{
                color: '#888',
                fontSize: '11px',
                textAlign: 'center'
              }}>
                {Math.round(masterVolume * 100)}%
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
