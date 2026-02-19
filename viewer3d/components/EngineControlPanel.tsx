'use client'

import { useState } from 'react'
import { useSceneStore } from '@/store/scene-store'

type PanelSection = 'camera' | 'render' | 'postprocessing' | 'world' | 'debug' | 'performance'

export default function EngineControlPanel() {
  const [isOpen, setIsOpen] = useState(false)
  const [activeSection, setActiveSection] = useState<PanelSection>('camera')

  // Scene store
  const autoRotate = useSceneStore((state) => state.autoRotate)
  const setAutoRotate = useSceneStore((state) => state.setAutoRotate)
  const showGrid = useSceneStore((state) => state.showGrid)
  const toggleGrid = useSceneStore((state) => state.toggleGrid)
  const cameraMode = useSceneStore((state) => state.cameraMode)

  const sections: { id: PanelSection; label: string; icon: string }[] = [
    { id: 'camera', label: 'Camera', icon: '📷' },
    { id: 'render', label: 'Render', icon: '🎨' },
    { id: 'postprocessing', label: 'Post-FX', icon: '✨' },
    { id: 'world', label: 'World', icon: '🌍' },
    { id: 'debug', label: 'Debug', icon: '🔧' },
    { id: 'performance', label: 'Perf', icon: '⚡' },
  ]

  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 right-4 z-50 bg-black/80 hover:bg-black/90 text-white px-4 py-2 rounded-lg backdrop-blur-sm border border-white/20 transition-all"
      >
        {isOpen ? '✕ Close' : '⚙️ Engine'}
      </button>

      {/* Main Panel */}
      {isOpen && (
        <div className="fixed top-16 right-4 z-40 w-80 bg-black/90 backdrop-blur-md rounded-lg border border-white/20 shadow-2xl">
          {/* Header */}
          <div className="px-4 py-3 border-b border-white/10">
            <h2 className="text-white font-semibold text-lg">Engine Control Panel</h2>
            <p className="text-white/60 text-xs mt-1">Configure rendering & scene settings</p>
          </div>

          {/* Section Tabs */}
          <div className="flex overflow-x-auto border-b border-white/10 bg-black/40">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`flex-1 px-3 py-2 text-xs font-medium transition-all ${
                  activeSection === section.id
                    ? 'bg-blue-600 text-white'
                    : 'text-white/60 hover:text-white hover:bg-white/5'
                }`}
              >
                <div>{section.icon}</div>
                <div className="mt-1">{section.label}</div>
              </button>
            ))}
          </div>

          {/* Content Area */}
          <div className="p-4 max-h-96 overflow-y-auto">
            {activeSection === 'camera' && <CameraControls />}
            {activeSection === 'render' && <RenderSettings />}
            {activeSection === 'postprocessing' && <PostProcessingSettings />}
            {activeSection === 'world' && <WorldSettings />}
            {activeSection === 'debug' && <DebugPanel />}
            {activeSection === 'performance' && <PerformancePanel />}
          </div>
        </div>
      )}
    </>
  )
}

// Camera Controls Section
function CameraControls() {
  const autoRotate = useSceneStore((state) => state.autoRotate)
  const setAutoRotate = useSceneStore((state) => state.setAutoRotate)
  const cameraMode = useSceneStore((state) => state.cameraMode)

  return (
    <div className="space-y-4">
      <h3 className="text-white font-medium text-sm mb-3">Camera Settings</h3>

      {/* Auto Rotate */}
      <div className="flex items-center justify-between">
        <label className="text-white/80 text-sm">Auto Rotate</label>
        <button
          onClick={() => setAutoRotate(!autoRotate)}
          className={`w-12 h-6 rounded-full transition-all ${
            autoRotate ? 'bg-blue-600' : 'bg-white/20'
          }`}
        >
          <div
            className={`w-5 h-5 bg-white rounded-full transition-transform ${
              autoRotate ? 'translate-x-6' : 'translate-x-1'
            }`}
          />
        </button>
      </div>

      {/* Camera Mode */}
      <div>
        <label className="text-white/80 text-sm block mb-2">Camera Mode</label>
        <div className="text-white/60 text-xs bg-white/5 px-3 py-2 rounded">
          {cameraMode || 'Orbit'}
        </div>
      </div>

      {/* FOV Control (placeholder for now) */}
      <div>
        <label className="text-white/80 text-sm block mb-2">Field of View</label>
        <input
          type="range"
          min="30"
          max="120"
          defaultValue="75"
          className="w-full"
        />
        <div className="text-white/40 text-xs mt-1">75°</div>
      </div>

      {/* Camera Speed */}
      <div>
        <label className="text-white/80 text-sm block mb-2">Movement Speed</label>
        <input
          type="range"
          min="0.1"
          max="5"
          step="0.1"
          defaultValue="1"
          className="w-full"
        />
        <div className="text-white/40 text-xs mt-1">1.0x</div>
      </div>
    </div>
  )
}

// Render Settings Section
function RenderSettings() {
  const showGrid = useSceneStore((state) => state.showGrid)
  const toggleGrid = useSceneStore((state) => state.toggleGrid)

  return (
    <div className="space-y-4">
      <h3 className="text-white font-medium text-sm mb-3">Render Settings</h3>

      {/* Show Grid */}
      <div className="flex items-center justify-between">
        <label className="text-white/80 text-sm">Show Grid</label>
        <button
          onClick={toggleGrid}
          className={`w-12 h-6 rounded-full transition-all ${
            showGrid ? 'bg-blue-600' : 'bg-white/20'
          }`}
        >
          <div
            className={`w-5 h-5 bg-white rounded-full transition-transform ${
              showGrid ? 'translate-x-6' : 'translate-x-1'
            }`}
          />
        </button>
      </div>

      {/* Shadow Quality */}
      <div>
        <label className="text-white/80 text-sm block mb-2">Shadow Quality</label>
        <select className="w-full bg-white/10 text-white border border-white/20 rounded px-3 py-2 text-sm">
          <option value="low">Low</option>
          <option value="medium" selected>Medium</option>
          <option value="high">High</option>
          <option value="ultra">Ultra</option>
        </select>
      </div>

      {/* Render Scale */}
      <div>
        <label className="text-white/80 text-sm block mb-2">Render Scale</label>
        <input
          type="range"
          min="0.5"
          max="2"
          step="0.1"
          defaultValue="1"
          className="w-full"
        />
        <div className="text-white/40 text-xs mt-1">100%</div>
      </div>

      {/* Anti-Aliasing */}
      <div className="flex items-center justify-between">
        <label className="text-white/80 text-sm">Anti-Aliasing</label>
        <button
          className="w-12 h-6 rounded-full transition-all bg-blue-600"
        >
          <div className="w-5 h-5 bg-white rounded-full transition-transform translate-x-6" />
        </button>
      </div>
    </div>
  )
}

// Post-Processing Settings Section (placeholder)
function PostProcessingSettings() {
  return (
    <div className="space-y-4">
      <h3 className="text-white font-medium text-sm mb-3">Post-Processing</h3>
      <p className="text-white/60 text-xs">Coming soon...</p>
    </div>
  )
}

// World Settings Section (placeholder)
function WorldSettings() {
  return (
    <div className="space-y-4">
      <h3 className="text-white font-medium text-sm mb-3">World Settings</h3>
      <p className="text-white/60 text-xs">Coming soon...</p>
    </div>
  )
}

// Debug Panel Section (placeholder)
function DebugPanel() {
  return (
    <div className="space-y-4">
      <h3 className="text-white font-medium text-sm mb-3">Debug Tools</h3>
      <p className="text-white/60 text-xs">Coming soon...</p>
    </div>
  )
}

// Performance Panel Section (placeholder)
function PerformancePanel() {
  return (
    <div className="space-y-4">
      <h3 className="text-white font-medium text-sm mb-3">Performance Monitor</h3>
      <p className="text-white/60 text-xs">Coming soon...</p>
    </div>
  )
}
