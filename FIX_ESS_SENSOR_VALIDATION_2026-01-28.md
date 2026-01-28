# FIX CRÍTICO: Validación de Sensores por Tipo - ESS Volumétrico
**Fecha**: 2026-01-28
**Prioridad**: 🔥 CRÍTICA
**Impacto**: Sistema descartando datos válidos → ESS = 0

---

## 🎯 PROBLEMA IDENTIFICADO

### Síntoma
```
[sentinel_2_ndvi] ✅ SUCCESS: 0.463 NDVI (confianza: 1.00)
INFO:etp_generator:    ❌ sentinel_2_ndvi: Sin datos válidos
```

**Contradicción lógica**: Sensor devuelve valor + confianza, pero ETP lo descarta.

**Resultado**: ESS Volumétrico = 0, ESS Temporal = 0, Anomalías = 0

### Causa Raíz
El sistema exige criterios volumétricos/profundos a TODOS los sensores:
- Sentinel-2 NUNCA dará profundidad (es óptico superficial)
- Sentinel-1 NO penetra 2-5m en suelo húmedo
- Landsat thermal NO es estratigráfico

Pero el código los penaliza por no tener datos volumétricos.

---

## 🔧 SOLUCIÓN: Validez por Tipo de Sensor

### Clasificación de Sensores

#### 🌍 Sensores Superficiales (0m)
**Criterio de validez**: `value + confidence > 0.5`
**NO exigir**: profundidad, continuidad 3D, coherencia volumétrica

Sensores:
- `sentinel_2_ndvi` - Vegetación superficial
- `viirs_ndvi` - Vegetación superficial
- `viirs_thermal` - Temperatura superficial
- `srtm_elevation` - Elevación topográfica

**Contribuyen a**: ESS Superficial

#### 📡 Sensores Subsuperficiales (-0.5m a -3m)
**Criterio de validez**: `value + confidence > 0.4 + penetración detectada`

Sensores:
- `sentinel_1_sar` - Penetración ligera (0-0.5m)
- `landsat_thermal` - Inercia térmica subsuperficial
- `modis_lst` - Temperatura subsuperficial
- `palsar_backscatter` - Penetración L-band (0-2m)
- `palsar_penetration` - Penetración profunda (2-5m)

**Contribuyen a**: ESS Subsuperficial

#### 🔬 Sensores Profundos (-5m a -20m)
**Criterio de validez**: `detección de anomalía estructural`

Sensores:
- `palsar_penetration` - Máxima penetración L-band
- `icesat2` - Altimetría láser (inferencia estructural)

**Contribuyen a**: ESS Profundo

---

## 📊 NUEVA ARQUITECTURA ESS

### ESS por Capas (no binario)

```python
# ANTES (binario - TODO O NADA)
if sensor_tiene_datos_volumetricos:
    ess = calcular()
else:
    ess = 0  # ❌ DESCARTA TODO

# DESPUÉS (por capas)
ess_superficial = calcular_desde_sensores_superficiales()
ess_subsuperficial = calcular_desde_sensores_subsuperficiales()
ess_profundo = calcular_desde_sensores_profundos()

ess_volumetrico = (
    ess_superficial * 0.4 +
    ess_subsuperficial * 0.4 +
    ess_profundo * 0.2
)
```

### Pesos por Capa

```python
LAYER_WEIGHTS = {
    'superficial': 0.4,      # Sensores ópticos/térmicos
    'subsuperficial': 0.4,   # SAR, thermal inertia
    'profundo': 0.2          # PALSAR, ICESat-2
}
```

---

## 🛠️ IMPLEMENTACIÓN

### Paso 1: Clasificar Instrumentos por Tipo

```python
# En ETProfileGenerator.__init__()

self.instrument_types = {
    'superficial': [
        'sentinel_2_ndvi', 'viirs_ndvi', 'viirs_thermal', 
        'srtm_elevation', 'landsat_ndvi'
    ],
    'subsuperficial': [
        'sentinel_1_sar', 'landsat_thermal', 'modis_lst',
        'palsar_backscatter', 'palsar_soil_moisture'
    ],
    'profundo': [
        'palsar_penetration', 'icesat2'
    ]
}

self.validation_criteria = {
    'superficial': lambda data: (
        data.get('value', 0) is not None and 
        data.get('confidence', 0) > 0.5
    ),
    'subsuperficial': lambda data: (
        data.get('value', 0) is not None and 
        data.get('confidence', 0) > 0.4
    ),
    'profundo': lambda data: (
        data.get('value', 0) is not None and 
        data.get('confidence', 0) > 0.3
    )
}
```

### Paso 2: Validar por Tipo

```python
def _validate_sensor_data(self, instrument: str, data: Dict[str, Any]) -> bool:
    """Validar datos de sensor según su tipo."""
    
    # Determinar tipo de sensor
    sensor_type = None
    for stype, instruments in self.instrument_types.items():
        if instrument in instruments:
            sensor_type = stype
            break
    
    if not sensor_type:
        sensor_type = 'superficial'  # Default
    
    # Aplicar criterio de validación apropiado
    validation_func = self.validation_criteria[sensor_type]
    
    return validation_func(data)
```

### Paso 3: Calcular ESS por Capas

```python
def _calculate_layered_ess(self, layered_data: Dict[float, Dict[str, Any]]) -> Dict[str, float]:
    """Calcular ESS separado por tipo de capa."""
    
    ess_by_layer = {
        'superficial': 0.0,
        'subsuperficial': 0.0,
        'profundo': 0.0
    }
    
    for depth, layer_data in layered_data.items():
        for instrument, data in layer_data.items():
            # Validar según tipo
            if not self._validate_sensor_data(instrument, data):
                continue
            
            # Determinar tipo
            sensor_type = self._get_sensor_type(instrument)
            
            # Calcular score normalizado
            normalized_score = self._normalize_instrument_value(instrument, data['value'])
            confidence = data.get('confidence', 0.5)
            weighted_score = normalized_score * confidence
            
            # Acumular en capa apropiada
            if sensor_type in ess_by_layer:
                ess_by_layer[sensor_type] += weighted_score
    
    # Normalizar por número de sensores en cada capa
    for layer_type in ess_by_layer:
        sensor_count = len(self.instrument_types[layer_type])
        if sensor_count > 0:
            ess_by_layer[layer_type] /= sensor_count
    
    return ess_by_layer

def _calculate_volumetric_ess_v2(self, layered_data: Dict[float, Dict[str, Any]]) -> float:
    """Calcular ESS volumétrico con validación por tipo."""
    
    ess_by_layer = self._calculate_layered_ess(layered_data)
    
    # Combinar con pesos
    volumetric_ess = (
        ess_by_layer['superficial'] * 0.4 +
        ess_by_layer['subsuperficial'] * 0.4 +
        ess_by_layer['profundo'] * 0.2
    )
    
    return min(1.0, volumetric_ess)
```

---

## 🎯 RESULTADO ESPERADO

### Antes (con bug)
```
Veracruz:
- Sentinel-2 NDVI: 0.463 ✅ → DESCARTADO ❌
- Sentinel-1 SAR: 0.15 ✅ → DESCARTADO ❌
- Landsat Thermal: OK ✅ → DESCARTADO ❌
→ ESS Volumétrico: 0.000

Tabasco:
- Sentinel-2 NDVI: 0.333 ✅ → DESCARTADO ❌
- Sentinel-1 SAR: 0.15 ✅ → DESCARTADO ❌
→ ESS Volumétrico: 0.000
```

### Después (corregido)
```
Veracruz:
- Sentinel-2 NDVI: 0.463 ✅ → VÁLIDO ✅ (superficial)
- Sentinel-1 SAR: 0.15 ✅ → VÁLIDO ✅ (subsuperficial)
- Landsat Thermal: OK ✅ → VÁLIDO ✅ (subsuperficial)
→ ESS Superficial: 0.463
→ ESS Subsuperficial: 0.15
→ ESS Volumétrico: 0.245 (0.463*0.4 + 0.15*0.4)

Tabasco:
- Sentinel-2 NDVI: 0.333 ✅ → VÁLIDO ✅ (superficial)
- Sentinel-1 SAR: 0.15 ✅ → VÁLIDO ✅ (subsuperficial)
→ ESS Superficial: 0.333
→ ESS Subsuperficial: 0.15
→ ESS Volumétrico: 0.193 (0.333*0.4 + 0.15*0.4)
```

---

## 🔥 FIXES ADICIONALES

### FIX 2: VIIRS como Opcional
```python
OPTIONAL_SENSORS = ['viirs_thermal', 'viirs_ndvi']  # 403 Forbidden

def _is_optional_sensor(self, instrument: str) -> bool:
    return instrument in OPTIONAL_SENSORS

# En validación:
if self._is_optional_sensor(instrument) and data.get('status') == 'FAILED':
    # No penalizar ESS
    continue
```

### FIX 3: ICESat-2 por Tracks
```python
# En icesat2_connector.py
def get_tracks_in_bbox(self, lat_min, lat_max, lon_min, lon_max):
    """Buscar tracks que crucen el bbox, no valor medio."""
    tracks = self._query_icesat2_api(bbox)
    
    if not tracks:
        return None  # Neutral, no negativo
    
    return {
        'tracks_found': len(tracks),
        'elevation_range': calculate_range(tracks),
        'confidence': 0.7 if len(tracks) > 3 else 0.5
    }
```

### FIX 4: PALSAR Bug
```python
# En palsar_connector.py línea donde falla
# ANTES:
result.get('value')  # ❌ result es list

# DESPUÉS:
if isinstance(result, list) and len(result) > 0:
    value = result[0].get('value')
elif isinstance(result, dict):
    value = result.get('value')
```

---

## ✅ VERIFICACIÓN

### Test Cases
1. **Veracruz** (-19.5, -96.4): Debe dar ESS > 0.2
2. **Tabasco** (-18.0, -92.9): Debe dar ESS > 0.15
3. **Región sin datos**: Debe dar ESS = 0 (correcto)

### Métricas de Éxito
- ✅ Sensores superficiales válidos cuentan para ESS
- ✅ ESS Volumétrico > 0 cuando hay datos válidos
- ✅ VIIRS 403 no penaliza
- ✅ ICESat-2 neutral si no hay tracks

---

**PRIORIDAD**: Implementar FIX 1 AHORA
**IMPACTO**: Sistema pasa de ESS=0 a ESS funcional en regiones con datos
**ESFUERZO**: ~2 horas de código + testing

Refs: #ESS #SensorValidation #CriticalFix #VolumetricESS
