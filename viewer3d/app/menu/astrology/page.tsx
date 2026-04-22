'use client'

import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

// ─── CONSTANTES ASTRONÓMICAS ────────────────────────────────────────────────
const ZODIAC = [
  { name: 'Aries',       glyph: '♈', color: '#ef4444', element: 'Fuego',  ruler: 'Marte' },
  { name: 'Tauro',       glyph: '♉', color: '#22c55e', element: 'Tierra', ruler: 'Venus' },
  { name: 'Géminis',     glyph: '♊', color: '#fbbf24', element: 'Aire',   ruler: 'Mercurio' },
  { name: 'Cáncer',      glyph: '♋', color: '#60a5fa', element: 'Agua',   ruler: 'Luna' },
  { name: 'Leo',         glyph: '♌', color: '#f97316', element: 'Fuego',  ruler: 'Sol' },
  { name: 'Virgo',       glyph: '♍', color: '#a3e635', element: 'Tierra', ruler: 'Mercurio' },
  { name: 'Libra',       glyph: '♎', color: '#f472b6', element: 'Aire',   ruler: 'Venus' },
  { name: 'Escorpio',    glyph: '♏', color: '#dc2626', element: 'Agua',   ruler: 'Plutón' },
  { name: 'Sagitario',   glyph: '♐', color: '#a78bfa', element: 'Fuego',  ruler: 'Júpiter' },
  { name: 'Capricornio', glyph: '♑', color: '#6b7280', element: 'Tierra', ruler: 'Saturno' },
  { name: 'Acuario',     glyph: '♒', color: '#38bdf8', element: 'Aire',   ruler: 'Urano' },
  { name: 'Piscis',      glyph: '♓', color: '#818cf8', element: 'Agua',   ruler: 'Neptuno' },
]

const PLANETS_META = [
  { id: 'sun',     name: 'Sol',      glyph: '☉', color: '#fbbf24', speed: 0.9856 },
  { id: 'moon',    name: 'Luna',     glyph: '☽', color: '#e2e8f0', speed: 13.176 },
  { id: 'mercury', name: 'Mercurio', glyph: '☿', color: '#a3e635', speed: 4.0923 },
  { id: 'venus',   name: 'Venus',    glyph: '♀', color: '#f472b6', speed: 1.6021 },
  { id: 'mars',    name: 'Marte',    glyph: '♂', color: '#ef4444', speed: 0.5241 },
  { id: 'jupiter', name: 'Júpiter',  glyph: '♃', color: '#a78bfa', speed: 0.0831 },
  { id: 'saturn',  name: 'Saturno',  glyph: '♄', color: '#6b7280', speed: 0.0335 },
  { id: 'uranus',  name: 'Urano',    glyph: '♅', color: '#38bdf8', speed: 0.0117 },
  { id: 'neptune', name: 'Neptuno',  glyph: '♆', color: '#818cf8', speed: 0.0060 },
  { id: 'pluto',   name: 'Plutón',   glyph: '♇', color: '#dc2626', speed: 0.0040 },
]

// ─── MOTOR ASTRONÓMICO SIMPLIFICADO ──────────────────────────────────────────
function getPlanetPositions(date: Date) {
  const jd = (date.getTime() / 86400000) + 2440587.5
  const d = jd - 2451545.0
  const toRad = Math.PI / 180
  const toDeg = 180 / Math.PI

  // Sol (Geocéntrico)
  const sunL = (280.460 + 0.9856474 * d) % 360
  const sunM = (357.528 + 0.9856003 * d) % 360
  const sunLon = (sunL + 1.915 * Math.sin(sunM * toRad) + 0.020 * Math.sin(2 * sunM * toRad)) % 360

  // Luna (Geocéntrico)
  const moonL = (218.316 + 13.176396 * d) % 360
  const moonM = (134.963 + 13.064993 * d) % 360
  const moonLon = (moonL + 6.289 * Math.sin(moonM * toRad)) % 360

  // Motor Geocéntrico Mejorado
  const calcPlanetGeo = (days: number, baseL: number, daily: number, ecc: number, peri: number, dist: number, isInferior: boolean) => {
    const L = (baseL + daily * days) % 360
    const M = (L - peri) % 360
    const helioLon = (L + (2 * ecc * Math.sin(M * toRad) + 1.25 * ecc * ecc * Math.sin(2 * M * toRad)) * toDeg) % 360
    const relLon = (helioLon - sunLon) * toRad
    let geoLon
    if (!isInferior) {
      geoLon = sunLon + Math.atan2(Math.sin(relLon), (1/dist) + Math.cos(relLon)) * toDeg
    } else {
      geoLon = sunLon + Math.atan2(dist * Math.sin(relLon), 1 + dist * Math.cos(relLon)) * toDeg
    }
    return (geoLon + 360) % 360
  }

  // Elementos Orbitales (Aproximación J2000 calibrada para 2026)
  const mercury = (dd: number) => calcPlanetGeo(dd, 252.25, 4.0923, 0.2056, 77.45, 0.387, true)
  const venus   = (dd: number) => calcPlanetGeo(dd, 181.98, 1.6021, 0.0068, 131.57, 0.723, true)
  const mars    = (dd: number) => calcPlanetGeo(dd, 355.45, 0.5241, 0.0934, 336.06, 1.524, false)
  const jupiter = (dd: number) => calcPlanetGeo(dd, 34.40,  0.0831, 0.0484, 14.75, 5.203, false)
  const saturn  = (dd: number) => calcPlanetGeo(dd, 50.08,  0.0335, 0.0565, 92.43, 9.537, false)
  const uranus  = (dd: number) => calcPlanetGeo(dd, 314.05, 0.0117, 0.0463, 170.95, 19.191, false)
  const neptune = (dd: number) => calcPlanetGeo(dd, 304.34, 0.0060, 0.0090, 44.97, 30.069, false)
  const pluto   = (dd: number) => calcPlanetGeo(dd, 238.93, 0.0040, 0.2488, 224.06, 39.482, false)

  const positions: Record<string, number> = {
    sun: (sunLon + 360) % 360,
    moon: (moonLon + 360) % 360,
    mercury: mercury(d),
    venus: venus(d),
    mars: mars(d),
    jupiter: jupiter(d),
    saturn: saturn(d),
    uranus: uranus(d),
    neptune: neptune(d),
    pluto: pluto(d),
  }

  const isRetrograde = (id: string) => {
    if (id === 'sun' || id === 'moon') return false
    const posFuncs: Record<string, (dd: number) => number> = { mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto }
    const f = posFuncs[id]
    if (!f) return false
    const p1 = f(d)
    const p0 = f(d - 0.1)
    let diff = p1 - p0
    if (diff > 180) diff -= 360
    if (diff < -180) diff += 360
    return diff < 0
  }

  return { positions, isRetrograde }
}

function getAspects(positions: Record<string, number>) {
  const aspects: { p1: string, p2: string, type: string, orb: number, glyph: string }[] = []
  const keys = Object.keys(positions)
  const types = [
    { name: 'Conjunción', angle: 0,   orb: 8, glyph: '☌' },
    { name: 'Oposición',  angle: 180, orb: 8, glyph: '☍' },
    { name: 'Trígono',    angle: 120, orb: 7, glyph: '△' },
    { name: 'Cuadratura', angle: 90,  orb: 7, glyph: '□' },
    { name: 'Sextil',     angle: 60,  orb: 5, glyph: '⚹' },
  ]

  for (let i = 0; i < keys.length; i++) {
    for (let j = i + 1; j < keys.length; j++) {
      const diff = Math.abs(positions[keys[i]] - positions[keys[j]])
      const angle = diff > 180 ? 360 - diff : diff
      
      for (const t of types) {
        const orb = Math.abs(angle - t.angle)
        if (orb <= t.orb) {
          aspects.push({ p1: keys[i], p2: keys[j], type: t.name, orb, glyph: t.glyph })
          break
        }
      }
    }
  }
  return aspects
}

function getSign(lon: number) {
  const idx = Math.floor(lon / 30) % 12
  return ZODIAC[idx]
}

export default function AstrologyPage() {
  const router = useRouter()
  const [selectedDate, setSelectedDate] = useState(new Date())

  const data = useMemo(() => {
    const { positions, isRetrograde } = getPlanetPositions(selectedDate)
    const aspects = getAspects(positions)
    return { positions, isRetrograde, aspects }
  }, [selectedDate])

  const moonPhase = useMemo(() => {
    const jd = (selectedDate.getTime() / 86400000) + 2440587.5
    const lunarCycle = 29.530588853
    const phase = ((jd - 2451550.1) / lunarCycle) % 1
    const phaseNorm = phase < 0 ? phase + 1 : phase
    
    let name = 'Luna Nueva', glyph = '🌑'
    if (phaseNorm > 0.03 && phaseNorm <= 0.23) { name = 'Cuarto Creciente'; glyph = '🌒' }
    else if (phaseNorm > 0.23 && phaseNorm <= 0.27) { name = 'Primer Cuarto'; glyph = '🌓' }
    else if (phaseNorm > 0.27 && phaseNorm <= 0.47) { name = 'Gibosa Creciente'; glyph = '🌔' }
    else if (phaseNorm > 0.47 && phaseNorm <= 0.53) { name = 'Luna Llena'; glyph = '🌕' }
    else if (phaseNorm > 0.53 && phaseNorm <= 0.73) { name = 'Gibosa Menguante'; glyph = '🌖' }
    else if (phaseNorm > 0.73 && phaseNorm <= 0.77) { name = 'Último Cuarto'; glyph = '🌗' }
    else if (phaseNorm > 0.77 && phaseNorm <= 0.97) { name = 'Cuarto Menguante'; glyph = '🌘' }
    
    return { name, glyph, val: phaseNorm * 100 }
  }, [selectedDate])

  return (
    <main style={{ width: '100vw', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', background: 'linear-gradient(180deg, #0a0a1a, #1a0a2e, #0a0a1a)', padding: '40px 20px', color: '#fff', overflowY: 'auto' }}>
      <div style={{ fontSize: '18px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '12px', cursor: 'pointer', textAlign: 'center' }} onClick={() => router.push('/menu')}>← MENÚ PRINCIPAL</div>
      <h1 className="title-responsive" style={{ color: '#a78bfa' }}>ASTROLOGÍA ARQUEOSCÓPICA</h1>
      <p className="subtitle-responsive" style={{ marginBottom: '8px' }}>Sincronía Planetaria · Tránsitos y Aspectos</p>
      <p className="text-responsive" style={{ marginBottom: '24px', color: 'rgba(255,255,255,0.3)' }}>Cálculo de posiciones geocéntricas y relaciones angulares sagradas.</p>

      <input type="date" value={selectedDate.toISOString().split('T')[0]} onChange={(e) => setSelectedDate(new Date(e.target.value + 'T12:00:00'))}
        style={{ padding: '12px 24px', fontSize: '18px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(167,139,250,0.3)', borderRadius: '8px', color: '#a78bfa', marginBottom: '40px', cursor: 'pointer' }} />

      {/* ─── ESTADO LUNAR ────────────────────────────────────────────── */}
      <div className="info-card" style={{ background: 'rgba(226,232,240,0.04)', border: '1px solid rgba(226,232,240,0.2)', padding: 'clamp(16px, 5vw, 32px)', maxWidth: '500px' }}>
        <div style={{ fontSize: 'clamp(50px, 12vw, 64px)', marginBottom: '8px' }}>{moonPhase.glyph}</div>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '3px', marginBottom: '4px' }}>FASE LUNAR</div>
        <h2 style={{ color: '#e2e8f0' }}>{moonPhase.name}</h2>
        <div style={{ fontSize: '18px', color: 'rgba(255,255,255,0.6)', marginTop: '8px' }}>Iluminación: {moonPhase.val.toFixed(1)}%</div>
      </div>

      {/* ─── POSICIONES PLANETARIAS ──────────────────────────────────── */}
      <div className="info-card" style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.1)', maxWidth: '900px', width: '100%', padding: 'clamp(16px, 4vw, 24px)' }}>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '20px', textAlign: 'center' }}>POSICIONES DEL ZODIACO</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          {PLANETS_META.map((p) => {
            const lon = data.positions[p.id]
            const sign = getSign(lon)
            const deg = Math.floor(lon % 30)
            const isRetro = data.isRetrograde(p.id)
            return (
              <div key={p.id} style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '12px', textAlign: 'left', position: 'relative' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                  <span style={{ fontSize: '32px', color: p.color }}>{p.glyph}</span>
                  <div>
                    <div style={{ fontWeight: 'bold', fontSize: '18px' }}>{p.name} {isRetro && <span style={{ color: '#ef4444', fontSize: '12px' }}>[Rx]</span>}</div>
                    <div style={{ color: sign.color, fontSize: '14px' }}>{deg}° {sign.name} {sign.glyph}</div>
                  </div>
                </div>
                <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.3)' }}>Elemento: {sign.element} · Regente: {sign.ruler}</div>
                {isRetro && <div style={{ fontSize: '10px', color: '#ef4444', marginTop: '4px' }}>⚠️ Retrogradación activa</div>}
              </div>
            )
          })}
        </div>
      </div>

      {/* ─── ASPECTOS PLANETARIAS ───────────────────────────────────── */}
      <div className="info-card" style={{ background: 'rgba(167,139,250,0.03)', border: '1px solid rgba(167,139,250,0.15)', maxWidth: '900px', width: '100%', padding: 'clamp(16px, 4vw, 24px)' }}>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '20px', textAlign: 'center' }}>ASPECTOS MAYORES (RELACIONES ANGULARES)</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '12px' }}>
          {data.aspects.length > 0 ? data.aspects.map((a, i) => {
            const p1 = PLANETS_META.find(p => p.id === a.p1)!
            const p2 = PLANETS_META.find(p => p.id === a.p2)!
            return (
              <div key={i} style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ color: p1.color }}>{p1.glyph}</span>
                  <span style={{ fontSize: '20px', fontWeight: 'bold', color: '#a78bfa' }}>{a.glyph}</span>
                  <span style={{ color: p2.color }}>{p2.glyph}</span>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '14px', fontWeight: 'bold' }}>{a.type}</div>
                  <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.4)' }}>Orb: {a.orb.toFixed(1)}°</div>
                </div>
              </div>
            )
          }) : (
            <div style={{ gridColumn: '1/-1', color: 'rgba(255,255,255,0.3)', padding: '20px' }}>No hay aspectos mayores significativos en este momento.</div>
          )}
        </div>
      </div>

      {/* ─── GUÍA DE INTERPRETACIÓN ─────────────────────────────────── */}
      <div className="info-card" style={{ background: 'rgba(251,191,36,0.02)', border: '1px solid rgba(251,191,36,0.1)', maxWidth: '900px', width: '100%', padding: 'clamp(16px, 4vw, 24px)' }}>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '16px', textAlign: 'center' }}>GUÍA DE ASPECTOS</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', textAlign: 'left' }}>
          <div>
            <strong style={{ color: '#fbbf24' }}>☌ Conjunción:</strong> Fusión de energías. Potencia el impacto de ambos planetas.
          </div>
          <div>
            <strong style={{ color: '#fbbf24' }}>☍ Oposición:</strong> Tensión y equilibrio. Necesidad de integrar polaridades.
          </div>
          <div>
            <strong style={{ color: '#fbbf24' }}>□ Cuadratura:</strong> Desafío y acción. Tensión que impulsa el cambio.
          </div>
          <div>
            <strong style={{ color: '#fbbf24' }}>△ Trígono:</strong> Armonía y fluidez. Talentos naturales que fluyen sin esfuerzo.
          </div>
          <div>
            <strong style={{ color: '#fbbf24' }}>⚹ Sextil:</strong> Oportunidad y colaboración. Estímulo creativo y facilidad de comunicación.
          </div>
        </div>
      </div>

      <button onClick={() => router.push('/menu')} className="btn-responsive"
        onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#fff' }}
        onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)' }}>
        Volver
      </button>
    </main>
  )
}
