'use client'

import { useState } from 'react'
import { useSceneStore } from '@/store/scene-store'

export default function UI() {
  const [showInfo, setShowInfo] = useState(true)
  
  const autoRotate = useSceneStore((state) => state.autoRotate)
  const setAutoRotate = useSceneStore((state) => state.setAutoRotate)
  const showGrid = useSceneStore((state) => state.showGrid)
  const toggleGrid = useSceneStore((state) => state.toggleGrid)
  const cameraMode = useSceneStore((state) => state.cameraMode)

  return (
    <>


    </>
  )
}
