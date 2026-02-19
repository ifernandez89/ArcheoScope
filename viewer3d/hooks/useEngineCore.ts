/**
 * useEngineCore - Hook para integrar EngineCore con React
 * NO causa re-renders innecesarios
 */

import { useEffect, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import EngineCore from '@/engines/EngineCore'

/**
 * Hook principal - Conecta EngineCore con R3F
 * Usar UNA SOLA VEZ en el componente raíz de la escena
 */
export function useEngineCore() {
  const { gl } = useThree()
  const startedRef = useRef(false)

  useEffect(() => {
    if (startedRef.current) return
    
    // Configurar renderer
    EngineCore.setRenderer(gl)
    
    // Iniciar motor
    EngineCore.start()
    
    startedRef.current = true

    return () => {
      EngineCore.stop()
      startedRef.current = false
    }
  }, [gl])

  // Tick principal - ÚNICO useFrame en toda la app
  useFrame((state, delta) => {
    EngineCore.tick(state.clock.elapsedTime, delta)
  })
}

/**
 * Hook para registrar callback de update
 * NO causa re-renders
 */
export function useEngineUpdate(callback: (delta: number) => void, deps: any[] = []) {
  useEffect(() => {
    const unsubscribe = EngineCore.onUpdate(callback)
    return unsubscribe
  }, deps)
}

/**
 * Hook para registrar callback de render
 * NO causa re-renders
 */
export function useEngineRender(callback: () => void, deps: any[] = []) {
  useEffect(() => {
    const unsubscribe = EngineCore.onRender(callback)
    return unsubscribe
  }, deps)
}

/**
 * Hook para registrar sistema
 */
export function useEngineSystem(
  name: string,
  update: (delta: number) => void,
  enabled: boolean = true
) {
  useEffect(() => {
    const system = {
      update,
      enabled
    }
    
    EngineCore.registerSystem(name, system)

    return () => {
      EngineCore.unregisterSystem(name)
    }
  }, [name, update, enabled])
}

/**
 * Ejemplo de uso:
 * 
 * // En el componente raíz de la escena (UNA SOLA VEZ)
 * function Scene() {
 *   useEngineCore()
 *   
 *   return <group>...</group>
 * }
 * 
 * // En componentes que necesitan update (NO causa re-renders)
 * function MyComponent() {
 *   const positionRef = useRef(new THREE.Vector3())
 *   
 *   useEngineUpdate((delta) => {
 *     // Lógica que corre cada frame
 *     // NO dispara re-renders
 *     positionRef.current.x += delta
 *   }, [])
 *   
 *   return <mesh position={positionRef.current} />
 * }
 * 
 * // Para sistemas complejos
 * function PhysicsSystem() {
 *   useEngineSystem('physics', (delta) => {
 *     // Actualizar física
 *   }, true)
 *   
 *   return null
 * }
 */
