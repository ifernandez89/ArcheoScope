'use client'

import { useEffect } from 'react'

const ALIEN_CURSOR =
  "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Cpolygon points='16,2 30,16 16,30 2,16' fill='none' stroke='%2300aaff' stroke-width='1.2' opacity='0.9'/%3E%3Cpolygon points='16,8 24,16 16,24 8,16' fill='none' stroke='%2300aaff' stroke-width='0.8' opacity='0.6'/%3E%3Ccircle cx='16' cy='16' r='2' fill='%2300aaff' opacity='1'/%3E%3Cline x1='16' y1='2' x2='16' y2='8' stroke='%2300aaff' stroke-width='1' opacity='0.5'/%3E%3Cline x1='16' y1='24' x2='16' y2='30' stroke='%2300aaff' stroke-width='1' opacity='0.5'/%3E%3Cline x1='2' y1='16' x2='8' y2='16' stroke='%2300aaff' stroke-width='1' opacity='0.5'/%3E%3Cline x1='24' y1='16' x2='30' y2='16' stroke='%2300aaff' stroke-width='1' opacity='0.5'/%3E%3C/svg%3E\") 16 16, crosshair"

function forceOnAll() {
  document.querySelectorAll<HTMLElement>('canvas, body, html').forEach(el => {
    el.style.setProperty('cursor', ALIEN_CURSOR, 'important')
  })
}

export default function AlienCursorTrail() {
  useEffect(() => {
    forceOnAll()

    const mo = new MutationObserver(forceOnAll)
    const observe = () => {
      document.querySelectorAll('canvas').forEach(c =>
        mo.observe(c, { attributes: true, attributeFilter: ['style'] })
      )
      mo.observe(document.body, { attributes: true, attributeFilter: ['style'] })
      mo.observe(document.documentElement, { attributes: true, attributeFilter: ['style'] })
    }
    observe()

    const domMo = new MutationObserver(() => { observe(); forceOnAll() })
    domMo.observe(document.body, { childList: true, subtree: true })

    const interval = setInterval(forceOnAll, 200)

    return () => {
      mo.disconnect()
      domMo.disconnect()
      clearInterval(interval)
    }
  }, [])

  return null
}
