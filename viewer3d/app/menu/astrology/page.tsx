'use client'

import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

// ─── SIGNOS ZODIACALES ───────────────────────────────────────────────────────
const ZODIAC = [
  { name: 'Aries',       glyph: '♈', dates: 'Mar 21 – Abr 19', element: 'Fuego',  color: '#ef4444', ruler: 'Marte',    quality: 'Cardinal',  trait: 'Iniciativa, Coraje, Impulso' },
  { name: 'Tauro',       glyph: '♉', dates: 'Abr 20 – May 20', element: 'Tierra', color: '#22c55e', ruler: 'Venus',    quality: 'Fijo',      trait: 'Estabilidad, Sensualidad, Persistencia' },
  { name: 'Géminis',     glyph: '♊', dates: 'May 21 – Jun 20', element: 'Aire',   color: '#fbbf24', ruler: 'Mercurio', quality: 'Mutable',   trait: 'Comunicación, Versatilidad, Curiosidad' },
  { name: 'Cáncer',      glyph: '♋', dates: 'Jun 21 – Jul 22', element: 'Agua',   color: '#60a5fa', ruler: 'Luna',     quality: 'Cardinal',  trait: 'Protección, Emoción, Intuición' },
  { name: 'Leo',         glyph: '♌', dates: 'Jul 23 – Ago 22', element: 'Fuego',  color: '#f97316', ruler: 'Sol',      quality: 'Fijo',      trait: 'Creatividad, Liderazgo, Generosidad' },
  { name: 'Virgo',       glyph: '♍', dates: 'Ago 23 – Sep 22', element: 'Tierra', color: '#a3e635', ruler: 'Mercurio', quality: 'Mutable',   trait: 'Análisis, Servicio, Perfección' },
  { name: 'Libra',       glyph: '♎', dates: 'Sep 23 – Oct 22', element: 'Aire',   color: '#f472b6', ruler: 'Venus',    quality: 'Cardinal',  trait: 'Equilibrio, Armonía, Justicia' },
  { name: 'Escorpio',    glyph: '♏', dates: 'Oct 23 – Nov 21', element: 'Agua',   color: '#dc2626', ruler: 'Plutón',   quality: 'Fijo',      trait: 'Transformación, Intensidad, Poder' },
  { name: 'Sagitario',   glyph: '♐', dates: 'Nov 22 – Dic 21', element: 'Fuego',  color: '#a78bfa', ruler: 'Júpiter',  quality: 'Mutable',   trait: 'Expansión, Filosofía, Aventura' },
  { name: 'Capricornio', glyph: '♑', dates: 'Dic 22 – Ene 19', element: 'Tierra', color: '#6b7280', ruler: 'Saturno',  quality: 'Cardinal',  trait: 'Ambición, Disciplina, Estructura' },
  { name: 'Acuario',     glyph: '♒', dates: 'Ene 20 – Feb 18', element: 'Aire',   color: '#38bdf8', ruler: 'Urano',    quality: 'Fijo',      trait: 'Innovación, Libertad, Humanidad' },
  { name: 'Piscis',      glyph: '♓', dates: 'Feb 19 – Mar 20', element: 'Agua',   color: '#818cf8', ruler: 'Neptuno',  quality: 'Mutable',   trait: 'Compasión, Imaginación, Trascendencia' },
]

// ─── PLANETAS ────────────────────────────────────────────────────────────────
const PLANETS = [
  { name: 'Sol',      glyph: '☉', color: '#fbbf24', meaning: 'Identidad, Voluntad, Vitalidad' },
  { name: 'Luna',     glyph: '☽', color: '#e2e8f0', meaning: 'Emociones, Instinto, Subconsciente' },
  { name: 'Mercurio', glyph: '☿', color: '#a3e635', meaning: 'Comunicación, Intelecto, Movimiento' },
  { name: 'Venus',    glyph: '♀', color: '#f472b6', meaning: 'Amor, Belleza, Valores' },
  { name: 'Marte',    glyph: '♂', color: '#ef4444', meaning: 'Acción, Deseo, Energía' },
  { name: 'Júpiter',  glyph: '♃', color: '#a78bfa', meaning: 'Expansión, Sabiduría, Abundancia' },
  { name: 'Saturno',  glyph: '♄', color: '#6b7280', meaning: 'Estructura, Disciplina, Tiempo' },
]

/**
 * Calcular signo solar basado en fecha
 */
function getSolarSign(date: Date) {
  const m = date.getMonth() + 1
  const d = date.getDate()
  if ((m === 3 && d >= 21) || (m === 4 && d <= 19)) return 0
  if ((m === 4 && d >= 20) || (m === 5 && d <= 20)) return 1
  if ((m === 5 && d >= 21) || (m === 6 && d <= 20)) return 2
  if ((m === 6 && d >= 21) || (m === 7 && d <= 22)) return 3
  if ((m === 7 && d >= 23) || (m === 8 && d <= 22)) return 4
  if ((m === 8 && d >= 23) || (m === 9 && d <= 22)) return 5
  if ((m === 9 && d >= 23) || (m === 10 && d <= 22)) return 6
  if ((m === 10 && d >= 23) || (m === 11 && d <= 21)) return 7
  if ((m === 11 && d >= 22) || (m === 12 && d <= 21)) return 8
  if ((m === 12 && d >= 22) || (m === 1 && d <= 19)) return 9
  if ((m === 1 && d >= 20) || (m === 2 && d <= 18)) return 10
  return 11
}

/**
 * Calcular signo lunar aproximado (ciclo de 29.5 días)
 */
function getLunarSign(date: Date) {
  const ref = new Date(2000, 0, 6) // Luna nueva conocida
  const diffDays = (date.getTime() - ref.getTime()) / 86400000
  const lunarCycle = 29.53059
  const dayInCycle = ((diffDays % lunarCycle) + lunarCycle) % lunarCycle
  const signIdx = Math.floor((dayInCycle / lunarCycle) * 12) % 12
  const phase = dayInCycle / lunarCycle
  let phaseName = 'Nueva'
  if (phase > 0.03 && phase <= 0.25) phaseName = 'Creciente'
  else if (phase > 0.25 && phase <= 0.53) phaseName = 'Llena'
  else if (phase > 0.53 && phase <= 0.75) phaseName = 'Menguante'
  else if (phase > 0.75) phaseName = 'Balsámica'
  return { signIdx, phaseName }
}

export default function AstrologyPage() {
  const router = useRouter()
  const [selectedDate, setSelectedDate] = useState(new Date())

  const solarIdx = useMemo(() => getSolarSign(selectedDate), [selectedDate])
  const lunar = useMemo(() => getLunarSign(selectedDate), [selectedDate])
  const solarSign = ZODIAC[solarIdx]
  const lunarSign = ZODIAC[lunar.signIdx]

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'flex-start',
      background: 'linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 50%, #0a0a1a 100%)',
      margin: 0, padding: '40px 20px', overflow: 'auto', color: '#fff',
    }}>
      <h1 style={{ fontSize: '48px', marginBottom: '8px', letterSpacing: '6px', fontFamily: 'Archeoscope, serif', color: '#a78bfa' }}>
        ASTROLOGÍA
      </h1>
      <p style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', marginBottom: '30px', letterSpacing: '2px' }}>
        Tránsito Planetario y Carta del Momento
      </p>

      {/* Selector de fecha */}
      <input
        type="date"
        value={selectedDate.toISOString().split('T')[0]}
        onChange={(e) => setSelectedDate(new Date(e.target.value + 'T12:00:00'))}
        style={{
          padding: '10px 20px', fontSize: '16px', background: 'rgba(255,255,255,0.05)',
          border: '1px solid rgba(167,139,250,0.3)', borderRadius: '8px', color: '#a78bfa',
          marginBottom: '30px', cursor: 'pointer',
        }}
      />

      {/* Signo Solar */}
      <div style={{
        maxWidth: '500px', width: '100%', padding: '28px',
        background: `rgba(${solarSign.color === '#ef4444' ? '239,68,68' : solarSign.color === '#22c55e' ? '34,197,94' : '251,191,36'},0.06)`,
        border: `1px solid ${solarSign.color}40`,
        borderRadius: '16px', textAlign: 'center', marginBottom: '20px',
      }}>
        <div style={{ fontSize: '56px', marginBottom: '4px' }}>{solarSign.glyph}</div>
        <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '4px' }}>SOL EN</div>
        <div style={{ fontSize: '36px', fontWeight: 'bold', color: solarSign.color, fontFamily: 'Archeoscope, serif' }}>
          {solarSign.name}
        </div>
        <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)', marginTop: '4px' }}>{solarSign.dates}</div>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.7)', marginTop: '10px' }}>{solarSign.trait}</div>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginTop: '12px', fontSize: '12px', color: 'rgba(255,255,255,0.4)' }}>
          <span>Elemento: <strong style={{ color: solarSign.color }}>{solarSign.element}</strong></span>
          <span>Regente: <strong style={{ color: solarSign.color }}>{solarSign.ruler}</strong></span>
          <span>Cualidad: <strong style={{ color: solarSign.color }}>{solarSign.quality}</strong></span>
        </div>
      </div>

      {/* Luna */}
      <div style={{
        maxWidth: '500px', width: '100%', padding: '24px',
        background: 'rgba(226,232,240,0.04)', border: '1px solid rgba(226,232,240,0.2)',
        borderRadius: '12px', textAlign: 'center', marginBottom: '20px',
      }}>
        <div style={{ fontSize: '40px', marginBottom: '4px' }}>☽</div>
        <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '4px' }}>LUNA EN</div>
        <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#e2e8f0', fontFamily: 'Archeoscope, serif' }}>
          {lunarSign.name}
        </div>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.5)', marginTop: '6px' }}>
          Fase: <strong style={{ color: '#e2e8f0' }}>{lunar.phaseName}</strong>
        </div>
        <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)', marginTop: '4px' }}>{lunarSign.trait}</div>
      </div>

      {/* Rueda zodiacal */}
      <div style={{
        maxWidth: '500px', width: '100%', padding: '20px',
        background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '12px', marginBottom: '20px',
      }}>
        <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '14px', textAlign: 'center' }}>
          ZODIACO
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '8px' }}>
          {ZODIAC.map((z, i) => (
            <div key={z.name} style={{
              padding: '6px 12px', borderRadius: '6px', fontSize: '14px',
              background: i === solarIdx ? `${z.color}25` : 'rgba(255,255,255,0.03)',
              border: `1px solid ${i === solarIdx ? z.color : 'rgba(255,255,255,0.08)'}`,
              color: i === solarIdx ? z.color : 'rgba(255,255,255,0.4)',
              fontWeight: i === solarIdx ? 'bold' : 'normal',
              transition: 'all 0.2s',
            }}>
              {z.glyph} {z.name}
            </div>
          ))}
        </div>
      </div>

      {/* Planetas */}
      <div style={{
        maxWidth: '500px', width: '100%', padding: '20px',
        background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '12px', marginBottom: '30px',
      }}>
        <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '14px', textAlign: 'center' }}>
          CUERPOS CELESTES
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
          {PLANETS.map((p) => (
            <div key={p.name} style={{
              padding: '10px 14px', borderRadius: '8px',
              background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)',
            }}>
              <div style={{ fontSize: '20px', marginBottom: '2px' }}>{p.glyph} <span style={{ color: p.color, fontSize: '14px', fontWeight: 'bold' }}>{p.name}</span></div>
              <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.4)' }}>{p.meaning}</div>
            </div>
          ))}
        </div>
      </div>

      <button
        onClick={() => router.push('/menu')}
        style={{
          padding: '16px 60px', fontSize: '20px', fontWeight: 'bold', color: '#fff',
          background: 'transparent', border: '2px solid #fff', borderRadius: '8px',
          cursor: 'pointer', letterSpacing: '2px', textTransform: 'uppercase', transition: 'all 0.3s',
        }}
        onMouseEnter={(e) => { e.currentTarget.style.background = '#fff'; e.currentTarget.style.color = '#000' }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#fff' }}
      >
        Volver
      </button>
    </main>
  )
}
