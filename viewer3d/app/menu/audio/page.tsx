'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { loadGameSettings, updateAudioSettings } from '@/types/gameSettings'
import { getProceduralAudio } from '@/systems/ProceduralAudio'

export default function AudioPage() {
  const router = useRouter()
  const [masterVolume, setMasterVolume] = useState(70)
  const [harmoniaVolume, setHarmoniaVolume] = useState(70)
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    setIsMobile(/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768)
    const settings = loadGameSettings()
    setMasterVolume(Math.round(settings.audio.masterVolume * 100))
    setHarmoniaVolume(Math.round((settings.audio.musicVolume ?? 0.7) * 100))
  }, [])

  const handleSave = () => {
    const vol = masterVolume / 100
    const harmVol = harmoniaVolume / 100
    updateAudioSettings({ masterVolume: vol, musicVolume: harmVol, sfxVolume: vol })
    getProceduralAudio().setMasterVolume(vol)
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      getHarmoniaMundi().setMasterVolume(harmVol)
    })
    router.push('/menu')
  }

  const sliderBg = (value: number, color: string) =>
    `linear-gradient(to right, ${color} 0%, ${color} ${value}%, #333 ${value}%, #333 100%)`

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: '#000', color: '#fff',
      padding: isMobile ? '16px' : '40px', boxSizing: 'border-box'
    }}>
      <h1 style={{
        fontSize: isMobile ? '24px' : '48px',
        marginBottom: isMobile ? '30px' : '60px',
        letterSpacing: '4px', fontFamily: 'Archeoscope, serif'
      }}>
        AUDIO
      </h1>

      <div style={{
        display: 'flex', flexDirection: 'column',
        gap: isMobile ? '24px' : '40px',
        width: isMobile ? '100%' : '600px', maxWidth: '100%'
      }}>
        {/* Volumen General */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: isMobile ? '8px' : '15px' }}>
          <label style={{ fontSize: isMobile ? '15px' : '22px', letterSpacing: '2px', textTransform: 'uppercase' }}>
            🌦️ Volumen General: {masterVolume}%
          </label>
          <input
            type="range" min="0" max="100" value={masterVolume}
            onChange={(e) => setMasterVolume(parseInt(e.target.value))}
            style={{ width: '100%', height: '8px', borderRadius: '4px', outline: 'none', cursor: 'pointer', background: sliderBg(masterVolume, '#4a9eff') }}
          />
          <span style={{ fontSize: isMobile ? '12px' : '16px', color: '#888' }}>
            Clima, lluvia, viento y efectos
          </span>
        </div>

        <div style={{ height: '1px', background: '#333' }} />

        {/* Música de Esferas */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: isMobile ? '8px' : '15px' }}>
          <label style={{ fontSize: isMobile ? '15px' : '22px', letterSpacing: '2px', textTransform: 'uppercase', color: '#FFD700' }}>
            🎼 Música de las Esferas: {harmoniaVolume}%
          </label>
          <input
            type="range" min="0" max="100" value={harmoniaVolume}
            onChange={(e) => setHarmoniaVolume(parseInt(e.target.value))}
            style={{ width: '100%', height: '8px', borderRadius: '4px', outline: 'none', cursor: 'pointer', background: sliderBg(harmoniaVolume, '#FFD700') }}
          />
          <span style={{ fontSize: isMobile ? '12px' : '16px', color: '#888' }}>
            Música cósmica procedural — se despierta con cada misión
          </span>
        </div>
      </div>

      {/* Botones */}
      <div style={{
        display: 'flex', gap: isMobile ? '12px' : '20px',
        marginTop: isMobile ? '30px' : '70px',
        flexDirection: isMobile ? 'column' : 'row',
        width: isMobile ? '100%' : 'auto'
      }}>
        <button
          onClick={() => router.push('/menu')}
          style={{
            padding: isMobile ? '14px 24px' : '18px 70px',
            fontSize: isMobile ? '16px' : '20px', fontWeight: 'bold',
            color: '#fff', background: 'transparent', border: '2px solid #fff',
            borderRadius: '8px', cursor: 'pointer', letterSpacing: '2px',
            textTransform: 'uppercase', width: isMobile ? '100%' : 'auto'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.background = '#fff'; e.currentTarget.style.color = '#000' }}
          onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#fff' }}
        >
          Cancelar
        </button>
        <button
          onClick={handleSave}
          style={{
            padding: isMobile ? '14px 24px' : '18px 70px',
            fontSize: isMobile ? '16px' : '20px', fontWeight: 'bold',
            color: '#000', background: '#4a9eff', border: '2px solid #4a9eff',
            borderRadius: '8px', cursor: 'pointer', letterSpacing: '2px',
            textTransform: 'uppercase', width: isMobile ? '100%' : 'auto'
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
