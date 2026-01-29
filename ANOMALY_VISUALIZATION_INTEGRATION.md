# 🗺️ INTEGRACIÓN VISUALIZACIÓN DE ANOMALÍAS
## Fecha: 2026-01-29

---

## 📋 RESUMEN

Sistema de visualización en tiempo real de mapas de anomalía multifuente.

**Objetivo**: Mostrar inmediatamente después del análisis una síntesis espacial que responde:
> "¿Dónde coinciden espacialmente señales físicas que no deberían coincidir en un entorno natural?"

---

## 🧠 CONCEPTO CLAVE

### NO es:
- ❌ Una foto satelital real
- ❌ Una imagen RGB natural
- ❌ Una "prueba" de presencia arqueológica

### SÍ es:
- ✅ Síntesis espacial multifuente
- ✅ Visualización de convergencia de anomalías
- ✅ Mapa científico normalizado

---

## 🧩 INSTRUMENTOS EN LA IMAGEN

| Fuente | Qué aporta | Peso (árido) |
|--------|------------|--------------|
| **SAR** (Sentinel-1/PALSAR) | Textura, linealidad, bordes enterrados | 40% |
| **Thermal** (Landsat/MODIS/ERA5) | Inercia térmica anómala | 40% |
| **ICESat-2** | Micro-relieve / rugosidad | 15% |
| **DEM** (SRTM/Copernicus) | Pendientes no naturales | 5% |
| **NDVI** | Solo contextual (exclusión) | - |

---

## 🧪 PIPELINE DE GENERACIÓN

### 1️⃣ Rasterización Común
- Misma grilla
- Misma resolución lógica (30-50m)
- Cada fuente → mapa de anomalía normalizado

```
A_sar(x,y)
A_thermal(x,y)
A_rugosity(x,y)
A_slope(x,y)
```

### 2️⃣ Normalización por Contexto
**CLAVE**: Regional, NO global

```python
A_norm = (valor - media_regional) / std_regional
```

### 3️⃣ Fusión Ponderada (Environment-Aware)
```python
ANOMALY_MAP(x,y) = 
    w_sar * A_sar +
    w_thermal * A_thermal +
    w_rugosity * A_rugosity +
    w_slope * A_slope
```

Pesos dependen de `environment_type`.

### 4️⃣ Realce Estructural
- Detección de bordes (Sobel)
- Coherencia espacial
- Filtros morfológicos

**Resultado**: Aparecen rectángulos, alineaciones, plataformas, trazas lineales

---

## 🎨 VISUALIZACIÓN

### Colormap Científico
- 🔵 **Azul**: Fondo natural (bajo)
- 🟡 **Amarillo**: Anomalía débil (medio)
- 🔴 **Rojo**: Convergencia multifuente fuerte (alto)
- ⚪ **Blanco**: Features geométricas detectadas

### Overlay
- Contornos blancos = detección geométrica
- DEM suave opcional

---

## 🔥 VALOR CIENTÍFICO

### Declaración Correcta
> "No afirmamos presencia arqueológica. Visualizamos la convergencia espacial de anomalías físicas compatibles con intervención humana enterrada."

### Lenguaje Ético
**NUNCA decir**:
- ❌ "estructura"
- ❌ "ruina"
- ❌ "edificio"

**SIEMPRE decir**:
- ✅ "anomalía estructurada"
- ✅ "patrón no natural"
- ✅ "firma compatible"

---

## 🛠️ IMPLEMENTACIÓN

### Backend

#### 1. Generador de Mapas
**Archivo**: `backend/anomaly_map_generator.py`

**Clases**:
- `AnomalyLayer` - Capa individual
- `AnomalyMap` - Mapa fusionado
- `AnomalyMapGenerator` - Generador principal

**Métodos principales**:
```python
generate_anomaly_map(measurements, lat_min, lat_max, lon_min, lon_max, environment_type)
export_to_png(anomaly_map, output_path)
```

#### 2. API Endpoint
**Archivo**: `backend/api/anomaly_visualization_endpoint.py`

**Endpoints**:
- `POST /api/generate-anomaly-map` - Generar mapa desde análisis
- `GET /api/anomaly-map/{analysis_id}` - Obtener mapa existente
- `GET /api/anomaly-map/{analysis_id}/png` - Descargar PNG

### Frontend

#### 3. Visor de Mapas
**Archivo**: `frontend/anomaly_map_viewer.js`

**Clase**: `AnomalyMapViewer`

**Features**:
- Visualización automática post-análisis
- Colormap científico
- Overlay de features geométricas
- Controles de opacidad y capas
- Descarga PNG
- Metadata científica

**Uso**:
```javascript
const viewer = new AnomalyMapViewer('map-container');

// Después del análisis
viewer.generateAndLoadMap({
    analysis_id: analysisId,
    measurements: measurements,
    lat_min: lat_min,
    lat_max: lat_max,
    lon_min: lon_min,
    lon_max: lon_max,
    environment_type: 'arid',
    resolution_m: 30.0
});
```

---

## 🔗 INTEGRACIÓN CON PIPELINE EXISTENTE

### En `backend/scientific_pipeline.py`

Agregar al final de `analyze_candidate()`:

```python
# FASE H: Generar mapa de anomalía
from anomaly_map_generator import AnomalyMapGenerator

generator = AnomalyMapGenerator(resolution_m=30.0)

anomaly_map = generator.generate_anomaly_map(
    measurements=raw_measurements,
    lat_min=lat_min,
    lat_max=lat_max,
    lon_min=lon_min,
    lon_max=lon_max,
    environment_type=environment_type
)

# Guardar en output
output.anomaly_map_metadata = {
    'layers_used': anomaly_map.layers_used,
    'resolution_m': anomaly_map.resolution_m,
    'anomaly_mean': anomaly_map.metadata['anomaly_mean'],
    'anomaly_max': anomaly_map.metadata['anomaly_max'],
    'geometric_features_count': anomaly_map.metadata['geometric_features_count']
}

# Exportar PNG
output_path = f"anomaly_maps/{candidate_id}.png"
generator.export_to_png(anomaly_map, output_path)
output.anomaly_map_path = output_path
```

### En Frontend (index.html o main app)

Agregar después de mostrar resultados:

```javascript
// Cargar visor de mapas
const mapViewer = new AnomalyMapViewer('anomaly-map-container');

// Cuando llega resultado del análisis
fetch('/api/analyze', {
    method: 'POST',
    body: JSON.stringify(analysisRequest)
})
.then(response => response.json())
.then(result => {
    // Mostrar resultados normales
    displayResults(result);
    
    // Generar y mostrar mapa de anomalía
    mapViewer.generateAndLoadMap({
        analysis_id: result.candidate_id,
        measurements: result.measurements,
        lat_min: result.lat_min,
        lat_max: result.lat_max,
        lon_min: result.lon_min,
        lon_max: result.lon_max,
        environment_type: result.environment_type,
        resolution_m: 30.0
    });
});
```

---

## 🧪 TEST

### Test Backend
```bash
python backend/anomaly_map_generator.py
```

**Output esperado**:
```
🗺️ Anomaly Map Generator - Test
================================================================================
✅ Mapa generado:
   Shape: (100, 100)
   Layers: ['sar', 'thermal', 'rugosity', 'slope']
   Anomaly range: [0.123, 0.876]
   Geometric features: 234 pixels
💾 Mapa exportado: test_anomaly_map.png
================================================================================
✅ Test completado
```

### Test Frontend
Abrir `frontend/test_anomaly_viewer.html` en navegador.

---

## 📊 IMPACTO UX

### ANTES
```
Usuario: "¿Dónde está la anomalía?"
Sistema: "Score: 0.73"
Usuario: "¿Y eso qué significa?"
```

### DESPUÉS
```
Usuario: "¿Dónde está la anomalía?"
Sistema: [Muestra mapa visual]
Usuario: "¡Ah! Veo la convergencia en el centro"
```

**Mejora**: El cerebro humano entiende patrones visuales mejor que scores numéricos.

---

## 🚀 PRÓXIMOS PASOS

### Inmediato
1. ✅ Módulos creados
2. 📋 Integrar en pipeline principal
3. 📋 Registrar endpoint en FastAPI
4. 📋 Agregar visor a frontend principal

### Corto plazo
5. 📋 Test con datos reales
6. 📋 Optimizar performance (cache, compresión)
7. 📋 Agregar más controles (zoom, pan)

### Medio plazo
8. 📋 CNNs para clasificar mapas generados
9. 📋 Comparación con sitios conocidos
10. 📋 Exportar a GeoTIFF

---

## 📝 ARCHIVOS CREADOS

### Backend
- `backend/anomaly_map_generator.py` (✅ funcional)
- `backend/api/anomaly_visualization_endpoint.py` (✅ funcional)

### Frontend
- `frontend/anomaly_map_viewer.js` (✅ funcional)

### Documentación
- `ANOMALY_VISUALIZATION_INTEGRATION.md` (este archivo)

---

## 🎯 CONCLUSIÓN

**Estado**: Módulos funcionales, pendiente integración en pipeline principal

**Valor**: Visualización inmediata post-análisis mejora dramáticamente la UX y validación científica

**Próximo paso crítico**: Integrar en `scientific_pipeline.py` y registrar endpoint en FastAPI

**Tiempo estimado**: 1-2 horas para integración completa

---

**Fecha**: 2026-01-29  
**Autor**: Kiro AI Assistant  
**Versión**: 1.0
