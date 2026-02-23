'use client'

/**
 * EnvironmentSystem - Sistema de entorno modular
 * Se carga solo cuando se necesitan elementos del entorno
 */

import DynamicSky from '../DynamicSky'
import VolumetricFog from '../VolumetricFog'
import RealisticWater from '../RealisticWater'

interface EnvironmentSystemProps {
  isDay: boolean
  skyColor: string
  fogColor: string
  stormDarkness: number
  fogDensity: number
  showWater: boolean
  waterPosition?: [number, number, number]
  waterSize?: number
  waterColor?: string
}

export default function EnvironmentSystem({
  isDay,
  skyColor,
  fogColor,
  stormDarkness,
  fogDensity,
  showWater,
  waterPosition = [0, -0.5, 0],
  waterSize = 150,
  waterColor = '#1e3a5f'
}: EnvironmentSystemProps) {
  console.log('EnvironmentSystem - showWater:', showWater)
  
  return (
    <>
      {/* Cielo dinámico */}
      <DynamicSky 
        isDay={isDay} 
        skyColor={skyColor} 
        stormDarkness={stormDarkness} 
      />

      {/* Niebla volumétrica */}
      <VolumetricFog
        color={fogColor}
        density={fogDensity}
      />

      {/* Agua realista con Fresnel, Reflection y Refraction */}
      {showWater && (
        <RealisticWater
          position={waterPosition}
          size={waterSize}
          color={waterColor}
        />
      )}
    </>
  )
}
