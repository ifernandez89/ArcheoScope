# Detección de Subestructuras Huecas en ArcheoScope

## 🎯 Objetivo

Sistema científico para detectar **subestructuras huecas subsuperficiales** usando datos satelitales, con filtros rigurosos y conclusiones defendibles.

## 🔬 Fundamento Científico

### Principio Fundamental

> **Un vacío NO se ve directamente desde satélite.**  
> **Se infiere por CONTRADICCIONES FÍSICAS persistentes.**

### ¿Qué es una "subestructura hueca" detectable?

Una cavidad subsuperficial que produce señales anómalas **persistentes** y **convergentes** en múltiples sensores:

1. **SAR**: Pérdida de coherencia + baja retrodispersión
2. **Térmico**: Enfriamiento nocturno anómalo + desacople día/noche
3. **Humedad**: NDVI bajo pero estable (condensación interna)
4. **Topografía**: Micro-hundimiento simétrico

## 🚫 Filtro Duro Obligatorio

### ANTES de buscar vacíos, descartar:

❌ **Hielo/glaciares** (no estable)  
❌ **Cuerpos de agua** (no aplicable)  
❌ **Sedimentos activos** (dunas móviles)  
❌ **Pendientes >15°** (laderas inestables)  
❌ **NDVI >0.25** (vegetación densa)  
❌ **Actividad volcánica** (varianza térmica alta)

### Implementación

```python
def is_stable_continental_land(context):
    return (
        context.surface_type == "land" and
        context.is_ice == False and
        context.is_water == False and
        context.slope < 15 and
        context.ndvi_mean < 0.25 and
        context.thermal_variance < 5.0
    )
```

**Si falla → NO analizar vacíos.**

## 📊 Señales de Vacío

### A. SAR (Sentinel-1) — 35% peso

**Buscar:**
- Pérdida local de coherencia (< 0.5)
- Baja retrodispersión persistente (< -15 dB)
- Geometría regular

**Física:**
> Huecos → menos masa → peor retorno radar

```python
sar_void_score = (
    low_backscatter and
    coherence_drop and
    spatial_symmetry
)
```

### B. Térmico Nocturno (Landsat LST) — 25% peso

**Buscar:**
- Enfriamiento más rápido de noche (> 2°C anomalía)
- Desacople día/noche (rango < 5°C)
- Patrón estable multi-temporal

**Física:**
> Cavidades → menor inercia térmica

```python
thermal_anomaly = night_temp < expected_by_elevation - 2.0
```

### C. Humedad Persistente (NDVI) — 20% peso

**Buscar:**
- NDVI bajo (< 0.2)
- NDVI estable (varianza < 0.05)
- Persistencia temporal (> 0.7)

**Física:**
> Condensación interna / microclima subterráneo

```python
humidity_signal = (
    ndvi_mean < 0.2 and
    ndvi_variance < 0.05 and
    temporal_stability > 0.7
)
```

### D. Micro-hundimiento (DEM/LiDAR) — 20% peso

**Buscar:**
- Depresión local (< -0.5m)
- Forma simétrica (> 0.6)
- NO explicable por erosión

**Física:**
> Colapso gradual sobre vacío

```python
subsidence_score = (
    local_depression and
    symmetric_shape and
    not_explained_by_erosion
)
```

## 🎯 Score Compuesto

```python
void_probability = (
    sar_score * 0.35 +
    thermal_score * 0.25 +
    humidity_score * 0.20 +
    subsidence_score * 0.20
)
```

### Umbrales Científicos

| Score | Interpretación | Acción |
|-------|----------------|--------|
| < 0.4 | **Natural** | Descartar |
| 0.4 - 0.6 | **Ambiguo** | Monitorear |
| 0.6 - 0.75 | **Cavidad probable** | Análisis detallado |
| > 0.75 | **Subestructura hueca fuerte** | Validación de campo |

## 🔍 Clasificación: Artificial vs Natural

### Indicadores de Artificialidad

✅ **Simetría geométrica** (> 0.7)  
✅ **Ángulos rectos** detectados  
✅ **Orientación no geomorfológica**  
✅ **Repetición modular**

```python
if symmetry > 0.7 and (right_angles or orientation_bias):
    classification = "ARTIFICIAL_CANDIDATE"
else:
    classification = "NATURAL_CAVITY_OR_UNKNOWN"
```

## 📝 Conclusión Científica

### Formato Riguroso

```
"La región analizada presenta [señales detectadas]. 
Estos indicadores combinados [interpretación] 
en terreno continental estable. [Nota de origen]"
```

### Ejemplo Real

```
"La región analizada presenta pérdida persistente de coherencia SAR, 
anomalía térmica nocturna desacoplada de la topografía, humedad 
sub-superficial estable y micro-hundimiento simétrico. Estos 
indicadores combinados son consistentes con la presencia de una 
subestructura hueca en terreno continental estable. La geometría 
regular y orientación sugieren posible origen antrópico."
```

**Características:**
- ✅ Rigurosa
- ✅ Defendible
- ✅ No afirmativa
- ✅ Científica

## 🏗️ Integración con ArcheoScope

### 1. Flujo Completo

```
Usuario ingresa coordenadas
         ↓
Environment Classifier → ¿Tierra estable?
         ↓ SÍ
Obtener datos satelitales (BD o APIs)
         ↓
Subsurface Void Detector
         ↓
Guardar en timt_analysis_results
         ↓
Mostrar conclusión científica
```

### 2. Módulos Involucrados

```
backend/
├── environment_classifier.py      # Filtro de estabilidad
├── subsurface_void_detector.py    # Detector principal
├── satellite_connectors/
│   ├── gpr_connector.py           # GPR (complementario)
│   └── ...
└── database.py                     # Persistencia
```

### 3. Tablas de BD

#### `timt_measurements`
Datos satelitales crudos:
- `sar_backscatter`, `sar_coherence`
- `lst_day`, `lst_night`
- `ndvi_mean`, `ndvi_variance`
- `elevation`, `slope`

#### `timt_analysis_results`
Resultados de análisis:
- `void_probability_score`
- `void_probability_level`
- `void_classification`
- `sar_score`, `thermal_score`, `humidity_score`, `subsidence_score`
- `scientific_conclusion`
- `confidence`

## 🧪 Testing en Casa

### Paso 1: Migración de BD

```bash
python apply_void_detection_migration.py
```

Esto crea/actualiza la tabla `timt_analysis_results`.

### Paso 2: Test con Coordenadas

```bash
# Desierto (buenas condiciones)
python test_void_detection_with_db.py --lat 30.0 --lon 31.0

# Montaña (rechazado por pendiente)
python test_void_detection_with_db.py --lat -13.1631 --lon -72.5450

# Océano (rechazado por agua)
python test_void_detection_with_db.py --lat 0.0 --lon -30.0
```

### Paso 3: Verificar Resultados

```sql
SELECT 
    lat, lon,
    void_probability_score,
    void_probability_level,
    void_classification,
    scientific_conclusion,
    confidence
FROM timt_analysis_results
WHERE analysis_type = 'subsurface_void_detection'
ORDER BY created_at DESC
LIMIT 10;
```

## 🎯 Casos de Uso

### Caso 1: Meseta Árida (Altiplano)

```
Coordenadas: -16.5, -68.1 (Bolivia)
Ambiente: semi_arid, pendiente 5°

Señales detectadas:
✓ SAR coherencia: 0.42 (caída)
✓ Thermal noche: 3.2°C más frío
✓ NDVI: 0.15 (bajo, estable)
✓ Depresión: -0.8m (simétrica)

Score: 0.78 → STRONG_VOID
Clasificación: ARTIFICIAL_CANDIDATE
Conclusión: "Consistente con subestructura hueca de origen antrópico"
```

### Caso 2: Desierto Costero (Atacama)

```
Coordenadas: -23.5, -70.2 (Chile)
Ambiente: desert, pendiente 3°

Señales detectadas:
✓ SAR backscatter: -17.2 dB
✓ Thermal anomalía: 2.8°C
✓ NDVI: 0.08 (extremadamente bajo)
✓ Simetría geométrica: 0.82

Score: 0.85 → STRONG_VOID
Clasificación: ARTIFICIAL_CANDIDATE
Conclusión: "Fuerte evidencia de cavidad subsuperficial artificial"
```

### Caso 3: Selva (Rechazado)

```
Coordenadas: -3.0, -60.0 (Amazonas)
Ambiente: forest, NDVI 0.75

Filtro de estabilidad: RECHAZADO
Razón: "NDVI 0.75 > 0.25 (vegetación densa)"
Score: 0.0
Conclusión: "Análisis no aplicable: vegetación densa"
```

## ⚠️ Limitaciones

### 1. NO es Detección Directa
- GPR real sería ideal, pero no está disponible satelitalmente
- Este sistema **infiere** basado en contradicciones físicas

### 2. Falsos Positivos Posibles
- Formaciones geológicas naturales (karst, lava tubes)
- Variaciones de suelo natural
- **Siempre requiere validación de campo**

### 3. Dependencia de Datos
- Calidad de datos satelitales
- Cobertura temporal
- Resolución espacial

### 4. Ambientes Limitados
- Óptimo: Desiertos, mesetas áridas
- Limitado: Bosques, zonas urbanas
- No aplicable: Agua, hielo, pendientes altas

## 📚 Referencias Científicas

1. **SAR Coherence for Subsurface Detection**  
   Tapete, D. & Cigna, F. (2017). *Remote Sensing*

2. **Thermal Inertia and Archaeological Features**  
   Agapiou, A. et al. (2016). *Journal of Archaeological Science*

3. **NDVI Anomalies over Buried Structures**  
   Lasaponara, R. & Masini, N. (2012). *Springer*

4. **Micro-topography and Subsurface Voids**  
   Chase, A. F. et al. (2014). *PNAS*

## 🚀 Roadmap

### Fase 1: Validación (Actual)
- [x] Detector implementado
- [x] Filtros de estabilidad
- [x] Score compuesto
- [x] Integración con BD
- [ ] Testing con datos reales

### Fase 2: Refinamiento
- [ ] Ajustar pesos según validación de campo
- [ ] Incorporar más señales (gravimetría, magnetometría)
- [ ] Mejorar clasificación artificial/natural
- [ ] Series temporales multi-año

### Fase 3: Producción
- [ ] API endpoint dedicado
- [ ] Visualización en frontend
- [ ] Reportes científicos automatizados
- [ ] Integración con GPR real (cuando disponible)

## 🎓 Conclusión

Este sistema proporciona una **metodología científicamente rigurosa** para detectar subestructuras huecas usando datos satelitales públicos.

**Fortalezas:**
- ✅ Filtros duros previenen delirios
- ✅ Múltiples señales convergentes
- ✅ Conclusiones defendibles
- ✅ Clasificación artificial/natural
- ✅ Integración completa con ArcheoScope

**Uso correcto:**
> Herramienta de **priorización** para validación de campo,  
> NO como evidencia definitiva de estructuras arqueológicas.

---

**Preparado para testing en casa con BD PostgreSQL real.**
