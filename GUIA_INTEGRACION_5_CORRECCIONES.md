
# GUÍA DE INTEGRACIÓN MANUAL - 5 CORRECCIONES CRÍTICAS
=====================================================

## ✅ 1. SAR Enhanced Processing (COMPLETADO)

Ya integrado en `backend/satellite_connectors/real_data_integrator_v2.py`:
- Import agregado
- Procesamiento SAR mejorado en `get_instrument_measurement_robust()`
- Índice estructural reemplaza normalización agresiva

## 📋 2. Coverage Assessment (PENDIENTE)

### Agregar a `backend/scientific_pipeline.py`:

```python
# En imports (línea ~20)
from pipeline.coverage_assessment import (
    calculate_coverage_score,
    separate_confidence_and_signal,
    CoverageAssessment
)

# En ScientificPipeline.__init__() (línea ~200)
self.coverage_assessment_enabled = True

# En analyze_candidate() - DESPUÉS de phase_a_normalize (línea ~400)
# Calcular coverage score
instruments_available = list(raw_measurements.get('instrumental_measurements', {}).keys())
coverage_assessment = calculate_coverage_score(instruments_available)

# Separar confianza de señal
confidence_signal = separate_confidence_and_signal(
    measurements=list(raw_measurements.get('instrumental_measurements', {}).values()),
    coverage_assessment=coverage_assessment
)

# Agregar a output
output.coverage_raw = coverage_assessment.coverage_score
output.coverage_effective = confidence_signal['coverage_factor']
output.instruments_measured = coverage_assessment.instruments_available
output.instruments_available = coverage_assessment.instruments_total
```

## 📋 3. Scientific Narrative (PENDIENTE)

### Agregar a `backend/scientific_pipeline.py`:

```python
# En imports (línea ~20)
from scientific_narrative import (
    generate_archaeological_narrative,
    ArchaeologicalNarrative
)

# En analyze_candidate() - AL FINAL, antes de return (línea ~800)
# Generar narrativa científica
narrative = generate_archaeological_narrative(
    thermal_stability=tas_result.thermal_stability if tas_result else 0.0,
    sar_structural_index=sar_enhanced_result.get('sar_structural_index', 0.0) if sar_enhanced_result else 0.0,
    icesat2_rugosity=icesat2_rugosity,
    ndvi_persistence=tas_result.ndvi_persistence if tas_result else 0.0,
    tas_score=tas_result.tas_score if tas_result else 0.0,
    coverage_score=coverage_assessment.coverage_score,
    environment_type=raw_measurements.get('environment_type', 'temperate'),
    flags=tas_result.flags if tas_result else []
)

# Agregar a output
output.notes = narrative.full_narrative
output.recommended_action = narrative.recommendations[0] if narrative.recommendations else "Monitoreo continuo"
```

## 🔧 4. TAS Pesos Dinámicos (MEJORA)

### Modificar `backend/temporal_archaeological_signature.py`:

En `_calculate_tas_score()` (línea ~450), agregar ajuste dinámico:

```python
# DESPUÉS de determinar pesos base por ambiente
# Ajustar dinámicamente según señales detectadas
if sar_coherence > 0.5:
    weights['sar_coherence'] *= 1.2  # Aumentar SAR si hay señal fuerte
    weights['ndvi_persistence'] *= 0.9  # Reducir NDVI proporcionalmente

if thermal_stability > 0.85:
    weights['thermal_stability'] *= 1.3  # Aumentar térmico si muy estable
    weights['ndvi_persistence'] *= 0.8  # Reducir NDVI más

# Renormalizar pesos
total_weight = sum(weights.values())
weights = {k: v/total_weight for k, v in weights.items()}
```

## 🧪 5. Test de Integración

Ejecutar:
```bash
python test_5_correcciones_integradas.py
```

Debe mostrar:
- ✅ SAR structural index > 0.3
- ✅ Coverage score separado de signal strength
- ✅ Narrativa científica explícita
- ✅ TAS adaptativo con pesos dinámicos

## 📊 Impacto Esperado

ANTES:
- SAR: norm=0.003 (ignorado)
- Coverage: 38.5% (penaliza score)
- Conclusión: "Zona con anomalías térmicas" (vago)

DESPUÉS:
- SAR: structural_index=0.52 (señal principal)
- Coverage: 45% pero signal_strength=0.7 (separado)
- Conclusión: "Candidato arqueológico de baja visibilidad superficial. 
  Alta estabilidad térmica multidecadal sugiere estructuras enterradas. 
  Recomendado para SAR + térmico de alta resolución."

