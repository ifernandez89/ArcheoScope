'use client'
import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

// ═══════════════════════════════════════════════════════════════════════════════
// CALENDARIO SEXAGESIMAL MESOPOTÁMICO (Babilonia / Sumer)
// Base 60 — el sistema que heredamos para tiempo, ángulos y coordenadas celestes
// ═══════════════════════════════════════════════════════════════════════════════

// 6 ciclos de 60 días = 360 días (año idealizado babilónico)
// Cada ciclo tiene nombre de una deidad/planeta babilónico
const CICLOS = [
  { num: 1, name: 'Shamash',  glyph: '☀️', planet: 'Sol',     color: '#fbbf24', meaning: 'Dios del Sol · Justicia · Verdad · Luz divina' },
  { num: 2, name: 'Sin',      glyph: '🌙', planet: 'Luna',    color: '#e2e8f0', meaning: 'Dios de la Luna · Sabiduría · Ciclos · Tiempo' },
  { num: 3, name: 'Nergal',   glyph: '🔴', planet: 'Marte',   color: '#ef4444', meaning: 'Dios de la Guerra · Fuego · Transformación' },
  { num: 4, name: 'Nabu',     glyph: '✍️', planet: 'Mercurio',color: '#a3e635', meaning: 'Dios de la Escritura · Conocimiento · Destino' },
  { num: 5, name: 'Marduk',   glyph: '⚡', planet: 'Júpiter', color: '#a78bfa', meaning: 'Rey de los Dioses · Expansión · Orden cósmico' },
  { num: 6, name: 'Ishtar',   glyph: '⭐', planet: 'Venus',   color: '#f472b6', meaning: 'Diosa del Amor · Belleza · Fertilidad · Guerra' },
]

// 60 días del ciclo divididos en 6 semanas de 10 días (décadas)
const DECADAS = ['Primera', 'Segunda', 'Tercera', 'Cuarta', 'Quinta', 'Sexta']

// Coordenadas celestes en formato sexagesimal (RA/Dec de estrellas clave)
const ESTRELLAS_BABILONICAS = [
  { name: 'Sirio (Kakkab)',      ra: '06h 45m 08.9s', dec: '-16° 42\' 58"', mag: -1.46, note: 'La más brillante — marcaba el año nuevo en Babilonia' },
  { name: 'Aldebarán (Pidnu)',   ra: '04h 35m 55.2s', dec: '+16° 30\' 33"', mag:  0.87, note: 'Ojo del Toro — equinoccio de primavera ~3000 a.C.' },
  { name: 'Régulo (Sharru)',     ra: '10h 08m 22.3s', dec: '+11° 58\' 02"', mag:  1.35, note: 'El Rey — corazón del León, estrella real' },
  { name: 'Antares (Biru)',      ra: '16h 29m 24.4s', dec: '-26° 25\' 55"', mag:  1.06, note: 'Corazón del Escorpión — solsticio de verano ~3000 a.C.' },
  { name: 'Fomalhaut (Lumasi)',  ra: '22h 57m 39.0s', dec: '-29° 37\' 20"', mag:  1.16, note: 'Boca del Pez — equinoccio de otoño ~3000 a.C.' },
]

/**
 * Calcular posición en el calendario sexagesimal babilónico
 * Referencia: 1 enero 3000 a.C. = día 0 del ciclo 1
 * El año babilónico tenía 360 días + 5 días intercalares (Epagómenos)
 */
function calcSexagesimal(date: Date) {
  // Días desde referencia aproximada (1 enero 3000 a.C. ≈ JDN 625307)
  const JDN_REF = 625307
  const y = date.getFullYear(), m = date.getMonth()+1, d = date.getDate()
  const a = Math.floor((14-m)/12), yy = y+4800-a, mm = m+12*a-3
  const jdn = d + Math.floor((153*mm+2)/5) + 365*yy + Math.floor(yy/4) - Math.floor(yy/100) + Math.floor(yy/400) - 32045
  const totalDays = jdn - JDN_REF

  // Año babilónico: 360 días + 5 epagómenos
  const yearLen = 365
  const yearPos = ((totalDays % yearLen) + yearLen) % yearLen
  const babilYear = Math.floor(totalDays / yearLen)

  // Posición en el ciclo de 360 días
  const dayOf360 = yearPos % 360
  const cicloIdx = Math.floor(dayOf360 / 60) % 6
  const dayInCiclo = dayOf360 % 60
  const decadaIdx = Math.floor(dayInCiclo / 10)
  const dayInDecada = dayInCiclo % 10 + 1

  // Epagómenos (5 días fuera del tiempo)
  const isEpagomenos = yearPos >= 360

  // Hora en base 60
  const now = new Date()
  const totalSecs = now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds()
  const beru = Math.floor(totalSecs / 7200) // 1 beru = 2 horas
  const ush = Math.floor((totalSecs % 7200) / 60) // 1 ush = 1 minuto
  const ninda = totalSecs % 60 // 1 ninda = 1 segundo

  // Ángulo solar en base 60 (azimut)
  const azimutSexag = {
    grados: Math.floor(0), // placeholder — se podría conectar con solarState
    minutos: 0,
    segundos: 0
  }

  return { cicloIdx, dayInCiclo, dayInDecada, decadaIdx, isEpagomenos, babilYear, dayOf360, beru, ush, ninda, yearPos }
}

/**
 * Convertir decimal a notación sexagesimal (grados°minutos'segundos")
 */
function toSexagesimal(decimal: number): string {
  const abs = Math.abs(decimal)
  const deg = Math.floor(abs)
  const minFull = (abs - deg) * 60
  const min = Math.floor(minFull)
  const sec = Math.floor((minFull - min) * 60)
  const sign = decimal < 0 ? '-' : '+'
  return `${sign}${deg}° ${min}' ${sec}"`
}

export default function SexagesimalPage() {
  const router = useRouter()
  const [date, setDate] = useState(new Date())
  const r = useMemo(() => calcSexagesimal(date), [date])
  const ciclo = CICLOS[r.cicloIdx]

  return (
    <main style={{ width:'100vw', minHeight:'100vh', display:'flex', flexDirection:'column', alignItems:'center', background:'linear-gradient(180deg,#0a0a1a,#1a0a2e,#0a0a1a)', padding:'40px 20px', color:'#fff' }}>
      <div style={{ fontSize:'12px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'4px', cursor:'pointer' }} onClick={() => router.push('/menu/calendarios')}>← CALENDARIOS ANTIGUOS</div>
      <h1 style={{ fontSize:'38px', marginBottom:'4px', letterSpacing:'5px', fontFamily:'Archeoscope, serif', color: '#38bdf8' }}>CALENDARIO BABILÓNICO</h1>
      <p style={{ fontSize:'12px', color:'rgba(255,255,255,0.3)', marginBottom:'6px', letterSpacing:'2px' }}>Sistema Sexagesimal · Mesopotamia · Base 60</p>
      <p style={{ fontSize:'11px', color:'rgba(255,255,255,0.2)', marginBottom:'24px' }}>El origen del tiempo moderno: 60 min/hora · 360°/círculo · RA/Dec estelar</p>

      <input type="date" value={date.toISOString().split('T')[0]} onChange={e => setDate(new Date(e.target.value+'T12:00:00'))}
        style={{ padding:'10px 20px', fontSize:'16px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(56,189,248,0.3)', borderRadius:'8px', color:'#38bdf8', marginBottom:'24px', cursor:'pointer' }} />

      {/* Ciclo planetario */}
      <div style={{ maxWidth:'520px', width:'100%', padding:'28px', background:`rgba(56,189,248,0.05)`, border:'1px solid rgba(56,189,248,0.2)', borderRadius:'16px', textAlign:'center', marginBottom:'14px' }}>
        <div style={{ fontSize:'52px', marginBottom:'4px' }}>{ciclo.glyph}</div>
        <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'4px' }}>
          {r.isEpagomenos ? 'DÍAS EPAGÓMENOS (FUERA DEL TIEMPO)' : `CICLO ${ciclo.num} DE 6 · DÍA ${r.dayInCiclo + 1} DE 60`}
        </div>
        <div style={{ fontSize:'32px', fontWeight:'bold', color: ciclo.color, fontFamily:'Archeoscope, serif', marginBottom:'4px' }}>
          {r.isEpagomenos ? 'Epagómenos' : ciclo.name}
        </div>
        <div style={{ fontSize:'16px', color:'rgba(255,255,255,0.6)', marginBottom:'8px' }}>
          {r.isEpagomenos ? '5 días sagrados fuera del calendario' : `Planeta: ${ciclo.planet}`}
        </div>
        {!r.isEpagomenos && <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.5)' }}>{ciclo.meaning}</div>}
      </div>

      {/* Posición en el año + Décadas */}
      {!r.isEpagomenos && (
        <div style={{ maxWidth:'520px', width:'100%', display:'grid', gridTemplateColumns:'1fr 1fr', gap:'12px', marginBottom:'14px' }}>
          <div style={{ padding:'18px', background:'rgba(56,189,248,0.06)', border:'1px solid rgba(56,189,248,0.2)', borderRadius:'12px', textAlign:'center' }}>
            <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'1px', marginBottom:'6px' }}>DÍA DEL AÑO (360)</div>
            <div style={{ fontSize:'32px', fontWeight:'bold', color:'#38bdf8' }}>{r.dayOf360 + 1}</div>
            <div style={{ fontSize:'12px', color:'rgba(255,255,255,0.4)', marginTop:'4px' }}>de 360 días</div>
          </div>
          <div style={{ padding:'18px', background:'rgba(56,189,248,0.06)', border:'1px solid rgba(56,189,248,0.2)', borderRadius:'12px', textAlign:'center' }}>
            <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'1px', marginBottom:'6px' }}>DÉCADA</div>
            <div style={{ fontSize:'22px', fontWeight:'bold', color:'#38bdf8' }}>{DECADAS[r.decadaIdx]}</div>
            <div style={{ fontSize:'12px', color:'rgba(255,255,255,0.4)', marginTop:'4px' }}>Día {r.dayInDecada} de 10</div>
          </div>
        </div>
      )}

      {/* Hora en base 60 */}
      <div style={{ maxWidth:'520px', width:'100%', padding:'20px', background:'rgba(251,191,36,0.05)', border:'1px solid rgba(251,191,36,0.2)', borderRadius:'12px', marginBottom:'14px' }}>
        <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'10px', textAlign:'center' }}>TIEMPO BABILÓNICO (BASE 60)</div>
        <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:'10px', textAlign:'center' }}>
          <div>
            <div style={{ fontSize:'28px', fontWeight:'bold', color:'#fbbf24' }}>{r.beru}</div>
            <div style={{ fontSize:'11px', color:'rgba(255,255,255,0.4)' }}>Beru</div>
            <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.25)' }}>1 beru = 2h</div>
          </div>
          <div>
            <div style={{ fontSize:'28px', fontWeight:'bold', color:'#fbbf24' }}>{r.ush}</div>
            <div style={{ fontSize:'11px', color:'rgba(255,255,255,0.4)' }}>Uš</div>
            <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.25)' }}>1 uš = 1min</div>
          </div>
          <div>
            <div style={{ fontSize:'28px', fontWeight:'bold', color:'#fbbf24' }}>{r.ninda}</div>
            <div style={{ fontSize:'11px', color:'rgba(255,255,255,0.4)' }}>Ninda</div>
            <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.25)' }}>1 ninda = 1s</div>
          </div>
        </div>
      </div>

      {/* Coordenadas celestes en base 60 */}
      <div style={{ maxWidth:'520px', width:'100%', padding:'20px', background:'rgba(167,139,250,0.05)', border:'1px solid rgba(167,139,250,0.2)', borderRadius:'12px', marginBottom:'14px' }}>
        <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'12px', textAlign:'center' }}>
          ESTRELLAS BABILÓNICAS — COORDENADAS SEXAGESIMALES (RA/Dec)
        </div>
        {ESTRELLAS_BABILONICAS.map((s, i) => (
          <div key={i} style={{ padding:'10px 0', borderBottom: i < ESTRELLAS_BABILONICAS.length-1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
            <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start' }}>
              <div>
                <span style={{ color:'#a78bfa', fontWeight:'bold', fontSize:'13px' }}>{s.name}</span>
                <span style={{ color:'rgba(255,255,255,0.3)', fontSize:'11px', marginLeft:'8px' }}>mag {s.mag}</span>
              </div>
              <div style={{ textAlign:'right', fontSize:'11px', fontFamily:'monospace', color:'#38bdf8' }}>
                <div>RA: {s.ra}</div>
                <div>Dec: {s.dec}</div>
              </div>
            </div>
            <div style={{ fontSize:'11px', color:'rgba(255,255,255,0.35)', marginTop:'3px' }}>{s.note}</div>
          </div>
        ))}
      </div>

      {/* Herencia del sistema */}
      <div style={{ maxWidth:'520px', width:'100%', padding:'16px', background:'rgba(255,255,255,0.02)', border:'1px solid rgba(255,255,255,0.06)', borderRadius:'8px', marginBottom:'28px' }}>
        <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'10px', textAlign:'center' }}>HERENCIA DEL SISTEMA SEXAGESIMAL</div>
        <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'8px', fontSize:'12px' }}>
          {[
            ['⏰ Tiempo', '60 min/hora · 60 seg/min'],
            ['🔵 Ángulos', '360° = 6 × 60 · 1° = 60\''],
            ['🌟 RA Estelar', 'horas · minutos · segundos'],
            ['📐 Dec Estelar', 'grados · arcmin · arcsec'],
            ['🗺️ Geografía', 'Latitud/Longitud en °\' "'],
            ['🏛️ Origen', 'Sumer ~3000 a.C. · Babilonia'],
          ].map(([k, v]) => (
            <div key={k} style={{ padding:'8px', background:'rgba(255,255,255,0.03)', borderRadius:'6px' }}>
              <div style={{ color:'#38bdf8', fontSize:'11px', marginBottom:'2px' }}>{k}</div>
              <div style={{ color:'rgba(255,255,255,0.5)', fontSize:'11px' }}>{v}</div>
            </div>
          ))}
        </div>
      </div>

      <button onClick={() => router.push('/menu/calendarios')} style={{ padding:'14px 50px', fontSize:'18px', color:'#fff', background:'transparent', border:'2px solid rgba(255,255,255,0.3)', borderRadius:'8px', cursor:'pointer', letterSpacing:'2px', textTransform:'uppercase', transition:'all 0.3s' }}
        onMouseEnter={e => e.currentTarget.style.borderColor='#fff'} onMouseLeave={e => e.currentTarget.style.borderColor='rgba(255,255,255,0.3)'}>
        Volver
      </button>
    </main>
  )
}
