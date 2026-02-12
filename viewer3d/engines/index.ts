/**
 * Engines - Sistema modular de motores
 * Arquitectura limpia y escalable
 */

export { default as GeoEngine } from './GeoEngine'
export { default as WorldEngine } from './WorldEngine'
export { default as ArcheoEngine } from './ArcheoEngine'
export { default as AvatarEngine } from './AvatarEngine'
export { default as AstroEngine } from './AstroEngine'

export type { ArchaeologicalSite } from './ArcheoEngine'
export type { Emotion, Gesture, AvatarState, ConversationContext } from './AvatarEngine'
export type { SolarPosition } from './AstroEngine'
