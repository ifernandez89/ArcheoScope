'use client'

import dynamic from 'next/dynamic'
import UI from '@/components/UI'
import HelpPanel from '@/components/HelpPanel'

// Importar Scene3D dinámicamente para evitar SSR issues con Three.js
const Scene3D = dynamic(() => import('@/components/Scene3D'), {
  ssr: false,
  loading: () => (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%)',
      color: '#fff',
      fontFamily: 'monospace'
    }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{
          fontSize: '3rem',
          marginBottom: '1rem'
        }}>
          🏛️
        </div>
        <div style={{ fontSize: '1.25rem' }}>
          Inicializando visualizador 3D...
        </div>
      </div>
    </div>
  )
})

export default function Home() {
  return (
    <main>
      <Scene3D />
      <UI />
      <HelpPanel />
    </main>
  )
}
