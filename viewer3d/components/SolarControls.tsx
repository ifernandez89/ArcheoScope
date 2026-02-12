'use client'

import { useState, useEffect } from 'react'
import type { SolarPosition } from '@/astro/solar-calculator'
import type { GeographicCoordinates } from '@/geo/coordinate-system'

interface SolarControlsProps {
  onDateChange: (date: Date) => void
  onLocationChange: (location: GeographicCoordinates) => void
  onTimeSpeedChange: (speed: number) => void
  currentDate: Date
  currentLocation: GeographicCoordinates
  solarPosition: SolarPosition | null
  isSimulating: boolean
  onToggleSimulation: () => void
}

export default function SolarControls({
  onDateChange,
  onLocationChange,
  onTimeSpeedChange,
  currentDate,
  currentLocation,
  solarPosition,
  isSimulating,
  onToggleSimulation
}: SolarControlsProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [timeSpeed, setTimeSpeed] = useState(1)

  const handleTimeSpeedChange = (speed: number) => {
    setTimeSpeed(speed)
    onTimeSpeedChange(speed)
  }

  const handleQuickTime = (hour: number) => {
    const newDate = new Date(currentDate)
    newDate.setHours(hour, 0, 0, 0)
    onDateChange(newDate)
  }

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          top: '160px',
          right: '20px',
          width: '50px',
          height: '50px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #ffa726 0%, #fb8c00 100%)',
          border: 'none',
          color: 'white',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
          zIndex: 1000,
          transition: 'transform 0.2s',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
        onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
      >
        ☀️
      </button>

      {/* Panel de controles */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          top: '220px',
          right: '20px',
          width: '320px',
          background: 'rgba(0, 0, 0, 0.85)',
          backdropFilter: 'blur(10px)',
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          zIndex: 999,
          maxHeight: '500px',
          overflowY: 'auto'
        }}>
          <h3 style={{
            margin: '0 0 15px 0',
            color: 'white',
            fontSize: '18px',
            fontWeight: 'bold'
          }}>
            ☀️ Control Solar
          </h3>

          {/* Simulación toggle */}
          <button
            onClick={onToggleSimulation}
            style={{
              width: '100%',
              padding: '12px',
              marginBottom: '15px',
              background: isSimulating 
                ? 'rgba(239, 68, 68, 0.3)' 
                : 'rgba(74, 222, 128, 0.3)',
              border: isSimulating 
                ? '2px solid #ef4444' 
                : '2px solid #4ade80',
              borderRadius: '8px',
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
          >
            {isSimulating ? '⏸️ Pausar Simulación' : '▶️ Iniciar Simulación'}
          </button>

          {/* Posición solar actual */}
          {solarPosition && (
            <div style={{
              background: 'rgba(255, 167, 38, 0.1)',
              border: '1px solid rgba(255, 167, 38, 0.3)',
              borderRadius: '8px',
              padding: '12px',
              marginBottom: '15px'
            }}>
              <div style={{
                color: 'rgba(255,255,255,0.7)',
                fontSize: '12px',
                marginBottom: '8px',
                fontWeight: 'bold'
              }}>
                POSICIÓN SOLAR
              </div>
              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '8px',
                fontSize: '13px',
                color: 'white'
              }}>
                <div>
                  <span style={{ color: 'rgba(255,255,255,0.6)' }}>Azimut:</span>
                  <br />
                  {solarPosition.azimuth.toFixed(1)}°
                </div>
                <div>
                  <span style={{ color: 'rgba(255,255,255,0.6)' }}>Altitud:</span>
                  <br />
                  {solarPosition.altitude.toFixed(1)}°
                </div>
              </div>
            </div>
          )}

          {/* Fecha y hora */}
          <div style={{ marginBottom: '15px' }}>
            <label style={{
              color: 'rgba(255,255,255,0.7)',
              fontSize: '12px',
              fontWeight: 'bold',
              display: 'block',
              marginBottom: '5px'
            }}>
              FECHA Y HORA
            </label>
            <input
              type="datetime-local"
              value={currentDate.toISOString().slice(0, 16)}
              onChange={(e) => onDateChange(new Date(e.target.value))}
              style={{
                width: '100%',
                padding: '8px',
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '6px',
                color: 'white',
                fontSize: '13px'
              }}
            />
          </div>

          {/* Atajos de hora */}
          <div style={{ marginBottom: '15px' }}>
            <label style={{
              color: 'rgba(255,255,255,0.7)',
              fontSize: '12px',
              fontWeight: 'bold',
              display: 'block',
              marginBottom: '8px'
            }}>
              ATAJOS DE HORA
            </label>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '6px'
            }}>
              {[6, 9, 12, 15, 18, 21].map(hour => (
                <button
                  key={hour}
                  onClick={() => handleQuickTime(hour)}
                  style={{
                    padding: '8px',
                    background: 'rgba(255,255,255,0.1)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    borderRadius: '6px',
                    color: 'white',
                    fontSize: '12px',
                    cursor: 'pointer'
                  }}
                >
                  {hour}:00
                </button>
              ))}
            </div>
          </div>

          {/* Velocidad de tiempo */}
          <div style={{ marginBottom: '15px' }}>
            <label style={{
              color: 'rgba(255,255,255,0.7)',
              fontSize: '12px',
              fontWeight: 'bold',
              display: 'block',
              marginBottom: '5px'
            }}>
              VELOCIDAD: {timeSpeed}x
            </label>
            <input
              type="range"
              min="1"
              max="3600"
              step="1"
              value={timeSpeed}
              onChange={(e) => handleTimeSpeedChange(Number(e.target.value))}
              disabled={!isSimulating}
              style={{
                width: '100%',
                height: '6px',
                borderRadius: '3px',
                background: `linear-gradient(to right, #ffa726 0%, #ffa726 ${(Math.log(timeSpeed) / Math.log(3600)) * 100}%, rgba(255,255,255,0.1) ${(Math.log(timeSpeed) / Math.log(3600)) * 100}%, rgba(255,255,255,0.1) 100%)`,
                outline: 'none',
                cursor: isSimulating ? 'pointer' : 'not-allowed',
                opacity: isSimulating ? 1 : 0.5
              }}
            />
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              fontSize: '10px',
              color: 'rgba(255,255,255,0.5)',
              marginTop: '3px'
            }}>
              <span>1x</span>
              <span>60x</span>
              <span>3600x</span>
            </div>
          </div>

          {/* Ubicación */}
          <div style={{ marginBottom: '15px' }}>
            <label style={{
              color: 'rgba(255,255,255,0.7)',
              fontSize: '12px',
              fontWeight: 'bold',
              display: 'block',
              marginBottom: '8px'
            }}>
              UBICACIÓN
            </label>
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }}>
              <div>
                <label style={{
                  color: 'rgba(255,255,255,0.6)',
                  fontSize: '11px',
                  display: 'block',
                  marginBottom: '3px'
                }}>
                  Latitud
                </label>
                <input
                  type="number"
                  value={currentLocation.latitude.toFixed(4)}
                  onChange={(e) => onLocationChange({
                    ...currentLocation,
                    latitude: Number(e.target.value)
                  })}
                  step="0.0001"
                  style={{
                    width: '100%',
                    padding: '6px',
                    background: 'rgba(255,255,255,0.1)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    borderRadius: '4px',
                    color: 'white',
                    fontSize: '12px'
                  }}
                />
              </div>
              <div>
                <label style={{
                  color: 'rgba(255,255,255,0.6)',
                  fontSize: '11px',
                  display: 'block',
                  marginBottom: '3px'
                }}>
                  Longitud
                </label>
                <input
                  type="number"
                  value={currentLocation.longitude.toFixed(4)}
                  onChange={(e) => onLocationChange({
                    ...currentLocation,
                    longitude: Number(e.target.value)
                  })}
                  step="0.0001"
                  style={{
                    width: '100%',
                    padding: '6px',
                    background: 'rgba(255,255,255,0.1)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    borderRadius: '4px',
                    color: 'white',
                    fontSize: '12px'
                  }}
                />
              </div>
            </div>
          </div>

          {/* Info */}
          <div style={{
            padding: '10px',
            background: 'rgba(255, 167, 38, 0.1)',
            border: '1px solid rgba(255, 167, 38, 0.3)',
            borderRadius: '6px',
            fontSize: '11px',
            color: 'rgba(255,255,255,0.7)',
            lineHeight: '1.4'
          }}>
            💡 La simulación calcula la posición real del sol basada en fecha, hora y ubicación geográfica.
          </div>
        </div>
      )}
    </>
  )
}
