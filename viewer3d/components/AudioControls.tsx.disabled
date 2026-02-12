'use client'

import { useState, useEffect } from 'react'
import type { AudioSystem } from '@/core/audio'

interface AudioControlsProps {
  audioSystem: AudioSystem | null
}

export default function AudioControls({ audioSystem }: AudioControlsProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [masterVolume, setMasterVolume] = useState(100)
  const [musicVolume, setMusicVolume] = useState(70)
  const [narrationVolume, setNarrationVolume] = useState(100)
  const [effectsVolume, setEffectsVolume] = useState(80)

  useEffect(() => {
    if (audioSystem) {
      setIsMuted(audioSystem.isMutedState())
      setMasterVolume(audioSystem.getMasterVolume() * 100)
      setMusicVolume(audioSystem.getMusicVolume() * 100)
      setNarrationVolume(audioSystem.getNarrationVolume() * 100)
      setEffectsVolume(audioSystem.getEffectsVolume() * 100)
    }
  }, [audioSystem])

  const handleMuteToggle = () => {
    if (audioSystem) {
      audioSystem.toggleMute()
      setIsMuted(audioSystem.isMutedState())
    }
  }

  const handleMasterVolumeChange = (value: number) => {
    setMasterVolume(value)
    if (audioSystem) {
      audioSystem.setMasterVolume(value / 100)
    }
  }

  const handleMusicVolumeChange = (value: number) => {
    setMusicVolume(value)
    if (audioSystem) {
      audioSystem.setMusicVolume(value / 100)
    }
  }

  const handleNarrationVolumeChange = (value: number) => {
    setNarrationVolume(value)
    if (audioSystem) {
      audioSystem.setNarrationVolume(value / 100)
    }
  }

  const handleEffectsVolumeChange = (value: number) => {
    setEffectsVolume(value)
    if (audioSystem) {
      audioSystem.setEffectsVolume(value / 100)
    }
  }

  if (!audioSystem) return null

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          width: '50px',
          height: '50px',
          borderRadius: '50%',
          background: isMuted 
            ? 'linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)'
            : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
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
        {isMuted ? '🔇' : '🔊'}
      </button>

      {/* Panel de controles */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          top: '80px',
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
            🎵 Control de Audio
          </h3>

          {/* Botón Mute/Unmute */}
          <button
            onClick={handleMuteToggle}
            style={{
              width: '100%',
              padding: '12px',
              marginBottom: '20px',
              background: isMuted 
                ? 'rgba(255, 107, 107, 0.3)' 
                : 'rgba(79, 172, 254, 0.3)',
              border: isMuted 
                ? '2px solid #ff6b6b' 
                : '2px solid #4facfe',
              borderRadius: '8px',
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            {isMuted ? '🔇 Activar Audio' : '🔊 Silenciar Todo'}
          </button>

          {/* Volumen Master */}
          <VolumeSlider
            label="Volumen General"
            icon="🎚️"
            value={masterVolume}
            onChange={handleMasterVolumeChange}
            disabled={isMuted}
          />

          {/* Volumen Música */}
          <VolumeSlider
            label="Música de Fondo"
            icon="🎵"
            value={musicVolume}
            onChange={handleMusicVolumeChange}
            disabled={isMuted}
          />

          {/* Volumen Narración */}
          <VolumeSlider
            label="Narración"
            icon="🎙️"
            value={narrationVolume}
            onChange={handleNarrationVolumeChange}
            disabled={isMuted}
          />

          {/* Volumen Efectos */}
          <VolumeSlider
            label="Efectos de Sonido"
            icon="🔔"
            value={effectsVolume}
            onChange={handleEffectsVolumeChange}
            disabled={isMuted}
          />
        </div>
      )}
    </>
  )
}

// Componente auxiliar para sliders de volumen
function VolumeSlider({
  label,
  icon,
  value,
  onChange,
  disabled
}: {
  label: string
  icon: string
  value: number
  onChange: (value: number) => void
  disabled: boolean
}) {
  return (
    <div style={{
      marginBottom: '15px',
      opacity: disabled ? 0.5 : 1,
      transition: 'opacity 0.2s'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '8px'
      }}>
        <span style={{
          color: 'rgba(255,255,255,0.9)',
          fontSize: '13px',
          fontWeight: '500'
        }}>
          {icon} {label}
        </span>
        <span style={{
          color: 'rgba(255,255,255,0.7)',
          fontSize: '12px',
          fontWeight: 'bold'
        }}>
          {Math.round(value)}%
        </span>
      </div>
      <input
        type="range"
        min="0"
        max="100"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        disabled={disabled}
        style={{
          width: '100%',
          height: '6px',
          borderRadius: '3px',
          background: `linear-gradient(to right, #4facfe 0%, #4facfe ${value}%, rgba(255,255,255,0.1) ${value}%, rgba(255,255,255,0.1) 100%)`,
          outline: 'none',
          cursor: disabled ? 'not-allowed' : 'pointer',
          WebkitAppearance: 'none',
          appearance: 'none'
        }}
      />
      <style jsx>{`
        input[type="range"]::-webkit-slider-thumb {
          -webkit-appearance: none;
          appearance: none;
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: white;
          cursor: pointer;
          box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }
        input[type="range"]::-moz-range-thumb {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: white;
          cursor: pointer;
          border: none;
          box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }
      `}</style>
    </div>
  )
}
