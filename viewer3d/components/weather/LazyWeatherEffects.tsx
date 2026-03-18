/**
 * Lazy loading de efectos de clima
 * Solo se cargan cuando se activan
 */

import dynamic from 'next/dynamic'

// Lazy load de cada efecto
export const LightningEffect = dynamic(() => import('./LightningEffect'), { ssr: false })
export const TornadoEffect = dynamic(() => import('./TornadoEffect'), { ssr: false })
export const EarthquakeEffect = dynamic(() => import('./EarthquakeEffect'), { ssr: false })
export const WindEffect = dynamic(() => import('./WindEffect'), { ssr: false })
export const DynamicFog = dynamic(() => import('./DynamicFog'), { ssr: false })
export const CloudSky = dynamic(() => import('./CloudSky'), { ssr: false })
export const RealisticWind = dynamic(() => import('./RealisticWind'), { ssr: false })
export const RealisticFog = dynamic(() => import('./RealisticFog'), { ssr: false })
export const ProceduralLightning = dynamic(() => import('./ProceduralLightning'), { ssr: false })
export const VisibleSun = dynamic(() => import('./VisibleSun'), { ssr: false })
export const VisibleMoon = dynamic(() => import('./VisibleMoon'), { ssr: false })
