'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import InventoryItem from './InventoryItem'
import { subscribeInventory, requestDrop, subscribeScan, type InventoryEntry } from './TrainingRoom'

function isMobile() {
  if (typeof window === 'undefined') return false
  return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
}

// ─── Joystick virtual ────────────────────────────────────────────────────────
function TouchJoystick({ onMove }: { onMove: (dx: number, dy: number) => void }) {
  const baseRef = useRef<HTMLDivElement>(null)
  const stickRef = useRef<HTMLDivElement>(null)
  const activeTouch = useRef<number | null>(null)
  const basePos = useRef({ x: 0, y: 0 })
  const SIZE = 110, STICK = 44, MAX = 38

  const handleStart = (e: React.TouchEvent) => {
    const t = e.changedTouches[0]
    activeTouch.current = t.identifier
    const rect = baseRef.current!.getBoundingClientRect()
    basePos.current = { x: rect.left + SIZE / 2, y: rect.top + SIZE / 2 }
  }

  const handleMove = (e: React.TouchEvent) => {
    const t = Array.from(e.changedTouches).find(t => t.identifier === activeTouch.current)
    if (!t || !stickRef.current) return
    let dx = t.clientX - basePos.current.x
    let dy = t.clientY - basePos.current.y
    const dist = Math.sqrt(dx * dx + dy * dy)
    if (dist > MAX) { dx = dx / dist * MAX; dy = dy / dist * MAX }
    stickRef.current.style.transform = `translate(${dx}px, ${dy}px)`
    onMove(dx / MAX, dy / MAX)
  }

  const handleEnd = (e: React.TouchEvent) => {
    const t = Array.from(e.changedTouches).find(t => t.identifier === activeTouch.current)
    if (!t) return
    activeTouch.current = null
    if (stickRef.current) stickRef.current.style.transform = 'translate(0,0)'
    onMove(0, 0)
  }

  return (
    <div ref={baseRef} onTouchStart={handleStart} onTouchMove={handleMove} onTouchEnd={handleEnd}
      style={{
        width: SIZE, height: SIZE, borderRadius: '50%',
        background: 'rgba(255,255,255,0.08)', border: '2px solid rgba(255,255,255,0.25)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', touchAction: 'none',
      }}>
      <div ref={stickRef} style={{
        width: STICK, height: STICK, borderRadius: '50%',
        background: 'rgba(74,158,255,0.7)', border: '2px solid #4a9eff',
        transition: 'transform 0.05s', pointerEvents: 'none',
      }} />
    </div>
  )
}

// ─── Botón touch ─────────────────────────────────────────────────────────────
function TouchBtn({ label, onPress, onRelease, color = '#4a9eff', size = 64 }:
  { label: string, onPress: () => void, onRelease?: () => void, color?: string, size?: number }) {
  return (
    <div
      onTouchStart={(e) => { e.preventDefault(); onPress() }}
      onTouchEnd={(e) => { e.preventDefault(); onRelease?.() }}
      style={{
        width: size, height: size, borderRadius: '50%',
        background: `${color}22`, border: `2px solid ${color}`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        color, fontSize: size * 0.28, fontWeight: 'bold', userSelect: 'none',
        touchAction: 'none', textAlign: 'center', lineHeight: 1.1,
      }}
    >{label}</div>
  )
}

export default function TrainingUI() {
  const router = useRouter()
  const [keys, setKeys] = useState<Record<string, boolean>>({})
  const [inventory, setInventory] = useState<InventoryEntry[]>([])
  const [scanData, setScanData] = useState<{ name: string, desc: string } | null>(null)
  const [mobile, setMobile] = useState(false)
  const [showGlobeInfo, setShowGlobeInfo] = useState(false)

  useEffect(() => { setMobile(isMobile()) }, [])
  useEffect(() => { const u = subscribeScan(setScanData); return u }, [])
  useEffect(() => { const u = subscribeInventory(items => setInventory([...items])); return u }, [])

  // Teclado físico
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      setKeys(p => ({ ...p, [e.key.toLowerCase()]: true }))
      if (e.code === 'Space') setKeys(p => ({ ...p, space: true }))
    }
    const up = (e: KeyboardEvent) => {
      setKeys(p => ({ ...p, [e.key.toLowerCase()]: false }))
      if (e.code === 'Space') setKeys(p => ({ ...p, space: false }))
    }
    window.addEventListener('keydown', down)
    window.addEventListener('keyup', up)
    return () => { window.removeEventListener('keydown', down); window.removeEventListener('keyup', up) }
  }, [])

  // Simular teclas desde controles touch
  const fireKey = (key: string, down: boolean) => {
    const ev = new KeyboardEvent(down ? 'keydown' : 'keyup', { key, code: key === ' ' ? 'Space' : `Key${key.toUpperCase()}`, bubbles: true })
    window.dispatchEvent(ev)
  }

  const handleJoystick = (dx: number, dy: number) => {
    const threshold = 0.3
    fireKey('w', dy < -threshold); fireKey('s', dy > threshold)
    fireKey('a', dx < -threshold); fireKey('d', dx > threshold)
  }

  const Key = ({ label, active, size = 56, width }: { label: string, active: boolean, size?: number, width?: number }) => (
    <div style={{
      width: width || size, height: size,
      background: active ? '#4a9eff' : 'rgba(100,100,100,0.3)',
      border: `2px solid ${active ? '#4a9eff' : 'rgba(255,255,255,0.4)'}`,
      borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center',
      color: active ? '#000' : '#fff', fontSize: size * 0.38, fontWeight: 'bold',
      transition: 'all 0.1s', boxShadow: active ? '0 0 15px #4a9eff' : 'none',
      fontFamily: 'monospace', backdropFilter: 'blur(4px)',
    }}>{label}</div>
  )

  return (
    <div style={{
      position: 'fixed', inset: 0, pointerEvents: 'none',
      padding: mobile ? '16px' : '40px',
      display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
      color: '#fff', fontFamily: 'Archeoscope, serif', zIndex: 100,
    }}>

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: mobile ? '20px' : '28px', letterSpacing: '3px' }}>TRAINING ROOM</h1>
          <p style={{ margin: '4px 0 0', opacity: 0.5, fontSize: mobile ? '11px' : '13px' }}>MANUAL DE VUELO Y ACCIONES</p>
        </div>

        {/* Inventario */}
        {inventory.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', pointerEvents: 'auto', alignItems: 'flex-end' }}>
            <div style={{ fontSize: '11px', letterSpacing: '2px', color: '#ffd700', fontWeight: 'bold' }}>🎒 Inventario</div>
            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', justifyContent: 'flex-end', maxWidth: '260px' }}>
              {inventory.map(item => (
                <InventoryItem key={item.id} modelPath={item.modelPath} itemName={item.itemName} show onDrop={() => requestDrop(item.id)} />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* ── CONTROLES PC (teclado) ── */}
      {!mobile && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'flex', gap: '8px', marginLeft: '64px' }}><Key label="W" active={!!keys['w']} /></div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <Key label="A" active={!!keys['a']} /><Key label="S" active={!!keys['s']} /><Key label="D" active={!!keys['d']} />
            </div>
            <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.8 }}>NAVEGACIÓN BÁSICA</p>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <Key label="SHIFT" active={!!keys['shift']} size={56} width={90} />
              <span style={{ fontSize: '18px' }}>+</span>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div style={{ padding: '4px 8px', background: 'rgba(100,100,100,0.3)', border: '1px solid rgba(255,255,255,0.4)', borderRadius: '4px', fontSize: '10px' }}>MOUSE UP</div>
                <div style={{ padding: '4px 8px', background: 'rgba(100,100,100,0.3)', border: '1px solid rgba(255,255,255,0.4)', borderRadius: '4px', fontSize: '10px' }}>MOUSE DOWN</div>
              </div>
            </div>
            <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.8 }}>ALTITUD Y VELOCIDAD</p>
          </div>
          <div style={{ display: 'flex', gap: '32px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <div style={{ display: 'flex', gap: '8px' }}>
                <Key label="Q" active={!!keys['q']} /><Key label="E" active={!!keys['e']} />
              </div>
              <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.8 }}>ROTACIÓN</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <Key label="SPACE" active={!!keys['space']} size={56} width={140} />
              <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.8 }}>HABILIDAD ESPECIAL</p>
            </div>
          </div>
        </div>
      )}

      {/* ── CONTROLES TOUCH (mobile) ── */}
      {mobile && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', pointerEvents: 'auto', padding: '0 8px 16px' }}>
          {/* Joystick izquierdo */}
          <TouchJoystick onMove={handleJoystick} />

          {/* Botones derecha */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'center' }}>
            <TouchBtn label="▲" size={56} color="#4a9eff"
              onPress={() => fireKey('ArrowUp', true)} onRelease={() => fireKey('ArrowUp', false)} />
            <div style={{ display: 'flex', gap: '10px' }}>
              <TouchBtn label="⚡" size={64} color="#fbbf24"
                onPress={() => fireKey(' ', true)} onRelease={() => fireKey(' ', false)} />
              <TouchBtn label="▼" size={56} color="#4a9eff"
                onPress={() => fireKey('ArrowDown', true)} onRelease={() => fireKey('ArrowDown', false)} />
            </div>
            <p style={{ margin: 0, fontSize: '10px', opacity: 0.6, textAlign: 'center' }}>SUBIR · HABILIDAD · BAJAR</p>
          </div>
        </div>
      )}

      {/* Bottom: Interacciones + Salir */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', pointerEvents: 'auto' }}>
        <div style={{
          background: 'rgba(0,0,0,0.7)', padding: mobile ? '12px' : '18px',
          borderRadius: '10px', border: '1px solid rgba(255,255,255,0.2)', backdropFilter: 'blur(10px)',
          maxWidth: mobile ? '200px' : '340px',
        }}>
          <h3 style={{ margin: '0 0 10px', color: '#4a9eff', fontSize: mobile ? '13px' : '16px' }}>INTERACCIONES</h3>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <li style={{ fontSize: mobile ? '12px' : '15px' }}>
              {mobile ? '👆' : '🖱️'} Roca → <span style={{ color: '#ffd700', fontWeight: 'bold' }}>JUNTAR</span>
            </li>
            <li style={{ fontSize: mobile ? '12px' : '15px' }}>
              🎒 Inventario → <span style={{ color: '#ffd700', fontWeight: 'bold' }}>SOLTAR</span>
            </li>
            <li style={{ fontSize: mobile ? '12px' : '15px' }}>
              ♻️ Repetir <span style={{ color: '#4a9eff', fontWeight: 'bold' }}>infinitamente</span>
            </li>
          </ul>
        </div>

        {/* Botón: PC = FINALIZAR TUTORIAL (con modal del globo), Mobile = SALIR (vuelve al menú) */}
        {mobile ? (
          <button
            onClick={() => router.push('/menu')}
            style={{
              padding: '12px 24px', fontSize: '14px',
              background: 'rgba(0,0,0,0.8)', color: '#fff',
              border: '2px solid rgba(255,255,255,0.5)', borderRadius: '8px',
              cursor: 'pointer', fontWeight: 'bold', letterSpacing: '2px', transition: 'all 0.3s',
            }}
          >
            ← SALIR
          </button>
        ) : (
          <button
            onClick={() => setShowGlobeInfo(true)}
            style={{
              padding: '16px 36px', fontSize: '18px',
              background: '#ffffff', color: '#000000',
              border: 'none', borderRadius: '8px',
              cursor: 'pointer', fontWeight: 'normal', letterSpacing: '3px', transition: 'all 0.3s',
              fontFamily: 'Archeoscope, serif',
            }}
            onMouseEnter={e => { e.currentTarget.style.background = '#4a9eff'; e.currentTarget.style.color = '#fff' }}
            onMouseLeave={e => { e.currentTarget.style.background = '#ffffff'; e.currentTarget.style.color = '#000' }}
          >
            FINALIZAR TUTORIAL
          </button>
        )}
      </div>

      {/* Modal del Globo — solo PC */}
      {showGlobeInfo && !mobile && (
        <div style={{
          position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.9)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 1000, pointerEvents: 'auto',
        }}>
          <div style={{
            maxWidth: '600px', background: '#111', padding: '40px',
            borderRadius: '16px', border: '2px solid #4a9eff', textAlign: 'center',
            boxShadow: '0 0 50px rgba(74,158,255,0.3)',
          }}>
            <h2 style={{ color: '#4a9eff', marginBottom: '30px', fontSize: '28px' }}>SISTEMA DE NAVEGACIÓN GLOBAL</h2>
            <div style={{ textAlign: 'left', lineHeight: '1.8', fontSize: '18px', marginBottom: '40px' }}>
              <p>📍 En la vista del <b>Globo</b>:</p>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                <li>🚀 Tu <b>nave</b> actúa como el puntero del mouse.</li>
                <li>⚡ Se utiliza como <b>&quot;Velocidad Espacial&quot;</b>.</li>
                <li>🖱️ Usa la <b>rueda del mouse</b> para controlar el Zoom.</li>
                <li>🔘 Haz <b>Click</b> para entrar a los diferentes mundos.</li>
              </ul>
            </div>
            <button
              onClick={() => router.push('/game')}
              style={{
                width: '100%', padding: '20px', fontSize: '20px',
                background: '#4a9eff', color: '#fff', border: 'none',
                borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold', letterSpacing: '2px',
              }}
            >
              ENTRAR AL MUNDO
            </button>
          </div>
        </div>
      )}

      {/* Oracle Scan HUD */}
      {scanData && (
        <div style={{
          position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%,-50%)',
          background: 'rgba(0,20,30,0.92)', border: '2px solid #00ffff',
          borderRadius: '12px', padding: '28px 36px', maxWidth: '480px', width: '90%',
          textAlign: 'center', zIndex: 200, pointerEvents: 'none',
          boxShadow: '0 0 40px rgba(0,255,255,0.3)',
        }}>
          <div style={{ fontSize: '10px', marginBottom: '8px', opacity: 0.8, letterSpacing: '2px', color: '#00ffff' }}>
            📡 ORACLE_SCAN // SIGNATURE_IDENTIFIED
          </div>
          <div style={{ fontSize: '26px', fontWeight: '900', marginBottom: '10px', letterSpacing: '4px', textShadow: '0 0 10px #00ffff', color: '#fff' }}>
            {scanData.name}
          </div>
          <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.8)', lineHeight: '1.7', fontStyle: 'italic' }}>
            {scanData.desc}
          </div>
          <div style={{ marginTop: '14px', height: '3px', background: 'rgba(0,255,255,0.2)', borderRadius: '2px', overflow: 'hidden' }}>
            <div style={{ height: '100%', background: '#00ffff', animation: 'scanBar 2s linear' }} />
          </div>
          <style>{`
            @keyframes scanBar { from { width: 0% } to { width: 100% } }
          `}</style>
        </div>
      )}
    </div>
  )
}
