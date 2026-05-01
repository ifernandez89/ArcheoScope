# Changelog

All notable changes to Archeoscope: The Forgotten Relics will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-01

### 🌌 Escenas 3D
- **Sistema Solar 3D** — 9 planetas con texturas reales, órbitas astronómicas, asteroides, anillos de Saturno
- **Constelaciones** — 27 constelaciones con líneas y nombres, 83,130 estrellas en 3 capas, Vía Láctea procedimental, luna billboard con textura, terreno desierto con vegetación
- **Escenas terrestres** — 7 sitios arqueológicos (Puma Punku, Giza, Teotihuacán, Isla de Pascua, Veracruz, Göbekli Tepe, Mictlán)
- **Sistema climático** — lluvia, nieve, viento, rayos, tormentas, terremotos, erupciones volcánicas

### 🔭 Astronomía y Astrología
- **Motor astronómico** — astronomy-engine (VSOP87/ELP, precisión ~1 arcmin)
- **Rueda astrológica SVG** — 12 signos, 10 planetas, aspectos ptolemaicos, casas
- **Velocidad instantánea dλ/dt** — detección de planetas estacionarios y retrogradaciones (Δt=1h)
- **Elementos predominantes** — balance Fuego/Tierra/Aire/Agua con interpretación diaria
- **Nodos lunares** — Nodo Norte/Sur con signo, grado e interpretación del alma
- **Lectura astrológica dinámica** — interpretación profesional generada por fecha
- **Notas metodológicas** — fuentes citadas (Ptolomeo, Greene, Arroyo, JPL/NASA)

### 📅 Calendarios
- **Cholq'ij** — calendario sagrado maya (13 números × 20 nawales), información espiritual, tabla comparativa con Tzolk'in clásico
- **Tzolk'in Clásico** — correlación GMT 584283, Cuenta Larga + Haab
- **Calendario Babilónico** — sistema sexagesimal base 60, coordenadas celestes RA/Dec

### 🌤️ Clima Local
- **Open-Meteo API** — temperatura, humedad, viento, probabilidad de lluvia
- **Fase lunar precisa** — astronomy-engine con signo zodiacal (ej: "Luna Llena en Escorpio")
- **Amanecer/Atardecer** — hora local exacta + duración del día
- **Animaciones CSS** — día soleado, noche estrellada, lluvia, nieve, tormenta, niebla (adaptativas día/noche)
- **Geocoding** — ciudad y país via OpenStreetMap Nominatim
- **Cache 30 minutos** — localStorage para reducir llamadas API

### 📱 Mobile
- **Menú demo** — Controles, Constelaciones, Astrología, Calendarios, Clima Local, Información, 3D Solar System
- **Touch D-pad** — movimiento WASD + rotación Q/R para escenas terrestres
- **Landscape lock** — orientación horizontal forzada con fallback portrait overlay
- **Optimizaciones GPU** — pixelRatio 1.2, sin bloom/vignette, partículas reducidas 50%, terreno 48×48, frame skip
- **MOBILE_STORM_WEATHER** — tormenta reducida sin rayos para evitar crash de memoria en Edge

### 🎮 Juego (PC)
- **5 naves UFO** — cada una con habilidad especial (cloaking, campo EM, teletransporte, escáner, fuerza bruta)
- **Sistema de misiones** — 5 sitios principales con NPCs, diálogos interactivos, items coleccionables
- **Inventario** — items recolectables con drag & drop
- **HarmoniaMundi** — música cósmica procedural que se desbloquea con misiones
- **Audio procedural** — clima, viento, lluvia, truenos generados en tiempo real

### ⚖️ Licencia y PWA
- **CC BY-NC 4.0** — código fuente abierto para uso no comercial
- **All Rights Reserved** — assets protegidos (modelos, texturas, audio)
- **Service Worker** — soporte offline, cache de assets estáticos
- **Digital Asset Links** — preparado para Google Play Store via TWA

### 🛠️ Infraestructura
- Next.js 14 (App Router) + Three.js + React Three Fiber + TypeScript + Bun
- GitHub Pages deployment con basePath `/ArcheoScope`
- Yale Bright Star Catalogue (~130 estrellas reales con RA/Dec)
- Catálogo de 27 constelaciones IAU

---

Copyright (c) 2026 Ignacio Fernandez
