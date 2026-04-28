'use client'

/**
 * LocalWeather — Clima Local solo para mobile
 * 
 * Muestra:
 * 🌡 Temperatura actual
 * 🌧 Probabilidad de lluvia
 * 🌙 Fase lunar (calculada localmente)
 * 
 * API: Open-Meteo (gratis, sin API key, global)
 * Cache: 30 minutos
 */

import { useEffect, useState } from 'react'

interface WeatherData {
  temperature: number
  rainProbability: number
  moonPhase: string
  moonEmoji: string
  lastUpdate: number
}

// Calcular fase lunar (algoritmo simple y preciso)
function getMoonPhase(): { phase: string; emoji: string } {
  const now = new Date()
  const lp = 2551443 // segundos del ciclo lunar
  const newMoon = new Date('1970-01-07T20:35:00Z')
  
  const phase = ((now.getTime() - newMoon.getTime()) / 1000) % lp
  const phaseIndex = Math.floor((phase / lp) * 8)
  
  const phases = [
    { name: 'Luna Nueva', emoji: '🌑' },
    { name: 'Creciente', emoji: '🌒' },
    { name: 'Cuarto Creciente', emoji: '🌓' },
    { name: 'Gibosa Creciente', emoji: '🌔' },
    { name: 'Luna Llena', emoji: '🌕' },
    { name: 'Gibosa Menguante', emoji: '🌖' },
    { name: 'Cuarto Menguante', emoji: '🌗' },
    { name: 'Menguante', emoji: '🌘' }
  ]
  
  return { phase: phases[phaseIndex].name, emoji: phases[phaseIndex].emoji }
}

// Obtener clima desde Open-Meteo
async function fetchWeather(lat: number, lon: number): Promise<Omit<WeatherData, 'lastUpdate'>> {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,precipitation_probability`
  
  try {
    const response = await fetch(url)
    const data = await response.json()
    
    const moon = getMoonPhase()
    
    return {
      temperature: Math.round(data.current.temperature_2m),
      rainProbability: data.current.precipitation_probability || 0,
      moonPhase: moon.phase,
      moonEmoji: moon.emoji
    }
  } catch (error) {
    console.error('❌ Error fetching weather:', error)
    const moon = getMoonPhase()
    return {
      temperature: 0,
      rainProbability: 0,
      moonPhase: moon.phase,
      moonEmoji: moon.emoji
    }
  }
}

// Cache key
const CACHE_KEY = 'archeoscope_local_weather'
const CACHE_DURATION = 30 * 60 * 1000 // 30 minutos

export default function LocalWeather() {
  const [weather, setWeather] = useState<WeatherData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isExpanded, setIsExpanded] = useState(false)

  useEffect(() => {
    // Solo cargar en mobile
    const isMobile = window.innerWidth <= 768
    if (!isMobile) {
      setLoading(false)
      return
    }

    // Intentar cargar desde cache
    const cached = localStorage.getItem(CACHE_KEY)
    if (cached) {
      const data: WeatherData = JSON.parse(cached)
      const age = Date.now() - data.lastUpdate
      
      if (age < CACHE_DURATION) {
        console.log('🌤️ Clima cargado desde cache')
        setWeather(data)
        setLoading(false)
        return
      }
    }

    // Obtener ubicación y clima
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords
          console.log('📍 Ubicación obtenida:', { latitude, longitude })
          
          const weatherData = await fetchWeather(latitude, longitude)
          const fullData: WeatherData = {
            ...weatherData,
            lastUpdate: Date.now()
          }
          
          // Guardar en cache
          localStorage.setItem(CACHE_KEY, JSON.stringify(fullData))
          
          setWeather(fullData)
          setLoading(false)
        },
        (err) => {
          console.error('❌ Error de geolocalización:', err)
          setError('Ubicación no disponible')
          setLoading(false)
        }
      )
    } else {
      setError('Geolocalización no soportada')
      setLoading(false)
    }
  }, [])

  // No mostrar en desktop
  if (typeof window !== 'undefined' && window.innerWidth > 768) {
    return null
  }

  if (loading) {
    return (
      <div style={{
        position: 'fixed',
        top: 12,
        left: 12,
        zIndex: 999,
        background: 'rgba(0, 0, 0, 0.75)',
        backdropFilter: 'blur(8px)',
        borderRadius: '12px',
        padding: '8px 12px',
        border: '1px solid rgba(255, 255, 255, 0.15)',
        color: '#fff',
        fontSize: '12px',
        letterSpacing: '0.5px'
      }}>
        <span style={{ opacity: 0.6 }}>⏳ Cargando clima...</span>
      </div>
    )
  }

  if (error || !weather) {
    return null // No mostrar si hay error
  }

  // Vista compacta (por defecto)
  if (!isExpanded) {
    return (
      <button
        onClick={() => setIsExpanded(true)}
        style={{
          position: 'fixed',
          top: 12,
          left: 12,
          zIndex: 999,
          background: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(8px)',
          borderRadius: '12px',
          padding: '8px 12px',
          border: '1px solid rgba(255, 255, 255, 0.15)',
          color: '#fff',
          fontSize: '13px',
          letterSpacing: '0.5px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          WebkitTapHighlightColor: 'transparent'
        }}
      >
        <span>☀</span>
        <span style={{ fontWeight: 'bold' }}>{weather.temperature}°C</span>
        <span style={{ opacity: 0.5 }}>▼</span>
      </button>
    )
  }

  // Vista expandida
  return (
    <div
      onClick={() => setIsExpanded(false)}
      style={{
        position: 'fixed',
        top: 12,
        left: 12,
        zIndex: 999,
        background: 'rgba(0, 0, 0, 0.85)',
        backdropFilter: 'blur(10px)',
        borderRadius: '16px',
        padding: '16px',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        color: '#fff',
        minWidth: '200px',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        WebkitTapHighlightColor: 'transparent'
      }}
    >
      <div style={{
        fontSize: '11px',
        letterSpacing: '1.5px',
        textTransform: 'uppercase',
        opacity: 0.6,
        marginBottom: '12px',
        fontWeight: 'bold'
      }}>
        Local Sky Conditions
      </div>

      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '10px'
      }}>
        {/* Temperatura */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <span style={{ fontSize: '20px' }}>🌡</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: '11px', opacity: 0.6, letterSpacing: '0.5px' }}>Temperature</div>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{weather.temperature}°C</div>
          </div>
        </div>

        {/* Probabilidad de lluvia */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <span style={{ fontSize: '20px' }}>🌧</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: '11px', opacity: 0.6, letterSpacing: '0.5px' }}>Rain Probability</div>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{weather.rainProbability}%</div>
          </div>
        </div>

        {/* Fase lunar */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <span style={{ fontSize: '20px' }}>{weather.moonEmoji}</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: '11px', opacity: 0.6, letterSpacing: '0.5px' }}>Moon Phase</div>
            <div style={{ fontSize: '14px', fontWeight: 'bold' }}>{weather.moonPhase}</div>
          </div>
        </div>
      </div>

      <div style={{
        marginTop: '12px',
        fontSize: '9px',
        opacity: 0.4,
        textAlign: 'center',
        letterSpacing: '0.5px'
      }}>
        Tap to collapse
      </div>
    </div>
  )
}
