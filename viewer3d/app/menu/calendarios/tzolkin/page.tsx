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
  // Offset correcto: día 0.0.0.0.0 = 4 Ahau → num offset=4, sello offset=19
  const num = ((md + 4) % 13 + 13) % 13 || 13
  const sel = ((md + 19) % 20 + 20) % 20
  const haabDay = ((md + 348) % 365 + 365) % 365
  const hMonth = Math.min(Math.floor(haabDay/20), 18)
  const hDay = haabDay % 20
  let d2 = md
  const lk = d2%20; d2=Math.floor(d2/20); const lu=d2%18; d2=Math.floor(d2/18)
  const lt = d2%20; d2=Math.floor(d2/20); const lka=d2%20; d2=Math.floor(d2/20)
  const kin = ((md%260)+260)%260 || 260
  return { jdn, md, num, sel, haab: { day: hDay, month: hMonth }, lc: { b: d2, ka: lka, t: lt, u: lu, k: lk }, kin }
}

export default function TzolkinPage() {
  const router = useRouter()
  const [date, setDate] = useState(new Date())
  const r = useMemo(() => calc(date), [date])
  const sello = SELLOS[r.sel]
  const tono = TONOS[r.num - 1]

  return (
    <main style={{ width:'100vw', minHeight:'100vh', display:'flex', flexDirection:'column', alignItems:'center', background:'linear-gradient(180deg,#0a0a1a,#1a0a2e,#0a0a1a)', padding:'40px 20px', color:'#fff' }}>
      <div style={{ fontSize:'12px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'4px', cursor:'pointer' }} onClick={() => router.push('/menu/calendarios')}>← CALENDARIOS ANTIGUOS</div>
      <h1 style={{ fontSize:'42px', marginBottom:'4px', letterSpacing:'6px', fontFamily:'Archeoscope, serif', color:'#fbbf24' }}>TZOLK'IN CLÁSICO</h1>
      <p style={{ fontSize:'12px', color:'rgba(255,255,255,0.3)', marginBottom:'6px', letterSpacing:'2px' }}>Correlación GMT 584283 · Sistema Arqueológico Maya</p>
      <p style={{ fontSize:'11px', color:'rgba(255,255,255,0.2)', marginBottom:'24px' }}>21 dic 2012 = 4 Ahau ✓ · Válido para cualquier fecha histórica</p>

      <input type="date" value={date.toISOString().split('T')[0]} onChange={e => setDate(new Date(e.target.value+'T12:00:00'))}
        style={{ padding:'10px 20px', fontSize:'16px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(251,191,36,0.3)', borderRadius:'8px', color:'#fbbf24', marginBottom:'24px', cursor:'pointer' }} />

      {/* Cuenta Larga */}
      <div style={{ maxWidth:'500px', width:'100%', padding:'18px', background:'rgba(251,191,36,0.04)', border:'1px solid rgba(251,191,36,0.15)', borderRadius:'12px', textAlign:'center', marginBottom:'14px' }}>
        <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'6px' }}>CUENTA LARGA</div>
        <div style={{ fontSize:'34px', fontWeight:'bold', color:'#fbbf24', fontFamily:'monospace', letterSpacing:'4px' }}>
          {r.lc.b}.{r.lc.ka}.{r.lc.t}.{r.lc.u}.{r.lc.k}
        </div>
        <div style={{ fontSize:'11px', color:'rgba(255,255,255,0.25)', marginTop:'4px' }}>JDN: {r.jdn} · Días Maya: {r.md.toLocaleString()}</div>
      </div>

      {/* Kin del día */}
      <div style={{ maxWidth:'500px', width:'100%', padding:'28px', background:'rgba(251,191,36,0.06)', border:'1px solid rgba(251,191,36,0.25)', borderRadius:'16px', textAlign:'center', marginBottom:'14px' }}>
        <div style={{ fontSize:'52px', marginBottom:'4px' }}>{sello.glyph}</div>
        <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'4px' }}>ENERGÍA DEL DÍA · KIN {r.kin}</div>
        <div style={{ fontSize:'32px', fontWeight:'bold', color:'#fbbf24', fontFamily:'Archeoscope, serif', marginBottom:'4px' }}>{r.num} {sello.name}</div>
        <div style={{ fontSize:'16px', color:'rgba(255,255,255,0.7)', marginBottom:'8px' }}>Tono {tono}</div>
        <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.5)' }}>{sello.meaning}</div>
      </div>

      {/* Tzolkin + Haab */}
      <div style={{ maxWidth:'500px', width:'100%', display:'grid', gridTemplateColumns:'1fr 1fr', gap:'12px', marginBottom:'14px' }}>
        <div style={{ padding:'18px', background:'rgba(167,139,250,0.08)', border:'1px solid rgba(167,139,250,0.25)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'1px', marginBottom:'6px' }}>TZOLK'IN</div>
          <div style={{ fontSize:'28px', fontWeight:'bold', color:'#a78bfa' }}>{r.num}</div>
          <div style={{ fontSize:'14px', color:'#fff' }}>{tono}</div>
          <div style={{ fontSize:'12px', color:'rgba(255,255,255,0.4)', marginTop:'4px' }}>{sello.name}</div>
        </div>
        <div style={{ padding:'18px', background:'rgba(34,197,94,0.08)', border:'1px solid rgba(34,197,94,0.25)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'1px', marginBottom:'6px' }}>HAAB (365 DÍAS)</div>
          <div style={{ fontSize:'28px', fontWeight:'bold', color:'#22c55e' }}>{r.haab.day} {HAAB[r.haab.month]}</div>
          <div style={{ fontSize:'12px', color:'rgba(255,255,255,0.4)', marginTop:'4px' }}>Mes {r.haab.month+1} de 19</div>
        </div>
      </div>

      {/* Referencia */}
      <div style={{ maxWidth:'500px', width:'100%', padding:'14px', background:'rgba(255,255,255,0.02)', border:'1px solid rgba(255,255,255,0.06)', borderRadius:'8px', marginBottom:'28px', textAlign:'center' }}>
        <div style={{ fontSize:'11px', color:'rgba(255,255,255,0.3)', lineHeight:'1.8' }}>
          Correlación GMT: <strong style={{ color:'rgba(255,255,255,0.5)' }}>584283</strong> · Inicio: <strong style={{ color:'rgba(255,255,255,0.5)' }}>11 ago 3114 a.C.</strong><br/>
          0.0.0.0.0 = 4 Ahau 8 Kumku · 1 Baktun = 144,000 días
        </div>
      </div>

      <button onClick={() => router.push('/menu/calendarios')} style={{ padding:'14px 50px', fontSize:'18px', color:'#fff', background:'transparent', border:'2px solid rgba(255,255,255,0.3)', borderRadius:'8px', cursor:'pointer', letterSpacing:'2px', textTransform:'uppercase', transition:'all 0.3s' }}
        onMouseEnter={e => e.currentTarget.style.borderColor='#fff'} onMouseLeave={e => e.currentTarget.style.borderColor='rgba(255,255,255,0.3)'}>
        Volver
      </button>
    </main>
  )
}
