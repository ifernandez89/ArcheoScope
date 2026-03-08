'use client'

import { useRouter } from 'next/navigation'

export default function InfoPage() {
  const router = useRouter()

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
      color: '#ffffff'
    }}>
      <h1 style={{
        fontSize: '48px',
        marginBottom: '40px',
        letterSpacing: '4px'
      }}>
        INFORMACIÓN
      </h1>
      
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
        Volver
      </button>
    </main>
  )
}
