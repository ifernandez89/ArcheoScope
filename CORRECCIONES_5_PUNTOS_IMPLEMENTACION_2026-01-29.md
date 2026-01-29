# 🔴 CORRECCIONES 5 PUNTOS - IMPLEMENTACIÓN 2026-01-29

## 📋 ORDEN DE PRIORIDAD: 3 → 2 → 1 → 4 → 5

---

## ✅ 3️⃣ ICESat-2: Señal derivada válida (COMPLETADO)

### Problema
```
Rugosity (std): 15.72 m ← 🔥 señal arqueológica brutal
raw_value = None → instrumento descartado
```

### Solución Implementada
1. ✅ ICESat-2 devuelve `SatelliteData` con `indices`
2. ✅ `indices` contiene: `elevation_std`, `elevation_variance`, `elevation_gradient`
3. ✅ Integrador prioriza `elevation_std` sobre `elevation_mean`
4. ✅ Logging: "ICESat-2 rugosity: X.XXm (señal arqueológica)"

### Archivos Modificados
- `backend/satellite_connectors/icesat2_connector.py`
- `backend/satellite_connectors/real_data_integrator_v2.py`

### Estado
✅ **COMPLETADO** - Commit: `4a3a4ab`

---

## ✅ 2️⃣ Normalización SAR menos agresiva (COMPLETADO)

### Problema
```
sentinel_1_sar: norm = 0.003
"Gracias SAR, sentate y no hables."
```

### Solución Implementada
1. ✅ Creado `backend/sar_enhanced_processing.py`
2. ✅ Normalización regional (50-100km, no global)
3. ✅ Derivados estructurales:
   - Textura (GLCM)
   - Gradiente espacial
   - Anomalías locales (z-score por vecindad)
4. ✅ Índice estructural combinado

### Funciones Implementadas
```python
calculate_sar_texture()        # Homogeneidad, contraste, entropía
calculate_sar_gradient()       # Bordes, estructuras
calculate_sar_local_anomalies() # Outliers locales
normalize_sar_regional()       # Z-score regional
process_sar_enhanced()         # Pipeline completo
```

### Archivos Creados
- `backend/sar_enhanced_processing.py`

### Estado
✅ **COMPLETADO** - Pendiente integración en pipeline

---

## 📋 1️⃣ Penalización implícita por sensores faltantes (PENDIENTE)

### Problema
```
Menos sensores ⇒ menos features ⇒ score más plano
Usuario ve ⚠️⚠️⚠️ ⇒ desconfianza cognitiva
Confunde ausencia de datos con ausencia de señal
```

### Solución Propuesta
1. Agregar `data_coverage_score ∈ [0,1]`
2. Separar:
   - `confidence_level` (qué tan confiable es el score)
   - `anthropic_signal_strength` (qué tan fuerte es la señal)
3. Mensaje UX:
   ```
   "Cobertura parcial (0.42), pero señales térmicas y SAR coherentes detectadas"
   ```

### Implementación
```python
# backend/pipeline/coverage_assessment.py

def calculate_coverage_score(instruments_available: List[str], 
                             instruments_required: List[str]) -> Dict[str, Any]:
    """
    Calcular score de cobertura instrumental.
    
    Returns:
        {
            'coverage_score': float,  # 0-1
            'instruments_available': int,
            'instruments_required': int,
            'missing_instruments': List[str],
            'coverage_quality': str  # FULL, PARTIAL, MINIMAL
        }
    """
    pass

def separate_confidence_and_signal(measurements: List[Measurement]) -> Dict[str, float]:
    """
    Separar confianza de fuerza de señal.
    
    Returns:
        {
            'confidence_level': float,  # Qué tan confiable
            'signal_strength': float,   # Qué tan fuerte
            'coverage_factor': float    # Penalización por cobertura
        }
    """
    pass
```

### Archivos a Crear
- `backend/pipeline/coverage_assessment.py`

### Estado
📋 **PENDIENTE** - Alta prioridad

---

## 📋 4️⃣ TAS environment-aware weighting (PARCIALMENTE COMPLETADO)

### Problema
```
TAS = 0.363 no es bajo para:
- Ambiente árido
- Sin vegetación
- Estructuras enterradas

Modelo piensa: "Si no hay verde → meh"
```

### Solución Parcial Implementada
✅ TAS adaptativo por ambiente (ya implementado)
✅ THERMAL ANCHOR ZONE (thermal > 0.9)

### Solución Completa Propuesta
```python
# Ajustar pesos dinámicamente según señales detectadas
if environment == "arid":
    if thermal_stability > 0.9:
        w_thermal *= 1.5  # Aumentar más
    if ndvi_persistence < 0.1:
        w_ndvi *= 0.2     # Reducir más
    if sar_structural_index > 0.5:
        w_sar *= 1.4      # Aumentar SAR estructural
```

### Archivos a Modificar
- `backend/temporal_archaeological_signature.py` (ya modificado parcialmente)

### Estado
⚠️ **PARCIALMENTE COMPLETADO** - Mejorar pesos dinámicos

---

## 📋 5️⃣ Conclusión explícita y narrativa científica (PENDIENTE)

### Problema
```
Sistema sabe que es interesante...
pero habla como si tuviera miedo de afirmarlo
```

### Solución Propuesta
```python
# backend/scientific_narrative.py

def generate_archaeological_narrative(analysis_results: Dict[str, Any]) -> str:
    """
    Generar narrativa científica explícita.
    
    Ejemplo:
    "Candidato arqueológico de baja visibilidad superficial. 
    Alta estabilidad térmica multidecadal sugiere estructuras 
    enterradas o uso humano prolongado no monumental. 
    Recomendado para análisis focalizado SAR + térmico de alta resolución."
    """
    
    narrative_parts = []
    
    # 1. Clasificación principal
    if thermal_stability > 0.9:
        narrative_parts.append(
            "Candidato arqueológico de baja visibilidad superficial"
        )
    
    # 2. Evidencia principal
    if thermal_stability > 0.9:
        narrative_parts.append(
            f"Alta estabilidad térmica multidecadal ({thermal_stability:.2f}) "
            "sugiere estructuras enterradas o uso humano prolongado no monumental"
        )
    
    if sar_structural_index > 0.5:
        narrative_parts.append(
            f"Anomalías estructurales SAR ({sar_structural_index:.2f}) "
            "indican heterogeneidad subsuperficial coherente"
        )
    
    # 3. Recomendación accionable
    recommendations = []
    if thermal_stability > 0.9:
        recommendations.append("análisis térmico de alta resolución")
    if sar_structural_index > 0.5:
        recommendations.append("SAR multi-temporal")
    if icesat2_rugosity > 10:
        recommendations.append("LIDAR aéreo")
    
    if recommendations:
        narrative_parts.append(
            f"Recomendado para: {', '.join(recommendations)}"
        )
    
    return ". ".join(narrative_parts) + "."
```

### Archivos a Crear
- `backend/scientific_narrative.py`

### Estado
📋 **PENDIENTE** - Alta prioridad (impacto UX enorme)

---

## 📊 RESUMEN DE ESTADO

| # | Corrección | Estado | Prioridad | Impacto |
|---|------------|--------|-----------|---------|
| 3 | ICESat-2 señal derivada | ✅ COMPLETADO | CRÍTICO | Alto |
| 2 | SAR normalización | ✅ COMPLETADO | CRÍTICO | Alto |
| 1 | Cobertura vs señal | 📋 PENDIENTE | ALTO | Medio |
| 4 | TAS environment-aware | ⚠️ PARCIAL | MEDIO | Medio |
| 5 | Narrativa científica | 📋 PENDIENTE | ALTO | Alto (UX) |

---

## 🚀 PRÓXIMOS PASOS

### Inmediato (hoy)
1. ✅ Commitear SAR enhanced processing
2. 📋 Implementar coverage_assessment.py
3. 📋 Implementar scientific_narrative.py

### Corto plazo (mañana)
4. 📋 Integrar SAR enhanced en pipeline
5. 📋 Mejorar TAS pesos dinámicos
6. 📋 Test completo con caso real

### Medio plazo (próxima semana)
7. 📋 Validar con arqueólogos
8. 📋 Ajustar narrativa según feedback
9. 📋 Documentar sistema completo

---

## 🎯 IMPACTO ESPERADO

### ANTES
```
Coverage: 38.5%
SAR: norm=0.003 (ignorado)
ICESat-2: raw_value=None (descartado)
TAS: 0.363 (conservador)
Conclusión: "Zona con anomalías térmicas" (vago)
```

### DESPUÉS
```
Coverage: 45%+ (ICESat-2 recuperado)
SAR: structural_index=0.52 (señal principal)
ICESat-2: rugosity=15.72m (señal arqueológica)
TAS: 0.58 (realista con thermal anchor)
Conclusión: "Candidato arqueológico de baja visibilidad superficial. 
Alta estabilidad térmica multidecadal sugiere estructuras enterradas. 
Recomendado para SAR + térmico de alta resolución."
```

---

**Fecha**: 2026-01-29  
**Estado**: 2/5 completadas, 3/5 pendientes  
**Próximo paso**: Implementar coverage_assessment.py + scientific_narrative.py

