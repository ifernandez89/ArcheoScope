'use client'
import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

const SELLOS = [
  { name: 'Dragón',    glyph: '🐉', color: '#ef4444', meaning: 'Nacimiento · Nutrición · Ser' },
  { name: 'Viento',    glyph: '🌬️', color: '#a78bfa', meaning: 'Espíritu · Comunicación · Aliento' },
  { name: 'Noche',     glyph: '🌙', color: '#3b82f6', meaning: 'Abundancia · Intuición · Sueño' },
  { name: 'Semilla',   glyph: '🌱', color: '#22c55e', meaning: 'Florecimiento · Conciencia · Objetivo' },
  { name: 'Serpiente', glyph: '🐍', color: '#dc2626', meaning: 'Fuerza Vital · Instinto · Kundalini' },
  { name: 'Enlazador', glyph: '💀', color: '#94a3b8', meaning: 'Muerte · Igualdad · Oportunidad' },
  { name: 'Mano',      glyph: '✋', color: '#3b82f6', meaning: 'Conocimiento · Sanación · Realización' },
  { name: 'Estrella',  glyph: '⭐', color: '#fbbf24', meaning: 'Elegancia · Arte · Belleza' },
  { name: 'Luna',      glyph: '🌊', color: '#ef4444', meaning: 'Agua Universal · Purificación · Flujo' },
  { name: 'Perro',     glyph: '🐕', color: '#f5f5f5', meaning: 'Amor · Lealtad · Corazón' },
  { name: 'Mono',      glyph: '🐒', color: '#3b82f6', meaning: 'Magia · Juego · Ilusión' },
  { name: 'Humano',    glyph: '🧑', color: '#fbbf24', meaning: 'Libre Albedrío · Sabiduría · Influencia' },
  { name: 'Caminante', glyph: '🏔️', color: '#ef4444', meaning: 'Espacio · Exploración · Vigilia' },
  { name: 'Mago',      glyph: '🔮', color: '#f5f5f5', meaning: 'Atemporalidad · Receptividad · Jaguar' },
  { name: 'Águila',    glyph: '🦅', color: '#3b82f6', meaning: 'Visión · Creatividad · Mente' },
  { name: 'Guerrero',  glyph: '⚔️', color: '#fbbf24', meaning: 'Inteligencia · Valentía · Cuestionar' },
  { name: 'Tierra',    glyph: '🌍', color: '#ef4444', meaning: 'Navegación · Sincronía · Evolución' },
  { name: 'Espejo',    glyph: '🪞', color: '#f5f5f5', meaning: 'Orden Sin Fin · Reflexión · Verdad' },
  { name: 'Tormenta',  glyph: '⛈️', color: '#3b82f6', meaning: 'Autogeneración · Energía · Catalización' },
  { name: 'Sol',       glyph: '☀️', color: '#fbbf24', meaning: 'Fuego Universal · Iluminación · Vida' },
]
const TONOS = [
  { num:1,  name:'Magnético',     power:'Propósito',     action:'Unificar',     essence:'Atraer' },
  { num:2,  name:'Lunar',         power:'Desafío',       action:'Polarizar',    essence:'Estabilizar' },
  { num:3,  name:'Eléctrico',     power:'Servicio',      action:'Activar',      essence:'Vincular' },
  { num:4,  name:'Autoexistente', power:'Forma',         action:'Definir',      essence:'Medir' },
  { num:5,  name:'Entonado',      power:'Resplandor',    action:'Empoderar',    essence:'Comandar' },
  { num:6,  name:'Rítmico',       power:'Igualdad',      action:'Organizar',    essence:'Equilibrar' },
  { num:7,  name:'Resonante',     power:'Sintonización', action:'Canalizar',    essence:'Inspirar' },
  { num:8,  name:'Galáctico',     power:'Integridad',    action:'Armonizar',    essence:'Modelar' },
  { num:9,  name:'Solar',         power:'Intención',     action:'Pulsar',       essence:'Realizar' },
  { num:10, name:'Planetario',    power:'Manifestación', action:'Perfeccionar', essence:'Producir' },
  { num:11, name:'Espectral',     power:'Liberación',    action:'Disolver',     essence:'Soltar' },
  { num:12, name:'Cristal',       power:'Cooperación',   action:'Dedicar',      essence:'Universalizar' },
  { num:13, name:'Cósmico',       power:'Presencia',     action:'Perdurar',     essence:'Trascender' },
]

// Dreamspell: referencia fija 26 julio 1987 = Kin 24
// (Harmonic Convergence — base del Sincronario 13 Lunas)
const DS_REF = new Date(1987, 6, 26)
const DS_REF_KIN = 24

function calcDreamspell(date: Date) {
  const diff = Math.floor((date.getTime() - DS_REF.getTime()) / 86400000)
  const kin = ((DS_REF_KIN + diff - 1) % 260 + 260) % 260 + 1
  const selIdx = (kin - 1) % 20
  const tonoIdx = (kin - 1) % 13
  const ondaIdx = ((selIdx - tonoIdx) % 20 + 20) % 20
  // Luna galáctica (13 lunas de 28 días desde 26 julio)
  const refYear = (date.getMonth() < 7 || (date.getMonth() === 6 && date.getDate() < 26))
    ? date.getFullYear() - 1 : date.getFullYear()
  const yearStart = new Date(refYear, 6, 26)
  const dayOfYear = Math.floor((date.getTime() - yearStart.getTime()) / 86400000)
  const luna = Math.floor(dayOfYear / 28) % 13 + 1
  const diaLuna = dayOfYear % 28 + 1
  return { kin, selIdx, tonoIdx, ondaIdx, luna, diaLuna, refYear }
}

const LUNAS = ['Magnética','Lunar','Eléctrica','Autoexistente','Entonada','Rítmica','Resonante','Galáctica','Solar','Planetaria','Espectral','Cristal','Cósmica']

export default function DreamspellPage() {
  const router = useRouter()
  const [date, setDate] = useState(new Date())
  const r = useMemo(() => calcDreamspell(date), [date])
  const sello = SELLOS[r.selIdx]
  const tono = TONOS[r.tonoIdx]
  const onda = SELLOS[r.ondaIdx]

  return (
    <main style={{ width:'100vw', minHeight:'100vh', display:'flex', flexDirection:'column', alignItems:'center', background:'linear-gradient(180deg,#0a0a1a,#1a0a2e,#0a0a1a)', padding:'40px 20px', color:'#fff' }}>
      <div style={{ fontSize:'12px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'4px', cursor:'pointer' }} onClick={() => router.push('/menu/calendarios')}>← CALENDARIOS ANTIGUOS</div>
      <h1 style={{ fontSize:'38px', marginBottom:'4px', letterSpacing:'5px', fontFamily:'Archeoscope, serif', color:'#a78bfa' }}>SINCRONARIO 13 LUNAS</h1>
      <p style={{ fontSize:'12px', color:'rgba(255,255,255,0.3)', marginBottom:'6px', letterSpacing:'2px' }}>Dreamspell · José Argüelles · Año Nuevo 26 Julio</p>
      <p style={{ fontSize:'11px', color:'rgba(255,255,255,0.2)', marginBottom:'24px' }}>Año Galáctico {r.refYear}/{r.refYear+1}</p>

      <input type="date" value={date.toISOString().split('T')[0]} onChange={e => setDate(new Date(e.target.value+'T12:00:00'))}
        style={{ padding:'10px 20px', fontSize:'16px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(167,139,250,0.3)', borderRadius:'8px', color:'#a78bfa', marginBottom:'24px', cursor:'pointer' }} />

      {/* Kin del día */}
      <div style={{ maxWidth:'500px', width:'100%', padding:'28px', background:'rgba(167,139,250,0.06)', border:'1px solid rgba(167,139,250,0.25)', borderRadius:'16px', textAlign:'center', marginBottom:'14px' }}>
        <div style={{ fontSize:'52px', marginBottom:'4px' }}>{sello.glyph}</div>
        <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'2px', marginBottom:'4px' }}>ENERGÍA DEL DÍA · KIN {r.kin}</div>
        <div style={{ fontSize:'32px', fontWeight:'bold', color:'#a78bfa', fontFamily:'Archeoscope, serif', marginBottom:'4px' }}>{tono.num} {sello.name}</div>
        <div style={{ fontSize:'16px', color:'rgba(255,255,255,0.7)', marginBottom:'8px' }}>Tono {tono.name}</div>
        <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.5)' }}>{sello.meaning}</div>
      </div>

      {/* Tono + Onda + Luna */}
      <div style={{ maxWidth:'500px', width:'100%', display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:'10px', marginBottom:'14px' }}>
        <div style={{ padding:'16px', background:'rgba(167,139,250,0.08)', border:'1px solid rgba(167,139,250,0.2)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'1px', marginBottom:'6px' }}>TONO</div>
          <div style={{ fontSize:'26px', fontWeight:'bold', color:'#a78bfa' }}>{tono.num}</div>
          <div style={{ fontSize:'13px', color:'#fff', marginBottom:'6px' }}>{tono.name}</div>
          <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.4)', lineHeight:'1.6' }}>
            {tono.power}<br/>{tono.action}<br/>{tono.essence}
          </div>
        </div>
        <div style={{ padding:'16px', background:'rgba(244,114,182,0.08)', border:'1px solid rgba(244,114,182,0.2)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'1px', marginBottom:'6px' }}>ONDA ENCANTADA</div>
          <div style={{ fontSize:'28px' }}>{onda.glyph}</div>
          <div style={{ fontSize:'13px', color:'#f472b6', fontWeight:'bold' }}>{onda.name}</div>
          <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.4)', marginTop:'4px' }}>{onda.meaning.split('·')[0]}</div>
        </div>
        <div style={{ padding:'16px', background:'rgba(56,189,248,0.08)', border:'1px solid rgba(56,189,248,0.2)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.3)', letterSpacing:'1px', marginBottom:'6px' }}>LUNA GALÁCTICA</div>
          <div style={{ fontSize:'26px', fontWeight:'bold', color:'#38bdf8' }}>{r.luna}</div>
          <div style={{ fontSize:'13px', color:'#fff', marginBottom:'4px' }}>{LUNAS[r.luna-1]}</div>
          <div style={{ fontSize:'10px', color:'rgba(255,255,255,0.4)' }}>Día {r.diaLuna} de 28</div>
        </div>
      </div>

      {/* Nota */}
      <div style={{ maxWidth:'500px', width:'100%', padding:'14px', background:'rgba(255,255,255,0.02)', border:'1px solid rgba(255,255,255,0.06)', borderRadius:'8px', marginBottom:'28px', textAlign:'center' }}>
        <div style={{ fontSize:'11px', color:'rgba(255,255,255,0.3)', lineHeight:'1.8' }}>
          Referencia: <strong style={{ color:'rgba(255,255,255,0.5)' }}>26 julio 1987 = Kin 24</strong> · Harmonic Convergence<br/>
          Ciclo continuo de 260 días · Año nuevo galáctico: <strong style={{ color:'rgba(255,255,255,0.5)' }}>26 julio</strong>
        </div>
      </div>

      <button onClick={() => router.push('/menu/calendarios')} style={{ padding:'14px 50px', fontSize:'18px', color:'#fff', background:'transparent', border:'2px solid rgba(255,255,255,0.3)', borderRadius:'8px', cursor:'pointer', letterSpacing:'2px', textTransform:'uppercase', transition:'all 0.3s' }}
        onMouseEnter={e => e.currentTarget.style.borderColor='#fff'} onMouseLeave={e => e.currentTarget.style.borderColor='rgba(255,255,255,0.3)'}>
        Volver
      </button>
    </main>
  )
}
