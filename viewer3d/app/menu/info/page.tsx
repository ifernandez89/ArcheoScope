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
      justifyContent: 'flex-start',
      background: '#000000',
      margin: 0,
      padding: '40px 20px',
      overflow: 'auto',
      color: '#ffffff'
    }}>
      <h1 style={{
        fontSize: '48px',
        marginBottom: '20px',
        letterSpacing: '4px'
      }}>
        INFORMACIÓN
      </h1>
      
      {/* Contenedor de contenido con scroll */}
      <div style={{
        maxWidth: '800px',
        width: '100%',
        marginBottom: '30px',
        padding: '20px',
        overflowY: 'auto',
        maxHeight: 'calc(100vh - 200px)'
      }}>
        
        {/* Sección de Inspiración */}
        <section style={{
          marginBottom: '40px',
          padding: '30px',
          background: 'rgba(102, 126, 234, 0.1)',
          border: '1px solid rgba(102, 126, 234, 0.3)',
          borderRadius: '12px'
        }}>
          <h2 style={{
            fontSize: '32px',
            marginBottom: '20px',
            color: '#667eea',
            letterSpacing: '2px'
          }}>
            📜 Inspiración
          </h2>
          
          <p style={{
            fontSize: '16px',
            lineHeight: '1.8',
            marginBottom: '20px',
            opacity: 0.9
          }}>
            <strong>Archeoscope</strong> toma inspiración de diversas culturas antiguas, teorías arqueológicas y estudios sobre la conciencia.
          </p>
          
          <p style={{
            fontSize: '16px',
            lineHeight: '1.8',
            marginBottom: '20px',
            opacity: 0.9
          }}>
            Parte de su narrativa y concepto de <strong>red energética planetaria</strong> está influenciado por las ideas del investigador mexicano <strong>Jacobo Grinberg-Zylberbaum</strong>, especialmente su obra <em>La teoría sintérgica</em>.
          </p>
          
          <p style={{
            fontSize: '16px',
            lineHeight: '1.8',
            opacity: 0.9
          }}>
            Estas referencias han sido reinterpretadas libremente con fines artísticos y narrativos.
          </p>
        </section>
        
        {/* Sección de Créditos */}        
        <section style={{
          marginBottom: '20px',
          padding: '25px',
          background: 'rgba(139, 92, 46, 0.15)',
          border: '1px solid rgba(205, 133, 63, 0.4)',
          borderRadius: '8px',
          fontFamily: 'monospace'
        }}>
          <div style={{
            fontSize: '12px',
            color: '#cd853f',
            marginBottom: '15px',
            letterSpacing: '1px'
          }}>
            [Créditos]
          </div>
          
          <p style={{
            fontSize: '14px',
            lineHeight: '1.8',
            opacity: 0.9,
            fontStyle: 'italic'
          }}>
            "Algunos antiguos sistemas sugieren que la realidad es una red estructurada de información. Si dicha red es alterada, el espacio y el tiempo podrían deformarse."
          </p>
          
          <div style={{
            fontSize: '12px',
            color: '#cd853f',
            marginTop: '15px',
            opacity: 0.7
          }}>
            — Registro atribuido a un investigador previo a la desaparición.
          </div>
        </section>
      </div>
      
      <button
        onClick={() => router.push('/menu')}
        style={{
          padding: '20px 80px',
          fontSize: '24px',
          fontWeight: 'bold',
          color: '#ffffff',
          background: 'transparent',
          border: '2px solid #ffffff',
          borderRadius: '8px',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          letterSpacing: '2px',
          textTransform: 'uppercase',
          width: '350px',
          marginTop: '20px'
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
