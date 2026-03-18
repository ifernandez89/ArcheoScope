import type { Metadata } from 'next'
import './globals.css'
import AlienCursorTrail from '@/components/AlienCursorTrail'
import WebVitalsInit from '@/components/WebVitalsInit'
import PerformanceStats from '@/components/PerformanceStats'

export const metadata: Metadata = {
  title: 'Archeoscope: The Forgotten Relics',
  description: 'Explora civilizaciones antiguas y descubre reliquias olvidadas en un viaje inmersivo por la historia',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>
        {children}
        <AlienCursorTrail />
        <WebVitalsInit />
        <PerformanceStats />
      </body>
    </html>
  )
}
