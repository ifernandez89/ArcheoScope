'use client'

import { Html } from '@react-three/drei'
import type { ArchaeologicalSite } from '../engines'

/** Panel HTML 3D con información del sitio arqueológico */
export default function SiteInfo({ site }: { site: ArchaeologicalSite }) {
  return (
    <Html
      position={[0, 2.5, 0]}
      center
      distanceFactor={8}
      style={{
        background: 'rgba(0, 0, 0, 0.85)',
        padding: '12px 20px',
        borderRadius: '12px',
        border: '2px solid rgba(251, 191, 36, 0.5)',
        color: 'white',
        fontSize: '13px',
        fontFamily: 'system-ui',
        pointerEvents: 'none',
        minWidth: '250px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.5)'
      }}
    >
      <div style={{ fontWeight: 'bold', marginBottom: '8px', color: '#fbbf24', fontSize: '16px' }}>
        🛕 {site.name}
      </div>
      <div style={{ fontSize: '11px', color: '#888', marginBottom: '6px' }}>
        {site.culture} • {site.period}
      </div>
      <div style={{ fontSize: '11px', color: '#ccc', lineHeight: '1.4' }}>
        {site.description}
      </div>
    </Html>
  )
}
