# 🎯 CORRECCIONES FINALES - 5 PUNTOS CRÍTICOS

## 📊 ANÁLISIS DEL USUARIO (PERFECTO)

Región analizada: Altiplano andino (-16.55, -68.67)

**Diagnóstico**:
```
Esta región NO es "ruido". Es un candidato de baja visibilidad superficial,
pero con firma térmica + estabilidad estructural → típico de:
- Ocupación antigua
- Estructuras erosionadas
- Uso humano prolongado pero no monumental
```

---

## 1️⃣ NDVI BAJO Y SIN PERSISTENCIA

### Problema Identificado
```
NDVI: 0.061 (muy bajo)
NDVI Persistence: 0.000 (sin señal temporal)
```

**Qué pasa**: Ambiente árido o muy degradado → NDVI no sirve como señal fuerte.

### Solución Implementada (Parcial)

**Ya hecho**: TAS adaptativo reduce peso NDVI en árido (10% vs 30%)

**Pendiente**:
1. **Agregar NDWI** (Normalized Difference Water Index)
   - Detecta humedad del suelo
   - Útil en árido para detectar paleocauces

2. **Agregar SAVI** (Soil Adjusted Vegetation Index)
   - Corrige reflectancia del suelo
   - Mejor que NDVI en vegetación escasa

3. **Reponderar dinámicamente**:
   ```python
   if ndvi < 0.1 and environment == "arid":
       weights = {
           'thermal': 0.45,  # ↑ Aumentar (señal fuerte)
           'sar': 0.40,      # ↑ Aumentar
           'ndvi': 0.05,     # ↓ Reducir más (casi cero)
           'topo': 0.10
       }
   ```

### Implementación

**Archivo**: `backend/satellite_connectors/planetary_computer.py`

```python
async def get_ndwi_data(self, lat_min, lat_max, lon_min, lon_max):
    """
    Calcular NDWI (Normalized Difference Water Index).
    
    NDWI = (Green - NIR) / (Green + NIR)
    
    Detecta:
    - Humedad del suelo
    - Paleocauces
    - Zonas de acumulación de agua
    """
    # Usar Sentinel-2 bands: B3 (Green), B8 (NIR)
    pass

async def get_savi_data(self, lat_min, lat_max, lon_min, lon_max):
    """
    Calcular SAVI (Soil Adjusted Vegetation Index).
    
    SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)
    L = 0.5 (factor de ajuste de suelo)
    
    Mejor que NDVI en:
    - Vegetación escasa
    - Suelo desnudo
    - Ambientes áridos
    """
    # Usar Sentinel-2 bands: B4 (Red), B8 (NIR)
    pass
```

**Archivo**: `backend/temporal_archaeological_signature.py`

```python
# Ajustar pesos si NDVI < 0.1
if ndvi_persistence < 0.1 and environment_type == "arid":
    weights['ndvi_persistence'] = 0.05  # Reducir más
    weights['thermal_stability'] = 0.45  # Aumentar (señal fuerte)
    logger.info("   ⚠️ NDVI muy bajo - Priorizando thermal + SAR")
```

---

## 2️⃣ SAR CON SEÑAL DÉBIL PERO ESTABLE

### Problema Identificado
```
SAR: 0.052 dB (muy bajo)
SAR Coherence: Alta (std baja)
```

**Qué pasa**: No es ruido, pero tampoco destaca. Señal sutil.

### Solución

**En lugar de valor absoluto, usar**:

1. **Gradiente espacial SAR**
   - Detecta cambios bruscos (bordes de estructuras)
   - Más sensible que valor absoluto

2. **Anomalías locales SAR (z-score por vecindad)**
   - Compara pixel con vecinos
   - Detecta outliers locales

3. **Modo micro-topografía SAR**
   - Patrones lineales (caminos, muros)
   - Patrones geométricos (plataformas, terrazas)

### Implementación

**Archivo**: `backend/satellite_connectors/planetary_computer.py`

```python
async def get_sar_gradient(self, lat_min, lat_max, lon_min, lon_max):
    """
    Calcular gradiente espacial SAR.
    
    Detecta:
    - Bordes de estructuras
    - Cambios bruscos de backscatter
    - Límites de ocupación
    """
    sar_data = await self.get_sar_data(...)
    
    # Calcular gradiente con Sobel
    from scipy import ndimage
    gradient_x = ndimage.sobel(sar_data, axis=0)
    gradient_y = ndimage.sobel(sar_data, axis=1)
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    return {
        'gradient_mean': np.mean(gradient_magnitude),
        'gradient_std': np.std(gradient_magnitude),
        'gradient_max': np.max(gradient_magnitude)
    }

async def get_sar_local_anomalies(self, lat_min, lat_max, lon_min, lon_max):
    """
    Detectar anomalías locales SAR (z-score por vecindad).
    
    Detecta:
    - Outliers locales
    - Estructuras sutiles
    - Patrones no evidentes en valor absoluto
    """
    sar_data = await self.get_sar_data(...)
    
    # Calcular z-score local (ventana 3x3)
    from scipy.ndimage import generic_filter
    
    def local_zscore(window):
        center = window[len(window)//2]
        mean = np.mean(window)
        std = np.std(window)
        if std == 0:
            return 0
        return (center - mean) / std
    
    zscore_map = generic_filter(sar_data, local_zscore, size=3)
    
    # Contar anomalías (|z| > 2)
    anomalies = np.abs(zscore_map) > 2
    anomaly_fraction = np.sum(anomalies) / anomalies.size
    
    return {
        'anomaly_fraction': anomaly_fraction,
        'anomaly_mean_zscore': np.mean(np.abs(zscore_map[anomalies])) if np.any(anomalies) else 0
    }
```

**Archivo**: `backend/human_traces_analysis.py`

```python
def detect_linear_patterns_sar(sar_data: np.ndarray) -> Dict[str, Any]:
    """
    Detectar patrones lineales en SAR (caminos, muros).
    
    Usa Hough Transform para detectar líneas.
    """
    from skimage.transform import hough_line, hough_line_peaks
    from skimage.feature import canny
    
    # Detectar bordes
    edges = canny(sar_data, sigma=2)
    
    # Hough transform
    h, theta, d = hough_line(edges)
    
    # Detectar picos (líneas prominentes)
    h_peaks, angles, dists = hough_line_peaks(h, theta, d, threshold=0.5*np.max(h))
    
    return {
        'linear_features_count': len(h_peaks),
        'dominant_angles': angles.tolist(),
        'linearity_score': len(h_peaks) / 10.0  # Normalizado
    }
```

---

## 3️⃣ TÉRMICO FUERTE Y ESTABLE

### Problema Identificado
```
Thermal Stability: 0.932 (altísima)
```

**Qué pasa**: Señal arqueológica REAL. Estructuras enterradas estabilizan temperatura.

### Solución

1. **Subir peso de Thermal Stability en TAS**
   - Actual: 40% en árido
   - Propuesto: 50% en árido (si thermal > 0.9)

2. **Añadir inercia térmica nocturna vs diurna**
   - Landsat 8/9 tiene banda térmica
   - Comparar día vs noche

3. **Marcar como "thermal anchor zone"**
   - Flag especial para zonas con thermal > 0.9
   - Prioridad alta para validación

### Implementación

**Archivo**: `backend/temporal_archaeological_signature.py`

```python
# Ajustar pesos si thermal_stability > 0.9
if thermal_stability > 0.9 and environment_type == "arid":
    weights['thermal_stability'] = 0.50  # ↑ Aumentar (señal MUY fuerte)
    weights['sar_coherence'] = 0.35
    weights['ndvi_persistence'] = 0.05
    weights['stress_frequency'] = 0.10
    
    logger.info("   🔥 Thermal Stability MUY ALTA (>0.9) - THERMAL ANCHOR ZONE")
    logger.info("   📌 Prioridad alta para validación de campo")

# Añadir flag
if thermal_stability > 0.9:
    tas.flags = ['THERMAL_ANCHOR_ZONE']
    tas.priority = 'HIGH'
```

**Archivo**: `backend/satellite_connectors/planetary_computer.py`

```python
async def get_thermal_inertia(self, lat_min, lat_max, lon_min, lon_max):
    """
    Calcular inercia térmica (día vs noche).
    
    Inercia térmica alta = masa enterrada (estructuras).
    """
    # Landsat 8/9: Band 10 (Thermal)
    # Comparar escenas diurnas vs nocturnas
    
    day_temp = await self.get_thermal_data(..., time='day')
    night_temp = await self.get_thermal_data(..., time='night')
    
    # Inercia = diferencia día-noche (menor = más inercia)
    thermal_inertia = abs(day_temp - night_temp)
    
    return {
        'thermal_inertia': thermal_inertia,
        'day_temp': day_temp,
        'night_temp': night_temp
    }
```

---

## 4️⃣ INSTRUMENTOS OPCIONALES FALLANDO

### Problema Identificado
```
VIIRS: ❌ Skipped
ICESat-2: ⚠️ Degraded (ahora ✅ con rugosidad)
ERA5: ⚠️ Parcial
```

**Qué pasa**: Sistema robusto, pero pierde densidad informativa.

### Solución

1. **Confidence floor dinámico**
   ```python
   if strong_sensors >= 2:
       # No penalizar faltantes
       confidence_penalty = 0.0
   else:
       # Penalizar proporcionalmente
       confidence_penalty = (required_sensors - strong_sensors) * 0.1
   ```

2. **Registrar explícitamente razón de falta**
   ```python
   missing_data_reason = {
       'VIIRS': 'availability',  # API 403
       'ICESat-2': 'seasonal',   # Órbita no cubre
       'ERA5': 'API'             # Timeout
   }
   ```

3. **Mejorar UX**
   ```
   ANTES: ⚠️ Sin datos superficiales
   DESPUÉS: ℹ️ VIIRS no disponible (API 403) - No afecta análisis (2/3 sensores térmicos OK)
   ```

### Implementación

**Archivo**: `backend/instrument_status.py`

```python
class MissingDataReason(Enum):
    AVAILABILITY = "availability"  # API caído, 403, etc.
    SEASONAL = "seasonal"          # Órbita, cobertura temporal
    API_ERROR = "api_error"        # Timeout, error de red
    NO_COVERAGE = "no_coverage"    # Región fuera de cobertura
    QUALITY = "quality"            # Datos de baja calidad descartados

def calculate_confidence_with_floor(strong_sensors: int, required_sensors: int) -> float:
    """
    Calcular confianza con floor dinámico.
    
    Si ≥2 sensores fuertes → no penalizar faltantes.
    """
    if strong_sensors >= 2:
        return 1.0  # No penalizar
    else:
        penalty = (required_sensors - strong_sensors) * 0.1
        return max(0.5, 1.0 - penalty)  # Floor en 0.5
```

**Archivo**: `backend/satellite_connectors/real_data_integrator_v2.py`

```python
# Registrar razón de falta
if result.status == "FAILED":
    if "403" in result.error_details:
        result.missing_reason = MissingDataReason.AVAILABILITY
    elif "timeout" in result.error_details.lower():
        result.missing_reason = MissingDataReason.API_ERROR
    elif "no granules" in result.error_details.lower():
        result.missing_reason = MissingDataReason.NO_COVERAGE

# Mensaje UX mejorado
if result.missing_reason == MissingDataReason.AVAILABILITY:
    logger.info(f"ℹ️ {instrument_name} no disponible (API) - No afecta análisis ({strong_sensors}/{required_sensors} sensores OK)")
```

---

## 5️⃣ ESS SUPERFICIAL REPETIDO Y SIN FUSIÓN FINAL

### Problema Identificado
```
Se calculan muchos ESS superficiales parciales:
- sentinel_1_sar + modis
- sentinel_1_sar + landsat
- sentinel_2_ndvi + srtm

Pero no se ve un ESS consolidado jerárquico.
```

### Solución

**Crear ESS_FINAL con pesos por familia**:

```python
ESS_FINAL = 0.4 * thermal + 0.35 * sar + 0.25 * topo
```

### Implementación

**Archivo**: `backend/explainability/explanatory_strangeness_score.py`

```python
class ESSFamily(Enum):
    THERMAL = "thermal"      # MODIS, Landsat, VIIRS
    SAR = "sar"              # Sentinel-1, PALSAR
    TOPOGRAPHY = "topo"      # SRTM, ICESat-2, OpenTopo
    OPTICAL = "optical"      # Sentinel-2, Landsat
    CLIMATE = "climate"      # ERA5, CHIRPS

def calculate_ess_final(measurements: List[InstrumentMeasurement]) -> Dict[str, float]:
    """
    Calcular ESS_FINAL consolidado por familia.
    
    Evita redundancia y crea decisión única accionable.
    """
    
    # Agrupar por familia
    families = {
        ESSFamily.THERMAL: [],
        ESSFamily.SAR: [],
        ESSFamily.TOPOGRAPHY: [],
        ESSFamily.OPTICAL: [],
        ESSFamily.CLIMATE: []
    }
    
    for m in measurements:
        family = classify_instrument_family(m.instrument_name)
        families[family].append(m)
    
    # Calcular ESS por familia (una vez)
    ess_thermal = calculate_ess_family(families[ESSFamily.THERMAL])
    ess_sar = calculate_ess_family(families[ESSFamily.SAR])
    ess_topo = calculate_ess_family(families[ESSFamily.TOPOGRAPHY])
    ess_optical = calculate_ess_family(families[ESSFamily.OPTICAL])
    ess_climate = calculate_ess_family(families[ESSFamily.CLIMATE])
    
    # Pesos por familia (ajustables por ambiente)
    weights = {
        ESSFamily.THERMAL: 0.40,      # Inercia térmica (señal fuerte)
        ESSFamily.SAR: 0.35,           # Estructura (penetración)
        ESSFamily.TOPOGRAPHY: 0.25,    # Preservación (contexto)
        ESSFamily.OPTICAL: 0.00,       # No usar en árido (NDVI bajo)
        ESSFamily.CLIMATE: 0.00        # Contextual, no directo
    }
    
    # ESS_FINAL consolidado
    ess_final = (
        ess_thermal * weights[ESSFamily.THERMAL] +
        ess_sar * weights[ESSFamily.SAR] +
        ess_topo * weights[ESSFamily.TOPOGRAPHY]
    )
    
    return {
        'ess_final': ess_final,
        'ess_thermal': ess_thermal,
        'ess_sar': ess_sar,
        'ess_topo': ess_topo,
        'weights': weights,
        'interpretation': interpret_ess_final(ess_final, ess_thermal, ess_sar, ess_topo)
    }

def interpret_ess_final(ess_final: float, ess_thermal: float, ess_sar: float, ess_topo: float) -> str:
    """Interpretar ESS_FINAL de forma accionable."""
    
    if ess_final > 0.7:
        classification = "🟢 HIGH CONFIDENCE"
        action = "Validación de campo prioritaria (GPR + magnetometría)"
    elif ess_final > 0.5:
        classification = "🟡 MODERATE CONFIDENCE"
        action = "Análisis fino recomendado (LIDAR + SAR multi-temporal)"
    elif ess_final > 0.3:
        classification = "🟠 LOW CONFIDENCE"
        action = "Monitoreo continuo (SAR series largas)"
    else:
        classification = "🔴 NOISE"
        action = "No acción requerida"
    
    # Identificar señal dominante
    if ess_thermal > 0.8:
        dominant = "Thermal anchor zone (inercia térmica alta)"
    elif ess_sar > 0.6:
        dominant = "SAR structural anomaly (penetración detecta estructura)"
    elif ess_topo > 0.6:
        dominant = "Topographic preservation (microrrelieve preservado)"
    else:
        dominant = "Multi-sensor convergence (señales débiles pero consistentes)"
    
    return f"{classification} - {dominant}. {action}"
```

---

## 📊 IMPACTO ESPERADO

| Corrección | ANTES | DESPUÉS | Mejora |
|------------|-------|---------|--------|
| **1. NDVI bajo** | Penaliza | NDWI/SAVI + peso 5% | Realista |
| **2. SAR débil** | Valor absoluto | Gradiente + anomalías | Sensible |
| **3. Thermal fuerte** | Peso 40% | Peso 50% + flag | Priorizado |
| **4. Instrumentos faltantes** | Confuso | Razón explícita + floor | Claro |
| **5. ESS repetido** | Redundante | ESS_FINAL consolidado | Accionable |

---

## 🎯 CLASIFICACIÓN FINAL ESPERADA

```
🟡 MODERATE CONFIDENCE - Thermal anchor zone (inercia térmica alta)
Análisis fino recomendado (LIDAR + SAR multi-temporal)

ESS_FINAL: 0.58
├─ Thermal: 0.85 (40% peso) → 0.34
├─ SAR: 0.42 (35% peso) → 0.15
└─ Topo: 0.36 (25% peso) → 0.09

Señal dominante: Thermal Stability (0.932)
Tipo de sitio: Ocupación antigua / Estructuras erosionadas
Recomendación: GPR + magnetometría para validación
```

---

## 📋 PLAN DE IMPLEMENTACIÓN

### FASE 1: Correcciones Inmediatas (hoy)
1. ✅ ICESat-2 rugosidad (completado)
2. 🔧 TAS: Ajustar pesos si thermal > 0.9
3. 🔧 Confidence floor dinámico

### FASE 2: Mejoras SAR (mañana)
4. 🔧 SAR gradiente espacial
5. 🔧 SAR anomalías locales (z-score)

### FASE 3: Consolidación ESS (próxima semana)
6. 🔧 ESS_FINAL por familias
7. 🔧 Interpretación accionable

### FASE 4: Índices adicionales (opcional)
8. 🔧 NDWI (humedad del suelo)
9. 🔧 SAVI (vegetación ajustada)
10. 🔧 Inercia térmica día/noche

---

**Fecha**: 2026-01-29  
**Estado**: 📋 PLAN DEFINIDO  
**Próximo paso**: Implementar FASE 1 (ajustes TAS + confidence floor)

