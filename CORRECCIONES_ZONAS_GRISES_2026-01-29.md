# 🔧 CORRECCIONES ZONAS GRISES - 2026-01-29

## TU ANÁLISIS (PERFECTO)

---

## 🟡 ZONAS GRISES / RUIDO (AJUSTAR)

### 1. ESS Superficial: matemáticamente válido, semánticamente confuso

**Problema detectado**:
```
ESS Superficial: 0.351 / 0.431 / 0.446
```

Pero:
- Sentinel-1 SAR aporta casi cero peso real (norm=0.003)
- Score empujado por: térmico (MODIS/Landsat) + elevación (SRTM)

**Conclusión**: No mide "arqueología superficial", sino **estabilidad térmica + topografía**

**Corrección**:
```python
# Renombrar internamente
"ess_superficial" → "ess_geo_climatic_proxy"

# O ajustar pesos según hipótesis
if environment_type == "arid":
    weights = {
        'sar': 0.4,      # Aumentar SAR
        'thermal': 0.3,  # Reducir térmico
        'elevation': 0.2,
        'ndvi': 0.1      # Reducir NDVI
    }
```

---

### 2. NDVI extremadamente bajo (0.061)

**Observación**:
```
NDVI ~0.06 = suelo desnudo / árido / mineral
Stress Frequency = 0
NDVI Persistence = 0
```

**Interpretación correcta**:
- ✅ No invalida arqueología
- ✅ Indica: No esperes marcas vegetacionales claras
- ✅ Todo lo interesante viene por: SAR + térmico + microtopografía

**Corrección**: Ajustar mensaje
```python
if ndvi < 0.1:
    notes.append("⚠️ NDVI muy bajo (suelo desnudo) - Detección basada en SAR/térmico/topografía")
```

---

### 3. Mucho "Sin datos superficiales"

**Problema UX**:
```
⚠️ Sin datos superficiales
⚠️ Sin datos superficiales
⚠️ Sin datos superficiales
```

Pero en realidad **SÍ hay datos**, solo que:
- No coinciden con profundidad/capa esperada
- Fueron descartados por filtros

**Corrección**: Mensaje más claro
```python
# Antes
"⚠️ Sin datos superficiales"

# Después
"ℹ️ Datos superficiales fuera de rango esperado (descartados por filtros)"
```

---

## 🔴 PROBLEMAS REALES (CORREGIR)

### 1. VIIRS 403 constante

**Problema**:
```
VIIRS API error: 403
VIIRS API error: 403
VIIRS API error: 403
```

**Impacto**:
- ✅ Marcado como opcional
- ✅ No penaliza
- ❌ Ensucia ruido
- ❌ Da falsa sensación de "sensores caídos"

**Corrección**:
```python
# backend/satellite_connectors/viirs_connector.py

class VIIRSConnector:
    def __init__(self):
        self.available = False  # Desactivar por defecto
        self.disabled_reason = "VIIRS temporarily unavailable (403 Forbidden)"
        logger.info(f"⚠️ VIIRS: {self.disabled_reason}")
    
    async def get_thermal_data(self, ...):
        if not self.available:
            logger.info("ℹ️ VIIRS: Skipped (temporarily unavailable)")
            return None
```

---

### 2. ICESat-2: dato válido descartado

**Problema CRÍTICO**:
```
ICESat-2 processed: 1802 valid points, mean=439.31m
❌ Valor extraído es None/inf/nan
```

**Desconexión**:
- Conector SÍ tiene datos
- Capa de agregación los invalida

**Causa probable**: Bug de normalización o chequeo demasiado estricto

**Corrección**:
```python
# backend/satellite_connectors/real_data_integrator_v2.py

# Extraer valor principal con sanitización
value = None

if hasattr(api_data, 'indices') and api_data.indices:
    indices = api_data.indices
    
    # ICESat-2: elevation_mean puede ser muy alto (>1000m)
    if 'elevation_mean' in indices:
        raw_value = indices['elevation_mean']
        
        # NO normalizar elevación (puede ser >1000m)
        if isinstance(raw_value, (int, float)) and not (np.isnan(raw_value) or np.isinf(raw_value)):
            value = float(raw_value)
            logger.info(f"   ✅ ICESat-2 elevation: {value:.1f}m (sin normalizar)")
```

---

### 3. TAS: correcto pero conservador

**Observación**:
```
TAS = 0.339 (confianza 0.9)
- Alta estabilidad térmica ✔️
- Coherencia SAR moderada ✔️
- Cero señal biológica (esperable)
```

**Problema**: Para regiones áridas, el peso NDVI está sobrando

**Corrección**: TAS adaptativo por environment_type
```python
# backend/temporal_archaeological_signature.py

def calculate_tas(self, environment_type: str):
    """TAS adaptativo según ambiente."""
    
    if environment_type == "arid":
        weights = {
            'thermal_stability': 0.4,  # Aumentar
            'sar_coherence': 0.4,      # Aumentar
            'ndvi_persistence': 0.1,   # Reducir (casi cero en árido)
            'elevation_consistency': 0.1
        }
    elif environment_type == "tropical":
        weights = {
            'thermal_stability': 0.2,
            'sar_coherence': 0.3,
            'ndvi_persistence': 0.3,   # Aumentar (importante en tropical)
            'elevation_consistency': 0.2
        }
    else:  # temperate
        weights = {
            'thermal_stability': 0.3,
            'sar_coherence': 0.3,
            'ndvi_persistence': 0.2,
            'elevation_consistency': 0.2
        }
    
    return self._calculate_weighted_tas(weights)
```

---

## 🧠 LECTURA FINAL (TU CONCLUSIÓN)

### ¿Esto detecta un sitio arqueológico?

**👉 No confirma, pero sí identifica un territorio interesante**

**Clasificación correcta**:
```
🟡 CANDIDATE – Geo-Thermal Stable Zone
Interés: bajo-moderado
Dependiente de: microrelieves y subsuelo somero
```

**No es**:
- ❌ Machu Picchu escondido
- ❌ Ruido aleatorio

**Es**:
- ✅ Zona estable geo-climática
- ✅ Candidato para investigación de campo
- ✅ Requiere validación con GPR/excavación

---

## 📋 PLAN DE CORRECCIÓN

### INMEDIATO (hoy)

1. ✅ **Desactivar VIIRS** (403 constante)
   - Archivo: `backend/satellite_connectors/viirs_connector.py`
   - Cambio: `self.available = False` por defecto

2. ✅ **Corregir ICESat-2** (dato válido descartado)
   - Archivo: `backend/satellite_connectors/real_data_integrator_v2.py`
   - Cambio: No normalizar elevación, solo validar finito

3. ✅ **Mejorar mensajes UX**
   - "Sin datos superficiales" → "Datos fuera de rango esperado"
   - Agregar contexto NDVI bajo

### CORTO PLAZO (mañana)

4. **TAS adaptativo por ambiente**
   - Archivo: `backend/temporal_archaeological_signature.py`
   - Cambio: Pesos dinámicos según `environment_type`

5. **Renombrar ESS Superficial**
   - `ess_superficial` → `ess_geo_climatic_proxy`
   - O ajustar pesos SAR

### OPCIONAL (próxima semana)

6. **Sistema de clasificación de candidatos**
   ```python
   class CandidateClassification(Enum):
       HIGH_CONFIDENCE = "🟢 HIGH - Strong archaeological signals"
       MODERATE = "🟡 MODERATE - Geo-thermal stable zone"
       LOW = "🟠 LOW - Weak signals, requires validation"
       NOISE = "🔴 NOISE - Natural variation"
   ```

---

## 🎯 RESULTADO ESPERADO

### Antes (confuso)
```
ESS Superficial: 0.446
⚠️ Sin datos superficiales
⚠️ Sin datos superficiales
VIIRS API error: 403
ICESat-2: ❌ None
```

### Después (claro)
```
ESS Geo-Climatic: 0.446
ℹ️ NDVI muy bajo (suelo desnudo) - Detección basada en SAR/térmico
ℹ️ VIIRS: Skipped (temporarily unavailable)
ICESat-2: ✅ 439.31m (1802 points)

🟡 CANDIDATE – Geo-Thermal Stable Zone
Interés: bajo-moderado, requiere validación de campo
```

---

**Fecha**: 2026-01-29  
**Análisis**: Usuario (perfecto)  
**Estado**: Plan de corrección definido  
**Próximo paso**: Implementar correcciones
