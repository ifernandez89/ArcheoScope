'use client'

import dynamic from 'next/dynamic'

const MobileSolarScene = dynamic(() => import('@/components/MobileSolarScene'), { ssr: false })

export default function MobileSolarPage() {
  return <MobileSolarScene />
}
