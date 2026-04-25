'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'
import { PlayerState, DEFAULT_PLAYER_STATE, savePlayerState } from '@/types/player'

const ShipPreview = dynamic(() => import('@/components/ShipPreview'), {
  ssr: false,
  loading: () => (
    <div style={{
      width: '100%',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#0a0a0a',
      border: '2px solid #ffffff',
      borderRadius: '8px',
      color: '#ffffff'
    }}>
      Cargando nave...
    </div>
  )
})

const ships = [
  { id: 'ufo_1', name: '🌫️', model: '/ufo_1.glb', specialty: 'Cloaking / Invisibilidad', description: 'Infiltración y espionaje', ability: 'Camuflaje óptico', missions: 'Infiltración, espionaje, recuperar artefactos' },
  { id: 'ufo_2', name: '🛡️', model: '/ufo_2.glb', specialty: 'Defensa / Campo EM', description: 'Protección y control físico', ability: 'Campo electromagnético', missions: 'Defensa, protección de sitios, control de amenazas' },
  { id: 'ufo_3', name: '⚡', model: '/ufo_3.glb', specialty: 'Velocidad / Teletransporte', description: 'Movilidad extrema', ability: 'Salto cuántico', missions: 'Exploración rápida, rescate, reconocimiento' },
  { id: 'ufo_4', name: '🔬', model: '/ufo_4.glb', specialty: 'Ciencia / Escaneo', description: 'Conocimiento y análisis', ability: 'Escáner cuántico', missions: 'Análisis, investigación, descifrar misterios' },
  { id: 'ufo_5', name: '💣', model: '/ufo_5.glb', specialty: 'Fuerza Bruta / Impacto', description: 'Potencia y resistencia', ability: 'Masa + potencia', missions: 'Mover estructuras, fuerza bruta, excavación' }
]

export default function PlayerSetupPage() {
  const router = useRouter()
  const [selectedShip, setSelectedShip] = useState(0)
  const [playerName, setPlayerName] = useState('')
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const check = () => setIsMobile(
      /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
    )
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])

  const handlePrevShip = () => setSelectedShip(p => (p === 0 ? ships.length - 1 : p - 1))
  const handleNextShip = () => setSelectedShip(p => (p === ships.length - 1 ? 0 : p + 1))

  const handleStart = () => {
    if (!playerName.trim()) return

    const playerState: PlayerState = {
      ...DEFAULT_PLAYER_STATE,
      playerName: playerName.trim(),
      ship: ships[selectedShip],
      createdAt: new Date().toISOString(),
      lastPlayed: new Date().toISOString()
    }
    savePlayerState(playerState)
    localStorage.setItem('playerName', playerName)
    localStorage.setItem('selectedShip', ships[selectedShip].model)
    sessionStorage.setItem('game_session_active', 'true')

    // Mobile: directo a mobile-game (sin training)
    // PC: va a training
    if (isMobile) {
      // Marcar partida mobile activa para poder continuar desde menú
      sessionStorage.setItem('mobile_game_active', 'true')
      router.push('/mobile-game')
    } else {
      router.push('/training')
    }
  }

  // ═══════════════════════════════════════════════════════════════════════
  // MOBILE LAYOUT — vertical, compacto
  // ═══════════════════════════════════════════════════════════════════════
  if (isMobile) {
    return (
      <main style={{
        width: '100vw', height: '100vh', background: '#000',
        display: 'flex', flexDirection: 'column', padding: '16px',
        boxSizing: 'border-box', gap: '12px', overflow: 'hidden'
      }}>
        {/* Título */}
        <h1 style={{ color: '#fff', fontSize: '20px', textAlign: 'center', margin: 0, letterSpacing: '2px' }}>
          CONFIGURACIÓN
        </h1>

        {/* Visor 3D con flechas */}
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: '8px', minHeight: 0 }}>
          <button onClick={handlePrevShip} style={arrowBtnStyle}>‹</button>
          <div style={{ flex: 1, height: '100%' }}>
            <ShipPreview shipModel={ships[selectedShip].model} />
          </div>
          <button onClick={handleNextShip} style={arrowBtnStyle}>›</button>
        </div>

        {/* Nombre nave */}
        <div style={{ color: '#fff', fontSize: '24px', textAlign: 'center' }}>
          {ships[selectedShip].name}
        </div>

        {/* Info nave compacta */}
        <div style={{
          background: '#0a0a0a', border: '1px solid #4a9eff', borderRadius: '8px',
          padding: '10px', fontSize: '12px', color: '#fff'
        }}>
          <div style={{ color: '#4a9eff', fontWeight: 'bold', marginBottom: '4px' }}>
            {ships[selectedShip].specialty}
          </div>
          <div>{ships[selectedShip].description}</div>
          <div style={{ color: '#4a9eff', marginTop: '4px' }}>{ships[selectedShip].ability}</div>
        </div>

        {/* Input nombre */}
        <input
          type="text"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
          maxLength={20}
          placeholder="Nombre del Piloto"
          style={{
            padding: '12px', fontSize: '16px', background: 'transparent',
            border: '2px solid #fff', borderRadius: '8px', color: '#fff',
            outline: 'none', textAlign: 'center'
          }}
        />

        {/* Botones */}
        <div style={{ display: 'flex', gap: '12px' }}>
          <button onClick={() => router.push('/menu')} style={btnStyle(true)}>Volver</button>
          <button onClick={handleStart} disabled={!playerName.trim()} style={btnStyle(!!playerName.trim(), true)}>
            Comenzar
          </button>
        </div>
      </main>
    )
  }

  // ═══════════════════════════════════════════════════════════════════════
  // PC LAYOUT — horizontal, original
  // ═══════════════════════════════════════════════════════════════════════
  return (
    <main style={{
      width: '100vw', height: '100vh', display: 'flex', background: '#000',
      margin: 0, padding: '40px', boxSizing: 'border-box', gap: '40px'
    }}>
      {/* Visor 3D - Izquierda */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <h2 style={{ color: '#fff', fontSize: '32px', margin: 0, textAlign: 'center' }}>🌌</h2>
        <div style={{ flex: 1, position: 'relative', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <button onClick={handlePrevShip} style={arrowBtnStylePC}>‹</button>
          <div style={{ flex: 1, height: '100%' }}>
            <ShipPreview shipModel={ships[selectedShip].model} />
          </div>
          <button onClick={handleNextShip} style={arrowBtnStylePC}>›</button>
        </div>
        <div style={{ color: '#fff', fontSize: '28px', textAlign: 'center', fontWeight: 'bold' }}>
          {ships[selectedShip].name}
        </div>
      </div>

      {/* Panel Configuración - Derecha */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '30px', justifyContent: 'center', padding: '0 40px' }}>
        <h1 style={{ color: '#fff', fontSize: '48px', margin: 0, letterSpacing: '4px', textAlign: 'center' }}>
          CONFIGURACIÓN
        </h1>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <label style={{ color: '#fff', fontSize: '20px', letterSpacing: '2px', textTransform: 'uppercase' }}>
            Nombre del Piloto
          </label>
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            maxLength={20}
            placeholder="Ingresa tu nombre"
            style={{
              padding: '15px 20px', fontSize: '20px', background: 'transparent',
              border: '2px solid #fff', borderRadius: '8px', color: '#fff', outline: 'none'
            }}
          />
        </div>

        <div style={{
          display: 'flex', flexDirection: 'column', gap: '15px', padding: '25px',
          background: '#0a0a0a', border: '2px solid #4a9eff', borderRadius: '8px', minHeight: '200px'
        }}>
          <div style={{ color: '#4a9eff', fontSize: '22px', fontWeight: 'bold', borderBottom: '1px solid #4a9eff', paddingBottom: '10px' }}>
            {ships[selectedShip].specialty}
          </div>
          <div style={{ color: '#fff', fontSize: '18px', lineHeight: 1.6 }}>{ships[selectedShip].description}</div>
          <div style={{ color: '#4a9eff', fontSize: '18px', fontWeight: 'bold' }}>{ships[selectedShip].ability}</div>
        </div>

        <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
          <button onClick={() => router.push('/menu')} style={btnStylePC(true)}>Volver</button>
          <button onClick={handleStart} disabled={!playerName.trim()} style={btnStylePC(!!playerName.trim(), true)}>
            Comenzar
          </button>
        </div>
      </div>
    </main>
  )
}

// Estilos helpers
const arrowBtnStyle: React.CSSProperties = {
  width: 40, height: 40, fontSize: 24, color: '#fff', background: 'transparent',
  border: '2px solid #fff', borderRadius: '50%', cursor: 'pointer', flexShrink: 0
}
const arrowBtnStylePC: React.CSSProperties = {
  width: 60, height: 60, fontSize: 32, color: '#fff', background: 'transparent',
  border: '2px solid #fff', borderRadius: '50%', cursor: 'pointer', flexShrink: 0,
  display: 'flex', alignItems: 'center', justifyContent: 'center'
}
const btnStyle = (enabled: boolean, primary = false): React.CSSProperties => ({
  flex: 1, padding: '14px', fontSize: '14px', fontWeight: 'bold',
  color: primary && enabled ? '#000' : '#fff',
  background: primary && enabled ? '#fff' : 'transparent',
  border: `2px solid ${enabled ? '#fff' : '#666'}`,
  borderRadius: '8px', cursor: enabled ? 'pointer' : 'not-allowed',
  opacity: enabled ? 1 : 0.5, letterSpacing: '1px', textTransform: 'uppercase'
})
const btnStylePC = (enabled: boolean, primary = false): React.CSSProperties => ({
  flex: 1, padding: '20px', fontSize: '20px',
  color: primary && enabled ? '#000' : '#fff',
  background: primary && enabled ? '#fff' : 'transparent',
  border: `2px solid ${enabled ? '#fff' : '#666'}`,
  borderRadius: '8px', cursor: enabled ? 'pointer' : 'not-allowed',
  opacity: enabled ? 1 : 0.5, letterSpacing: '2px', textTransform: 'uppercase'
})
