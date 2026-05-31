/**
 * Service Worker — Archeoscope PWA
 * Enables offline support, caching, and Play Store TWA compatibility
 */

const CACHE_NAME = 'archeoscope-v1'
const STATIC_ASSETS = [
  '/ArcheoScope/',
  '/ArcheoScope/menu',
  '/ArcheoScope/manifest.json',
  '/ArcheoScope/branding/logo/logo-main.png',
  '/ArcheoScope/branding/loading/logo-loading.png',
]

// Install: cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch(() => {
        // Ignore errors for missing assets
      })
    })
  )
  self.skipWaiting()
})

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  )
  self.clients.claim()
})

// Fetch: network-first for API/3D assets, cache-first for static
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url)

  // Skip non-GET requests
  if (event.request.method !== 'GET') return

  // Skip API routes
  if (url.pathname.startsWith('/api/')) return

  // Skip large 3D assets (GLB, textures) — always fetch fresh
  if (url.pathname.match(/\.(glb|gltf|fbx|obj)$/i)) return

  // Network-first strategy for HTML pages
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() =>
        caches.match('/ArcheoScope/') || caches.match('/')
      )
    )
    return
  }

  // Cache-first for static assets (JS, CSS, images, fonts)
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached
      return fetch(event.request).then((response) => {
        if (response.ok && response.type === 'basic') {
          const clone = response.clone()
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone))
        }
        return response
      })
    })
  )
})
