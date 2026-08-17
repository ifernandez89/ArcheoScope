'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import UI from '@/components/UI'
import { useProgress } from '@react-three/drei'
import { getAssetPath } from '@/lib/paths'

const LOGO_LOADING = getAssetPath('/branding/loading/logo-loading.png')

function LoadingScreen() {
  const { progress, active } = useProgress()
  const [opacity, setOpacity] = useState(0)
  useEffect(() => {
    const t = setTimeout(() => setOpacity(1), 50)
    return () => clearTimeout(t)
  }, [])

  return (
    <div style={{
      width: '100vw', height: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%)',
      color: '#fff', fontFamily: 'monospace',
      opacity, transition: 'opacity 0.5s ease'
    }}>
      <div style={{
        marginBottom: '32px',
        animation: 'logoPulse 3s ease-in-out infinite'
      }}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={LOGO_LOADING}
          alt="Archeoscope: The Forgotten Relics"
          style={{ width: '240px', height: '240px', objectFit: 'contain' }}
        />
      </div>

      {/* Barra de progreso */}
      <div style={{ width: '320px', marginBottom: '16px' }}>
        <div style={{
          width: '100%', height: '4px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '2px', overflow: 'hidden'
        }}>
          <div style={{
            height: '100%',
            width: `${progress}%`,
            background: 'linear-gradient(90deg, #667eea, #764ba2)',
            borderRadius: '2px',
            transition: 'width 0.3s ease',
            boxShadow: '0 0 8px rgba(102,126,234,0.8)'
          }} />
        </div>
      </div>

      <div style={{
        fontSize: '12px', letterSpacing: '3px',
        color: 'rgba(255,255,255,0.4)', textTransform: 'uppercase'
      }}>
        {active ? `Cargando... ${Math.round(progress)}%` : 'Iniciando mundo...'}
      </div>

      <style>{`
        @keyframes logoPulse {
          0%, 100% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.6)); }
          50% { filter: drop-shadow(0 0 35px rgba(102, 126, 234, 0.9)); }
        }
      `}</style>
    </div>
  )
}

// Importar Scene3D dinámicamente para evitar SSR issues con Three.js
const Scene3D = dynamic(() => import('@/components/Scene3D'), {
  ssr: false,
  loading: () => <LoadingScreen />
})

export default function GamePage() {
  const [load3D, setLoad3D] = useState(false)
  
  useEffect(() => {
    const timer = setTimeout(() => setLoad3D(true), 100)
    return () => clearTimeout(timer)
  }, [])
  
  return (
    <main>
      {load3D && <Scene3D />}
      <UI />
    </main>
  )
}
