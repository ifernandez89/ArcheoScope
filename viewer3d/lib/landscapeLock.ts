/**
 * Landscape Lock — Forzar orientación horizontal en mobile
 * 
 * Usa la Screen Orientation API cuando está disponible.
 * Fallback: muestra overlay pidiendo rotar el dispositivo.
 */

/**
 * Intentar bloquear la pantalla en modo landscape
 * @returns true si se logró bloquear, false si no está soportado
 */
export async function lockLandscape(): Promise<boolean> {
  if (typeof window === 'undefined') return false
  
  try {
    // Screen Orientation API (Chrome Android, algunos navegadores)
    const orientation = screen.orientation as ScreenOrientation & { lock?: (orientation: string) => Promise<void> }
    if (orientation && typeof orientation.lock === 'function') {
      await orientation.lock('landscape')
      console.log('📱 Orientación bloqueada en landscape')
      return true
    }
  } catch (err) {
    console.warn('📱 No se pudo bloquear orientación:', err)
  }
  
  return false
}

/**
 * Desbloquear la orientación de pantalla
 */
export function unlockOrientation(): void {
  if (typeof window === 'undefined') return
  
  try {
    if (screen.orientation && 'unlock' in screen.orientation) {
      screen.orientation.unlock()
      console.log('📱 Orientación desbloqueada')
    }
  } catch (err) {
    // Ignorar errores
  }
}

/**
 * Detectar si estamos en modo portrait (vertical)
 */
export function isPortrait(): boolean {
  if (typeof window === 'undefined') return false
  return window.innerHeight > window.innerWidth
}

/**
 * Detectar si es un dispositivo móvil
 */
export function isMobileDevice(): boolean {
  if (typeof window === 'undefined') return false
  return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
}

/**
 * Entrar en fullscreen (ayuda a que el lock funcione mejor)
 */
export async function enterFullscreen(): Promise<boolean> {
  if (typeof document === 'undefined') return false
  
  try {
    const elem = document.documentElement as HTMLElement & { webkitRequestFullscreen?: () => Promise<void> }
    if (elem.requestFullscreen) {
      await elem.requestFullscreen()
      return true
    }
    // Safari
    if (elem.webkitRequestFullscreen) {
      await elem.webkitRequestFullscreen()
      return true
    }
  } catch (err) {
    console.warn('📱 No se pudo entrar en fullscreen:', err)
  }
  
  return false
}

/**
 * Salir de fullscreen
 */
export function exitFullscreen(): void {
  if (typeof document === 'undefined') return
  
  try {
    const doc = document as Document & { webkitExitFullscreen?: () => void }
    if (doc.exitFullscreen) {
      doc.exitFullscreen()
    } else if (doc.webkitExitFullscreen) {
      doc.webkitExitFullscreen()
    }
  } catch (err) {
    // Ignorar
  }
}
