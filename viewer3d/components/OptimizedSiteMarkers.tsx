'use client'

import { useRef, useState, useMemo, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Html } from '@react-three/drei'
import * as THREE from 'three'
import sitesData from '../data/archaeological-sites.json'

interface OptimizedSiteMarkersProps {
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

/**
 * Marcadores de sitios arqueológicos optimizados con InstancedMesh
 * Renderiza cientos de marcadores con un solo draw call
 */
export default function OptimizedSiteMarkers({ 
  onSiteClick, 
  radius = 5.3 
}: OptimizedSiteMarkersProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null)
  const [clickedSite, setClickedSite] = useState<ArchaeologicalSite | null>(null)
  const { camera, raycaster, pointer } = useThree()
  
  const sites = sitesData.sites as ArchaeologicalSite[]
  const count = sites.length

  // Geometría y material compartidos
  const geometry = useMemo(() => new THREE.SphereGeometry(0.02, 12, 12), [])
  const material = useMemo(() => 
    new THREE.MeshStandardMaterial({
      color: '#ef4444',
      emissive: '#ef4444',
      emissiveIntensity: 0.3,
      metalness: 0,
      roughness: 0.5,
      transparent: true,
      opacity: 0.6
    }),
    []
  )

  // Calcular posiciones de todos los sitios
  const sitePositions = useMemo(() => 
    sites.map(site => latLonToVector3(site.lat, site.lon, radius)),
    [sites, radius]
  )

  // Configurar matrices de instancias
  useEffect(() => {
    if (!meshRef.current) return

    const tempObject = new THREE.Object3D()
    const tempColor = new THREE.Color()
    
    sitePositions.forEach((position, i) => {
      tempObject.position.copy(position)
      tempObject.scale.setScalar(1)
      tempObject.updateMatrix()
      
      meshRef.current!.setMatrixAt(i, tempObject.matrix)
      
      // Color inicial
      tempColor.set('#ef4444')
      meshRef.current!.setColorAt(i, tempColor)
    })
    
    meshRef.current.instanceMatrix.needsUpdate = true
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true
    }
  }, [sitePositions])

  // Objetos reutilizables para useFrame
  const tempObject = useMemo(() => new THREE.Object3D(), [])
  const tempColor = useMemo(() => new THREE.Color(), [])

  // Animación y hover
  useFrame(({ clock, pointer: framePointer }) => {
    if (!meshRef.current) return

    const time = clock.getElapsedTime()

    // Raycasting para detectar hover
    raycaster.setFromCamera(framePointer, camera)
    const intersects = raycaster.intersectObject(meshRef.current)
    
    let newHoveredIndex: number | null = null
    if (intersects.length > 0) {
      newHoveredIndex = intersects[0].instanceId ?? null
    }
    
    if (newHoveredIndex !== hoveredIndex) {
      setHoveredIndex(newHoveredIndex)
      document.body.style.cursor = newHoveredIndex !== null ? 'pointer' : 'default'
    }

    // Actualizar cada instancia
    sitePositions.forEach((position, i) => {
      const isHovered = i === hoveredIndex
      
      // Escala con pulsación
      const pulseScale = 1 + Math.sin(time * 2 + i * 0.5) * 0.05
      const scale = isHovered ? 1.8 * pulseScale : pulseScale
      
      tempObject.position.copy(position)
      tempObject.scale.setScalar(scale)
      tempObject.updateMatrix()
      
      meshRef.current!.setMatrixAt(i, tempObject.matrix)
      
      // Color
      tempColor.set(isHovered ? '#fbbf24' : '#ef4444')
      meshRef.current!.setColorAt(i, tempColor)
    })
    
    meshRef.current.instanceMatrix.needsUpdate = true
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true
    }
  })

  // Manejar clicks
  const handleClick = (event: any) => {
    event.stopPropagation()
    
    if (hoveredIndex !== null && hoveredIndex < sites.length) {
      const site = sites[hoveredIndex]
      setClickedSite(site)
      onSiteClick?.(site)
    }
  }

  return (
    <>
      <instancedMesh
        ref={meshRef}
        args={[geometry, material, count]}
        onClick={handleClick}
        frustumCulled
      />
      
      {/* Tooltip para sitio hover */}
      {hoveredIndex !== null && hoveredIndex < sites.length && (
        <SiteTooltip 
          site={sites[hoveredIndex]} 
          position={sitePositions[hoveredIndex]} 
        />
      )}
    </>
  )
}

interface SiteTooltipProps {
  site: ArchaeologicalSite
  position: THREE.Vector3
}

function SiteTooltip({ site, position }: SiteTooltipProps) {
  return (
    <group position={position}>
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
