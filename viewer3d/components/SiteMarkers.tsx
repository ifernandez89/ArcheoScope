'use client'

import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { Html } from '@react-three/drei'
import * as THREE from 'three'
import sitesData from '../data/archaeological-sites.json'

interface SiteMarkersProps {
  onSiteClick?: (site: ArchaeologicalSite) => void
  radius?: number
}

export interface ArchaeologicalSite {
  id: string
  name: string
  lat: number
  lon: number
  model: string
  description: string
  period: string
  culture: string
}

export default function SiteMarkers({ onSiteClick, radius = 5.3 }: SiteMarkersProps) {
  const [hoveredSite, setHoveredSite] = useState<string | null>(null)
  
  return (
    <group>
      {sitesData.sites.map((site) => (
        <SiteMarker
          key={site.id}
          site={site}
          radius={radius}
          isHovered={hoveredSite === site.id}
          onHover={() => setHoveredSite(site.id)}
          onUnhover={() => setHoveredSite(null)}
          onClick={() => onSiteClick?.(site)}
        />
      ))}
    </group>
  )
}

interface SiteMarkerProps {
  site: ArchaeologicalSite
  radius: number
  isHovered: boolean
  onHover: () => void
  onUnhover: () => void
  onClick: () => void
}

function SiteMarker({ site, radius, isHovered, onHover, onUnhover, onClick }: SiteMarkerProps) {
  const markerRef = useRef<THREE.Mesh>(null)
  const position = latLonToVector3(site.lat, site.lon, radius)
  
  useFrame((state) => {
    if (markerRef.current) {
      const scale = isHovered ? 1.5 : 1
      const pulseScale = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1
      markerRef.current.scale.setScalar(scale * pulseScale)
    }
  })
  
  return (
    <group position={position}>
      <mesh
        ref={markerRef}
        onClick={(e) => {
          e.stopPropagation()
          onClick()
        }}
        onPointerOver={(e) => {
          e.stopPropagation()
          document.body.style.cursor = 'pointer'
          onHover()
        }}
        onPointerOut={(e) => {
          e.stopPropagation()
          document.body.style.cursor = 'default'
          onUnhover()
        }}
      >
        <sphereGeometry args={[0.05, 16, 16]} />
        <meshBasicMaterial
          color={isHovered ? '#fbbf24' : '#ef4444'}
          emissive={isHovered ? '#fbbf24' : '#ef4444'}
          emissiveIntensity={2}
        />
      </mesh>
      
      {isHovered && (
        <Html
          distanceFactor={10}
          style={{
            background: 'rgba(0, 0, 0, 0.9)',
            padding: '12px 16px',
            borderRadius: '8px',
            border: '1px solid rgba(255,255,255,0.3)',
            color: 'white',
            fontSize: '12px',
            fontFamily: 'system-ui',
            pointerEvents: 'none',
            whiteSpace: 'nowrap',
            transform: 'translate(-50%, -120%)',
            minWidth: '200px'
          }}
        >
          <div style={{ fontWeight: 'bold', marginBottom: '4px', color: '#fbbf24' }}>
            {site.name}
          </div>
          <div style={{ fontSize: '10px', color: '#888', marginBottom: '4px' }}>
            {site.culture} • {site.period}
          </div>
          <div style={{ fontSize: '10px', color: '#ccc' }}>
            {site.description}
          </div>
          <div style={{ fontSize: '9px', color: '#666', marginTop: '6px', fontFamily: 'monospace' }}>
            📍 {site.lat.toFixed(4)}°, {site.lon.toFixed(4)}°
          </div>
        </Html>
      )}
    </group>
  )
}

function latLonToVector3(lat: number, lon: number, radius: number): THREE.Vector3 {
  const phi = (90 - lat) * (Math.PI / 180)
  const theta = (lon + 180) * (Math.PI / 180)
  
  const x = -radius * Math.sin(phi) * Math.cos(theta)
  const z = radius * Math.sin(phi) * Math.sin(theta)
  const y = radius * Math.cos(phi)
  
  return new THREE.Vector3(x, y, z)
}
