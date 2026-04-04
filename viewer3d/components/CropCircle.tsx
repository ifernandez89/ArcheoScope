'use client'

import { useRef, useMemo } from 'react'
import * as THREE from 'three'
import { useFrame } from '@react-three/fiber'
import { Html, useTexture } from '@react-three/drei'
import { getAssetPath } from '@/lib/paths'

interface CropCircleProps {
  type: 'julia' | 'galaxy' | 'toroid' | 'flower' | 'metatron'
  position: [number, number, number]
  scale?: number
  visible?: boolean
}

const CROP_CIRCLE_METADATA = {
  julia: {
    name: 'Julia Set Fractal',
    lore: 'Los antiguos descubrieron patrones fractales que replican la estructura del cosmos.',
    mechanic: 'Portal dimensional / Navegación entre niveles',
    texture: '/textures/crop_circles/julia.png',
    color: '#00ffff'
  },
  galaxy: {
    name: 'Milk Hill Galaxy',
    lore: 'Mapa de energía cósmica / expansión de una señal antigua.',
    mechanic: 'Mapa estelar de alta densidad',
    texture: '/textures/crop_circles/galaxy.png',
    color: '#00aaff'
  },
  toroid: {
    name: 'Mandala / Toroide Energético',
    lore: 'Resonador energético toroidal que funciona como generador o escudo.',
    mechanic: 'Generador de energía / Activación de portales',
    texture: '/textures/crop_circles/toroid.png',
    color: '#ffee00'
  },
  flower: {
    name: 'Flower of Life',
    lore: 'Geometría fundamental de la realidad, usada para activar artefactos estelares.',
    mechanic: 'Resonancia energética / Desbloqueo tecnológico',
    texture: '/textures/crop_circles/flower.png',
    color: '#ff00ff'
  },
  metatron: {
    name: 'Cubo de Metatrón',
    lore: 'Codificación de la estructura de la materia y la red energética planetaria.',
    mechanic: 'Escáner científico / Análisis alienígena',
    texture: '/textures/crop_circles/metatron.png',
    color: '#ffffff'
  }
}

export default function CropCircle({ type, position, scale = 15, visible = true }: CropCircleProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  // Usar metadata para cargar textura y configuración
  const meta = CROP_CIRCLE_METADATA[type]
  
  // Cargar textura (drei useTexture maneja el cache y suspense)
  const texture = useTexture(getAssetPath(meta.texture))

  useFrame((state) => {
    if (meshRef.current) {
      // Sutil animación de levitación y rotación lenta
      const t = state.clock.getElapsedTime()
      // Levitación sobre el suelo
      meshRef.current.position.y = position[1] + Math.sin(t * 0.5) * 0.05 + 0.1
      // Rotación muy sutil
      meshRef.current.rotation.z = t * 0.02
    }
  })

  if (!visible) return null

  return (
    <group position={position}>
      {/* Sombra proyectada plana en el suelo (opcional) */}
      
      {/* El Círculo de Cosecha Holográfico */}
      <mesh ref={meshRef} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[scale, scale]} />
        <meshStandardMaterial
          map={texture}
          transparent
          opacity={0.8}
          emissive={meta.color}
          emissiveIntensity={3}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.DoubleSide}
        />
      </mesh>
      
      {/* Reflejo/Aura en el suelo */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}>
        <circleGeometry args={[scale * 0.55, 32]} />
        <meshBasicMaterial
          color={meta.color}
          transparent
          opacity={0.12}
          blending={THREE.AdditiveBlending}
        />
      </mesh>

      {/* Etiqueta de información holográfica que mira a la cámara */}
      <Html position={[0, 3, 0]} center distanceFactor={20}>
        <div style={{
          background: 'rgba(0, 15, 30, 0.9)',
          border: `2px solid ${meta.color}`,
          boxShadow: `0 0 25px ${meta.color}66, inset 0 0 10px ${meta.color}33`,
          color: 'white',
          padding: '15px 20px',
          borderRadius: '4px',
          width: '280px',
          fontFamily: '"Orbitron", "Inter", sans-serif',
          backdropFilter: 'blur(12px)',
          pointerEvents: 'none',
          textAlign: 'left',
          animation: 'hologramPulse 4s infinite ease-in-out'
        }}>
          <style dangerouslySetInnerHTML={{ __html: `
            @keyframes hologramPulse {
              0%, 100% { transform: scale(1); opacity: 0.9; }
              50% { transform: scale(1.02); opacity: 1; }
            }
          `}} />
          
          <div style={{ 
            color: meta.color, 
            fontWeight: 'bold', 
            fontSize: '16px', 
            marginBottom: '8px',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            borderBottom: `1px solid ${meta.color}44`,
            paddingBottom: '4px'
          }}>
            {meta.name}
          </div>
          
          <div style={{ fontSize: '12px', lineHeight: '1.5', marginBottom: '12px' }}>
            {meta.lore}
          </div>
          
          <div style={{ 
            marginTop: '10px', 
            background: `${meta.color}11`,
            padding: '8px',
            borderRadius: '4px',
            fontSize: '11px',
            color: meta.color,
            borderLeft: `3px solid ${meta.color}`
          }}>
            <strong>REVELACIÓN TECNOLÓGICA:</strong>
            <div style={{ marginTop: '2px', color: 'white' }}>{meta.mechanic}</div>
          </div>
        </div>
      </Html>
    </group>
  )
}
