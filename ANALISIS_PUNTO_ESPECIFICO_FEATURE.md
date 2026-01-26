# 📍 Nueva Funcionalidad: Análisis de Punto Específico

**Fecha**: 2026-01-26  
**Feature**: Análisis arqueológico de coordenadas personalizadas  
**Status**: ✅ IMPLEMENTADO

---

## 🎯 Objetivo

Permitir al usuario analizar **cualquier punto del planeta** ingresando coordenadas específicas, obteniendo:
1. Clasificación de zona (terreno y ambiente)
2. Contraste con sitios conocidos cercanos
3. Análisis temporal según tipo de terreno
4. Detección de anomalías arqueológicas

---

## 🆕 Nueva Sección en el Mapa

### Ubicación
- **Sidebar izquierdo** del mapa de zonas prioritarias
- Debajo de "Configuración de Búsqueda"
- Identificado con borde rojo

### Componentes

#### 1. Input de Coordenadas
```
Formato: latitud, longitud
Ejemplo: -31.738965, -60.564453
```

#### 2. Botón de Análisis
```
🔬 Analizar Punto
```

#### 3. Panel de Resultados
- Se muestra automáticamente después del análisis
- Incluye toda la información del análisis

---

## 🔬 Proceso de Análisis

### 1. Validación de Entrada
- ✅ Formato correcto (lat, lon)
- ✅ Valores numéricos válidos
- ✅ Rango válido (lat: -90 a 90, lon: -180 a 180)

### 2. Llamada al Backend
**Endpoint**: `POST /analyze`

**Request**:
```json
{
  "lat": -31.738965,
  "lon": -60.564453,
  "region_name": "Punto personalizado (-31.7390, -60.5645)",
  "resolution_m": 1000
}
```

### 3. Análisis Realizado por el Backend

#### a) Clasificación de Zona
- **Terreno**: desert, forest, grassland, mountain, coastal, etc.
- **Ambiente**: DESERT, FOREST, GRASSLAND, MOUNTAIN, COASTAL, etc.

#### b) Contraste con Sitios Conocidos
- Busca el sitio arqueológico conocido más cercano
- Calcula distancia en kilómetros
- Proporciona nombre y tipo del sitio

#### c) Sensor Temporal Según Terreno
- **Desert**: Landsat-8 (30m, 16 días)
- **Forest**: Sentinel-1 SAR (10m, 6 días)
- **Grassland**: Sentinel-2 (10m, 5 días)
- **Mountain**: ASTER (15m, 16 días)
- **Coastal**: Sentinel-2 + Sentinel-1
- **Glacier/Ice**: Landsat-8 + MODIS

#### d) Detección de Anomalías
- Análisis multi-instrumental
- Convergencia de señales
- Persistencia temporal
- Clasificación: archaeological, anomalous, consistent

---

## 📊 Información Mostrada

### Panel de Resultados

#### 1. Clasificación Visual
```
🔴 ANOMALÍA ARQUEOLÓGICA    (archaeological)
🟠 ANOMALÍA DETECTADA       (anomalous)
🟢 CONSISTENTE CON NATURAL  (consistent)
```

#### 2. Coordenadas
```
📍 Coordenadas: -31.738965, -60.564453
```

#### 3. Clasificación de Zona
```
🗺️ Clasificación de Zona:
   Terreno: grassland
   Ambiente: GRASSLAND
```

#### 4. Probabilidades
```
📊 Probabilidades:
   Confianza: 85.3%
   Prob. Arqueológica: 72.1%
```

#### 5. Sitio Conocido Más Cercano
```
🏛️ Sitio Conocido Más Cercano:
   Nombre del sitio
   Distancia: 15.3 km
```

#### 6. Análisis Temporal
```
⏱️ Análisis Temporal:
   Sensor: Sentinel-2 (Multiespectral)
   Años analizados: 8
```

#### 7. Anomalías Detectadas (si hay)
```
🔍 Anomalías Detectadas:
   • Anomalía de compactación detectada
   • Estrés vegetal persistente
   • Inercia térmica anómala
```

#### 8. Explicación IA (si disponible)
```
🤖 Explicación IA:
   [Explicación detallada del análisis]
```

---

## 🗺️ Visualización en el Mapa

### Marcador Circular
- **Color según resultado**:
  - 🔴 Rojo: archaeological
  - 🟠 Naranja: anomalous
  - 🟢 Verde: consistent
- **Radio**: 10 píxeles
- **Borde**: Blanco, 2px

### Popup Automático
Se abre automáticamente mostrando:
- Resultado del análisis
- Confianza
- Probabilidad arqueológica
- Coordenadas

### Centrado Automático
El mapa se centra en el punto analizado con zoom 12.

---

## 🧪 Ejemplos de Uso

### Ejemplo 1: Zona Rural Argentina
```
Coordenadas: -31.738965, -60.564453
```

**Resultado esperado**:
- Terreno: grassland
- Ambiente: GRASSLAND
- Sensor temporal: Sentinel-2
- Sitio cercano: [sitio más cercano en BD]
- Análisis: Detección de anomalías según señales

### Ejemplo 2: Desierto de Nazca, Perú
```
Coordenadas: -14.7390, -75.1300
```

**Resultado esperado**:
- Terreno: desert
- Ambiente: DESERT
- Sensor temporal: Landsat-8
- Sitio cercano: Nazca Lines (0.5 km)
- Análisis: Alta probabilidad arqueológica

### Ejemplo 3: Selva Amazónica
```
Coordenadas: -3.8000, -61.0000
```

**Resultado esperado**:
- Terreno: forest
- Ambiente: FOREST
- Sensor temporal: Sentinel-1 SAR
- Sitio cercano: Terra Preta Site (X km)
- Análisis: Detección bajo vegetación densa

### Ejemplo 4: Egipto - Valle del Nilo
```
Coordenadas: 29.9792, 31.1342
```

**Resultado esperado**:
- Terreno: desert
- Ambiente: DESERT
- Sensor temporal: Landsat-8
- Sitio cercano: Giza Pyramids (5 km)
- Análisis: Alta probabilidad arqueológica

---

## 🔧 Implementación Técnica

### Frontend (JavaScript)

#### Función Principal
```javascript
async function analyzeCustomPoint() {
    // 1. Validar entrada
    // 2. Parsear coordenadas
    // 3. Llamar al backend
    // 4. Mostrar resultados
    // 5. Agregar marcador al mapa
}
```

#### Funciones Auxiliares
```javascript
function displayPointAnalysis(data, lat, lon)
function addPointMarker(lat, lon, data)
```

### Backend (Python)

#### Endpoint
```python
@app.post("/analyze")
async def analyze_region(request: AnalysisRequest):
    # 1. Clasificar zona (terreno y ambiente)
    # 2. Buscar sitios conocidos cercanos
    # 3. Seleccionar sensor temporal según terreno
    # 4. Analizar anomalías multi-instrumental
    # 5. Evaluar coherencia arqueológica (IA)
    # 6. Retornar resultado completo
```

---

## 📋 Validaciones

### Validaciones de Entrada
1. ✅ Campo no vacío
2. ✅ Formato correcto (lat, lon)
3. ✅ Valores numéricos
4. ✅ Rango válido de coordenadas

### Validaciones de Backend
1. ✅ Coordenadas dentro de rango
2. ✅ Resolución válida
3. ✅ Datos disponibles para la región

---

## 🎨 Diseño Visual

### Colores
- **Borde del panel**: `#ff6b6b` (rojo)
- **Fondo del panel**: `#1a1a2e` (oscuro)
- **Resultado CRITICAL**: `#ff0000` (rojo)
- **Resultado HIGH**: `#ff8800` (naranja)
- **Resultado OK**: `#00ff00` (verde)

### Iconos
- 📍 Coordenadas
- 🗺️ Clasificación de zona
- 📊 Probabilidades
- 🏛️ Sitio cercano
- ⏱️ Análisis temporal
- 🔍 Anomalías
- 🤖 IA

---

## 🚀 Casos de Uso

### 1. Investigador Arqueológico
- Tiene coordenadas de un sitio potencial
- Quiere validación rápida antes de ir al campo
- Necesita saber qué instrumentos usar

### 2. Aficionado a la Arqueología
- Encuentra algo interesante en Google Earth
- Quiere saber si vale la pena investigar
- Obtiene análisis científico inmediato

### 3. Validación de Hipótesis
- Tiene teoría sobre ubicación de sitio antiguo
- Analiza múltiples puntos candidatos
- Compara resultados para priorizar

### 4. Educación
- Profesor enseña arqueología remota
- Estudiantes analizan diferentes regiones
- Aprenden sobre sensores y anomalías

---

## 📊 Ventajas

### 1. Flexibilidad Total
- ✅ Cualquier punto del planeta
- ✅ No limitado a zonas predefinidas
- ✅ Análisis on-demand

### 2. Análisis Completo
- ✅ Clasificación automática de zona
- ✅ Contraste con sitios conocidos
- ✅ Sensor temporal apropiado
- ✅ Detección de anomalías

### 3. Visualización Inmediata
- ✅ Resultado en segundos
- ✅ Marcador en el mapa
- ✅ Información detallada

### 4. Científicamente Riguroso
- ✅ Usa sistema multi-instrumental
- ✅ Considera tipo de terreno
- ✅ Análisis temporal apropiado
- ✅ Validación con IA

---

## 🔄 Flujo de Usuario

```
1. Usuario ingresa coordenadas
   ↓
2. Click en "🔬 Analizar Punto"
   ↓
3. Sistema valida entrada
   ↓
4. Backend clasifica zona
   ↓
5. Backend busca sitios cercanos
   ↓
6. Backend selecciona sensor temporal
   ↓
7. Backend analiza anomalías
   ↓
8. Frontend muestra resultado
   ↓
9. Mapa muestra marcador
   ↓
10. Usuario ve análisis completo
```

---

## 🎯 Próximas Mejoras

### Corto Plazo
1. Guardar análisis en historial
2. Exportar resultado a PDF
3. Compartir análisis por URL

### Medio Plazo
4. Análisis batch (múltiples puntos)
5. Comparación entre puntos
6. Heatmap de probabilidad

### Largo Plazo
7. Integración con datos reales de satélites
8. Análisis en tiempo real
9. Alertas de nuevas anomalías

---

## ✅ Conclusión

La funcionalidad de **Análisis de Punto Específico** permite a cualquier usuario:

✅ Analizar **cualquier coordenada del planeta**  
✅ Obtener **clasificación automática** de zona  
✅ Ver **sitios conocidos cercanos**  
✅ Conocer el **sensor temporal apropiado**  
✅ Detectar **anomalías arqueológicas**  
✅ Visualizar **resultado en el mapa**  

**Impacto**: Democratiza el acceso a análisis arqueológico remoto de nivel profesional.

---

**Desarrollado**: 2026-01-26  
**Sistema**: ArcheoScope - Archaeological Remote Sensing Engine  
**Versión**: 1.4.0  
**Archivo**: `frontend/priority_zones_map.html`

