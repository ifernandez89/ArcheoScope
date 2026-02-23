/**
 * Helper para rutas de assets
 * En desarrollo: /archivo.glb
 * En producción (GitHub Pages): /ArcheoScope/archivo.glb
 */

export function getAssetPath(path: string): string {
  // Si estamos en desarrollo (localhost), no agregar prefijo
  if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
    return path
  }
  
  // En producción (GitHub Pages), agregar prefijo /ArcheoScope
  return `/ArcheoScope${path}`
}
