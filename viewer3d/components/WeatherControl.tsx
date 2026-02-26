'use client'

import { useState } from 'react'

export interface WeatherState {
  snow: boolean
  rainLight: boolean
  rainModerate: boolean
  rainHeavy: boolean
  wind: boolean
  fog: boolean
  storm: boolean
  lightning: boolean
  tornado: boolean
  clouds: boolean
  earthquake: boolean
}

interface WeatherControlProps {
  onWeatherChange: (weather: WeatherState) => void
}

export default function WeatherControl({ onWeatherChange }: WeatherControlProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [weather, setWeather] = useState<WeatherState>({ 
    snow: false, 
    rainLight: false,
    rainModerate: false,
    rainHeavy: false,
    wind: false,
    fog: false,
    storm: false,
    lightning: false,
    tornado: false,
    clouds: false,
    earthquake: false
  })

  const handleToggle = (type: keyof WeatherState) => {
    let newWeather = { ...weather }
    
    // Si se activa un tipo de lluvia, desactivar los otros tipos de lluvia
    if (type.startsWith('rain')) {
      newWeather.rainLight = false
      newWeather.rainModerate = false
      newWeather.rainHeavy = false
      newWeather[type] = !weather[type]
    } 
    // Si se activa tormenta, activar lluvia fuerte automáticamente
    else if (type === 'storm') {
      newWeather.storm = !weather.storm
      if (newWeather.storm) {
        newWeather.rainHeavy = true
        newWeather.rainLight = false
        newWeather.rainModerate = false
        newWeather.lightning = true // Activar rayos con tormenta
      }
    }
    // Para otros efectos, solo toggle
    else {
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
            minWidth: '220px',
            maxHeight: '500px',
            overflowY: 'auto',
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
            Sistema Climático
          </div>

          {/* Precipitación */}
          <div style={{ 
            margin: '10px 0', 
            borderTop: '1px solid rgba(255,255,255,0.1)',
            paddingTop: '10px'
          }}>
            <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '11px', marginBottom: '8px', textTransform: 'uppercase' }}>
              Precipitación
            </div>
          </div>

          <WeatherCheckbox 
            checked={weather.snow} 
            onChange={() => handleToggle('snow')}
            icon="❄️"
            label="Nieve"
          />

          <WeatherCheckbox 
            checked={weather.rainLight} 
            onChange={() => handleToggle('rainLight')}
            icon="🌧️"
            label="Lluvia Ligera"
          />

          <WeatherCheckbox 
            checked={weather.rainModerate} 
            onChange={() => handleToggle('rainModerate')}
            icon="🌧️"
            label="Lluvia Moderada"
          />

          <WeatherCheckbox 
            checked={weather.rainHeavy} 
            onChange={() => handleToggle('rainHeavy')}
            icon="⛈️"
            label="Lluvia Fuerte"
          />

          {/* Efectos Atmosféricos */}
          <div style={{ 
            margin: '10px 0', 
            borderTop: '1px solid rgba(255,255,255,0.1)',
            paddingTop: '10px'
          }}>
            <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '11px', marginBottom: '8px', textTransform: 'uppercase' }}>
              Atmósfera
            </div>
          </div>

          <WeatherCheckbox 
            checked={weather.wind} 
            onChange={() => handleToggle('wind')}
            icon="🌬️"
            label="Viento"
          />

          <WeatherCheckbox 
            checked={weather.fog} 
            onChange={() => handleToggle('fog')}
            icon="🌫️"
            label="Niebla"
          />

          <WeatherCheckbox 
            checked={weather.clouds} 
            onChange={() => handleToggle('clouds')}
            icon="☁️"
            label="Nubes"
          />

          {/* Fenómenos Extremos */}
          <div style={{ 
            margin: '10px 0', 
            borderTop: '1px solid rgba(255,255,255,0.1)',
            paddingTop: '10px'
          }}>
            <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '11px', marginBottom: '8px', textTransform: 'uppercase' }}>
              Fenómenos Extremos
            </div>
          </div>

          <WeatherCheckbox 
            checked={weather.storm} 
            onChange={() => handleToggle('storm')}
            icon="⚡"
            label="Tormenta Eléctrica"
          />

          <WeatherCheckbox 
            checked={weather.lightning} 
            onChange={() => handleToggle('lightning')}
            icon="⚡"
            label="Rayos"
          />

          <WeatherCheckbox 
            checked={weather.tornado} 
            onChange={() => handleToggle('tornado')}
            icon="🌪️"
            label="Tornado"
          />

          <WeatherCheckbox 
            checked={weather.earthquake} 
            onChange={() => handleToggle('earthquake')}
            icon="🌋"
            label="Terremoto"
          />

          <div style={{ 
            marginTop: '12px', 
            paddingTop: '12px', 
            borderTop: '1px solid rgba(255,255,255,0.1)',
            color: 'rgba(255,255,255,0.5)',
            fontSize: '10px',
            textAlign: 'center'
          }}>
            Sistema climático dinámico v2.0
          </div>
        </div>
      )}
    </>
  )
}

// Componente reutilizable para checkboxes
function WeatherCheckbox({ 
  checked, 
  onChange, 
  icon, 
  label 
}: { 
  checked: boolean
  onChange: () => void
  icon: string
  label: string
}) {
  return (
    <label
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        padding: '8px',
        cursor: 'pointer',
        borderRadius: '6px',
        transition: 'background 0.2s ease',
        marginBottom: '4px'
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
        checked={checked}
        onChange={onChange}
        style={{
          width: '16px',
          height: '16px',
          cursor: 'pointer',
          accentColor: '#4299e1'
        }}
      />
      <span style={{ color: 'white', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}>
        <span>{icon}</span>
        {label}
      </span>
    </label>
  )
}
