# 🎯 Explicación de Scores y Clasificación de Prioridad

**Fecha**: 2026-01-26  
**Pregunta**: ¿Por qué Egipto (Valle del Nilo) muestra candidatas MEDIUM (amarillo) en lugar de HIGH/CRITICAL (naranja/rojo)?

---

## 🔍 Investigación

### Resultados en Valle del Nilo (Egipto)

**Región**: 25-30°N, 30-35°E  
**Sitios en BD**: 1,743 sitios arqueológicos

---

## 📊 Dos Sistemas de Scoring Diferentes

### 1️⃣ Sistema BASE (Zonas Prioritarias)

**Endpoint**: `/archaeological-sites/recommended-zones-geojson`

**Factores de scoring** (sin enriquecimiento multi-instrumental):
- Prior Cultural: 25%
- Terreno Favorable: 15%
- Complemento LiDAR: 20%
- Gap de Excavación: 10%
- IA Coherencia: 25% (si disponible)
- Documentación: 5%

**Scores en Egipto**:
- HZ_000000: 0.552 → **HIGH** 🟠
- HZ_000005: 0.552 → **HIGH** 🟠
- HZ_000006: 0.546 → **MEDIUM** 🟡
- HZ_000004: 0.531 → **MEDIUM** 🟡
- HZ_000002: 0.526 → **MEDIUM** 🟡
- HZ_000001: 0.524 → **MEDIUM** 🟡
- HZ_000003: 0.521 → **MEDIUM** 🟡

**Clasificación**:
- 🔴 CRITICAL: score > 0.75
- 🟠 HIGH: score > 0.55
- 🟡 MEDIUM: score > 0.35
- 🟢 LOW: score < 0.35

---

### 2️⃣ Sistema ENRIQUECIDO (Multi-Instrumental)

**Endpoint**: `/archaeological-sites/enriched-candidates`

**Factores adicionales**:
- ✅ Señales de 5 instrumentos (LiDAR, SAR, Térmico, Multiespectral, Multitemporal)
- ✅ Convergencia multi-instrumental (cuántos instrumentos detectan)
- ✅ Persistencia temporal (años de persistencia)
- ✅ Interpretación de cada señal

**Scores en Egipto** (MUCHO MÁS ALTOS):
- CND_HZ_000003: **0.692** → **field_validation** ✅
- CND_HZ_000002: **0.692** → **field_validation** ✅
- CND_HZ_000006: **0.677** → **field_validation** ✅
- CND_HZ_000001: **0.672** → **field_validation** ✅
- CND_HZ_000000: **0.645** → **field_validation** ✅

**Convergencia**: 4/4 instrumentos (100%)  
**Persistencia temporal**: 10-11 años ✅

---

## 🎯 ¿Por Qué el Mapa Muestra MEDIUM (Amarillo)?

**Respuesta**: El mapa interactivo (`priority_zones_map.html`) está usando el **endpoint BASE** (`recommended-zones-geojson`), NO el endpoint enriquecido.

**Endpoint actual del mapa**:
```javascript
const url = `${API_BASE}/archaeological-sites/recommended-zones-geojson?...`;
```

**Debería usar**:
```javascript
const url = `${API_BASE}/archaeological-sites/enriched-candidates?...`;
```

---

## 🔥 ¿Qué se Necesita para CRITICAL (Rojo)?

### Opción 1: Sistema BASE

Para que una zona sea **CRITICAL** en el sistema base, necesita:

**Score > 0.75**, lo cual requiere:

1. **Alta densidad cultural** (muchos sitios conocidos cerca)
2. **LiDAR disponible + no excavado** (GOLD CLASS) = +0.20
3. **IA coherencia alta** (score > 0.8) = +0.20
4. **Terreno muy favorable** (desierto) = +0.135
5. **Prior cultural alto** (zona caliente) = +0.25

**Ejemplo de zona CRITICAL**:
```
Prior cultural: 0.9 × 0.25 = 0.225
Terreno: 0.9 × 0.15 = 0.135
LiDAR GOLD: 1.0 × 0.20 = 0.200
Excavación gap: 1.0 × 0.10 = 0.100
IA coherencia: 0.9 × 0.25 = 0.225
Documentación: 0.8 × 0.05 = 0.040
-----------------------------------
TOTAL: 0.925 → CRITICAL 🔴
```

### Opción 2: Sistema ENRIQUECIDO

Para que una candidata sea **field_validation** (máxima prioridad):

**Score multi-instrumental > 0.75 Y convergencia > 0.6**, O  
**Persistencia temporal ≥ 10 años**

**Egipto YA cumple esto**:
- ✅ Scores: 0.692, 0.677, 0.672, 0.645
- ✅ Convergencia: 100% (4/4 instrumentos)
- ✅ Persistencia: 10-11 años
- ✅ Acción: **field_validation**

---

## 🛠️ Solución

### Opción A: Actualizar el Mapa para Usar Candidatas Enriquecidas

**Ventajas**:
- ✅ Scores más altos y precisos
- ✅ Convergencia multi-instrumental
- ✅ Persistencia temporal
- ✅ Interpretación de señales

**Desventajas**:
- ⚠️ Más lento (procesa instrumentos)
- ⚠️ Requiere datos instrumentales

### Opción B: Ajustar Umbrales del Sistema BASE

**Cambiar umbrales**:
```python
# Actual
if final_score > 0.75:  # CRITICAL
if final_score > 0.55:  # HIGH
if final_score > 0.35:  # MEDIUM

# Propuesto
if final_score > 0.65:  # CRITICAL (más accesible)
if final_score > 0.50:  # HIGH
if final_score > 0.30:  # MEDIUM
```

**Ventajas**:
- ✅ Más zonas CRITICAL/HIGH
- ✅ Rápido (no procesa instrumentos)

**Desventajas**:
- ⚠️ Menos selectivo
- ⚠️ Puede generar más falsos positivos

### Opción C: Híbrido (RECOMENDADO)

1. **Mapa inicial**: Usar sistema BASE (rápido)
2. **Al hacer clic en zona**: Enriquecer con multi-instrumental
3. **Mostrar score actualizado**: Con convergencia y persistencia

**Ventajas**:
- ✅ Rápido para exploración inicial
- ✅ Preciso cuando se necesita
- ✅ Mejor UX

---

## 📊 Comparación de Scores: Egipto

| Zona | Score BASE | Clase BASE | Score ENRIQUECIDO | Convergencia | Persistencia | Acción |
|------|------------|------------|-------------------|--------------|--------------|--------|
| HZ_000003 | 0.521 | MEDIUM 🟡 | **0.692** | 4/4 (100%) | 11 años | field_validation ✅ |
| HZ_000002 | 0.526 | MEDIUM 🟡 | **0.692** | 4/4 (100%) | 11 años | field_validation ✅ |
| HZ_000006 | 0.546 | MEDIUM 🟡 | **0.677** | 4/4 (100%) | 11 años | field_validation ✅ |
| HZ_000001 | 0.524 | MEDIUM 🟡 | **0.672** | 4/4 (100%) | 11 años | field_validation ✅ |
| HZ_000000 | 0.552 | HIGH 🟠 | **0.645** | 4/4 (100%) | 10 años | field_validation ✅ |

**Conclusión**: El sistema enriquecido **aumenta los scores en ~0.15 puntos** gracias a:
- Convergencia multi-instrumental
- Persistencia temporal
- Señales instrumentales reales

---

## 🎯 Recomendación Final

**Para el Valle del Nilo (Egipto)**:

Las candidatas **SÍ son de alta prioridad** cuando se usa el sistema enriquecido:
- ✅ 5 candidatas con **field_validation**
- ✅ Scores: 0.645-0.692
- ✅ Convergencia: 100%
- ✅ Persistencia: 10-11 años

**El mapa muestra MEDIUM (amarillo) porque usa el sistema BASE sin enriquecimiento.**

**Solución inmediata**:
1. Usar endpoint `/enriched-candidates` en el mapa
2. O ajustar umbrales del sistema BASE
3. O implementar enriquecimiento on-demand al hacer clic

---

## 🔬 Señales Detectadas en Egipto

**Instrumentos que detectan anomalías**:
- ✅ **SAR**: 13/13 candidatas (100%) - Compactación alta
- ✅ **Multiespectral**: 13/13 candidatas (100%) - Estrés vegetal
- ✅ **Térmico**: 11/13 candidatas (85%) - Inercia térmica
- ✅ **Multitemporal**: 10/13 candidatas (77%) - Persistencia 8-11 años

**Interpretaciones**:
- "High compaction detected (roads, platforms, walls)"
- "Buried structures detected (warmer at night, cooler at day)"
- "Vegetation stress detected (altered soil chemistry)"
- "High persistence (11 years) - NOT natural fluctuation"

**Esto es evidencia FUERTE de actividad humana antigua.**

---

## 💡 Conclusión

**Pregunta**: ¿Qué debería haber en la zona para que sea rojo (CRITICAL)?

**Respuesta**:

1. **En el sistema BASE**: Score > 0.75 (requiere LiDAR GOLD + IA coherencia alta + prior cultural muy alto)

2. **En el sistema ENRIQUECIDO**: Egipto **YA tiene candidatas de máxima prioridad** (field_validation) con scores 0.645-0.692

3. **El problema es visual**: El mapa usa el sistema BASE que muestra scores más bajos

**Egipto NO tiene un problema de prioridad, tiene un problema de visualización.**

---

**Desarrollado**: 2026-01-26  
**Sistema**: ArcheoScope - Archaeological Remote Sensing Engine  
**Versión**: 1.3.0
