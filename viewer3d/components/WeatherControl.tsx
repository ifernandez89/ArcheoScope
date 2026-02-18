'use client'

import { useState } from 'react'

interface WeatherControlProps {
  onWeatherChange: (weather: { 
    snow: boolean
    rainLight: boolean
    rainModerate: boolean
    rainHeavy: boolean
  }) => void
}

export default function WeatherControl({ onWeatherChange }: WeatherControlProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [weather, setWeather] = useState({ 
    snow: false, 
    rainLight: false,
    rainModerate: false,
    rainHeavy: false
  })

  const handleToggle = (type: 'snow' | 'rainLight' | 'rainModerate' | 'rainHeavy') => {
    // Si se activa un tipo de lluvia, desactivar los otros tipos de lluvia
    let newWeather = { ...weather }
    
    if (type.startsWith('rain')) {
      // Desactivar todos los tipos de lluvia primero
      newWeather.rainLight = false
      newWeather.rainModerate = false
      newWeather.rainHeavy = false
      // Activar solo el seleccionado
      newWeather[type] = !weather[type]
    } else {
      // Para nieve, solo toggle
      newWeather[type] = !weather[type]
    }
    
    setWeather(newWeather)
    onWeatherChange(newWeather)
  }

  return (
    <>
      {/* Botón principal */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 1001,
          padding: '10px 16px',
          background: 'rgba(66, 153, 225, 0.85)',
          border: '1px solid rgba(255,255,255,0.3)',
          borderRadius: '8px',
          color: 'white',
          fontSize: '13px',
          fontWeight: '600',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          transition: 'all 0.2s ease'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'rgba(66, 153, 225, 0.95)'
          e.currentTarget.style.transform = 'translateY(-2px)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'rgba(66, 153, 225, 0.85)'
          e.currentTarget.style.transform = 'translateY(0)'
        }}
      >
        <span style={{ fontSize: '16px' }}>🌦️</span>
        Clima
      </button>

      {/* Panel desplegable */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '70px',
            right: '20px',
            zIndex: 1000,
            background: 'rgba(26, 32, 44, 0.95)',
            border: '1px solid rgba(255,255,255,0.2)',
            borderRadius: '12px',
            padding: '16px',
            minWidth: '200px',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 8px 24px rgba(0,0,0,0.3)',
            animation: 'slideUp 0.2s ease'
          }}
        >
          <style jsx>{`
            @keyframes slideUp {
              from {
                opacity: 0;
                transform: translateY(10px);
              }
              to {
                opacity: 1;
                transform: translateY(0);
              }
            }
          `}</style>

          <div style={{ marginBottom: '12px', color: 'white', fontSize: '14px', fontWeight: '600' }}>
            Efectos Climáticos
          </div>

          {/* Checkbox Nieve */}
          <label
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              padding: '8px',
              cursor: 'pointer',
              borderRadius: '6px',
              transition: 'background 0.2s ease',
              marginBottom: '6px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
            }}
          >
            <input
              type="checkbox"
              checked={weather.snow}
              onChange={() => handleToggle('snow')}
              style={{
                width: '16px',
                height: '16px',
                cursor: 'pointer',
                accentColor: '#4299e1'
              }}
            />
            <span style={{ color: 'white', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>❄️</span>
              Nieve
            </span>
          </label>

          {/* Separador */}
          <div style={{ 
            margin: '10px 0', 
            borderTop: '1px solid rgba(255,255,255,0.1)',
            paddingTop: '10px'
          }}>
            <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '12px', marginBottom: '8px' }}>
              Lluvia
            </div>
          </div>

          {/* Checkbox Lluvia Ligera */}
          <label
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              padding: '8px',
              cursor: 'pointer',
              borderRadius: '6px',
              transition: 'background 0.2s ease',
              marginBottom: '6px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
            }}
          >
            <input
              type="checkbox"
              checked={weather.rainLight}
              onChange={() => handleToggle('rainLight')}
              style={{
                width: '16px',
                height: '16px',
                cursor: 'pointer',
                accentColor: '#4299e1'
              }}
            />
            <span style={{ color: 'white', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>🌧️</span>
              Ligera
            </span>
          </label>

          {/* Checkbox Lluvia Moderada */}
          <label
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              padding: '8px',
              cursor: 'pointer',
              borderRadius: '6px',
              transition: 'background 0.2s ease',
              marginBottom: '6px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
            }}
          >
            <input
              type="checkbox"
              checked={weather.rainModerate}
              onChange={() => handleToggle('rainModerate')}
              style={{
                width: '16px',
                height: '16px',
                cursor: 'pointer',
                accentColor: '#4299e1'
              }}
            />
            <span style={{ color: 'white', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>🌧️</span>
              Moderada
            </span>
          </label>

          {/* Checkbox Lluvia Fuerte */}
          <label
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              padding: '8px',
              cursor: 'pointer',
              borderRadius: '6px',
              transition: 'background 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
            }}
          >
            <input
              type="checkbox"
              checked={weather.rainHeavy}
              onChange={() => handleToggle('rainHeavy')}
              style={{
                width: '16px',
                height: '16px',
                cursor: 'pointer',
                accentColor: '#4299e1'
              }}
            />
            <span style={{ color: 'white', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>⛈️</span>
              Fuerte
            </span>
          </label>

          <div style={{ 
            marginTop: '12px', 
            paddingTop: '12px', 
            borderTop: '1px solid rgba(255,255,255,0.1)',
            color: 'rgba(255,255,255,0.6)',
            fontSize: '11px',
            textAlign: 'center'
          }}>
            Más climas próximamente
          </div>
        </div>
      )}
    </>
  )
}
