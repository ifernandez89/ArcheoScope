# Validador de Sitios Conocidos - Reescritura Completa

**Fecha:** 2026-01-26  
**Estado:** ✅ COMPLETADO - SOLO DATOS REALES  
**Archivo:** `backend/validation/known_sites_validator.py`

---

## CAMBIO FUNDAMENTAL

### ❌ ANTES (INVENTABA DATOS):
```python
# Simulaba análisis con np.random
np.random.seed(hash(site_name) % 2**32)
fake_probability = np.random.uniform(0.2, 0.9)
```

### ✅ AHORA (SOLO DATOS REALES):
```python
# Recibe análisis REAL de CoreAnomalyDetector
analysis_result = await core_detector.detect_anomaly(...)
real_probability = analysis_result.archaeological_probability
```

---

## FLUJO CORRECTO

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USUARIO ANALIZA ZONA                                     │
│    → CoreAnomalyDetector con APIs satelitales REALES       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. MEDICIONES REALES                                        │
│    → Sentinel-2: NDVI real                                  │
│    → Sentinel-1: SAR real                                   │
│    → Landsat: Térmico real                                  │
│    → ICESat-2: Elevación real                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. DETECCIÓN CON DATOS REALES                              │
│    → Score base determinista                                │
│    → Probabilidad arqueológica calculada                    │
│    → Convergencia instrumental                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. CONTRASTE CON BD DE SITIOS DOCUMENTADOS                 │
│    → Query a PostgreSQL (7,844 sitios reales)              │
│    → Buscar sitios cercanos                                 │
│    → Calcular distancias                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. VALIDACIÓN LÓGICA CON OPENCODE (DESPUÉS)                │
│    → Solo si probabilidad > 0.7                             │
│    → Valida coherencia lógica                               │
│    → NO se usa para detección                               │
│    → Asíncrono, no bloquea                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. CREAR REGISTRO DE CANDIDATO EN BD                       │
│    → Mediciones REALES guardadas                            │
│    → Sitios documentados cercanos                           │
│    → Validación lógica (si aplica)                          │
│    → Status: validated/candidate/false_positive/needs_review│
└─────────────────────────────────────────────────────────────┘
```

---

## ARQUITECTURA OPENCODE

### 🧠 ¿Qué ES OpenCode en este contexto?

**Herramienta cognitiva especializada**, NO un LLM conversacional.

**Sirve para:**
- ✅ Validar hipótesis
- ✅ Revisar consistencia lógica
- ✅ Generar explicaciones estructuradas
- ✅ Detectar contradicciones
- ✅ Estandarizar decisiones

**NO sirve para:**
- ❌ Inferencia pesada
- ❌ Detección primaria
- ❌ Reemplazar modelos locales

---

### 🧩 Arquitectura Correcta

```
[ Instrumentos Satelitales ]
         ↓
[ Mediciones REALES ]
         ↓
[ Detección de Anomalías ]
         ↓
[ Score Base Determinista ]
         ↓
[ Clasificación del Terreno ]
         ↓
[ 🧠 OpenCode / Zen ]   ← ACÁ (DESPUÉS, nunca antes)
         ↓
[ Candidato Validado ]
```

**👉 Después del análisis duro, nunca antes.**

---

### ⏱️ ¿Impacto en Performance?

| Componente | Impacto |
|------------|---------|
| APIs satelitales | 🔴 Alto (15-30 min) |
| SAR / NDVI cálculo | 🟠 Medio (2-5 min) |
| OpenCode puntual | 🟢 Bajo (30-90 seg) |
| OpenCode masivo | 🔴 Muy alto (NO HACER) |

**Usado correctamente:** Impacto mínimo (~2% del tiempo total)

---

### ✅ Uso Correcto de OpenCode

```python
# ✅ CORRECTO: Después del análisis, solo para alta probabilidad
if analysis_result.archaeological_probability > 0.7:
    logical_validation = await opencode.validate(context)

# ✅ CORRECTO: Asíncrono, no bloquea
async def validate_with_opencode(...):
    validation = await self.opencode.validate(context)

# ✅ CORRECTO: Cacheable (mismo input → mismo output)
cache_key = f"{candidate_hash}_{task_type}"
if cache_key in cache:
    return cache[cache_key]
```

### ❌ Uso INCORRECTO de OpenCode

```python
# ❌ INCORRECTO: En loop caliente
for pixel in city_grid:
    await opencode.validate(pixel)  # ¡NO!

# ❌ INCORRECTO: Antes del análisis
validation = await opencode.validate(...)
if validation.ok:
    analysis = await core_detector.detect(...)  # ¡NO!

# ❌ INCORRECTO: Como dependencia crítica
if not opencode_available:
    raise Error("Cannot proceed")  # ¡NO!
```

---

## NUEVO VALIDADOR - CARACTERÍSTICAS

### ✅ Lo que SÍ hace:

1. **Recibe análisis REAL**
   - De `CoreAnomalyDetector`
   - Con mediciones de APIs satelitales reales
   - Score base determinista

2. **Consulta BD de sitios documentados**
   - PostgreSQL con 7,844 sitios reales
   - Query espacial con PostGIS
   - Calcula distancias reales

3. **Contrasta datos REALES**
   - Mediciones reales vs sitios conocidos
   - Determina status del candidato
   - Lógica basada en datos, no simulación

4. **Valida coherencia lógica (OpenCode)**
   - Solo para probabilidad > 0.7
   - DESPUÉS del análisis
   - Asíncrono, no bloquea
   - Opcional (no crítico)

5. **Crea registro en BD**
   - Guarda mediciones REALES
   - Sitios documentados cercanos
   - Validación lógica (si aplica)
   - Status determinado

### ❌ Lo que NO hace:

1. ❌ Inventar datos
2. ❌ Simular mediciones
3. ❌ Usar np.random
4. ❌ Llamar OpenCode en loop
5. ❌ Bloquear el flujo principal

---

## EJEMPLO DE USO

```python
from backend.core_anomaly_detector import CoreAnomalyDetector
from backend.validation.known_sites_validator import KnownSitesValidator
from backend.database import db

# 1. Inicializar componentes
core_detector = CoreAnomalyDetector(
    environment_classifier=env_classifier,
    real_validator=real_validator,
    data_loader=data_loader
)

validator = KnownSitesValidator(
    db_connection=db,
    opencode_client=opencode  # Opcional
)

# 2. Analizar zona con DATOS REALES
analysis_result = await core_detector.detect_anomaly(
    lat=13.1631,
    lon=-72.5450,
    lat_min=13.1531,
    lat_max=13.1731,
    lon_min=-72.5550,
    lon_max=-72.5350,
    region_name="Machu Picchu Area"
)

# analysis_result contiene:
# - measurements: Lista de InstrumentMeasurement (DATOS REALES)
# - archaeological_probability: 0.87 (calculado con datos reales)
# - confidence_level: "high"
# - environment_type: "mountain"

# 3. Validar contra sitios documentados
validation_result = await validator.validate_analysis(
    analysis_result=analysis_result,  # ← DATOS REALES
    lat_min=13.1531,
    lat_max=13.1731,
    lon_min=-72.5550,
    lon_max=-72.5350,
    region_name="Machu Picchu Area"
)

# validation_result contiene:
# - real_measurements: Mediciones de APIs satelitales
# - documented_sites_nearby: [DocumentedSite("Machu Picchu", distance=0.3km)]
# - logical_validation: {coherence_score: 0.92, ...}
# - candidate_id: "cand_a1b2c3d4e5f6"
# - candidate_status: "validated"

# 4. Usar resultado
print(f"✅ Candidato creado: {validation_result.candidate_id}")
print(f"📊 Status: {validation_result.candidate_status}")
print(f"🎯 Probabilidad: {validation_result.archaeological_probability:.2%}")

if validation_result.closest_site:
    print(f"📍 Sitio más cercano: {validation_result.closest_site.name}")
    print(f"📏 Distancia: {validation_result.distance_to_closest_km:.2f} km")

if validation_result.logical_validation:
    print(f"🧠 Coherencia lógica: {validation_result.logical_validation['coherence_score']:.2f}")
```

---

## ESTRUCTURA DE DATOS

### ValidationResult

```python
{
    "validation_id": "val_a1b2c3d4e5f6",
    "analysis_date": "2026-01-26T15:30:00",
    
    # Ubicación
    "center_lat": 13.1631,
    "center_lon": -72.5450,
    "area_analyzed_km2": 4.0,
    
    # Mediciones REALES
    "real_measurements": [
        {
            "instrument": "sentinel_2_ndvi",
            "value": 0.45,
            "threshold": 0.40,
            "exceeds_threshold": true,
            "confidence": "high",
            "notes": "Fuente: Copernicus Sentinel-2 | Fecha: 2026-01-20"
        },
        {
            "instrument": "sentinel_1_sar",
            "value": -8.5,
            "threshold": -10.0,
            "exceeds_threshold": true,
            "confidence": "moderate",
            "notes": "Fuente: Copernicus Sentinel-1 | Fecha: 2026-01-19"
        }
    ],
    
    # Resultado de detección
    "anomaly_detected": true,
    "archaeological_probability": 0.87,
    "confidence_level": "high",
    
    # Sitios documentados
    "documented_sites_nearby": [
        {
            "id": "site_12345",
            "name": "Machu Picchu",
            "distance_km": 0.3,
            "confidence_level": "CONFIRMED",
            "source": "excavated"
        }
    ],
    
    # Validación lógica (OpenCode)
    "logical_validation": {
        "coherence_score": 0.92,
        "logical_consistency": "high",
        "explanation": "Convergencia instrumental consistente con sitio monumental...",
        "flags": [],
        "recommendations": ["Validación en terreno recomendada"]
    },
    
    # Candidato creado
    "candidate_id": "cand_a1b2c3d4e5f6",
    "candidate_status": "validated"
}
```

---

## REGLAS ABSOLUTAS

### 1. JAMÁS INVENTAR DATOS

```python
# ❌ PROHIBIDO
np.random.seed(...)
fake_value = np.random.uniform(...)

# ✅ CORRECTO
real_value = await real_data_integrator.get_measurement(...)
```

### 2. OpenCode DESPUÉS, nunca antes

```python
# ❌ PROHIBIDO
validation = await opencode.validate(...)
if validation.ok:
    analysis = await detect(...)

# ✅ CORRECTO
analysis = await detect(...)
if analysis.probability > 0.7:
    validation = await opencode.validate(...)
```

### 3. NO bloquear el flujo principal

```python
# ❌ PROHIBIDO
for candidate in candidates:
    await opencode.validate(candidate)  # Bloquea

# ✅ CORRECTO
high_value = [c for c in candidates if c.probability > 0.7]
validations = await asyncio.gather(*[
    opencode.validate(c) for c in high_value
])
```

### 4. Cachear TODO

```python
# ✅ CORRECTO
cache_key = f"{candidate_hash}_{task_type}"
if cache_key in cache:
    return cache[cache_key]

validation = await opencode.validate(...)
cache[cache_key] = validation
```

---

## COMPARACIÓN ANTES/DESPUÉS

| Aspecto | ANTES | AHORA |
|---------|-------|-------|
| **Datos** | ❌ Inventados (np.random) | ✅ Reales (APIs satelitales) |
| **Análisis** | ❌ Simulado | ✅ CoreAnomalyDetector real |
| **BD** | ❌ Hardcoded | ✅ PostgreSQL (7,844 sitios) |
| **Validación** | ❌ No existía | ✅ OpenCode (opcional) |
| **Candidatos** | ❌ No se guardaban | ✅ Registro en BD |
| **Reproducible** | ⚠️ Parcial (seed) | ✅ Total (datos reales) |
| **Científico** | ❌ No | ✅ Sí |

---

## CONCLUSIÓN

### ✅ LOGROS

1. **Eliminado np.random completamente**
   - Reemplazado por datos reales de APIs
   - Contraste con BD de sitios documentados
   - Validación lógica con OpenCode

2. **Arquitectura correcta**
   - OpenCode DESPUÉS del análisis
   - Asíncrono, no bloquea
   - Opcional, no crítico

3. **Flujo científicamente válido**
   - Mediciones reales → Detección → Contraste → Validación → Registro
   - Reproducible con datos reales
   - Trazabilidad completa

### 🎯 RESULTADO FINAL

**ArcheoScope ahora tiene un validador que:**
- ✅ Solo usa datos REALES
- ✅ Contrasta con sitios documentados REALES
- ✅ Valida coherencia lógica (OpenCode)
- ✅ Crea registros de candidatos en BD
- ✅ Es científicamente válido
- ✅ Es reproducible
- ✅ Es eficiente

---

**Fecha de completación:** 2026-01-26  
**Estado:** ✅ COMPLETADO Y DOCUMENTADO  
**Próximo paso:** Integrar en flujo principal de ArcheoScope

---

*"La ciencia se basa en la verdad, no en la conveniencia."*
