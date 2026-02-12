// Global State Management with Zustand
import { create } from 'zustand'
import type { CameraMode } from '@/core/types'

interface SceneState {
  // Model state
  currentModel: string | null
  modelLoading: boolean
  loadingProgress: number
  
  // Camera state
  cameraMode: CameraMode['type']
  autoRotate: boolean
  
  // Animation state
  currentAnimation: number
  animationPlaying: boolean
  
  // Timeline state
  timelineActive: boolean
  currentTime: number
  
  // UI state
  showControls: boolean
  showGrid: boolean
  showStats: boolean
  
  // Actions
  setCurrentModel: (model: string | null) => void
  setModelLoading: (loading: boolean) => void
  setLoadingProgress: (progress: number) => void
  setCameraMode: (mode: CameraMode['type']) => void
  setAutoRotate: (rotate: boolean) => void
  setCurrentAnimation: (index: number) => void
  setAnimationPlaying: (playing: boolean) => void
  setTimelineActive: (active: boolean) => void
  setCurrentTime: (time: number) => void
  toggleControls: () => void
  toggleGrid: () => void
  toggleStats: () => void
}

export const useSceneStore = create<SceneState>((set) => ({
  // Initial state
  currentModel: null,
  modelLoading: false,
  loadingProgress: 0,
  cameraMode: 'orbital',
  autoRotate: false,  // Desactivado por defecto - el modelo se mantiene vertical
  currentAnimation: 0,
  animationPlaying: false,
  timelineActive: false,
  currentTime: 0,
  showControls: true,
  showGrid: true,
  showStats: false,
  
  // Actions
  setCurrentModel: (model) => set({ currentModel: model }),
  setModelLoading: (loading) => set({ modelLoading: loading }),
  setLoadingProgress: (progress) => set({ loadingProgress: progress }),
  setCameraMode: (mode) => set({ cameraMode: mode }),
  setAutoRotate: (rotate) => set({ autoRotate: rotate }),
  setCurrentAnimation: (index) => set({ currentAnimation: index }),
  setAnimationPlaying: (playing) => set({ animationPlaying: playing }),
  setTimelineActive: (active) => set({ timelineActive: active }),
  setCurrentTime: (time) => set({ currentTime: time }),
  toggleControls: () => set((state) => ({ showControls: !state.showControls })),
  toggleGrid: () => set((state) => ({ showGrid: !state.showGrid })),
  toggleStats: () => set((state) => ({ showStats: !state.showStats }))
}))
