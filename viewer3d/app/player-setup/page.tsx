'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'
import { PlayerState, DEFAULT_PLAYER_STATE, savePlayerState } from '@/types/player'
import { lockLandscape, enterFullscreen, unlockOrientation, isPortrait } from '@/lib/landscapeLock'

const ShipPreview = dynamic(() => import('@/components/ShipPreview'), {
  ssr: false,
  loading: () => (
    <div style={{
      width: '100%', height: '100%',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: '#0a0a0a', border: '2px solid #ffffff',
      borderRadius: '8px', color: '#ffffff', fontSize: '12px'
    }}>
      Cargando...
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
  const [showPortraitOverlay, setShowPortraitOverlay] = useState(false)

  useEffect(() => {
    const check = () => setIsMobile(
      /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
    )
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])

  // Forzar landscape en mobile
  useEffect(() => {
    if (!isMobile) return

    const initLandscape = async () => {
      await enterFullscreen()
      const locked = await lockLandscape()
      if (!locked) {
        const checkOrientation = () => setShowPortraitOverlay(isPortrait())
        checkOrientation()
        window.addEventListener('resize', checkOrientation)
        window.addEventListener('orientationchange', checkOrientation)
        return () => {
          window.removeEventListener('resize', checkOrientation)
          window.removeEventListener('orientationchange', checkOrientation)
        }
      }
    }
    initLandscape()
    return () => { unlockOrientation() }
  }, [isMobile])

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
    if (isMobile) {
      sessionStorage.setItem('mobile_game_active', 'true')
      router.push('/mobile-game')
    } else {
      router.push('/training')
    }
  }

  // ═══════════════════════════════════════════════════════════════════════
  // PORTRAIT OVERLAY — pedir que rote
  // ═══════════════════════════════════════════════════════════════════════
  if (isMobile && showPortraitOverlay) {
    return (
      <div style={{
        width: '100vw', height: '100vh', background: '#000',
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
        color: '#fff', textAlign: 'center', padding: '20px'
      }}>
        <div style={{ fontSize: '60px', marginBottom: '16px' }}>📱↔️</div>
        <h2 style={{ fontSize: '22px', marginBottom: '8px' }}>Rota tu dispositivo</h2>
        <p style={{ fontSize: '14px', color: '#888' }}>Usa el modo horizontal para jugar</p>
      </div>
    )
  }

  // ═══════════════════════════════════════════════════════════════════════
  // MOBILE LAYOUT — HORIZONTAL (landscape)
  // Izquierda: visor 3D con flechas
  // Derecha: info + nombre + botones
  // ═══════════════════════════════════════════════════════════════════════
  if (isMobile) {
    return (
      <main style={{
        width: '100vw', height: '100vh', background: '#000',
        display: 'flex', flexDirection: 'row',
        padding: '12px', boxSizing: 'border-box', gap: '12px',
        overflow: 'hidden'
      }}>
        {/* IZQUIERDA — Visor 3D cuadrado */}
        <div style={{
          display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center',
          gap: '8px', width: '45%', flexShrink: 0
        }}>
          {/* Flechas + visor */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', width: '100%', flex: 1, minHeight: 0 }}>
            <button onClick={handlePrevShip} style={arrowBtn}>‹</button>
            {/* Contenedor cuadrado para el visor — evita estiramiento */}
            <div style={{
              flex: 1, aspectRatio: '1 / 1', maxHeight: '100%',
              position: 'relative', overflow: 'hidden', borderRadius: '8px'
            }}>
              <div style={{ position: 'absolute', inset: 0 }}>
                <ShipPreview shipModel={ships[selectedShip].model} />
              </div>
            </div>
            <button onClick={handleNextShip} style={arrowBtn}>›</button>
          </div>
          {/* Emoji nave */}
          <div style={{ color: '#fff', fontSize: '20px' }}>{ships[selectedShip].name}</div>
        </div>

        {/* DERECHA — Info + controles */}
        <div style={{
          flex: 1, display: 'flex', flexDirection: 'column',
          justifyContent: 'space-between', minWidth: 0
        }}>
          {/* Título */}
          <h1 style={{ color: '#fff', fontSize: '16px', margin: 0, letterSpacing: '2px', textAlign: 'center' }}>
            CONFIGURACIÓN
          </h1>

          {/* Info nave */}
          <div style={{
            background: '#0a0a0a', border: '1px solid #4a9eff',
            borderRadius: '8px', padding: '8px', fontSize: '11px', color: '#fff', flex: 1,
            margin: '8px 0', overflow: 'hidden'
          }}>
            <div style={{ color: '#4a9eff', fontWeight: 'bold', marginBottom: '3px', fontSize: '12px' }}>
              {ships[selectedShip].specialty}
            </div>
            <div style={{ color: '#ccc', marginBottom: '3px' }}>{ships[selectedShip].description}</div>
            <div style={{ color: '#4a9eff' }}>{ships[selectedShip].ability}</div>
          </div>

          {/* Input nombre */}
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            maxLength={20}
            placeholder="Nombre del Piloto"
            style={{
              padding: '10px', fontSize: '14px', background: 'transparent',
              border: '2px solid #fff', borderRadius: '8px', color: '#fff',
              outline: 'none', textAlign: 'center', marginBottom: '8px'
            }}
          />

          {/* Botones */}
          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={() => router.push('/menu')} style={btn(true)}>Volver</button>
            <button onClick={handleStart} disabled={!playerName.trim()} style={btn(!!playerName.trim(), true)}>
              Comenzar
            </button>
          </div>
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
          <button onClick={handlePrevShip} style={arrowBtnPC}>‹</button>
          <div style={{ flex: 1, height: '100%' }}>
            <ShipPreview shipModel={ships[selectedShip].model} />
          </div>
          <button onClick={handleNextShip} style={arrowBtnPC}>›</button>
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
          <button onClick={() => router.push('/menu')} style={btnPC(true)}>Volver</button>
          <button onClick={handleStart} disabled={!playerName.trim()} style={btnPC(!!playerName.trim(), true)}>
            Comenzar
          </button>
        </div>
      </div>
    </main>
  )
}

// ─── Estilos ────────────────────────────────────────────────────────────────
const arrowBtn: React.CSSProperties = {
  width: 36, height: 36, fontSize: 22, color: '#fff', background: 'transparent',
  border: '2px solid #fff', borderRadius: '50%', cursor: 'pointer', flexShrink: 0,
  display: 'flex', alignItems: 'center', justifyContent: 'center'
}
const arrowBtnPC: React.CSSProperties = {
  width: 60, height: 60, fontSize: 32, color: '#fff', background: 'transparent',
  border: '2px solid #fff', borderRadius: '50%', cursor: 'pointer', flexShrink: 0,
  display: 'flex', alignItems: 'center', justifyContent: 'center'
}
const btn = (enabled: boolean, primary = false): React.CSSProperties => ({
  flex: 1, padding: '10px', fontSize: '13px', fontWeight: 'bold',
  color: primary && enabled ? '#000' : '#fff',
  background: primary && enabled ? '#fff' : 'transparent',
  border: `2px solid ${enabled ? '#fff' : '#666'}`,
  borderRadius: '8px', cursor: enabled ? 'pointer' : 'not-allowed',
  opacity: enabled ? 1 : 0.5, letterSpacing: '1px', textTransform: 'uppercase'
})
const btnPC = (enabled: boolean, primary = false): React.CSSProperties => ({
  flex: 1, padding: '20px', fontSize: '20px',
  color: primary && enabled ? '#000' : '#fff',
  background: primary && enabled ? '#fff' : 'transparent',
  border: `2px solid ${enabled ? '#fff' : '#666'}`,
  borderRadius: '8px', cursor: enabled ? 'pointer' : 'not-allowed',
  opacity: enabled ? 1 : 0.5, letterSpacing: '2px', textTransform: 'uppercase'
})
