'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'

interface WeatherData {
  temp: number
  feelsLike: number
  humidity: number
  windSpeed: number
  rainProbability: number
  weatherCode: number
  city: string
  country: string
  moonPhase: string
  moonEmoji: string
  lat: number
  lon: number
}

// ─── Fase lunar (algoritmo preciso) ──────────────────────────────────────────
function getMoonPhase(): { phase: string; emoji: string; illumination: number } {
  const now = new Date()
  const lp = 2551443 // segundos del ciclo lunar
  const newMoon = new Date('1970-01-07T20:35:00Z')
  const phase = ((now.getTime() - newMoon.getTime()) / 1000) % lp
  const idx = Math.floor((phase / lp) * 8)
  const pct = Math.round((phase / lp) * 100)
  const phases = [
    { name: 'Luna Nueva',         emoji: '🌑', illum: 0 },
    { name: 'Creciente',          emoji: '🌒', illum: 25 },
    { name: 'Cuarto Creciente',   emoji: '🌓', illum: 50 },
    { name: 'Gibosa Creciente',   emoji: '🌔', illum: 75 },
    { name: 'Luna Llena',         emoji: '🌕', illum: 100 },
    { name: 'Gibosa Menguante',   emoji: '🌖', illum: 75 },
    { name: 'Cuarto Menguante',   emoji: '🌗', illum: 50 },
    { name: 'Menguante',          emoji: '🌘', illum: 25 },
  ]
  return { phase: phases[idx].name, emoji: phases[idx].emoji, illumination: phases[idx].illum }
}

// ─── WMO Weather Code helpers ─────────────────────────────────────────────────
function getWeatherDesc(code: number): string {
  if (code === 0) return 'Despejado'
  if (code <= 2) return 'Parcialmente nublado'
  if (code === 3) return 'Nublado'
  if (code <= 49) return 'Niebla'
  if (code <= 59) return 'Llovizna'
  if (code <= 69) return 'Lluvia'
  if (code <= 79) return 'Nieve'
  if (code <= 82) return 'Chubascos'
  if (code <= 86) return 'Nieve intensa'
  if (code <= 99) return 'Tormenta'
  return 'Variable'
}

function getWeatherIcon(code: number): string {
  if (code === 0) return '☀️'
  if (code <= 2) return '⛅'
  if (code === 3) return '☁️'
  if (code <= 49) return '🌫️'
  if (code <= 59) return '🌦️'
  if (code <= 69) return '🌧️'
  if (code <= 79) return '❄️'
  if (code <= 82) return '🌦️'
  if (code <= 86) return '🌨️'
  if (code <= 99) return '⛈️'
  return '🌡️'
}

function getRainColor(pct: number): string {
  if (pct < 20) return '#34d399'
  if (pct < 50) return '#fbbf24'
  if (pct < 75) return '#f97316'
  return '#ef4444'
}

const CACHE_KEY = 'archeoscope_weather_full'
const CACHE_DURATION = 30 * 60 * 1000 // 30 min

export default function WeatherPage() {
  const router = useRouter()
  const [weather, setWeather] = useState<WeatherData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Try cache first
    try {
      const cached = localStorage.getItem(CACHE_KEY)
      if (cached) {
        const { data, ts } = JSON.parse(cached)
        if (Date.now() - ts < CACHE_DURATION) {
          setWeather(data)
          setLoading(false)
          return
        }
      }
    } catch {}

    if (!navigator.geolocation) {
      setError('Geolocalización no disponible.')
      setLoading(false)
      return
    }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude: lat, longitude: lon } = pos.coords
        try {
          // Open-Meteo — gratis, sin API key
          const res = await fetch(
            `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}` +
            `&current=temperature_2m,relative_humidity_2m,apparent_temperature,` +
            `wind_speed_10m,weather_code,precipitation_probability` +
            `&wind_speed_unit=kmh&timezone=auto`
          )
          const d = await res.json()
          const c = d.current
          const moon = getMoonPhase()

          let city = `${lat.toFixed(2)}°, ${lon.toFixed(2)}°`
          let country = ''
          try {
            const geo = await fetch(
              `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`
            )
            const gd = await geo.json()
            city = gd.address?.city || gd.address?.town || gd.address?.village || gd.address?.county || city
            country = gd.address?.country || ''
          } catch {}

          const data: WeatherData = {
            temp: Math.round(c.temperature_2m),
            feelsLike: Math.round(c.apparent_temperature),
            humidity: c.relative_humidity_2m,
            windSpeed: Math.round(c.wind_speed_10m),
            rainProbability: c.precipitation_probability || 0,
            weatherCode: c.weather_code,
            city, country,
            moonPhase: moon.phase,
            moonEmoji: moon.emoji,
            lat, lon,
          }
          localStorage.setItem(CACHE_KEY, JSON.stringify({ data, ts: Date.now() }))
          setWeather(data)
        } catch {
          setError('No se pudo obtener el clima.')
        }
        setLoading(false)
      },
      () => { setError('Permiso de ubicación denegado.'); setLoading(false) },
      { timeout: 10000 }
    )
  }, [])

  const moon = getMoonPhase()

  return (
    <main style={{
      width: '100vw', minHeight: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'flex-start',
      background: 'linear-gradient(160deg, #050510 0%, #0a0f2e 40%, #0a1a1a 100%)',
      color: '#fff', padding: '28px 16px 32px', boxSizing: 'border-box',
      overflowY: 'auto'
    }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '28px' }}>
        <h1 style={{ fontSize: '22px', letterSpacing: '5px', margin: 0, fontFamily: 'Archeoscope, serif', color: '#a5f3fc' }}>
          CLIMA LOCAL
        </h1>
        <p style={{ fontSize: '11px', color: 'rgba(255,255,255,0.3)', letterSpacing: '2px', margin: '6px 0 0' }}>
          CONDICIONES ATMOSFÉRICAS EN TIEMPO REAL
        </p>
      </div>

      {/* Loading */}
      {loading && (
        <div style={{ textAlign: 'center', color: '#888', marginTop: '60px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px', animation: 'spin 2s linear infinite' }}>🌍</div>
          <p style={{ letterSpacing: '2px', fontSize: '13px' }}>Obteniendo ubicación...</p>
          <style>{`@keyframes spin { from { transform: rotate(0deg) } to { transform: rotate(360deg) } }`}</style>
        </div>
      )}

      {/* Error */}
      {error && !loading && (
        <div style={{
          background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)',
          borderRadius: '16px', padding: '24px', textAlign: 'center', maxWidth: '320px', marginTop: '40px'
        }}>
          <div style={{ fontSize: '36px', marginBottom: '10px' }}>⚠️</div>
          <p style={{ color: '#fca5a5', margin: 0, fontSize: '14px' }}>{error}</p>
        </div>
      )}

      {/* Weather data */}
      {weather && !loading && (
        <div style={{ width: '100%', maxWidth: '380px', display: 'flex', flexDirection: 'column', gap: '14px' }}>

          {/* Location */}
          <div style={{ textAlign: 'center', marginBottom: '4px' }}>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#a5f3fc' }}>{weather.city}</div>
            {weather.country && <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.4)', marginTop: '2px' }}>{weather.country}</div>}
            <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.2)', marginTop: '4px' }}>
              {weather.lat.toFixed(4)}°, {weather.lon.toFixed(4)}°
            </div>
          </div>

          {/* Main card */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(14,165,233,0.12), rgba(6,182,212,0.06))',
            border: '1px solid rgba(14,165,233,0.25)',
            borderRadius: '20px', padding: '28px 20px', textAlign: 'center',
            boxShadow: '0 0 40px rgba(14,165,233,0.08)'
          }}>
            <div style={{ fontSize: '64px', lineHeight: 1, marginBottom: '8px' }}>
              {getWeatherIcon(weather.weatherCode)}
            </div>
            <div style={{ fontSize: '64px', fontWeight: '200', letterSpacing: '-2px', lineHeight: 1 }}>
              {weather.temp}°
            </div>
            <div style={{ fontSize: '16px', color: 'rgba(255,255,255,0.6)', marginTop: '6px', letterSpacing: '1px' }}>
              {getWeatherDesc(weather.weatherCode)}
            </div>
            <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.35)', marginTop: '4px' }}>
              Sensación {weather.feelsLike}°C
            </div>
          </div>

          {/* Stats grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
            {[
              { icon: '💧', label: 'Humedad', value: `${weather.humidity}%`, color: '#38bdf8' },
              { icon: '💨', label: 'Viento', value: `${weather.windSpeed} km/h`, color: '#a78bfa' },
              { icon: '🌧️', label: 'Lluvia', value: `${weather.rainProbability}%`, color: getRainColor(weather.rainProbability) },
              { icon: weather.moonEmoji, label: 'Fase Lunar', value: weather.moonPhase, color: '#fde68a' },
            ].map(({ icon, label, value, color }) => (
              <div key={label} style={{
                background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.07)',
                borderRadius: '14px', padding: '16px 12px', textAlign: 'center'
              }}>
                <div style={{ fontSize: '24px', marginBottom: '6px' }}>{icon}</div>
                <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '4px', textTransform: 'uppercase' }}>{label}</div>
                <div style={{ fontSize: '15px', fontWeight: 'bold', color }}>{value}</div>
              </div>
            ))}
          </div>

          {/* Rain probability bar */}
          <div style={{
            background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.07)',
            borderRadius: '14px', padding: '16px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px', fontSize: '12px' }}>
              <span style={{ color: 'rgba(255,255,255,0.5)', letterSpacing: '1px' }}>PROBABILIDAD DE LLUVIA</span>
              <span style={{ color: getRainColor(weather.rainProbability), fontWeight: 'bold' }}>{weather.rainProbability}%</span>
            </div>
            <div style={{ height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '3px', overflow: 'hidden' }}>
              <div style={{
                height: '100%', width: `${weather.rainProbability}%`,
                background: `linear-gradient(90deg, #34d399, ${getRainColor(weather.rainProbability)})`,
                borderRadius: '3px', transition: 'width 1s ease'
              }} />
            </div>
          </div>

          {/* Moon card */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(253,230,138,0.08), rgba(251,191,36,0.04))',
            border: '1px solid rgba(253,230,138,0.15)',
            borderRadius: '14px', padding: '16px',
            display: 'flex', alignItems: 'center', gap: '16px'
          }}>
            <div style={{ fontSize: '40px' }}>{weather.moonEmoji}</div>
            <div>
              <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.4)', letterSpacing: '1px', marginBottom: '4px' }}>FASE LUNAR HOY</div>
              <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#fde68a' }}>{weather.moonPhase}</div>
              <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.3)', marginTop: '2px' }}>
                Ciclo lunar: ~29.5 días
              </div>
            </div>
          </div>

          <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.2)', textAlign: 'center', letterSpacing: '1px' }}>
            Open-Meteo · OpenStreetMap · Cache 30 min
          </div>
        </div>
      )}

      {/* Back button */}
      <button
        onClick={() => router.push('/menu')}
        style={{
          marginTop: '28px', padding: '14px 48px', fontSize: '15px',
          fontWeight: 'bold', color: '#fff', background: 'transparent',
          border: '2px solid rgba(255,255,255,0.3)', borderRadius: '10px',
          cursor: 'pointer', letterSpacing: '3px', textTransform: 'uppercase',
          transition: 'all 0.2s'
        }}
        onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#fff'; e.currentTarget.style.background = 'rgba(255,255,255,0.05)' }}
        onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)'; e.currentTarget.style.background = 'transparent' }}
      >
        Volver
      </button>
    </main>
  )
}
