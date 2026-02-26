# Features implementadas — 26/02/2026

## 🌩️ Clima por defecto al llegar a sitios
- Al navegar a cualquier sitio arqueológico (por marcador o coordenadas), el clima se activa automáticamente: tormenta eléctrica + rayos + lluvia fuerte + viento + nubes.
- El menú de clima sigue disponible para activar/desactivar manualmente.
- Al volver al globo, el audio climático se silencia completamente.

## 🏛️ Secuencia de descubrimiento de megaestructura
- Al mover un bloque en Puma Punku, se activa terremoto simultáneamente con el fade-in de la estructura.
- A los 3.2 segundos (cuando la estructura es completamente visible), todo el clima cesa — calma total.
- El descubrimiento es **por sitio**: una vez descubierto, al volver al sitio el clima ya es tranquilo. Los demás sitios mantienen tormenta hasta que se descubra su estructura.
- `discoveredSites` persiste durante la sesión como `Set<string>`.

## 🌲 Triple de árboles al descubrir la megaestructura
- Al revelar la estructura, `blockMoved = true` triplica los árboles en la escena.
- Los árboles extra aparecen en radio exterior (≥35 unidades) para no colisionar con la estructura.
- Sistema anti-superposición: `occupied[]` registra zonas bloqueadas (estructura + cada árbol colocado). Cada nuevo árbol verifica distancia mínima con hasta 8 intentos de reubicación.

## ☁️ Nubes de tormenta en triple capa
- En modo tormenta, se renderizan 3 capas de `CloudSky` a distintas alturas (60, 100, 160) y velocidades, con 60 nubes por textura — cielo completamente cubierto y oscuro.

## 🎯 Cursor alien azul (rombo HUD sci-fi)
- Cursor SVG inline: rombo doble concéntrico + punto central azul `#00aaff`.
- `MutationObserver` + `setInterval(200ms)` fuerzan el cursor en todos los canvas, body y html, revirtiendo cualquier override de Three.js/R3F.
- Sin estela de partículas.

## 🔊 Audio ambiente en modo exploración
- `AmbientAudio.tsx` — componente R3F independiente que inicializa `AtmosphericSound` en primera interacción del usuario.
- Funciona en modo órbita y avatar, sin depender de `AstronomicalSystem`.
