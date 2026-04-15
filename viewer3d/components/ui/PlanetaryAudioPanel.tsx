'use client'

import { useEffect, useState } from 'react'
import { getHarmoniaMundi } from '@/systems/HarmoniaMundiSystem'

interface PlanetInfo {
  id: string
  name: string
  frequency: number
  note: string
  orbitalPeriod: number
  droneFrequency: number
  audibleFrequency: number
  isInfrasound: boolean
}

export default function PlanetaryAudioPanel() {
  const [isOpen, setIsOpen] = useState(false)
  const [planets, setPlanets] = useState<PlanetInfo[]>([])
  const [isEnabled, setIsEnabled] = useState(false)
  const [allPlanetsActive, setAllPlanetsActive] = useState(false)

  useEffect(() => {
    const harmonia = getHarmoniaMundi()
    setIsEnabled(harmonia.isEnabled())
    
    if (harmonia.isEnabled()) {
      setPlanets(harmonia.getAllPlanetsInfo())
    }
  }, [])

  const handleEnable = async () => {
    const harmonia = getHarmoniaMundi()
    await harmonia.enable()
    setIsEnabled(true)
    setPlanets(harmonia.getAllPlanetsInfo())
  }

  const handleActivateAllPlanets = () => {
    const harmonia = getHarmoniaMundi()
    harmonia.activateAllPlanets()
    setAllPlanetsActive(true)
  }

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 right-4 z-50 bg-purple-600 hover:bg-purple-700 text-white rounded-full p-4 shadow-lg transition-all"
        title="Panel de Audio Planetario"
      >
        🪐 🎵
      </button>

      {/* Panel */}
      {isOpen && (
        <div className="fixed bottom-20 right-4 z-50 bg-black/90 backdrop-blur-md border border-purple-500/30 rounded-lg p-6 w-96 max-h-[600px] overflow-y-auto shadow-2xl">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-purple-300">
              🎼 Harmonia Mundi
            </h2>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-white"
            >
              ✕
            </button>
          </div>

          {!isEnabled ? (
            <div className="text-center py-8">
              <p className="text-gray-300 mb-4">
                Sistema de audio desactivado
              </p>
              <button
                onClick={handleEnable}
                className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg transition-colors"
              >
                🎵 Activar Audio Cósmico
              </button>
            </div>
          ) : (
            <>
              {/* Botón para activar todos los planetas */}
              <div className="mb-6">
                <button
                  onClick={handleActivateAllPlanets}
                  disabled={allPlanetsActive}
                  className={`w-full py-3 rounded-lg font-bold transition-all ${
                    allPlanetsActive
                      ? 'bg-green-600/50 text-green-200 cursor-not-allowed'
                      : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white'
                  }`}
                >
                  {allPlanetsActive ? '✅ Todos los Planetas Activos' : '🪐 Activar Todos los Planetas'}
                </button>
                {allPlanetsActive && (
                  <p className="text-xs text-green-400 mt-2 text-center">
                    Escucha la sinfonía completa del sistema solar
                  </p>
                )}
              </div>

              {/* Lista de planetas */}
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-purple-400 mb-2">
                  Frecuencias Planetarias:
                </h3>
                {planets.map((planet) => (
                  <div
                    key={planet.id}
                    className="bg-white/5 rounded-lg p-3 border border-purple-500/20"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-bold text-white">{planet.name}</h4>
                        <p className="text-xs text-gray-400">
                          Nota: {planet.note} | Órbita: {planet.orbitalPeriod.toLocaleString()} días
                        </p>
                      </div>
                      {planet.isInfrasound && (
                        <span className="text-xs bg-red-500/20 text-red-300 px-2 py-1 rounded">
                          Infrasonido
                        </span>
                      )}
                    </div>
                    
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Base:</span>
                        <span className="text-purple-300 font-mono">
                          {planet.frequency.toFixed(2)} Hz
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Drone:</span>
                        <span className="text-blue-300 font-mono">
                          {planet.droneFrequency.toFixed(2)} Hz
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Audible:</span>
                        <span className="text-green-300 font-mono">
                          {planet.audibleFrequency.toFixed(2)} Hz
                        </span>
                      </div>
                    </div>

                    {planet.isInfrasound && (
                      <p className="text-xs text-yellow-400 mt-2 italic">
                        ⚠️ Transpuesto {Math.round(Math.log2(planet.audibleFrequency / planet.droneFrequency))} octavas para audibilidad
                      </p>
                    )}
                  </div>
                ))}
              </div>

              {/* Información adicional */}
              <div className="mt-6 p-3 bg-purple-900/20 rounded-lg border border-purple-500/30">
                <p className="text-xs text-gray-300">
                  <strong className="text-purple-300">Rango audible humano:</strong> 20 Hz - 20,000 Hz
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  Las frecuencias infrasonoras (&lt;20 Hz) se transponen automáticamente al rango audible.
                </p>
              </div>
            </>
          )}
        </div>
      )}
    </>
  )
}
