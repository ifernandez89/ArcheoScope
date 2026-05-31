import type { Metadata } from 'next'
import localFont from 'next/font/local'
import { Inter } from 'next/font/google'
import './globals.css'
import AlienCursorTrail from '@/components/AlienCursorTrail'
import WebVitalsInit from '@/components/WebVitalsInit'

// Fuente de marca: Spaceport 2006 — títulos, headings, botones de identidad
const archeoscope = localFont({
  src: '../public/fonts/Spaceport_2006.otf',
  variable: '--font-archeoscope',
  display: 'swap',
  weight: '400',
})

// Fuente UI: Inter — body text, labels, descripciones, UI general (WCAG AA)
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
  weight: ['400', '500', '600', '700'],
})

const BASE_PATH = process.env.NODE_ENV === 'production' ? '/ArcheoScope' : ''
const BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://ifernandez89.github.io/ArcheoScope'
  : 'http://localhost:3000'

export const metadata: Metadata = {
  title: 'Archeoscope: The Forgotten Relics',
  description: 'Explora civilizaciones antiguas y descubre reliquias olvidadas en un viaje inmersivo por la historia',
  manifest: `${BASE_PATH}/manifest.json`,
  icons: {
    icon: [
      { url: `${BASE_PATH}/branding/icons/logo-simple.png`, sizes: '32x32', type: 'image/png' },
      { url: `${BASE_PATH}/branding/icons/logo-simple-2.png`, sizes: '192x192', type: 'image/png' },
    ],
    apple: [
      { url: `${BASE_PATH}/branding/icons/logo-simple-3.png`, sizes: '180x180', type: 'image/png' },
    ],
    shortcut: `${BASE_PATH}/branding/icons/logo-simple.png`,
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
    <html lang="es" className={`${archeoscope.variable} ${inter.variable}`}>
      <body className={inter.className}>
        {children}
        <AlienCursorTrail />
        <WebVitalsInit />
        <script dangerouslySetInnerHTML={{ __html: `
          if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
              navigator.serviceWorker.register('/ArcheoScope/sw.js').catch(() => {})
            })
          }
        `}} />
      </body>
    </html>
  )
}
