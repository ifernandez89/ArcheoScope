import { useState, useEffect } from 'react'
import * as THREE from 'three'

interface InfoPanelProps {
  title: string
  content: React.ReactNode
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
  visible?: boolean
  onClose?: () => void
}

/**
 * Panel de información 2D overlay
 */
export function InfoPanel({
  title,
  content,
  position = 'top-right',
  visible = true,
  onClose
}: InfoPanelProps) {
  if (!visible) return null
  
  const positionStyles = {
    'top-left': { top: 20, left: 20 },
    'top-right': { top: 20, right: 20 },
    'bottom-left': { bottom: 20, left: 20 },
    'bottom-right': { bottom: 20, right: 20 }
  }
  
  return (
    <div style={{
      position: 'absolute',
      ...positionStyles[position],
      background: 'rgba(0, 0, 0, 0.9)',
      padding: '20px',
      borderRadius: '12px',
      border: '1px solid rgba(255, 255, 255, 0.2)',
      color: 'white',
      fontFamily: 'system-ui',
      maxWidth: '400px',
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)',
      zIndex: 1000
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '15px'
      }}>
        <h3 style={{ margin: 0, fontSize: '18px', fontWeight: 'bold' }}>
          {title}
        </h3>
        {onClose && (
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'white',
              fontSize: '20px',
              cursor: 'pointer',
              padding: '0 5px'
            }}
          >
            ×
          </button>
        )}
      </div>
      <div style={{ fontSize: '14px', lineHeight: '1.6' }}>
        {content}
      </div>
    </div>
  )
}

interface SiteInfoPanelProps {
  site: {
    name: string
    culture: string
    period: string
    description: string
    lat: number
    lon: number
    elevation?: number
    discovered?: string
    significance?: string
  }
  onClose?: () => void
  onNavigate?: () => void
  onLearnMore?: () => void
}

/**
 * Panel específico para sitios arqueológicos
 */
export function SiteInfoPanel({ site, onClose, onNavigate, onLearnMore }: SiteInfoPanelProps) {
  return (
    <InfoPanel
      title={site.name}
      position="top-right"
      visible={true}
      onClose={onClose}
      content={
        <div>
          <div style={{ marginBottom: '12px' }}>
            <div style={{ color: '#ffaa00', fontSize: '12px', marginBottom: '4px' }}>
              {site.culture} • {site.period}
            </div>
            <div style={{ color: '#ccc' }}>
              {site.description}
            </div>
          </div>
          
          <div style={{ 
            background: 'rgba(255, 255, 255, 0.05)',
            padding: '10px',
            borderRadius: '6px',
            marginBottom: '12px',
            fontSize: '12px'
          }}>
            <div style={{ marginBottom: '4px' }}>
              📍 Coordenadas: {site.lat.toFixed(4)}°, {site.lon.toFixed(4)}°
            </div>
            {site.elevation && (
              <div style={{ marginBottom: '4px' }}>
                ⛰️ Elevación: {site.elevation}m
              </div>
            )}
            {site.discovered && (
              <div>
                🔍 Descubierto: {site.discovered}
              </div>
            )}
          </div>
          
          {site.significance && (
            <div style={{ 
              marginBottom: '12px',
              padding: '10px',
              background: 'rgba(255, 170, 0, 0.1)',
              borderLeft: '3px solid #ffaa00',
              borderRadius: '4px',
              fontSize: '12px'
            }}>
              <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                Importancia:
              </div>
              {site.significance}
            </div>
          )}
          
          <div style={{ display: 'flex', gap: '8px' }}>
            {onNavigate && (
              <button
                onClick={onNavigate}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  background: '#ffaa00',
                  border: 'none',
                  borderRadius: '6px',
                  color: 'black',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  fontSize: '12px'
                }}
              >
                🧭 Navegar
              </button>
            )}
            {onLearnMore && (
              <button
                onClick={onLearnMore}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  borderRadius: '6px',
                  color: 'white',
                  cursor: 'pointer',
                  fontSize: '12px'
                }}
              >
                📚 Más info
              </button>
            )}
          </div>
        </div>
      }
    />
  )
}

interface MeasurementPanelProps {
  distance: number
  points: number
  area?: number
  onClear?: () => void
  onExport?: () => void
}

/**
 * Panel para herramientas de medición
 */
export function MeasurementPanel({
  distance,
  points,
  area,
  onClear,
  onExport
}: MeasurementPanelProps) {
  return (
    <InfoPanel
      title="📏 Mediciones"
      position="top-left"
      visible={true}
      content={
        <div>
          <div style={{ 
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '10px',
            marginBottom: '15px'
          }}>
            <div style={{
              background: 'rgba(255, 255, 255, 0.05)',
              padding: '10px',
              borderRadius: '6px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ffaa00' }}>
                {distance.toFixed(2)}
              </div>
              <div style={{ fontSize: '10px', color: '#888' }}>
                metros
              </div>
            </div>
            
            <div style={{
              background: 'rgba(255, 255, 255, 0.05)',
              padding: '10px',
              borderRadius: '6px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#4a9eff' }}>
                {points}
              </div>
              <div style={{ fontSize: '10px', color: '#888' }}>
                puntos
              </div>
            </div>
          </div>
          
          {area !== undefined && (
            <div style={{
              background: 'rgba(255, 255, 255, 0.05)',
              padding: '10px',
              borderRadius: '6px',
              marginBottom: '15px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#7cb342' }}>
                {area.toFixed(2)} m²
              </div>
              <div style={{ fontSize: '10px', color: '#888' }}>
                área
              </div>
            </div>
          )}
          
          <div style={{ display: 'flex', gap: '8px' }}>
            {onClear && (
              <button
                onClick={onClear}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  background: 'rgba(255, 0, 0, 0.2)',
                  border: '1px solid rgba(255, 0, 0, 0.5)',
                  borderRadius: '6px',
                  color: 'white',
                  cursor: 'pointer',
                  fontSize: '12px'
                }}
              >
                🗑️ Limpiar
              </button>
            )}
            {onExport && (
              <button
                onClick={onExport}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  borderRadius: '6px',
                  color: 'white',
                  cursor: 'pointer',
                  fontSize: '12px'
                }}
              >
                💾 Exportar
              </button>
            )}
          </div>
        </div>
      }
    />
  )
}

interface TourPanelProps {
  currentStop: number
  totalStops: number
  stopInfo: {
    title: string
    description: string
    image?: string
  }
  onNext?: () => void
  onPrevious?: () => void
  onExit?: () => void
}

/**
 * Panel para tour guiado
 */
export function TourPanel({
  currentStop,
  totalStops,
  stopInfo,
  onNext,
  onPrevious,
  onExit
}: TourPanelProps) {
  return (
    <InfoPanel
      title={`🎯 Tour: Parada ${currentStop}/${totalStops}`}
      position="bottom-right"
      visible={true}
      onClose={onExit}
      content={
        <div>
          {stopInfo.image && (
            <img 
              src={stopInfo.image}
              alt={stopInfo.title}
              style={{
                width: '100%',
                borderRadius: '8px',
                marginBottom: '12px'
              }}
            />
          )}
          
          <h4 style={{ margin: '0 0 8px 0', color: '#ffaa00' }}>
            {stopInfo.title}
          </h4>
          
          <p style={{ margin: '0 0 15px 0', fontSize: '13px', color: '#ccc' }}>
            {stopInfo.description}
          </p>
          
          <div style={{ display: 'flex', gap: '8px' }}>
            {onPrevious && currentStop > 1 && (
              <button
                onClick={onPrevious}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  borderRadius: '6px',
                  color: 'white',
                  cursor: 'pointer',
                  fontSize: '12px'
                }}
              >
                ← Anterior
              </button>
            )}
            {onNext && currentStop < totalStops && (
              <button
                onClick={onNext}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  background: '#ffaa00',
                  border: 'none',
                  borderRadius: '6px',
                  color: 'black',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  fontSize: '12px'
                }}
              >
                Siguiente →
              </button>
            )}
          </div>
        </div>
      }
    />
  )
}

/**
 * Mini-mapa 2D
 */
export function MiniMap({
  playerPosition,
  waypoints,
  size = 150
}: {
  playerPosition: THREE.Vector3
  waypoints: Array<{ position: THREE.Vector3; label: string }>
  size?: number
}) {
  return (
    <div style={{
      position: 'absolute',
      bottom: 20,
      left: 20,
      width: size,
      height: size,
      background: 'rgba(0, 0, 0, 0.8)',
      border: '2px solid rgba(255, 255, 255, 0.3)',
      borderRadius: '8px',
      overflow: 'hidden'
    }}>
      <svg width={size} height={size}>
        {/* Grid */}
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="0.5"/>
          </pattern>
        </defs>
        <rect width={size} height={size} fill="url(#grid)" />
        
        {/* Waypoints */}
        {waypoints.map((waypoint, index) => {
          const x = (waypoint.position.x / 100) * size / 2 + size / 2
          const y = (waypoint.position.z / 100) * size / 2 + size / 2
          
          return (
            <circle
              key={index}
              cx={x}
              cy={y}
              r={3}
              fill="#ffaa00"
              stroke="#fff"
              strokeWidth={1}
            />
          )
        })}
        
        {/* Player */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={5}
          fill="#4a9eff"
          stroke="#fff"
          strokeWidth={2}
        />
      </svg>
    </div>
  )
}
