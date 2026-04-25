/**
 * Sistema de Premium/Licencia — preparado para validación futura
 *
 * Por ahora: siempre desbloqueado
 * Futuro: validar con servidor, código de activación, o in-app purchase
 */

// Flag interno para toggle rápido durante desarrollo
const PREMIUM_FEATURES_ENABLED = true

// Clave de localStorage (ofuscada)
const STORAGE_KEY = '_as_lic_v1'

// Hash simple para ofuscar el valor (no es seguridad real, solo ofuscación)
function simpleHash(str: string): string {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash
  }
  return Math.abs(hash).toString(36)
}

// Obtener ID único del dispositivo (fingerprint básico)
function getDeviceId(): string {
  if (typeof window === 'undefined') return 'server'
  const nav = window.navigator
  const screen = window.screen
  const raw = [
    nav.userAgent,
    nav.language,
    screen.width,
    screen.height,
    screen.colorDepth,
    new Date().getTimezoneOffset(),
  ].join('|')
  return simpleHash(raw)
}

// Token esperado para validación
function getExpectedToken(): string {
  return simpleHash(`premium_${getDeviceId()}_archeoscope`)
}

/**
 * Verificar si premium está desbloqueado
 */
export function isPremiumUnlocked(): boolean {
  if (!PREMIUM_FEATURES_ENABLED) return false
  if (typeof window === 'undefined') return false

  // Por ahora: siempre true (disponible para todos)
  // Futuro: descomentar validación
  return true

  /*
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return false
    return stored === getExpectedToken()
  } catch {
    return false
  }
  */
}

/**
 * Desbloquear premium (para uso futuro con código de activación)
 */
export function unlockPremium(activationCode?: string): boolean {
  if (typeof window === 'undefined') return false

  // Futuro: validar activationCode con servidor
  // Por ahora: simplemente guardar token

  try {
    const token = getExpectedToken()
    localStorage.setItem(STORAGE_KEY, token)
    return true
  } catch {
    return false
  }
}

/**
 * Revocar premium
 */
export function revokePremium(): void {
  if (typeof window === 'undefined') return
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {}
}

/**
 * Detectar si es mobile
 */
export function isMobileDevice(): boolean {
  if (typeof window === 'undefined') return false
  return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
}
