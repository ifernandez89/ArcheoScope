# 🔥 Guía de Visualización de Zonas Calientes - ArcheoScope

**Fecha:** 2026-01-26  
**Versión:** 1.0.0  
**Estado:** ✅ OPERATIVO

---

## 📋 Descripción

Sistema de visualización interactiva de **zonas calientes** (hot zones) para análisis arqueológico prioritario. Permite identificar y filtrar regiones con alto potencial arqueológico basándose en:

- Densidad de sitios conocidos
- Tipo de terreno (bosque, desierto, montaña, etc.)
- Disponibilidad de LiDAR
- Scoring multi-criterio

---

## 🚀 Acceso Rápido

### URLs:
- **Mapa de Zonas Prioritarias:** http://localhost:8080/priority_zones_map.html
- **API Backend:** http://localhost:8002
- **Swagger Docs:** http://localhost:8002/docs

### Comandos:
```bash
# Levantar backend
python run_archeoscope.py

# Levantar frontend
python start_frontend.py
```

---

## 🗺️ Características del Mapa

### 1. Filtros Disponibles

#### Por Región:
- **Presets rápidos:**
  - 📍 Petén, Guatemala (16-18°N, 91-89°W)
  - 📍 Valle del Nilo, Egipto (25-27°N, 31-33°E)
  - 📍 Valle Sagrado, Perú (14-12°S, 73-71°W)
- **Personalizado:** Ingresar coordenadas manualmente

#### Por Tipo de Terreno:
- 🌳 **FOREST** - Bosque/Selva
- 🏜️ **DESERT** - Desierto
- ⛰️ **MOUNTAIN** - Montaña
- 🏖️ **COASTAL** - Costero
- 🌾 **SEMI_ARID** - Semi-árido

#### Por Estrategia:
- **Buffer** - Anillos alrededor de sitios conocidos (RECOMENDADO)
- **Grid** - Cuadrícula uniforme
- **Density** - Por densidad cultural

#### Opciones Adicionales:
- ✅ Priorizar zonas con LiDAR disponible
- Máximo de zonas (10-200)

---

## 🎨 Código de Colores

### Prioridad de Zonas:
- 🔴 **CRITICAL** - Máxima prioridad (score > 0.7)
- 🟠 **HIGH** - Alta prioridad (score 0.5-0.7)
- 🟡 **MEDIUM** - Media prioridad (score 0.3-0.5)
- 🟢 **LOW** - Baja prioridad (score < 0.3)

### Opacidad:
- Relleno: 40% (permite ver mapa base)
- Borde: 80% (delimita claramente la zona)

---

## 📊 Panel de Estadísticas

El sidebar muestra en tiempo real:

### Resumen General:
- Total de zonas generadas
- Sitios arqueológicos analizados

### Por Prioridad:
- Cantidad de zonas CRITICAL
- Cantidad de zonas HIGH
- Cantidad de zonas MEDIUM
- Cantidad de zonas LOW

### Por Terreno:
- Distribución de zonas por tipo de ambiente
- Iconos visuales para cada tipo

---

## 🔍 Interacción con el Mapa

### Click en Zona:
Muestra popup con:
- **ID de zona**
- **Prioridad y score**
- **Tipo de terreno**
- **Área en km²**
- **Disponibilidad de LiDAR**
- **Sitios cercanos**
- **Botón "Analizar Zona"** (próximamente)

### Lista de Zonas:
- Ordenadas por score (mayor a menor)
- Click para hacer zoom a la zona
- Código de color por prioridad

---

## 🛠️ API Endpoints

### 1. Generar Zonas (GeoJSON)

```http
GET /archaeological-sites/recommended-zones-geojson
```

**Parámetros:**
- `lat_min`, `lat_max`, `lon_min`, `lon_max` (required) - Bounding box
- `strategy` (optional) - buffer, grid, density (default: buffer)
- `max_zones` (optional) - Máximo de zonas (default: 100)
- `lidar_priority` (optional) - Priorizar LiDAR (default: true)

**Ejemplo:**
```bash
curl "http://localhost:8002/archaeological-sites/recommended-zones-geojson?\
lat_min=16&lat_max=18&lon_min=-91&lon_max=-89&\
strategy=buffer&max_zones=50&lidar_priority=true"
```

**Respuesta:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon, lat], ...]]
      },
      "properties": {
        "zone_id": "HZ_000001",
        "priority_score": 0.650,
        "priority_class": "HIGH",
        "environment_type": "FOREST",
        "area_km2": 25.5,
        "lidar_available": true,
        "nearby_sites_count": 12
      }
    }
  ],
  "metadata": {
    "total_zones": 50,
    "strategy": "buffer",
    "generated_at": "2026-01-26T..."
  }
}
```

---

## 📈 Algoritmo de Scoring

### Factores Considerados:

1. **Densidad Cultural (40%)**
   - Proximidad a sitios conocidos
   - Concentración de hallazgos

2. **Disponibilidad de LiDAR (30%)**
   - GOLD CLASS: LiDAR + no excavado
   - SILVER: LiDAR disponible
   - BRONZE: Sin LiDAR

3. **Tipo de Terreno (20%)**
   - Bosque: Alta prioridad (difícil acceso)
   - Desierto: Media prioridad (buena visibilidad)
   - Montaña: Media prioridad (terrazas)

4. **Área de Análisis (10%)**
   - Zonas pequeñas: Más rápido
   - Zonas grandes: Más cobertura

### Fórmula:
```
score = (density * 0.4) + (lidar * 0.3) + (terrain * 0.2) + (area * 0.1)
```

---

## 🎯 Casos de Uso

### 1. Exploración de Nueva Región
```
1. Seleccionar preset o ingresar coordenadas
2. Estrategia: Buffer
3. Filtro terreno: Todos
4. Generar zonas
5. Revisar zonas HIGH/CRITICAL
6. Analizar zonas prioritarias
```

### 2. Búsqueda en Bosque Denso
```
1. Región: Petén, Guatemala
2. Filtro terreno: FOREST
3. LiDAR priority: ✅ Activado
4. Generar zonas
5. Enfocarse en zonas con LiDAR
```

### 3. Análisis de Desierto
```
1. Región: Valle del Nilo
2. Filtro terreno: DESERT
3. Estrategia: Density
4. Generar zonas
5. Priorizar zonas CRITICAL
```

---

## 📝 Flujo de Trabajo Recomendado

### Fase 1: Exploración (5-10 min)
1. Cargar región de interés
2. Generar zonas con estrategia Buffer
3. Revisar distribución de prioridades
4. Identificar zonas CRITICAL/HIGH

### Fase 2: Filtrado (2-5 min)
1. Aplicar filtro por terreno
2. Activar prioridad LiDAR si aplica
3. Ajustar máximo de zonas
4. Regenerar

### Fase 3: Análisis (variable)
1. Click en zonas prioritarias
2. Revisar metadata
3. Exportar coordenadas
4. Planificar análisis detallado

---

## 🔧 Configuración Técnica

### Frontend:
- **Framework:** Leaflet.js 1.9.4
- **Tiles:** OpenStreetMap
- **Puerto:** 8080
- **Archivo:** `frontend/priority_zones_map.html`

### Backend:
- **Framework:** FastAPI
- **Puerto:** 8002
- **Endpoint:** `/archaeological-sites/recommended-zones-geojson`
- **Base de datos:** PostgreSQL (80,512 sitios)

### Rendimiento:
- Generación de zonas: ~2-5 segundos
- Renderizado mapa: <1 segundo
- Filtrado: Instantáneo (client-side)

---

## 🐛 Troubleshooting

### Problema: No se generan zonas
**Solución:**
- Verificar que backend esté corriendo (http://localhost:8002/docs)
- Revisar coordenadas (lat_min < lat_max, lon_min < lon_max)
- Aumentar `max_zones`

### Problema: Filtro por terreno no funciona
**Solución:**
- Verificar que los sitios en la región tengan `environmentType`
- Regenerar zonas después de cambiar filtro
- Revisar consola del navegador (F12)

### Problema: Mapa no carga
**Solución:**
- Verificar frontend en http://localhost:8080
- Limpiar caché del navegador
- Revisar consola para errores CORS

---

## 📚 Recursos Adicionales

### Documentación:
- **API Swagger:** http://localhost:8002/docs
- **Guía de Base de Datos:** `DATABASE_SUMMARY.md`
- **Guía de Candidatas Reales:** `HARVEST_REPORT_2026-01-25.md`

### Scripts Relacionados:
- `bulk_import_new_sites.py` - Importar sitios adicionales
- `research_additional_sources.py` - Investigar nuevas fuentes
- `generate_real_candidates.py` - Generar candidatas con APIs reales

---

## 🚀 Próximas Mejoras

### Corto Plazo:
- [ ] Exportar zonas a CSV/GeoJSON
- [ ] Análisis detallado al click
- [ ] Heatmap de densidad
- [ ] Filtros múltiples simultáneos

### Mediano Plazo:
- [ ] Integración con análisis ArcheoScope
- [ ] Comparación temporal de zonas
- [ ] Alertas de nuevos sitios
- [ ] Reportes automáticos

### Largo Plazo:
- [ ] Machine Learning para predicción
- [ ] Integración con drones
- [ ] Colaboración multi-usuario
- [ ] API pública

---

## 📞 Soporte

**Sistema:** ArcheoScope Hot Zones Visualization  
**Versión:** 1.0.0  
**Fecha:** 2026-01-26  
**Estado:** ✅ PRODUCCIÓN

---

**Generado automáticamente por ArcheoScope**  
*Visualización científica de zonas arqueológicas prioritarias*
