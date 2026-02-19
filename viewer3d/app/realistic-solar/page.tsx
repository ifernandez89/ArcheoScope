'use client'

import dynamic from 'next/dynamic'

/**
 * Página de prueba para el Sistema Solar Realista
 * 
 * Acceso: http://localhost:3000/realistic-solar
 * 
 * ⚡ OPTIMIZACIÓN: Dynamic import para NO cargar en bundle inicial
 */

// Dynamic import - NO se carga hasta que se accede a esta página
const RealisticSolarSystemScene = dynamic(
  () => import('@/components/RealisticSolarSystemScene'),
  { 
    ssr: false,
    loading: () => (
      <div style={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#000',
        color: '#fff',
        fontSize: '24px'
      }}>
        🌍 Cargando Sistema Solar...
      </div>
    )
  }
)

export default function RealisticSolarPage() {
  return (
    <main style={{ width: '100vw', height: '100vh', margin: 0, padding: 0 }}>
      <RealisticSolarSystemScene />
    </main>
  )
}
