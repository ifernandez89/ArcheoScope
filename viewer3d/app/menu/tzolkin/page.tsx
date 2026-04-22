'use client'

import { useRouter } from 'next/navigation'
import { useState, useMemo } from 'react'

// ═══════════════════════════════════════════════════════════════════════════════
// MOTOR CALENDÁRICO MAYA — Correlación GMT (584283)
// Gregoriano → JDN → Días Maya → Tzolkin + Haab + Cuenta Larga
// Funciona para cualquier fecha: 10000 a.C. → 5000 d.C.
// ═══════════════════════════════════════════════════════════════════════════════

const GMT_CORRELATION = 584283 // Constante GMT (Goodman-Martínez-Thompson)

// ─── 20 Sellos Solares (Nawales) ─────────────────────────────────────────────
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

// ─── 13 Tonos Galácticos ─────────────────────────────────────────────────────
const TONOS = [
  { num: 1,  name: 'Magnético',     power: 'Propósito',      action: 'Unificar',      essence: 'Atraer' },
  { num: 2,  name: 'Lunar',         power: 'Desafío',        action: 'Polarizar',     essence: 'Estabilizar' },
  { num: 3,  name: 'Eléctrico',     power: 'Servicio',       action: 'Activar',       essence: 'Vincular' },
  { num: 4,  name: 'Autoexistente', power: 'Forma',          action: 'Definir',       essence: 'Medir' },
  { num: 5,  name: 'Entonado',      power: 'Resplandor',     action: 'Empoderar',     essence: 'Comandar' },
  { num: 6,  name: 'Rítmico',       power: 'Igualdad',       action: 'Organizar',     essence: 'Equilibrar' },
  { num: 7,  name: 'Resonante',     power: 'Sintonización',  action: 'Canalizar',     essence: 'Inspirar' },
  { num: 8,  name: 'Galáctico',     power: 'Integridad',     action: 'Armonizar',     essence: 'Modelar' },
  { num: 9,  name: 'Solar',         power: 'Intención',      action: 'Pulsar',        essence: 'Realizar' },
  { num: 10, name: 'Planetario',    power: 'Manifestación',  action: 'Perfeccionar',  essence: 'Producir' },
  { num: 11, name: 'Espectral',     power: 'Liberación',     action: 'Disolver',      essence: 'Soltar' },
  { num: 12, name: 'Cristal',       power: 'Cooperación',    action: 'Dedicar',       essence: 'Universalizar' },
  { num: 13, name: 'Cósmico',       power: 'Presencia',      action: 'Perdurar',      essence: 'Trascender' },
]

// ─── 19 Meses Haab (18 × 20 + Wayeb 5) ──────────────────────────────────────
const HAAB_MONTHS = [
  'Pop', 'Wo', 'Sip', 'Sotz', 'Sek', 'Xul', 'Yaxkin', 'Mol', 'Chen',
  'Yax', 'Sak', 'Keh', 'Mak', 'Kankin', 'Muwan', 'Pax', 'Kayab', 'Kumku', 'Wayeb'
]

// ═══════════════════════════════════════════════════════════════════════════════
// FUNCIONES DE CÁLCULO
// ═══════════════════════════════════════════════════════════════════════════════

/** Gregoriano → Número de Día Juliano (JDN) — válido para cualquier fecha */
function gregorianToJDN(year: number, month: number, day: number): number {
  const a = Math.floor((14 - month) / 12)
  const y = year + 4800 - a
  const m = month + 12 * a - 3
  return day + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045
}

/** JDN → Días desde el inicio de la Cuenta Larga Maya (0.0.0.0.0) */
function jdnToMayaDays(jdn: number): number {
  return jdn - GMT_CORRELATION
}

/** Días Maya → Tzolkin (número 1-13 + sello 0-19) */
function calcTzolkin(mayaDays: number) {
  // El día 0.0.0.0.0 era 4 Ahau → offset de número = 3, offset de sello = 19
  const numero = ((mayaDays + 3) % 13 + 13) % 13 + 1  // 1-13
  const selloIdx = ((mayaDays + 19) % 20 + 20) % 20    // 0-19
  return { numero, selloIdx }
}

/** Días Maya → Haab (día 0-19 del mes + mes 0-18) */
function calcHaab(mayaDays: number) {
  // El día 0.0.0.0.0 era 8 Kumku → offset = 348 (8 Kumku = día 348 del Haab)
  const haabDay = ((mayaDays + 348) % 365 + 365) % 365
  const monthIdx = Math.floor(haabDay / 20)
  const dayInMonth = haabDay % 20
  return { dayInMonth, monthIdx, monthName: HAAB_MONTHS[Math.min(monthIdx, 18)] }
}

/** Días Maya → Cuenta Larga (Baktun.Katun.Tun.Uinal.Kin) */
function calcLongCount(mayaDays: number) {
  let d = mayaDays
  const kin    = d % 20; d = Math.floor(d / 20)
  const uinal  = d % 18; d = Math.floor(d / 18)
  const tun    = d % 20; d = Math.floor(d / 20)
  const katun  = d % 20; d = Math.floor(d / 20)
  const baktun = d
  return { baktun, katun, tun, uinal, kin }
}

/** Cálculo completo desde fecha */
function calcMayaDate(date: Date) {
  const jdn = gregorianToJDN(date.getFullYear(), date.getMonth() + 1, date.getDate())
  const mayaDays = jdnToMayaDays(jdn)
  const tzolkin = calcTzolkin(mayaDays)
  const haab = calcHaab(mayaDays)
  const longCount = calcLongCount(mayaDays)

  const sello = SELLOS[tzolkin.selloIdx]
  const tono = TONOS[tzolkin.numero - 1]
  // Onda encantada: el sello que inicia el ciclo de 13 días
  const ondaOffset = (tzolkin.numero - 1)
  const ondaSelloIdx = ((tzolkin.selloIdx - ondaOffset) % 20 + 20) % 20
  const onda = SELLOS[ondaSelloIdx]
  // Kin absoluto en el ciclo de 260
  const kinNum = ((mayaDays % 260) + 260) % 260 || 260

  return { jdn, mayaDays, tzolkin, haab, longCount, sello, tono, onda, kinNum }
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPONENTE
// ═══════════════════════════════════════════════════════════════════════════════

export default function TzolkinPage() {
  const router = useRouter()
  const [selectedDate, setSelectedDate] = useState(new Date())
  const maya = useMemo(() => calcMayaDate(selectedDate), [selectedDate])

  const lc = maya.longCount

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'flex-start',
      background: 'linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 50%, #0a0a1a 100%)',
      margin: 0, padding: '40px 20px', overflow: 'auto', color: '#fff',
    }}>
      <h1 style={{ fontSize: '48px', marginBottom: '4px', letterSpacing: '6px', fontFamily: 'Archeoscope, serif', color: '#fbbf24' }}>
        TZOLKIN
      </h1>
      <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.35)', marginBottom: '6px', letterSpacing: '2px' }}>
        Calendario Sagrado Maya — 260 Kines
      </p>
      <p style={{ fontSize: '11px', color: 'rgba(255,255,255,0.25)', marginBottom: '24px', letterSpacing: '1px' }}>
        Correlación GMT (584283) · Válido para cualquier fecha de la historia
      </p>

      {/* Selector de fecha */}
      <input
        type="date"
        value={selectedDate.toISOString().split('T')[0]}
        onChange={(e) => setSelectedDate(new Date(e.target.value + 'T12:00:00'))}
        style={{
          padding: '10px 20px', fontSize: '16px', background: 'rgba(255,255,255,0.05)',
          border: '1px solid rgba(251,191,36,0.3)', borderRadius: '8px', color: '#fbbf24',
          marginBottom: '24px', cursor: 'pointer',
        }}
      />

      {/* ─── CUENTA LARGA ─────────────────────────────────────────────── */}
      <div style={{
        maxWidth: '520px', width: '100%', padding: '20px',
        background: 'rgba(251,191,36,0.04)', border: '1px solid rgba(251,191,36,0.15)',
        borderRadius: '12px', textAlign: 'center', marginBottom: '16px',
      }}>
        <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.3)', letterSpacing: '2px', marginBottom: '8px' }}>
          CUENTA LARGA
        </div>
        <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#fbbf24', fontFamily: 'monospace', letterSpacing: '4px' }}>
          {lc.baktun}.{lc.katun}.{lc.tun}.{lc.uinal}.{lc.kin}
        </div>
        <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.3)', marginTop: '6px' }}>
          Día Juliano: {maya.jdn} · Días Maya: {maya.mayaDays.toLocaleString()}
        </div>
      </div>

      {/* ─── KIN DEL DÍA ─────────────────────────────────────────────── */}
      <div style={{
        maxWidth: '520px', width: '100%', padding: '28px',
        background: 'rgba(251,191,36,0.06)', border: '1px solid rgba(251,191,36,0.25)',
        borderRadius: '16px', textAlign: 'center', marginBottom: '16px',
      }}>
        <div style={{ fontSize: '56px', marginBottom: '4px' }}>{maya.sello.glyph}</div>
        <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.3)', letterSpacing: '2px', marginBottom: '4px' }}>
          ENERGÍA DEL DÍA
        </div>
        <div style={{ fontSize: '40px', fontWeight: 'bold', color: '#fbbf24', fontFamily: 'Archeoscope, serif', marginBottom: '2px' }}>
          Kin {maya.kinNum}
        </div>
        <div style={{ fontSize: '22px', color: '#fff', fontFamily: 'Archeoscope, serif', marginBottom: '4px' }}>
          {maya.tzolkin.numero} {maya.sello.name}
        </div>
        <div style={{ fontSize: '16px', color: 'rgba(255,255,255,0.6)', marginBottom: '10px' }}>
          Tono {maya.tono.name}
        </div>
        <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.5)', lineHeight: '1.6' }}>
          {maya.sello.meaning}
        </div>
      </div>

      {/* ─── TZOLKIN + HAAB ──────────────────────────────────────────── */}
      <div style={{
        maxWidth: '520px', width: '100%', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px',
      }}>
        {/* Tono Galáctico */}
        <div style={{
          padding: '20px', background: 'rgba(167,139,250,0.08)', border: '1px solid rgba(167,139,250,0.25)',
          borderRadius: '12px', textAlign: 'center',
        }}>
          <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.3)', letterSpacing: '1px', marginBottom: '8px' }}>TONO GALÁCTICO</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#a78bfa' }}>{maya.tono.num}</div>
          <div style={{ fontSize: '15px', color: '#fff', marginBottom: '8px' }}>{maya.tono.name}</div>
          <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.4)', lineHeight: '1.7' }}>
            Poder: <strong style={{ color: '#c4b5fd' }}>{maya.tono.power}</strong><br/>
            Acción: <strong style={{ color: '#c4b5fd' }}>{maya.tono.action}</strong><br/>
            Esencia: <strong style={{ color: '#c4b5fd' }}>{maya.tono.essence}</strong>
          </div>
        </div>

        {/* Haab */}
        <div style={{
          padding: '20px', background: 'rgba(34,197,94,0.08)', border: '1px solid rgba(34,197,94,0.25)',
          borderRadius: '12px', textAlign: 'center',
        }}>
          <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.3)', letterSpacing: '1px', marginBottom: '8px' }}>HAAB (CIVIL 365)</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#22c55e' }}>
            {maya.haab.dayInMonth} {maya.haab.monthName}
          </div>
          <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.4)', marginTop: '8px', lineHeight: '1.7' }}>
            Mes {maya.haab.monthIdx + 1} de 19<br/>
            {maya.haab.monthName === 'Wayeb' ? '5 días sin nombre (peligrosos)' : `Día ${maya.haab.dayInMonth} de 20`}
          </div>
        </div>
      </div>

      {/* ─── ONDA ENCANTADA ──────────────────────────────────────────── */}
      <div style={{
        maxWidth: '520px', width: '100%', padding: '18px',
        background: 'rgba(244,114,182,0.06)', border: '1px solid rgba(244,114,182,0.2)',
        borderRadius: '12px', textAlign: 'center', marginBottom: '16px',
      }}>
        <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.3)', letterSpacing: '1px', marginBottom: '6px' }}>ONDA ENCANTADA</div>
        <div style={{ fontSize: '28px', marginBottom: '2px' }}>{maya.onda.glyph}</div>
        <div style={{ fontSize: '18px', color: '#f472b6', fontWeight: 'bold' }}>{maya.onda.name}</div>
        <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.4)', marginTop: '4px' }}>{maya.onda.meaning}</div>
      </div>

      {/* ─── SELLO SOLAR (NAWAL) ─────────────────────────────────────── */}
      <div style={{
        maxWidth: '520px', width: '100%', padding: '18px',
        background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: '12px', textAlign: 'center', marginBottom: '16px',
      }}>
        <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.3)', letterSpacing: '1px', marginBottom: '6px' }}>SELLO SOLAR (NAWAL)</div>
        <div style={{ fontSize: '15px', color: '#fff' }}>
          {maya.sello.glyph} <strong>{maya.sello.nawal}</strong> — {maya.sello.meaning}
        </div>
      </div>

      {/* ─── REFERENCIA CIENTÍFICA ───────────────────────────────────── */}
      <div style={{
        maxWidth: '520px', width: '100%', padding: '16px',
        background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)',
        borderRadius: '8px', marginBottom: '28px',
      }}>
        <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.25)', letterSpacing: '1px', marginBottom: '8px', textAlign: 'center' }}>
          REFERENCIA CIENTÍFICA
        </div>
        <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.35)', lineHeight: '1.8', textAlign: 'center' }}>
          Correlación GMT: <strong style={{ color: 'rgba(255,255,255,0.5)' }}>584283</strong> · 
          Inicio Cuenta Larga: <strong style={{ color: 'rgba(255,255,255,0.5)' }}>11 ago 3114 a.C.</strong><br/>
          Día 0.0.0.0.0 = 4 Ahau 8 Kumku · Sistema vigesimal (base 20)<br/>
          1 Tun = 360 días · 1 Katun = 7,200 días · 1 Baktun = 144,000 días
        </div>
      </div>

      <button
        onClick={() => router.push('/menu')}
        style={{
          padding: '16px 60px', fontSize: '20px', fontWeight: 'bold', color: '#fff',
          background: 'transparent', border: '2px solid #fff', borderRadius: '8px',
          cursor: 'pointer', letterSpacing: '2px', textTransform: 'uppercase', transition: 'all 0.3s',
        }}
        onMouseEnter={(e) => { e.currentTarget.style.background = '#fff'; e.currentTarget.style.color = '#000' }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#fff' }}
      >
        Volver
      </button>
    </main>
  )
}
