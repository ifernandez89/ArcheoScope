# Parámetros Enviados a la IA para Análisis Arqueológico

## 📋 Resumen Ejecutivo

Cuando ArcheoScope analiza un sitio, envía estos parámetros a Ollama/OpenRouter:

---

## 🔧 Configuración del Modelo

### Parámetros de Ollama (backend/ai/archaeological_assistant.py línea 338-348)

```python
payload = {
    "model": "phi4-mini-reasoning:latest",  # o qwen2.5:3b-instruct
    "prompt": "[PROMPT LARGO - ver abajo]",
    "stream": False,
    "options": {
        "temperature": 0.3,      # Más determinista (0-1, default 0.8)
        "top_p": 0.9,           # Nucleus sampling (0-1, default 0.9)
        "num_predict": 200      # Máximo tokens a generar (REDUCIDO de 500)
    }
}

# Timeout
timeout = 30  # segundos (REDUCIDO de 120)
```

---

## 📝 Estructura del Prompt

### Versión OPTIMIZADA (Actual - Corta)

```
Análisis arqueológico de [NOMBRE_REGION] ([AREA] km²).

Anomalías detectadas:
- thermal_anomalies: prob=0.75
- sar_backscatter: prob=0.65
- ndvi_stress: prob=0.55

Proporciona en 2-3 frases:
1. Qué patrones se detectaron
2. Posible interpretación arqueológica (cauteloso)
3. Recomendación principal

Sé breve y científico.
```

**Longitud**: ~150-200 caracteres
**Tokens estimados**: ~50-70 tokens de entrada

---

### Versión ANTERIOR (Larga - PROBLEMA)

```
[PROMPT BASE LARGO - 500+ caracteres]

CONTEXTO REGIONAL:
- Región: Giza Pyramids Complex
- Área: 10,000 km²
- Coordenadas: 29.9792, 31.1342
- Tipo de paisaje: Mixto

ANOMALÍAS DETECTADAS:

1. Tipo: thermal_anomalies
   - Probabilidad arqueológica: 0.75
   - Coherencia geométrica: 0.85
   - Persistencia temporal: 0.90
   - Píxeles afectados: 1,234
   - Características: buried_structures, thermal_inertia

2. Tipo: sar_backscatter
   - Probabilidad arqueológica: 0.65
   - Coherencia geométrica: 0.70
   - Persistencia temporal: 0.80
   - Píxeles afectados: 987
   - Características: surface_roughness, geometric_patterns

[... más anomalías ...]

EVALUACIONES DE REGLAS:

- rule_1: anomalous
  Probabilidad arqueológica: 0.80
  Violaciones: vegetation_decoupling, thermal_persistence

[... más reglas ...]

TAREA:
Analiza estos hallazgos desde una perspectiva arqueológica científica. Proporciona:

1. EXPLICACIÓN CLARA: ¿Qué patrones espaciales se detectaron?
2. INTERPRETACIÓN ARQUEOLÓGICA: ¿Qué podrían indicar estos patrones? (cauteloso)
3. RAZONAMIENTO CIENTÍFICO: ¿Por qué estos patrones son significativos?
4. EVALUACIÓN DE CONFIANZA: ¿Qué tan confiables son estas interpretaciones?
5. LIMITACIONES: ¿Qué no podemos concluir con certeza?
6. RECOMENDACIONES: ¿Qué investigación adicional se necesita?

Recuerda: Nunca afirmes descubrimientos definitivos. Usa lenguaje científico cauteloso.
```

**Longitud**: ~2000-3000 caracteres
**Tokens estimados**: ~600-900 tokens de entrada
**PROBLEMA**: Demasiado largo, hace que phi4 tarde 60+ segundos

---

## 🎯 Datos de Entrada Reales

### Ejemplo: Análisis de Giza Pyramids

```json
{
  "anomalies": [
    {
      "type": "thermal_anomalies",
      "archaeological_probability": 0.75,
      "geometric_coherence": 0.85,
      "temporal_persistence": 0.90,
      "affected_pixels": 1234,
      "suspected_features": ["buried_structures", "thermal_inertia"]
    },
    {
      "type": "sar_backscatter",
      "archaeological_probability": 0.65,
      "geometric_coherence": 0.70,
      "temporal_persistence": 0.80,
      "affected_pixels": 987,
      "suspected_features": ["surface_roughness", "geometric_patterns"]
    },
    {
      "type": "ndvi_stress",
      "archaeological_probability": 0.55,
      "geometric_coherence": 0.60,
      "temporal_persistence": 0.75,
      "affected_pixels": 654,
      "suspected_features": ["vegetation_suppression"]
    }
  ],
  "rule_evaluations": {
    "vegetation_decoupling": {
      "result": "anomalous",
      "archaeological_probability": 0.80,
      "rule_violations": ["ndvi_topography_mismatch"]
    },
    "thermal_persistence": {
      "result": "anomalous",
      "archaeological_probability": 0.75,
      "rule_violations": ["day_night_thermal_anomaly"]
    }
  },
  "context": {
    "region_name": "Giza Pyramids Complex",
    "area_km2": 10000,
    "coordinates": "29.9792, 31.1342",
    "landscape_type": "desert",
    "analysis_type": "remote_sensing_archaeology"
  }
}
```

---

## ⏱️ Tiempos de Procesamiento

### Con Prompt LARGO (Anterior)
- **phi4-mini-reasoning**: 60-120 segundos ❌
- **qwen2.5:3b-instruct**: 90-180 segundos ❌
- **Causa**: Demasiados tokens de entrada + 500 tokens de salida

### Con Prompt CORTO (Optimizado)
- **phi4-mini-reasoning**: 15-30 segundos ✅ (esperado)
- **qwen2.5:3b-instruct**: 20-40 segundos ✅ (esperado)
- **Mejora**: ~75% más rápido

---

## 🔍 Flujo Completo de Llamada a IA

### 1. Endpoint `/analyze` recibe request
```python
request = {
    "lat_min": 29.969,
    "lat_max": 29.989,
    "lon_min": 31.124,
    "lon_max": 31.144,
    "region_name": "Giza Pyramids",
    "resolution_m": 1000
}
```

### 2. Sistema detecta anomalías
- Clasificación de ambiente: `desert`
- Mediciones instrumentales: 3 instrumentos
- Convergencia: 2/3 instrumentos exceden umbral
- Probabilidad arqueológica: 0.75

### 3. Se prepara llamada a IA
```python
# backend/api/main.py línea ~1970
ai_explanations = perform_archaeological_ai_explanation(
    spatial_results,      # Resultados espaciales
    archaeological_results  # Resultados arqueológicos
)
```

### 4. Se construye prompt
```python
# backend/ai/archaeological_assistant.py línea ~230
prompt = _build_archaeological_prompt(
    anomalies,           # Top 3 anomalías
    rule_evaluations,    # Evaluaciones de reglas
    context             # Contexto regional
)
```

### 5. Se llama a Ollama
```python
# backend/ai/archaeological_assistant.py línea ~338
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi4-mini-reasoning:latest",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 200
        }
    },
    timeout=30
)
```

### 6. Se parsea respuesta
```python
# backend/ai/archaeological_assistant.py línea ~360
result = response.json()
ai_response = result.get('response', '')

# Se estructura en ArchaeologicalExplanation
return ArchaeologicalExplanation(
    explanation=ai_response[:500],
    archaeological_interpretation="...",
    confidence_assessment="...",
    recommendations=[...],
    limitations="...",
    scientific_reasoning="..."
)
```

---

## 🚀 Optimizaciones Implementadas

### ✅ Reducción de Prompt
- **Antes**: 2000-3000 caracteres (~600-900 tokens)
- **Ahora**: 150-200 caracteres (~50-70 tokens)
- **Mejora**: ~90% reducción

### ✅ Reducción de Tokens de Salida
- **Antes**: `num_predict: 500`
- **Ahora**: `num_predict: 200`
- **Mejora**: 60% reducción

### ✅ Reducción de Timeout
- **Antes**: `timeout: 120` segundos
- **Ahora**: `timeout: 30` segundos
- **Mejora**: 75% reducción

### ✅ Solo Top 3 Anomalías
- **Antes**: Todas las anomalías (5-10)
- **Ahora**: Solo las 3 más relevantes
- **Mejora**: Menos datos a procesar

---

## 📊 Comparación de Parámetros

| Parámetro | Antes | Ahora | Mejora |
|-----------|-------|-------|--------|
| Longitud prompt | 2000-3000 chars | 150-200 chars | 90% ↓ |
| Tokens entrada | 600-900 | 50-70 | 92% ↓ |
| Tokens salida | 500 | 200 | 60% ↓ |
| Timeout | 120s | 30s | 75% ↓ |
| Anomalías | Todas (5-10) | Top 3 | 70% ↓ |
| Tiempo esperado | 60-120s | 15-30s | 75% ↓ |

---

## 🎯 Recomendaciones Adicionales

### Si sigue siendo lento:

1. **Usar modelo más rápido**
   ```bash
   # En .env.local cambiar a:
   OLLAMA_MODEL1=qwen2.5:1.5b  # Más pequeño = más rápido
   ```

2. **Reducir aún más tokens**
   ```python
   "num_predict": 100  # En lugar de 200
   ```

3. **Desactivar IA temporalmente**
   ```python
   # En .env.local:
   OLLAMA_ENABLED=false
   ```

4. **Usar solo para análisis final**
   - No llamar IA en cada análisis
   - Solo cuando usuario solicite explicación detallada

---

## 🔧 Archivos Modificados

1. **backend/ai/archaeological_assistant.py**
   - Línea 230-260: Prompt optimizado (corto)
   - Línea 338-348: Parámetros Ollama optimizados
   - Línea 348: Timeout reducido a 30s

2. **backend/api/main.py**
   - Línea ~1970: Llamada a IA en análisis

---

## 💡 Conclusión

El problema principal era:
- ❌ Prompt demasiado largo (2000+ chars)
- ❌ Demasiados tokens de salida (500)
- ❌ Timeout muy alto (120s)
- ❌ Modelo phi4 es lento con prompts largos

Solución implementada:
- ✅ Prompt ultra-corto (150-200 chars)
- ✅ Menos tokens de salida (200)
- ✅ Timeout razonable (30s)
- ✅ Solo top 3 anomalías más relevantes

**Tiempo esperado ahora**: 15-30 segundos por análisis
