/**
 * Tests para scene-store (Zustand)
 * Testea: Estado inicial, mutaciones, toggles
 */

import { describe, it, expect, beforeEach } from 'vitest'
import { useSceneStore } from './scene-store'

describe('SceneStore - Estado inicial', () => {
  beforeEach(() => {
    // Reset store antes de cada test
    useSceneStore.setState({
      currentModel: null,
      modelLoading: false,
      loadingProgress: 0,
      cameraMode: 'orbit',
      autoRotate: false,
      currentAnimation: 0,
      animationPlaying: false,
      timelineActive: false,
      currentTime: 0,
      showControls: true,
      showGrid: true,
      showStats: false
    })
  })

  it('debe tener valores iniciales correctos', () => {
    const state = useSceneStore.getState()
    
    expect(state.currentModel).toBe(null)
    expect(state.modelLoading).toBe(false)
    expect(state.loadingProgress).toBe(0)
    expect(state.cameraMode).toBe('orbit')
    expect(state.autoRotate).toBe(false)
    expect(state.showControls).toBe(true)
    expect(state.showGrid).toBe(true)
    expect(state.showStats).toBe(false)
  })
})

describe('SceneStore - Mutaciones de modelo', () => {
  beforeEach(() => {
    useSceneStore.setState({
      currentModel: null,
      modelLoading: false,
      loadingProgress: 0
    })
  })

  it('debe actualizar currentModel', () => {
    const { setCurrentModel } = useSceneStore.getState()
    
    setCurrentModel('machu-picchu.glb')
    expect(useSceneStore.getState().currentModel).toBe('machu-picchu.glb')
    
    setCurrentModel(null)
    expect(useSceneStore.getState().currentModel).toBe(null)
  })

  it('debe actualizar modelLoading', () => {
    const { setModelLoading } = useSceneStore.getState()
    
    setModelLoading(true)
    expect(useSceneStore.getState().modelLoading).toBe(true)
    
    setModelLoading(false)
    expect(useSceneStore.getState().modelLoading).toBe(false)
  })

  it('debe actualizar loadingProgress', () => {
    const { setLoadingProgress } = useSceneStore.getState()
    
    setLoadingProgress(0)
    expect(useSceneStore.getState().loadingProgress).toBe(0)
    
    setLoadingProgress(50)
    expect(useSceneStore.getState().loadingProgress).toBe(50)
    
    setLoadingProgress(100)
    expect(useSceneStore.getState().loadingProgress).toBe(100)
  })

  it('debe manejar secuencia de carga completa', () => {
    const { setModelLoading, setLoadingProgress, setCurrentModel } = useSceneStore.getState()
    
    // Inicio de carga
    setModelLoading(true)
    setLoadingProgress(0)
    expect(useSceneStore.getState().modelLoading).toBe(true)
    expect(useSceneStore.getState().loadingProgress).toBe(0)
    
    // Progreso
    setLoadingProgress(50)
    expect(useSceneStore.getState().loadingProgress).toBe(50)
    
    // Completado
    setLoadingProgress(100)
    setCurrentModel('model.glb')
    setModelLoading(false)
    
    const state = useSceneStore.getState()
    expect(state.modelLoading).toBe(false)
    expect(state.loadingProgress).toBe(100)
    expect(state.currentModel).toBe('model.glb')
  })
})

describe('SceneStore - Mutaciones de cámara', () => {
  beforeEach(() => {
    useSceneStore.setState({
      cameraMode: 'orbit',
      autoRotate: false
    })
  })

  it('debe cambiar cameraMode', () => {
    const { setCameraMode } = useSceneStore.getState()
    
    setCameraMode('free')
    expect(useSceneStore.getState().cameraMode).toBe('free')
    
    setCameraMode('cinematic')
    expect(useSceneStore.getState().cameraMode).toBe('cinematic')
    
    setCameraMode('orbit')
    expect(useSceneStore.getState().cameraMode).toBe('orbit')
  })

  it('debe cambiar autoRotate', () => {
    const { setAutoRotate } = useSceneStore.getState()
    
    setAutoRotate(true)
    expect(useSceneStore.getState().autoRotate).toBe(true)
    
    setAutoRotate(false)
    expect(useSceneStore.getState().autoRotate).toBe(false)
  })
})

describe('SceneStore - Mutaciones de animación', () => {
  beforeEach(() => {
    useSceneStore.setState({
      currentAnimation: 0,
      animationPlaying: false
    })
  })

  it('debe cambiar currentAnimation', () => {
    const { setCurrentAnimation } = useSceneStore.getState()
    
    setCurrentAnimation(1)
    expect(useSceneStore.getState().currentAnimation).toBe(1)
    
    setCurrentAnimation(5)
    expect(useSceneStore.getState().currentAnimation).toBe(5)
  })

  it('debe cambiar animationPlaying', () => {
    const { setAnimationPlaying } = useSceneStore.getState()
    
    setAnimationPlaying(true)
    expect(useSceneStore.getState().animationPlaying).toBe(true)
    
    setAnimationPlaying(false)
    expect(useSceneStore.getState().animationPlaying).toBe(false)
  })
})

describe('SceneStore - Mutaciones de timeline', () => {
  beforeEach(() => {
    useSceneStore.setState({
      timelineActive: false,
      currentTime: 0
    })
  })

  it('debe cambiar timelineActive', () => {
    const { setTimelineActive } = useSceneStore.getState()
    
    setTimelineActive(true)
    expect(useSceneStore.getState().timelineActive).toBe(true)
    
    setTimelineActive(false)
    expect(useSceneStore.getState().timelineActive).toBe(false)
  })

  it('debe cambiar currentTime', () => {
    const { setCurrentTime } = useSceneStore.getState()
    
    setCurrentTime(100)
    expect(useSceneStore.getState().currentTime).toBe(100)
    
    setCurrentTime(5000)
    expect(useSceneStore.getState().currentTime).toBe(5000)
  })
})

describe('SceneStore - Toggles de UI', () => {
  beforeEach(() => {
    useSceneStore.setState({
      showControls: true,
      showGrid: true,
      showStats: false
    })
  })

  it('debe hacer toggle de showControls', () => {
    const { toggleControls } = useSceneStore.getState()
    
    expect(useSceneStore.getState().showControls).toBe(true)
    
    toggleControls()
    expect(useSceneStore.getState().showControls).toBe(false)
    
    toggleControls()
    expect(useSceneStore.getState().showControls).toBe(true)
  })

  it('debe hacer toggle de showGrid', () => {
    const { toggleGrid } = useSceneStore.getState()
    
    expect(useSceneStore.getState().showGrid).toBe(true)
    
    toggleGrid()
    expect(useSceneStore.getState().showGrid).toBe(false)
    
    toggleGrid()
    expect(useSceneStore.getState().showGrid).toBe(true)
  })

  it('debe hacer toggle de showStats', () => {
    const { toggleStats } = useSceneStore.getState()
    
    expect(useSceneStore.getState().showStats).toBe(false)
    
    toggleStats()
    expect(useSceneStore.getState().showStats).toBe(true)
    
    toggleStats()
    expect(useSceneStore.getState().showStats).toBe(false)
  })

  it('debe manejar múltiples toggles independientes', () => {
    const { toggleControls, toggleGrid, toggleStats } = useSceneStore.getState()
    
    toggleControls()
    toggleGrid()
    toggleStats()
    
    const state = useSceneStore.getState()
    expect(state.showControls).toBe(false)
    expect(state.showGrid).toBe(false)
    expect(state.showStats).toBe(true)
  })
})
