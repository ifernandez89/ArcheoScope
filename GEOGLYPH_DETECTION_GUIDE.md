# 🔍 Sistema de Detección de Geoglifos - ArcheoScope

## 📋 Resumen Ejecutivo

Sistema especializado para detección y análisis de geoglifos (Arabia, Nazca, Jordania, etc.) integrado en ArcheoScope.

### Capacidades Implementadas

✅ **Análisis Geométrico Avanzado**
- Orientación principal (PCA sobre contorno)
- Simetría bilateral
- Relación largo/ancho (aspect ratio)
- Repetición angular

✅ **Contexto Geológico**
- Análisis volcánico (harrats, basaltos)
- Paleohidrología (wadis, paleocanales)
- Transiciones roca-sedimento

✅ **Alineaciones Astronómicas**
- Solsticios (verano/invierno)
- Equinoccios
- Estrellas (Sirio, Orión) con corrección de precesión

✅ **Modos Operativos**
- **Científico**: Umbrales estrictos, FP=NO, ideal papers
- **Explorador**: Más sensibilidad, detecta "rarezas"
- **Cognitivo**: Patrones no lineales, solo señalar

✅ **Zonas Prometedoras**
- Sur de Harrat Uwayrid
- Límite Arabia-Jordania
- Bordes de Rub' al Khali

---

## 🎯 Reglas Críticas de Resolución Espacial

### Para Geoglifos tipo Arabia

| Sensor | Resolución Requerida | Ideal |
|--------|---------------------|-------|
| **Óptico** | ≤ 1 m/pixel | **0.5 m/pixel** (WorldView/Pleiades) |
| **DEM** | ≥ 10-30 m | SRTM sirve, NASADEM mejor |
| **Derivados** | Slope + Aspect | Crítico para orientación |

> ⚠️ **REGLA DE ORO**: Si no ves los extremos con claridad, NO entrenes todavía.

---

## 🚀 Quick Start

### 1. Instalación

```bash
# Ya está integrado en ArcheoScope
# No requiere instalación adicional
```

### 2. Iniciar Backend

```bash
cd c:\Python\ArcheoScope
python backend/api/main.py
```

El endpoint estará disponible en: `http://localhost:8003/geoglyph`

### 3. Uso Básico

#### Detectar Geoglifo Individual

```bash
curl -X POST "http://localhost:8003/geoglyph/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 26.5,
    "lon": 38.5,
    "lat_min": 26.4,
    "lat_max": 26.6,
    "lon_min": 38.4,
    "lon_max": 38.6,
    "resolution_m": 0.5,
    "mode": "scientific"
  }'
```

#### Obtener Zonas Prometedoras

```bash
curl "http://localhost:8003/geoglyph/zones/promising"
```

#### Ver Tipos de Geoglifos

```bash
curl "http://localhost:8003/geoglyph/types"
```

#### Ver Modos Operativos

```bash
curl "http://localhost:8003/geoglyph/modes"
```

---

## 📊 Métricas Automáticas Implementadas

### 1. Orientación & Simetría

| Métrica | Cómo se Calcula |
|---------|----------------|
| **Orientación principal** | PCA sobre contorno |
| **Longitud eje mayor** | Bounding ellipse |
| **Simetría bilateral** | Mirror error (0=perfecto, 1=asimétrico) |
| **Repetición angular** | Histograma de ángulos |
| **Relación largo/ancho** | Shape ratio (aspect ratio) |

### 2. Patrones Conocidos

**Pendants y Gates suelen:**
- Orientarse NW–SE o E–W
- Tener colas apuntando a zonas bajas
- Aspect ratio > 3.0 (pendants) o 1.5-3.0 (gates)

---

## 🌋 Cruce con Volcanes (Harrats)

### Datos Necesarios

- Mapas de basalt flows
- Tubos de lava
- Cráteres antiguos

### Patrón Conocido

✅ **SÍ**: Superficies estables, bordes de coladas  
❌ **NO**: Dentro de coladas jóvenes

### Implementación

```python
volcanic_ctx = detector.analyze_volcanic_context(lat, lon)

if volcanic_ctx.on_stable_surface and not volcanic_ctx.on_young_flow:
    print("✅ Contexto volcánico favorable")
```

---

## 💧 Agua Antigua (ORO para Geoglifos)

### Cruces Clave

1. **Paleocanales** (DEM + flow accumulation)
2. **Antiguos wadis**
3. **Playas secas / lagos fósiles**

### Patrón Conocido

Muchos geoglifos:
- Apuntan a zonas donde hubo agua estacional
- Están en transiciones: roca ↔ sedimento

### Implementación

```python
hydro = detector.analyze_paleohydrology(dem_data, lat, lon)

if hydro.on_sediment_transition:
    print("🏆 ORO: Transición roca-sedimento")

if hydro.distance_to_wadi_km < 2.0:
    print(f"💧 Cerca de wadi: {hydro.distance_to_wadi_km:.1f}km")
```

---

## 🌌 Alineaciones Solares/Estelares

### Solar (Empezar por Acá)

Para cada estructura:
1. Calcular azimut del eje principal
2. Comparar con:
   - Solsticio de verano
   - Solsticio de invierno
   - Equinoccios

> 👉 Si hay picos repetidos, NO es casual

### Estelar (Nivel Avanzado)

Opciones realistas:
- Salida de Sirio
- Cinturón de Orión
- **Corregir precesión (~8.000 años)**

> 💡 Si ves coherencia regional → **paper-level discovery**

### Implementación

```python
celestial = detector.analyze_celestial_alignments(orientation, lat, lon)

if celestial.best_solar_alignment != "none":
    print(f"☀️ Alineación: {celestial.best_solar_alignment}")
    
if celestial.regional_coherence > 0.70:
    print("🏆 PAPER-LEVEL: Coherencia regional alta")
```

---

## 🤖 IA para Detectar Nuevos Geoglifos

### Pipeline Recomendado

1. **Segmentación** (U-Net / SAM)
2. **Clasificación**:
   - gate
   - pendant
   - wheel
   - kite
   - ruido geológico
3. **Scoring cultural**:
   - forma
   - contexto
   - orientación
   - entorno hídrico

> 👉 **NO entrenar solo con Arabia**: agregar Nazca / Jordania / Sinaí para generalizar

### TODO: Integración ML

```python
# TODO: Implementar en versión futura
# from geoglyph_ml_classifier import GeoglyphClassifier
# 
# classifier = GeoglyphClassifier()
# classifier.train(datasets=["arabia", "nazca", "jordan"])
# geoglyph_type = classifier.predict(features)
```

---

## 🗺️ Zonas Aún No Catalogadas

### Estrategia de Exploración

Buscar zonas con:
- ✅ Basalto antiguo
- ✅ Baja intervención moderna
- ✅ Cercanía a paleorutas
- ✅ Ausencia de papers arqueológicos

### Regiones Prometedoras

| Zona | Coordenadas | Prioridad | Razón |
|------|-------------|-----------|-------|
| **Sur de Harrat Uwayrid** | 26-27°N, 38-39°E | 🔴 Alta | Basalto antiguo, baja intervención |
| **Límite Arabia-Jordania** | 29-30°N, 37-38°E | 🔴 Crítica | Paleorutas, sin papers |
| **Bordes Rub' al Khali** | 19-21°N, 50-52°E | 🟡 Media | Bordes, no centro |

### Uso

```python
zones = get_promising_zones()

for zone_id, zone_info in zones.items():
    print(f"📍 {zone_info['name']}")
    print(f"   Prioridad: {zone_info['priority']}")
    print(f"   Razón: {zone_info['reason']}")
```

---

## ⚙️ Modos Operativos

### 🧪 Modo Científico Duro

```python
detector = GeoglyphDetector(mode=DetectionMode.SCIENTIFIC)
```

- **Umbrales**: Muy estrictos
- **Falsos Positivos**: NO tolerados
- **Uso**: Papers científicos
- **Cultural Score Mínimo**: 0.75
- **Resolución Mínima**: 1.0 m/pixel

### 🧭 Modo Explorador

```python
detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
```

- **Umbrales**: Moderados
- **Falsos Positivos**: Hasta 35% aceptable
- **Uso**: Descubrimientos, nuevas zonas
- **Cultural Score Mínimo**: 0.50
- **Resolución Mínima**: 2.0 m/pixel

### 🧠 Modo Cognitivo/Anómalo

```python
detector = GeoglyphDetector(mode=DetectionMode.COGNITIVE)
```

- **Umbrales**: Muy permisivos
- **Falsos Positivos**: Hasta 50% (solo señalar)
- **Uso**: Hipótesis nuevas, patrones inusuales
- **Cultural Score Mínimo**: 0.30
- **Resolución Mínima**: 5.0 m/pixel
- **Filosofía**: **NO afirmar, solo señalar**

---

## 📈 Scoring Cultural

### Componentes del Score

```python
cultural_score = (
    form_score * 0.25 +           # Simetría + aspect ratio
    orientation_score * 0.25 +    # Orientaciones conocidas + alineaciones
    context_score * 0.20 +        # Contexto volcánico
    hydrology_score * 0.30        # Contexto hídrico (ORO)
)
```

### Interpretación

| Score | Interpretación | Acción |
|-------|---------------|--------|
| **0.85+** | Muy alta probabilidad | Prioridad CRÍTICA |
| **0.70-0.84** | Alta probabilidad | Prioridad ALTA |
| **0.50-0.69** | Probabilidad moderada | Prioridad MEDIA |
| **< 0.50** | Baja probabilidad | Prioridad BAJA |

---

## 🔬 Ejemplo Completo

```python
from backend.geoglyph_detector import GeoglyphDetector, DetectionMode
import numpy as np

# 1. Inicializar detector
detector = GeoglyphDetector(mode=DetectionMode.SCIENTIFIC)

# 2. Preparar datos (ejemplo)
lat, lon = 26.5, 38.5
bbox = (26.4, 26.6, 38.4, 38.6)
dem_data = np.random.rand(100, 100)  # TODO: datos reales

# 3. Detectar
result = detector.detect_geoglyph(
    lat=lat,
    lon=lon,
    lat_min=bbox[0],
    lat_max=bbox[1],
    lon_min=bbox[2],
    lon_max=bbox[3],
    dem_data=dem_data,
    resolution_m=0.5
)

# 4. Analizar resultado
print(f"🔍 Tipo: {result.geoglyph_type.value}")
print(f"📊 Cultural Score: {result.cultural_score:.2f}")
print(f"📐 Orientación: {result.orientation.azimuth_deg:.1f}°")
print(f"🌋 Superficie estable: {result.volcanic_context.on_stable_surface}")
print(f"💧 Cerca de wadi: {result.paleo_hydrology.distance_to_wadi_km:.1f}km")
print(f"☀️ Alineación solar: {result.celestial_alignment.best_solar_alignment}")

if result.paper_level_discovery:
    print("🏆 PAPER-LEVEL DISCOVERY!")

# 5. Razonamiento
print("\n📝 Razonamiento:")
for reason in result.detection_reasoning:
    print(f"  - {reason}")

# 6. Riesgos FP
print("\n⚠️ Riesgos de Falso Positivo:")
for risk in result.false_positive_risks:
    print(f"  - {risk}")
```

---

## 🔗 Integración con Pipeline Científico

El sistema de geoglifos se puede integrar con el pipeline científico existente:

```python
from backend.scientific_pipeline import ScientificPipeline
from backend.geoglyph_detector import GeoglyphDetector, DetectionMode

# Pipeline científico estándar
pipeline = ScientificPipeline()
result = await pipeline.analyze(lat, lon, lat_min, lat_max, lon_min, lon_max)

# Si el ambiente es desierto y hay anomalía, aplicar detector de geoglifos
if result.environment_type == "desert" and result.anomaly_score > 0.6:
    geoglyph_detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
    geoglyph_result = geoglyph_detector.detect_geoglyph(
        lat=lat, lon=lon,
        lat_min=lat_min, lat_max=lat_max,
        lon_min=lon_min, lon_max=lon_max,
        resolution_m=1.0
    )
    
    if geoglyph_result.cultural_score > 0.7:
        print("🔍 Posible geoglifo detectado!")
```

---

## 📚 Referencias Científicas

### Geoglifos de Arabia

- Kennedy, D. (2011). "The 'Works of the Old Men' in Arabia"
- Crassard, R. et al. (2015). "Addressing the Desert Kites Phenomenon"

### Geoglifos de Nazca

- Lambers, K. (2006). "The Geoglyphs of Palpa, Peru"
- Clarkson, P. (1990). "The Archaeology of the Nazca Pampa"

### Alineaciones Astronómicas

- Hawkins, G. (1969). "Ancient Lines in the Peruvian Desert"
- Aveni, A. (1990). "The Lines of Nazca"

---

## 🚧 Roadmap Futuro

### Fase 1: Mejoras Inmediatas
- [ ] Integrar datos reales de basalt flows
- [ ] Implementar cálculo de flow accumulation
- [ ] Mejorar detección de paleocanales

### Fase 2: ML/IA
- [ ] Entrenar clasificador U-Net para segmentación
- [ ] Dataset multi-región (Arabia + Nazca + Jordania)
- [ ] Transfer learning desde imágenes satelitales

### Fase 3: Exploración Sistemática
- [ ] Implementar batch scanning real
- [ ] Sistema de priorización automática
- [ ] Integración con WorldView/Pleiades

### Fase 4: Validación
- [ ] Comparación con catálogos existentes
- [ ] Validación con arqueólogos
- [ ] Publicación científica

---

## 📞 Soporte

Para preguntas o issues:
1. Revisar esta documentación
2. Consultar `/geoglyph/modes` para modos operativos
3. Consultar `/geoglyph/types` para tipos de geoglifos
4. Usar modo `explorer` para exploración inicial

---

## ⚖️ Consideraciones Éticas

> ⚠️ **IMPORTANTE**: Los geoglifos son patrimonio cultural.

- **NO** compartir coordenadas públicamente sin autorización
- **SÍ** reportar descubrimientos a autoridades arqueológicas
- **SÍ** usar para investigación científica responsable
- **NO** usar para saqueo o destrucción

---

**ArcheoScope - Geoglyph Detection System**  
*Versión 1.0 - Enero 2026*
