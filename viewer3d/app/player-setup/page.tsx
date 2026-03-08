'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'
import { PlayerState, DEFAULT_PLAYER_STATE, savePlayerState } from '@/types/player'

// Importar ShipPreview dinámicamente para evitar SSR issues
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
  { 
    id: 'ufo_1', 
    name: '🌫️ Phantom', 
    model: '/ufo_1.glb',
    specialty: 'Cloaking / Invisibilidad',
    description: 'Especialidad: infiltración y espionaje',
    ability: 'Habilidad principal: camuflaje óptico',
    missions: 'Tipo de misiones: infiltración, espionaje, recuperar artefactos, entrar a ruinas antiguas'
  },
  { 
    id: 'ufo_2', 
    name: '🛡️ Aegis', 
    model: '/ufo_2.glb',
    specialty: 'Defensa / Campo EM',
    description: 'Especialidad: protección y control físico',
    ability: 'Habilidad principal: campo electromagnético',
    missions: 'Tipo de misiones: atravesar campos de asteroides, rescates, misiones de escolta, limpiar escombros espaciales'
  },
  { 
    id: 'ufo_3', 
    name: '⚡ Vector', 
    model: '/ufo_3.glb',
    specialty: 'Velocidad / Teletransporte',
    description: 'Especialidad: movilidad extrema',
    ability: 'Habilidad principal: salto cuántico',
    missions: 'Tipo de misiones: carreras, persecuciones, exploración, entrega urgente'
  },
  { 
    id: 'ufo_4', 
    name: '🔬 Oracle', 
    model: '/ufo_4.glb',
    specialty: 'Ciencia / Escaneo',
    description: 'Especialidad: conocimiento y análisis',
    ability: 'Habilidad principal: escáner cuántico',
    missions: 'Tipo de misiones: exploración planetaria, arqueología alienígena, investigación, cartografía'
  },
  { 
    id: 'ufo_5', 
    name: '💣 Titan', 
    model: '/ufo_5.glb',
    specialty: 'Fuerza Bruta / Impacto',
    description: 'Especialidad: potencia y resistencia',
    ability: 'Habilidad principal: masa + potencia',
    missions: 'Tipo de misiones: combate, minería pesada, abrir rutas, destruir obstáculos'
  }
]

export default function PlayerSetupPage() {
  const router = useRouter()
  const [selectedShip, setSelectedShip] = useState(0)
  const [playerName, setPlayerName] = useState('')

  const handlePrevShip = () => {
    setSelectedShip((prev) => (prev === 0 ? ships.length - 1 : prev - 1))
  }

  const handleNextShip = () => {
    setSelectedShip((prev) => (prev === ships.length - 1 ? 0 : prev + 1))
  }

  const handleStart = () => {
    if (playerName.trim()) {
      // Crear estado completo del jugador
      const playerState: PlayerState = {
        ...DEFAULT_PLAYER_STATE,
        playerName: playerName.trim(),
        ship: ships[selectedShip],
        createdAt: new Date().toISOString(),
        lastPlayed: new Date().toISOString()
      }
      
      // Guardar estado completo en localStorage
      savePlayerState(playerState)
      
      // También guardar referencias individuales para compatibilidad
      localStorage.setItem('playerName', playerName)
      localStorage.setItem('selectedShip', ships[selectedShip].model)
      
      // Activar flag de sesión activa (solo para esta sesión)
      sessionStorage.setItem('game_session_active', 'true')
      
      console.log('🎮 Jugador configurado:', playerState)
      
      // Ir al juego
      router.push('/game')
    }
  }

  return (
    <main style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      background: '#000000',
      margin: 0,
      padding: '40px',
      boxSizing: 'border-box',
      gap: '40px'
    }}>
      {/* Visor 3D - Izquierda */}
      <div style={{
        flex: '1',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px'
      }}>
        <h2 style={{
          color: '#ffffff',
          fontSize: '32px',
          margin: 0,
          letterSpacing: '2px',
          textAlign: 'center'
        }}>
          ðŸŒ
        </h2>
        
        {/* Visor con flechas de navegación */}
        <div style={{ 
          flex: 1,
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          gap: '20px'
        }}>
          {/* Flecha Izquierda */}
          <button
            onClick={handlePrevShip}
            style={{
              width: '60px',
              height: '60px',
              fontSize: '32px',
              color: '#ffffff',
              background: 'transparent',
              border: '2px solid #ffffff',
              borderRadius: '50%',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#ffffff'
              e.currentTarget.style.color = '#000000'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = '#ffffff'
            }}
          >
            ‹
          </button>

          {/* Visor 3D */}
          <div style={{ flex: 1, height: '100%' }}>
            <ShipPreview shipModel={ships[selectedShip].model} />
          </div>

          {/* Flecha Derecha */}
          <button
            onClick={handleNextShip}
            style={{
              width: '60px',
              height: '60px',
              fontSize: '32px',
              color: '#ffffff',
              background: 'transparent',
              border: '2px solid #ffffff',
              borderRadius: '50%',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#ffffff'
              e.currentTarget.style.color = '#000000'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = '#ffffff'
            }}
          >
            ›
          </button>
        </div>
        
        <div style={{
          color: '#ffffff',
          fontSize: '28px',
          textAlign: 'center',
          letterSpacing: '1px',
          fontWeight: 'bold'
        }}>
          {ships[selectedShip].name}
        </div>
      </div>

      {/* Panel de Configuración - Derecha */}
      <div style={{
        flex: '1',
        display: 'flex',
        flexDirection: 'column',
        gap: '30px',
        justifyContent: 'center',
        padding: '0 40px'
      }}>
        <h1 style={{
          color: '#ffffff',
          fontSize: '48px',
          margin: 0,
          letterSpacing: '4px',
          textAlign: 'center'
        }}>
          CONFIGURACIÓN
        </h1>

        {/* Nombre del Jugador */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '10px'
        }}>
          <label style={{
            color: '#ffffff',
            fontSize: '20px',
            letterSpacing: '2px',
            textTransform: 'uppercase'
          }}>
            Nombre del Piloto
          </label>
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            maxLength={20}
            placeholder="Ingresa tu nombre"
            style={{
              padding: '15px 20px',
              fontSize: '20px',
              background: 'transparent',
              border: '2px solid #ffffff',
              borderRadius: '8px',
              color: '#ffffff',
              fontFamily: 'inherit',
              letterSpacing: '1px',
              outline: 'none'
            }}
            onFocus={(e) => {
              e.currentTarget.style.borderColor = '#4a9eff'
            }}
            onBlur={(e) => {
              e.currentTarget.style.borderColor = '#ffffff'
            }}
          />
        </div>

        {/* Descripción de la Nave */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '15px',
          padding: '25px',
          background: '#0a0a0a',
          border: '2px solid #4a9eff',
          borderRadius: '8px',
          minHeight: '280px'
        }}>
          <div style={{
            color: '#4a9eff',
            fontSize: '22px',
            fontWeight: 'bold',
            letterSpacing: '1px',
            textTransform: 'uppercase',
            borderBottom: '1px solid #4a9eff',
            paddingBottom: '10px'
          }}>
            {ships[selectedShip].specialty}
          </div>
          
          <div style={{
            color: '#ffffff',
            fontSize: '18px',
            lineHeight: '1.6',
            letterSpacing: '0.5px'
          }}>
            {ships[selectedShip].description}
          </div>
          
          <div style={{
            color: '#ffffff',
            fontSize: '18px',
            lineHeight: '1.6',
            letterSpacing: '0.5px'
          }}>
            <span style={{ color: '#4a9eff', fontWeight: 'bold' }}>
              {ships[selectedShip].ability}
            </span>
          </div>
          
          <div style={{
            color: '#cccccc',
            fontSize: '16px',
            lineHeight: '1.6',
            letterSpacing: '0.5px',
            marginTop: '10px'
          }}>
            <span style={{ color: '#4a9eff', fontWeight: 'bold' }}>
              {ships[selectedShip].missions}
            </span>
          </div>
        </div>

        {/* Botones de Acción */}
        <div style={{
          display: 'flex',
          gap: '20px',
          marginTop: '20px'
        }}>
          <button
            onClick={() => router.push('/menu')}
            style={{
              flex: 1,
              padding: '20px',
              fontSize: '20px',
              color: '#ffffff',
              background: 'transparent',
              border: '2px solid #ffffff',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              letterSpacing: '2px',
              textTransform: 'uppercase'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#ffffff'
              e.currentTarget.style.color = '#000000'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = '#ffffff'
            }}
          >
            Volver
          </button>
          
          <button
            onClick={handleStart}
            disabled={!playerName.trim()}
            style={{
              flex: 1,
              padding: '20px',
              fontSize: '20px',
              color: playerName.trim() ? '#000000' : '#666666',
              background: playerName.trim() ? '#ffffff' : '#333333',
              border: '2px solid ' + (playerName.trim() ? '#ffffff' : '#666666'),
              borderRadius: '8px',
              cursor: playerName.trim() ? 'pointer' : 'not-allowed',
              transition: 'all 0.3s ease',
              letterSpacing: '2px',
              textTransform: 'uppercase',
              opacity: playerName.trim() ? 1 : 0.5
            }}
            onMouseEnter={(e) => {
              if (playerName.trim()) {
                e.currentTarget.style.background = '#4a9eff'
                e.currentTarget.style.borderColor = '#4a9eff'
              }
            }}
            onMouseLeave={(e) => {
              if (playerName.trim()) {
                e.currentTarget.style.background = '#ffffff'
                e.currentTarget.style.borderColor = '#ffffff'
              }
            }}
          >
            Comenzar
          </button>
        </div>
      </div>
    </main>
  )
}
