/**
 * Layers - Exportación centralizada de todas las capas
 * 
 * Nueva arquitectura por responsabilidad funcional:
 * - CoreEngine: Motor mínimo (siempre cargado)
 * - EnvironmentLayer: Terreno, agua, vegetación (lazy)
 * - EffectsLayer: Post-processing, bloom, partículas (lazy fuerte)
 * - InteractionLayer: Raycasting, input (semi-lazy)
 * - UISystems: Controles UI (siempre cargado)
 * - OptionalSystems: Clima, audio (lazy + condicional)
 */

// Nueva arquitectura
export { default as CoreEngine } from './CoreEngine'
export { default as EnvironmentLayer } from './EnvironmentLayer'
export { default as EffectsLayer } from './EffectsLayer'
export { default as InteractionLayer } from './InteractionLayer'
export { default as UISystems } from './UISystems'
export { default as OptionalSystems } from './OptionalSystems'
