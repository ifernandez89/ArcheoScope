# OpenCode/Zen Integration Plan - ArcheoScope

**Fecha:** 2026-01-26  
**Objetivo:** Integrar OpenCode/Zen como herramienta de validación lógica post-scoring  
**Principio:** Complementar, no reemplazar. Nunca en loop crítico.

---

## 🎯 Filosofía de Integración

### ✅ Lo que OpenCode DEBE hacer
- Validar coherencia lógica de candidatos fuertes (score > 0.75)
- Generar explicaciones estructuradas y auditables
- Detectar inconsistencias en evidencia multi-instrumental
- Clasificar semánticamente patrones arqueológicos

### ❌ Lo que OpenCode NO DEBE hacer
- Detección primaria de anomalías
- Scoring de candidatos
- Reemplazar instrumentos deterministas
- Ejecutarse en loops de píxeles

---

## 🏗️ Arquitectura Propuesta

```
[ Instrumentos satelitales ]
         ↓
[ Detección de anomalías ]
         ↓
[ Scoring determinista ]
         ↓
[ Clasificación de terreno ]
         ↓
[ 🧠 OpenCode Validator ]  ← NUEVO (opcional, async)
         ↓
[ Candidato validado + explicación ]
```

**Punto de inserción:** Después del scoring, antes de retornar al usuario.

---

## 📋 Plan de Implementación

### Fase 1: Estructura Base (30 min)

**1.1 Crear módulo validador**

```bash
# Archivo: backend/ai/opencode_validator.py
```

**Responsabilidades:**
- Conexión con OpenCode API/CLI
- Caché de resultados (determinismo)
- Feature flag para habilitar/deshabilitar
- Timeout y error handling

**1.2 Variables de entorno**
```bash
# Agregar a .env.local.example
OPENCODE_ENABLED=false
OPENCODE_API_URL=http://localhost:8080  # o URL de OpenCode
OPENCODE_TIMEOUT=30
OPENCODE_MIN_SCORE=0.75
```

**1.3 Dependencias**
```bash
# Agregar a backend/requirements.txt (si usa HTTP)
# httpx  # ya existe probablemente
# o usar subprocess si es CLI local
```

---

### Fase 2: Implementación del Validador (45 min)

**2.1 Clase OpenCodeValidator**

Estructura básica:
```python
class OpenCodeValidator:
    def __init__(self):
        self.enabled = os.getenv("OPENCODE_ENABLED", "false").lower() == "true"
        self.api_url = os.getenv("OPENCODE_API_URL")
        self.timeout = int(os.getenv("OPENCODE_TIMEOUT", "30"))
        self.min_score = float(os.getenv("OPENCODE_MIN_SCORE", "0.75"))
        self.cache = {}  # {candidate_hash: result}
    
    async def validate_candidate(self, candidate: Dict) -> Optional[Dict]:
        """Valida coherencia lógica de un candidato arqueológico"""
        pass
    
    async def explain_evidence(self, candidate: Dict) -> Optional[Dict]:
        """Genera explicación estructurada de evidencia"""
        pass
    
    def _should_validate(self, candidate: Dict) -> bool:
        """Decide si vale la pena validar este candidato"""
        pass
```

**2.2 Tasks canónicos para OpenCode**

Definir 3 tasks principales:

1. **validate_coherence**
   - Input: instrumentos + scores + contexto temporal
   - Output: coherente/incoherente + razones

2. **explain_archaeological**
   - Input: candidato completo
   - Output: explicación científica estructurada

3. **classify_pattern**
   - Input: patrón espacial + contexto
   - Output: tipo probable (asentamiento/camino/estructura/etc)

---

### Fase 3: Integración en Pipeline (30 min)

**3.1 Modificar endpoint /analyze**

```python
# En backend/routes/analyze.py o similar

@app.post("/analyze")
async def analyze_region(request: AnalysisRequest):
    # Pipeline actual (SIN CAMBIOS)
    result = await archaeological_analysis(request)
    
    # Validación OpenCode (OPCIONAL, ASYNC)
    if opencode_validator.enabled:
        if opencode_validator.should_validate(result):
            # No bloquea respuesta principal
            asyncio.create_task(
                enrich_with_opencode(result.id, result)
            )
    
    return result
```

**3.2 Endpoint dedicado (recomendado)**

```python
@app.post("/validate_candidate/{candidate_id}")
async def validate_candidate_opencode(candidate_id: str):
    """
    Validación profunda con OpenCode - llamada manual.
    Útil para candidatos que el usuario quiere investigar más.
    """
    candidate = get_candidate_from_db(candidate_id)
    validation = await opencode_validator.validate_candidate(candidate)
    return validation
```

---

### Fase 4: Caché y Performance (20 min)

**4.1 Sistema de caché**

```python
def _hash_candidate(self, candidate: Dict) -> str:
    """Hash determinista del candidato para caché"""
    key_data = {
        "coords": candidate["spatial_context"],
        "scores": candidate["archaeological_results"],
        "instruments": [i["type"] for i in candidate["evidence_layers"]]
    }
    return hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
```

**4.2 Persistencia de caché (opcional)**

```python
# Guardar en disco para reutilizar entre sesiones
CACHE_FILE = "cache/opencode_validations.json"

def load_cache(self):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            self.cache = json.load(f)

def save_cache(self):
    with open(CACHE_FILE, 'w') as f:
        json.dump(self.cache, f, indent=2)
```

---

### Fase 5: Testing (30 min)

**5.1 Test unitario del validador**

```bash
# Archivo: test_opencode_validator.py
```

Tests mínimos:
- Conexión con OpenCode
- Caché funciona correctamente
- Feature flag respetado
- Timeout no bloquea sistema
- Errores manejados gracefully

**5.2 Test de integración**

```python
# test_opencode_integration.py

def test_high_score_candidate_gets_validated():
    """Candidatos con score > 0.75 deben validarse"""
    pass

def test_low_score_candidate_skipped():
    """Candidatos con score < 0.75 no se validan"""
    pass

def test_validation_cached():
    """Segunda validación del mismo candidato usa caché"""
    pass

def test_disabled_flag_skips_validation():
    """Con OPENCODE_ENABLED=false no se llama"""
    pass
```

**5.3 Test de performance**

```python
# test_opencode_performance.py

def test_validation_does_not_slow_main_pipeline():
    """Validar que análisis principal no se ralentiza"""
    
    # Medir tiempo sin OpenCode
    start = time.time()
    result1 = analyze_region(test_coords)
    time_without = time.time() - start
    
    # Medir tiempo con OpenCode (async)
    start = time.time()
    result2 = analyze_region(test_coords)
    time_with = time.time() - start
    
    # Diferencia debe ser < 5%
    assert time_with < time_without * 1.05
```

---

### Fase 6: Documentación (15 min)

**6.1 Actualizar AGENTS.md**

Agregar sección:
```markdown
### OpenCode Integration

# When to use
- Post-scoring validation (score > 0.75)
- Manual deep-dive on specific candidates
- Generating structured explanations

# When NOT to use
- Primary detection
- Pixel-level analysis
- Critical path operations
```

**6.2 Crear guía de uso**

```bash
# Archivo: OPENCODE_USAGE_GUIDE.md
```

Contenido:
- Cómo habilitar OpenCode
- Qué esperar en los resultados
- Cómo interpretar validaciones
- Troubleshooting común

---

## 🧪 Criterios de Éxito

### Funcionales
- ✅ OpenCode se llama solo para candidatos fuertes
- ✅ Resultados son deterministas (mismo input = mismo output)
- ✅ Sistema funciona igual con OpenCode deshabilitado
- ✅ Caché evita llamadas redundantes

### Performance
- ✅ Análisis principal no se ralentiza (< 5% overhead)
- ✅ Validaciones son async (no bloquean respuesta)
- ✅ Timeout previene cuelgues

### Científicos
- ✅ Explicaciones son auditables
- ✅ Validaciones mejoran confianza en candidatos
- ✅ No introduce falsos positivos/negativos

---

## 🚀 Orden de Ejecución Recomendado

```bash
# 1. Setup inicial
cp .env.local.example .env.local
# Editar: OPENCODE_ENABLED=false (por ahora)

# 2. Crear estructura
mkdir -p backend/ai
touch backend/ai/opencode_validator.py
touch backend/ai/__init__.py

# 3. Implementar validador
# (seguir estructura de Fase 2)

# 4. Crear tests
touch test_opencode_validator.py
touch test_opencode_integration.py
touch test_opencode_performance.py

# 5. Implementar tests básicos
python test_opencode_validator.py

# 6. Integrar en pipeline (opcional, async)
# Modificar backend/routes/analyze.py

# 7. Crear endpoint dedicado (recomendado)
# Agregar /validate_candidate/{id}

# 8. Testing completo
python test_opencode_integration.py
python test_opencode_performance.py

# 9. Habilitar en producción
# .env.local: OPENCODE_ENABLED=true

# 10. Monitorear logs
tail -f logs/archeoscope.log | grep opencode
```

---

## 📊 Métricas a Monitorear

### Durante desarrollo
- Tiempo de respuesta con/sin OpenCode
- Tasa de caché hit/miss
- Errores de timeout
- Candidatos validados vs total

### En producción
- Latencia p50, p95, p99 del endpoint /analyze
- Uso de caché (% hits)
- Validaciones exitosas vs fallidas
- Correlación score vs validación OpenCode

---

## ⚠️ Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| OpenCode lento | Media | Alto | Timeout + async + caché |
| OpenCode caído | Media | Bajo | Feature flag + graceful degradation |
| Resultados inconsistentes | Baja | Medio | Validar determinismo en tests |
| Overhead en pipeline | Baja | Alto | Async + threshold alto |

---

## 🔄 Rollback Plan

Si algo falla:

```bash
# 1. Deshabilitar inmediatamente
echo "OPENCODE_ENABLED=false" >> .env.local

# 2. Reiniciar backend
python run_archeoscope.py

# 3. Sistema vuelve a estado anterior
# (OpenCode es completamente opcional)
```

---

## 📚 Referencias

- OpenCode/Zen documentation: [agregar URL]
- ArcheoScope AI integration: `backend/ai/`
- Existing AI validators: `backend/ai/ollama_client.py`
- Testing patterns: `test_ai_validation_system.py`

---

## ✅ Checklist Final

Antes de considerar completo:

- [ ] `backend/ai/opencode_validator.py` implementado
- [ ] Variables de entorno documentadas
- [ ] Tests unitarios pasando
- [ ] Tests de integración pasando
- [ ] Tests de performance OK (< 5% overhead)
- [ ] Feature flag funciona
- [ ] Caché funciona
- [ ] Timeout funciona
- [ ] Endpoint `/validate_candidate` funcional
- [ ] Documentación actualizada
- [ ] AGENTS.md actualizado
- [ ] Logs implementados
- [ ] Rollback plan probado

---

## 🎯 Próximos Pasos (Post-Integración)

Una vez estable:

1. **Análisis de resultados**
   - ¿OpenCode detecta inconsistencias reales?
   - ¿Las explicaciones son útiles científicamente?

2. **Optimización**
   - Ajustar threshold de validación
   - Refinar tasks canónicos
   - Mejorar caché

3. **Expansión (opcional)**
   - Validación batch de candidatos históricos
   - Dashboard de validaciones OpenCode
   - Export de explicaciones para papers

---

**Tiempo estimado total:** 2.5 - 3 horas  
**Complejidad:** Media  
**Riesgo:** Bajo (completamente opcional y reversible)

---

*Plan generado: 2026-01-26*  
*Versión: 1.0*  
*Status: Ready for implementation*
