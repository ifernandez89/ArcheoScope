import type { Metadata } from 'next'
import './globals.css'
import AlienCursorTrail from '@/components/AlienCursorTrail'

export const metadata: Metadata = {
  title: 'ArcheoScope 3D Viewer',
  description: 'Visualizador 3D interactivo para modelos arqueológicos',
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
      </body>
    </html>
  )
}
