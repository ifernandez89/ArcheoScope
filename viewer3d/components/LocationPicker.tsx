'use client'

import { useState } from 'react'
import type { ArchaeologicalSite } from '@/geo/coordinate-system'
import { ARCHAEOLOGICAL_SITES } from '@/data/archaeological-sites'

interface LocationPickerProps {
  onSiteSelect: (site: ArchaeologicalSite) => void
  currentSiteId: string | null
}

export default function LocationPicker({ onSiteSelect, currentSiteId }: LocationPickerProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterCulture, setFilterCulture] = useState<string>('all')

  // Filtrar sitios
  const filteredSites = ARCHAEOLOGICAL_SITES.filter(site => {
    const matchesSearch = site.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         site.culture.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCulture = filterCulture === 'all' || site.culture === filterCulture
    return matchesSearch && matchesCulture
  })

  // Obtener culturas únicas
  const cultures = ['all', ...Array.from(new Set(ARCHAEOLOGICAL_SITES.map(s => s.culture)))]

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '90px',
          left: '20px',
          width: '50px',
          height: '50px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
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
        🗺️
      </button>

      {/* Panel de ubicaciones */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '150px',
          left: '20px',
          width: '360px',
          maxHeight: '550px',
          background: 'rgba(0, 0, 0, 0.85)',
          backdropFilter: 'blur(10px)',
          borderRadius: '12px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          zIndex: 999,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden'
        }}>
          {/* Header */}
          <div style={{
            padding: '20px 20px 15px 20px',
            borderBottom: '1px solid rgba(255,255,255,0.1)'
          }}>
            <h3 style={{
              margin: '0 0 15px 0',
              color: 'white',
              fontSize: '18px',
              fontWeight: 'bold'
            }}>
              🗺️ Sitios Arqueológicos
            </h3>

            {/* Búsqueda */}
            <input
              type="text"
              placeholder="Buscar sitio..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                padding: '10px',
                marginBottom: '10px',
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '8px',
                color: 'white',
                fontSize: '14px',
                outline: 'none'
              }}
            />

            {/* Filtro de cultura */}
            <select
              value={filterCulture}
              onChange={(e) => setFilterCulture(e.target.value)}
              style={{
                width: '100%',
                padding: '8px',
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '6px',
                color: 'white',
                fontSize: '13px',
                outline: 'none'
              }}
            >
              {cultures.map(culture => (
                <option key={culture} value={culture} style={{ background: '#1a1a1a' }}>
                  {culture === 'all' ? 'Todas las culturas' : culture}
                </option>
              ))}
            </select>
          </div>

          {/* Lista de sitios */}
          <div style={{
            flex: 1,
            overflowY: 'auto',
            padding: '15px'
          }}>
            {filteredSites.length === 0 ? (
              <div style={{
                textAlign: 'center',
                color: 'rgba(255,255,255,0.5)',
                fontSize: '14px',
                padding: '20px'
              }}>
                No se encontraron sitios
              </div>
            ) : (
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '10px'
              }}>
                {filteredSites.map(site => (
                  <button
                    key={site.id}
                    onClick={() => {
                      onSiteSelect(site)
                      setIsOpen(false)
                    }}
                    style={{
                      padding: '12px',
                      background: site.id === currentSiteId 
                        ? 'rgba(67, 233, 123, 0.2)' 
                        : 'rgba(255,255,255,0.05)',
                      border: site.id === currentSiteId 
                        ? '2px solid #43e97b' 
                        : '1px solid rgba(255,255,255,0.1)',
                      borderRadius: '8px',
                      color: 'white',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.2s'
                    }}
                    onMouseEnter={(e) => {
                      if (site.id !== currentSiteId) {
                        e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
                      }
                    }}
                    onMouseLeave={(e) => {
                      if (site.id !== currentSiteId) {
                        e.currentTarget.style.background = 'rgba(255,255,255,0.05)'
                      }
                    }}
                  >
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      marginBottom: '6px'
                    }}>
                      <div style={{
                        fontSize: '15px',
                        fontWeight: 'bold'
                      }}>
                        {site.name}
                      </div>
                      {site.id === currentSiteId && (
                        <span style={{
                          fontSize: '16px',
                          color: '#43e97b'
                        }}>
                          ✓
                        </span>
                      )}
                    </div>
                    <div style={{
                      fontSize: '12px',
                      color: 'rgba(255,255,255,0.6)',
                      marginBottom: '6px'
                    }}>
                      {site.culture} • {site.period}
                    </div>
                    <div style={{
                      fontSize: '11px',
                      color: 'rgba(255,255,255,0.5)',
                      lineHeight: '1.4'
                    }}>
                      📍 {site.coordinates.latitude.toFixed(4)}°, {site.coordinates.longitude.toFixed(4)}°
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          <div style={{
            padding: '12px 20px',
            borderTop: '1px solid rgba(255,255,255,0.1)',
            fontSize: '12px',
            color: 'rgba(255,255,255,0.6)',
            textAlign: 'center'
          }}>
            {filteredSites.length} sitio{filteredSites.length !== 1 ? 's' : ''} disponible{filteredSites.length !== 1 ? 's' : ''}
          </div>
        </div>
      )}
    </>
  )
}
