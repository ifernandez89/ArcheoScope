'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import UI from '@/components/UI'
import { getAssetPath } from '@/lib/paths'

function LoadingScreen() {
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
          src={getAssetPath('/branding/loading/logo-loading.png')}
          alt="Archeoscope: The Forgotten Relics"
          style={{ width: '280px', height: '280px', objectFit: 'contain' }}
        />
      </div>
      <div style={{
        fontSize: '13px', letterSpacing: '4px',
        color: 'rgba(255,255,255,0.5)', textTransform: 'uppercase',
        animation: 'textPulse 1.5s ease-in-out infinite'
      }}>
        Cargando motor 3D...
      </div>
      <style>{`
        @keyframes logoPulse {
          0%, 100% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.6)); }
          50% { filter: drop-shadow(0 0 35px rgba(102, 126, 234, 0.9)); }
        }
        @keyframes textPulse {
          0%, 100% { opacity: 0.5; }
          50% { opacity: 1; }
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
