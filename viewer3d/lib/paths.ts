/**
 * Helper para rutas de assets
 * En desarrollo (localhost): /archivo.glb
 * En itch.io (iframe root): /archivo.glb
 * En GitHub Pages (/ArcheoScope): /ArcheoScope/archivo.glb
 */

export function getAssetPath(path: string): string {
  // Si estamos configurados explícitamente para itch.io, no agregar prefijo
  if (process.env.NEXT_PUBLIC_DEPLOY_TARGET === 'itch') {
    return path
  }

  // Si estamos en cliente y la ruta no empieza por /ArcheoScope o es localhost, no agregar prefijo
  if (typeof window !== 'undefined') {
    if (
      window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1' ||
      !window.location.pathname.startsWith('/ArcheoScope')
    ) {
      return path
    }
  }
  
  // En producción GitHub Pages, agregar prefijo /ArcheoScope
  return `/ArcheoScope${path}`
}
