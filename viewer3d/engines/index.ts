/**
 * Engines - Sistema modular de motores
 * Arquitectura limpia y escalable
 */

export { default as GeoEngine } from './GeoEngine'
export { default as WorldEngine } from './WorldEngine'
export { default as ArcheoEngine } from './ArcheoEngine'
export { default as AvatarEngine } from './AvatarEngine'
export { default as AstroEngine } from './AstroEngine'

// Astronomical-Geometric engines (new)
export { SolarEngine } from './SolarEngine'
export { SeasonalLight } from './SeasonalLight'
export { MicroMotion } from './MicroMotion'
export { SkyEngine } from './SkyEngine'
export { GeometryField } from './GeometryField'
export { AtmosphericSound } from './AtmosphericSound'

export type { ArchaeologicalSite } from './ArcheoEngine'
export type { Emotion, Gesture, AvatarState, ConversationContext } from './AvatarEngine'
export type { SolarPosition } from './AstroEngine'

// New types
export type { SolarState } from './SolarEngine'
export type { SeasonalState } from './SeasonalLight'
export type { MotionState } from './MicroMotion'
export type { SkyState } from './SkyEngine'
export type { SoundState } from './AtmosphericSound'

