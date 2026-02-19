# 🎧 Sistema de Audio Profesional

## 🎯 Regla de Oro

**El sonido NO es "reproducir audios"**

Es un AudioSystem desacoplado del ClimateSystem que mezcla capas dinámicamente.

---

## 🏗️ Arquitectura

```
ClimateSystem
    ↓ emite eventos
AudioSystem
    ↓ mezcla capas dinámicamente
Web Audio API
```

### NO hacer
```typescript
❌ if (lluvia) play("rain.mp3")
```

### SÍ hacer
```typescript
✅ ClimateSystem.emit('weather:rain', { intensity: 0.7 })
✅ AudioSystem.updateRain(0.7) // Mezcla capas
```

---

## 🎼 Audio por Capas (Layered Ambience)

### Lluvia (4 capas)
```
rain_base_loop.ogg       // Base continua
rain_droplets_near.ogg   // Gotas cercanas
rain_droplets_far.ogg    // Gotas lejanas
rain_roof_impact.ogg     // Impacto en techo (opcional)
```

### Volumen según intensidad
| Tipo | Ligera | Moderada | Fuerte |
|------|--------|----------|--------|
| Base | 0.2 | 0.5 | 0.9 |
| Near | 0.0 | 0.3 | 0.7 |
| Far | 0.1 | 0.2 | 0.3 |

**Beneficio**: No cambiar archivos, solo volumen

---

## 🌬️ Viento

### Capas
```
wind_low_loop.ogg    // Viento continuo
wind_gust.ogg        // Ráfaga ocasional
```

### Integración con WindSystem
```typescript
// Cuando hay turbulencia alta
if (turbulence > threshold) {
  ClimateAudio.playWindGust(intensity)
}
```

**Beneficio**: Audio conectado con sistema real

---

## ⚡ Rayos / Tormenta

### Simulación Realista
```typescript
// Flash visual
LightningEffect.flash()

// Delay basado en distancia
const delay = distance / 343 // velocidad del sonido m/s

// Trueno
ClimateAudio.playThunder(distance)
```

### Ejemplo
```
Distancia: 1000m
Delay: 2.9s
Volumen: 0.8 (cerca)

Distancia: 5000m
Delay: 14.6s
Volumen: 0.2 (lejos)
```

**Beneficio**: Inmersión brutal

---

## 🌨️ Nieve

### Muy Sutil
```
snow_wind_loop.ogg   // Viento frío
```

**Volumen**: 0.4 máximo

**Por qué**: La nieve real casi no suena

---

## 🌪️ Tornado

### Capas
```
tornado_rumble.ogg       // Rumble bajo
tornado_wind_circular.ogg // Viento circular
tornado_debris.ogg       // Impactos ocasionales
```

**No usar**: Un solo sonido genérico

**Usar**: 2-3 capas mezcladas

---

## 🔧 Implementación Técnica

### Web Audio API (NO Three.js Audio)
```typescript
const context = new AudioContext()
const masterGain = context.createGain()
const ambienceGain = context.createGain()
const fxGain = context.createGain()

// Conectar
ambienceGain.connect(masterGain)
fxGain.connect(masterGain)
masterGain.connect(context.destination)
```

**Por qué Web Audio API**:
- ✅ Más flexible
- ✅ Mejor control de ganancia
- ✅ No depende de Three.js
- ✅ Fades suaves nativos

---

## 🎚️ Fades Suaves (CLAVE)

### NO hacer
```typescript
❌ rainSound.stop()
```

### SÍ hacer
```typescript
✅ fadeOut(rainSound, 2000) // 2 segundos
```

### Implementación
```typescript
// Loop de actualización
setInterval(() => {
  layers.forEach(layer => {
    const diff = layer.targetVolume - layer.currentVolume
    layer.currentVolume += diff * fadeSpeed * delta
    layer.gainNode.gain.value = layer.currentVolume
  })
}, 16) // ~60fps
```

**Beneficio**: Cambia completamente la calidad percibida

---

## 📦 Optimización

### Compresión
- ✅ Usar OGG (mejor compresión que MP3)
- ✅ Loops cortos (10-20s)
- ✅ Bitrate: 96-128 kbps (suficiente para ambiente)

### Lazy Loading
```typescript
// NO cargar todos al inicio
❌ await loadAllSounds()

// SÍ cargar cuando se necesita
✅ if (weather.rain) {
  await loadSound('rain_base')
}
```

### Límites
- ✅ Máximo 4 loops simultáneos
- ✅ Máximo 2 efectos simultáneos
- ✅ Total: ~500KB de audio en memoria

---

## 🎮 Controles (Engine Serio)

### Volúmenes Separados
```typescript
AudioSystem.setMasterVolume(0.7)    // General
AudioSystem.setAmbienceVolume(0.8)  // Ambiente
AudioSystem.setFxVolume(0.6)        // Efectos
```

### Opcional (Avanzado)
```typescript
// Atenuación por distancia
AudioSystem.setDistanceModel('exponential')

// Sonido espacial 3D
AudioSystem.playPositional('thunder', position)
```

---

## 🌍 Audio Arqueológico (ArcheoScope)

### Filosofía
**NO Fortnite. SÍ mundo evolutivo.**

El sonido debe ser:
- ✅ Atmosférico
- ✅ Elegante
- ✅ No invasivo
- ✅ Ambiental

### Características Especiales
```typescript
// Viento cambia tono según presión atmosférica
if (pressure < 1000) {
  windPitch = 0.95 // Más grave antes de tormenta
}

// Sonido anticipa el clima
if (pressureDropping) {
  increaseWindVolume(0.1)
  decreaseAmbienceVolume(0.1)
}
```

**Beneficio**: Diseño sistémico

---

## 📊 Estructura de Archivos

```
public/audio/
├── ambience/
│   ├── rain_base_loop.ogg
│   ├── rain_droplets_near.ogg
│   ├── rain_droplets_far.ogg
│   ├── wind_low_loop.ogg
│   ├── snow_wind_loop.ogg
│   └── tornado_rumble.ogg
│
└── fx/
    ├── wind_gust.ogg
    ├── thunder_1.ogg
    ├── thunder_2.ogg
    └── thunder_3.ogg
```

**Total estimado**: 2-3 MB comprimido

---

## 🚀 Uso en Código

### Inicializar
```typescript
import { getClimateAudio } from '@/systems/ClimateAudioSystem'

const climateAudio = getClimateAudio()
await climateAudio.initialize()
```

### Actualizar Clima
```typescript
// Desde WeatherSystem
climateAudio.updateWeather({
  rain: weather.rainHeavy ? 0.9 : weather.rainModerate ? 0.6 : 0.3,
  wind: weather.wind ? 0.7 : 0,
  snow: weather.snow ? 0.5 : 0
})
```

### Trueno con Distancia
```typescript
// Desde LightningEffect
const distance = 1500 // metros
climateAudio.playThunder(distance)
```

### Ráfaga de Viento
```typescript
// Desde WindSystem cuando turbulence > threshold
if (turbulence > 0.7) {
  climateAudio.playWindGust(turbulence)
}
```

---

## ✅ Checklist de Implementación

- [x] Crear AudioSystem.ts (base)
- [x] Crear ClimateAudioSystem.ts (clima)
- [x] Implementar fades suaves
- [x] Implementar capas por intensidad
- [x] Implementar truenos con delay
- [x] Documentar sistema completo
- [ ] Grabar/conseguir archivos de audio
- [ ] Comprimir a OGG
- [ ] Integrar con WeatherSystem
- [ ] Integrar con WindSystem
- [ ] Integrar con LightningEffect
- [ ] Testear en diferentes climas
- [ ] Ajustar volúmenes

---

## 🎉 Resultado Final

**De "reproducir audios" a sistema de audio profesional**

### Antes
```
❌ if (lluvia) play("rain.mp3")
❌ Sin fades
❌ Sin capas
❌ Sin integración
```

### Después
```
✅ Sistema desacoplado
✅ Audio por capas
✅ Fades suaves
✅ Mezcla dinámica
✅ Integración con clima
✅ Simulación realista
```

**Nivel alcanzado**: Engine serio con audio cinematográfico 🎧

---

## 💡 Próximos Pasos

### Corto Plazo
1. Conseguir/grabar archivos de audio
2. Comprimir a OGG
3. Integrar con WeatherSystem

### Medio Plazo
1. Audio espacial 3D
2. Reverb según entorno
3. Oclusión por objetos

### Largo Plazo
1. Audio procedural
2. Síntesis de sonido
3. Audio adaptativo por bioma

---

**Fecha**: 2026-02-19  
**Estado**: ✅ Arquitectura implementada  
**Archivos**: Pendientes  
**Integración**: Pendiente  
**Filosofía**: Atmosférico, no invasivo
