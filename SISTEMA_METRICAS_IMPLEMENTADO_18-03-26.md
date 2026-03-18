# Sistema de Métricas de Performance Implementado
**Fecha**: 18 de marzo de 2026
**Rama**: mejorasoptimas

## 🎯 Objetivo

Implementar un sistema completo de monitoreo de performance que mida métricas REALES de usuarios, no estimaciones, para identificar cuellos de botella y optimizar la experiencia.

## 📦 Dependencias Instaladas

```bash
npm install web-vitals stats.js
```

- **web-vitals**: Librería oficial de Google para medir Core Web Vitals
- **stats.js**: Monitor visual de FPS en tiempo real

## 🏗️ Arquitectura Implementada

### 1. Sistema de Web Vitals (Métricas Reales)

**Archivo**: `viewer3d/lib/webVitals.ts`

**Métricas capturadas**:
- **FCP** (First Contentful Paint): Cuándo aparece el primer contenido
- **LCP** (Largest Contentful Paint): Cuándo aparece el contenido principal
- **TTFB** (Time to First Byte): Tiempo de respuesta del servidor
- **CLS** (Cumulative Layout Shift): Estabilidad visual
- **INP** (Interaction to Next Paint): Interactividad real

**Características**:
- ✅ Captura automática de métricas
- ✅ Almacenamiento en localStorage (últimas 100 métricas)
- ✅ Envío a backend vía `/api/metrics`
- ✅ Detección de dispositivo (mobile/tablet/desktop)
- ✅ Detección de ruta actual
- ✅ Rating automático (good/needs-improvement/poor)

**Uso**:
```typescript
import { initWebVitals } from '@/lib/webVitals'

// Inicializar en el layout
useEffect(() => {
  initWebVitals()
}, [])
```

### 2. Sistema de Métricas 3D Personalizadas

**Archivo**: `viewer3d/lib/performance3D.ts`

**Métricas capturadas**:
- Tiempo de carga del motor 3D
- Tiempo de carga de modelos individuales
- FPS promedio
- Tiempo de primer render
- Métricas custom por operación

**Características**:
- ✅ API de Performance nativa
- ✅ Marcas y medidas personalizadas
- ✅ Wrapper para carga de modelos
- ✅ Medición de FPS
- ✅ Almacenamiento en localStorage
- ✅ Resumen estadístico (avg, min, max)

**Uso**:
```typescript
import { mark3D, measure3D, measureModelLoad } from '@/lib/performance3D'

// Marcar inicio
mark3D('operation-start')

// Medir duración
measure3D('operation-complete', 'operation-start', { metadata: 'value' })

// Medir carga de modelo
const model = await measureModelLoad('moai', async () => {
  return await loader.loadAsync('/moai.glb')
})
```

### 3. Monitor Visual de FPS (Stats.js)

**Archivo**: `viewer3d/components/PerformanceStats.tsx`

**Características**:
- ✅ Monitor visual en esquina de pantalla
- ✅ 3 paneles: FPS / MS / MB
- ✅ Click para cambiar panel
- ✅ Solo visible en desarrollo (configurable)
- ✅ Posicionamiento configurable

**Uso**:
```typescript
<PerformanceStats 
  enabled={true} 
  position="top-left" 
/>
```

### 4. API Endpoint para Métricas

**Archivo**: `viewer3d/app/api/metrics/route.ts`

**Endpoints**:
- `POST /api/metrics`: Recibir métricas del cliente
- `GET /api/metrics`: Obtener métricas (solo desarrollo)

**Características**:
- ✅ Validación de datos
- ✅ Almacenamiento en archivo JSONL (desarrollo)
- ✅ Preparado para integración con DB
- ✅ Logs en servidor

**Formato de datos**:
```json
{
  "name": "FCP",
  "value": 1200,
  "rating": "good",
  "route": "/game",
  "device": "desktop",
  "timestamp": 1710777600000
}
```

### 5. Dashboard de Visualización

**Archivo**: `viewer3d/app/metrics/page.tsx`

**Ruta**: `/metrics`

**Características**:
- ✅ Resumen de Web Vitals (avg, min, max)
- ✅ Resumen de métricas 3D
- ✅ Tabla de métricas recientes (últimas 20)
- ✅ Botón de refresh
- ✅ Botón de limpiar métricas
- ✅ Diseño responsive
- ✅ Color coding por rating

**Secciones**:
1. Web Vitals Summary (cards con promedios)
2. 3D Performance Metrics (cards con tiempos)
3. Recent Web Vitals (tabla detallada)
4. Recent 3D Metrics (tabla detallada)

### 6. Integración en Layout

**Archivo**: `viewer3d/app/layout.tsx`

**Componentes agregados**:
- `<WebVitalsInit />`: Inicializa Web Vitals
- `<PerformanceStats />`: Monitor visual de FPS

**Resultado**: Métricas se capturan automáticamente en toda la app

### 7. Integración en Scene3D

**Archivo**: `viewer3d/components/Scene3D.tsx`

**Métricas capturadas**:
- `scene3d-mount`: Cuando el componente se monta
- `scene3d-ready`: Cuando modelo y cámara están listos

**Resultado**: Tiempo de carga del 3D medido automáticamente

## 📊 Métricas Capturadas

### Web Vitals (Automáticas)

| Métrica | Qué mide | Objetivo |
|---------|----------|----------|
| FCP | Primer contenido visible | < 1.8s |
| LCP | Contenido principal visible | < 2.5s |
| TTFB | Respuesta del servidor | < 600ms |
| CLS | Estabilidad visual | < 0.1 |
| INP | Interactividad | < 200ms |

### Métricas 3D (Personalizadas)

| Métrica | Qué mide | Objetivo |
|---------|----------|----------|
| scene3d-ready | Carga completa del 3D | < 2s |
| model-load-* | Carga de modelo específico | Varía |
| fps-measurement | FPS promedio | 50-60 |
| 3d-first-frame | Primer frame renderizado | < 2s |

## 🔍 Cómo Usar el Sistema

### 1. Ver Métricas en Tiempo Real

**Desarrollo**:
1. Iniciar app: `npm run dev`
2. Abrir navegador
3. Ver console: Métricas se loggean automáticamente
4. Ver esquina superior izquierda: Monitor de FPS

**Dashboard**:
1. Navegar a `/metrics`
2. Ver resumen de todas las métricas
3. Refrescar para actualizar
4. Limpiar para resetear

### 2. Capturar Métricas Custom

```typescript
import { mark3D, measure3D } from '@/lib/performance3D'

// En tu componente
useEffect(() => {
  mark3D('my-operation-start')
  
  // ... hacer algo pesado ...
  
  measure3D('my-operation', 'my-operation-start', {
    customData: 'value'
  })
}, [])
```

### 3. Medir Carga de Modelos

```typescript
import { measureModelLoad } from '@/lib/performance3D'

const model = await measureModelLoad('pyramid', async () => {
  const loader = await getGLTFLoader()
  return await loader.loadAsync('/pyramid.glb')
})

// Métrica automáticamente guardada como "model-load-pyramid"
```

### 4. Medir FPS

```typescript
import { measureFPS } from '@/lib/performance3D'

// Medir FPS durante 1 segundo
const fps = await measureFPS(1000)
console.log(`FPS: ${fps}`)
```

### 5. Analizar Métricas

```typescript
import { getMetricsSummary } from '@/lib/webVitals'
import { get3DSummary } from '@/lib/performance3D'

// Obtener resumen
const webVitals = getMetricsSummary()
const metrics3D = get3DSummary()

console.log('FCP promedio:', webVitals.fcp.avg)
console.log('Carga 3D promedio:', metrics3D['scene3d-ready']?.avg)
```

## 📈 Datos Recopilados

### Almacenamiento Local

**localStorage**:
- `archeoscope_metrics`: Web Vitals (últimas 100)
- `archeoscope_3d_metrics`: Métricas 3D (últimas 100)

**Archivo** (desarrollo):
- `metrics.jsonl`: Todas las métricas enviadas al servidor

### Formato de Almacenamiento

**Web Vitals**:
```json
{
  "name": "LCP",
  "value": 2100,
  "rating": "good",
  "delta": 2100,
  "id": "v3-1710777600000-1234567890",
  "navigationType": "navigate",
  "route": "/game",
  "device": "desktop",
  "timestamp": 1710777600000
}
```

**Métricas 3D**:
```json
{
  "name": "model-load-moai",
  "value": 850,
  "timestamp": 1710777600000,
  "metadata": {
    "modelName": "moai"
  }
}
```

## 🎯 Próximos Pasos

### Análisis de Datos

1. **Identificar Cuellos de Botella**:
   - Revisar métricas en `/metrics`
   - Identificar operaciones lentas
   - Priorizar optimizaciones

2. **Correlaciones**:
   - FPS vs modelos cargados
   - LCP vs dispositivo
   - Tiempo de carga vs ruta

3. **Optimizaciones Dirigidas**:
   - Optimizar modelos lentos
   - Mejorar rutas lentas
   - Ajustar para dispositivos específicos

### Integraciones Futuras

1. **Base de Datos**:
   - Guardar métricas en DB
   - Análisis histórico
   - Tendencias a largo plazo

2. **Analytics**:
   - Google Analytics
   - Vercel Analytics
   - Custom dashboard

3. **Alertas**:
   - Notificar si métricas empeoran
   - Threshold automáticos
   - Monitoreo continuo

## 🚀 Beneficios

### Antes (Estimaciones)
- ❌ Métricas teóricas
- ❌ No sabemos qué ven usuarios reales
- ❌ Optimizaciones a ciegas

### Después (Métricas Reales)
- ✅ Datos de usuarios reales
- ✅ Identificación precisa de problemas
- ✅ Optimizaciones basadas en datos
- ✅ Monitoreo continuo
- ✅ Validación de mejoras

## 📝 Archivos Creados

1. `viewer3d/lib/webVitals.ts` - Sistema de Web Vitals
2. `viewer3d/lib/performance3D.ts` - Métricas 3D personalizadas
3. `viewer3d/components/PerformanceStats.tsx` - Monitor visual FPS
4. `viewer3d/components/WebVitalsInit.tsx` - Inicializador
5. `viewer3d/app/api/metrics/route.ts` - API endpoint
6. `viewer3d/app/metrics/page.tsx` - Dashboard de visualización

## 📝 Archivos Modificados

1. `viewer3d/app/layout.tsx` - Integración de Web Vitals y Stats
2. `viewer3d/components/Scene3D.tsx` - Métricas de carga 3D
3. `viewer3d/package.json` - Dependencias agregadas

## ✅ Estado

**Sistema completamente funcional**:
- ✅ Web Vitals capturando métricas reales
- ✅ Métricas 3D personalizadas funcionando
- ✅ Monitor FPS visible en desarrollo
- ✅ Dashboard de visualización operativo
- ✅ API endpoint recibiendo datos
- ✅ Almacenamiento local funcionando
- ✅ Build exitoso sin errores

**Listo para**:
- Análisis de performance real
- Identificación de cuellos de botella
- Optimizaciones basadas en datos
- Monitoreo continuo

---

**Conclusión**: Sistema de métricas de nivel PRO implementado. Ahora podemos medir performance REAL de usuarios y optimizar basándonos en datos concretos, no estimaciones.
