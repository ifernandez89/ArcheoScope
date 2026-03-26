'use client'

import { useRef, useEffect, useState, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { useGLTF, Html, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface ItemDiscoveryPopupProps {
  itemName: string
  itemDescription: string
  modelPath: string
  onClose: () => void
}

export default function ItemDiscoveryPopup({
  itemName,
  itemDescription,
  modelPath,
  onClose
}: ItemDiscoveryPopupProps) {
  const groupRef = useRef<THREE.Group>(null)
  const { scene } = useGLTF(modelPath)
  const timeRef = useRef(0)
  const [modelLoaded, setModelLoaded] = useState(false)

  // Configurar modelo
  useEffect(() => {
    if (scene) {
      // Calcular bounding box y centrar
      const box = new THREE.Box3().setFromObject(scene)
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())

      // Centrar modelo
      scene.position.x = -center.x
      scene.position.y = -center.y
      scene.position.z = -center.z

      // Escalar para que sea BIEN VISIBLE
      const maxDim = Math.max(size.x, size.y, size.z)
      const scale = 2.0 / maxDim
      scene.scale.setScalar(scale)

      // Habilitar sombras
      scene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          child.castShadow = true
          child.receiveShadow = true
        }
      })
      
      setModelLoaded(true)
      console.log('🏺 Modelo cargado:', { size, scale, maxDim })
    }
  }, [scene])

  // Rotación suave del item
  useFrame((state, delta) => {
    if (groupRef.current) {
      timeRef.current += delta
      groupRef.current.rotation.y += delta * 0.5
      // Oscilación vertical sutil
      groupRef.current.position.y = Math.sin(timeRef.current * 2) * 0.1
    }
  })

  // Detectar click en el botón X (no en toda la pantalla)
  const handleClose = (e: React.MouseEvent) => {
    e.stopPropagation()
    onClose()
  }

  return (
    <>
      {/* Fondo oscuro semitransparente */}
      <Html fullscreen>
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 9999,
            animation: 'fadeIn 0.3s ease-in'
          }}
        >
          {/* Ventana modal centrada */}
          <div
            style={{
              position: 'relative',
              width: '500px',
              height: '600px',
              backgroundColor: 'rgba(20, 20, 30, 0.95)',
              borderRadius: '12px',
              border: '2px solid rgba(255, 215, 0, 0.3)',
              boxShadow: '0 0 40px rgba(255, 215, 0, 0.2)',
              display: 'flex',
              flexDirection: 'column',
              overflow: 'hidden'
            }}
          >
            {/* Botón cerrar */}
            <button
              onClick={handleClose}
              style={{
                position: 'absolute',
                top: '10px',
                right: '10px',
                width: '30px',
                height: '30px',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '50%',
                color: '#ffffff',
                fontSize: '18px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 10000,
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.2)'
                e.currentTarget.style.transform = 'scale(1.1)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.1)'
                e.currentTarget.style.transform = 'scale(1)'
              }}
            >
              ×
            </button>

            {/* Header */}
            <div
              style={{
                padding: '20px',
                textAlign: 'center',
                borderBottom: '1px solid rgba(255, 215, 0, 0.2)'
              }}
            >
              <div
                style={{
                  fontSize: '1.2rem',
                  fontWeight: 'bold',
                  color: '#ffd700',
                  textShadow: '0 0 10px rgba(255, 215, 0, 0.5)',
                  marginBottom: '8px',
                  animation: 'glow 2s ease-in-out infinite'
                }}
              >
                ¡Nuevo Item Descubierto!
              </div>
              <div
                style={{
                  fontSize: '1.1rem',
                  fontWeight: '600',
                  color: '#ffffff'
                }}
              >
                {itemName}
              </div>
            </div>

            {/* Área del modelo 3D - 60% del espacio */}
            <div
              style={{
                flex: '0 0 360px',
                position: 'relative',
                backgroundColor: 'rgba(0, 0, 0, 0.3)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              {!modelLoaded && (
                <div style={{ color: '#888', fontSize: '0.9rem' }}>
                  Cargando modelo...
                </div>
              )}
            </div>

            {/* Descripción */}
            <div
              style={{
                flex: 1,
                padding: '20px',
                overflowY: 'auto',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center'
              }}
            >
              <div
                style={{
                  fontSize: '0.85rem',
                  color: '#cccccc',
                  lineHeight: '1.5',
                  textAlign: 'center'
                }}
              >
                {itemDescription}
              </div>
            </div>
          </div>

          {/* Estilos de animación */}
          <style jsx>{`
            @keyframes fadeIn {
              from {
                opacity: 0;
              }
              to {
                opacity: 1;
              }
            }

            @keyframes glow {
              0%, 100% {
                text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
              }
              50% {
                text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
              }
            }
          `}</style>
        </div>
      </Html>

      {/* Modelo 3D renderizado en el espacio 3D */}
      {modelLoaded && (
        <group position={[0, 0, 0]}>
          {/* Cámara dedicada para el item */}
          <PerspectiveCamera makeDefault position={[0, 0, 3]} fov={50} />

          {/* Iluminación para el item */}
          <ambientLight intensity={0.5} />
          <directionalLight position={[3, 3, 3]} intensity={1.5} />
          <pointLight position={[-2, 2, 2]} intensity={0.8} color="#ffd700" />
          <pointLight position={[2, -2, 2]} intensity={0.6} color="#87ceeb" />

          {/* Modelo del item */}
          <group ref={groupRef} position={[0, 0, 0]}>
            <primitive object={scene} />
          </group>

          {/* Partículas brillantes alrededor */}
          <ParticleRing />
        </group>
      )}
    </>
  )
}

// Anillo de partículas brillantes
function ParticleRing() {
  const particlesRef = useRef<THREE.Points>(null)

  // Geometría memoizada para evitar recrear cada render
  const particlesGeometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    const particleCount = 50
    const positions = new Float32Array(particleCount * 3)

    for (let i = 0; i < particleCount; i++) {
      const angle = (i / particleCount) * Math.PI * 2
      const radius = 3 + Math.random() * 0.5
      positions[i * 3] = Math.cos(angle) * radius
      positions[i * 3 + 1] = (Math.random() - 0.5) * 2
      positions[i * 3 + 2] = Math.sin(angle) * radius
    }

    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geo
  }, [])

  useFrame(() => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y += 0.01
    }
  })

  return (
    <points ref={particlesRef} geometry={particlesGeometry}>
      <pointsMaterial
        size={0.05}
        color="#ffd700"
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  )
}
