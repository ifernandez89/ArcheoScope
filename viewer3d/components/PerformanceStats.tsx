'use client'

import { useState, useEffect, useRef } from 'react'

export default function PerformanceStats() {
  const [fps, setFps] = useState(60)
  const [frameTime, setFrameTime] = useState(0)
  const frameCount = useRef(0)
  const lastTime = useRef(performance.now())

  useEffect(() => {
    let animationId: number

    const updateStats = () => {
      frameCount.current++
      const currentTime = performance.now()
      const delta = currentTime - lastTime.current

      if (delta >= 1000) {
        const currentFps = Math.round((frameCount.current * 1000) / delta)
        const avgFrameTime = delta / frameCount.current
        
        setFps(currentFps)
        setFrameTime(Math.round(avgFrameTime * 100) / 100)
        
        frameCount.current = 0
        lastTime.current = currentTime
      }

      animationId = requestAnimationFrame(updateStats)
    }

    animationId = requestAnimationFrame(updateStats)

    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId)
      }
    }
  }, [])

  return (
    <div style={{
      position: 'fixed',
      top: '100px',
      left: '20px',
      padding: '12px 16px',
      background: 'rgba(0, 0, 0, 0.85)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      zIndex: 1000,
      minWidth: '120px'
    }}>
      <div style={{ 
        marginBottom: '8px',
        fontSize: '11px',
        color: '#888',
        textTransform: 'uppercase',
        letterSpacing: '1px'
      }}>
        Performance
      </div>
      
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between',
        marginBottom: '4px'
      }}>
        <span style={{ color: '#888' }}>FPS:</span>
        <span style={{ 
          color: fps >= 55 ? '#4ade80' : fps >= 30 ? '#fbbf24' : '#ef4444',
          fontWeight: 'bold'
        }}>
          {fps}
        </span>
      </div>
      
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between'
      }}>
        <span style={{ color: '#888' }}>Frame:</span>
        <span style={{ color: '#60a5fa' }}>
          {frameTime}ms
        </span>
      </div>

      <div style={{
        marginTop: '8px',
        paddingTop: '8px',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        fontSize: '10px',
        color: '#666'
      }}>
        {fps >= 55 ? '✓ Optimal' : fps >= 30 ? '⚠ Moderate' : '✗ Low'}
      </div>
    </div>
  )
}
