# 📡 Archeoscope — Guía de Replicación de Módulos como Páginas Independientes
> Para alimentar un asistente IA con datos actualizados. Cada sección puede existir como página web autónoma o endpoint JSON scrapeable.

---

## Stack base recomendado (sin framework)

```html
<!-- Mínimo para cualquier módulo -->
<script src="https://cdn.jsdelivr.net/npm/astronomy-engine@2/astronomy.browser.min.js"></script>
```

Dependencias por módulo:
- **Astronomía/Astrología/Hoy**: `astronomy-engine` (VSOP87, sin API key)
- **Clima**: `Open-Meteo API` (gratis, sin API key) + `Nominatim` (geocoding)
- **Brújula**: `DeviceOrientationEvent` (nativa del browser)
- **Calendarios**: Solo JS puro (algoritmos matemáticos)

---

## 📐 Formato de salida recomendado para scraping IA

Cada página debe incluir un bloque JSON embebido en el HTML:

```html
<script id="ai-data" type="application/json">
  { /* datos estructurados */ }
</script>
```

O un endpoint dedicado: `GET /api/module?lat=XX&lon=YY&date=YYYY-MM-DD`

---

## 1. 🌌 MÓDULO: HOY — Qué pasa en el cielo ahora

**Ruta actual**: `/menu/calendarios/today`

### Datos que expone

| Dato | Fuente | Tipo |
|------|--------|------|
| Fase lunar (nombre + emoji + iluminación %) | `astronomy-engine` | Calculado |
| Posición lunar (signo zodiacal + grados) | `astronomy-engine` | Calculado |
| Posición solar (signo + grados) | `astronomy-engine` | Calculado |
| Día Cholq'ij/Tzolk'in | Algoritmo GMT | Calculado |
| Estación solar (progreso %) + días al próximo evento | Algoritmo DOY | Calculado |
| Próximos eventos astronómicos (lluvias de meteoros, solsticios) | Array estático + DOY | Calculado |
| Próximos eclipses (solar/lunar, tipo, días) | `astronomy-engine` | Calculado |
| Ventana de eclipse Dresden Codex | Ciclo dracónico 173.31d | Calculado |
| Planetas visibles esta noche (elongación >20° del Sol) | `astronomy-engine` | Calculado |
| Condiciones de observación nocturna | Fase lunar + elongación | Calculado |

### Implementación mínima

```javascript
// Dependencias: astronomy-engine
import * as Astronomy from 'astronomy-engine'

function getTodaySkyData(date = new Date()) {
  const t = Astronomy.MakeTime(date)
  const SIGNS = ['Aries','Tauro','Géminis','Cáncer','Leo','Virgo',
                 'Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis']
  const GLYPHS = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓']

  // --- LUNA ---
  const moonLon    = Astronomy.EclipticLongitude(Astronomy.Body.Moon, t)
  const phaseAngle = Astronomy.MoonPhase(t)
  const illumination = Math.round((1 - Math.cos(phaseAngle * Math.PI / 180)) / 2 * 100)
  const PHASE_NAMES = [
    [11.25,'Luna Nueva','🌑'],[78.75,'Creciente','🌒'],
    [101.25,'Cuarto Creciente','🌓'],[168.75,'Gibosa Creciente','🌔'],
    [191.25,'Luna Llena','🌕'],[258.75,'Gibosa Menguante','🌖'],
    [281.25,'Cuarto Menguante','🌗'],[348.75,'Menguante','🌘']
  ]
  let phaseName = 'Luna Nueva', phaseEmoji = '🌑'
  for (const [limit, name, emoji] of PHASE_NAMES) {
    if (phaseAngle < limit) { phaseName = name; phaseEmoji = emoji; break }
  }

  // --- SOL ---
  const sunLon = Astronomy.SunPosition(t).elon

  // --- PRÓXIMA FASE ---
  const nextQ = Astronomy.SearchMoonQuarter(t)
  const QN = ['Luna Nueva','Cuarto Creciente','Luna Llena','Cuarto Menguante']

  // --- PLANETAS VISIBLES (elongación >20° del Sol) ---
  const PLANETS = [
    { body: Astronomy.Body.Mercury, name: 'Mercurio' },
    { body: Astronomy.Body.Venus,   name: 'Venus' },
    { body: Astronomy.Body.Mars,    name: 'Marte' },
    { body: Astronomy.Body.Jupiter, name: 'Júpiter' },
    { body: Astronomy.Body.Saturn,  name: 'Saturno' },
  ]
  const visible = PLANETS.map(p => {
    const lon = Astronomy.EclipticLongitude(p.body, t)
    let diff = Math.abs(lon - sunLon)
    if (diff > 180) diff = 360 - diff
    return { ...p, visible: diff > 20,
      sign: SIGNS[Math.floor(lon/30)%12],
      deg: (lon%30).toFixed(1) }
  }).filter(p => p.visible)

  return {
    date: date.toISOString(),
    moon: {
      phase: phaseName, emoji: phaseEmoji, illumination,
      sign: SIGNS[Math.floor(moonLon/30)%12],
      glyph: GLYPHS[Math.floor(moonLon/30)%12],
      degrees: (moonLon%30).toFixed(2),
      nextPhase: { name: QN[nextQ.quarter], date: nextQ.time.date.toISOString() }
    },
    sun: {
      sign: SIGNS[Math.floor(sunLon/30)%12],
      glyph: GLYPHS[Math.floor(sunLon/30)%12],
      degrees: (sunLon%30).toFixed(2)
    },
    visiblePlanets: visible.map(p => ({ name: p.name, sign: p.sign, degrees: p.deg }))
  }
}
```

### Cholq'ij (sin dependencias externas)

```javascript
// Referencia: 1 ene 2000 = 11 B'atz' (nawal idx 10, num idx 10)
const NAWALES = ['Imox','Iq\'','Aq\'ab\'al','K\'at','Kan','Keme','Kej',
                 'Q\'anil','Toj','Tz\'i\'','B\'atz\'','E','Aj','I\'x',
                 'Tz\'ikin','Ajmaq','No\'j','Tijax','Kawoq','Ajpu']
const REF = new Date(2000, 0, 1)
const REF_NAWAL = 10, REF_NUM = 10

function getCholqij(date = new Date()) {
  const diff = Math.floor((date - REF) / 86400000)
  return {
    nawal: NAWALES[((REF_NAWAL + diff) % 20 + 20) % 20],
    num:   (((REF_NUM   + diff) % 13 + 13) % 13) + 1
  }
}
```


### Estructura JSON de salida esperada

```json
{
  "date": "2026-06-23T12:00:00.000Z",
  "moon": {
    "phase": "Gibosa Menguante",
    "emoji": "🌖",
    "illumination": 72,
    "sign": "Acuario",
    "glyph": "♒",
    "degrees": "14.33",
    "nextPhase": { "name": "Cuarto Menguante", "date": "2026-06-26T..." }
  },
  "sun": { "sign": "Cáncer", "glyph": "♋", "degrees": "1.85" },
  "visiblePlanets": [
    { "name": "Júpiter", "sign": "Géminis", "degrees": "18.2" },
    { "name": "Saturno", "sign": "Piscis",  "degrees": "4.7" }
  ],
  "cholqij": { "nawal": "Tijax", "num": 8 }
}
```

---

## 2. 🪐 MÓDULO: ASTROLOGÍA — Carta Celeste

**Ruta actual**: `/menu/astrology`

### Datos que expone

| Dato | Fuente | Tipo |
|------|--------|------|
| Posición de 10 planetas (signo + grados) | `astronomy-engine` | Calculado |
| Estado de cada planeta (directo/retrógrado/estacionario) | Δλ/Δt en 1h | Calculado |
| 5 tipos de aspectos (conjunción, oposición, trígono, cuadratura, sextil) | Diferencia angular | Calculado |
| Balance de elementos (Fuego/Tierra/Aire/Agua) | Signo de cada planeta | Calculado |
| Nodos Lunares (Norte/Sur + signo) | Aproximación clásica | Calculado |
| Luna Azul (detección doble luna llena en el mes) | `astronomy-engine` | Calculado |
| Interpretación textual de aspectos y posiciones | Tabla de interpretaciones | Estático + Calculado |
| Próximas luna nueva y llena (fecha + signo) | `astronomy-engine` | Calculado |
| Selector de fecha (cualquier fecha histórica o futura) | Input del usuario | — |

### Implementación mínima (posiciones planetarias)

```javascript
import * as Astronomy from 'astronomy-engine'

const BODIES = {
  sun:     null, // usa SunPosition()
  moon:    Astronomy.Body.Moon,
  mercury: Astronomy.Body.Mercury,
  venus:   Astronomy.Body.Venus,
  mars:    Astronomy.Body.Mars,
  jupiter: Astronomy.Body.Jupiter,
  saturn:  Astronomy.Body.Saturn,
  uranus:  Astronomy.Body.Uranus,
  neptune: Astronomy.Body.Neptune,
  pluto:   Astronomy.Body.Pluto,
}

const SIGNS = ['Aries','Tauro','Géminis','Cáncer','Leo','Virgo',
               'Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis']

function getPlanetPositions(date = new Date()) {
  const t = Astronomy.MakeTime(date)
  const positions = {}
  const retrograde = {}

  // Sol (método especial)
  positions.sun = Astronomy.SunPosition(t).elon

  // Planetas
  for (const [id, body] of Object.entries(BODIES)) {
    if (!body) continue
    const lon = Astronomy.EclipticLongitude(body, t)
    positions[id] = lon

    // Velocidad instantánea (Δt = 1 hora)
    const tNext = Astronomy.MakeTime(new Date(date.getTime() + 3600000))
    let dlon = Astronomy.EclipticLongitude(body, tNext) - lon
    if (dlon > 180) dlon -= 360
    if (dlon < -180) dlon += 360
    retrograde[id] = (dlon * 24) < 0 // velocidad diaria negativa = retrógrado
  }

  return Object.fromEntries(
    Object.entries(positions).map(([id, lon]) => [id, {
      longitude: lon,
      sign: SIGNS[Math.floor(lon/30)%12],
      degrees: (lon%30).toFixed(2),
      retrograde: retrograde[id] || false
    }])
  )
}
```

### Algoritmo de aspectos

```javascript
const ASPECTS = [
  { name: 'Conjunción', angle: 0,   orb: 8, glyph: '☌' },
  { name: 'Oposición',  angle: 180, orb: 8, glyph: '☍' },
  { name: 'Trígono',    angle: 120, orb: 7, glyph: '△' },
  { name: 'Cuadratura', angle: 90,  orb: 7, glyph: '□' },
  { name: 'Sextil',     angle: 60,  orb: 5, glyph: '⚹' },
]

function getAspects(positions) {
  const lons = Object.entries(positions).map(([id, p]) => [id, p.longitude])
  const aspects = []
  for (let i = 0; i < lons.length; i++) {
    for (let j = i+1; j < lons.length; j++) {
      const [id1, lon1] = lons[i]
      const [id2, lon2] = lons[j]
      const diff = Math.abs(lon1 - lon2)
      const angle = diff > 180 ? 360 - diff : diff
      for (const asp of ASPECTS) {
        if (Math.abs(angle - asp.angle) <= asp.orb) {
          aspects.push({ p1: id1, p2: id2, ...asp,
            orb: Math.abs(angle - asp.angle).toFixed(2) })
          break
        }
      }
    }
  }
  return aspects
}
```

### Nodos Lunares (aproximación clásica)

```javascript
// Ciclo de 18.6 años, velocidad -0.05295°/día
// Referencia: Nodo Norte en 0° Aries el 1 enero 2005 (JD 2453371.5)
function getLunarNodes(date = new Date()) {
  const jd = (date.getTime() / 86400000) + 2440587.5
  const northNode = ((0 - 0.05295 * (jd - 2453371.5)) % 360 + 360) % 360
  const southNode = (northNode + 180) % 360
  return {
    northNode: { longitude: northNode, sign: SIGNS[Math.floor(northNode/30)%12] },
    southNode: { longitude: southNode, sign: SIGNS[Math.floor(southNode/30)%12] }
  }
}
```


---

## 3. 🌦️ MÓDULO: CLIMA LOCAL

**Ruta actual**: `/menu/weather`

### Datos que expone

| Dato | API | Autenticación |
|------|-----|---------------|
| Temperatura actual + sensación térmica | Open-Meteo | ❌ Sin key |
| Humedad, viento, código climático WMO | Open-Meteo | ❌ Sin key |
| Probabilidad de lluvia | Open-Meteo | ❌ Sin key |
| Amanecer / Atardecer / Duración del día | Open-Meteo `daily` | ❌ Sin key |
| Pronóstico 6 días (max, min, lluvia, código WMO) | Open-Meteo `daily` | ❌ Sin key |
| Nombre de ciudad/país | Nominatim (OpenStreetMap) | ❌ Sin key |
| Fase lunar (integrada) | `astronomy-engine` | ❌ Sin key |
| Condiciones de observación astronómica | Cálculo local | — |
| Geocoding inverso (lat/lon → nombre) | Nominatim | ❌ Sin key |

### Implementación mínima

```javascript
async function getWeatherData(lat, lon) {
  // 1. Clima (Open-Meteo)
  const url = `https://api.open-meteo.com/v1/forecast`
    + `?latitude=${lat}&longitude=${lon}`
    + `&current=temperature_2m,relative_humidity_2m,apparent_temperature,`
    + `wind_speed_10m,weather_code,precipitation_probability`
    + `&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min,`
    + `precipitation_probability_max,weather_code`
    + `&wind_speed_unit=kmh&timezone=auto`

  const res  = await fetch(url)
  const data = await res.json()
  const c    = data.current

  // 2. Geocoding inverso (Nominatim)
  let city = `${lat.toFixed(2)}°, ${lon.toFixed(2)}°`, country = ''
  try {
    const geo = await fetch(
      `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`
    )
    const gd = await geo.json()
    city    = gd.address?.city || gd.address?.town || gd.address?.village || city
    country = gd.address?.country || ''
  } catch {}

  // 3. Sunrise/Sunset
  const fmtTime = iso => iso ? new Date(iso).toLocaleTimeString('es-ES',
    { hour: '2-digit', minute: '2-digit' }) : '--:--'
  const sunrise = fmtTime(data.daily?.sunrise?.[0])
  const sunset  = fmtTime(data.daily?.sunset?.[0])

  // 4. Duración del día
  let dayLength = '--'
  if (data.daily?.sunrise?.[0] && data.daily?.sunset?.[0]) {
    const mins = Math.round((new Date(data.daily.sunset[0]) -
      new Date(data.daily.sunrise[0])) / 60000)
    dayLength = `${Math.floor(mins/60)}h ${mins%60}m`
  }

  return {
    city, country, lat, lon,
    current: {
      temp: Math.round(c.temperature_2m),
      feelsLike: Math.round(c.apparent_temperature),
      humidity: c.relative_humidity_2m,
      windSpeed: Math.round(c.wind_speed_10m),
      rainProbability: c.precipitation_probability || 0,
      weatherCode: c.weather_code,
      description: getWeatherDesc(c.weather_code)  // ver función abajo
    },
    solar: { sunrise, sunset, dayLength },
    forecast: (data.daily?.time || []).slice(1, 7).map((dateStr, i) => ({
      date: dateStr,
      tempMax: Math.round(data.daily.temperature_2m_max[i+1]),
      tempMin: Math.round(data.daily.temperature_2m_min[i+1]),
      rainProb: data.daily.precipitation_probability_max[i+1] || 0,
      weatherCode: data.daily.weather_code[i+1] || 0
    }))
  }
}

// Tabla de códigos WMO
function getWeatherDesc(code) {
  if (code === 0)    return 'Despejado'
  if (code <= 2)     return 'Parcialmente nublado'
  if (code === 3)    return 'Nublado'
  if (code <= 49)    return 'Niebla'
  if (code <= 59)    return 'Llovizna'
  if (code <= 69)    return 'Lluvia'
  if (code <= 79)    return 'Nieve'
  if (code <= 82)    return 'Chubascos'
  if (code <= 86)    return 'Nieve intensa'
  if (code <= 99)    return 'Tormenta'
  return 'Variable'
}
```

### Estructura JSON de salida

```json
{
  "city": "Buenos Aires", "country": "Argentina",
  "lat": -34.6037, "lon": -58.3816,
  "current": {
    "temp": 12, "feelsLike": 9, "humidity": 71,
    "windSpeed": 18, "rainProbability": 5,
    "weatherCode": 1, "description": "Parcialmente nublado"
  },
  "solar": { "sunrise": "07:43", "sunset": "18:02", "dayLength": "10h 19m" },
  "forecast": [
    { "date": "2026-06-24", "tempMax": 14, "tempMin": 8, "rainProb": 10, "weatherCode": 0 }
  ]
}
```

### Caché recomendada
Cache en `localStorage` por 30 min (o en Redis si es un servidor):
```javascript
const CACHE_KEY = 'weather_data'
const CACHE_TTL = 30 * 60 * 1000 // 30 minutos
```

---

## 4. 🧭 MÓDULO: BRÚJULA

**Ruta actual**: `/menu/brujula`

### Datos que expone

| Dato | Fuente | Notas |
|------|--------|-------|
| Rumbo magnético (0-360°) | `DeviceOrientationEvent` | Solo mobile/HTTPS |
| Dirección cardinal (N/NE/E/SE/S/SO/O/NO) | Cálculo local | — |
| Precisión del sensor (±N°) | `webkitCompassAccuracy` | Solo iOS |

### Implementación mínima

```javascript
function startCompass(onUpdate) {
  // iOS: requiere permiso explícito (click del usuario)
  async function requestAndStart() {
    if (typeof DeviceOrientationEvent?.requestPermission === 'function') {
      const result = await DeviceOrientationEvent.requestPermission()
      if (result !== 'granted') throw new Error('Permiso denegado')
    }
    attachListeners()
  }

  let smoothed = null
  function smooth(raw) {
    if (smoothed === null) { smoothed = raw; return raw }
    let diff = raw - smoothed
    if (diff > 180)  diff -= 360
    if (diff < -180) diff += 360
    smoothed = ((smoothed + diff * 0.15) + 360) % 360
    return smoothed
  }

  function handler(e) {
    let raw = null
    if (e.webkitCompassHeading !== undefined) {
      raw = e.webkitCompassHeading  // iOS: ya es el norte real
    } else if (e.alpha !== null) {
      raw = (360 - e.alpha) % 360   // Android
    }
    if (raw !== null) onUpdate({
      heading:  smooth(raw),
      cardinal: toCardinal(smooth(raw)),
      accuracy: e.webkitCompassAccuracy ?? null
    })
  }

  // deviceorientationabsolute es más preciso en Android
  window.addEventListener('deviceorientationabsolute', handler, true)
  window.addEventListener('deviceorientation', handler, true)
  return () => {
    window.removeEventListener('deviceorientationabsolute', handler, true)
    window.removeEventListener('deviceorientation', handler, true)
  }
}

function toCardinal(deg) {
  const n = ((deg % 360) + 360) % 360
  const dirs = ['N','NE','E','SE','S','SO','O','NO']
  return dirs[Math.round(n / 45) % 8]
}
```

### Notas importantes
- **Requiere HTTPS** — `DeviceOrientationEvent` no funciona en HTTP
- **iOS 13+**: requiere `DeviceOrientationEvent.requestPermission()` activado desde un gesto del usuario (botón)
- **Android**: no requiere permiso explícito, inicia automáticamente
- **No scraping posible en servidor** — es una API del dispositivo físico; para IA, documentar la estructura de salida y que el cliente la envíe al servidor

### Estructura JSON de salida (enviar al servidor)

```json
{
  "heading": 247.3,
  "cardinal": "SO",
  "cardinalLabel": "Suroeste",
  "accuracy": 15,
  "timestamp": "2026-06-23T20:15:30.000Z"
}
```

---

## 5. 📅 MÓDULO: CALENDARIOS ANTIGUOS

**Ruta actual**: `/menu/calendarios` + 4 sub-páginas

---

### 5a. 🌌 Vista Integrada "Hoy"

(Ver Módulo 1 — ya documentado arriba con Cholq'ij, eclipses, estación)

---

### 5b. 🏛️ Tzolk'in Clásico (GMT 584283)

**Ruta**: `/menu/calendarios/tzolkin`

#### Datos que expone

| Dato | Algoritmo | Precisión |
|------|-----------|-----------|
| Cuenta Larga Maya | JDN − GMT | ✅ Exacta |
| Tzolk'in (número + sello/kin) | Módulo 13×20 desde GMT | ✅ Exacta |
| Haab (día + mes) | Módulo 365 desde GMT | ✅ Exacta |
| Ciclo Venus (584 días, fase actual) | Módulo 584 desde GMT | Aproximada |
| Fase lunar maya (29.53 días) | Módulo 29.53 desde GMT | Aproximada |
| Temporada de eclipses (173.31 días) | Semestre dracónico | Aproximada |
| Rueda Calendárica (18,980 días ≈ 52 años) | Tzolk'in × Haab | ✅ Exacta |
| Sincronía Venus-Solar (2,920 días) | 5 Venus = 8 años | ✅ Exacta |

#### Implementación mínima

```javascript
const GMT_CORRELATION = 584283

function toJDN(y, m, d) {
  const a = Math.floor((14-m)/12), yy = y+4800-a, mm = m+12*a-3
  return d + Math.floor((153*mm+2)/5) + 365*yy + Math.floor(yy/4)
       - Math.floor(yy/100) + Math.floor(yy/400) - 32045
}

const SELLOS = ['Imix','Ik','Akbal','Kan','Chicchan','Cimi','Manik','Lamat',
                'Muluc','Oc','Chuen','Eb','Ben','Ix','Men','Cib',
                'Caban','Etznab','Cauac','Ahau']
const TONOS  = ['Magnético','Lunar','Eléctrico','Autoexistente','Entonado',
                'Rítmico','Resonante','Galáctico','Solar','Planetario',
                'Espectral','Cristal','Cósmico']
const HAAB   = ['Pop','Wo','Sip','Sotz','Sek','Xul','Yaxkin','Mol','Chen',
                'Yax','Sak','Keh','Mak','Kankin','Muwan','Pax','Kayab','Kumku','Wayeb']

function getMayanCalendar(date = new Date()) {
  const jdn = toJDN(date.getFullYear(), date.getMonth()+1, date.getDate())
  const md  = jdn - GMT_CORRELATION  // días desde 0.0.0.0.0

  // Tzolk'in
  const num  = ((md + 4) % 13 + 13) % 13 || 13
  const seal = ((md + 19) % 20 + 20) % 20
  const kin  = ((md % 260) + 260) % 260 || 260

  // Haab
  const haabDay   = ((md + 348) % 365 + 365) % 365
  const haabMonth = Math.min(Math.floor(haabDay/20), 18)
  const haabDayN  = haabDay % 20

  // Cuenta Larga (base 20-20-18-20-20)
  let d2 = md
  const kin_lc = d2%20; d2=Math.floor(d2/20)
  const uinal   = d2%18; d2=Math.floor(d2/18)
  const tun     = d2%20; d2=Math.floor(d2/20)
  const katun   = d2%20; d2=Math.floor(d2/20)
  const baktun  = d2

  // Ciclos astronómicos
  const venusCycle   = 584
  const venusDay     = ((md % venusCycle) + venusCycle) % venusCycle
  const calRoundDay  = ((md % 18980)      + 18980)      % 18980
  const eclipseDay   = ((md % 173.31)     + 173.31)     % 173.31

  return {
    gregorian:   date.toISOString().split('T')[0],
    jdn, mayanDays: md,
    longCount:   `${baktun}.${katun}.${tun}.${uinal}.${kin_lc}`,
    tzolkin: { num, tone: TONOS[num-1], sealIndex: seal, seal: SELLOS[seal], kin },
    haab: { day: haabDayN, monthIndex: haabMonth, month: HAAB[haabMonth] },
    cycles: {
      venus: { day: venusDay, progress: Math.round(venusDay/venusCycle*100) },
      calendarRound: { day: calRoundDay, year52: Math.floor(calRoundDay/365) },
      eclipseSeason: { day: eclipseDay, active: eclipseDay < 18 || eclipseDay > 155 }
    }
  }
}
```

#### Verificación

```
21 dic 2012 → Tzolk'in: 4 Ahau, Haab: 3 Kankin ✓ (correlación GMT 584283)
```


---

### 5c. 🌀 Cholq'ij / Dreamspell

**Ruta**: `/menu/calendarios/dreamspell`

Mismo algoritmo que el Tzolk'in Clásico pero con los nombres en k'iche' (maya moderno).

#### Datos que expone

| Dato | Valor |
|------|-------|
| Nombre del nawal (en k'iche') | 20 nawales: Imox, Iq', Aq'ab'al... |
| Número del día (1–13) | Tono energético |
| Descripción espiritual del nawal | Texto descriptivo |
| Mensaje diario | Texto interpretativo |
| Selector de fecha | Cualquier fecha |

#### Diferencia con Tzolk'in clásico

```
Maya clásico → k'iche' moderno
Imix        → Imox
Ik'         → Iq'
Akbal       → Aq'ab'al
Ahau        → Ajpu
Cauac       → Kawoq
```

**Mismo algoritmo de cálculo** — solo cambia la tabla de nombres:

```javascript
const NAWALES_KICHE = [
  'Imox', "Iq'", "Aq'ab'al", "K'at", 'Kan', 'Keme', 'Kej',
  "Q'anil", 'Toj', "Tz'i'", "B'atz'", 'E', 'Aj', "I'x",
  "Tz'ikin", 'Ajmaq', "No'j", 'Tijax', 'Kawoq', 'Ajpu'
]
// Referencia: 1 ene 2000 = nawal idx 10 (B'atz'), número 11 (idx 10)
```

### JSON de salida

```json
{
  "date": "2026-06-26",
  "nawal": { "name": "Tijax", "index": 17, "glyph": "🔪",
             "meaning": "Pedernal · Curación · Corte",
             "message": "Corta lo que ya no sirve. La sanación requiere valentía." },
  "number": { "value": 8, "name": "Wajxaqib'", "meaning": "Justicia · Integridad · Armonía" }
}
```

---

### 5d. ⚡ Calendario Babilónico Sexagesimal

**Ruta**: `/menu/calendarios/sexagesimal`

#### Datos que expone

| Dato | Algoritmo | Tipo |
|------|-----------|------|
| Ciclo planetario actual (1–6) | Módulo 60 desde JDN ref | Calculado |
| Dios/planeta del ciclo (Shamash, Sin, Nergal, Nabu, Marduk, Ishtar) | Tabla | Estático |
| Día dentro del ciclo (1–60) | — | Calculado |
| Década (1–6, de 10 días c/u) | — | Calculado |
| Día del año babilónico (1–360) | — | Calculado |
| ¿Es período Epagómenos? (días 361–365) | — | Calculado |
| Hora en sistema babilónico (Beru/Uš/Ninda) | Reloj en tiempo real | Calculado |
| Coordenadas RA/Dec de 5 estrellas en base 60 | Datos fijos | Estático |

#### Implementación mínima

```javascript
const JDN_REF = 625307  // ~1 enero 3000 a.C.
const CICLOS = ['Shamash','Sin','Nergal','Nabu','Marduk','Ishtar']
const PLANETAS = ['Sol','Luna','Marte','Mercurio','Júpiter','Venus']

function getBabylonianCalendar(date = new Date()) {
  const y = date.getFullYear(), m = date.getMonth()+1, d = date.getDate()
  const a = Math.floor((14-m)/12), yy = y+4800-a, mm = m+12*a-3
  const jdn = d + Math.floor((153*mm+2)/5) + 365*yy + Math.floor(yy/4)
            - Math.floor(yy/100) + Math.floor(yy/400) - 32045

  const total    = jdn - JDN_REF
  const yearPos  = ((total % 365) + 365) % 365
  const dayOf360 = yearPos % 360
  const cycleIdx = Math.floor(dayOf360 / 60) % 6
  const dayInCycle = dayOf360 % 60
  const decade   = Math.floor(dayInCycle / 10)
  const dayInDecade = dayInCycle % 10 + 1
  const isEpagomenos = yearPos >= 360

  // Hora babilónica
  const now = new Date()
  const secs = now.getHours()*3600 + now.getMinutes()*60 + now.getSeconds()

  return {
    cycle: { index: cycleIdx, name: CICLOS[cycleIdx], planet: PLANETAS[cycleIdx] },
    dayInCycle: dayInCycle + 1,
    decade: decade + 1,
    dayInDecade,
    dayOfYear: dayOf360 + 1,
    isEpagomenos,
    babylonianTime: {
      beru:  Math.floor(secs / 7200),       // 1 beru = 2 horas
      ush:   Math.floor((secs % 7200) / 60), // 1 uš = 1 minuto
      ninda: secs % 60                       // 1 ninda = 1 segundo
    }
  }
}
```

### JSON de salida

```json
{
  "date": "2026-06-26",
  "cycle": { "index": 2, "name": "Nergal", "planet": "Marte" },
  "dayInCycle": 23,
  "decade": 3,
  "dayInDecade": 3,
  "dayOfYear": 143,
  "isEpagomenos": false,
  "babylonianTime": { "beru": 10, "ush": 30, "ninda": 45 }
}
```

---

## 6. ✦ MÓDULO: CONSTELACIONES

> **Nota**: Este módulo usa Three.js/React Three Fiber para visualización 3D. No tiene lógica compleja de datos — los datos de posición de estrellas son un catálogo estático + `astronomy-engine` para la orientación del cielo en tiempo real.

### Datos que expone

| Dato | Fuente |
|------|--------|
| Catálogo de constelaciones con estrellas (RA/Dec) | JSON estático |
| Posición del sol (para visibilidad nocturna) | `astronomy-engine` |
| Orientación del cielo local (lat/lon) | Coordenadas del usuario |
| Constelación activa del sol (signo solar) | `astronomy-engine` |

### Implementación mínima (catálogo + posición)

```javascript
import * as Astronomy from 'astronomy-engine'

// Catálogo mínimo — posiciones J2000 (RA en horas, Dec en grados)
const CONSTELLATIONS = [
  { name: 'Orión', stars: [
    { name: 'Betelgeuse', ra: 5.919,  dec:  7.407, mag: 0.42 },
    { name: 'Rigel',      ra: 5.242,  dec: -8.202, mag: 0.18 },
    { name: 'Bellatrix',  ra: 5.419,  dec:  6.350, mag: 1.64 },
  ]},
  { name: 'Escorpio', stars: [
    { name: 'Antares', ra: 16.490, dec: -26.432, mag: 1.06 },
  ]},
  // ... más constelaciones
]

function getSkyOrientation(date = new Date(), lat = 0, lon = 0) {
  const t = Astronomy.MakeTime(date)
  // Tiempo sidéreo local (LST) en horas
  const gst = Astronomy.SiderealTime(t)  // Greenwich Sidereal Time
  const lst = (gst + lon / 15 + 24) % 24 // Local Sidereal Time
  return { lst, sunLongitude: Astronomy.SunPosition(t).elon }
}
```

---

## 🔧 Arquitectura recomendada para el asistente IA

### Opción A — Páginas estáticas scrapeables (más simple)

```
GET https://tu-dominio.com/api/sky-now?lat=-34.6&lon=-58.4
→ JSON con todos los módulos integrados
```

### Opción B — Un endpoint JSON por módulo

```
/api/sky-now      → moon, sun, visible planets, cholqij
/api/astrology    → planet positions, aspects, nodes
/api/weather      → clima Open-Meteo + geocoding
/api/calendars    → tzolkin, babylonian, season
```

### Endpoint "todo en uno" recomendado

```javascript
// Ejecuta en Node.js / Edge / Vercel Function
import * as Astronomy from 'astronomy-engine'

export async function GET(req) {
  const { searchParams } = new URL(req.url)
  const lat  = parseFloat(searchParams.get('lat') || '0')
  const lon  = parseFloat(searchParams.get('lon') || '0')
  const dateStr = searchParams.get('date')
  const date = dateStr ? new Date(dateStr) : new Date()

  const [weatherData] = await Promise.all([
    getWeatherData(lat, lon),  // Open-Meteo
  ])

  return Response.json({
    generated: new Date().toISOString(),
    location: { lat, lon },
    sky: getTodaySkyData(date),
    astrology: { planets: getPlanetPositions(date), aspects: getAspects(...) },
    weather: weatherData,
    calendars: {
      cholqij:    getCholqij(date),
      mayan:      getMayanCalendar(date),
      babylonian: getBabylonianCalendar(date)
    }
  })
}
```

---

## 📦 Dependencias por módulo (npm)

```json
{
  "astronomy-engine": "^2.1.19",
  "node-fetch": "^3.3.2"
}
```

Todo lo demás es JavaScript puro — sin librerías adicionales.

---

## ⚠️ Consideraciones para scraping con IA

1. **Clima**: siempre requiere coordenadas GPS del usuario — no es scrappeable de forma genérica. Cachear 30 min.
2. **Brújula**: es hardware del dispositivo — no se puede replicar en servidor. El cliente debe enviar el dato.
3. **Astronomy-engine**: funciona en Node.js y en el browser — ideal para endpoints serverless.
4. **Calendarios**: 100% matemático, sin APIs externas. Funciona offline.
5. **Nominatim** (geocoding): tiene rate limit de 1 req/seg — usar cacheo agresivo.

---

*Informe generado: Junio 2026 — Archeoscope v1.x*
