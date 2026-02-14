import { useState, useEffect } from 'react'
import * as THREE from 'three'

/**
 * Hook para cargar texturas de forma segura
 * Retorna null si la textura no se puede cargar
 */
export function useTexture(path: string): THREE.Texture | null {
  const [texture, setTexture] = useState<THREE.Texture | null>(null)
  
  useEffect(() => {
    const loader = new THREE.TextureLoader()
    
    loader.load(
      path,
      (loadedTexture) => {
        setTexture(loadedTexture)
      },
      undefined,
      (error) => {
        console.warn(`No se pudo cargar textura: ${path}`)
        setTexture(null)
      }
    )
  }, [path])
  
  return texture
}
