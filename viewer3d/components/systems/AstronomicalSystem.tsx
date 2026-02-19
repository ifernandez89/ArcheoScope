'use client'

/**
 * AstronomicalSystem - Sistema astronómico modular
 * Se carga solo cuando se necesita el sistema astronómico
 */

import AstronomicalWorld from '../AstronomicalWorld'
import SolarTrajectory from '../SolarTrajectory'

interface AstronomicalSystemProps {
  location?: { lat: number; lon: number } | null
  enabled: boolean
  showGeometry: boolean
  onDayNightChange: (isDay: boolean) => void
  onSolarUpdate: (
    direction: { x: number; y: number; z: number },
    altitude: number,
    azimuth: number,
    declination: number
  ) => void
  solarState: { altitude: number; azimuth: number; declination: number }
  isDay: boolean
  showTrajectory?: boolean
}

export default function AstronomicalSystem({
  location,
  enabled,
  showGeometry,
  onDayNightChange,
  onSolarUpdate,
  solarState,
  isDay,
  showTrajectory = true
}: AstronomicalSystemProps) {
  return (
    <>
      {/* Sistema astronómico-geométrico vivo */}
      <AstronomicalWorld
        location={location}
        enabled={enabled}
        showGeometry={showGeometry}
        onDayNightChange={onDayNightChange}
        onSolarUpdate={onSolarUpdate}
      />

      {/* Trayectoria solar del día */}
      {showTrajectory && (
        <SolarTrajectory
          solarAltitude={solarState.altitude}
          solarAzimuth={solarState.azimuth}
          declination={solarState.declination}
          latitude={(location?.lat || 0) * Math.PI / 180}
          isDay={isDay}
          visible={true}
        />
      )}
    </>
  )
}
