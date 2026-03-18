/**
 * Lazy loaders para Three.js
 * Micro-chunking: cada loader se carga solo cuando se necesita
 */

// Cache de loaders ya cargados
const loaderCache = new Map<string, any>()

export async function getGLTFLoader() {
  if (loaderCache.has('gltf')) {
    return loaderCache.get('gltf')
  }
  
  const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js')
  const loader = new GLTFLoader()
  loaderCache.set('gltf', loader)
  return loader
}

export async function getDRACOLoader() {
  if (loaderCache.has('draco')) {
    return loaderCache.get('draco')
  }
  
  const { DRACOLoader } = await import('three/examples/jsm/loaders/DRACOLoader.js')
  const loader = new DRACOLoader()
  loader.setDecoderPath('/draco/')
  loaderCache.set('draco', loader)
  return loader
}

export async function getTextureLoader() {
  if (loaderCache.has('texture')) {
    return loaderCache.get('texture')
  }
  
  const { TextureLoader } = await import('three')
  const loader = new TextureLoader()
  loaderCache.set('texture', loader)
  return loader
}

export async function getGLTFLoaderWithDraco() {
  const gltfLoader = await getGLTFLoader()
  const dracoLoader = await getDRACOLoader()
  gltfLoader.setDRACOLoader(dracoLoader)
  return gltfLoader
}

// Limpiar cache si es necesario
export function clearLoaderCache() {
  loaderCache.clear()
}
