'use client'

import { useRouter } from 'next/navigation'

export default function CalendariosPage() {
  const router = useRouter()

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 50%, #0a0a1a 100%)',
      margin: 0, padding: '40px 20px', color: '#fff',
    }}>
      <h1 style={{ fontSize: '42px', marginBottom: '8px', letterSpacing: '6px', fontFamily: 'Archeoscope, serif', color: '#fbbf24' }}>
        CALENDARIOS ANTIGUOS
      </h1>
      <p style={{ fontSize: '13px', color: 'rgba(255,255,255,0.35)', marginBottom: '50px', letterSpacing: '2px' }}>
        Sistemas de medición del tiempo de la civilización Maya
      </p>

      <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', justifyContent: 'center', maxWidth: '1000px' }}>

        {/* Tzolk'in Arqueológico */}
        <div
          onClick={() => router.push('/menu/calendarios/tzolkin')}
          style={{
            width: '280px', padding: '32px 24px', cursor: 'pointer',
            background: 'rgba(251,191,36,0.05)', border: '1px solid rgba(251,191,36,0.3)',
            borderRadius: '16px', textAlign: 'center', transition: 'all 0.3s',
          }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(251,191,36,0.12)'; (e.currentTarget as HTMLDivElement).style.borderColor = '#fbbf24' }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(251,191,36,0.05)'; (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(251,191,36,0.3)' }}
        >
          <div style={{ fontSize: '44px', marginBottom: '10px' }}>🏛️</div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#fbbf24', fontFamily: 'Archeoscope, serif', marginBottom: '6px' }}>Tzolk'in Clásico</div>
          <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '12px' }}>ARQUEOLÓGICO · GMT 584283</div>
          <p style={{ fontSize: '12px', color: 'rgba(255,255,255,0.55)', lineHeight: '1.7' }}>Sistema original maya. Cuenta Larga + Tzolk'in + Haab.</p>
          <div style={{ marginTop: '12px', fontSize: '11px', color: 'rgba(251,191,36,0.6)' }}>21 dic 2012 = 4 Ahau ✓</div>
        </div>

        {/* Dreamspell */}
        <div
          onClick={() => router.push('/menu/calendarios/dreamspell')}
          style={{
            width: '280px', padding: '32px 24px', cursor: 'pointer',
            background: 'rgba(167,139,250,0.05)', border: '1px solid rgba(167,139,250,0.3)',
            borderRadius: '16px', textAlign: 'center', transition: 'all 0.3s',
          }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(167,139,250,0.12)'; (e.currentTarget as HTMLDivElement).style.borderColor = '#a78bfa' }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(167,139,250,0.05)'; (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(167,139,250,0.3)' }}
        >
          <div style={{ fontSize: '44px', marginBottom: '10px' }}>🌀</div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#a78bfa', fontFamily: 'Archeoscope, serif', marginBottom: '6px' }}>Sincronario 13 Lunas</div>
          <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '12px' }}>DREAMSPELL · ARGÜELLES</div>
          <p style={{ fontSize: '12px', color: 'rgba(255,255,255,0.55)', lineHeight: '1.7' }}>Kin del día, Onda Encantada, Luna Galáctica. Reinicia 26 julio.</p>
          <div style={{ marginTop: '12px', fontSize: '11px', color: 'rgba(167,139,250,0.6)' }}>26 jul 1987 = Kin 24 ✓</div>
        </div>

        {/* Sexagesimal */}
        <div
          onClick={() => router.push('/menu/calendarios/sexagesimal')}
          style={{
            width: '280px', padding: '32px 24px', cursor: 'pointer',
            background: 'rgba(56,189,248,0.05)', border: '1px solid rgba(56,189,248,0.3)',
            borderRadius: '16px', textAlign: 'center', transition: 'all 0.3s',
          }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(56,189,248,0.12)'; (e.currentTarget as HTMLDivElement).style.borderColor = '#38bdf8' }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(56,189,248,0.05)'; (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(56,189,248,0.3)' }}
        >
          <div style={{ fontSize: '44px', marginBottom: '10px' }}>⚡</div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#38bdf8', fontFamily: 'Archeoscope, serif', marginBottom: '6px' }}>Calendario Babilónico</div>
          <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '12px' }}>SEXAGESIMAL · BASE 60</div>
          <p style={{ fontSize: '12px', color: 'rgba(255,255,255,0.55)', lineHeight: '1.7' }}>6 ciclos × 60 días. Coordenadas celestes RA/Dec. Origen del tiempo moderno.</p>
          <div style={{ marginTop: '12px', fontSize: '11px', color: 'rgba(56,189,248,0.6)' }}>60 min/h · 360° · RA/Dec ✓</div>
        </div>
      </div>

      <button
        onClick={() => router.push('/menu')}
        style={{
          marginTop: '48px', padding: '14px 50px', fontSize: '18px', fontWeight: 'bold',
          color: '#fff', background: 'transparent', border: '2px solid rgba(255,255,255,0.3)',
          borderRadius: '8px', cursor: 'pointer', letterSpacing: '2px', textTransform: 'uppercase', transition: 'all 0.3s',
        }}
        onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#fff' }}
        onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)' }}
      >
        Volver
      </button>
    </main>
  )
}
