'use client'

import { useState } from 'react'

interface Phase {
  id: number
  title: string
  status: 'completed' | 'in-progress' | 'planned'
  description: string
  features: string[]
  technical?: string
}

const PHASES: Phase[] = [
  {
    id: 1,
    title: 'Mapa 3D Real',
    status: 'planned',
    description: 'Globe 3D interactivo con CesiumJS para visualización científica del planeta',
    features: [
      'Globe 3D real con terreno y elevación',
      'Posición solar realista',
      'Datos geoespaciales precisos',
      'Renderizado científico'
    ],
    technical: 'CesiumJS - Más potente para globe real 3D'
  },
  {
    id: 2,
    title: 'Teletransporte Cinemático',
    status: 'planned',
    description: 'Sistema de navegación fluida entre sitios arqueológicos',
    features: [
      'Click en coordenadas → vuelo suave',
      'Activación de terreno local',
      'Instanciación de modelos .glb en lat/lon',
      'Transiciones cinematográficas'
    ],
    technical: 'viewer.camera.flyTo() + Cesium.Cartesian3.fromDegrees()'
  },
  {
    id: 3,
    title: 'Movimiento Street View 3D',
    status: 'planned',
    description: 'Exploración inmersiva en primera persona',
    features: [
      'Cámara first-person',
      'Movimiento WASD o joystick',
      'Colisiones simples',
      'Terreno simplificado'
    ],
    technical: 'PointerLockControls (Three.js) o controlador custom (Cesium)'
  },
  {
    id: 4,
    title: 'Motor Geoespacial + Astronómico',
    status: 'completed',
    description: 'Sistema de coordenadas y cálculos astronómicos',
    features: [
      '✅ Sistema de coordenadas geográficas',
      '✅ Cálculos solares (Julian day, sidereal time)',
      '✅ Alineaciones astronómicas',
      '✅ 20 sitios arqueológicos reales',
      '✅ Sistema de teletransporte'
    ],
    technical: 'CoordinateSystem + SolarCalculator + AlignmentCalculator'
  },
  {
    id: 5,
    title: 'Avatar Conversacional con IA',
    status: 'completed',
    description: 'Modelo 3D con presencia, personalidad y cognición',
    features: [
      '✅ Cerebro con personalidad persistente',
      '✅ Estado emocional evolutivo',
      '✅ Memoria conversacional',
      '✅ Mirada inteligente que sigue cámara',
      '✅ Respiración y parpadeo',
      '✅ Gestos contextuales',
      '✅ Voz mejorada con TTS',
      '✅ OpenRouter + Ollama'
    ],
    technical: 'AvatarBrain + AvatarBody + OpenRouterIntegration'
  },
  {
    id: 6,
    title: 'Experiencia Inmersiva Completa',
    status: 'in-progress',
    description: 'Integración de todos los sistemas en una experiencia cohesiva',
    features: [
      '🔄 Globe 3D visible al entrar',
      '🔄 Click en coordenada → cámara vuela',
      '🔄 Modelo aparece en sitio',
      '🔄 Usuario camina y se acerca',
      '🔄 Modelo detecta proximidad',
      '🔄 Interacción automática',
      '✅ Chat con IA + gestos'
    ],
    technical: 'Integración: Cesium + R3F + AvatarSystem + ProximityDetection'
  }
]

export default function RoadmapPanel() {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedPhase, setSelectedPhase] = useState<Phase | null>(null)

  const getStatusColor = (status: Phase['status']) => {
    switch (status) {
      case 'completed': return '#10b981'
      case 'in-progress': return '#f59e0b'
      case 'planned': return '#6b7280'
    }
  }

  const getStatusIcon = (status: Phase['status']) => {
    switch (status) {
      case 'completed': return '✅'
      case 'in-progress': return '🔄'
      case 'planned': return '📋'
    }
  }

  const getStatusText = (status: Phase['status']) => {
    switch (status) {
      case 'completed': return 'Completado'
      case 'in-progress': return 'En Progreso'
      case 'planned': return 'Planeado'
    }
  }

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '100px',
          right: '20px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          border: '2px solid rgba(255,255,255,0.3)',
          color: 'white',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 4px 20px rgba(102, 126, 234, 0.5)',
          zIndex: 1000,
          transition: 'all 0.3s ease',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
        onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
        title="Roadmap del Proyecto"
      >
        🗺️
      </button>

      {/* Panel de roadmap */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '90%',
          maxWidth: '1200px',
          height: '80vh',
          background: 'rgba(10, 10, 10, 0.95)',
          backdropFilter: 'blur(20px)',
          borderRadius: '16px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.5)',
          zIndex: 1001,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          border: '1px solid rgba(255,255,255,0.1)'
        }}>
          {/* Header */}
          <div style={{
            padding: '20px 30px',
            borderBottom: '1px solid rgba(255,255,255,0.1)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)'
          }}>
            <div>
              <h2 style={{
                margin: 0,
                color: 'white',
                fontSize: '24px',
                fontWeight: 'bold',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>
                🗺️ Roadmap: ArcheoScope 3D Viewer
              </h2>
              <p style={{
                margin: '5px 0 0 0',
                color: '#888',
                fontSize: '14px'
              }}>
                De viewer estático a experiencia inmersiva con IA
              </p>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              style={{
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '8px',
                color: 'white',
                fontSize: '20px',
                width: '40px',
                height: '40px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              ✕
            </button>
          </div>

          {/* Content */}
          <div style={{
            flex: 1,
            display: 'flex',
            overflow: 'hidden'
          }}>
            {/* Lista de fases */}
            <div style={{
              width: '350px',
              borderRight: '1px solid rgba(255,255,255,0.1)',
              overflowY: 'auto',
              padding: '20px'
            }}>
              {PHASES.map((phase) => (
                <div
                  key={phase.id}
                  onClick={() => setSelectedPhase(phase)}
                  style={{
                    padding: '15px',
                    marginBottom: '10px',
                    background: selectedPhase?.id === phase.id 
                      ? 'rgba(102, 126, 234, 0.2)' 
                      : 'rgba(255,255,255,0.05)',
                    border: `1px solid ${selectedPhase?.id === phase.id ? '#667eea' : 'rgba(255,255,255,0.1)'}`,
                    borderRadius: '8px',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    if (selectedPhase?.id !== phase.id) {
                      e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedPhase?.id !== phase.id) {
                      e.currentTarget.style.background = 'rgba(255,255,255,0.05)'
                    }
                  }}
                >
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    marginBottom: '8px'
                  }}>
                    <span style={{ fontSize: '20px' }}>
                      {getStatusIcon(phase.status)}
                    </span>
                    <div style={{ flex: 1 }}>
                      <div style={{
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: 'bold'
                      }}>
                        FASE {phase.id}
                      </div>
                      <div style={{
                        color: getStatusColor(phase.status),
                        fontSize: '11px',
                        marginTop: '2px'
                      }}>
                        {getStatusText(phase.status)}
                      </div>
                    </div>
                  </div>
                  <div style={{
                    color: '#ccc',
                    fontSize: '13px',
                    lineHeight: '1.4'
                  }}>
                    {phase.title}
                  </div>
                </div>
              ))}
            </div>

            {/* Detalle de fase */}
            <div style={{
              flex: 1,
              overflowY: 'auto',
              padding: '30px'
            }}>
              {selectedPhase ? (
                <>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '15px',
                    marginBottom: '20px'
                  }}>
                    <span style={{ fontSize: '40px' }}>
                      {getStatusIcon(selectedPhase.status)}
                    </span>
                    <div>
                      <h3 style={{
                        margin: 0,
                        color: 'white',
                        fontSize: '28px',
                        fontWeight: 'bold'
                      }}>
                        FASE {selectedPhase.id}: {selectedPhase.title}
                      </h3>
                      <div style={{
                        color: getStatusColor(selectedPhase.status),
                        fontSize: '14px',
                        marginTop: '5px',
                        fontWeight: 'bold'
                      }}>
                        {getStatusText(selectedPhase.status)}
                      </div>
                    </div>
                  </div>

                  <p style={{
                    color: '#ccc',
                    fontSize: '16px',
                    lineHeight: '1.6',
                    marginBottom: '25px'
                  }}>
                    {selectedPhase.description}
                  </p>

                  {selectedPhase.technical && (
                    <div style={{
                      padding: '15px',
                      background: 'rgba(102, 126, 234, 0.1)',
                      border: '1px solid rgba(102, 126, 234, 0.3)',
                      borderRadius: '8px',
                      marginBottom: '25px'
                    }}>
                      <div style={{
                        color: '#667eea',
                        fontSize: '12px',
                        fontWeight: 'bold',
                        marginBottom: '8px'
                      }}>
                        💻 TÉCNICO
                      </div>
                      <div style={{
                        color: '#ccc',
                        fontSize: '14px',
                        fontFamily: 'monospace'
                      }}>
                        {selectedPhase.technical}
                      </div>
                    </div>
                  )}

                  <div style={{
                    color: 'white',
                    fontSize: '16px',
                    fontWeight: 'bold',
                    marginBottom: '15px'
                  }}>
                    Características:
                  </div>

                  <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '10px'
                  }}>
                    {selectedPhase.features.map((feature, index) => (
                      <div
                        key={index}
                        style={{
                          padding: '12px 15px',
                          background: 'rgba(255,255,255,0.05)',
                          border: '1px solid rgba(255,255,255,0.1)',
                          borderRadius: '6px',
                          color: '#ccc',
                          fontSize: '14px',
                          lineHeight: '1.5'
                        }}
                      >
                        {feature}
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: '100%',
                  color: '#666',
                  fontSize: '16px'
                }}>
                  Selecciona una fase para ver detalles
                </div>
              )}
            </div>
          </div>

          {/* Footer con progreso */}
          <div style={{
            padding: '15px 30px',
            borderTop: '1px solid rgba(255,255,255,0.1)',
            background: 'rgba(0,0,0,0.3)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div style={{
              display: 'flex',
              gap: '20px',
              fontSize: '14px'
            }}>
              <div style={{ color: '#10b981' }}>
                ✅ Completadas: {PHASES.filter(p => p.status === 'completed').length}
              </div>
              <div style={{ color: '#f59e0b' }}>
                🔄 En Progreso: {PHASES.filter(p => p.status === 'in-progress').length}
              </div>
              <div style={{ color: '#6b7280' }}>
                📋 Planeadas: {PHASES.filter(p => p.status === 'planned').length}
              </div>
            </div>
            <div style={{
              color: '#888',
              fontSize: '12px'
            }}>
              Progreso: {Math.round((PHASES.filter(p => p.status === 'completed').length / PHASES.length) * 100)}%
            </div>
          </div>
        </div>
      )}
    </>
  )
}
