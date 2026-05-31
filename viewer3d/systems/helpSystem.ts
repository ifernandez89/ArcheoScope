/**
 * helpSystem.ts
 * Sistema de ayuda contextual — toggle global en gameSettings
 */

const HELP_KEY = 'archeoscope_help_enabled'

export function isHelpEnabled(): boolean {
  if (typeof window === 'undefined') return true
  const val = localStorage.getItem(HELP_KEY)
  return val === null ? true : val === 'true' // default: ON
}

export function setHelpEnabled(enabled: boolean): void {
  if (typeof window === 'undefined') return
  localStorage.setItem(HELP_KEY, String(enabled))
  // Notificar a listeners
  window.dispatchEvent(new CustomEvent('help-toggle', { detail: { enabled } }))
}

export function toggleHelp(): boolean {
  const next = !isHelpEnabled()
  setHelpEnabled(next)
  return next
}
