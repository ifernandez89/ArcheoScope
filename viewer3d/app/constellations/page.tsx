'use client'

import dynamic from 'next/dynamic'

const ConstellationsScene = dynamic(() => import('@/components/ConstellationsScene'), { ssr: false })

export default function ConstellationsPage() {
  return <ConstellationsScene />
}
