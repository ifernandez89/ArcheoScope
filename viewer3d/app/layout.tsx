import type { Metadata } from 'next'
import './globals.css'
import AlienCursorTrail from '@/components/AlienCursorTrail'
import WebVitalsInit from '@/components/WebVitalsInit'

const BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://ifernandez89.github.io/ArcheoScope'
  : 'http://localhost:3000'

export const metadata: Metadata = {
  title: 'Archeoscope: The Forgotten Relics',
  description: 'Explora civilizaciones antiguas y descubre reliquias olvidadas en un viaje inmersivo por la historia',
  icons: {
    icon: [
      { url: '/branding/icons/logo-simple.png', sizes: '32x32', type: 'image/png' },
      { url: '/branding/icons/logo-simple-2.png', sizes: '192x192', type: 'image/png' },
    ],
    apple: [
      { url: '/branding/icons/logo-simple-3.png', sizes: '180x180', type: 'image/png' },
    ],
    shortcut: '/branding/icons/logo-simple.png',
  },
  openGraph: {
    title: 'Archeoscope: The Forgotten Relics',
    description: 'Explora civilizaciones antiguas y descubre reliquias olvidadas en un viaje inmersivo por la historia',
    url: BASE_URL,
    siteName: 'Archeoscope',
    images: [
      {
        url: `${BASE_URL}/branding/logo/logo-main.png`,
        width: 1200,
        height: 630,
        alt: 'Archeoscope: The Forgotten Relics',
      },
    ],
    locale: 'es_ES',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Archeoscope: The Forgotten Relics',
    description: 'Explora civilizaciones antiguas y descubre reliquias olvidadas',
    images: [`${BASE_URL}/branding/logo/logo-main.png`],
  },
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
      </body>
    </html>
  )
}
