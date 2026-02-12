'use client'

import { useState } from 'react'

interface CoordinateInputProps {
  onCoordinateSubmit: (lat: number, lon: number) => void
  currentLocation?: { lat: number, lon: number } | null
}

export default function CoordinateInput({ onCoordinateSubmit, currentLocation }: CoordinateInputProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [lat, setLat] = useState(currentLocation?.lat.toFixed(4) || '')
  const [lon, setLon] = useState(currentLocation?.lon.toFixed(4) || '')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const latitude = parseFloat(lat)
    const longitude = parseFloat(lon)

    if (isNaN(latitude) || isNaN(longitude)) {
      alert('Por favor ingresa coordenadas válidas')
      return
    }

    if (latitude < -90 || latitude > 90) {
      alert('Latitud debe estar entre -90 y 90')
      return
    }

    if (longitude < -180 || longitude > 180) {
      alert('Longitud debe estar entre -180 y 180')
      return
    }

    onCoordinateSubmit(latitude, longitude)
    setIsOpen(false)
  }

  // Coordenadas de sitios famosos
  const famousSites = [
    { name: 'Machu Picchu', lat: -13.1631, lon: -72.5450 },
    { name: 'Pirámides de Giza', lat: 29.9792, lon: 31.1342 },
    { name: 'Stonehenge', lat: 51.1789, lon: -1.8262 },
    { name: 'Isla de Pascua', lat: -27.1127, lon: -109.3497 },
    { name: 'Angkor Wat', lat: 13.4125, lon: 103.8670 },
    { name: 'Petra', lat: 30.3285, lon: 35.4444 },
  ]

  return (
    <>
      {/* Botón para abrir panel */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          zIndex: 1001,
          padding: '12px 20px',
          background: 'rgba(102, 126, 234, 0.9)',
          border: '1px solid rgba(255,255,255,0.3)',
          borderRadius: '8px',
          color: 'white',
          fontSize: '14px',
          fontWeight: 'bold',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          transition: 'all 0.2s',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
        }}
        onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(102, 126, 234, 1)'}
        onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(102, 126, 234, 0.9)'}
      >
        📍 Coordenadas
      </button>

      {/* Panel de coordenadas */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          top: '80px',
          right: '20px',
          zIndex: 1000,
          width: '350px',
          background: 'rgba(0, 0, 0, 0.95)',
          backdropFilter: 'blur(10px)',
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          border: '1px solid rgba(255,255,255,0.1)'
        }}>
          <h3 style={{
            margin: '0 0 15px 0',
            color: 'white',
            fontSize: '18px',
            fontWeight: 'bold'
          }}>
            Ingresar Coordenadas
          </h3>

          {/* Ubicación actual */}
          {currentLocation && (
            <div style={{
              padding: '10px',
              background: 'rgba(102, 126, 234, 0.2)',
              borderRadius: '6px',
              marginBottom: '15px',
              fontSize: '12px',
              color: 'rgba(255,255,255,0.8)'
            }}>
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>📍 Ubicación actual:</div>
              <div>Lat: {currentLocation.lat.toFixed(4)}°</div>
              <div>Lon: {currentLocation.lon.toFixed(4)}°</div>
            </div>
          )}

          {/* Formulario */}
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <label style={{
                display: 'block',
                color: 'rgba(255,255,255,0.8)',
                fontSize: '12px',
                marginBottom: '5px'
              }}>
                Latitud (-90 a 90)
              </label>
              <input
                type="text"
                value={lat}
                onChange={(e) => setLat(e.target.value)}
                placeholder="-13.1631"
                style={{
                  width: '100%',
                  padding: '10px',
                  background: 'rgba(255,255,255,0.1)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '6px',
                  color: 'white',
                  fontSize: '14px',
                  outline: 'none'
                }}
              />
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label style={{
                display: 'block',
                color: 'rgba(255,255,255,0.8)',
                fontSize: '12px',
                marginBottom: '5px'
              }}>
                Longitud (-180 a 180)
              </label>
              <input
                type="text"
                value={lon}
                onChange={(e) => setLon(e.target.value)}
                placeholder="-72.5450"
                style={{
                  width: '100%',
                  padding: '10px',
                  background: 'rgba(255,255,255,0.1)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '6px',
                  color: 'white',
                  fontSize: '14px',
                  outline: 'none'
                }}
              />
            </div>

            <button
              type="submit"
              style={{
                width: '100%',
                padding: '12px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                borderRadius: '8px',
                color: 'white',
                fontSize: '14px',
                fontWeight: 'bold',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              🌍 Ir a Ubicación
            </button>
          </form>

          {/* Sitios famosos */}
          <div style={{ marginTop: '20px' }}>
            <div style={{
              color: 'rgba(255,255,255,0.6)',
              fontSize: '12px',
              marginBottom: '10px',
              fontWeight: 'bold'
            }}>
              Sitios Arqueológicos Famosos:
            </div>
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '6px'
            }}>
              {famousSites.map((site) => (
                <button
                  key={site.name}
                  onClick={() => {
                    setLat(site.lat.toFixed(4))
                    setLon(site.lon.toFixed(4))
                  }}
                  style={{
                    padding: '8px 12px',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '6px',
                    color: 'rgba(255,255,255,0.8)',
                    fontSize: '12px',
                    cursor: 'pointer',
                    textAlign: 'left',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
                    e.currentTarget.style.borderColor = 'rgba(102, 126, 234, 0.5)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'rgba(255,255,255,0.05)'
                    e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)'
                  }}
                >
                  {site.name}
                </button>
              ))}
            </div>
          </div>

          {/* Botón cerrar */}
          <button
            onClick={() => setIsOpen(false)}
            style={{
              marginTop: '15px',
              width: '100%',
              padding: '8px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: '6px',
              color: 'rgba(255,255,255,0.6)',
              fontSize: '12px',
              cursor: 'pointer'
            }}
          >
            Cerrar
          </button>
        </div>
      )}
    </>
  )
}
