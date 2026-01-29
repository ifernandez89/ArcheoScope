# 🔧 CORRECCIONES CRÍTICAS ROUND 2 - 2026-01-29

## 🎯 PROBLEMAS IDENTIFICADOS (ANÁLISIS USUARIO)

### 1️⃣ Redundancia Excesiva en ESS

**Problema**:
```
Calculando ESS superficial muchísimas veces con los mismos pares:
- sentinel_1_sar + modis
- sentinel_1_sar + landsat
- sentinel_2_ndvi + srtm
```

**Impacto**:
- ❌ Cálculos redundantes
- ❌ Tiempo de procesamiento inflado
- ❌ Puntaje inflado artificialmente

**Solución**:
```python
# ANTES: Calcular ESS por cada par de instrumentos
for i1 in instruments:
    for i2 in instruments:
        ess = calculate_ess(i1, i2)  # ❌ Redundante

# DESPUÉS: Agrupar por profundidad, calcular una vez
layers = {
    'superficial': [sentinel_1_sar, sentinel_2_ndvi, modis, landsat],
    'subsuperficial': [icesat2, srtm, palsar],
    'profundo': [gpr, magnetometry]
}

for layer_name, instruments in layers.items():
    ess = calculate_ess_layer(instruments)  # ✅ Una vez por capa
    # Ponderar por diversidad de sensores, no cantidad
```

**Criterio de ponderación**:
- Diversidad de sensores: SAR + Óptico + Térmico = 3 tipos → peso 1.0
- Redundancia: SAR + SAR + SAR = 1 tipo → peso 0.33

---

### 2️⃣ ICESat-2 Desperdiciado

**Problema CRÍTICO**:
```
ICESat-2 processed: 1802 valid points, mean=439.31m
❌ raw_value=None
```

**Causa**:
- Estamos usando `mean` (valor absoluto)
- Deberíamos usar **rugosidad** o **varianza**

**Solución**:
```python
# ANTES (incorrecto)
if 'elevation_mean' in indices:
    value = indices['elevation_mean']  # ❌ Valor absoluto no sirve

# DESPUÉS (correcto)
if 'elevation_std' in indices or 'elevation_variance' in indices:
    # Usar rugosidad/varianza como señal arqueológica
    rugosity = indices.get('elevation_std', 0)
    variance = indices.get('elevation_variance', 0)
    
    # Rugosidad alta = terreno irregular = posible estructura
    value = rugosity if rugosity > 0 else variance
    
    logger.info(f"   ✅ ICESat-2 rugosity: {value:.2f}m (1802 points)")

# O usar gradiente altimétrico
if 'elevation_gradient' in indices:
    value = indices['elevation_gradient']  # Cambio de elevación
```

**Métricas arqueológicas ICESat-2**:
- **Rugosidad (std)**: Detecta irregularidades (muros, montículos)
- **Varianza**: Detecta heterogeneidad (estructuras enterradas)
- **Gradiente**: Detecta terrazas, plataformas
- ❌ **Mean**: NO sirve (valor absoluto sin contexto)

---

### 3️⃣ ERA5 y CHIRPS - raw_value=None

**Problema**:
```
ERA5 descarga perfecto pero luego:
❌ raw_value=None
```

**Causa probable**:
- Filtro temporal muy agresivo
- Umbral descartando valores bajos válidos

**Solución**:
```python
# Revisar filtros en ERA5Connector
async def get_climate_context(self, ...):
    # ANTES: Filtro agresivo
    if value < threshold:  # ❌ Descarta valores bajos válidos
        return None
    
    # DESPUÉS: Validar solo finito
    if isinstance(value, (int, float)) and not (np.isnan(value) or np.isinf(value)):
        return value  # ✅ Acepta valores bajos

# Revisar CHIRPS similar
async def get_precipitation_history(self, ...):
    # Aceptar precipitación baja (0-10mm) en árido
    if precip >= 0 and precip < 1000:  # Rango válido
        return precip
```

---

## 📋 PLAN DE IMPLEMENTACIÓN

### PRIORIDAD 1: ICESat-2 Rugosidad (CRÍTICO)

**Archivo**: `backend/satellite_connectors/icesat2_connector.py`

**Cambios**:
1. Calcular `elevation_std` (rugosidad)
2. Calcular `elevation_variance`
3. Calcular `elevation_gradient` (opcional)
4. Devolver en `indices`

**Archivo**: `backend/satellite_connectors/real_data_integrator_v2.py`

**Cambios**:
1. Priorizar `elevation_std` sobre `elevation_mean`
2. Logging: "ICESat-2 rugosity: X.XXm"

**Impacto esperado**:
- ✅ ICESat-2: raw_value != None
- ✅ Señal arqueológica real (rugosidad)
- ✅ Coverage score: 38.5% → 40%+

---

### PRIORIDAD 2: Redundancia ESS (IMPORTANTE)

**Archivo**: `backend/explainability/explanatory_strangeness_score.py`

**Cambios**:
1. Agrupar instrumentos por profundidad
2. Calcular ESS una vez por capa
3. Ponderar por diversidad de sensores

**Estructura**:
```python
class LayerDefinition:
    SUPERFICIAL = {
        'instruments': ['sentinel_1_sar', 'sentinel_2_ndvi', 'modis_lst', 'landsat_thermal'],
        'sensor_types': ['SAR', 'Optical', 'Thermal'],
        'depth_range': (0, 0.5)  # metros
    }
    
    SUBSUPERFICIAL = {
        'instruments': ['icesat2', 'srtm', 'palsar', 'viirs'],
        'sensor_types': ['LiDAR', 'DEM', 'SAR-L'],
        'depth_range': (0.5, 5)  # metros
    }
    
    PROFUNDO = {
        'instruments': ['gpr', 'magnetometry', 'era5'],
        'sensor_types': ['GPR', 'Magnetic', 'Climate'],
        'depth_range': (5, 50)  # metros
    }

def calculate_ess_by_layer(layer_instruments: List[str]) -> float:
    """Calcular ESS una vez por capa, no por cada par."""
    
    # Obtener mediciones de la capa
    measurements = [get_measurement(inst) for inst in layer_instruments]
    valid_measurements = [m for m in measurements if m is not None]
    
    if len(valid_measurements) < 2:
        return 0.0
    
    # Calcular diversidad de sensores
    sensor_types = set([m.sensor_type for m in valid_measurements])
    diversity_factor = len(sensor_types) / len(valid_measurements)
    
    # Calcular ESS combinado
    ess_combined = calculate_combined_strangeness(valid_measurements)
    
    # Ponderar por diversidad
    ess_weighted = ess_combined * diversity_factor
    
    return ess_weighted
```

**Impacto esperado**:
- ✅ Tiempo de procesamiento: -50%
- ✅ ESS más honesto (no inflado)
- ✅ Ponderación por diversidad

---

### PRIORIDAD 3: ERA5/CHIRPS Filtros (OPCIONAL)

**Archivo**: `backend/satellite_connectors/era5_connector.py`

**Cambios**:
1. Revisar umbrales de validación
2. Aceptar valores bajos válidos
3. Logging explícito de descarte

**Archivo**: `backend/satellite_connectors/chirps_connector.py`

**Cambios**:
1. Aceptar precipitación baja (0-10mm en árido)
2. Validar solo finito, no rango

**Impacto esperado**:
- ✅ ERA5: raw_value != None
- ✅ CHIRPS: raw_value != None
- ✅ Coverage score: +2-3%

---

## 🎯 CLASIFICACIÓN CORRECTA DEL SITIO

```
🟡 CANDIDATE / MONITORING_TARGETED

✔️ NO es Machu Picchu
✔️ NO es ruido
✔️ SÍ es una zona que merece:
   - LIDAR si se puede
   - SAR multi-ángulo
   - Análisis microtopográfico fino
```

**Recomendaciones**:
1. **Validación de campo**: GPR + magnetometría
2. **Análisis fino**: LIDAR aéreo (si disponible)
3. **SAR multi-temporal**: Sentinel-1 series largas
4. **Microtopografía**: DEM de alta resolución (<1m)

---

## 📊 IMPACTO ESPERADO

| Métrica | ACTUAL | ESPERADO | Mejora |
|---------|--------|----------|--------|
| **ICESat-2** | ❌ None | ✅ Rugosity | Recuperado |
| **Coverage Score** | 38.5% | 42-45% | +10% |
| **Tiempo ESS** | 100% | 50% | -50% |
| **ESS Honesto** | Inflado | Ponderado | Realista |
| **ERA5/CHIRPS** | ❌ None | ✅ Valid | Recuperado |

---

## 🧪 TESTS A IMPLEMENTAR

### Test 1: ICESat-2 Rugosidad
```python
async def test_icesat2_rugosity():
    result = await integrator.get_instrument_measurement_robust(
        instrument_name='icesat2',
        lat_min=-16.55, lat_max=-16.54,
        lon_min=-68.67, lon_max=-68.66
    )
    
    assert result.value is not None, "ICESat-2 debe devolver rugosidad"
    assert result.unit == "m", "Unidad debe ser metros"
    assert "rugosity" in result.source.lower() or "std" in result.source.lower()
    print(f"✅ ICESat-2 rugosity: {result.value:.2f}m")
```

### Test 2: ESS No Redundante
```python
def test_ess_no_redundant():
    # Simular 3 instrumentos del mismo tipo
    instruments = ['sar1', 'sar2', 'sar3']
    
    ess_old = calculate_ess_all_pairs(instruments)  # Redundante
    ess_new = calculate_ess_by_layer(instruments)   # Agrupado
    
    assert ess_new < ess_old, "ESS agrupado debe ser menor (no inflado)"
    print(f"ESS redundante: {ess_old:.3f}")
    print(f"ESS agrupado: {ess_new:.3f}")
    print(f"Reducción: {(1 - ess_new/ess_old)*100:.1f}%")
```

### Test 3: ERA5/CHIRPS Válidos
```python
async def test_era5_chirps_valid():
    era5_result = await era5_connector.get_climate_context(...)
    chirps_result = await chirps_connector.get_precipitation_history(...)
    
    assert era5_result is not None, "ERA5 debe devolver datos"
    assert chirps_result is not None, "CHIRPS debe devolver datos"
    
    # Aceptar valores bajos
    assert era5_result.get('temperature') >= 0, "Temperatura válida"
    assert chirps_result.get('precipitation') >= 0, "Precipitación válida (puede ser 0)"
```

---

## 📁 ARCHIVOS A MODIFICAR

### PRIORIDAD 1 (Crítico)
1. `backend/satellite_connectors/icesat2_connector.py`
2. `backend/satellite_connectors/real_data_integrator_v2.py`

### PRIORIDAD 2 (Importante)
3. `backend/explainability/explanatory_strangeness_score.py`
4. `backend/pipeline/scientific_pipeline_with_persistence.py`

### PRIORIDAD 3 (Opcional)
5. `backend/satellite_connectors/era5_connector.py`
6. `backend/satellite_connectors/chirps_connector.py`

---

**Fecha**: 2026-01-29  
**Estado**: 📋 PLAN DEFINIDO  
**Próximo paso**: Implementar PRIORIDAD 1 (ICESat-2 rugosidad)

