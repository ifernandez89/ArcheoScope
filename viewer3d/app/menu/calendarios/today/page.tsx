'use client'

import { useRouter } from 'next/navigation'
import { useMemo } from 'react'
import * as Astronomy from 'astronomy-engine'
import { getUpcomingEclipses, isDresdenEclipseWindow, DRESDEN_CODEX_INFO } from '@/utils/eclipse-calculator'

// ─── Datos del Tzolk'in (Cholq'ij) ──────────────────────────────────────────
const NAWALES = ['Imox','Iq\'','Aq\'ab\'al','K\'at','Kan','Keme','Kej','Q\'anil','Toj','Tz\'i\'','B\'atz\'','E','Aj','I\'x','Tz\'ikin','Ajmaq','No\'j','Tijax','Kawoq','Ajpu']
const NUMEROS_KICHE = ['Jun','Ki\'eb\'','Oxib\'','Kajib\'','Jo\'ob\'','Waqib\'','Wuqub\'','Wajxaqib\'','B\'elejeb\'','Lajuj','Junlajuj','Kab\'lajuj','Oxlajuj']
const REF_DATE = new Date(2000, 0, 1)
const REF_NAWAL = 10
const REF_NUM = 10

function calcCholqij(date: Date) {
  const diff = Math.floor((date.getTime() - REF_DATE.getTime()) / 86400000)
  const nawalIdx = ((REF_NAWAL + diff) % 20 + 20) % 20
  const numIdx = ((REF_NUM + diff) % 13 + 13) % 13
  return { nawal: NAWALES[nawalIdx], num: numIdx + 1, numName: NUMEROS_KICHE[numIdx] }
}

// ─── Eventos astronómicos (lluvias de meteoros + solsticios/equinoccios) ──────
const METEOR_SHOWERS = [
  { doy: 3, name: 'Cuadrántidas', emoji: '🌠' },
  { doy: 112, name: 'Líridas', emoji: '🌠' },
  { doy: 126, name: 'Eta Acuáridas', emoji: '🌠' },
  { doy: 209, name: 'Delta Acuáridas', emoji: '🌠' },
  { doy: 224, name: 'Perseidas', emoji: '🌠' },
  { doy: 294, name: 'Oriónidas', emoji: '🌠' },
  { doy: 321, name: 'Leónidas', emoji: '🌠' },
  { doy: 348, name: 'Gemínidas', emoji: '🌠' },
]

const SOLAR_EVENTS = [
  { doy: 79, name: 'Equinoccio de Marzo', emoji: '☀️' },
  { doy: 172, name: 'Solsticio de Junio', emoji: '☀️' },
  { doy: 265, name: 'Equinoccio de Septiembre', emoji: '☀️' },
  { doy: 355, name: 'Solsticio de Diciembre', emoji: '☀️' },
]

function getUpcomingEvents(date: Date, count: number = 4) {
  const doy = Math.floor((date.getTime() - new Date(date.getFullYear(), 0, 0).getTime()) / 86400000)
  const allEvents = [...METEOR_SHOWERS, ...SOLAR_EVENTS]
    .map(e => {
      let days = e.doy - doy
      if (days < 0) days += 365
      return { ...e, days }
    })
    .sort((a, b) => a.days - b.days)
    .slice(0, count)
  return allEvents
}

// ─── Estación solar ──────────────────────────────────────────────────────────
function getSeason(date: Date): { name: string; emoji: string; progress: number; nextEvent: string; daysToNext: number } {
  const doy = Math.floor((date.getTime() - new Date(date.getFullYear(), 0, 0).getTime()) / 86400000)
  const lat = -31.7 // Hemisferio sur (Argentina)
  let name: string, emoji: string
  // Hemisferio sur: estaciones invertidas
  if (doy >= 355 || doy < 80) { name = 'Verano'; emoji = '☀️' }
  else if (doy < 172) { name = 'Otoño'; emoji = '🍂' }
  else if (doy < 266) { name = 'Invierno'; emoji = '❄️' }
  else { name = 'Primavera'; emoji = '🌸' }

  // Próximo evento solar
  const events = [
    { doy: 80, label: 'Equinoccio Mar' }, { doy: 172, label: 'Solsticio Jun' },
    { doy: 266, label: 'Equinoccio Sep' }, { doy: 355, label: 'Solsticio Dic' },
  ]
  let nextEvent = events[0].label, daysToNext = 365
  for (const ev of events) {
    const d = ev.doy - doy
    if (d > 0 && d < daysToNext) { daysToNext = d; nextEvent = ev.label }
  }
  if (daysToNext === 365) { daysToNext = events[0].doy + (365 - doy); nextEvent = events[0].label }

  // Progreso dentro de la estación (0-100)
  const seasonStarts = [355, 80, 172, 266]
  let progress = 50
  for (let i = 0; i < seasonStarts.length; i++) {
    const start = seasonStarts[i]
    const end = seasonStarts[(i + 1) % 4]
    const len = end > start ? end - start : 365 - start + end
    const elapsed = doy >= start ? doy - start : doy + 365 - start
    if (elapsed < len) { progress = Math.round((elapsed / len) * 100); break }
  }

  return { name, emoji, progress, nextEvent, daysToNext }
}

export default function TodayPage() {
  const router = useRouter()
  const today = new Date()

  const data = useMemo(() => {
    const t = Astronomy.MakeTime(today)
    const moonLon = Astronomy.EclipticLongitude(Astronomy.Body.Moon, t)
    const sunLon = Astronomy.SunPosition(t).elon
    const phaseAngle = Astronomy.MoonPhase(t)
    const signs = ['Aries','Tauro','Géminis','Cáncer','Leo','Virgo','Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis']
    const glyphs = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓']
    const moonSignIdx = Math.floor(moonLon / 30) % 12
    const sunSignIdx = Math.floor(sunLon / 30) % 12
    const illumination = Math.round((1 - Math.cos(phaseAngle * Math.PI / 180)) / 2 * 100)
    let phaseName: string, phaseEmoji: string
    if (phaseAngle < 11.25)       { phaseName = 'Luna Nueva';        phaseEmoji = '🌑' }
    else if (phaseAngle < 78.75)  { phaseName = 'Creciente';         phaseEmoji = '🌒' }
    else if (phaseAngle < 101.25) { phaseName = 'Cuarto Creciente';  phaseEmoji = '🌓' }
    else if (phaseAngle < 168.75) { phaseName = 'Gibosa Creciente';  phaseEmoji = '🌔' }
    else if (phaseAngle < 191.25) { phaseName = 'Luna Llena';        phaseEmoji = '🌕' }
    else if (phaseAngle < 258.75) { phaseName = 'Gibosa Menguante';  phaseEmoji = '🌖' }
    else if (phaseAngle < 281.25) { phaseName = 'Cuarto Menguante';  phaseEmoji = '🌗' }
    else if (phaseAngle < 348.75) { phaseName = 'Menguante';         phaseEmoji = '🌘' }
    else                          { phaseName = 'Luna Nueva';        phaseEmoji = '🌑' }

    const cholqij = calcCholqij(today)
    const season = getSeason(today)
    const events = getUpcomingEvents(today)
    const eclipses = getUpcomingEclipses(today, 3)
    const dresdenWindow = isDresdenEclipseWindow(today)

    return {
      date: today.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }),
      moonPhase: phaseName, moonEmoji: phaseEmoji, moonSign: signs[moonSignIdx], moonGlyph: glyphs[moonSignIdx],
      moonDeg: (moonLon % 30).toFixed(1), illumination,
      sunSign: signs[sunSignIdx], sunGlyph: glyphs[sunSignIdx], sunDeg: (sunLon % 30).toFixed(1),
      cholqij, season, events, eclipses, dresdenWindow,
    }
  }, [])

  const cardStyle = (color: string) => ({
    padding: 'clamp(14px, 3vw, 20px)',
    background: `${color}08`,
    border: `1px solid ${color}25`,
    borderRadius: '14px',
  })

  return (
    <main style={{
      width: '100vw', minHeight: '100vh',
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      background: 'linear-gradient(180deg, #06060f, #0d0820, #06060f)',
      padding: 'clamp(24px, 5vw, 40px) 16px', color: '#fff', overflowY: 'auto',
    }}>
      <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.35)', letterSpacing: '2px', marginBottom: '10px', cursor: 'pointer' }}
        onClick={() => router.push('/menu/calendarios')}>← CALENDARIOS</div>

      <h1 style={{ fontSize: 'clamp(22px, 5vw, 36px)', color: '#22c55e', letterSpacing: '4px', marginBottom: '6px', fontFamily: 'Archeoscope, serif' }}>HOY</h1>
      <p style={{ fontSize: 'clamp(12px, 2.5vw, 16px)', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '24px', textAlign: 'center', textTransform: 'capitalize' }}>
        {data.date}
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', width: '100%', maxWidth: '500px' }}>

        {/* Fase Lunar */}
        <div style={cardStyle('rgba(253,230,138)')}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <span style={{ fontSize: 'clamp(36px, 8vw, 48px)' }}>{data.moonEmoji}</span>
            <div>
              <div style={{ fontSize: 'clamp(10px, 2vw, 13px)', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px' }}>FASE LUNAR</div>
              <div style={{ fontSize: 'clamp(16px, 3.5vw, 22px)', fontWeight: 'bold', color: '#fde68a' }}>{data.moonPhase}</div>
              <div style={{ fontSize: 'clamp(13px, 2.5vw, 17px)', color: 'rgba(255,255,255,0.5)' }}>
                {data.moonDeg}° {data.moonSign} {data.moonGlyph} · {data.illumination}%
              </div>
            </div>
          </div>
        </div>

        {/* Sol */}
        <div style={cardStyle('rgba(251,191,36)')}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <span style={{ fontSize: 'clamp(36px, 8vw, 48px)' }}>☀️</span>
            <div>
              <div style={{ fontSize: 'clamp(10px, 2vw, 13px)', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px' }}>SOL</div>
              <div style={{ fontSize: 'clamp(16px, 3.5vw, 22px)', fontWeight: 'bold', color: '#fbbf24' }}>
                {data.sunDeg}° {data.sunSign} {data.sunGlyph}
              </div>
            </div>
          </div>
        </div>

        {/* Cholq'ij / Tzolk'in */}
        <div style={cardStyle('rgba(167,139,250)')}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <span style={{ fontSize: 'clamp(36px, 8vw, 48px)' }}>🌀</span>
            <div>
              <div style={{ fontSize: 'clamp(10px, 2vw, 13px)', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px' }}>CHOLQ'IJ (TZOLK'IN)</div>
              <div style={{ fontSize: 'clamp(16px, 3.5vw, 22px)', fontWeight: 'bold', color: '#a78bfa' }}>
                {data.cholqij.num} {data.cholqij.nawal}
              </div>
              <div style={{ fontSize: 'clamp(12px, 2.5vw, 16px)', color: 'rgba(255,255,255,0.4)' }}>
                {data.cholqij.numName}
              </div>
            </div>
          </div>
        </div>

        {/* Estación Solar */}
        <div style={cardStyle('rgba(34,197,94)')}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '10px' }}>
            <span style={{ fontSize: 'clamp(36px, 8vw, 48px)' }}>{data.season.emoji}</span>
            <div>
              <div style={{ fontSize: 'clamp(10px, 2vw, 13px)', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px' }}>ESTACIÓN SOLAR</div>
              <div style={{ fontSize: 'clamp(16px, 3.5vw, 22px)', fontWeight: 'bold', color: '#22c55e' }}>{data.season.name}</div>
              <div style={{ fontSize: 'clamp(12px, 2.5vw, 16px)', color: 'rgba(255,255,255,0.4)' }}>
                Próximo: {data.season.nextEvent} en {data.season.daysToNext}d
              </div>
            </div>
          </div>
          <div style={{ height: '4px', background: 'rgba(255,255,255,0.08)', borderRadius: '2px', overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${data.season.progress}%`, background: '#22c55e', borderRadius: '2px' }} />
          </div>
        </div>

        {/* Eventos Astronómicos */}
        {data.events.length > 0 && (
          <div style={cardStyle('rgba(56,189,248)')}>
            <div style={{ fontSize: 'clamp(10px, 2vw, 13px)', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '10px' }}>
              🌠 PRÓXIMOS EVENTOS ASTRONÓMICOS
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {data.events.map((ev, i) => (
                <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '18px' }}>{ev.emoji}</span>
                    <span style={{ fontSize: 'clamp(13px, 2.5vw, 17px)', color: 'rgba(255,255,255,0.7)' }}>{ev.name}</span>
                  </div>
                  <span style={{ fontSize: 'clamp(12px, 2vw, 15px)', color: ev.days === 0 ? '#22c55e' : 'rgba(255,255,255,0.35)' }}>
                    {ev.days === 0 ? '¡HOY!' : `en ${ev.days}d`}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Eclipses — dinámicos con astronomy-engine */}
        {data.eclipses.length > 0 && (
          <div style={cardStyle('rgba(239,68,68)')}>
            <div style={{ fontSize: 'clamp(10px, 2vw, 13px)', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '10px' }}>
              🌑 PRÓXIMOS ECLIPSES (astronomy-engine)
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {data.eclipses.map((e, i) => (
                <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '18px' }}>{e.emoji}</span>
                    <div>
                      <span style={{ fontSize: 'clamp(13px, 2.5vw, 16px)', color: 'rgba(255,255,255,0.7)' }}>
                        Eclipse {e.type === 'solar' ? 'Solar' : 'Lunar'} {e.kind}
                      </span>
                      <div style={{ fontSize: 'clamp(11px, 2vw, 13px)', color: 'rgba(255,255,255,0.35)' }}>{e.dateStr}</div>
                    </div>
                  </div>
                  <span style={{ fontSize: 'clamp(12px, 2vw, 15px)', color: e.daysFromNow <= 7 ? '#ef4444' : 'rgba(255,255,255,0.35)' }}>
                    {e.daysFromNow === 0 ? '¡HOY!' : `en ${e.daysFromNow}d`}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Códice de Dresde — ventana de eclipse maya */}
        <div style={cardStyle('rgba(251,191,36)')}>
          <div style={{ fontSize: 'clamp(10px, 2vw, 13px)', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '10px' }}>
            📜 CÓDICE DE DRESDE — CICLOS DE ECLIPSE MAYA
          </div>
          <div style={{ fontSize: 'clamp(12px, 2.5vw, 15px)', color: 'rgba(255,255,255,0.55)', lineHeight: '1.6', marginBottom: '10px' }}>
            {DRESDEN_CODEX_INFO.description}
          </div>
          <div style={{
            padding: '10px',
            background: data.dresdenWindow.inWindow ? 'rgba(239,68,68,0.1)' : 'rgba(34,197,94,0.05)',
            border: `1px solid ${data.dresdenWindow.inWindow ? 'rgba(239,68,68,0.3)' : 'rgba(34,197,94,0.15)'}`,
            borderRadius: '8px',
          }}>
            <div style={{ fontSize: 'clamp(12px, 2.5vw, 15px)', fontWeight: 'bold', color: data.dresdenWindow.inWindow ? '#ef4444' : '#22c55e' }}>
              {data.dresdenWindow.inWindow
                ? '⚠️ Ventana de eclipse activa (tradición maya)'
                : `✓ Fuera de ventana — próxima en ${data.dresdenWindow.daysToWindow}d`
              }
            </div>
            <div style={{ fontSize: 'clamp(11px, 2vw, 13px)', color: 'rgba(255,255,255,0.35)', marginTop: '4px' }}>
              Ciclo: {data.dresdenWindow.cycleType}
            </div>
          </div>
        </div>

        {/* Gregoriano */}
        <div style={{ fontSize: 'clamp(11px, 2vw, 14px)', color: 'rgba(255,255,255,0.2)', textAlign: 'center', marginTop: '8px', letterSpacing: '1px' }}>
          Día {Math.floor((today.getTime() - new Date(today.getFullYear(), 0, 0).getTime()) / 86400000)} del año · Semana {Math.ceil(((today.getTime() - new Date(today.getFullYear(), 0, 1).getTime()) / 86400000) / 7)}
        </div>
      </div>

      <button onClick={() => router.push('/menu/calendarios')} className="btn-responsive" style={{ marginTop: '28px' }}
        onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#fff' }}
        onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)' }}>
        Volver
      </button>
    </main>
  )
}
