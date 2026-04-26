'use client'
import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

// ─── 20 Nawales del Cholq'ij ────────────────────────────────────────────────
const NAWALES = [
  { name: "Imox",    glyph: '🌀', color: '#3b82f6', meaning: 'Agua · Locura sagrada · Lo desconocido', desc: 'Nawal del agua y del mundo invisible. Representa el inconsciente colectivo, la intuición profunda y lo que está más allá de la razón. Los ajq\'ijab\' lo invocan para conectar con los ancestros y el mundo espiritual.' },
  { name: "Iq'",    glyph: '🌬️', color: '#a78bfa', meaning: 'Viento · Espíritu · Vida', desc: 'Nawal del viento y del aliento vital. Es el espíritu que anima todo ser vivo. Representa la comunicación sagrada, la voz de los ancestros y la presencia del creador en cada respiración.' },
  { name: "Aq'ab'al", glyph: '🌅', color: '#fbbf24', meaning: 'Amanecer · Claridad · Nuevo comienzo', desc: 'Nawal del amanecer y la transición entre la oscuridad y la luz. Simboliza los nuevos comienzos, la claridad mental y el momento en que lo oculto se vuelve visible. Día propicio para iniciar proyectos.' },
  { name: "K'at",   glyph: '🕸️', color: '#f59e0b', meaning: 'Red · Abundancia · Atrapamiento', desc: 'Nawal de la red y la abundancia. Representa las conexiones entre todos los seres y la riqueza que surge de ellas. También advierte sobre las trampas del ego y los enredos que nos impiden avanzar.' },
  { name: "Kan",    glyph: '🐍', color: '#ef4444', meaning: 'Serpiente · Fuerza vital · Kundalini', desc: 'Nawal de la serpiente y la energía vital. Representa la fuerza primordial que sube por la columna vertebral, la sexualidad sagrada y el poder de transformación. Es la energía que sostiene la vida.' },
  { name: "Keme",   glyph: '💀', color: '#94a3b8', meaning: 'Muerte · Transformación · Ancestros', desc: 'Nawal de la muerte y la transformación. No representa el fin, sino el paso entre mundos. Es el guardián de los ancestros y el portal hacia la vida eterna. Día para honrar a los que partieron.' },
  { name: "Kej",    glyph: '🦌', color: '#22c55e', meaning: 'Venado · Autoridad · Los cuatro pilares', desc: 'Nawal del venado y la autoridad espiritual. Representa los cuatro puntos cardinales y los pilares que sostienen el cosmos. Es el guardián de la naturaleza y el líder que sirve a su comunidad.' },
  { name: "Q'anil", glyph: '🌽', color: '#84cc16', meaning: 'Semilla · Madurez · Abundancia', desc: 'Nawal de la semilla y la fertilidad. Representa el potencial que duerme en cada ser y el momento de la cosecha. Es el nawal de la abundancia material y espiritual, del maíz sagrado que sustenta la vida maya.' },
  { name: "Toj",    glyph: '🔥', color: '#f97316', meaning: 'Fuego · Pago · Equilibrio cósmico', desc: 'Nawal del fuego y el pago ceremonial. Representa el equilibrio entre lo que recibimos y lo que devolvemos al cosmos. Los ajq\'ijab\' realizan ofrendas en este día para saldar deudas espirituales y restaurar la armonía.' },
  { name: "Tz'i'",  glyph: '🐕', color: '#d97706', meaning: 'Perro · Justicia · Fidelidad', desc: 'Nawal del perro y la justicia divina. Representa la lealtad, la autoridad de la ley y el guardián del camino al inframundo. Es el nawal de los líderes comunitarios y quienes administran justicia.' },
  { name: "B'atz'", glyph: '🧵', color: '#8b5cf6', meaning: 'Hilo · Tiempo · Arte sagrado', desc: 'Nawal del hilo y el tiempo. Es uno de los más sagrados: representa el tejido del destino, el arte, la música y la continuidad de la vida. El día 8 B\'atz\' es el año nuevo de los ajq\'ijab\' y el día de iniciación de nuevos sacerdotes.' },
  { name: "E",      glyph: '🛤️', color: '#10b981', meaning: 'Camino · Destino · Viaje', desc: 'Nawal del camino y el destino. Representa el viaje de la vida, los pasos que damos y la dirección que elegimos. Es el nawal de los viajeros, los comerciantes y quienes buscan su propósito.' },
  { name: "Aj",     glyph: '🌿', color: '#059669', meaning: 'Caña · Hogar · Autoridad espiritual', desc: 'Nawal de la caña y el hogar sagrado. Representa la columna vertebral del cosmos, la autoridad espiritual y la protección del hogar y la familia. Es el nawal de los guías espirituales y los que cuidan a su comunidad.' },
  { name: "I'x",    glyph: '🐆', color: '#7c3aed', meaning: 'Jaguar · Magia · Fuerza femenina', desc: 'Nawal del jaguar y la magia. Representa la fuerza femenina, el poder de la oscuridad sagrada y la capacidad de moverse entre mundos. Es el nawal de los chamanes y quienes trabajan con energías invisibles.' },
  { name: "Tz'ikin", glyph: '🦅', color: '#0ea5e9', meaning: 'Pájaro · Visión · Mensajero', desc: 'Nawal del pájaro y la visión elevada. Representa la capacidad de ver desde lo alto, la libertad del espíritu y el papel de mensajero entre el mundo humano y el divino. Es el nawal de la prosperidad y los sueños.' },
  { name: "Ajmaq",  glyph: '🦉', color: '#6366f1', meaning: 'Búho · Pecado · Perdón · Ancestros', desc: 'Nawal del búho y el perdón. Representa los errores cometidos y la posibilidad de sanarlos. Es el nawal de los ancestros que guían desde el más allá y el día para pedir perdón y liberarse de cargas del pasado.' },
  { name: "No'j",   glyph: '🧠', color: '#06b6d4', meaning: 'Mente · Sabiduría · Conocimiento', desc: 'Nawal de la mente y la sabiduría cósmica. Representa el pensamiento elevado, la inteligencia al servicio del bien y el conocimiento ancestral. Es el nawal de los maestros, los estudiantes y quienes buscan la verdad.' },
  { name: "Tijax",  glyph: '🔪', color: '#dc2626', meaning: 'Pedernal · Curación · Corte', desc: 'Nawal del pedernal y la curación. Representa el corte que libera, la cirugía espiritual que elimina lo que enferma. Es el nawal de los sanadores, los médicos y quienes tienen el poder de cortar lazos negativos.' },
  { name: "Kawoq",  glyph: '⛈️', color: '#2563eb', meaning: 'Tormenta · Comunidad · Familia', desc: 'Nawal de la tormenta y la comunidad. Representa la fuerza colectiva, la lluvia que nutre la tierra y los lazos familiares que nos sostienen. Es el nawal de las mujeres, el hogar y la vida en comunidad.' },
  { name: "Ajpu",   glyph: '☀️', color: '#fbbf24', meaning: 'Sol · Héroe · Luz · Cazador', desc: 'Nawal del sol y el héroe espiritual. Representa la luz que vence a la oscuridad, la valentía del guerrero espiritual y la iluminación. Es el nawal de los líderes, los artistas y quienes irradian luz a su alrededor.' },
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

      {/* Número + Ciclo en grid, Nawal como card separada */}
      <div style={{
        maxWidth: 'min(600px, 95vw)', width: '100%',
        display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '10px', marginBottom: '10px'
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

      {/* Nawal — card ancha con descripción completa */}
      <div style={{
        maxWidth: 'min(600px, 95vw)', width: '100%', marginBottom: '14px',
        padding: '20px', background: 'rgba(244,114,182,0.08)',
        border: '1px solid rgba(244,114,182,0.25)', borderRadius: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
          <div style={{ fontSize: '32px' }}>{nawal.glyph}</div>
          <div>
            <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px' }}>NAWAL DEL DÍA</div>
            <div style={{ fontSize: '20px', color: '#f472b6', fontWeight: 'bold' }}>{nawal.name}</div>
            <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)' }}>{nawal.meaning}</div>
          </div>
        </div>
        <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.65)', lineHeight: '1.8', borderTop: '1px solid rgba(244,114,182,0.15)', paddingTop: '12px' }}>
          {nawal.desc}
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

      {/* Aclaración: Cholq'ij vs Tzolk'in clásico */}
      <div className="info-card" style={{
        padding: '20px', background: 'rgba(251,191,36,0.04)',
        border: '1px solid rgba(251,191,36,0.2)', marginBottom: '8px'
      }}>
        <div style={{ fontSize: '13px', color: '#fbbf24', letterSpacing: '2px', marginBottom: '12px' }}>
          📜 CHOLQ'IJ Y TZOLK'IN — LA MISMA RAÍZ
        </div>
        <div className="text-responsive" style={{ color: 'rgba(255,255,255,0.65)', lineHeight: '1.8', marginBottom: '16px' }}>
          El Cholq'ij usado hoy por sacerdotes mayas es prácticamente el mismo sistema que el Tzolk'in clásico. También usa 13 números y 20 nawales. La diferencia principal es el nombre de los días en idiomas mayas modernos (k'iche', kaqchikel, etc.).
        </div>
        {/* Tabla comparativa */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px', fontSize: '13px' }}>
          <div style={{ color: '#fbbf24', fontWeight: 'bold', padding: '6px 10px', background: 'rgba(251,191,36,0.1)', borderRadius: '6px 6px 0 0', textAlign: 'center' }}>Maya clásico</div>
          <div style={{ color: '#a78bfa', fontWeight: 'bold', padding: '6px 10px', background: 'rgba(167,139,250,0.1)', borderRadius: '6px 6px 0 0', textAlign: 'center' }}>Cholq'ij moderno</div>
          {[
            ['Ajaw', 'Ajpu'],
            ['Imix', 'Imox'],
            ["Ik'", "Iq'"],
            ["Ak'bal", "Aq'ab'al"],
          ].map(([clasico, moderno], i) => (
            <>
              <div key={`c${i}`} style={{ padding: '5px 10px', background: 'rgba(251,191,36,0.05)', color: 'rgba(255,255,255,0.7)', textAlign: 'center', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>{clasico}</div>
              <div key={`m${i}`} style={{ padding: '5px 10px', background: 'rgba(167,139,250,0.05)', color: 'rgba(255,255,255,0.7)', textAlign: 'center', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>{moderno}</div>
            </>
          ))}
        </div>
        <div className="text-responsive" style={{ color: 'rgba(255,255,255,0.45)', lineHeight: '1.7', marginTop: '12px', fontStyle: 'italic' }}>
          La estructura del calendario es idéntica. Solo cambian los nombres según el idioma maya.
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
