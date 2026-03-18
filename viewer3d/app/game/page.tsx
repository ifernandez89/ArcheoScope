'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import UI from '@/components/UI'

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
          Cargando motor 3D...
        </div>
      </div>
    </div>
  )
})

export default function GamePage() {
  const [load3D, setLoad3D] = useState(false)
  
  // Cargar 3D después del primer render (permite que el bundle inicial sea más liviano)
  useEffect(() => {
    // Pequeño delay para que la UI se renderice primero
    const timer = setTimeout(() => {
      setLoad3D(true)
    }, 100)
    
    return () => clearTimeout(timer)
  }, [])
  
  return (
    <main>
      {load3D && <Scene3D />}
      <UI />
    </main>
  )
}
