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

// ─── MOTOR ASTRONÓMICO — astronomy-engine (VSOP87/ELP, precisión ~1 arcmin) ──
import * as Astronomy from 'astronomy-engine'

// Velocidad instantánea dλ/dt en grados/día (Δt = 1 hora para máxima precisión)
function getPlanetSpeed(body: Astronomy.Body, t: Astronomy.AstroTime): number {
  const dt = 1 / 24 // 1 hora en días
  const tNext = Astronomy.MakeTime(new Date(t.date.getTime() + dt * 86400000))
  const lonNow = Astronomy.EclipticLongitude(body, t)
  const lonNext = Astronomy.EclipticLongitude(body, tNext)
  let diff = lonNext - lonNow
  if (diff > 180) diff -= 360
  if (diff < -180) diff += 360
  return diff / dt // grados/día
}

// Clasificar estado del planeta según velocidad
function getPlanetStatus(speed: number, avgSpeed: number): 'direct' | 'retrograde' | 'stationary-direct' | 'stationary-retrograde' {
  const stationaryThreshold = Math.abs(avgSpeed) * 0.05 // <5% de velocidad media = estacionario
  if (Math.abs(speed) < stationaryThreshold) {
    return speed >= 0 ? 'stationary-direct' : 'stationary-retrograde'
  }
  return speed > 0 ? 'direct' : 'retrograde'
}

function getPlanetPositions(date: Date) {
  const t = Astronomy.MakeTime(date)

  // Sol: usa SunPosition (elon = longitud eclíptica)
  const sunPos = Astronomy.SunPosition(t)
  const sunLon = sunPos.elon

  // Luna y planetas: EclipticLongitude con Body enum
  const moonLon = Astronomy.EclipticLongitude(Astronomy.Body.Moon, t)

  const positions: Record<string, number> = {
    sun: sunLon,
    moon: moonLon,
    mercury: Astronomy.EclipticLongitude(Astronomy.Body.Mercury, t),
    venus: Astronomy.EclipticLongitude(Astronomy.Body.Venus, t),
    mars: Astronomy.EclipticLongitude(Astronomy.Body.Mars, t),
    jupiter: Astronomy.EclipticLongitude(Astronomy.Body.Jupiter, t),
    saturn: Astronomy.EclipticLongitude(Astronomy.Body.Saturn, t),
    uranus: Astronomy.EclipticLongitude(Astronomy.Body.Uranus, t),
    neptune: Astronomy.EclipticLongitude(Astronomy.Body.Neptune, t),
    pluto: Astronomy.EclipticLongitude(Astronomy.Body.Pluto, t),
  }

  const bodyMap: Record<string, Astronomy.Body> = {
    mercury: Astronomy.Body.Mercury, venus: Astronomy.Body.Venus,
    mars: Astronomy.Body.Mars, jupiter: Astronomy.Body.Jupiter,
    saturn: Astronomy.Body.Saturn, uranus: Astronomy.Body.Uranus,
    neptune: Astronomy.Body.Neptune, pluto: Astronomy.Body.Pluto
  }

  // Velocidades instantáneas (Δt = 1 hora — más preciso en puntos estacionarios)
  const speeds: Record<string, number> = {}
  Object.entries(bodyMap).forEach(([id, body]) => {
    speeds[id] = getPlanetSpeed(body, t)
  })
  // Sol y Luna: velocidad aproximada
  speeds.sun = 0.9856
  speeds.moon = 13.176

  // Estado del planeta: direct / retrograde / stationary-direct / stationary-retrograde
  const planetStatus: Record<string, ReturnType<typeof getPlanetStatus>> = {}
  Object.entries(bodyMap).forEach(([id, _]) => {
    const avgSpeed = PLANETS_META.find(p => p.id === id)?.speed || 1
    planetStatus[id] = getPlanetStatus(speeds[id], avgSpeed)
  })
  planetStatus.sun = 'direct'
  planetStatus.moon = 'direct'

  // isRetrograde: Δt = 1 hora (más preciso que 1 día en puntos estacionarios)
  const isRetrograde = (id: string) => {
    if (id === 'sun' || id === 'moon') return false
    return speeds[id] < 0
  }

  return { positions, isRetrograde, speeds, planetStatus }
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

// ─── INTERPRETACIÓN ASTROLÓGICA PROFESIONAL ──────────────────────────────────
const PLANET_INTERPRETATIONS: Record<string, Record<string, string>> = {
  sun: {
    Aries: 'Voluntad directa y pionera. Impulso de liderazgo y acción inmediata.',
    Tauro: 'Voluntad estable y constructiva. Búsqueda de seguridad material y sensorial.',
    Géminis: 'Identidad versátil y comunicativa. Necesidad de variedad intelectual.',
    Cáncer: 'Identidad emocional y protectora. Raíces familiares como centro vital.',
    Leo: 'Expresión creativa plena. Necesidad de reconocimiento y brillo personal.',
    Virgo: 'Identidad analítica y servicial. Perfeccionismo como motor de crecimiento.',
    Libra: 'Búsqueda de equilibrio y armonía. Identidad definida a través de las relaciones.',
    Escorpio: 'Voluntad transformadora e intensa. Profundidad emocional como fuerza.',
    Sagitario: 'Expansión filosófica y aventurera. Búsqueda de significado y libertad.',
    Capricornio: 'Disciplina y estructura como identidad. Ambición orientada a logros duraderos.',
    Acuario: 'Identidad innovadora y humanitaria. Visión de futuro y originalidad.',
    Piscis: 'Sensibilidad trascendente. Conexión con lo invisible y lo espiritual.',
  },
  moon: {
    Aries: 'Emociones impulsivas y directas. Necesidad de independencia emocional.',
    Tauro: 'Emociones estables y sensoriales. Seguridad afectiva a través de lo tangible.',
    Géminis: 'Emociones cambiantes y curiosas. Procesamiento intelectual de los sentimientos.',
    Cáncer: 'Emociones profundas y nutritivas. Gran capacidad empática y protectora.',
    Leo: 'Emociones expresivas y generosas. Necesidad de ser visto y apreciado.',
    Virgo: 'Emociones contenidas y analíticas. Cuidado expresado a través del servicio.',
    Libra: 'Emociones equilibradas y diplomáticas. Necesidad de armonía en las relaciones.',
    Escorpio: 'Emociones intensas y transformadoras. Profundidad que busca la verdad.',
    Sagitario: 'Emociones expansivas y optimistas. Libertad emocional como prioridad.',
    Capricornio: 'Emociones controladas y responsables. Madurez emocional temprana.',
    Acuario: 'Emociones desapegadas e innovadoras. Necesidad de espacio y originalidad.',
    Piscis: 'Emociones oceánicas y compasivas. Sensibilidad extrema al entorno.',
  },
}

const ASPECT_INTERPRETATIONS: Record<string, string> = {
  'sun-moon-Conjunción': 'Luna nueva interior: las emociones y la voluntad están alineadas. Momento de siembra.',
  'sun-moon-Oposición': 'Luna llena interior: tensión entre lo que quieres y lo que sientes. Momento de revelación.',
  'sun-mars-Conjunción': 'Energía vital amplificada. Gran capacidad de acción pero riesgo de impulsividad.',
  'sun-jupiter-Trígono': 'Expansión armoniosa. Optimismo natural y oportunidades que fluyen.',
  'sun-saturn-Cuadratura': 'Tensión entre deseo y responsabilidad. Crecimiento a través de la disciplina.',
  'venus-mars-Conjunción': 'Fusión de lo femenino y lo masculino. Magnetismo personal intenso.',
  'venus-jupiter-Trígono': 'Armonía social y abundancia. Período favorable para relaciones y finanzas.',
  'mars-saturn-Cuadratura': 'Frustración que impulsa la acción estratégica. Paciencia como virtud.',
  'jupiter-saturn-Conjunción': 'Ciclo de 20 años: expansión estructurada. Nuevos cimientos sociales.',
  'saturn-uranus-Cuadratura': 'Tensión entre tradición e innovación. Reestructuración necesaria.',
  'saturn-neptune-Oposición': 'Confrontación entre realidad e idealismo. Necesidad de anclar los sueños.',
}

function generateInterpretation(
  positions: Record<string, number>,
  aspects: { p1: string, p2: string, type: string, orb: number }[],
  isRetrograde: (id: string) => boolean
): string[] {
  const lines: string[] = []

  // Interpretación del Sol y Luna
  const sunSign = getSign(positions.sun)
  const moonSign = getSign(positions.moon)
  if (PLANET_INTERPRETATIONS.sun[sunSign.name]) {
    lines.push(`☉ Sol en ${sunSign.name}: ${PLANET_INTERPRETATIONS.sun[sunSign.name]}`)
  }
  if (PLANET_INTERPRETATIONS.moon[moonSign.name]) {
    lines.push(`☽ Luna en ${moonSign.name}: ${PLANET_INTERPRETATIONS.moon[moonSign.name]}`)
  }

  // Retrogradaciones
  const retros = PLANETS_META.filter(p => isRetrograde(p.id))
  if (retros.length > 0) {
    const names = retros.map(p => p.name).join(', ')
    lines.push(`⚠️ Retrogradaciones activas (${names}): período de revisión interna en las áreas gobernadas por estos planetas. No es momento de iniciar, sino de reconsiderar y ajustar.`)
  }

  // Planetas estacionarios (velocidad ~0) — muy raros y significativos
  const stationaries = PLANETS_META.filter(p => {
    const status = (positions as any)._status?.[p.id]
    return status === 'stationary-direct' || status === 'stationary-retrograde'
  })
  if (stationaries.length > 0) {
    const names = stationaries.map(p => p.name).join(', ')
    lines.push(`⊙ Planeta(s) estacionario(s) (${names}): momento de máxima intensidad. El planeta está cambiando de dirección — su energía se concentra y amplifica. Evento astronómico raro y astrológicamente significativo.`)
  }

  // Aspectos específicos
  aspects.forEach(a => {
    const key = `${a.p1}-${a.p2}-${a.type}`
    const keyReverse = `${a.p2}-${a.p1}-${a.type}`
    const interp = ASPECT_INTERPRETATIONS[key] || ASPECT_INTERPRETATIONS[keyReverse]
    if (interp) {
      const p1 = PLANETS_META.find(p => p.id === a.p1)
      const p2 = PLANETS_META.find(p => p.id === a.p2)
      if (p1 && p2) {
        lines.push(`${p1.glyph}${a.type === 'Conjunción' ? '☌' : a.type === 'Oposición' ? '☍' : a.type === 'Trígono' ? '△' : a.type === 'Cuadratura' ? '□' : '⚹'}${p2.glyph} ${p1.name}–${p2.name} (${a.type}): ${interp}`)
      }
    }
  })

  // Resumen general
  const trines = aspects.filter(a => a.type === 'Trígono').length
  const squares = aspects.filter(a => a.type === 'Cuadratura').length
  const opps = aspects.filter(a => a.type === 'Oposición').length
  const conjs = aspects.filter(a => a.type === 'Conjunción').length

  if (trines > squares + opps) {
    lines.push('✦ Clima general: predominan los aspectos armónicos. Período de fluidez y oportunidades naturales.')
  } else if (squares + opps > trines) {
    lines.push('✦ Clima general: predominan los aspectos tensos. Período de desafíos que impulsan el crecimiento y la acción.')
  } else {
    lines.push('✦ Clima general: equilibrio entre armonía y tensión. Momento de integración y decisiones conscientes.')
  }

  if (conjs >= 2) {
    lines.push('✦ Múltiples conjunciones activas: concentración de energía en áreas específicas. Momento de intensidad y enfoque.')
  }

  return lines
}

export default function AstrologyPage() {
  const router = useRouter()
  const [selectedDate, setSelectedDate] = useState(new Date())

  const data = useMemo(() => {
    const { positions, isRetrograde, speeds, planetStatus } = getPlanetPositions(selectedDate)
    const aspects = getAspects(positions)
    return { positions, isRetrograde, speeds, planetStatus, aspects }
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

  const wheelSize = typeof window !== 'undefined' && window.innerWidth < 500 ? 360 : 520
  const cx = wheelSize / 2
  const cy = wheelSize / 2
  const R = wheelSize / 2 - 8
  const lonToAngle = (lon: number) => ((lon - 90) * Math.PI) / 180
  const rOuter = R
  const rZodiac2 = R * 0.88
  const rZodiac1 = R * 0.72
  const rHouse2 = R * 0.70
  const rHouse1 = R * 0.55
  const rPlanet = R * 0.63
  const rAspect = R * 0.50
  const rCenter = R * 0.14
  const aspectColors: Record<string, string> = {
    'Conjunción': '#fbbf24', 'Oposición': '#ef4444',
    'Trígono': '#22c55e', 'Cuadratura': '#f97316', 'Sextil': '#38bdf8'
  }

  return (
    <main style={{ width: '100vw', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', background: 'linear-gradient(180deg, #06060f, #0d0820, #06060f)', padding: '32px 16px', color: '#fff', overflowY: 'auto' }}>
      <div style={{ fontSize: '19px', color: 'rgba(255,255,255,0.35)', letterSpacing: '2px', marginBottom: '10px', cursor: 'pointer', textAlign: 'center' }} onClick={() => router.push('/menu')}>← MENÚ PRINCIPAL</div>
      <h1 className="title-responsive" style={{ color: '#a78bfa', marginBottom: '4px' }}>ASTROLOGÍA ARQUEOSCÓPICA</h1>
      <p style={{ fontSize: '19px', color: 'rgba(255,255,255,0.35)', letterSpacing: '3px', marginBottom: '20px', textAlign: 'center' }}>CARTA CELESTE · POSICIONES GEOCÉNTRICAS · ASPECTOS</p>

      <input type="date" value={selectedDate.toISOString().split('T')[0]}
        onChange={(e) => setSelectedDate(new Date(e.target.value + 'T12:00:00'))}
        style={{ padding: '10px 20px', fontSize: '22px', background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(167,139,250,0.4)', borderRadius: '8px', color: '#a78bfa', marginBottom: '28px', cursor: 'pointer' }} />

      {/* RUEDA ASTROLÓGICA */}
      <div style={{ background: 'rgba(10,8,20,0.95)', border: '1px solid rgba(167,139,250,0.25)', borderRadius: '16px', padding: '20px', marginBottom: '20px', boxShadow: '0 0 60px rgba(167,139,250,0.08)' }}>
        <div style={{ fontSize: '17px', color: 'rgba(255,255,255,0.3)', letterSpacing: '3px', marginBottom: '14px', textAlign: 'center', textTransform: 'uppercase' }}>
          Carta Celeste · {selectedDate.toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' })} · Tropical/Geocéntrico
        </div>
        <svg width={wheelSize} height={wheelSize} viewBox={`0 0 ${wheelSize} ${wheelSize}`} style={{ display: 'block', margin: '0 auto' }}>
          <defs>
            <radialGradient id="bgGrad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#0d0820" />
              <stop offset="100%" stopColor="#06060f" />
            </radialGradient>
          </defs>
          <circle cx={cx} cy={cy} r={rOuter} fill="url(#bgGrad)" stroke="rgba(167,139,250,0.3)" strokeWidth="1" />
          {/* Marcas de grados */}
          {Array.from({ length: 72 }).map((_, i) => {
            const deg = i * 5
            const isMajor = deg % 30 === 0
            const isMed = deg % 10 === 0
            const angle = lonToAngle(deg)
            const r1 = isMajor ? rOuter * 0.94 : isMed ? rOuter * 0.96 : rOuter * 0.97
            return (
              <line key={i}
                x1={cx + rOuter * Math.cos(angle)} y1={cy + rOuter * Math.sin(angle)}
                x2={cx + r1 * Math.cos(angle)} y2={cy + r1 * Math.sin(angle)}
                stroke={isMajor ? 'rgba(167,139,250,0.6)' : 'rgba(167,139,250,0.25)'}
                strokeWidth={isMajor ? '1.2' : '0.6'}
              />
            )
          })}
          {/* Sectores zodiacales */}
          {ZODIAC.map((sign, i) => {
            const startA = lonToAngle(i * 30)
            const endA = lonToAngle((i + 1) * 30)
            const midA = lonToAngle(i * 30 + 15)
            const x1s = cx + rZodiac1 * Math.cos(startA), y1s = cy + rZodiac1 * Math.sin(startA)
            const x2s = cx + rZodiac2 * Math.cos(startA), y2s = cy + rZodiac2 * Math.sin(startA)
            const x3s = cx + rZodiac2 * Math.cos(endA), y3s = cy + rZodiac2 * Math.sin(endA)
            const x4s = cx + rZodiac1 * Math.cos(endA), y4s = cy + rZodiac1 * Math.sin(endA)
            const tx = cx + ((rZodiac1 + rZodiac2) / 2) * Math.cos(midA)
            const ty = cy + ((rZodiac1 + rZodiac2) / 2) * Math.sin(midA)
            return (
              <g key={sign.name}>
                <path d={`M ${x1s} ${y1s} L ${x2s} ${y2s} A ${rZodiac2} ${rZodiac2} 0 0 1 ${x3s} ${y3s} L ${x4s} ${y4s} A ${rZodiac1} ${rZodiac1} 0 0 0 ${x1s} ${y1s}`}
                  fill={`${sign.color}14`} stroke={`${sign.color}35`} strokeWidth="0.5" />
                <text x={tx} y={ty} textAnchor="middle" dominantBaseline="middle"
                  fontSize={wheelSize < 400 ? "19" : "22"} fill={sign.color} opacity="0.95" fontWeight="bold">{sign.glyph}</text>
              </g>
            )
          })}
          {/* Líneas divisorias signos */}
          {ZODIAC.map((_, i) => {
            const angle = lonToAngle(i * 30)
            return (
              <line key={i}
                x1={cx + rZodiac1 * Math.cos(angle)} y1={cy + rZodiac1 * Math.sin(angle)}
                x2={cx + rOuter * 0.93 * Math.cos(angle)} y2={cy + rOuter * 0.93 * Math.sin(angle)}
                stroke="rgba(167,139,250,0.4)" strokeWidth="0.8" />
            )
          })}
          {/* Anillos concéntricos */}
          {[rZodiac2, rZodiac1, rHouse2, rHouse1, rAspect * 1.05].map((r, i) => (
            <circle key={i} cx={cx} cy={cy} r={r} fill="none"
              stroke={i < 2 ? 'rgba(167,139,250,0.35)' : 'rgba(167,139,250,0.18)'}
              strokeWidth={i < 2 ? '0.8' : '0.5'} />
          ))}
          {/* Casas */}
          {Array.from({ length: 12 }).map((_, i) => {
            const angle = lonToAngle(i * 30)
            const midA = lonToAngle(i * 30 + 15)
            const tx = cx + ((rHouse1 + rHouse2) / 2) * Math.cos(midA)
            const ty = cy + ((rHouse1 + rHouse2) / 2) * Math.sin(midA)
            return (
              <g key={i}>
                <line x1={cx + rHouse1 * Math.cos(angle)} y1={cy + rHouse1 * Math.sin(angle)}
                  x2={cx + rHouse2 * Math.cos(angle)} y2={cy + rHouse2 * Math.sin(angle)}
                  stroke="rgba(167,139,250,0.25)" strokeWidth="0.5" />
                <text x={tx} y={ty} textAnchor="middle" dominantBaseline="middle"
                  fontSize={wheelSize < 400 ? "15" : "17"} fill="rgba(167,139,250,0.55)">{i + 1}</text>
              </g>
            )
          })}
          {/* Ejes AC/DC y MC/IC */}
          {[0, 90].map((deg, i) => {
            const a1 = lonToAngle(deg), a2 = lonToAngle(deg + 180)
            return (
              <line key={i}
                x1={cx + rHouse1 * Math.cos(a1)} y1={cy + rHouse1 * Math.sin(a1)}
                x2={cx + rHouse1 * Math.cos(a2)} y2={cy + rHouse1 * Math.sin(a2)}
                stroke={i === 0 ? 'rgba(239,68,68,0.5)' : 'rgba(167,139,250,0.4)'}
                strokeWidth="0.8" strokeDasharray={i === 1 ? '4,3' : 'none'} />
            )
          })}
          {/* Líneas de aspectos */}
          {data.aspects.map((a, i) => {
            const a1 = lonToAngle(data.positions[a.p1]), a2 = lonToAngle(data.positions[a.p2])
            const x1 = cx + rAspect * Math.cos(a1), y1 = cy + rAspect * Math.sin(a1)
            const x2 = cx + rAspect * Math.cos(a2), y2 = cy + rAspect * Math.sin(a2)
            return (
              <line key={i} x1={x1} y1={y1} x2={x2} y2={y2}
                stroke={aspectColors[a.type] || '#888'} strokeWidth="0.9" opacity="0.55"
                strokeDasharray={a.type === 'Cuadratura' || a.type === 'Oposición' ? '4,3' : 'none'} />
            )
          })}
          {/* Planetas */}
          {PLANETS_META.map((p) => {
            const lon = data.positions[p.id]
            const angle = lonToAngle(lon)
            const px = cx + rPlanet * Math.cos(angle), py = cy + rPlanet * Math.sin(angle)
            const isRetro = data.isRetrograde(p.id)
            const degInSign = Math.floor(lon % 30)
            const lx = cx + rZodiac1 * Math.cos(angle), ly = cy + rZodiac1 * Math.sin(angle)
            const fs = wheelSize < 400 ? 16 : 19
            return (
              <g key={p.id}>
                <line x1={px} y1={py} x2={lx} y2={ly} stroke={p.color} strokeWidth="0.5" opacity="0.3" />
                <circle cx={px} cy={py} r={wheelSize < 400 ? 11 : 13} fill="rgba(6,6,15,0.92)" stroke={p.color} strokeWidth="1.5" />
                <text x={px} y={py} textAnchor="middle" dominantBaseline="middle" fontSize={fs} fill={p.color} fontWeight="bold">{p.glyph}</text>
                <text x={px + (wheelSize < 400 ? 12 : 15)} y={py - (wheelSize < 400 ? 4 : 5)} fontSize={wheelSize < 400 ? "13" : "15"} fill={p.color} opacity="0.8">{degInSign}°</text>
                {isRetro && <text x={px + (wheelSize < 400 ? 12 : 15)} y={py + (wheelSize < 400 ? 6 : 8)} fontSize="13" fill="#ef4444" fontStyle="italic">Rx</text>}
              </g>
            )
          })}
          <circle cx={cx} cy={cy} r={rCenter} fill="rgba(10,8,20,0.95)" stroke="rgba(167,139,250,0.4)" strokeWidth="1" />
          <text x={cx} y={cy} textAnchor="middle" dominantBaseline="middle" fontSize={wheelSize < 400 ? "23" : "27"} fill="rgba(167,139,250,0.5)">⊕</text>
        </svg>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', justifyContent: 'center', marginTop: '14px', paddingTop: '12px', borderTop: '1px solid rgba(167,139,250,0.1)' }}>
          {Object.entries(aspectColors).map(([name, color]) => (
            <span key={name} style={{ fontSize: '24px', color, opacity: 0.85, letterSpacing: '0.5px' }}>
              {name === 'Conjunción' ? '☌' : name === 'Oposición' ? '☍' : name === 'Trígono' ? '△' : name === 'Cuadratura' ? '□' : '⚹'} {name}
            </span>
          ))}
        </div>
      </div>

      {/* FASE LUNAR */}
      <div className="info-card" style={{ background: 'rgba(226,232,240,0.04)', border: '1px solid rgba(226,232,240,0.2)', padding: 'clamp(16px, 5vw, 28px)', maxWidth: '500px' }}>
        <div style={{ fontSize: '19px', color: 'rgba(255,255,255,0.35)', letterSpacing: '3px', marginBottom: '8px', textAlign: 'center' }}>FASE LUNAR</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px', justifyContent: 'center' }}>
          <span style={{ fontSize: 'clamp(44px, 10vw, 56px)' }}>{moonPhase.glyph}</span>
          <div>
            <div style={{ fontSize: 'clamp(18px, 4vw, 22px)', fontWeight: 'bold', color: '#e2e8f0' }}>{moonPhase.name}</div>
            <div style={{ fontSize: '21px', color: 'rgba(255,255,255,0.5)', marginTop: '4px' }}>Iluminación: {moonPhase.val.toFixed(1)}%</div>
          </div>
        </div>
      </div>

      {/* POSICIONES */}
      <div className="info-card" style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.08)', maxWidth: '900px', width: '100%', padding: 'clamp(16px, 4vw, 24px)' }}>
        <div style={{ fontSize: '17px', color: 'rgba(255,255,255,0.35)', letterSpacing: '3px', marginBottom: '18px', textAlign: 'center' }}>POSICIONES DEL ZODIACO</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(190px, 1fr))', gap: '12px' }}>
          {PLANETS_META.map((p) => {
            const lon = data.positions[p.id]
            const sign = getSign(lon)
            const deg = Math.floor(lon % 30)
            const min = Math.floor((lon % 1) * 60)
            const isRetro = data.isRetrograde(p.id)
            const status = data.planetStatus[p.id]
            const speed = data.speeds[p.id]
            const isStationary = status === 'stationary-direct' || status === 'stationary-retrograde'
            const statusLabel = isStationary
              ? (status === 'stationary-direct' ? '⊙ Estacionario D' : '⊙ Estacionario Rx')
              : isRetro ? 'Rx' : null
            const statusColor = isStationary ? '#fbbf24' : '#ef4444'
            return (
              <div key={p.id} style={{
                padding: '14px',
                background: isStationary ? 'rgba(251,191,36,0.06)' : 'rgba(255,255,255,0.025)',
                border: `1px solid ${isStationary ? 'rgba(251,191,36,0.25)' : 'rgba(255,255,255,0.06)'}`,
                borderRadius: '10px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
                  <span style={{ fontSize: '36px', color: p.color }}>{p.glyph}</span>
                  <div>
                    <div style={{ fontWeight: 'bold', fontSize: '22px' }}>
                      {p.name}{' '}
                      {statusLabel && <span style={{ color: statusColor, fontSize: '14px', fontStyle: 'italic' }}>{statusLabel}</span>}
                    </div>
                    <div style={{ color: sign.color, fontSize: '20px' }}>{deg}°{min.toString().padStart(2,'0')}′ {sign.name} {sign.glyph}</div>
                  </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ fontSize: '17px', color: 'rgba(255,255,255,0.28)', letterSpacing: '0.5px' }}>{sign.element} · {sign.ruler}</div>
                  {p.id !== 'sun' && p.id !== 'moon' && (
                    <div style={{ fontSize: '13px', color: isRetro ? '#ef4444' : 'rgba(255,255,255,0.2)', letterSpacing: '0.5px' }}>
                      {speed > 0 ? '+' : ''}{speed.toFixed(3)}°/d
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* ASPECTOS */}
      <div className="info-card" style={{ background: 'rgba(167,139,250,0.02)', border: '1px solid rgba(167,139,250,0.12)', maxWidth: '900px', width: '100%', padding: 'clamp(16px, 4vw, 24px)' }}>
        <div style={{ fontSize: '17px', color: 'rgba(255,255,255,0.35)', letterSpacing: '3px', marginBottom: '16px', textAlign: 'center' }}>ASPECTOS MAYORES</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '10px' }}>
          {data.aspects.length > 0 ? data.aspects.map((a, i) => {
            const p1 = PLANETS_META.find(p => p.id === a.p1)!
            const p2 = PLANETS_META.find(p => p.id === a.p2)!
            return (
              <div key={i} style={{ padding: '10px 14px', background: 'rgba(255,255,255,0.025)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ color: p1.color, fontSize: '24px' }}>{p1.glyph}</span>
                  <span style={{ fontSize: '24px', fontWeight: 'bold', color: aspectColors[a.type] }}>{a.glyph}</span>
                  <span style={{ color: p2.color, fontSize: '24px' }}>{p2.glyph}</span>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '19px', fontWeight: 'bold', color: aspectColors[a.type] }}>{a.type}</div>
                  <div style={{ fontSize: '17px', color: 'rgba(255,255,255,0.35)' }}>orb {a.orb.toFixed(1)}°</div>
                </div>
              </div>
            )
          }) : (
            <div style={{ gridColumn: '1/-1', color: 'rgba(255,255,255,0.25)', padding: '16px', textAlign: 'center', fontSize: '20px' }}>Sin aspectos mayores significativos en esta fecha.</div>
          )}
        </div>
      </div>

      {/* INTERPRETACIÓN PROFESIONAL */}
      <div className="info-card" style={{ background: 'rgba(251,191,36,0.03)', border: '1px solid rgba(251,191,36,0.15)', maxWidth: '900px', width: '100%', padding: 'clamp(18px, 4vw, 28px)' }}>
        <div style={{ fontSize: 'clamp(11px, 2.5vw, 22px)', color: '#fbbf24', letterSpacing: '3px', marginBottom: '18px', textAlign: 'center' }}>
          LECTURA ASTROLÓGICA · {selectedDate.toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' })}
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {generateInterpretation(data.positions, data.aspects, data.isRetrograde).map((line, i) => (
            <div key={i} style={{
              fontSize: 'clamp(13px, 2.5vw, 20px)',
              color: line.startsWith('✦') ? 'rgba(251,191,36,0.85)' : line.startsWith('⚠') ? 'rgba(239,68,68,0.8)' : 'rgba(255,255,255,0.65)',
              lineHeight: '1.7',
              paddingLeft: line.startsWith('✦') || line.startsWith('⚠') ? '0' : '8px',
              borderLeft: line.startsWith('✦') || line.startsWith('⚠') ? 'none' : '2px solid rgba(251,191,36,0.2)',
              fontStyle: line.startsWith('✦') ? 'italic' : 'normal',
              fontWeight: line.startsWith('✦') ? 'bold' : 'normal',
              marginTop: line.startsWith('✦') ? '8px' : '0',
              paddingTop: line.startsWith('✦') ? '12px' : '0',
              borderTop: line.startsWith('✦') ? '1px solid rgba(251,191,36,0.1)' : 'none',
            }}>
              {line}
            </div>
          ))}
        </div>
      </div>

      {/* GUÍA */}
      <div className="info-card" style={{ background: 'rgba(251,191,36,0.02)', border: '1px solid rgba(251,191,36,0.08)', maxWidth: '900px', width: '100%', padding: 'clamp(14px, 4vw, 22px)' }}>
        <div style={{ fontSize: '17px', color: 'rgba(255,255,255,0.35)', letterSpacing: '3px', marginBottom: '14px', textAlign: 'center' }}>GUÍA DE ASPECTOS</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px', fontSize: '19px' }}>
          {[
            { g: '☌', n: 'Conjunción', d: 'Fusión de energías. Potencia el impacto de ambos planetas.' },
            { g: '☍', n: 'Oposición', d: 'Tensión y equilibrio. Necesidad de integrar polaridades.' },
            { g: '□', n: 'Cuadratura', d: 'Desafío y acción. Tensión que impulsa el cambio.' },
            { g: '△', n: 'Trígono', d: 'Armonía y fluidez. Talentos naturales sin esfuerzo.' },
            { g: '⚹', n: 'Sextil', d: 'Oportunidad y colaboración. Estímulo creativo.' },
          ].map(({ g, n, d }) => (
            <div key={n}>
              <div style={{ color: '#fbbf24', fontWeight: 'bold', marginBottom: '3px' }}>{g} {n}</div>
              <div style={{ color: 'rgba(255,255,255,0.45)', lineHeight: '1.5' }}>{d}</div>
            </div>
          ))}
        </div>
      </div>

      {/* NOTAS Y FUENTES */}
      <div style={{
        maxWidth: '900px', width: '100%', marginTop: '8px', marginBottom: '20px',
        padding: 'clamp(14px, 3vw, 24px)',
        background: 'rgba(255,255,255,0.015)',
        border: '1px solid rgba(255,255,255,0.06)',
        borderRadius: '12px',
        fontSize: 'clamp(11px, 2vw, 15px)',
        color: 'rgba(255,255,255,0.35)',
        lineHeight: '1.8'
      }}>
        <div style={{ color: 'rgba(255,255,255,0.5)', letterSpacing: '2px', marginBottom: '12px', fontSize: 'clamp(10px, 2vw, 13px)' }}>
          NOTAS METODOLÓGICAS Y FUENTES
        </div>
        <p style={{ margin: '0 0 10px' }}>
          <strong style={{ color: 'rgba(255,255,255,0.5)' }}>Cálculos astronómicos:</strong> Las posiciones planetarias se calculan con la librería <em>astronomy-engine</em> que implementa las efemérides VSOP87 (planetas) y ELP/MPP02 (Luna), las mismas utilizadas por el JPL de NASA. Precisión de ~1 arcminuto para planetas y ~10 arcsegundos para la Luna. Las posiciones son geocéntricas tropicales.
        </p>
        <p style={{ margin: '0 0 10px' }}>
          <strong style={{ color: 'rgba(255,255,255,0.5)' }}>Interpretaciones astrológicas:</strong> Basadas en la tradición astrológica occidental clásica (Ptolomeo, <em>Tetrabiblos</em>, siglo II d.C.) y la escuela psicológica moderna (Liz Greene, Stephen Arroyo, Howard Sasportas). Los significados de los aspectos ptolemaicos (conjunción, oposición, trígono, cuadratura, sextil) y las dignidades planetarias siguen el consenso de la tradición.
        </p>
        <p style={{ margin: '0 0 10px' }}>
          <strong style={{ color: 'rgba(255,255,255,0.5)' }}>Limitaciones:</strong> Esta herramienta calcula tránsitos generales, no cartas natales personales. Para una carta natal completa se requiere fecha, hora exacta y lugar de nacimiento, además del cálculo de casas astrológicas (Placidus, Koch, etc.) que no está implementado aquí. Las interpretaciones son orientativas y educativas.
        </p>
        <p style={{ margin: '0', fontStyle: 'italic', color: 'rgba(255,255,255,0.25)' }}>
          Datos orbitales: JPL/NASA · Efemérides: VSOP87 (planetas), ELP/MPP02 (Luna) · Catálogo estelar: Yale Bright Star Catalogue
        </p>
      </div>

      <button onClick={() => router.push('/menu')} className="btn-responsive"
        onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#fff' }}
        onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)' }}>
        Volver
      </button>
    </main>
  )
}


