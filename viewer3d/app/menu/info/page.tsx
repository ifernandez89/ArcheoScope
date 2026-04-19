'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { useEffect, useRef, Suspense } from 'react'

function InfoContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const isCredits = searchParams.get('credits') === 'true'
  const scrollRef = useRef<HTMLDivElement>(null)

  // Auto-scroll cuando viene desde Göbekli Tepe
  useEffect(() => {
    if (!isCredits || !scrollRef.current) return
    const el = scrollRef.current
    const totalHeight = el.scrollHeight - el.clientHeight
    if (totalHeight <= 0) return
    // Scroll suave: ~60px por segundo
    const duration = (totalHeight / 60) * 1000
    const start = performance.now()
    let raf: number
    const step = (now: number) => {
      const elapsed = now - start
      const progress = Math.min(elapsed / duration, 1)
      el.scrollTop = progress * totalHeight
      if (progress < 1) raf = requestAnimationFrame(step)
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [isCredits])

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
        letterSpacing: '4px',
        fontFamily: 'Archeoscope, serif'
      }}>
        INFORMACIÓN
      </h1>
      
      {/* Contenedor de contenido con scroll */}
      <div
        ref={scrollRef}
        style={{
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
            letterSpacing: '2px',
            fontFamily: 'Archeoscope, serif'
          }}>
            📜 Inspiración
          </h2>
          
          <p style={{
            fontSize: '19px',
            lineHeight: '1.8',
            marginBottom: '20px',
            opacity: 0.9
          }}>
            <strong>Archeoscope</strong> toma inspiración de diversas culturas antiguas, teorías arqueológicas y estudios sobre la conciencia.
          </p>
          
          <p style={{
            fontSize: '19px',
            lineHeight: '1.8',
            marginBottom: '20px',
            opacity: 0.9
          }}>
            El concepto de <strong>armonía cósmica</strong> está influenciado por el trabajo del astrónomo <strong>Johannes Kepler</strong> y su obra <em>Harmonices Mundi</em> (1619), donde propuso que los movimientos planetarios siguen proporciones matemáticas armónicas — la música de las esferas. Sus leyes del movimiento planetario son la base de nuestro sistema orbital.
          </p>
          
          <p style={{
            fontSize: '19px',
            lineHeight: '1.8',
            marginBottom: '20px',
            opacity: 0.9
          }}>
            Parte de su narrativa y concepto de <strong>red energética planetaria</strong> está influenciado por las ideas del investigador mexicano <strong>Jacobo Grinberg-Zylberbaum</strong>, especialmente su obra <em>La teoría sintérgica</em>.
          </p>
          
          <p style={{
            fontSize: '19px',
            lineHeight: '1.8',
            opacity: 0.9
          }}>
            Estas referencias han sido reinterpretadas libremente con fines artísticos y narrativos.
          </p>
        </section>
        
        {/* Sección de Requerimientos Mínimos */}
        <section style={{
          marginBottom: '40px',
          padding: '30px',
          background: 'rgba(239, 68, 68, 0.1)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          borderRadius: '12px'
        }}>
          <h2 style={{
            fontSize: '32px',
            marginBottom: '20px',
            color: '#ef4444',
            letterSpacing: '2px',
            fontFamily: 'Archeoscope, serif'
          }}>
            💻 Requerimientos Mínimos
          </h2>
          
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '15px',
            fontSize: '19px',
            lineHeight: '1.8'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '12px'
            }}>
              <span style={{ color: '#ef4444', fontSize: '20px', minWidth: '30px' }}>🖥️</span>
              <div>
                <strong style={{ color: '#ffffff' }}>Procesador:</strong>
                <span style={{ opacity: 0.9 }}> Intel Core i5 8va Gen o AMD Ryzen 5 2600 (o equivalentes)</span>
              </div>
            </div>
            
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '12px'
            }}>
              <span style={{ color: '#ef4444', fontSize: '20px', minWidth: '30px' }}>🧠</span>
              <div>
                <strong style={{ color: '#ffffff' }}>Memoria RAM:</strong>
                <span style={{ opacity: 0.9 }}> 12 GB mínimo (16 GB recomendado)</span>
              </div>
            </div>
            
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '12px'
            }}>
              <span style={{ color: '#ef4444', fontSize: '20px', minWidth: '30px' }}>🎮</span>
              <div>
                <strong style={{ color: '#ffffff' }}>Tarjeta Gráfica:</strong>
                <span style={{ opacity: 0.9 }}> NVIDIA GTX 1050 / AMD RX 560 o superior con soporte WebGL 2.0</span>
              </div>
            </div>
            
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '12px'
            }}>
              <span style={{ color: '#ef4444', fontSize: '20px', minWidth: '30px' }}>🌐</span>
              <div>
                <strong style={{ color: '#ffffff' }}>Navegador:</strong>
                <span style={{ opacity: 0.9 }}> Chrome 90+, Firefox 88+, Edge 90+ (con WebGL 2.0 habilitado)</span>
              </div>
            </div>
            
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '12px'
            }}>
              <span style={{ color: '#ef4444', fontSize: '20px', minWidth: '30px' }}>📡</span>
              <div>
                <strong style={{ color: '#ffffff' }}>Conexión:</strong>
                <span style={{ opacity: 0.9 }}> Recomendada para carga inicial de assets 3D</span>
              </div>
            </div>
            
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '12px'
            }}>
              <span style={{ color: '#ef4444', fontSize: '20px', minWidth: '30px' }}>🖼️</span>
              <div>
                <strong style={{ color: '#ffffff' }}>Resolución:</strong>
                <span style={{ opacity: 0.9 }}> 1920x1080 o superior para mejor experiencia visual</span>
              </div>
            </div>
          </div>
          
          <div style={{
            marginTop: '20px',
            padding: '15px',
            background: 'rgba(0, 0, 0, 0.3)',
            borderRadius: '8px',
            fontSize: '17px',
            opacity: 0.8,
            lineHeight: '1.6'
          }}>
            <strong style={{ color: '#fbbf24' }}>⚠️ Nota:</strong> El juego utiliza tecnologías web avanzadas (WebGL 2.0, Web Audio API, WebWorkers). 
            Para una experiencia óptima, asegúrate de tener los drivers de tu tarjeta gráfica actualizados y la aceleración por hardware habilitada en tu navegador.
          </div>
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
            fontSize: '17px',
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

        {/* Sistemas Técnicos */}
        {[
          {
            icon: '🎨',
            title: 'Sistema de Arte Generativo Orbital',
            color: '#a78bfa',
            border: 'rgba(167, 139, 250, 0.3)',
            bg: 'rgba(167, 139, 250, 0.08)',
            text: 'Motor de visualización matemática que transforma datos astronómicos en arte procedural en tiempo real. Detecta resonancias orbitales armónicas entre planetas (ratios 1/2, 2/3, 3/5, etc.) y genera mandalas gravitacionales mediante curvas de Lissajous. Crea patrones geométricos tipo spirograph basados en períodos orbitales reales y redes orbitales que conectan cuerpos celestes cercanos. El sistema combina geometría sagrada, matemáticas keplerianas y teoría musical de las esferas — cada configuración planetaria produce patrones únicos e irrepetibles que evolucionan con el movimiento orbital.'
          },
          {
            icon: '🎵',
            title: 'Sistema de Sonido — Harmonia Mundi',
            color: '#10b981',
            border: 'rgba(16, 185, 129, 0.3)',
            bg: 'rgba(16, 185, 129, 0.08)',
            text: 'Motor de audio procedural basado en frecuencias cósmicas reales. Cada misión completada desbloquea una nueva capa sonora construida sobre la frecuencia orbital de la Tierra (136.10 Hz). Los sitios arqueológicos actúan como amplificadores: filtros de resonancia únicos que modifican el espectro sonoro en tiempo real. Al completar Göbekli Tepe, el sistema activa el sonido del escarabajo sagrado — tres capas de síntesis (wingbeat, modulación LFO, armónicos aerodinámicos) que evocan a Khepri, el dios del renacimiento solar.'
          },
          {
            icon: '⭐',
            title: 'Sistema de Cálculo Estelar',
            color: '#fbbf24',
            border: 'rgba(251, 191, 36, 0.3)',
            bg: 'rgba(251, 191, 36, 0.08)',
            text: 'Motor astronómico de alta precisión que calcula la posición real del Sol para cualquier coordenada geográfica y fecha. Implementa las ecuaciones de declinación solar, ángulo horario y altitud/azimut con correcciones de refracción atmosférica. Simula los equinoccios, solsticios y la precesión axial de la Tierra a lo largo de ciclos de 26,000 años — el mismo ciclo que las civilizaciones antiguas codificaron en sus monumentos.'
          },
          {
            icon: '🪐',
            title: 'Sistema Orbital y de Planetas',
            color: '#34d399',
            border: 'rgba(52, 211, 153, 0.3)',
            bg: 'rgba(52, 211, 153, 0.08)',
            text: 'Simulación del sistema solar con órbitas keplerianas calculadas en tiempo real. Cada planeta se posiciona según su período orbital real (Mercurio 88 días, Venus 225, Marte 687, etc.). El sistema incluye fases lunares, eclipses y la posición de la Vía Láctea. La iluminación de cada escena responde dinámicamente a la posición solar calculada, recreando las condiciones lumínicas exactas de cada sitio arqueológico.'
          },
          {
            icon: '🎮',
            title: 'Sistema 3D y Gráficos',
            color: '#60a5fa',
            border: 'rgba(96, 165, 250, 0.3)',
            bg: 'rgba(96, 165, 250, 0.08)',
            text: 'Motor de renderizado basado en Three.js / React Three Fiber con optimizaciones avanzadas: instanced meshes para vegetación y NPCs, carga diferida de modelos por escena, compresión de geometría, LOD dinámico para terrenos y frustum culling. Los modelos 3D de sitios arqueológicos son reconstrucciones procedurales o digitalizaciones de alta fidelidad. El sistema climático genera lluvia, nieve, tormentas y erupciones volcánicas en tiempo real mediante sistemas de partículas.'
          },
          {
            icon: '🔷',
            title: 'Sistema de Geometría Sagrada',
            color: '#f472b6',
            border: 'rgba(244, 114, 182, 0.3)',
            bg: 'rgba(244, 114, 182, 0.08)',
            text: 'Generador procedural de patrones geométricos basados en matemáticas antiguas. Cada sitio arqueológico tiene asignado un patrón único: Lissajous (Giza), Cubo de Metatrón (Puma Punku), Espiral galáctica (Teotihuacán), Polígono estelar (Veracruz), Curva de Hilbert (Isla de Pascua). Al completar una misión, el patrón se graba en el terreno como crop circle. El sistema Sacred Geometry Engine genera además patrones únicos basados en la nave utilizada y las coordenadas del sitio — cada combinación produce una firma energética irrepetible.'
          }
        ].map((s) => (
          <section key={s.title} style={{
            marginBottom: '20px',
            padding: '25px',
            background: s.bg,
            border: `1px solid ${s.border}`,
            borderRadius: '12px'
          }}>
            <h2 style={{
              fontSize: '24px',
              marginBottom: '14px',
              color: s.color,
              letterSpacing: '1px',
              fontFamily: 'Archeoscope, serif'
            }}>
              {s.icon} {s.title}
            </h2>
            <p style={{
              fontSize: '18px',
              lineHeight: '1.8',
              opacity: 0.88
            }}>
              {s.text}
            </p>
          </section>
        ))}
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

export default function InfoPage() {
  return (
    <Suspense fallback={null}>
      <InfoContent />
    </Suspense>
  )
}