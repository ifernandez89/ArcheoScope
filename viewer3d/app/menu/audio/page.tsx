'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { loadGameSettings, updateAudioSettings } from '@/types/gameSettings'
import { getHarmoniaMundi } from '@/systems/HarmoniaMundiSystem'
import { getProceduralAudio } from '@/systems/ProceduralAudio'

export default function AudioPage() {
  const router = useRouter()
  const [masterVolume, setMasterVolume] = useState(70)   // Clima + efectos
  const [harmoniaVolume, setHarmoniaVolume] = useState(70) // Música de esferas

  useEffect(() => {
    const settings = loadGameSettings()
    setMasterVolume(Math.round(settings.audio.masterVolume * 100))
    setHarmoniaVolume(Math.round((settings.audio.musicVolume ?? 0.7) * 100))
  }, [])

  const handleSave = () => {
    const vol = masterVolume / 100
    const harmVol = harmoniaVolume / 100

    updateAudioSettings({
      masterVolume: vol,
      musicVolume: harmVol,
      sfxVolume: vol
    })

    // Clima, lluvia, viento
    getProceduralAudio().setMasterVolume(vol)

    // Música de esferas / misiones
    const harmonia = getHarmoniaMundi()
    harmonia.setMasterVolume(harmVol)

    router.push('/menu')
  }

  const sliderStyle = (value: number, color: string) => ({
    width: '100%',
    height: '8px',
    borderRadius: '4px',
    outline: 'none',
    cursor: 'pointer',
    background: `linear-gradient(to right, ${color} 0%, ${color} ${value}%, #333 ${value}%, #333 100%)`
  })

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: '#000', color: '#fff'
    }}>
      <h1 style={{ fontSize: '48px', marginBottom: '60px', letterSpacing: '4px' }}>
        AUDIO
      </h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '40px', width: '600px' }}>

        {/* Volumen General */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <label style={{ fontSize: '22px', letterSpacing: '2px', textTransform: 'uppercase' }}>
            🌦️ Volumen General: {masterVolume}%
          </label>
          <input
            type="range" min="0" max="100" value={masterVolume}
            onChange={(e) => setMasterVolume(parseInt(e.target.value))}
            style={sliderStyle(masterVolume, '#4a9eff') as React.CSSProperties}
          />
          <span style={{ fontSize: '13px', color: '#888' }}>
            Controla el clima, lluvia, viento y efectos de sonido
          </span>
        </div>

        {/* Separador */}
        <div style={{ height: '1px', background: '#333' }} />

        {/* Música de Esferas */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <label style={{ fontSize: '22px', letterSpacing: '2px', textTransform: 'uppercase', color: '#FFD700' }}>
            🎼 Música de las Esferas: {harmoniaVolume}%
          </label>
          <input
            type="range" min="0" max="100" value={harmoniaVolume}
            onChange={(e) => setHarmoniaVolume(parseInt(e.target.value))}
            style={sliderStyle(harmoniaVolume, '#FFD700') as React.CSSProperties}
          />
          <span style={{ fontSize: '13px', color: '#888' }}>
            Música cósmica procedural — se despierta con cada misión completada
          </span>
        </div>
      </div>

      {/* Botones */}
      <div style={{ display: 'flex', gap: '20px', marginTop: '70px' }}>
        <button
          onClick={() => router.push('/menu')}
          style={{
            padding: '18px 70px', fontSize: '20px', fontWeight: 'bold',
            color: '#fff', background: 'transparent', border: '2px solid #fff',
            borderRadius: '8px', cursor: 'pointer', letterSpacing: '2px', textTransform: 'uppercase'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.background = '#fff'; e.currentTarget.style.color = '#000' }}
          onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#fff' }}
        >
          Cancelar
        </button>
        <button
          onClick={handleSave}
          style={{
            padding: '18px 70px', fontSize: '20px', fontWeight: 'bold',
            color: '#000', background: '#4a9eff', border: '2px solid #4a9eff',
            borderRadius: '8px', cursor: 'pointer', letterSpacing: '2px', textTransform: 'uppercase'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.background = '#6ab7ff' }}
          onMouseLeave={(e) => { e.currentTarget.style.background = '#4a9eff' }}
        >
          Guardar
        </button>
      </div>
    </main>
  )
}
