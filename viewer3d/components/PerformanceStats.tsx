/**
 * Componente de Stats.js para monitoreo visual de FPS
 * Solo se muestra en desarrollo o cuando se activa manualmente
 */

'use client'

import { useEffect, useRef } from 'react'
import Stats from 'stats.js'

interface PerformanceStatsProps {
  enabled?: boolean
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
}

export default function PerformanceStats({ 
  enabled = process.env.NODE_ENV === 'development',
  position = 'top-left'
}: PerformanceStatsProps) {
  const statsRef = useRef<Stats | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (!enabled || typeof window === 'undefined') return
    
    // Crear instancia de Stats
    const stats = new Stats()
    statsRef.current = stats
    
    // Configurar panel (0: FPS, 1: MS, 2: MB)
    stats.showPanel(0) // FPS por defecto
    
    // Estilos del contenedor
    stats.dom.style.position = 'fixed'
    stats.dom.style.zIndex = '9999'
    
    // Posicionar según prop
    switch (position) {
      case 'top-left':
        stats.dom.style.left = '0'
        stats.dom.style.top = '0'
        break
      case 'top-right':
        stats.dom.style.right = '0'
        stats.dom.style.top = '0'
        stats.dom.style.left = 'auto'
        break
      case 'bottom-left':
        stats.dom.style.left = '0'
        stats.dom.style.bottom = '0'
        stats.dom.style.top = 'auto'
        break
      case 'bottom-right':
        stats.dom.style.right = '0'
        stats.dom.style.bottom = '0'
        stats.dom.style.top = 'auto'
        stats.dom.style.left = 'auto'
        break
    }
    
    // Agregar al DOM
    if (containerRef.current) {
      containerRef.current.appendChild(stats.dom)
    } else {
      document.body.appendChild(stats.dom)
    }
    
    // Loop de actualización
    let animationId: number
    
    function animate() {
      stats.begin()
      // El render real lo hace Three.js, aquí solo medimos
      stats.end()
      animationId = requestAnimationFrame(animate)
    }
    
    animate()
    
    // Cleanup
    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId)
      }
      if (stats.dom.parentElement) {
        stats.dom.parentElement.removeChild(stats.dom)
      }
    }
  }, [enabled, position])
  
  // Cambiar panel con click
  useEffect(() => {
    if (!statsRef.current) return
    
    const handleClick = () => {
      if (statsRef.current) {
        const currentPanel = statsRef.current.dom.children[0] as any
        const nextPanel = (parseInt(currentPanel.style.display === 'block' ? '0' : '1') + 1) % 3
        statsRef.current.showPanel(nextPanel)
      }
    }
    
    statsRef.current.dom.addEventListener('click', handleClick)
    
    return () => {
      if (statsRef.current) {
        statsRef.current.dom.removeEventListener('click', handleClick)
      }
    }
  }, [])
  
  if (!enabled) return null
  
  return <div ref={containerRef} />
}

// Hook para usar Stats en componentes Three.js
export function useStats() {
  const statsRef = useRef<Stats | null>(null)
  
  useEffect(() => {
    if (typeof window === 'undefined') return
    
    const stats = new Stats()
    statsRef.current = stats
    
    return () => {
      statsRef.current = null
    }
  }, [])
  
  const begin = () => statsRef.current?.begin()
  const end = () => statsRef.current?.end()
  
  return { begin, end, stats: statsRef.current }
}
