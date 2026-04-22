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
const DS_REF = new Date(1987, 6, 26)
const DS_REF_KIN = 24

function calcDreamspell(date: Date) {
  const diff = Math.floor((date.getTime() - DS_REF.getTime()) / 86400000)
  const kin = ((DS_REF_KIN + diff - 1) % 260 + 260) % 260 + 1
  const selIdx = (kin - 1) % 20
  const tonoIdx = (kin - 1) % 13
  const ondaIdx = ((selIdx - tonoIdx) % 20 + 20) % 20
  const refYear = (date.getMonth() < 7 || (date.getMonth() === 6 && date.getDate() < 26))
    ? date.getFullYear() - 1 : date.getFullYear()
  const yearStart = new Date(refYear, 6, 26)
  const dayOfYear = Math.floor((date.getTime() - yearStart.getTime()) / 86400000)
  const luna = Math.floor(dayOfYear / 28) % 13 + 1
  const diaLuna = dayOfYear % 28 + 1
  return { kin, selIdx, tonoIdx, ondaIdx, luna, diaLuna, refYear }
}

const LUNAS = ['Magnética','Lunar','Eléctrica','Autoexistente','Entonada','Rítmica','Resonante','Galáctica','Solar','Planetaria','Espectral','Cristal','Cósmica']

const SELLO_MENSAJE = [
  'Honra tus raíces. Nutre lo que te da vida. Hoy es un día para recibir.',
  'Habla desde el corazón. Tu voz es un instrumento del espíritu.',
  'Confía en tu intuición. Los sueños de anoche traen mensajes.',
  'Planta una intención. Lo que siembras hoy florece en el tiempo correcto.',
  'Escucha a tu cuerpo. Tu instinto es sabiduría ancestral.',
  'Suelta lo que ya no sirve. La muerte de lo viejo abre paso a lo nuevo.',
  'Sana con tus manos y tu presencia. Eres un canal de luz.',
  'Expresa tu belleza interior. El arte es tu lenguaje natural hoy.',
  'Fluye con las emociones. El agua siempre encuentra su camino.',
  'Ama sin condiciones. Tu corazón es tu brújula más confiable.',
  'Juega, crea, imagina. La magia vive en la ligereza del ser.',
  'Usa tu libre albedrío con sabiduría. Cada elección es sagrada.',
  'Explora nuevos horizontes. El universo te invita a expandirte.',
  'Observa en silencio. La verdad se revela a quien sabe esperar.',
  'Eleva tu visión. Desde las alturas todo cobra perspectiva.',
  'Cuestiona con valentía. Las preguntas correctas abren puertas.',
  'Sincronízate con la Tierra. Camina consciente sobre ella.',
  'Mira con honestidad. El espejo no miente, solo refleja.',
  'Libera la energía estancada. La tormenta limpia y renueva.',
  'Irradia tu luz. Hoy el sol brilla a través de ti.',
]

const TONO_CLIMA = [
  { clima: '🌱 Día de Inicio',      consejo: 'Ideal para comenzar proyectos. La energía atrae nuevas oportunidades.' },
  { clima: '⚖️ Día de Polaridad',   consejo: 'Observa los opuestos en tu vida. El equilibrio surge del contraste.' },
  { clima: '⚡ Día de Activación',  consejo: 'Energía alta para conectar con otros. Comparte, colabora, vincula.' },
  { clima: '📐 Día de Definición',  consejo: 'Clarifica tus formas y límites. Define qué es tuyo y qué no.' },
  { clima: '✨ Día de Poder',        consejo: 'Tu brillo interior está amplificado. Empodera a quienes te rodean.' },
  { clima: '🎵 Día de Ritmo',       consejo: 'Organiza tu espacio y tiempo. El orden trae paz y fluidez.' },
  { clima: '🎶 Día de Resonancia',  consejo: 'Medita, canaliza, inspírate. Estás sintonizado con el cosmos.' },
  { clima: '🌀 Día Galáctico',      consejo: 'Actúa con integridad total. Lo que haces hoy modela el futuro.' },
  { clima: '☀️ Día Solar',          consejo: 'Pulsa tu intención con fuerza. Lo que deseas está cerca de manifestarse.' },
  { clima: '🌍 Día de Manifestación', consejo: 'Perfecciona lo que construyes. La realidad responde a tu enfoque.' },
  { clima: '🌊 Día de Liberación',  consejo: 'Suelta, disuelve, deja ir. La libertad llega cuando sueltas el control.' },
  { clima: '💎 Día de Cooperación', consejo: 'Reúnete con tu tribu. La fuerza colectiva supera a la individual.' },
  { clima: '🌌 Día Cósmico',        consejo: 'Trasciende lo cotidiano. Hoy el velo entre mundos es más delgado.' },
]

export default function DreamspellPage() {
  const router = useRouter()
  const [date, setDate] = useState(new Date())
  const r = useMemo(() => calcDreamspell(date), [date])
  const sello = SELLOS[r.selIdx]
  const tono = TONOS[r.tonoIdx]
  const onda = SELLOS[r.ondaIdx]

  return (
    <main style={{ width:'100vw', minHeight:'100vh', display:'flex', flexDirection:'column', alignItems:'center', background:'linear-gradient(180deg,#0a0a1a,#1a0a2e,#0a0a1a)', padding:'40px 20px', color:'#fff', overflowY: 'auto' }}>
      <div style={{ fontSize:'18px', color:'rgba(255,255,255,0.4)', letterSpacing:'2px', marginBottom:'12px', cursor:'pointer', textAlign: 'center' }} onClick={() => router.push('/menu/calendarios')}>← CALENDARIOS ANTIGUOS</div>
      <h1 className="title-responsive" style={{ color:'#a78bfa' }}>SINCRONARIO 13 LUNAS</h1>
      <p className="subtitle-responsive" style={{ marginBottom:'8px' }}>Dreamspell · José Argüelles · Año Nuevo 26 Julio</p>
      <p className="text-responsive" style={{ marginBottom:'8px', color:'rgba(255,255,255,0.5)' }}>Interpretación moderna inspirada en calendarios mayas.</p>
      <p className="text-responsive" style={{ marginBottom:'24px', color:'rgba(255,255,255,0.3)' }}>Año Galáctico {r.refYear}/{r.refYear+1}</p>

      <input type="date" value={date.toISOString().split('T')[0]} onChange={e => setDate(new Date(e.target.value+'T12:00:00'))}
        style={{ padding:'12px 24px', fontSize:'18px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(167,139,250,0.3)', borderRadius:'8px', color:'#a78bfa', marginBottom:'40px', cursor:'pointer' }} />

      {/* Kin del día */}
      <div className="info-card" style={{ background:'rgba(167,139,250,0.06)', border:'1px solid rgba(167,139,250,0.25)', padding:'28px' }}>
        <div style={{ fontSize:'clamp(40px, 10vw, 52px)', marginBottom:'4px' }}>{sello.glyph}</div>
        <div style={{ fontSize:'14px', color:'rgba(255,255,255,0.4)', letterSpacing:'2px', marginBottom:'4px' }}>ENERGÍA DEL DÍA · KIN {r.kin}</div>
        <h2 style={{ color:'#a78bfa' }}>{tono.num} {sello.name}</h2>
        <div style={{ fontSize:'clamp(18px, 4vw, 21px)', color:'rgba(255,255,255,0.8)', marginBottom:'8px' }}>Tono {tono.name}</div>
        <div style={{ fontSize:'clamp(15px, 3.5vw, 18px)', color:'rgba(255,255,255,0.6)' }}>{sello.meaning}</div>
      </div>

      {/* CLIMA ENERGÉTICO DEL DÍA */}
      <div className="info-card" style={{ background:'rgba(167,139,250,0.08)', border:'1px solid rgba(167,139,250,0.3)', padding:'22px' }}>
        <div style={{ fontSize:'14px', color:'rgba(255,255,255,0.4)', letterSpacing:'2px', marginBottom:'12px', textAlign:'center' }}>
          🌤️ CLIMA ENERGÉTICO DEL DÍA
        </div>
        <div style={{ fontSize:'clamp(18px, 5vw, 24px)', fontWeight:'bold', color:'#a78bfa', textAlign:'center', marginBottom:'10px' }}>
          {TONO_CLIMA[r.tonoIdx].clima}
        </div>
        <div style={{ fontSize:'clamp(16px, 4vw, 20px)', color:'rgba(255,255,255,0.7)', textAlign:'center', lineHeight:'1.7', marginBottom:'14px' }}>
          {TONO_CLIMA[r.tonoIdx].consejo}
        </div>
        <div style={{ borderTop:'1px solid rgba(167,139,250,0.2)', paddingTop:'12px', fontSize:'clamp(16px, 4vw, 20px)', color:'rgba(255,255,255,0.6)', textAlign:'center', lineHeight:'1.7', fontStyle:'italic' }}>
          ✦ {SELLO_MENSAJE[r.selIdx]}
        </div>
      </div>

      {/* Tono + Onda + Luna */}
      <div style={{ maxWidth:'min(600px, 95vw)', width:'100%', display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(130px, 1fr))', gap:'10px', marginBottom:'14px' }}>
        <div style={{ padding:'16px', background:'rgba(167,139,250,0.08)', border:'1px solid rgba(167,139,250,0.2)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.4)', letterSpacing:'1px', marginBottom:'6px' }}>TONO</div>
          <div style={{ fontSize:'28px', fontWeight:'bold', color:'#a78bfa' }}>{tono.num}</div>
          <div style={{ fontSize:'16px', color:'#fff', marginBottom:'6px' }}>{tono.name}</div>
          <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.5)', lineHeight:'1.6' }}>
            {tono.power}<br/>{tono.action}<br/>{tono.essence}
          </div>
        </div>
        <div style={{ padding:'16px', background:'rgba(244,114,182,0.08)', border:'1px solid rgba(244,114,182,0.2)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.4)', letterSpacing:'1px', marginBottom:'6px' }}>ONDA ENCANTADA</div>
          <div style={{ fontSize:'28px' }}>{onda.glyph}</div>
          <div style={{ fontSize:'16px', color:'#f472b6', fontWeight:'bold' }}>{onda.name}</div>
          <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.5)', marginTop:'4px' }}>{onda.meaning.split('·')[0]}</div>
        </div>
        <div style={{ padding:'16px', background:'rgba(56,189,248,0.08)', border:'1px solid rgba(56,189,248,0.2)', borderRadius:'12px', textAlign:'center' }}>
          <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.4)', letterSpacing:'1px', marginBottom:'6px' }}>LUNA GALÁCTICA</div>
          <div style={{ fontSize:'28px', fontWeight:'bold', color:'#38bdf8' }}>{r.luna}</div>
          <div style={{ fontSize:'16px', color:'#fff', marginBottom:'4px' }}>{LUNAS[r.luna-1]}</div>
          <div style={{ fontSize:'13px', color:'rgba(255,255,255,0.5)' }}>Día {r.diaLuna} de 28</div>
        </div>
      </div>

      {/* Nota */}
      <div className="info-card" style={{ padding:'14px', background:'rgba(255,255,255,0.02)', border:'1px solid rgba(255,255,255,0.06)' }}>
        <div className="text-responsive" style={{ lineHeight:'1.8' }}>
          Referencia: <strong style={{ color:'rgba(255,255,255,0.6)' }}>26 julio 1987 = Kin 24</strong> · Harmonic Convergence<br/>
          Ciclo continuo de 260 días · Año nuevo galáctico: <strong style={{ color:'rgba(255,255,255,0.6)' }}>26 julio</strong>
        </div>
      </div>

      <button onClick={() => router.push('/menu/calendarios')} className="btn-responsive"
        onMouseEnter={e => e.currentTarget.style.borderColor='#fff'} onMouseLeave={e => e.currentTarget.style.borderColor='rgba(255,255,255,0.3)'}>
        Volver
      </button>
    </main>
  )
}
