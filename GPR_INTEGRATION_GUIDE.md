# GPR Integration in ArcheoScope

## 🎯 Objetivo

Integrar **GPR (Ground Penetrating Radar)** como herramienta secundaria fuerte para detección de anomalías subsuperficiales en contextos arqueológicos.

## 📊 Filosofía de Uso

### ✅ GPR como Validador, NO como Sensor Primario

```
FLUJO CORRECTO:
1. Detección satelital (SAR, Thermal, NDVI) → Candidata
2. Análisis de contexto ambiental → Selección de instrumentos
3. GPR (si ambiente apropiado) → Validación subsuperficial
4. Score final integrado → Priorización
```

### ❌ NO Buscar GPR en Tiempo Real

GPR público **NO** está disponible como servicio en tiempo real. Se usa mediante:
- Datasets descargados (Zenodo, repositorios arqueológicos)
- Patrones de referencia pre-calculados
- Simulación sintética (gprMax)

## 🌍 Ambientes Óptimos para GPR

### ⭐ Top Tier (Máxima Efectividad)

| Ambiente | Atenuación | Penetración | Uso Arqueológico |
|----------|------------|-------------|------------------|
| **Desierto** | Muy baja | 5-10m | Muros enterrados, fundaciones |
| **Semi-árido** | Baja | 3-6m | Cavidades, estructuras |
| **Mesetas rocosas** | Baja | 4-8m | Cámaras subterráneas |

### ⚠️ Ambientes Limitados

| Ambiente | Problema | Penetración |
|----------|----------|-------------|
| Selva densa | Alta atenuación (humedad) | <1m |
| Zonas urbanas | Ruido electromagnético | Variable |
| Suelos arcillosos | Alta conductividad | <2m |

## 🔧 Componentes del Sistema

### 1. GPR Connector (`gpr_connector.py`)

```python
from backend.satellite_connectors.gpr_connector import gpr_connector

# Calcular similitud con patrones conocidos (SINTÉTICO)
result = gpr_connector.get_gpr_similarity_score(
    lat=30.0,
    lon=31.0,
    environment_type='desert',
    target_depth_m=3.0
)

print(f"GPR Similarity Score: {result.value}")
print(f"Confidence: {result.confidence}") # 0.6 (CAP para sintéticos)
print(f"Source: {result.source}") # 'synthetic_reference'
```

#### Patrones de Referencia

El conector incluye patrones de:
- **Cavidades**: Cámaras subterráneas, tumbas, cisternas
- **Muros enterrados**: Fundaciones, muros de ciudades antiguas
- **Fundaciones**: Plataformas ceremoniales, edificios
- **Anomalías de humedad**: Túneles, acueductos, sistemas hidráulicos
- **Compactación diferencial**: Caminos antiguos, plazas

### 2. Environment Classifier (Actualizado)

El clasificador ahora recomienda GPR automáticamente en ambientes apropiados:

```python
from backend.environment_classifier import EnvironmentClassifier

classifier = EnvironmentClassifier()
context = classifier.classify(lat=30.0, lon=31.0)

# Para desiertos, GPR está en secondary_sensors
if 'GPR' in context.secondary_sensors:
    print("✅ GPR recomendado para este ambiente")
```

**Ambientes con GPR habilitado:**
- Sahara
- Desierto Arábigo
- Gobi
- Atacama
- Mesetas semiáridas

### 3. Multi-Instrumental Enrichment (Actualizado)

GPR ahora es parte del sistema multi-instrumental:

```python
from backend.multi_instrumental_enrichment import InstrumentType

# GPR tiene peso 0.13 (13% del score total)
# Especialmente fuerte en ambientes áridos
```

#### Score Multi-Instrumental con GPR

```
HuecoScore =
  0.17 * SAR_compaction +
  0.14 * Thermal_anomaly +
  0.13 * GPR_similarity +      ← NUEVO
  0.14 * Temporal_persistence +
  0.11 * NDVI_stress +
  0.18 * LiDAR_shape
```

## 📥 Uso de Datasets Públicos

### Zenodo - Archaeological GPR

```python
# Listar datasets disponibles
print(gpr_connector.public_datasets)

# Descargar dataset (manual por ahora)
gpr_connector.download_public_dataset(
    'zenodo_archaeological_gpr',
    target_region=(30.0, 31.0)
)
```

### Formato de Datos en Caché

Guardar datos GPR descargados en:
```
cache/gpr_data/gpr_data_{lat}_{lon}.json
```

Formato:
```json
{
  "lat": 30.05,
  "lon": 31.23,
  "source": "Zenodo Archaeological GPR Dataset",
  "acquisition_date": "2023-05-15",
  "depth_slices": [
    {
      "depth_m": 1.0,
      "mean_amplitude": 0.75,
      "variance": 0.15
    },
    {
      "depth_m": 2.0,
      "mean_amplitude": 0.82,
      "variance": 0.08
    }
  ],
  "reflectivity_map": [0.6, 0.7, 0.8, 0.75, 0.65]
}
```

## 🧪 Simulación GPR Sintética

Para validar hipótesis sin datos reales:

```python
from backend.satellite_connectors.gpr_connector import GPRSignatureType

# Simular cavidad a 2m de profundidad
synthetic_gpr = gpr_connector.simulate_gpr_signature(
    signature_type=GPRSignatureType.CAVITY,
    depth_m=2.0,
    width_m=3.0
)

print(f"Peak amplitude: {synthetic_gpr['peak_amplitude']}")
print(f"Two-way time: {synthetic_gpr['two_way_time_ns']} ns")
```

## 🎯 Casos de Uso Específicos

### Caso 1: Meseta Árida (Altiplano, Anatolia)

```
Ambiente: semi_arid
Objetivo: Detectar muros enterrados

Instrumentos seleccionados:
1. SAR → Compactación superficial
2. Thermal → Inercia térmica nocturna
3. GPR → Validación subsuperficial (0-3m)
4. NDVI → Estrés vegetal

Resultado esperado:
- SAR detecta anomalía de textura
- Thermal confirma inercia térmica alta
- GPR pattern matching: 0.75 similarity (buried_wall)
- Score final: 0.82 → field_validation
```

### Caso 2: Desierto Costero (Atacama, Perú)

```
Ambiente: desert (coastal)
Objetivo: Detectar fundaciones de estructuras

Instrumentos seleccionados:
1. Thermal → Máxima diferencia día/noche
2. SAR → Compactación
3. GPR → Penetración máxima (5-8m)
4. Multitemporal → Persistencia

Resultado esperado:
- Thermal: +2.5°C noche, -1.5°C día
- SAR: Backscatter +3.2 dB
- GPR: 0.88 similarity (foundation, 2.5m depth)
- Score final: 0.91 → field_validation (ALTA PRIORIDAD)
```

### Caso 3: Llanura Aluvial Abandonada

```
Ambiente: grassland (semi_arid)
Objetivo: Detectar sistemas hidráulicos antiguos

Instrumentos seleccionados:
1. SAR → Humedad residual
2. NDVI → Vegetación anómala
3. GPR → Túneles/acueductos
4. Multitemporal → Persistencia

Resultado esperado:
- SAR: Coherencia baja en líneas
- NDVI: Vegetación más verde (humedad)
- GPR: 0.70 similarity (moisture_anomaly, 3-5m)
- Score final: 0.78 → detailed_analysis
```

## 🔬 Recomendaciones de Frecuencia GPR

El sistema recomienda automáticamente la frecuencia óptima:

```python
recommendation = gpr_connector.get_recommended_gpr_frequency(
    environment_type='desert',
    target_depth_m=3.0
)

print(recommendation)
# {
#   'recommended_frequency_mhz': 400,
#   'expected_resolution_cm': 10,
#   'max_penetration_m': 3.6,
#   'environment_factor': 1.0,
#   'notes': 'Optimized for desert at 3.0m depth'
# }
```

## ⚠️ Limitaciones y Consideraciones

### 1. NO es Sensor Primario
- GPR se usa para **validar** anomalías detectadas por satélite
- NO reemplaza SAR, Thermal, o NDVI

### 2. Dependencia de Ambiente
- Efectividad varía dramáticamente según suelo
- Humedad alta = penetración baja
- Arcilla = alta atenuación

### 3. Datos Públicos Limitados
- Mayoría de GPR es de campo, no satelital
- Requiere descarga manual de datasets
- Cobertura geográfica irregular

### 4. Interpretación Requiere Experiencia
- Patrones GPR pueden ser ambiguos
- Validación de campo siempre necesaria
- Falsos positivos posibles (geología natural)

## 📊 Integración en el Pipeline Científico

```python
# En scientific_pipeline.py

def analyze_coordinates(lat, lon):
    # 1. Clasificar ambiente
    env_context = environment_classifier.classify(lat, lon)
    
    # 2. Verificar si GPR es apropiado
    if 'GPR' in env_context.secondary_sensors:
        # 3. Calcular similitud GPR
        gpr_result = gpr_connector.get_gpr_similarity_score(
            lat, lon,
            env_context.environment_type.value,
            target_depth_m=3.0
        )
        
        # 4. Agregar a datos disponibles
        available_data['gpr'] = {
            'subsurface_anomaly_detected': gpr_result.value > 0.6,
            'confidence': gpr_result.confidence,
            'similarity_score': gpr_result.value,
            'depth_m': 3.0,
            'anomaly_type': 'pattern_based',
            'source': gpr_result.source
        }
    
    # 5. Enriquecimiento multi-instrumental
    candidate = multi_instrumental_enrichment.enrich_candidate(
        zone, available_data
    )
    
    return candidate
```

## 🚀 Próximos Pasos

### Fase 1: Validación (Actual)
- [x] GPR Connector implementado
- [x] Patrones de referencia cargados
- [x] Integración con environment_classifier
- [x] Integración con multi_instrumental_enrichment

### Fase 2: Datos Reales
- [ ] Descargar datasets de Zenodo
- [ ] Procesar datos GPR reales
- [ ] Validar con sitios conocidos
- [ ] Ajustar pesos según resultados

### Fase 3: Simulación Avanzada
- [ ] Integrar gprMax para simulación
- [ ] Generar firmas sintéticas por tipo de sitio
- [ ] Entrenar detector de patrones
- [ ] Validación cruzada con datos reales

### Fase 4: Optimización
- [ ] Ajuste automático de frecuencia
- [ ] Corrección por tipo de suelo
- [ ] Integración con DEM para topografía
- [ ] Recomendaciones de campo específicas

## 📚 Referencias

- **Zenodo GPR Datasets**: https://zenodo.org/communities/gpr-archaeology
- **gprMax**: https://www.gprmax.com/
- **GPR Archaeological Prospection**: Conyers, L. B. (2013)
- **Subsurface Sensing**: Daniels, D. J. (2004)

## 🎓 Conclusión

GPR en ArcheoScope es una **herramienta de validación secundaria potente**, especialmente efectiva en:

✅ Desiertos y zonas áridas
✅ Mesetas rocosas estables
✅ Llanuras aluviales secas
✅ Contextos con baja humedad

**NO** es un sensor satelital en tiempo real, pero proporciona:
- Validación de anomalías superficiales
- Estimación de profundidad de estructuras
- Priorización de zonas para campo
- Contexto subsuperficial complementario

**Uso correcto**: Combinar con SAR + Thermal + NDVI para máxima señal/ruido.
