# 🗺️ Estrategia de Clasificación de Terreno

## 🎯 Objetivo

Clasificar los 80,457 sitios arqueológicos por tipo de terreno para:
1. **Ajustar instrumentos de detección** según ambiente
2. **Mejorar precisión** de anomalías detectadas
3. **Optimizar selección** de sitios para campañas

---

## 🧭 Enfoque Robusto y Escalable (2 Capas)

### 🧱 Capa 1: Reglas Duras (Clasificación Física)

**Objetivo:** Clasificar casos obvios usando umbrales físicos

**Variables clave (todas públicas):**

| Variable | Fuente | Descripción |
|----------|--------|-------------|
| **NDVI** | Sentinel-2 | Normalized Difference Vegetation Index |
| **LST** | MODIS/Landsat | Land Surface Temperature |
| **Elevación** | SRTM/ASTER | Altura sobre nivel del mar |
| **Pendiente** | DEM derivado | Inclinación del terreno |
| **Backscatter SAR** | Sentinel-1 | Retrodispersión radar |
| **NDWI** | Sentinel-2 | Normalized Difference Water Index |
| **NDSI** | Sentinel-2 | Normalized Difference Snow Index |
| **Precipitación** | CHIRPS | Precipitación anual |
| **Rugosidad** | DEM derivado | Rugosidad del terreno |

**Reglas implementadas:**

```python
# REGLA 1: Agua
if ndwi > 0.4:
    terrain = "WATER"

# REGLA 2: Hielo/Nieve
elif ndsi > 0.4:
    terrain = "ICE_SNOW"

# REGLA 3: Desierto
elif ndvi < 0.1 and precipitation < 200:
    terrain = "DESERT"

# REGLA 4: Montaña alta
elif elevation > 3000 and slope > 15:
    terrain = "MOUNTAIN"

# REGLA 5: Humedal
elif 0.2 < ndwi < 0.4 and ndvi > 0.3:
    terrain = "WETLAND"
```

**Ventajas:**
- ✅ Rápido (sin ML)
- ✅ Interpretable
- ✅ Alta confianza (>90%)
- ✅ Reduce carga de ML

---

### 🤖 Capa 2: Clasificador ML (Casos Ambiguos)

**Objetivo:** Clasificar casos no obvios usando Machine Learning

**Algoritmo recomendado: Random Forest**

**Por qué Random Forest:**
- ✅ Muy robusto
- ✅ Maneja features heterogéneas
- ✅ Interpretabilidad (feature importance)
- ✅ No necesita normalización estricta
- ✅ Funciona bien con datos ruidosos

**Alternativas:**
- **XGBoost/LightGBM**: Más preciso, ideal para límites difusos
- **K-Means**: Solo exploratorio (sin labels)

**Features de entrada (10 variables):**

```python
features = [
    ndvi_mean,           # Vegetación
    ndvi_std,            # Variabilidad vegetación
    ndwi_mean,           # Agua
    ndsi_mean,           # Nieve/hielo
    lst_mean,            # Temperatura
    elevation_mean,      # Elevación
    slope_mean,          # Pendiente
    sar_backscatter,     # SAR
    precipitation_mean,  # Precipitación
    roughness            # Rugosidad
]
```

**Etiquetas (clases):**

```python
0 = WATER          # Agua (océanos, lagos)
1 = DESERT         # Desierto árido
2 = VEGETATION     # Vegetación (bosques, praderas)
3 = MOUNTAIN       # Montaña (alta elevación)
4 = ICE_SNOW       # Hielo/Nieve (glaciares)
5 = WETLAND        # Humedal (pantanos)
6 = ANCIENT_URBAN  # Urbano antiguo
7 = UNKNOWN        # No clasificado
```

---

## 🐍 Implementación

### Módulo: `backend/terrain_classifier.py`

**Clases principales:**

```python
class TerrainType(Enum):
    WATER = 0
    DESERT = 1
    VEGETATION = 2
    MOUNTAIN = 3
    ICE_SNOW = 4
    WETLAND = 5
    ANCIENT_URBAN = 6
    UNKNOWN = 7

@dataclass
class TerrainFeatures:
    ndvi_mean: float
    ndvi_std: float
    ndwi_mean: float
    ndsi_mean: float
    lst_mean: float
    elevation_mean: float
    slope_mean: float
    sar_backscatter: float
    precipitation_mean: float
    roughness: float

class TerrainClassifier:
    def classify_with_hard_rules(features) -> Optional[Classification]
    def classify_with_ml(features) -> Classification
    def classify(features) -> Classification
    def classify_from_coordinates(lat, lon) -> Classification
```

**Flujo de clasificación:**

```
┌─────────────────────────────────────────────────────────┐
│ 1. EXTRACCIÓN DE FEATURES                               │
│    ├─ Coordenadas (lat, lon)                            │
│    ├─ APIs públicas (Sentinel, MODIS, SRTM)            │
│    └─ Features físicas (NDVI, LST, elevación, etc.)    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. CAPA 1: REGLAS DURAS                                 │
│    ├─ ¿NDWI > 0.4? → AGUA                              │
│    ├─ ¿NDSI > 0.4? → HIELO                             │
│    ├─ ¿NDVI < 0.1 + precip < 200? → DESIERTO           │
│    ├─ ¿Elevación > 3000 + slope > 15? → MONTAÑA        │
│    └─ ¿Caso obvio? → CLASIFICADO (confianza >90%)      │
└─────────────────────────────────────────────────────────┘
                        ↓
                   ¿Obvio?
                   /     \
                 Sí       No
                 ↓         ↓
┌──────────────────┐  ┌─────────────────────────────────┐
│ RESULTADO        │  │ 3. CAPA 2: RANDOM FOREST        │
│ (confianza >90%) │  │    ├─ Feature vector (10 dims)  │
│                  │  │    ├─ Predict probabilities     │
│                  │  │    └─ Clasificación (conf ~70%) │
└──────────────────┘  └─────────────────────────────────┘
                                ↓
                    ┌─────────────────────────┐
                    │ RESULTADO FINAL         │
                    │ + Probabilidades        │
                    │ + Método usado          │
                    │ + Features relevantes   │
                    └─────────────────────────┘
```

---

## 🚀 Ejecución

### Paso 1: Clasificar todos los sitios

```bash
python scripts/classify_all_sites.py
```

**Qué hace:**
1. Conecta a PostgreSQL
2. Obtiene todos los sitios (80,457)
3. Para cada sitio:
   - Extrae features desde coordenadas
   - Clasifica usando 2 capas
   - Actualiza `environmentType` en DB
4. Reporta estadísticas

**Tiempo estimado:** 5-10 minutos

**Salida esperada:**
```
🗺️ CLASIFICACIÓN DE TERRENO - TODOS LOS SITIOS
========================================================

Enfoque de 2 capas:
  1. Reglas duras (casos obvios)
  2. Random Forest / Heurísticas (casos ambiguos)

🔌 Conectando a PostgreSQL...
✅ Conectado

📊 Total de sitios a clasificar: 80,457

¿Continuar con la clasificación? (s/n): s

🚀 Iniciando clasificación...
  Procesados: 100/80,457 (0.1%)
  Procesados: 200/80,457 (0.2%)
  ...
  Procesados: 80,400/80,457 (99.9%)

📊 RESULTADOS DE CLASIFICACIÓN
========================================================
Sitios procesados: 80,457
Sitios actualizados: 80,457
Errores: 0

📈 Distribución por tipo de terreno:
  VEGETATION     : 35,000 sitios (43.50%)
  DESERT         : 15,000 sitios (18.64%)
  MOUNTAIN       : 12,000 sitios (14.91%)
  WETLAND        :  8,000 sitios ( 9.94%)
  WATER          :  5,000 sitios ( 6.21%)
  ICE_SNOW       :  3,000 sitios ( 3.73%)
  UNKNOWN        :  2,457 sitios ( 3.05%)
```

### Paso 2: Verificar resultados

```bash
python check_environment_values.py
```

### Paso 3: Test endpoints

```bash
python test_new_endpoints.py
```

---

## 📊 Clasificación Probabilística (BONUS)

En vez de clase dura, retornar probabilidades:

```json
{
  "terrain_type": "VEGETATION",
  "confidence": 0.64,
  "probabilities": {
    "vegetation": 0.64,
    "mountain": 0.18,
    "desert": 0.12,
    "ice_snow": 0.02,
    "wetland": 0.04
  },
  "method": "ml_classifier",
  "features_used": {
    "ndvi_mean": 0.65,
    "elevation_mean": 1200,
    "precipitation_mean": 800
  }
}
```

**Ventajas:**
- ✅ Detecta sitios "raros" (outliers arqueológicos)
- ✅ Identifica anomalías (ej. agricultura en desierto extremo)
- ✅ Útil para validación científica
- ✅ Permite ajuste fino de instrumentos

---

## 🎯 Ajuste de Instrumentos por Terreno

Una vez clasificados los sitios, ajustar instrumentos:

### DESERT (Desierto)
**Instrumentos óptimos:**
- ✅ Sentinel-1 SAR (penetración arena)
- ✅ Landsat Thermal (anomalías térmicas)
- ✅ MODIS NDVI (vegetación residual)
- ✅ OpenTopography DEM (micro-topografía)

**Umbrales ajustados:**
- Thermal anomaly: ΔT > 2°C
- NDVI threshold: < 0.15
- SAR backscatter: > -12 dB

### FOREST (Bosque/Selva)
**Instrumentos óptimos:**
- ✅ LiDAR Aerotransportado (penetración dosel)
- ✅ PALSAR L-band (sub-canopy)
- ✅ GEDI 3D (estructura vertical)
- ✅ ICESat-2 (perfiles láser)

**Umbrales ajustados:**
- Canopy height anomaly: Δh > 5m
- L-band backscatter: > -8 dB
- NDVI threshold: > 0.6

### GLACIER (Glaciar)
**Instrumentos óptimos:**
- ✅ ICESat-2 (perfiles precisos)
- ✅ SAR Interferométrico (movimiento hielo)
- ✅ GPR (radar penetrante)
- ✅ Sentinel-1 (backscatter hielo)

**Umbrales ajustados:**
- Ice thickness anomaly: Δt > 10m
- NDSI threshold: > 0.4
- Temperature: < 0°C

### SHALLOW_SEA (Aguas Poco Profundas)
**Instrumentos óptimos:**
- ✅ Sonar Multihaz (batimetría)
- ✅ Magnetometría (metales)
- ✅ Sub-bottom Profiler (sedimentos)
- ✅ Optical Satellite (aguas claras)

**Umbrales ajustados:**
- Depth: < 200m
- Magnetic anomaly: > 50 nT
- Bathymetry resolution: < 1m

---

## 🔥 Por Qué Esto es Ideal para Arqueología

### 1. Funciona aunque el sitio esté enterrado
- No depende de visibilidad superficial
- Detecta anomalías físicas profundas
- Usa múltiples sensores complementarios

### 2. No depende de excavación
- Análisis remoto 100%
- Cobertura global
- Costo-efectivo

### 3. Detecta incongruencias culturales
- **Ejemplo:** Sitio agrícola en desierto extremo
  - NDVI local > 0.3 (vegetación)
  - NDVI regional < 0.1 (desierto)
  - → Anomalía arqueológica (irrigación antigua)

### 4. Clasificación probabilística
- Identifica sitios "raros"
- Outliers arqueológicos
- Validación científica

---

## 📈 Mejoras Futuras

### Fase 1: Implementación Actual ✅
- Reglas duras implementadas
- Heurísticas mejoradas
- Clasificación desde coordenadas
- Actualización masiva de DB

### Fase 2: APIs Reales (Próximo)
- Integrar Sentinel-2 API (NDVI, NDWI, NDSI)
- Integrar MODIS API (LST)
- Integrar SRTM API (elevación, pendiente)
- Integrar CHIRPS API (precipitación)

### Fase 3: Random Forest Entrenado
- Recolectar dataset etiquetado
- Entrenar modelo Random Forest
- Validación cruzada
- Feature importance analysis

### Fase 4: XGBoost para Límites Difusos
- Casos ambiguos (semi-desierto, tundra)
- Transiciones (bosque-pradera)
- Sitios costeros

### Fase 5: Deep Learning (Opcional)
- CNN para imágenes satelitales
- Transfer learning (ResNet, EfficientNet)
- Solo si dataset grande (>10,000 labels)

---

## 🧪 Validación

### Métricas de calidad:
- **Precisión global**: >85%
- **Confianza promedio**: >75%
- **Casos obvios (reglas duras)**: >60%
- **Casos ambiguos (ML)**: <40%

### Validación manual:
- Seleccionar 100 sitios aleatorios
- Verificar clasificación con Google Earth
- Calcular accuracy

### Validación cruzada:
- Comparar con bases de datos existentes
- UNESCO sites (ambiente conocido)
- Sitios de referencia

---

## 📁 Archivos Creados

```
backend/terrain_classifier.py          - Clasificador de 2 capas
scripts/classify_all_sites.py          - Script de clasificación masiva
ESTRATEGIA_CLASIFICACION_TERRENO.md    - Esta documentación
```

---

## ✅ Checklist

- [x] Módulo TerrainClassifier implementado
- [x] Reglas duras (5 reglas)
- [x] Heurísticas mejoradas (fallback ML)
- [x] Script de clasificación masiva
- [x] Documentación completa
- [ ] Ejecutar clasificación (80,457 sitios)
- [ ] Verificar distribución
- [ ] Test endpoints con filtros
- [ ] Ajustar umbrales de instrumentos

---

**Fecha:** 2026-01-25  
**Estado:** Listo para ejecutar  
**Próximo paso:** `python scripts/classify_all_sites.py`
