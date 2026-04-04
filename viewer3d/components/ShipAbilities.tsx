'use client'

import React, { useEffect, useRef, useState } from 'react'
import { getAssetPath } from '@/lib/paths'

interface ShipAbilitiesProps {
  ufoNumber: number
  active: boolean
  onActionComplete?: () => void
}

export default function ShipAbilities({ ufoNumber, active, onActionComplete }: ShipAbilitiesProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [waves, setWaves] = useState<{ id: number, x: number, y: number }[]>([])
  const [shocks, setShocks] = useState<{ id: number, x: number, y: number }[]>([])


  // 📡 Scan Waves (UFO 4)
  useEffect(() => {
    if (ufoNumber === 4 && active) {
      const id = Date.now()
      setWaves(prev => [...prev, { id, x: 50, y: 50 }]) // Center relative
      const timer = setTimeout(() => {
        setWaves(prev => prev.filter(w => w.id !== id))
        if(onActionComplete) onActionComplete()
      }, 2000)
      return () => clearTimeout(timer)
    }
  }, [ufoNumber, active])

  // 💥 Shockwaves (UFO 5)
  useEffect(() => {
    if (ufoNumber === 5 && active) {
      const id = Date.now()
      setShocks(prev => [...prev, { id, x: 50, y: 50 }])
      const timer = setTimeout(() => {
        setShocks(prev => prev.filter(s => s.id !== id))
        if(onActionComplete) onActionComplete()
      }, 600)
      return () => clearTimeout(timer)
    }
  }, [ufoNumber, active])

  return (
    <div className={`ship-abilities-container ${active ? 'active' : ''}`} style={{
      position: 'fixed',
      inset: 0,
      pointerEvents: 'none',
      zIndex: 999,
      overflow: 'hidden'
    }}>
      {/* 🌫️ Phantom: Cloaking (UFO 1) */}
      {ufoNumber === 1 && (
        <div className={`cloak-effect ${active ? 'cloak-active' : ''}`} />
      )}



      {/* 🔬 Oracle: Scan Waves (UFO 4) */}
      {waves.map(w => (
        <div key={w.id} className="scan-wave" style={{
          left: `${w.x}%`,
          top: `${w.y}%`,
          position: 'absolute'
        }} />
      ))}

      {/* 💣 Titan: Shockwave (UFO 5) */}
      {shocks.map(s => (
        <div key={s.id} className="shockwave" style={{
          left: `${s.x}%`,
          top: `${s.y}%`,
          position: 'absolute',
          transform: 'translate(-50%, -50%)'
        }} />
      ))}

      <style jsx>{`
        .cloak-effect {
          position: absolute;
          inset: 0;
          backdrop-filter: blur(8px) brightness(1.1);
          opacity: 0;
          transition: opacity 0.4s ease;
          background: rgba(100, 150, 255, 0.05);
        }
        .cloak-active {
          opacity: 1;
        }


        .scan-wave {
          width: 200px;
          height: 200px;
          border: 4px solid cyan;
          border-radius: 50%;
          transform: translate(-50%, -50%) scale(0.2);
          animation: scan 2s ease-out forwards;
          box-shadow: 0 0 20px cyan;
        }

        @keyframes scan {
          from { transform: translate(-50%, -50%) scale(0.2); opacity: 1; }
          to { transform: translate(-50%, -50%) scale(5); opacity: 0; }
        }

        .shockwave {
          width: 300px;
          height: 300px;
          border-radius: 50%;
          background: radial-gradient(circle, rgba(255, 200, 0, 0.8), rgba(255, 100, 0, 0.3), transparent);
          animation: boom 0.6s ease-out forwards;
          filter: blur(4px);
        }

        @keyframes boom {
          from { transform: translate(-50%, -50%) scale(0.2); opacity: 1; }
          to { transform: translate(-50%, -50%) scale(3); opacity: 0; }
        }

        @keyframes screenShake {
          0% { transform: translate(0,0); }
          25% { transform: translate(4px, 2px); }
          50% { transform: translate(-3px, -2px); }
          75% { transform: translate(2px, -3px); }
          100% { transform: translate(0,0); }
        }
      `}</style>
    </div>
  )
}
