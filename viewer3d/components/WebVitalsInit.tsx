/**
 * Componente para inicializar Web Vitals
 * Se monta en el layout principal
 */

'use client'

import { useEffect } from 'react'
import { initWebVitals } from '@/lib/webVitals'

export default function WebVitalsInit() {
  useEffect(() => {
    // Inicializar Web Vitals
    initWebVitals()
  }, [])
  
  return null
}
