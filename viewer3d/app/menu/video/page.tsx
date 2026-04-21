'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { type QualityPreset, GRAPHICS_PRESETS } from '@/systems/GraphicsPresets'

const PRESET_INFO: Record<string, { label: string; icon: string; desc: string; color: string }> = {
  LOW: {
    label: 'Baja',
    icon: '🔋',
    desc: 'Sin sombras, sin bloom, resolución reducida. Ideal para laptops o navegadores lentos.',
    color: '#4ade80',
  },
  MEDIUM: {
    label: 'Media',
    icon: '⚡',
    desc: 'Sombras básicas, antialiasing, resolución nativa. Buen balance rendimiento/calidad.',
    color: '#fbbf24',
  },
  HIGH: {
    label: 'Alta',
    icon: '🔥',
    desc: 'Sombras suaves, bloom, SSAO, más luces y vegetación. Requiere GPU dedicada.',
    color: '#f97316',
  },
}

const PRESET_DETAILS: Record<string, Array<{ feature: string; enabled: boolean }>> = {
  LOW: [
    { feature: 'Sombras', enabled: false },
    { feature: 'Bloom', enabled: false },
    { feature: 'Antialiasing', enabled: false },
    { feature: 'SSAO', enabled: false },
    { feature: 'Resolución', enabled: true },
  ],
  MEDIUM: [
    { feature: 'Sombras', enabled: true },
    { feature: 'Bloom', enabled: false },
    { feature: 'Antialiasing', enabled: true },
    { feature: 'SSAO', enabled: false },
    { feature: 'Resolución', enabled: true },
  ],
  HIGH: [
    { feature: 'Sombras', enabled: true },
    { feature: 'Bloom', enabled: true },
    { feature: 'Antialiasing', enabled: true },
    { feature: 'SSAO', enabled: true },
    { feature: 'Resolución', enabled: true },
  ],
}

export default function VideoPage() {
  const router = useRouter()
  const [selected, setSelected] = useState<QualityPreset>('MEDIUM')

  useEffect(() => {
    const saved = localStorage.getItem('graphics_preset')
    if (saved && (saved === 'LOW' || saved === 'MEDIUM' || saved === 'HIGH')) {
      setSelected(saved as QualityPreset)
    }
  }, [])

  const handleSelect = (preset: QualityPreset) => {
    setSelected(preset)
    localStorage.setItem('graphics_preset', preset)
  }

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'flex-start',
      background: '#000000', margin: 0, padding: '40px 20px',
      overflow: 'auto', color: '#ffffff',
    }}>
      <h1 style={{
        fontSize: '48px', marginBottom: '30px',
        letterSpacing: '4px', fontFamily: 'Archeoscope, serif',
      }}>
        VIDEO
      </h1>

      <div style={{
        display: 'flex', gap: '24px', flexWrap: 'wrap',
        justifyContent: 'center', maxWidth: '900px', marginBottom: '40px',
      }}>
        {(['LOW', 'MEDIUM', 'HIGH'] as QualityPreset[]).map((preset) => {
          const info = PRESET_INFO[preset]
          const details = PRESET_DETAILS[preset]
          const isActive = selected === preset

          return (
            <div
              key={preset}
              onClick={() => handleSelect(preset)}
              style={{
                width: '260px',
                padding: '28px 24px',
                background: isActive ? `rgba(255,255,255,0.08)` : 'rgba(255,255,255,0.02)',
                border: `2px solid ${isActive ? info.color : 'rgba(255,255,255,0.15)'}`,
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                transform: isActive ? 'scale(1.03)' : 'scale(1)',
                boxShadow: isActive ? `0 0 20px ${info.color}40` : 'none',
              }}
            >
              <div style={{ textAlign: 'center', fontSize: '36px', marginBottom: '12px' }}>
                {info.icon}
              </div>
              <div style={{
                textAlign: 'center', fontSize: '24px', fontWeight: 'bold',
                color: isActive ? info.color : '#888',
                fontFamily: 'Archeoscope, serif', letterSpacing: '2px',
                marginBottom: '12px',
              }}>
                {info.label}
              </div>
              <p style={{
                fontSize: '13px', color: 'rgba(255,255,255,0.6)',
                textAlign: 'center', lineHeight: '1.5', marginBottom: '16px',
              }}>
                {info.desc}
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {details.map((d) => (
                  <div key={d.feature} style={{
                    display: 'flex', justifyContent: 'space-between',
                    fontSize: '13px', color: 'rgba(255,255,255,0.5)',
                  }}>
                    <span>{d.feature}</span>
                    <span style={{ color: d.enabled ? '#4ade80' : '#ef4444' }}>
                      {d.enabled ? '✓' : '✗'}
                    </span>
                  </div>
                ))}
              </div>

              {isActive && (
                <div style={{
                  marginTop: '14px', textAlign: 'center',
                  fontSize: '12px', color: info.color,
                  fontWeight: 'bold', letterSpacing: '1px',
                }}>
                  ● ACTIVO
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Detalles técnicos del preset seleccionado */}
      <div style={{
        maxWidth: '600px', width: '100%',
        padding: '20px', background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px',
        marginBottom: '30px',
      }}>
        <h3 style={{
          fontSize: '16px', color: PRESET_INFO[selected].color,
          marginBottom: '12px', fontFamily: 'Archeoscope, serif',
        }}>
          Detalles técnicos — {PRESET_INFO[selected].label}
        </h3>
        <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)', lineHeight: '1.8' }}>
          <div>Pixel Ratio: <strong style={{ color: '#fff' }}>{GRAPHICS_PRESETS[selected].pixelRatio}x</strong></div>
          <div>Shadow Map: <strong style={{ color: '#fff' }}>{GRAPHICS_PRESETS[selected].shadowMapSize}px</strong></div>
          <div>Max Luces: <strong style={{ color: '#fff' }}>{GRAPHICS_PRESETS[selected].maxLights}</strong></div>
          <div>Draw Distance: <strong style={{ color: '#fff' }}>{GRAPHICS_PRESETS[selected].maxDrawDistance}</strong></div>
          <div>Max Instancias: <strong style={{ color: '#fff' }}>{GRAPHICS_PRESETS[selected].maxInstancesPerMesh.toLocaleString()}</strong></div>
        </div>
      </div>

      <button
        onClick={() => router.push('/menu')}
        style={{
          padding: '20px 80px', fontSize: '24px', fontWeight: 'bold',
          color: '#ffffff', background: 'transparent',
          border: '2px solid #ffffff', borderRadius: '8px',
          cursor: 'pointer', transition: 'all 0.3s ease',
          letterSpacing: '2px', textTransform: 'uppercase', width: '350px',
        }}
        onMouseEnter={(e) => { e.currentTarget.style.background = '#ffffff'; e.currentTarget.style.color = '#000000' }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#ffffff' }}
      >
        Volver
      </button>
    </main>
  )
}
