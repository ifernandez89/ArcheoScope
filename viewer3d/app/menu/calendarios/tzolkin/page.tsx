'use client'
import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

const GMT = 584283
const SELLOS = [
  { name: 'Imix',    glyph: '🐉', color: '#ef4444', meaning: 'Nacimiento · Nutrición · Ser' },
  { name: 'Ik',      glyph: '🌬️', color: '#a78bfa', meaning: 'Espíritu · Comunicación · Aliento' },
  { name: 'Akbal',   glyph: '🌙', color: '#3b82f6', meaning: 'Abundancia · Intuición · Sueño' },
  { name: 'Kan',     glyph: '🌱', color: '#22c55e', meaning: 'Florecimiento · Conciencia · Objetivo' },
  { name: 'Chicchan',glyph: '🐍', color: '#dc2626', meaning: 'Fuerza Vital · Instinto · Kundalini' },
  { name: 'Cimi',    glyph: '💀', color: '#94a3b8', meaning: 'Muerte · Igualdad · Oportunidad' },
  { name: 'Manik',   glyph: '✋', color: '#3b82f6', meaning: 'Conocimiento · Sanación · Realización' },
  { name: 'Lamat',   glyph: '⭐', color: '#fbbf24', meaning: 'Elegancia · Arte · Belleza' },
  { name: 'Muluc',   glyph: '🌊', color: '#ef4444', meaning: 'Agua Universal · Purificación · Flujo' },
  { name: 'Oc',      glyph: '🐕', color: '#f5f5f5', meaning: 'Amor · Lealtad · Corazón' },
  { name: 'Chuen',   glyph: '🐒', color: '#3b82f6', meaning: 'Magia · Juego · Ilusión' },
  { name: 'Eb',      glyph: '🧑', color: '#fbbf24', meaning: 'Libre Albedrío · Sabiduría · Influencia' },
  { name: 'Ben',     glyph: '🏔️', color: '#ef4444', meaning: 'Espacio · Exploración · Vigilia' },
  { name: 'Ix',      glyph: '🔮', color: '#f5f5f5', meaning: 'Atemporalidad · Receptividad · Jaguar' },
  { name: 'Men',     glyph: '🦅', color: '#3b82f6', meaning: 'Visión · Creatividad · Mente' },
  { name: 'Cib',     glyph: '⚔️', color: '#fbbf24', meaning: 'Inteligencia · Valentía · Cuestionar' },
  { name: 'Caban',   glyph: '🌍', color: '#ef4444', meaning: 'Navegación · Sincronía · Evolución' },
  { name: 'Etznab',  glyph: '🪞', color: '#f5f5f5', meaning: 'Orden Sin Fin · Reflexión · Verdad' },
  { name: 'Cauac',   glyph: '⛈️', color: '#3b82f6', meaning: 'Autogeneración · Energía · Catalización' },
  { name: 'Ahau',    glyph: '☀️', color: '#fbbf24', meaning: 'Fuego Universal · Iluminación · Vida' },
]
const TONOS = ['Magnético','Lunar','Eléctrico','Autoexistente','Entonado','Rítmico','Resonante','Galáctico','Solar','Planetario','Espectral','Cristal','Cósmico']
const HAAB = ['Pop','Wo','Sip','Sotz','Sek','Xul','Yaxkin','Mol','Chen','Yax','Sak','Keh','Mak','Kankin','Muwan','Pax','Kayab','Kumku','Wayeb']

function toJDN(y: number, m: number, d: number) {
  const a = Math.floor((14-m)/12), yy = y+4800-a, mm = m+12*a-3
  return d + Math.floor((153*mm+2)/5) + 365*yy + Math.floor(yy/4) - Math.floor(yy/100) + Math.floor(yy/400) - 32045
}

function calc(date: Date) {
  const jdn = toJDN(date.getFullYear(), date.getMonth()+1, date.getDate())
  const md = jdn - GMT
  const num = ((md + 4) % 13 + 13) % 13 || 13
  const sel = ((md + 19) % 20 + 20) % 20
  const haabDay = ((md + 348) % 365 + 365) % 365
  const hMonth = Math.min(Math.floor(haabDay/20), 18)
  const hDay = haabDay % 20
  let d2 = md
  const lk = d2%20; d2=Math.floor(d2/20); const lu=d2%18; d2=Math.floor(d2/18)
  const lt = d2%20; d2=Math.floor(d2/20); const lka=d2%20; d2=Math.floor(d2/20)
  const kin = ((md%260)+260)%260 || 260

  // ─── RED DE CICLOS CÓSMICOS (Dresden Codex) ───────────────────────────────
  // Ciclo de Venus: 584 días sinódicos
  // Referencia: 0.0.0.0.0 = inicio del ciclo de Venus (fase Estrella de la Mañana)
  const venusCycle = 584
  const venusDay = ((md % venusCycle) + venusCycle) % venusCycle
  let venusPhase = '', venusIcon = ''
  if (venusDay < 236)      { venusPhase = 'Estrella de la Mañana'; venusIcon = '🌅' }
  else if (venusDay < 250) { venusPhase = 'Conjunción Superior';   venusIcon = '☀️' }
  else if (venusDay < 500) { venusPhase = 'Estrella de la Tarde';  venusIcon = '🌆' }
  else                     { venusPhase = 'Conjunción Inferior';   venusIcon = '🌑' }
  const venusProgress = Math.round((venusDay / venusCycle) * 100)

  // Ciclo Lunar: 29.53 días (Tabla de Eclipses del Dresden Codex)
  // Referencia: luna nueva conocida JDN 1507231 (correlación Dresden)
  const lunarCycle = 29.53059
  const lunarDay = ((md % lunarCycle) + lunarCycle) % lunarCycle
  let lunaPhase = '', lunaIcon = ''
  if (lunarDay < 1.85)       { lunaPhase = 'Luna Nueva';       lunaIcon = '🌑' }
  else if (lunarDay < 7.38)  { lunaPhase = 'Creciente';        lunaIcon = '🌒' }
  else if (lunarDay < 13.07) { lunaPhase = 'Cuarto Creciente'; lunaIcon = '🌓' }
  else if (lunarDay < 16.61) { lunaPhase = 'Luna Llena';       lunaIcon = '🌕' }
  else if (lunarDay < 22.15) { lunaPhase = 'Menguante';        lunaIcon = '🌖' }
  else if (lunarDay < 27.84) { lunaPhase = 'Cuarto Menguante'; lunaIcon = '🌗' }
  else                       { lunaPhase = 'Balsámica';        lunaIcon = '🌘' }

  // Temporada de Eclipses: cada 173.31 días (semestre dracónico)
  const eclipseSemester = 173.31
  const eclipseDay = ((md % eclipseSemester) + eclipseSemester) % eclipseSemester
  const inEclipseSeason = eclipseDay < 18 || eclipseDay > 155
  const eclipseProgress = Math.round((eclipseDay / eclipseSemester) * 100)

  // Rueda Calendárica: Tzolk'in (260) × Haab (365) = 18,980 días (~52 años)
  const calendarRound = 18980
  const crDay = ((md % calendarRound) + calendarRound) % calendarRound
  const crYear = Math.floor(crDay / 365)
  const crProgress = Math.round((crDay / calendarRound) * 100)

  // Sincronía Venus-Tzolk'in: 2,920 días = 5 Venus = 8 años solares = 11.2 Tzolk'in
  const venusTzolkin = 2920
  const vtDay = ((md % venusTzolkin) + venusTzolkin) % venusTzolkin
  const vtProgress = Math.round((vtDay / venusTzolkin) * 100)

  return {
    jdn, md, num, sel, haab: { day: hDay, month: hMonth },
    lc: { b: d2, ka: lka, t: lt, u: lu, k: lk }, kin,
    venus: { day: venusDay, phase: venusPhase, icon: venusIcon, progress: venusProgress },
    luna: { day: lunarDay, phase: lunaPhase, icon: lunaIcon },
    eclipse: { inSeason: inEclipseSeason, day: eclipseDay, progress: eclipseProgress },
    calRound: { day: crDay, year: crYear, progress: crProgress },
    venusTzolkin: { day: vtDay, progress: vtProgress }
  }
}

export default function TzolkinPage() {
  const router = useRouter()
  const [date, setDate] = useState(new Date())
  const r = useMemo(() => calc(date), [date])
  const sello = SELLOS[r.sel]
  const tono = TONOS[r.num - 1]

  return (
    <main style={{ width:'100vw', minHeight:'100vh', display:'flex', flexDirection:'column', alignItems:'center', background:'linear-gradient(180deg,#0a0a1a,#1a0a2e,#0a0a1a)', padding:'40px 20px', color:'#fff', overflowY: 'auto' }}>
      <div style={{ fontSize:'18px', color:'rgba(255,255,255,0.4)', letterSpacing:'2px', marginBottom:'12px', cursor:'pointer', textAlign: 'center' }} onClick={() => router.push('/menu/calendarios')}>← CALENDARIOS ANTIGUOS</div>
      <h1 className="title-responsive" style={{ color:'#fbbf24' }}>TZOLK'IN CLÁSICO</h1>
      <p className="subtitle-responsive" style={{ marginBottom:'8px' }}>Correlación GMT 584283 · Sistema Arqueológico Maya</p>
      <p className="text-responsive" style={{ marginBottom:'24px', color:'rgba(255,255,255,0.3)' }}>21 dic 2012 = 4 Ahau ✓ · Válido para cualquier fecha histórica</p>

      <input type="date" value={date.toISOString().split('T')[0]} onChange={e => setDate(new Date(e.target.value+'T12:00:00'))}
        style={{ padding:'10px 20px', fontSize:'16px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(251,191,36,0.3)', borderRadius:'8px', color:'#fbbf24', marginBottom:'24px', cursor:'pointer' }} />

      {/* Cuenta Larga */}
      <div className="info-card" style={{ background:'rgba(251,191,36,0.04)', border:'1px solid rgba(251,191,36,0.15)' }}>
        <div style={{ fontSize:'14px', color:'rgba(255,255,255,0.4)', letterSpacing:'2px', marginBottom:'6px' }}>CUENTA LARGA</div>
        <div style={{ fontSize:'clamp(24px, 7vw, 34px)', fontWeight:'bold', color:'#fbbf24', fontFamily:'monospace', letterSpacing:'4px' }}>
          {r.lc.b}.{r.lc.ka}.{r.lc.t}.{r.lc.u}.{r.lc.k}
        </div>
        <div style={{ fontSize:'14px', color:'rgba(255,255,255,0.4)', marginTop:'4px' }}>JDN: {r.jdn} · Días Maya: {r.md.toLocaleString()}</div>
      </div>

      {/* Kin del día */}
      <div className="info-card" style={{ background:'rgba(251,191,36,0.06)', border:'1px solid rgba(251,191,36,0.25)', padding:'28px' }}>
        <div style={{ fontSize:'clamp(40px, 10vw, 52px)', marginBottom:'4px' }}>{sello.glyph}</div>
        <div style={{ fontSize:'clamp(12px, 2.5vw, 15px)', color:'rgba(255,255,255,0.4)', letterSpacing:'2px', marginBottom:'4px' }}>ENERGÍA DEL DÍA · KIN {r.kin}</div>
        <h2 style={{ color:'#fbbf24' }}>{r.num} {sello.name}</h2>
        <div style={{ fontSize:'clamp(20px, 4vw, 23px)', color:'rgba(255,255,255,0.8)', marginBottom:'8px' }}>Tono {tono}</div>
        <div style={{ fontSize:'clamp(17px, 3.5vw, 20px)', color:'rgba(255,255,255,0.6)' }}>{sello.meaning}</div>
      </div>

      {/* Tzolkin + Haab */}
      <div style={{ maxWidth:'min(500px, 95vw)', width:'100%', display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(min(180px, 100%), 1fr))', gap:'12px', marginBottom:'14px' }}>
        <div style={{ padding:'18px', background:'rgba(167,139,250,0.08)', border:'1px solid rgba(167,139,250,0.25)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'clamp(12px, 2.5vw, 15px)', color:'rgba(255,255,255,0.4)', letterSpacing:'1px', marginBottom:'6px' }}>TZOLK'IN</div>
          <div style={{ fontSize:'clamp(24px, 6vw, 34px)', fontWeight:'bold', color:'#a78bfa' }}>{r.num}</div>
          <div style={{ fontSize:'clamp(16px, 3.5vw, 20px)', color:'#fff' }}>{tono}</div>
          <div style={{ fontSize:'clamp(16px, 3.5vw, 18px)', color:'rgba(255,255,255,0.5)', marginTop:'4px' }}>{sello.name}</div>
        </div>
        <div style={{ padding:'18px', background:'rgba(34,197,94,0.08)', border:'1px solid rgba(34,197,94,0.25)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'clamp(12px, 2.5vw, 15px)', color:'rgba(255,255,255,0.4)', letterSpacing:'1px', marginBottom:'6px' }}>HAAB (365 DÍAS)</div>
          <div style={{ fontSize:'clamp(22px, 5.5vw, 30px)', fontWeight:'bold', color:'#22c55e' }}>{r.haab.day} {HAAB[r.haab.month]}</div>
          <div style={{ fontSize:'clamp(16px, 3.5vw, 18px)', color:'rgba(255,255,255,0.5)', marginTop:'4px' }}>Mes {r.haab.month+1} de 19</div>
        </div>
      </div>

      {/* Referencia */}
      <div className="info-card" style={{ padding:'14px', background:'rgba(255,255,255,0.02)', border:'1px solid rgba(255,255,255,0.06)' }}>
        <div className="text-responsive" style={{ lineHeight:'1.8' }}>
          Correlación GMT: <strong style={{ color:'rgba(255,255,255,0.6)' }}>584283</strong> · Inicio: <strong style={{ color:'rgba(255,255,255,0.6)' }}>11 ago 3114 a.C.</strong><br/>
          0.0.0.0.0 = 4 Ahau 8 Kumku · 1 Baktun = 144,000 días
        </div>
      </div>

      {/* Ciclos astronómicos mayas */}
      <div className="info-card" style={{ background:'rgba(251,191,36,0.04)', border:'1px solid rgba(251,191,36,0.15)' }}>
        <div style={{ fontSize:'clamp(13px, 2.5vw, 16px)', color:'rgba(255,255,255,0.4)', letterSpacing:'2px', marginBottom:'12px', textAlign:'center' }}>CICLOS ASTRONÓMICOS MAYAS</div>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(min(180px, 100%), 1fr))', gap:'8px' }}>
          {[
            ['📅 Tzolk\'in', '260 días · 20 sellos × 13 tonos'],
            ['🌞 Haab', '365 días · 18 meses × 20 + 5 Wayeb'],
            ['☀️ Ciclo Solar', '365.25 días · Solsticios y equinoccios'],
            ['🌙 Ciclo Lunar', '29.53 días · Fases lunares'],
            ['⭐ Venus', '584 días · Ciclo sinódico completo'],
            ['🌀 Precesión', '25,772 años · Ciclo axial terrestre'],
          ].map(([k, v]) => (
            <div key={String(k)} style={{ padding:'8px', background:'rgba(255,255,255,0.03)', borderRadius:'6px' }}>
              <div style={{ color:'#fbbf24', fontSize:'clamp(17px, 4vw, 19px)', marginBottom:'2px' }}>{k}</div>
              <div style={{ color:'rgba(255,255,255,0.5)', fontSize:'clamp(15px, 3.5vw, 17px)' }}>{v}</div>
            </div>
          ))}
        </div>
      </div>

      {/* RED DE CICLOS CÓSMICOS — Sistema de Navegación Astronómica */}
      <div className="info-card" style={{ background:'rgba(56,189,248,0.05)', border:'1px solid rgba(56,189,248,0.2)' }}>
        <div style={{ fontSize:'clamp(12px, 2.5vw, 15px)', color:'rgba(255,255,255,0.4)', letterSpacing:'2px', marginBottom:'16px', textAlign:'center' }}>
          RED DE CICLOS CÓSMICOS · SISTEMA DE NAVEGACIÓN ASTRONÓMICA MAYA
        </div>

        {/* Venus */}
        <div style={{ marginBottom:'12px', padding:'12px', background:'rgba(244,114,182,0.08)', borderRadius:'8px' }}>
          <div className="cycle-header" style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'8px', flexWrap: 'wrap', gap: '4px' }}>
            <span style={{ fontSize:'clamp(14px, 3.5vw, 17px)', color:'#f472b6', fontWeight:'bold' }}>
              {r.venus.icon} Venus · Ciclo 584 días
            </span>
            <span style={{ fontSize:'clamp(15px, 3.5vw, 17px)', color:'rgba(255,255,255,0.5)' }}>Día {Math.round(r.venus.day)} · {r.venus.progress}%</span>
          </div>
          <div style={{ height:'4px', background:'rgba(255,255,255,0.1)', borderRadius:'2px', marginBottom:'8px' }}>
            <div style={{ height:'100%', width:`${r.venus.progress}%`, background:'#f472b6', borderRadius:'2px', transition:'width 0.3s' }} />
          </div>
          <div style={{ fontSize:'clamp(17px, 4vw, 19px)', color:'rgba(255,255,255,0.7)', textAlign:'left' }}>{r.venus.phase}</div>
        </div>

        {/* Luna */}
        <div style={{ marginBottom:'12px', padding:'12px', background:'rgba(226,232,240,0.06)', borderRadius:'8px' }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'6px' }}>
            <span style={{ fontSize:'clamp(14px, 3.5vw, 17px)', color:'#e2e8f0', fontWeight:'bold' }}>
              {r.luna.icon} Luna · Ciclo 29.53 días
            </span>
            <span style={{ fontSize:'clamp(15px, 3.5vw, 17px)', color:'rgba(255,255,255,0.5)' }}>Día {r.luna.day.toFixed(1)}</span>
          </div>
          <div style={{ fontSize:'clamp(17px, 4vw, 19px)', color:'rgba(255,255,255,0.7)', textAlign:'left' }}>{r.luna.phase}</div>
        </div>

        {/* Temporada de Eclipses */}
        <div style={{ marginBottom:'12px', padding:'12px', background: r.eclipse.inSeason ? 'rgba(239,68,68,0.12)' : 'rgba(255,255,255,0.04)', border: r.eclipse.inSeason ? '1px solid rgba(239,68,68,0.4)' : '1px solid transparent', borderRadius:'8px' }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'6px' }}>
            <span style={{ fontSize:'clamp(13px, 3vw, 16px)', color: r.eclipse.inSeason ? '#ef4444' : 'rgba(255,255,255,0.5)', fontWeight:'bold' }}>
              🌑 Temporada de Eclipses · 173.31 días
            </span>
            <span style={{ fontSize:'clamp(12px, 2.5vw, 15px)', color: r.eclipse.inSeason ? '#ef4444' : 'rgba(255,255,255,0.4)' }}>
              {r.eclipse.inSeason ? '⚠️ ACTIVA' : `Día ${Math.round(r.eclipse.day)}`}
            </span>
          </div>
          <div style={{ height:'4px', background:'rgba(255,255,255,0.1)', borderRadius:'2px' }}>
            <div style={{ height:'100%', width:`${r.eclipse.progress}%`, background: r.eclipse.inSeason ? '#ef4444' : 'rgba(255,255,255,0.3)', borderRadius:'2px' }} />
          </div>
        </div>

        {/* Rueda Calendárica */}
        <div style={{ marginBottom:'12px', padding:'12px', background:'rgba(251,191,36,0.06)', borderRadius:'8px' }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'6px' }}>
            <span style={{ fontSize:'clamp(13px, 3vw, 16px)', color:'#fbbf24', fontWeight:'bold' }}>🔄 Rueda Calendárica</span>
            <span style={{ fontSize:'clamp(12px, 2.5vw, 15px)', color:'rgba(255,255,255,0.5)' }}>Año {r.calRound.year + 1} de 52</span>
          </div>
          <div style={{ height:'4px', background:'rgba(255,255,255,0.1)', borderRadius:'2px' }}>
            <div style={{ height:'100%', width:`${r.calRound.progress}%`, background:'#fbbf24', borderRadius:'2px' }} />
          </div>
        </div>

        {/* Sincronía Venus-Tzolk'in */}
        <div style={{ padding:'12px', background:'rgba(167,139,250,0.06)', borderRadius:'8px' }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'6px' }}>
            <span style={{ fontSize:'clamp(13px, 3vw, 16px)', color:'#a78bfa', fontWeight:'bold' }}>⭐ Sincronía Venus-Solar</span>
            <span style={{ fontSize:'clamp(12px, 2.5vw, 15px)', color:'rgba(255,255,255,0.5)' }}>{r.venusTzolkin.progress}%</span>
          </div>
          <div style={{ height:'4px', background:'rgba(255,255,255,0.1)', borderRadius:'2px' }}>
            <div style={{ height:'100%', width:`${r.venusTzolkin.progress}%`, background:'#a78bfa', borderRadius:'2px' }} />
          </div>
        </div>
      </div>

      {/* Venus y el Dresden Codex */}
      <div className="info-card" style={{ background:'rgba(244,114,182,0.05)', border:'1px solid rgba(244,114,182,0.2)' }}>
        <div style={{ fontSize:'clamp(11px, 2.5vw, 14px)', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'10px', textAlign:'center' }}>VENUS Y EL DRESDEN CODEX</div>
        <div className="text-responsive" style={{ color:'rgba(255,255,255,0.6)', lineHeight:'1.8', textAlign:'left' }}>
          Venus aparece como <strong style={{ color:'#f472b6' }}>estrella de la mañana</strong> (Chak Ek') y <strong style={{ color:'#f472b6' }}>estrella de la tarde</strong>. Los mayas registraron su ciclo sinódico de <strong style={{ color:'#f472b6' }}>584 días</strong> con precisión extraordinaria.<br/><br/>
          El <strong style={{ color:'#f472b6' }}>Códice de Dresde</strong> contiene tablas completas del planeta Venus, asociando sus fases con <strong style={{ color:'rgba(255,255,255,0.7)' }}>guerra, rituales y augurios</strong>.
        </div>
      </div>

      <button onClick={() => router.push('/menu/calendarios')} className="btn-responsive"
        onMouseEnter={e => e.currentTarget.style.borderColor='#fff'} onMouseLeave={e => e.currentTarget.style.borderColor='rgba(255,255,255,0.3)'}>
        Volver
      </button>
    </main>
  )
}
