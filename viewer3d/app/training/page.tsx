'use client'

import dynamic from 'next/dynamic'
import TrainingUI from '@/components/TrainingUI'

// Importar TrainingRoom dinámicamente para evitar SSR issues con Three.js
const TrainingRoom = dynamic(() => import('@/components/TrainingRoom'), {
  ssr: false,
  loading: () => (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#000000',
      color: '#ffffff',
      fontFamily: 'monospace'
    }}>
      PREPARANDO SALA DE ENTRENAMIENTO...
    </div>
  )
})

export default function TrainingPage() {
  return (
    <main style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
      <TrainingRoom />
      <TrainingUI />
    </main>
  )
}
