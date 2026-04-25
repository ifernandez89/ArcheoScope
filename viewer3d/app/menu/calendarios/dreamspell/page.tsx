'use client'
import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

// ─── 20 Nawales del Cholq'ij ────────────────────────────────────────────────
const NAWALES = [
  { name: "Imox",    glyph: '🌀', color: '#3b82f6', meaning: 'Agua · Locura sagrada · Lo desconocido' },
  { name: "Iq'",    glyph: '🌬️', color: '#a78bfa', meaning: 'Viento · Espíritu · Vida' },
  { name: "Aq'ab'al", glyph: '🌅', color: '#fbbf24', meaning: 'Amanecer · Claridad · Nuevo comienzo' },
  { name: "K'at",   glyph: '🕸️', color: '#f59e0b', meaning: 'Red · Abundancia · Atrapamiento' },
  { name: "Kan",    glyph: '🐍', color: '#ef4444', meaning: 'Serpiente · Fuerza vital · Kundalini' },
  { name: "Keme",   glyph: '💀', color: '#94a3b8', meaning: 'Muerte · Transformación · Ancestros' },
  { name: "Kej",    glyph: '🦌', color: '#22c55e', meaning: 'Venado · Autoridad · Los cuatro pilares' },
  { name: "Q'anil", glyph: '🌽', color: '#84cc16', meaning: 'Semilla · Madurez · Abundancia' },
  { name: "Toj",    glyph: '🔥', color: '#f97316', meaning: 'Fuego · Pago · Equilibrio cósmico' },
  { name: "Tz'i'",  glyph: '🐕', color: '#d97706', meaning: 'Perro · Justicia · Fidelidad' },
  { name: "B'atz'", glyph: '🧵', color: '#8b5cf6', meaning: 'Hilo · Tiempo · Arte sagrado' },
  { name: "E",      glyph: '🛤️', color: '#10b981', meaning: 'Camino · Destino · Viaje' },
  { name: "Aj",     glyph: '🌿', color: '#059669', meaning: 'Caña · Hogar · Autoridad espiritual' },
  { name: "I'x",    glyph: '🐆', color: '#7c3aed', meaning: 'Jaguar · Magia · Fuerza femenina' },
  { name: "Tz'ikin", glyph: '🦅', color: '#0ea5e9', meaning: 'Pájaro · Visión · Mensajero' },
  { name: "Ajmaq",  glyph: '🦉', color: '#6366f1', meaning: 'Búho · Pecado · Perdón · Ancestros' },
  { name: "No'j",   glyph: '🧠', color: '#06b6d4', meaning: 'Mente · Sabiduría · Conocimiento' },
  { name: "Tijax",  glyph: '🔪', color: '#dc2626', meaning: 'Pedernal · Curación · Corte' },
  { name: "Kawoq",  glyph: '⛈️', color: '#2563eb', meaning: 'Tormenta · Comunidad · Familia' },
  { name: "Ajpu",   glyph: '☀️', color: '#fbbf24', meaning: 'Sol · Héroe · Luz · Cazador' },
]

// ─── 13 Números (tonos) ─────────────────────────────────────────────────────
const NUMEROS = [
  { num: 1,  name: 'Jun',     meaning: 'Unidad · Inicio · Propósito' },
  { num: 2,  name: 'Ki\'eb\'', meaning: 'Dualidad · Desafío · Polaridad' },
  { num: 3,  name: 'Oxib\'',  meaning: 'Movimiento · Activación · Ritmo' },
  { num: 4,  name: 'Kajib\'', meaning: 'Estabilidad · Forma · Los cuatro rumbos' },
  { num: 5,  name: 'Jo\'ob\'', meaning: 'Centro · Poder · Empoderamiento' },
  { num: 6,  name: 'Waqib\'', meaning: 'Flujo · Organización · Equilibrio' },
  { num: 7,  name: 'Wuqub\'', meaning: 'Reflexión · Misterio · Sintonía' },
  { num: 8,  name: 'Wajxaqib\'', meaning: 'Justicia · Integridad · Armonía' },
  { num: 9,  name: 'B\'elejeb\'', meaning: 'Paciencia · Realización · Intención' },
  { num: 10, name: 'Lajuj',   meaning: 'Manifestación · Perfección · Plenitud' },
  { num: 11, name: 'Junlajuj', meaning: 'Resolución · Liberación · Soltar' },
  { num: 12, name: 'Kab\'lajuj', meaning: 'Cooperación · Dedicación · Comunidad' },
  { num: 13, name: 'Oxlajuj', meaning: 'Trascendencia · Presencia · Cosmos' },
]

// ─── Mensajes por nawal ──────────────────────────────────────────────────────
const NAWAL_MENSAJE = [
  'Confía en lo que no puedes ver. Lo invisible también es real.',
  'Tu aliento es sagrado. Habla con verdad y escucha con el corazón.',
  'Un nuevo ciclo comienza. Abre los ojos a las señales del amanecer.',
  'Observa las redes que te conectan. La abundancia ya está tejida.',
  'Tu energía vital es poderosa. Úsala con conciencia y respeto.',
  'Honra a tus ancestros. Ellos caminan contigo en este día.',
  'Mantén los cuatro pilares de tu vida en equilibrio.',
  'Lo que siembras hoy germinará en el momento exacto.',
  'Haz un pago simbólico al fuego. Agradece lo que tienes.',
  'Actúa con justicia y fidelidad. El universo registra todo.',
  'Hoy es día de B\'atz\': sagrado para ceremonias y el arte.',
  'Camina con propósito. Tu destino se revela paso a paso.',
  'Cuida tu hogar y tu comunidad. Ahí está tu raíz.',
  'La magia está en ti. Confía en tu intuición más profunda.',
  'Eleva tu visión. Los mensajes llegan desde lo alto.',
  'Pide perdón y perdona. El ciclo se cierra con gracia.',
  'Usa tu mente al servicio del bien. El conocimiento es sagrado.',
  'Corta lo que ya no sirve. La sanación requiere valentía.',
  'Tu familia y comunidad son tu fuerza. Cuídalas.',
  'Irradia tu luz. Hoy el sol brilla a través de ti.',
]

// ─── Cálculo del Cholq'ij ────────────────────────────────────────────────────
// Referencia verificada: 1 enero 2000 = 11 B'atz' (nawal 10, número 10)
const REF_DATE = new Date(2000, 0, 1) // 1 enero 2000
const REF_NAWAL = 10  // índice 0-based → B'atz' (índice 10)
const REF_NUM   = 10  // número 1-based → 11 (índice 10)

function calcCholqij(date: Date) {
  const diff = Math.floor((date.getTime() - REF_DATE.getTime()) / 86400000)
  const nawalIdx = ((REF_NAWAL + diff) % 20 + 20) % 20
  const numIdx   = ((REF_NUM   + diff) % 13 + 13) % 13
  const num      = numIdx + 1  // 1–13
  return { nawalIdx, numIdx, num }
}

export default function CholqijPage() {
  const router = useRouter()
  const [date, setDate] = useState(new Date())
  const r = useMemo(() => calcCholqij(date), [date])
  const nawal  = NAWALES[r.nawalIdx]
  const numero = NUMEROS[r.numIdx]

  return (
    <main style={{
      width: '100vw', minHeight: '100vh',
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      background: 'linear-gradient(180deg,#0a0a1a,#1a0a2e,#0a0a1a)',
      padding: '40px 20px', color: '#fff', overflowY: 'auto'
    }}>
      {/* Navegación */}
      <div
        style={{ fontSize: '18px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '12px', cursor: 'pointer', textAlign: 'center' }}
        onClick={() => router.push('/menu/calendarios')}
      >
        ← CALENDARIOS ANTIGUOS
      </div>

      <h1 className="title-responsive" style={{ color: '#a78bfa' }}>CHOLQ'IJ</h1>
      <p className="subtitle-responsive" style={{ marginBottom: '8px' }}>Calendario Sagrado Maya · 260 días</p>
      <p className="text-responsive" style={{ marginBottom: '8px', color: 'rgba(255,255,255,0.5)' }}>
        13 números × 20 nawales · Usado en ceremonias hasta hoy
      </p>
      <p className="text-responsive" style={{ marginBottom: '24px', color: 'rgba(255,255,255,0.3)' }}>
        Los ajq'ijab' (guardianes del calendario) lo usan en Guatemala
      </p>

      {/* Selector de fecha */}
      <input
        type="date"
        value={date.toISOString().split('T')[0]}
        onChange={e => setDate(new Date(e.target.value + 'T12:00:00'))}
        style={{
          padding: '12px 24px', fontSize: '18px',
          background: 'rgba(255,255,255,0.05)',
          border: '1px solid rgba(167,139,250,0.3)',
          borderRadius: '8px', color: '#a78bfa',
          marginBottom: '40px', cursor: 'pointer'
        }}
      />

      {/* Día del Cholq'ij */}
      <div className="info-card" style={{
        background: 'rgba(167,139,250,0.06)',
        border: '1px solid rgba(167,139,250,0.25)',
        padding: '28px', textAlign: 'center'
      }}>
        <div style={{ fontSize: 'clamp(40px, 10vw, 52px)', marginBottom: '4px' }}>{nawal.glyph}</div>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '4px' }}>
          DÍA DEL CHOLQ'IJ
        </div>
        <h2 style={{ color: '#a78bfa' }}>{numero.num} {nawal.name}</h2>
        <div style={{ fontSize: 'clamp(18px, 4vw, 21px)', color: 'rgba(255,255,255,0.8)', marginBottom: '8px' }}>
          {numero.name}
        </div>
        <div style={{ fontSize: 'clamp(15px, 3.5vw, 18px)', color: 'rgba(255,255,255,0.6)' }}>
          {nawal.meaning}
        </div>
      </div>

      {/* Mensaje del día */}
      <div className="info-card" style={{
        background: 'rgba(167,139,250,0.08)',
        border: '1px solid rgba(167,139,250,0.3)',
        padding: '22px', textAlign: 'center'
      }}>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '2px', marginBottom: '12px' }}>
          🌀 MENSAJE DEL NAWAL
        </div>
        <div style={{ fontSize: 'clamp(16px, 4vw, 20px)', color: 'rgba(255,255,255,0.7)', lineHeight: '1.7', marginBottom: '14px' }}>
          {NAWAL_MENSAJE[r.nawalIdx]}
        </div>
        <div style={{ borderTop: '1px solid rgba(167,139,250,0.2)', paddingTop: '12px', fontSize: 'clamp(15px, 3.5vw, 18px)', color: 'rgba(255,255,255,0.5)', lineHeight: '1.7', fontStyle: 'italic' }}>
          ✦ {numero.meaning}
        </div>
      </div>

      {/* Número + Nawal */}
      <div style={{
        maxWidth: 'min(600px, 95vw)', width: '100%',
        display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
        gap: '10px', marginBottom: '14px'
      }}>
        {/* Número */}
        <div style={{
          padding: '16px', background: 'rgba(167,139,250,0.08)',
          border: '1px solid rgba(167,139,250,0.2)', borderRadius: '12px', textAlign: 'center'
        }}>
          <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '6px' }}>NÚMERO</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#a78bfa' }}>{numero.num}</div>
          <div style={{ fontSize: '16px', color: '#fff', marginBottom: '6px' }}>{numero.name}</div>
          <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)', lineHeight: '1.6' }}>
            Intensidad del día<br />Tono energético
          </div>
        </div>

        {/* Nawal */}
        <div style={{
          padding: '16px', background: 'rgba(244,114,182,0.08)',
          border: '1px solid rgba(244,114,182,0.2)', borderRadius: '12px', textAlign: 'center'
        }}>
          <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '6px' }}>NAWAL</div>
          <div style={{ fontSize: '28px' }}>{nawal.glyph}</div>
          <div style={{ fontSize: '16px', color: '#f472b6', fontWeight: 'bold' }}>{nawal.name}</div>
          <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)', marginTop: '4px' }}>
            {nawal.meaning.split('·')[0]}
          </div>
        </div>

        {/* Ciclo */}
        <div style={{
          padding: '16px', background: 'rgba(56,189,248,0.08)',
          border: '1px solid rgba(56,189,248,0.2)', borderRadius: '12px', textAlign: 'center'
        }}>
          <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '6px' }}>CICLO</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#38bdf8' }}>260</div>
          <div style={{ fontSize: '16px', color: '#fff', marginBottom: '4px' }}>días sagrados</div>
          <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)' }}>13 × 20</div>
        </div>
      </div>

      {/* Nota */}
      <div className="info-card" style={{ padding: '14px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)' }}>
        <div className="text-responsive" style={{ lineHeight: '1.8' }}>
          Ejemplos reales: <strong style={{ color: 'rgba(255,255,255,0.6)' }}>8 Ajpu · 3 Kawoq · 12 B'atz' · 1 Imox</strong><br />
          Número (1–13) → intensidad o tono · Nawal (1–20) → energía/arquetipo
        </div>
      </div>

      {/* Información espiritual expandida */}
      <div style={{ maxWidth: 'min(700px, 95vw)', width: '100%', display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '14px' }}>

        <div className="info-card" style={{ padding: '20px', background: 'rgba(167,139,250,0.04)', border: '1px solid rgba(167,139,250,0.15)' }}>
          <div style={{ fontSize: '13px', color: '#a78bfa', letterSpacing: '2px', marginBottom: '10px' }}>🌿 LOS NAWALES SON FUERZAS VIVAS</div>
          <div className="text-responsive" style={{ color: 'rgba(255,255,255,0.65)', lineHeight: '1.8' }}>
            En el Cholq'ij, cada nawal no es solo un símbolo — es un principio espiritual activo del universo. Representa una fuerza natural, un tipo de conciencia, una energía espiritual.<br /><br />
            <strong style={{ color: 'rgba(255,255,255,0.8)' }}>Ajpu</strong> → Sol, luz, sabiduría, el cazador espiritual<br />
            <strong style={{ color: 'rgba(255,255,255,0.8)' }}>B'atz'</strong> → creatividad, destino, el hilo de la vida<br />
            <strong style={{ color: 'rgba(255,255,255,0.8)' }}>Kawoq</strong> → comunidad, familia, lluvia<br />
            <strong style={{ color: 'rgba(255,255,255,0.8)' }}>Imox</strong> → agua, inconsciente, mundo interior
          </div>
        </div>

        <div className="info-card" style={{ padding: '20px', background: 'rgba(167,139,250,0.04)', border: '1px solid rgba(167,139,250,0.15)' }}>
          <div style={{ fontSize: '13px', color: '#a78bfa', letterSpacing: '2px', marginBottom: '10px' }}>🔢 LOS NÚMEROS: INTENSIDAD ESPIRITUAL</div>
          <div className="text-responsive" style={{ color: 'rgba(255,255,255,0.65)', lineHeight: '1.8' }}>
            Los 13 números indican el grado de fuerza o desarrollo de la energía del nawal.<br /><br />
            <strong style={{ color: 'rgba(255,255,255,0.8)' }}>1</strong> inicio · <strong style={{ color: 'rgba(255,255,255,0.8)' }}>5</strong> poder · <strong style={{ color: 'rgba(255,255,255,0.8)' }}>7</strong> equilibrio · <strong style={{ color: 'rgba(255,255,255,0.8)' }}>9</strong> intención espiritual · <strong style={{ color: 'rgba(255,255,255,0.8)' }}>13</strong> culminación<br /><br />
            Un día no es solo "Ajpu" — es por ejemplo <strong style={{ color: '#a78bfa' }}>8 Ajpu</strong>: la energía solar equilibrada y madura.
          </div>
        </div>

        <div className="info-card" style={{ padding: '20px', background: 'rgba(167,139,250,0.04)', border: '1px solid rgba(167,139,250,0.15)' }}>
          <div style={{ fontSize: '13px', color: '#a78bfa', letterSpacing: '2px', marginBottom: '10px' }}>🧭 DESTINO PERSONAL</div>
          <div className="text-responsive" style={{ color: 'rgba(255,255,255,0.65)', lineHeight: '1.8' }}>
            Cuando nace una persona, su día Cholq'ij se considera su guía espiritual, energía de vida y misión. No como algo fijo, sino como un camino que hay que aprender a equilibrar. Los ajq'ijab' realizan ceremonias para ayudar a armonizar ese camino.
          </div>
        </div>

        <div className="info-card" style={{ padding: '20px', background: 'rgba(167,139,250,0.04)', border: '1px solid rgba(167,139,250,0.15)' }}>
          <div style={{ fontSize: '13px', color: '#a78bfa', letterSpacing: '2px', marginBottom: '10px' }}>🌌 EL TIEMPO COMO SER VIVO</div>
          <div className="text-responsive" style={{ color: 'rgba(255,255,255,0.65)', lineHeight: '1.8' }}>
            En la visión maya, el tiempo no es abstracto. Cada día tiene espíritu. Por eso los ajq'ij dicen que <em>"los días hablan"</em>. Interpretar el calendario es escuchar la conversación entre los ciclos del cosmos y la vida humana — ciclos solares, lunares, agrícolas y espirituales, todos interconectados.
          </div>
        </div>

      </div>

      <button
        onClick={() => router.push('/menu/calendarios')}
        className="btn-responsive"
        onMouseEnter={e => e.currentTarget.style.borderColor = '#fff'}
        onMouseLeave={e => e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)'}
      >
        Volver
      </button>
    </main>
  )
}
