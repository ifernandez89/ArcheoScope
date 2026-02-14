'use client'

import { useState, useEffect } from 'react'
import { detectBiome, type BiomeInfo } from '@/utils/biome-detector'

interface LocationInfoProps {
  location: { lat: number, lon: number } | null
  site?: { name: string, culture: string, period: string } | null
}

export default function LocationInfo({ location, site }: LocationInfoProps) {
  const [info, setInfo] = useState<{
    region: string
    climate: string
    terrain: string
    archaeology: string
    biome?: BiomeInfo
  } | null>(null)

  useEffect(() => {
    if (!location) {
      setInfo(null)
      return
    }

    // Detectar bioma
    const biome = detectBiome(location.lat, location.lon)
    
    // Determinar información contextual basada en coordenadas
    const { lat, lon } = location
    
    let region = 'Región desconocida'
    let climate = 'Clima templado'
    let terrain = 'Terreno variado'
    let archaeology = 'Zona de interés arqueológico'

    // Determinar región
    if (lat >= -30 && lat <= -25 && lon >= -110 && lon <= -109) {
      region = 'Isla de Pascua (Rapa Nui)'
      climate = 'Subtropical oceánico'
      terrain = 'Volcánico con praderas'
      archaeology = 'Moais, Ahu, Petroglifos'
    } else if (lat >= -14 && lat <= -13 && lon >= -73 && lon <= -72) {
      region = 'Machu Picchu, Perú'
      climate = 'Tropical de montaña'
      terrain = 'Montañoso andino'
      archaeology = 'Ciudadela Inca, terrazas agrícolas'
    } else if (lat >= 29 && lat <= 30 && lon >= 31 && lon <= 32) {
      region = 'Pirámides de Giza, Egipto'
      climate = 'Desértico cálido'
      terrain = 'Meseta desértica'
      archaeology = 'Pirámides, Esfinge, templos'
    } else if (lat >= 51 && lat <= 52 && lon >= -2 && lon <= -1) {
      region = 'Stonehenge, Inglaterra'
      climate = 'Oceánico templado'
      terrain = 'Llanura de Salisbury'
      archaeology = 'Círculo megalítico neolítico'
    } else if (lat >= 13 && lat <= 14 && lon >= 103 && lon <= 104) {
      region = 'Angkor Wat, Camboya'
      climate = 'Tropical monzónico'
      terrain = 'Llanura aluvial'
      archaeology = 'Templos jemer, ciudad antigua'
    } else if (lat >= 30 && lat <= 31 && lon >= 35 && lon <= 36) {
      region = 'Petra, Jordania'
      climate = 'Desértico árido'
      terrain = 'Cañones de arenisca'
      archaeology = 'Ciudad nabatea tallada en roca'
    } else {
      // Determinar por latitud general
      if (Math.abs(lat) < 23.5) {
        region = 'Zona tropical'
        climate = 'Tropical'
      } else if (Math.abs(lat) < 66.5) {
        region = 'Zona templada'
        climate = 'Templado'
      } else {
        region = 'Zona polar'
        climate = 'Polar'
      }

      // Determinar terreno por contexto
      if (Math.abs(lat) < 10) {
        terrain = 'Selva tropical o sabana'
      } else if (Math.abs(lat) > 60) {
        terrain = 'Tundra o glacial'
      }
    }

    setInfo({ region, climate, terrain, archaeology, biome })
  }, [location])

  if (!location || !info) return null

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      left: '20px',
      zIndex: 1000,
      background: 'rgba(0, 0, 0, 0.9)',
      backdropFilter: 'blur(10px)',
      borderRadius: '12px',
      padding: '20px',
      maxWidth: '350px',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      border: '1px solid rgba(255,255,255,0.1)'
    }}>
      <h3 style={{
        margin: '0 0 15px 0',
        color: '#fbbf24',
        fontSize: '16px',
        fontWeight: 'bold',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}>
        📍 Información de Ubicación
      </h3>

      {site && (
        <div style={{
          padding: '12px',
          background: 'rgba(251, 191, 36, 0.1)',
          borderRadius: '8px',
          marginBottom: '15px',
          border: '1px solid rgba(251, 191, 36, 0.3)'
        }}>
          <div style={{ color: '#fbbf24', fontWeight: 'bold', marginBottom: '5px' }}>
            🏛️ {site.name}
          </div>
          <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: '12px' }}>
            {site.culture} • {site.period}
          </div>
        </div>
      )}

      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        color: 'white',
        fontSize: '13px'
      }}>
        <div>
          <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px', marginBottom: '4px' }}>
            Coordenadas
          </div>
          <div style={{ fontFamily: 'monospace', color: '#4a90e2' }}>
            {location.lat.toFixed(4)}°, {location.lon.toFixed(4)}°
          </div>
        </div>

        <div>
          <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px', marginBottom: '4px' }}>
            🌍 Región
          </div>
          <div>{info.region}</div>
        </div>

        <div>
          <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px', marginBottom: '4px' }}>
            🌡️ Clima
          </div>
          <div>{info.climate}</div>
        </div>

        <div>
          <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px', marginBottom: '4px' }}>
            ⛰️ Terreno
          </div>
          <div>{info.terrain}</div>
        </div>

        <div>
          <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px', marginBottom: '4px' }}>
            🏺 Arqueología
          </div>
          <div>{info.archaeology}</div>
        </div>

        {info.biome && (
          <div style={{
            marginTop: '8px',
            padding: '12px',
            background: info.biome.type === 'ice' 
              ? 'rgba(184, 212, 232, 0.15)' 
              : 'rgba(139, 92, 46, 0.15)',
            borderRadius: '8px',
            border: info.biome.type === 'ice'
              ? '1px solid rgba(184, 212, 232, 0.3)'
              : '1px solid rgba(139, 92, 46, 0.3)'
          }}>
            <div style={{ 
              color: info.biome.type === 'ice' ? '#b8d4e8' : '#fbbf24', 
              fontWeight: 'bold', 
              marginBottom: '8px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              {info.biome.type === 'ice' ? '❄️' : '🌋'} Bioma: {info.biome.name}
            </div>
            <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.7)', marginBottom: '6px' }}>
              {info.biome.description}
            </div>
            <div style={{ 
              display: 'flex', 
              gap: '12px', 
              fontSize: '11px',
              color: 'rgba(255,255,255,0.6)'
            }}>
              <span>🌡️ {info.biome.temperature}°C</span>
              <span>💧 {info.biome.humidity}%</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
