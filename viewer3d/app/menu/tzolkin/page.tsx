'use client'

import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

const SELLOS = [
  { name: 'Imix (Dragón)',       glyph: '🐉', color: '#ef4444', meaning: 'Nacimiento · Nutrición · Ser',           nawal: 'Imix' },
  { name: 'Ik (Viento)',         glyph: '🌬️', color: '#a78bfa', meaning: 'Espíritu · Comunicación · Aliento',     nawal: 'Ik' },
  { name: 'Akbal (Noche)',       glyph: '🌙', color: '#1e3a8a', meaning: 'Abundancia · Intuición · Sueño',        nawal: 'Akbal' },
  { name: 'Kan (Semilla)',       glyph: '🌱', color: '#22c55e', meaning: 'Florecimiento · Conciencia · Objetivo', nawal: 'Kan' },
  { name: 'Chicchan (Serpiente)',glyph: '🐍', color: '#dc2626', meaning: 'Fuerza Vital · Instinto · Kundalini',   nawal: 'Chicchan' },
  { name: 'Cimi (Enlazador)',    glyph: '💀', color: '#f5f5f5', meaning: 'Muerte · Igualdad · Oportunidad',       nawal: 'Cimi' },
  { name: 'Manik (Mano)',        glyph: '✋', color: '#3b82f6', meaning: 'Conocimiento · Sanación · Realización', nawal: 'Manik' },
  { name: 'Lamat (Estrella)',    glyph: '⭐', color: '#fbbf24', meaning: 'Elegancia · Arte · Belleza',            nawal: 'Lamat' },
  { name: 'Muluc (Luna)',        glyph: '🌊', color: '#ef4444', meaning: 'Agua Universal · Purificación · Flujo', nawal: 'Muluc' },
  { name: 'Oc (Perro)',          glyph: '🐕', color: '#f5f5f5', meaning: 'Amor · Lealtad · Corazón',             nawal: 'Oc' },
  { name: 'Chuen (Mono)',        glyph: '🐒', color: '#3b82f6', meaning: 'Magia · Juego · Ilusión',              nawal: 'Chuen' },
  { name: 'Eb (Humano)',         glyph: '🧑', color: '#fbbf24', meaning: 'Libre Albedrío · Sabiduría · Influencia', nawal: 'Eb' },
  { name: 'Ben (Caminante)',     glyph: '🏔️', color: '#ef4444', meaning: 'Espacio · Exploración · Vigilia',      nawal: 'Ben' },
  { name: 'Ix (Mago)',           glyph: '🔮', color: '#f5f5f5', meaning: 'Atemporalidad · Receptividad · Jaguar', nawal: 'Ix' },
  { name: 'Men (Águila)',        glyph: '🦅', color: '#3b82f6', meaning: 'Visión · Creatividad · Mente',          nawal: 'Men' },
  { name: 'Cib (Guerrero)',      glyph: '⚔️', color: '#fbbf24', meaning: 'Inteligencia · Valentía · Cuestionar',  nawal: 'Cib' },
  { name: 'Caban (Tierra)',      glyph: '🌍', color: '#ef4444', meaning: 'Navegación · Sincronía · Evolución',    nawal: 'Caban' },
  { name: 'Etznab (Espejo)',     glyph: '🪞', color: '#f5f5f5', meaning: 'Orden Sin Fin · Reflexión · Verdad',    nawal: 'Etznab' },
  { name: 'Cauac (Tormenta)',    glyph: '⛈️', color: '#3b82f6', meaning: 'Autogeneración · Energía · Catalización', nawal: 'Cauac' },
  { name: 'Ahau (Sol)',          glyph: '☀️', color: '#fbbf24', meaning: 'Fuego Universal · Iluminación · Vida',  nawal: 'Ahau' },
]

const TONOS = [
  { num: 1,  name: 'Magnético',     power: 'Propósito',      action: 'Unificar',      essence: 'Atraer' },
  { num: 2,  name: 'Lunar',         power: 'Desafío',        action: 'Polarizar',     essence: 'Estabilizar' },
  { num: 3,  name: 'Eléctrico',     power: 'Servicio',       action: 'Activar',       essence: 'Vincular' },
  { num: 4,  name: 'Autoexistente', power: 'Forma',          action: 'Definir',       essence: 'Medir' },
  { num: 5,  name: 'Entonado',      power: 'Resplandor',     action: 'Empoderar',     essence: 'Comandar' },
  { num: 6,  name: 'Rítmico',       power: 'Igualdad',       action: 'Organizar',     essence: 'Equilibrar' },
  { num: 7,  name: 'Resonante',     power: 'Sintonización',  action: 'Canalizar',     essence: 'Inspirar' },
  { num: 8,  name: 'Galáctico',     power: 'Integridad',     action: 'Armonizar',     essence: 'Modelar' },
  { num: 9,  name: 'Solar',         power: 'Intención',      action: 'Pulsar',       essence: 'Realizar' },
  { num: 10, name: 'Planetario',    power: 'Manifestación',  action: 'Perfeccionar',  essence: 'Producir' },
  { num: 11, name: 'Espectral',     power: 'Liberación',     action: 'Disolver',      essence: 'Soltar' },
  { num: 12, name: 'Cristal',       power: 'Cooperación',    action: 'Dedicar',       essence: 'Universalizar' },
  { num: 13, name: 'Cósmico',       power: 'Presencia',      action: 'Perdurar',      essence: 'Trascender' },
]

const HAAB_MONTHS = [
  'Pop', 'Wo', 'Sip', 'Sotz', 'Sek', 'Xul', 'Yaxkin', 'Mol', 'Chen',
  'Yax', 'Sak', 'Keh', 'Mak', 'Kankin', 'Muwan', 'Pax', 'Kayab', 'Kumku', 'Wayeb'
]

function gregorianToJDN(year: number, month: number, day: number): number {
  const a = Math.floor((14 - month) / 12)
  const y = year + 4800 - a
  const m = month + 12 * a - 3
  return day + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045
}

function calcMayaDate(date: Date) {
  const jdn = gregorianToJDN(date.getFullYear(), date.getMonth() + 1, date.getDate())
  const mayaDays = jdn - 584283
  const numero = ((mayaDays + 3) % 13 + 13) % 13 + 1
  const selloIdx = ((mayaDays + 19) % 20 + 20) % 20
  const haabDay = ((mayaDays + 348) % 365 + 365) % 365
  const haabMonthIdx = Math.floor(haabDay / 20)
  
  let d = mayaDays
  const kin = d % 20; d = Math.floor(d / 20)
  const uinal = d % 18; d = Math.floor(d / 18)
  const tun = d % 20; d = Math.floor(d / 20)
  const katun = d % 20; d = Math.floor(d / 20)
  const baktun = d

  return { 
    jdn, mayaDays, 
    tzolkin: { numero, selloIdx }, 
    haab: { day: haabDay % 20, monthIdx: haabMonthIdx, monthName: HAAB_MONTHS[Math.min(haabMonthIdx, 18)] },
    longCount: { baktun, katun, tun, uinal, kin },
    sello: SELLOS[selloIdx],
    tono: TONOS[numero - 1],
    kinNum: ((mayaDays % 260) + 260) % 260 || 260
  }
}

export default function TzolkinPage() {
  const router = useRouter()
  const [selectedDate, setSelectedDate] = useState(new Date())
  const maya = useMemo(() => calcMayaDate(selectedDate), [selectedDate])
  const lc = maya.longCount

  return (
    <main style={{ width: '100vw', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', background: 'linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 50%, #0a0a1a 100%)', padding: '40px 20px', color: '#fff', overflowY: 'auto' }}>
      <h1 className="title-responsive" style={{ color: '#fbbf24' }}>TZOLKIN</h1>
      <p className="subtitle-responsive" style={{ marginBottom: '8px' }}>Calendario Sagrado Maya — 260 Kines</p>
      <p className="text-responsive" style={{ marginBottom: '24px', color: 'rgba(255,255,255,0.3)' }}>Correlación GMT (584283) · Válido para cualquier fecha de la historia</p>

      <input type="date" value={selectedDate.toISOString().split('T')[0]} onChange={(e) => setSelectedDate(new Date(e.target.value + 'T12:00:00'))}
        style={{ padding: '10px 20px', fontSize: '18px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(251,191,36,0.3)', borderRadius: '8px', color: '#fbbf24', marginBottom: '24px', cursor: 'pointer' }} />

      <div className="info-card" style={{ background: 'rgba(251,191,36,0.04)', border: '1px solid rgba(251,191,36,0.15)' }}>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '6px' }}>CUENTA LARGA</div>
        <div style={{ fontSize: 'clamp(24px, 7vw, 42px)', fontWeight: 'bold', color: '#fbbf24', fontFamily: 'monospace', letterSpacing: '4px' }}>
          {lc.baktun}.{lc.katun}.{lc.tun}.{lc.uinal}.{lc.kin}
        </div>
        <div style={{ fontSize: '15px', color: 'rgba(255,255,255,0.4)', marginTop: '4px' }}>
          JDN: {maya.jdn} · Días Maya: {maya.mayaDays.toLocaleString()}
        </div>
      </div>

      <div className="info-card" style={{ background: 'rgba(251,191,36,0.06)', border: '1px solid rgba(251,191,36,0.25)', padding: '28px' }}>
        <div style={{ fontSize: 'clamp(40px, 10vw, 56px)', marginBottom: '4px' }}>{maya.sello.glyph}</div>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '4px' }}>ENERGÍA DEL DÍA</div>
        <h2 style={{ color: '#fbbf24' }}>Kin {maya.kinNum}</h2>
        <h3 style={{ fontSize: 'clamp(20px, 5vw, 28px)', color: '#fff', marginBottom: '8px' }}>
          {maya.tzolkin.numero} {maya.sello.name}
        </h3>
        <div style={{ fontSize: 'clamp(19px, 4vw, 23px)', color: 'rgba(255,255,255,0.7)', marginBottom: '12px' }}>
          Tono {maya.tono.name}
        </div>
        <div className="text-responsive" style={{ color: 'rgba(255,255,255,0.5)', lineHeight: '1.6', fontSize: 'clamp(16px, 3.5vw, 20px)' }}>
          {maya.sello.meaning}
        </div>
      </div>

      <div style={{ maxWidth: '520px', width: '100%', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px', marginBottom: '16px' }}>
        <div className="info-card" style={{ padding: '20px', background: 'rgba(167,139,250,0.08)', border: '1px solid rgba(167,139,250,0.25)', margin: 0 }}>
          <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '6px' }}>TONO GALÁCTICO</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#a78bfa' }}>{maya.tono.num}</div>
          <div style={{ fontSize: '18px', color: '#fff', marginBottom: '6px' }}>{maya.tono.name}</div>
          <div style={{ fontSize: 'clamp(15px, 3.5vw, 17px)', color: 'rgba(255,255,255,0.5)', lineHeight: '1.6' }}>
            {maya.tono.power} · {maya.tono.action} · {maya.tono.essence}
          </div>
        </div>

        <div className="info-card" style={{ padding: '20px', background: 'rgba(34,197,94,0.08)', border: '1px solid rgba(34,197,94,0.25)', margin: 0 }}>
          <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '6px' }}>HAAB (CIVIL 365)</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#22c55e' }}>
            {maya.haab.day} {maya.haab.monthName}
          </div>
          <div style={{ fontSize: 'clamp(15px, 3.5vw, 17px)', color: 'rgba(255,255,255,0.5)', marginTop: '8px' }}>
            Mes {maya.haab.monthIdx + 1} de 19
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
