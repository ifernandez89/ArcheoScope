# Sistema Climático Dinámico v2.0

Sistema completo de efectos climáticos para ArcheoScope con física realista y efectos visuales avanzados.

## 🌦️ Componentes del Sistema

### 1. WeatherManager
**Archivo:** `components/weather/WeatherManager.tsx`

Gestor central del sistema climático que coordina todos los efectos.

**Características:**
- Estados climáticos: `clear`, `rain`, `storm`, `snow`, `fog`, `wind`
- Transiciones suaves entre estados
- Sistema de eventos para comunicación entre componentes
- Control de frecuencia de rayos en tormentas

**Configuración:**
```typescript
{
  state: WeatherState
  intensity: number // 0-1
  windStrength: number
  fogDensity: number
  lightningFrequency: number // rayos por minuto
  transitionSpeed: number
}
```

---

### 2. WindEffect (Viento)
**Archivo:** `components/weather/WindEffect.tsx`

Sistema de viento con ráfagas y turbulencias.

**Características:**
- Vector de dirección configurable
- Oscilación natural con seno
- Ráfagas periódicas
- Partículas de polvo/hojas
- Sistema de eventos para que otros componentes reaccionen al viento

**Componentes:**
- `WindEffect`: Fuerza del viento (invisible)
- `WindParticles`: Partículas visuales (polvo, hojas)

**Uso:**
```tsx
<WindEffect strength={0.7} direction={[1, 0, 0.5]} gustFrequency={0.5} />
<WindParticles strength={0.7} />
```

---

### 3. LightningEffect (Rayos)
**Archivo:** `components/weather/LightningEffect.tsx`

Sistema de rayos con flash ambiental y geometría procedural.

**Características:**
- Flash ambiental (iluminación global)
- Geometría procedural del rayo con ramificaciones
- Timing realista (flash → trueno con delay)
- Sistema de eventos coordinado con WeatherManager

**Técnicas:**
- Mesh procedural con líneas fractales
- Blend aditivo para efecto brillante
- Fade out suave del flash
- Emissive intensity en materiales de la escena

**Uso:**
```tsx
<LightningEffect enabled={true} intensity={1} />
```

---

### 4. DynamicFog (Niebla)
**Archivo:** `components/weather/DynamicFog.tsx`

Niebla volumétrica con densidad animada.

**Características:**
- Transiciones suaves de densidad
- Animación de pulsación opcional
- Partículas volumétricas para efecto 3D
- Compatible con FogExp2 y Fog de Three.js

**Componentes:**
- `DynamicFog`: Niebla de escena (Three.js fog)
- `FogParticles`: Partículas volumétricas

**Uso:**
```tsx
<DynamicFog density={0.8} color="#b0b0b0" animated={true} />
<FogParticles density={0.8} />
```

---

### 5. TornadoEffect (Tornado)
**Archivo:** `components/weather/TornadoEffect.tsx`

Tornado con partículas en espiral y núcleo oscuro.

**Características:**
- Partículas en movimiento helicoidal
- Radio que crece con la altura (forma de embudo)
- Turbulencia procedural
- Núcleo cilíndrico oscuro
- 2000 partículas en movimiento

**Física:**
```
x = radius * cos(angle + time)
z = radius * sin(angle + time)
y = height
radius = 1 + (height / maxHeight) * 8
```

**Uso:**
```tsx
<TornadoEffect position={[20, 0, 20]} intensity={0.8} height={40} />
```

---

## 🎮 Panel de Control

**Archivo:** `components/WeatherControl.tsx`

Panel UI para activar/desactivar efectos climáticos.

### Categorías:

#### Precipitación
- ❄️ Nieve
- 🌧️ Lluvia Ligera (4,000 partículas)
- 🌧️ Lluvia Moderada (8,000 partículas)
- ⛈️ Lluvia Fuerte (18,000 partículas)

#### Atmósfera
- 🌬️ Viento
- 🌫️ Niebla

#### Fenómenos Extremos
- ⚡ Tormenta Eléctrica (activa lluvia fuerte + rayos)
- 🌪️ Tornado

---

## 🔧 Integración

### En ImmersiveScene.tsx:

```tsx
<WeatherManager
  config={{
    state: determineWeatherState(weather),
    intensity: calculateIntensity(weather),
    windStrength: weather.wind ? 0.7 : 0,
    fogDensity: weather.fog ? 0.8 : 0,
    lightningFrequency: weather.storm ? 12 : 0,
    transitionSpeed: 0.5
  }}
>
  {/* Efectos climáticos aquí */}
</WeatherManager>
```

---

## 📊 Rendimiento

### Optimizaciones:
- Partículas con BufferGeometry (eficiente)
- Depth write desactivado en partículas
- Blending modes optimizados
- Reciclaje de partículas (no se crean/destruyen)
- Sistema de eventos en lugar de props drilling

### Conteo de Partículas:
- Nieve: 2,000
- Lluvia Ligera: 4,000
- Lluvia Moderada: 8,000
- Lluvia Fuerte: 18,000
- Viento: 500
- Niebla: 1,000
- Tornado: 2,000

**Total máximo:** ~35,500 partículas (si todos activos)

---

## 🎨 Efectos Visuales

### Técnicas Utilizadas:

1. **Partículas Procedurales**
   - BufferGeometry con Float32Array
   - Actualización en useFrame
   - Reciclaje de posiciones

2. **Shaders**
   - PointsMaterial con size attenuation
   - Blending modes (Additive, Normal)
   - Transparencias

3. **Física Simulada**
   - Gravedad para lluvia/nieve
   - Movimiento helicoidal para tornado
   - Oscilación senoidal para viento
   - Turbulencia con ruido

4. **Post-processing**
   - Flash ambiental en rayos
   - Emissive intensity en materiales
   - Fog de escena dinámico

---

## 🚀 Futuras Mejoras

### Próximas Implementaciones:
- [ ] Granizo
- [ ] Aurora Boreal
- [ ] Arcoíris
- [ ] Nubes volumétricas
- [ ] Sonidos ambientales
- [ ] Ciclos climáticos automáticos
- [ ] Transiciones día/noche con clima
- [ ] Efectos de viento en vegetación (shader)
- [ ] Charcos y agua acumulada
- [ ] Nieve acumulada en terreno

---

## 📝 Notas Técnicas

### Sistema de Eventos:
El sistema usa CustomEvents del navegador para comunicación:
- `weather:lightning` - Dispara un rayo
- `weather:wind` - Actualiza vector de viento

### Compatibilidad:
- Three.js r150+
- React Three Fiber 8+
- TypeScript 5+

### Biomas:
El sistema respeta los biomas detectados:
- Nieve automática en biomas helados
- Sin efectos por defecto en otros biomas

---

## 🎯 Uso Recomendado

### Para Machu Picchu:
```tsx
weather = {
  rainLight: true,
  fog: true,
  wind: false
}
```

### Para Antártida:
```tsx
weather = {
  snow: true,
  wind: true,
  fog: false
}
```

### Para Tormenta Dramática:
```tsx
weather = {
  storm: true, // Activa lluvia fuerte + rayos automáticamente
  wind: true,
  fog: true
}
```

---

**Versión:** 2.0  
**Última actualización:** 2026-02-18  
**Autor:** ArcheoScope Team
