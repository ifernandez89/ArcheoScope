'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function ResetPage() {
  const router = useRouter()
  const [reset, setReset] = useState(false)

  const handleReset = () => {
    if (typeof window !== 'undefined') {
      // Limpiar todo el localStorage
      localStorage.clear()
      sessionStorage.clear()
      console.log('🗑️ Todos los datos del juego han sido eliminados')
      setReset(true)
      
      // Redirigir al inicio después de 2 segundos
      setTimeout(() => {
        router.push('/')
      }, 2000)
    }
  }

  return (
    <main style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#000000',
      margin: 0,
      padding: 0,
      overflow: 'hidden',
      color: '#ffffff',
      gap: '40px'
    }}>
      {!reset ? (
        <>
          <h1 style={{
            fontSize: '48px',
            marginBottom: '20px',
            letterSpacing: '4px',
            textAlign: 'center',
            fontFamily: 'Archeoscope, serif'
          }}>
            RESETEAR JUEGO
          </h1>
          
          <p style={{
            fontSize: '18px',
            color: '#cccccc',
            textAlign: 'center',
            maxWidth: '500px',
            lineHeight: '1.6'
          }}>
            Esto eliminará todos los datos guardados incluyendo:
            <br />• Configuración del jugador
            <br />• Nave seleccionada
            <br />• Progreso de misiones
            <br />• Configuración de audio
          </p>

          <div style={{
            display: 'flex',
            gap: '20px'
          }}>
            <button
              onClick={() => router.push('/menu')}
              style={{
                padding: '15px 40px',
                fontSize: '18px',
                color: '#ffffff',
                background: 'transparent',
                border: '2px solid #ffffff',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                letterSpacing: '2px',
                textTransform: 'uppercase'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#ffffff'
                e.currentTarget.style.color = '#000000'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent'
                e.currentTarget.style.color = '#ffffff'
              }}
            >
              Cancelar
            </button>

            <button
              onClick={handleReset}
              style={{
                padding: '15px 40px',
                fontSize: '18px',
                color: '#ffffff',
                background: '#ef4444',
                border: '2px solid #ef4444',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                letterSpacing: '2px',
                textTransform: 'uppercase'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#dc2626'
                e.currentTarget.style.borderColor = '#dc2626'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = '#ef4444'
                e.currentTarget.style.borderColor = '#ef4444'
              }}
            >
              Resetear
            </button>
          </div>
        </>
      ) : (
        <>
          <h1 style={{
            fontSize: '48px',
            color: '#4ade80',
            letterSpacing: '4px',
            fontFamily: 'Archeoscope, serif'
          }}>
            ✓ DATOS ELIMINADOS
          </h1>
          <p style={{
            fontSize: '18px',
            color: '#cccccc'
          }}>
            Redirigiendo al inicio...
          </p>
        </>
      )}
    </main>
  )
}
