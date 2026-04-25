'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import InventoryItem from './InventoryItem'
import { subscribeInventory, requestDrop, subscribeScan, type InventoryEntry } from './TrainingRoom'

export default function TrainingUI() {
  const router = useRouter()
  const [keys, setKeys] = useState<{ [key: string]: boolean }>({})
  const [showGlobeInfo, setShowGlobeInfo] = useState(false)
  const [inventory, setInventory] = useState<InventoryEntry[]>([])
  const [scanData, setScanData] = useState<{ name: string, desc: string } | null>(null)

  // Suscribirse al scan de Oracle
  useEffect(() => {
    const unsub = subscribeScan(setScanData)
    return unsub
  }, [])
  useEffect(() => {
    const unsub = subscribeInventory((items) => {
      setInventory([...items])
    })
    return unsub
  }, [])

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      setKeys(prev => ({ ...prev, [e.key.toLowerCase()]: true }))
      if (e.code === 'Space') setKeys(prev => ({ ...prev, space: true }))
    }
    const handleKeyUp = (e: KeyboardEvent) => {
      setKeys(prev => ({ ...prev, [e.key.toLowerCase()]: false }))
      if (e.code === 'Space') setKeys(prev => ({ ...prev, space: false }))
    }

    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('keyup', handleKeyUp)
    }

  }, [])

  const Key = ({ label, active, size = 60, width }: { label: string, active: boolean, size?: number, width?: number }) => (
    <div style={{
      width: width || size,
      height: size,
      background: active ? '#4a9eff' : 'rgba(100, 100, 100, 0.3)',
      border: `2px solid ${active ? '#4a9eff' : 'rgba(255, 255, 255, 0.4)'}`,
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: active ? '#000000' : '#ffffff',
      fontSize: size * 0.4,
      fontWeight: 'bold',
      transition: 'all 0.1s ease',
      boxShadow: active ? '0 0 15px #4a9eff' : 'none',
      fontFamily: 'monospace',
      backdropFilter: 'blur(4px)'
    }}>
      {label}
    </div>
  )

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      pointerEvents: 'none',
      padding: '40px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      color: '#ffffff',
      fontFamily: 'Archeoscope, serif',
      zIndex: 100
    }}>
      {/* Top Left: Title */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '32px', letterSpacing: '4px' }}>TRAINING ROOM</h1>
          <p style={{ margin: '5px 0 0', opacity: 0.6, fontSize: '14px' }}>MANUAL DE VUELO Y ACCIONES</p>
        </div>

        {/* Inventario visual - arriba a la derecha */}
        {inventory.length > 0 && (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
            pointerEvents: 'auto',
            alignItems: 'flex-end',
          }}>
            <div style={{
              fontSize: '12px',
              letterSpacing: '2px',
              color: '#ffd700',
              fontWeight: 'bold',
              marginBottom: '4px',
              textShadow: '0 0 8px rgba(255, 215, 0, 0.5)',
            }}>
              🎒 Inventario
            </div>
            <div style={{
              display: 'flex',
              gap: '8px',
              flexWrap: 'wrap',
              justifyContent: 'flex-end',
              maxWidth: '300px',
            }}>
              {inventory.map((item) => (
                <InventoryItem
                  key={item.id}
                  modelPath={item.modelPath}
                  itemName={item.itemName}
                  show={true}
                  onDrop={() => requestDrop(item.id)}
                />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Center Left: Controls */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div style={{ display: 'flex', gap: '10px', marginLeft: '70px' }}>
            <Key label="W" active={keys['w']} />
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <Key label="A" active={keys['a']} />
            <Key label="S" active={keys['s']} />
            <Key label="D" active={keys['d']} />
          </div>
          <p style={{ margin: '5px 0 0', fontSize: '16px', letterSpacing: '1px', opacity: 0.8 }}>NAVEGACIÓN BÁSICA</p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <Key label="SHIFT" active={keys['shift']} size={60} width={100} />
            <span style={{ fontSize: '20px' }}>+</span>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
              <div style={{ padding: '5px 10px', background: 'rgba(100,100,100,0.3)', border: '1px solid rgba(255,255,255,0.4)', borderRadius: '4px', fontSize: '10px' }}>MOUSE UP</div>
              <div style={{ padding: '5px 10px', background: 'rgba(100,100,100,0.3)', border: '1px solid rgba(255,255,255,0.4)', borderRadius: '4px', fontSize: '10px' }}>MOUSE DOWN</div>
            </div>
          </div>
          <p style={{ margin: '5px 0 0', fontSize: '16px', letterSpacing: '1px', opacity: 0.8 }}>ALTITUD Y VELOCIDAD</p>
        </div>

        <div style={{ display: 'flex', gap: '40px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            <div style={{ display: 'flex', gap: '10px' }}>
              <Key label="Q" active={keys['q']} />
              <Key label="E" active={keys['e']} />
            </div>
            <p style={{ margin: '5px 0 0', fontSize: '16px', letterSpacing: '1px', opacity: 0.8 }}>ROTACIÓN</p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            <div style={{ display: 'flex', gap: '10px' }}>
              <Key label="SPACE" active={keys['space']} size={60} width={150} />
            </div>
            <p style={{ margin: '5px 0 0', fontSize: '16px', letterSpacing: '1px', opacity: 0.8 }}>HABILIDAD ESPECIAL</p>
          </div>

        </div>
      </div>

      {/* Bottom Right: Interactions & Finish */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', pointerEvents: 'auto' }}>
        <div style={{ background: 'rgba(0,0,0,0.7)', padding: '20px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.2)', backdropFilter: 'blur(10px)' }}>
          <h3 style={{ margin: '0 0 15px', color: '#4a9eff' }}>INTERACCIONES</h3>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <li style={{ fontSize: '18px' }}>🖱️ Click en Roca → <span style={{ color: '#ffd700', fontWeight: 'bold' }}>&quot;JUNTAR&quot;</span> al inventario</li>
            <li style={{ fontSize: '18px' }}>🎒 Click en Inventario → <span style={{ color: '#ffd700', fontWeight: 'bold' }}>&quot;SOLTAR&quot;</span> al piso</li>
            <li style={{ fontSize: '18px' }}>♻️ Repetir <span style={{ color: '#4a9eff', fontWeight: 'bold' }}>infinitamente</span></li>
          </ul>
        </div>

        <button
          onClick={() => setShowGlobeInfo(true)}
          style={{
            padding: '20px 40px',
            fontSize: '20px',
            background: '#ffffff',
            color: '#000000',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            letterSpacing: '2px',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#4a9eff'
            e.currentTarget.style.color = '#ffffff'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = '#ffffff'
            e.currentTarget.style.color = '#000000'
          }}
        >
          FINALIZAR TUTORIAL
        </button>
      </div>

      {/* 🔬 Oracle: Scan HUD Overlay */}
      {scanData && (
        <div style={{
          position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
          background: 'rgba(0, 20, 30, 0.92)', border: '2px solid #00ffff',
          borderRadius: '12px', padding: '30px 40px', maxWidth: '500px', width: '90%',
          textAlign: 'center', zIndex: 200, pointerEvents: 'none',
          boxShadow: '0 0 40px rgba(0, 255, 255, 0.3)',
          animation: 'scanIn 0.3s ease-out',
        }}>
          <div style={{ fontSize: '10px', marginBottom: '8px', opacity: 0.8, letterSpacing: '2px', color: '#00ffff' }}>
            📡 ORACLE_SCAN // SIGNATURE_IDENTIFIED
          </div>
          <div style={{ fontSize: '28px', fontWeight: '900', marginBottom: '12px', letterSpacing: '4px', textShadow: '0 0 10px #00ffff', color: '#fff' }}>
            {scanData.name}
          </div>
          <div style={{ fontSize: '15px', color: 'rgba(255,255,255,0.8)', lineHeight: '1.7', fontStyle: 'italic' }}>
            {scanData.desc}
          </div>
          <div style={{ marginTop: '16px', height: '3px', background: 'rgba(0, 255, 255, 0.2)', borderRadius: '2px', overflow: 'hidden' }}>
            <div style={{ height: '100%', background: '#00ffff', animation: 'scanBar 2s linear' }} />
          </div>
          <style>{`
            @keyframes scanIn { from { opacity: 0; transform: translate(-50%, -50%) scale(0.9); } to { opacity: 1; transform: translate(-50%, -50%) scale(1); } }
            @keyframes scanBar { from { width: 0%; } to { width: 100%; } }
          `}</style>
        </div>
      )}

      {/* Globe Info Modal */}
      {showGlobeInfo && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0,0,0,0.9)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          pointerEvents: 'auto'
        }}>
          <div style={{
            maxWidth: '600px',
            background: '#111',
            padding: '40px',
            borderRadius: '16px',
            border: '2px solid #4a9eff',
            textAlign: 'center',
            boxShadow: '0 0 50px rgba(74, 158, 255, 0.3)'
          }}>
            <h2 style={{ color: '#4a9eff', marginBottom: '30px', fontSize: '28px' }}>SISTEMA DE NAVEGACIÓN GLOBAL</h2>
            <div style={{ textAlign: 'left', lineHeight: '1.8', fontSize: '18px', marginBottom: '40px' }}>
              <p>📍 En la vista del <b>Globo</b>:</p>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                <li>🚀 Tu <b>nave</b> actúa como el puntero del mouse.</li>
                <li>⚡ Se utiliza como <b>&quot;Velocidad Espacial&quot;</b>.</li>
                <li>🖱️ Usa la <b>rueda del mouse</b> para controlar el Zoom.</li>
                <li>🔘 Haz <b>Click</b> para entrar a los diferentes mundos(permitidos).</li>
              </ul>
            </div>
            <button
              onClick={() => router.push('/game')}
              style={{
                width: '100%',
                padding: '20px',
                fontSize: '20px',
                background: '#4a9eff',
                color: '#ffffff',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 'bold',
                letterSpacing: '2px'
              }}
            >
              ENTRAR
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
