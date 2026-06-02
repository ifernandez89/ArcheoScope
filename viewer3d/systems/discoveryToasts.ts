/**
 * discoveryToasts.ts
 * ─────────────────────────────────────────────────────────────────────────────
 * Mensajes de descubrimiento minimalistas, no intrusivos.
 *
 * Reglas de UX:
 * - Una sola vez por toda la vida del juego (localStorage permanente)
 * - Cooldown de 30s entre toasts para que nunca se encimen
 * - Respetan el toggle global de Ayuda (si está OFF, no aparecen)
 * - Texto en tono inmersivo, no técnico — despiertan asombro, no explican specs
 * - Auto-dismiss (el HelpBubble/toast se cierra solo)
 */

import { isHelpEnabled } from './helpSystem'

export interface DiscoveryToast {
  id: string
  icon: string
  text: string
}

// Catálogo de descubrimientos — texto inmersivo, no técnico
export const DISCOVERY_TOASTS: Record<string, DiscoveryToast> = {
  globe: {
    id: 'globe',
    icon: '🎨',
    text: 'El sistema dibuja arte único con las posiciones reales de los planetas — nunca se repite.',
  },
  site: {
    id: 'site',
    icon: '🌍',
    text: 'Cada lugar tiene una frecuencia que lo hace sentir distinto. Prestá atención.',
  },
  mission: {
    id: 'mission',
    icon: '🎵',
    text: 'Una nueva capa de la música cósmica despertó. El sonido crece con cada misión.',
  },
  constellations: {
    id: 'constellations',
    icon: '✦',
    text: 'El cielo que ves es real: cada estrella está en su posición astronómica exacta.',
  },
  night: {
    id: 'night',
    icon: '🌌',
    text: 'De noche aparecen las constelaciones reales. Buscá Orión y la Cruz del Sur.',
  },
}

const SEEN_KEY = 'archeoscope_discoveries_seen'
const COOLDOWN_MS = 30000 // 30s entre toasts

let lastShownAt = 0

function getSeen(): Set<string> {
  if (typeof window === 'undefined') return new Set()
  try {
    const raw = localStorage.getItem(SEEN_KEY)
    return raw ? new Set(JSON.parse(raw)) : new Set()
  } catch {
    return new Set()
  }
}

function markSeen(id: string): void {
  if (typeof window === 'undefined') return
  try {
    const seen = getSeen()
    seen.add(id)
    localStorage.setItem(SEEN_KEY, JSON.stringify([...seen]))
  } catch {}
}

/**
 * Intenta disparar un toast de descubrimiento.
 * Devuelve el toast si corresponde mostrarlo, o null si:
 * - la ayuda está desactivada
 * - ya se vio antes
 * - hay otro toast en cooldown
 */
export function tryTriggerDiscovery(id: keyof typeof DISCOVERY_TOASTS): DiscoveryToast | null {
  if (typeof window === 'undefined') return null
  if (!isHelpEnabled()) return null

  const toast = DISCOVERY_TOASTS[id]
  if (!toast) return null

  const seen = getSeen()
  if (seen.has(id)) return null

  const now = Date.now()
  if (now - lastShownAt < COOLDOWN_MS) return null

  lastShownAt = now
  markSeen(id)
  return toast
}

/** Resetea los descubrimientos vistos (para nueva partida / testing) */
export function resetDiscoveries(): void {
  if (typeof window === 'undefined') return
  try { localStorage.removeItem(SEEN_KEY) } catch {}
  lastShownAt = 0
}
