# LocalWeather Component

## 📱 Clima Local - Solo Mobile

Componente que muestra condiciones del cielo locales en tiempo real, diseñado exclusivamente para dispositivos móviles.

## ✨ Características

### Datos Mostrados
- 🌡 **Temperatura actual** (en °C)
- 🌧 **Probabilidad de lluvia** (en %)
- 🌙 **Fase lunar** (calculada localmente)

### Tecnologías Utilizadas

#### API de Clima: Open-Meteo
- ✅ **Gratuita** - Sin API key requerida
- ✅ **Cobertura global** - Funciona en cualquier lugar del mundo
- ✅ **Rápida y confiable** - Optimizada para PWAs
- ✅ **Sin límites** - Sin restricciones de uso

**Endpoint:**
```
https://api.open-meteo.com/v1/forecast
  ?latitude={LAT}
  &longitude={LON}
  &current=temperature_2m,precipitation_probability
```

#### Geolocalización
Usa la API nativa del navegador:
```javascript
navigator.geolocation.getCurrentPosition()
```

#### Fase Lunar
Calculada localmente usando algoritmo astronómico preciso:
- Ciclo lunar: 29.530588853 días
- Referencia: Luna Nueva del 7 de enero de 1970
- 8 fases: Nueva, Creciente, Cuarto Creciente, Gibosa Creciente, Llena, Gibosa Menguante, Cuarto Menguante, Menguante

## 🎨 Diseño UI

### Vista Compacta (por defecto)
```
┌─────────────────┐
│ ☀ 18°C ▼       │
└─────────────────┘
```

### Vista Expandida (al hacer tap)
```
┌──────────────────────────┐
│ LOCAL SKY CONDITIONS     │
│                          │
│ 🌡 Temperature           │
│    18°C                  │
│                          │
│ 🌧 Rain Probability      │
│    20%                   │
│                          │
│ 🌙 Moon Phase            │
│    Gibosa Creciente      │
│                          │
│ Tap to collapse          │
└──────────────────────────┘
```

## ⚡ Optimización

### Cache Inteligente
- **Duración:** 30 minutos
- **Storage:** localStorage
- **Key:** `archeoscope_local_weather`

### Estrategia de Carga
1. Verificar cache existente
2. Si cache válido → cargar inmediatamente
3. Si cache expirado → solicitar nueva ubicación
4. Obtener clima desde API
5. Guardar en cache

### Performance
- **Primera carga:** ~2-3 segundos (geolocalización + API)
- **Cargas subsecuentes:** Instantáneo (desde cache)
- **Fase lunar:** Cálculo local instantáneo (sin API)

## 🔧 Integración

### Ubicación en el Código
```
viewer3d/
├── components/
│   ├── LocalWeather.tsx          ← Componente principal
│   ├── LocalWeather.README.md    ← Esta documentación
│   └── ImmersiveScene.tsx        ← Integración
```

### Cómo se Integra
```tsx
// En ImmersiveScene.tsx
const LocalWeather = dynamic(() => import('./LocalWeather'), { ssr: false })

// En el return, antes del cierre del div principal
<LocalWeather />
```

## 📱 Detección de Mobile

El componente se auto-oculta en desktop:
```typescript
if (typeof window !== 'undefined' && window.innerWidth > 768) {
  return null
}
```

## 🌍 Ejemplo de Respuesta API

```json
{
  "current": {
    "temperature_2m": 18.4,
    "precipitation_probability": 20
  }
}
```

## 🎯 Casos de Uso

### Perfecto para:
- Jugadores explorando al aire libre
- Sincronización con clima real
- Inmersión narrativa (clima del juego = clima real)
- Planificación de sesiones de juego

### Mejoras Futuras Sugeridas
1. **Iluminación lunar** - Porcentaje de iluminación (0-100%)
2. **Salida/puesta de luna** - Horarios de visibilidad
3. **Sincronización con juego** - Aplicar clima real al mundo 3D
4. **Notificaciones** - Alertas de eventos astronómicos

## 🔐 Privacidad

- ✅ Solo solicita ubicación cuando el usuario abre el juego
- ✅ No almacena coordenadas GPS (solo clima resultante)
- ✅ Cache local (no se envía a servidores externos)
- ✅ API Open-Meteo no requiere autenticación

## 🐛 Manejo de Errores

### Geolocalización Denegada
```typescript
setError('Ubicación no disponible')
// Componente se oculta automáticamente
```

### API No Disponible
```typescript
// Fallback: muestra solo fase lunar
return {
  temperature: 0,
  rainProbability: 0,
  moonPhase: moon.phase,
  moonEmoji: moon.emoji
}
```

## 📊 Datos Técnicos

| Métrica | Valor |
|---------|-------|
| Tamaño del componente | ~6 KB |
| Requests por sesión | 1 (con cache de 30 min) |
| Tiempo de carga | <3s primera vez, instantáneo después |
| Compatibilidad | iOS 10+, Android 5+, todos los navegadores modernos |

## 🎮 Integración con Archeoscope

Este componente encaja perfectamente con la temática del juego:
- **Arqueología + Astronomía** - La fase lunar es clave en muchas culturas antiguas
- **Exploración** - Clima real para exploradores modernos
- **Ciencia** - Datos precisos y verificables
- **Inmersión** - Conexión entre mundo real y virtual

---

**Creado para:** Archeoscope - The Forgotten Relics  
**Versión:** 1.0.0  
**Fecha:** Abril 2026
