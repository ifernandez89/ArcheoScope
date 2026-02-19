/**
 * EngineIntegration - Integración de todos los sistemas de performance
 * Se usa UNA SOLA VEZ en cada Canvas
 */

'use client'

import { useEffect } from 'react'
import { useEngineCore, useEngineSystem } from '@/hooks/useEngineCore'
import { useCullingCamera } from '@/hooks/useCulling'
import CullingSystem from '@/systems/CullingSystem'
import InstanceManager from '@/systems/InstanceManager'
import GraphicsPresetManager from '@/systems/GraphicsPresets'

export default function EngineIntegration() {
  // 🎮 Inicializar EngineCore (ÚNICO useFrame en toda la app)
  useEngineCore()
  
  // ✂️ Configurar cámara para culling
  useCullingCamera()
  
  // 🔧 Integrar CullingSystem
  useEngineSystem('culling', (delta) => {
    CullingSystem.update(delta)
  }, true)
  
  // 🎨 Integrar InstanceManager
  useEngineSystem('instancing', () => {
    InstanceManager.update()
  }, true)
  
  // 📊 Log de inicialización
  useEffect(() => {
    console.log('🎮 EngineCore: Sistemas integrados')
    console.log('  ✂️ CullingSystem: Activo')
    console.log('  🎨 InstanceManager: Activo')
    console.log('  🎨 Graphics Preset:', GraphicsPresetManager.getPreset())
    
    // Configurar culling
    CullingSystem.configure({
      enableFrustumCulling: true,
      enableDistanceCulling: true,
      enableDisposal: true,
      maxRenderDistance: 2000,
      disposalDistance: 2500
    })
  }, [])
  
  return null
}
