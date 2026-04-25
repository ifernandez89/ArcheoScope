'use client'

import { useRouter } from 'next/navigation'

export default function CalendariosPage() {
  const router = useRouter()

  return (
    <main style={{
      width: '100vw', minHeight: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 50%, #0a0a1a 100%)',
      margin: 0, padding: '40px 20px', color: '#fff', overflowY: 'auto',
    }}>
      <h1 className="title-responsive" style={{ color: '#fbbf24' }}>
        CALENDARIOS ANTIGUOS
      </h1>
      <p className="subtitle-responsive" style={{ marginBottom: '50px' }}>
        Sistemas de medición del tiempo de la civilización Maya y Mesopotamia
      </p>

      <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', justifyContent: 'center', maxWidth: '1000px' }}>

        {/* Tzolk'in Arqueológico */}
        <div
          onClick={() => router.push('/menu/calendarios/tzolkin')}
          className="cal-card info-card"
          style={{
            maxWidth: '300px', padding: '32px 24px', cursor: 'pointer',
            background: 'rgba(251,191,36,0.05)', border: '1px solid rgba(251,191,36,0.3)',
            transition: 'all 0.3s',
          }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(251,191,36,0.12)'; (e.currentTarget as HTMLDivElement).style.borderColor = '#fbbf24' }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(251,191,36,0.05)'; (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(251,191,36,0.3)' }}
        >
          <div style={{ fontSize: '44px', marginBottom: '10px' }}>🏛️</div>
          <h2 style={{ color: '#fbbf24' }}>Tzolk'in Clásico</h2>
          <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '12px' }}>ARQUEOLÓGICO · GMT 584283</div>
          <p className="text-responsive" style={{ color: 'rgba(255,255,255,0.6)' }}>Sistema original maya. Cuenta Larga + Tzolk'in + Haab.</p>
          <div style={{ marginTop: '12px', fontSize: '15px', color: 'rgba(251,191,36,0.6)' }}>21 dic 2012 = 4 Ahau ✓</div>
        </div>

        {/* Cholq'ij */}
        <div
          onClick={() => router.push('/menu/calendarios/dreamspell')}
          className="cal-card info-card"
          style={{
            maxWidth: '300px', padding: '32px 24px', cursor: 'pointer',
            background: 'rgba(167,139,250,0.05)', border: '1px solid rgba(167,139,250,0.3)',
            transition: 'all 0.3s',
          }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(167,139,250,0.12)'; (e.currentTarget as HTMLDivElement).style.borderColor = '#a78bfa' }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(167,139,250,0.05)'; (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(167,139,250,0.3)' }}
        >
          <div style={{ fontSize: '44px', marginBottom: '10px' }}>🌀</div>
          <h2 style={{ color: '#a78bfa' }}>Cholq'ij</h2>
          <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '12px' }}>SAGRADO MAYA · 260 DÍAS</div>
          <p className="text-responsive" style={{ color: 'rgba(255,255,255,0.6)' }}>13 números × 20 nawales. Usado en ceremonias hasta hoy por los ajq'ijab'.</p>
          <div style={{ marginTop: '12px', fontSize: '15px', color: 'rgba(167,139,250,0.6)' }}>8 Ajpu · 3 Kawoq · 1 Imox ✓</div>
        </div>

        {/* Sexagesimal */}
        <div
          onClick={() => router.push('/menu/calendarios/sexagesimal')}
          className="cal-card info-card"
          style={{
            maxWidth: '300px', padding: '32px 24px', cursor: 'pointer',
            background: 'rgba(56,189,248,0.05)', border: '1px solid rgba(56,189,248,0.3)',
            transition: 'all 0.3s',
          }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(56,189,248,0.12)'; (e.currentTarget as HTMLDivElement).style.borderColor = '#38bdf8' }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(56,189,248,0.05)'; (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(56,189,248,0.3)' }}
        >
          <div style={{ fontSize: '44px', marginBottom: '10px' }}>⚡</div>
          <h2 style={{ color: '#38bdf8' }}>Calendario Babilónico</h2>
          <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '12px' }}>SEXAGESIMAL · BASE 60</div>
          <p className="text-responsive" style={{ color: 'rgba(255,255,255,0.6)' }}>6 ciclos × 60 días. Coordenadas celestes RA/Dec. Origen del tiempo moderno.</p>
          <div style={{ marginTop: '12px', fontSize: '15px', color: 'rgba(56,189,248,0.6)' }}>60 min/h · 360° · RA/Dec ✓</div>
        </div>
      </div>

      <button
        onClick={() => router.push('/menu')}
        className="btn-responsive"
        style={{ marginTop: '48px' }}
        onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#fff' }}
        onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)' }}
      >
        Volver
      </button>
    </main>
  )
}
