# 🚨 AUDITORÍA CRÍTICA DE INTEGRIDAD CIENTÍFICA
## ArcheoScope - Riesgo de Fraude Involuntario
## Fecha: 2026-01-26

---

## ⚠️ RECONOCIMIENTO DE RIESGO

**ESTO NO ES**: "Bugs técnicos normales" o "Deuda técnica"

**ESTO ES**:
- ✋ Riesgo de fraude científico involuntario
- ✋ Riesgo de pérdida total de confianza
- ✋ Riesgo de mal uso en campo
- ✋ Riesgo legal/reputacional si alguien publica resultados basados en esto

**ETIQUETA INTERNA CORRECTA**:
```
⚠️ PROTOTYPE CIENTÍFICO EN RIESGO DE MALA REPRESENTACIÓN DE RESULTADOS
```

---

## 🔴 PROBLEMAS CRÍTICOS IDENTIFICADOS

### A. AMBIGÜEDAD EN MODO DE DATOS

**PROBLEMA**: El sistema NO distingue explícitamente entre:
- Datos REALES de APIs satelitales
- Datos DERIVADOS de estimaciones
- Datos SIMULADOS (eliminados pero legacy persiste)

**RIESGO**: Un usuario puede interpretar una "anomalía detectada" como evidencia física cuando es:
- Una inferencia estadística
- Una estimación basada en ubicación
- Un patrón geométrico plausible (NO observado)

**EVIDENCIA**:
```python
# En nsidc_connector.py - Fallback honesto pero NO etiquetado
return {
    "value": estimated_value,
    "source": "NSIDC (estimated)",  # ← Dice "estimated" pero...
    "confidence": 0.7,
    # ❌ FALTA: "data_mode": "DERIVED"
}
```

**CONSECUENCIA**: Frontend puede mostrar esto como "dato real" sin disclaimer.

---

### B. LENGUAJE CIENTÍFICAMENTE IRRESPONSABLE

**PROBLEMA**: El sistema usa lenguaje definitivo cuando debería usar lenguaje hipotético.

**PALABRAS PROBLEMÁTICAS ENCONTRADAS**:

En `frontend/index.html`:
```javascript
// ❌ PELIGROSO
"📋 Documentar hallazgos para validación por expertos"
"Estructura detectada con X% de confianza"
"Validación temporal CONFIRMADA"
"Candidato confirmado temporalmente"
```

En `frontend/archaeological_app.js`:
```javascript
// ❌ PELIGROSO
"🏺 Sitio arqueológico confirmado"
"✅ Sensor temporal CONFIRMA anomalías"
"🔍 Si la masa se fragmenta en geometría → Estructura detectada"
```

**DEBERÍA DECIR**:
```javascript
// ✅ CORRECTO
"📋 Documentar HIPÓTESIS para validación por expertos"
"Patrón geométrico inferido con X% de plausibilidad estadística"
"Persistencia temporal detectada (NO constituye confirmación)"
"Candidato con persistencia temporal (requiere validación física)"
```

---

### C. VISUALIZACIÓN ENGAÑOSA

**PROBLEMA**: El frontend renderiza "estructuras" como si fueran datos LiDAR reales.

**EVIDENCIA**:
```javascript
// frontend/index.html - Genera geometría 3D
dimensions: generateRealisticDimensions(avgProbability)
// ❌ Esto NO es LiDAR real, es INFERENCIA GEOMÉTRICA
```

**RIESGO**: Un usuario ve una "pirámide 3D" y asume que es:
- Datos LiDAR reales
- Evidencia física confirmada
- Geometría observada

**REALIDAD**: Es una visualización de plausibilidad estadística.

**SOLUCIÓN REQUERIDA**:
- Wireframes, NO sólidos
- Transparencias obligatorias
- Disclaimer: "Geometría inferida por plausibilidad estadística. NO constituye evidencia física."
- Capas etiquetadas como "hypothesis layers"

---

### D. ALUCINACIÓN ESTRUCTURADA (Crítica más fina)

**PROBLEMA**: El sistema genera "candidatos" con:
- Dimensiones "realistas"
- Tipos de estructura (pirámide, templo, etc.)
- Geometría 3D renderizable

**PERO**: Estos NO son observaciones, son INFERENCIAS basadas en:
- Patrones estadísticos
- Plausibilidad geométrica
- Convergencia instrumental

**EJEMPLO PELIGROSO**:
```javascript
// ❌ Esto es alucinación estructurada
{
    type: 'pyramid',
    dimensions: {length: 120, width: 120, height: 40},
    confidence: 0.85,
    // ← NO hay LiDAR que confirme esto
}
```

**REALIDAD**: Solo hay:
- Anomalía térmica (MODIS LST)
- Backscatter SAR anómalo
- NDVI suprimido

**INFERENCIA VÁLIDA**: "Patrón compatible con estructura compacta enterrada"
**INFERENCIA INVÁLIDA**: "Pirámide de 120x120x40m detectada"

---

### E. BASE DE DATOS: ESQUEMA ASPIRACIONAL VS OPERATIVO

**PROBLEMA**: `prisma/schema.prisma` define modelos que NO están vivos.

**EVIDENCIA**:
```prisma
model ArchaeologicalCandidate {
  // ← Este modelo existe en schema
  // ❌ Pero NO está siendo usado en producción
}

model LidarDataset {
  // ← Este modelo es aspiracional
  // ❌ NO hay datos LiDAR reales cargados
}
```

**RIESGO**: Disonancia cognitiva entre:
- Lo que el código dice que hace
- Lo que realmente hace

**SOLUCIÓN REQUERIDA**:
- Documentar explícitamente qué modelos están vivos
- Marcar modelos aspiracionales como `// FUTURE:`
- O eliminar lo no usado

---

### F. TESTS SON EXPERIMENTOS, NO TESTS

**PROBLEMA**: Los archivos `test_*.py` NO son tests unitarios.

**REALIDAD**: Son experimentos históricos, scripts de exploración.

**EVIDENCIA**:
- 150+ archivos `test_*.py`
- NO hay suite de tests automatizada
- NO hay CI/CD
- NO hay cobertura de tests

**RIESGO**: Falsa sensación de "sistema testeado".

**SOLUCIÓN REQUERIDA**:
```
experiments/
  ├── 2026-01-20_titanic_detection.py
  ├── 2026-01-21_giza_thermal.py
  └── ...

tests/  ← REAL test suite
  ├── test_data_integrity.py
  ├── test_api_connectors.py
  └── ...
```

---

### G. SEGURIDAD: TRATAMIENTO COMO INCIDENTE

**PROBLEMA**: Credenciales expuestas múltiples veces en commits.

**EVIDENCIA**:
- `.env` NO estaba en `.gitignore` inicialmente
- Credenciales Earthdata y Copernicus en repositorio
- NO hay `.env.example`

**RIESGO**: Keys comprometidas, acceso no autorizado.

**ACCIÓN INMEDIATA REQUERIDA**:
1. ✅ `.env` en `.gitignore` (YA HECHO)
2. ❌ Rotar keys (NO HECHO - URGENTE)
3. ❌ Crear `.env.example` (NO HECHO)
4. ❌ Auditoría de commits anteriores (NO HECHO)

---

## 🔧 CORRECCIONES QUIRÚRGICAS REQUERIDAS

### PRIORIDAD ABSOLUTA (Hacer YA)

#### 1. Sistema de Etiquetado de Modo de Datos

**Crear**: `backend/data_integrity/data_mode.py`

```python
from enum import Enum

class DataMode(Enum):
    """
    Modo de datos - CRÍTICO para integridad científica
    """
    REAL = "REAL"           # Datos directos de API satelital
    DERIVED = "DERIVED"     # Estimaciones basadas en ubicación
    SIMULATED = "SIMULATED" # Simulaciones (PROHIBIDO en producción)
    INFERRED = "INFERRED"   # Inferencias geométricas/estadísticas

class DataIntegrityValidator:
    """
    Validador de integridad de datos
    """
    
    @staticmethod
    def validate_output(data: dict, mode: DataMode):
        """
        Validar que el output sea apropiado para el modo de datos
        """
        if mode == DataMode.SIMULATED:
            raise ValueError("SIMULATED data is PROHIBITED in production")
        
        if mode in [DataMode.DERIVED, DataMode.INFERRED]:
            # Forzar disclaimers
            if 'disclaimer' not in data:
                raise ValueError(f"{mode.value} data MUST include disclaimer")
        
        # Prohibir lenguaje definitivo en modos no-REAL
        if mode != DataMode.REAL:
            forbidden_words = [
                'confirmado', 'confirmed', 'detectado', 'detected',
                'hallazgo', 'discovery', 'estructura', 'structure'
            ]
            
            text = str(data).lower()
            for word in forbidden_words:
                if word in text:
                    raise ValueError(
                        f"Forbidden word '{word}' in {mode.value} data. "
                        f"Use hypothetical language."
                    )
        
        return True
```

#### 2. Actualizar TODOS los conectores

**Modificar**: Cada conector debe retornar `data_mode`:

```python
# backend/satellite_connectors/nsidc_connector.py
async def get_sea_ice_concentration(...):
    if real_api_success:
        return {
            "value": real_value,
            "data_mode": "REAL",  # ← AGREGAR
            "source": "NSIDC Sea Ice",
            "confidence": 0.9
        }
    else:
        # Fallback estimado
        return {
            "value": estimated_value,
            "data_mode": "DERIVED",  # ← AGREGAR
            "source": "NSIDC (estimated)",
            "confidence": 0.7,
            "disclaimer": "Estimación basada en ubicación y estación. NO constituye medición directa."
        }
```

#### 3. Actualizar Frontend con Disclaimers Forzados

**Modificar**: `frontend/index.html` y `frontend/archaeological_app.js`

```javascript
// ANTES (PELIGROSO):
"Estructura detectada con 85% de confianza"

// DESPUÉS (CORRECTO):
function formatResult(result) {
    if (result.data_mode === 'REAL') {
        return `Anomalía instrumental detectada (${result.confidence * 100}% confianza)`;
    } else if (result.data_mode === 'DERIVED') {
        return `Patrón estimado (${result.confidence * 100}% plausibilidad) - ${result.disclaimer}`;
    } else if (result.data_mode === 'INFERRED') {
        return `Geometría inferida (${result.confidence * 100}% plausibilidad estadística) - NO constituye evidencia física`;
    }
}
```

#### 4. Visualización: Wireframes, NO Sólidos

**Modificar**: Renderizado 3D

```javascript
// ANTES (ENGAÑOSO):
material = new THREE.MeshPhongMaterial({
    color: 0x8B4513,
    opacity: 1.0  // ← Parece real
});

// DESPUÉS (HONESTO):
material = new THREE.MeshBasicMaterial({
    color: 0x00FF00,
    wireframe: true,  // ← Claramente hipotético
    opacity: 0.3,
    transparent: true
});

// Agregar texto flotante
const disclaimer = createTextSprite(
    "GEOMETRÍA INFERIDA\nNO ES EVIDENCIA FÍSICA"
);
```

#### 5. Separar Inference de Interpretation

**Crear**: `backend/inference/` y `backend/interpretation/`

```
backend/
  ├── inference/          ← Detección instrumental pura
  │   ├── anomaly_detector.py
  │   └── convergence_analyzer.py
  │
  └── interpretation/     ← Interpretación contextual (IA)
      ├── geometric_interpreter.py
      └── archaeological_interpreter.py
```

**Regla**: `inference/` NO puede usar lenguaje definitivo.
**Regla**: `interpretation/` DEBE incluir disclaimers.

---

### PRIORIDAD ALTA (Esta semana)

#### 6. Renombrar Tests → Experiments

```bash
mkdir experiments/
mv test_*.py experiments/
# Renombrar con fechas
mv experiments/test_titanic.py experiments/2026-01-20_titanic_detection.py
```

#### 7. Crear Suite de Tests Real

```
tests/
  ├── test_data_integrity.py      ← Valida data_mode
  ├── test_api_connectors.py      ← Valida APIs reales
  ├── test_no_simulations.py      ← Verifica NO np.random
  └── test_language_safety.py     ← Detecta palabras prohibidas
```

#### 8. Documentar Esquema DB

**Crear**: `prisma/SCHEMA_STATUS.md`

```markdown
# Prisma Schema Status

## MODELOS VIVOS (en uso)
- `ArchaeologicalSite` ✅
- `ArchaeologicalCandidate` ✅

## MODELOS ASPIRACIONALES (futuro)
- `LidarDataset` 🔮 (requiere integración OpenTopography)
- `GeophysicalSurvey` 🔮 (requiere GPR data)

## MODELOS DEPRECADOS
- (ninguno actualmente)
```

#### 9. Rotar Credenciales

```bash
# URGENTE - Hacer manualmente
1. Cambiar password en Earthdata
2. Cambiar password en Copernicus Marine
3. Actualizar .env local
4. NO commitear .env
```

#### 10. Crear .env.example

```bash
# .env.example
EARTHDATA_USERNAME=your_username_here
EARTHDATA_PASSWORD=your_password_here
COPERNICUS_MARINE_USERNAME=your_username_here
COPERNICUS_MARINE_PASSWORD=your_password_here
OPENROUTER_API_KEY=your_key_here
```

---

## 📋 CHECKLIST DE INTEGRIDAD CIENTÍFICA

### Antes de cualquier release:

- [ ] Todos los outputs tienen `data_mode` explícito
- [ ] NO hay palabras definitivas en modos DERIVED/INFERRED
- [ ] Visualizaciones 3D son wireframes con disclaimers
- [ ] Frontend muestra disclaimers obligatorios
- [ ] Tests reales (NO experimentos) pasan
- [ ] NO hay `np.random` en código de producción
- [ ] Credenciales rotadas y seguras
- [ ] Documentación honesta sobre limitaciones

---

## 🎯 DEFINICIÓN HONESTA DEL SISTEMA

### LO QUE ARCHEOSCOPE ES:

✅ **Motor de hipótesis geoespaciales**
- Detecta anomalías instrumentales convergentes
- Genera hipótesis arqueológicas plausibles
- Prioriza zonas para investigación física

### LO QUE ARCHEOSCOPE NO ES:

❌ **NO es arqueología computacional definitiva**
- NO confirma sitios arqueológicos
- NO reemplaza excavación física
- NO genera evidencia publicable sin validación

### LENGUAJE CORRECTO:

| ❌ Incorrecto | ✅ Correcto |
|--------------|------------|
| "Estructura detectada" | "Patrón instrumental anómalo" |
| "Sitio confirmado" | "Candidato de alta prioridad" |
| "Pirámide de 120m" | "Anomalía compatible con estructura compacta" |
| "Hallazgo arqueológico" | "Hipótesis arqueológica" |
| "Validación confirmada" | "Persistencia temporal detectada" |

---

## 🚨 DISCLAIMER OBLIGATORIO

**Agregar a TODA la documentación y UI**:

```
⚠️ DISCLAIMER CIENTÍFICO

ArcheoScope es un motor de hipótesis geoespaciales que detecta anomalías 
instrumentales convergentes. Los "candidatos" generados son HIPÓTESIS que 
requieren validación física por arqueólogos profesionales.

Este sistema NO:
- Confirma sitios arqueológicos
- Genera evidencia publicable sin validación
- Reemplaza métodos arqueológicos tradicionales

Modo de datos:
- REAL: Mediciones directas de APIs satelitales
- DERIVED: Estimaciones basadas en modelos
- INFERRED: Inferencias geométricas/estadísticas

Ningún output de este sistema constituye evidencia arqueológica definitiva.
```

---

## 📊 MÉTRICAS DE INTEGRIDAD

### Estado Actual (ANTES de correcciones):

| Métrica | Estado | Riesgo |
|---------|--------|--------|
| Etiquetado de modo de datos | ❌ NO | 🔴 ALTO |
| Lenguaje científicamente responsable | ❌ NO | 🔴 ALTO |
| Visualización honesta | ❌ NO | 🔴 ALTO |
| Separación inference/interpretation | ❌ NO | 🟡 MEDIO |
| Tests reales | ❌ NO | 🟡 MEDIO |
| Seguridad de credenciales | ⚠️ PARCIAL | 🟡 MEDIO |
| Documentación honesta | ⚠️ PARCIAL | 🟡 MEDIO |

### Estado Objetivo (DESPUÉS de correcciones):

| Métrica | Estado | Riesgo |
|---------|--------|--------|
| Etiquetado de modo de datos | ✅ SÍ | 🟢 BAJO |
| Lenguaje científicamente responsable | ✅ SÍ | 🟢 BAJO |
| Visualización honesta | ✅ SÍ | 🟢 BAJO |
| Separación inference/interpretation | ✅ SÍ | 🟢 BAJO |
| Tests reales | ✅ SÍ | 🟢 BAJO |
| Seguridad de credenciales | ✅ SÍ | 🟢 BAJO |
| Documentación honesta | ✅ SÍ | 🟢 BAJO |

---

## 🧭 FILOSOFÍA DE MADUREZ CIENTÍFICA

### Principios fundamentales:

1. **Honestidad radical**: Preferir "no sé" sobre "probablemente"
2. **Transparencia total**: Cada dato debe tener `data_mode` y `source`
3. **Lenguaje hipotético**: Usar "compatible con" en vez de "es"
4. **Visualización honesta**: Wireframes, NO renders realistas
5. **Separación clara**: Inference (datos) vs Interpretation (contexto)

### Regla de oro:

> "Si un arqueólogo profesional viera este output y lo malinterpretara como 
> evidencia definitiva, el sistema ha fallado en su responsabilidad científica."

---

## ✅ COMPROMISO DE CORRECCIÓN

**Acepto que**:
1. ArcheoScope es un motor de hipótesis, NO arqueología definitiva
2. El lenguaje actual es científicamente irresponsable
3. Las visualizaciones actuales son engañosas
4. Se requiere cirugía quirúrgica, NO refactor masivo
5. La integridad científica es PRIORIDAD ABSOLUTA

**Me comprometo a**:
1. Implementar sistema de `data_mode` inmediatamente
2. Corregir lenguaje en frontend (palabras prohibidas)
3. Cambiar visualizaciones a wireframes con disclaimers
4. Separar inference de interpretation
5. Rotar credenciales comprometidas
6. Documentar honestamente las limitaciones

**NO voy a**:
1. Minimizar esto como "fase temprana"
2. Hacer refactor masivo que rompa todo
3. Agregar features antes de corregir integridad
4. Fingir que los tests actuales son una suite real

---

## 📅 PLAN DE ACCIÓN INMEDIATO

### HOY (2026-01-26):
- [x] Crear este documento de auditoría
- [ ] Implementar `DataMode` enum y validator
- [ ] Actualizar 3 conectores principales con `data_mode`
- [ ] Agregar disclaimer obligatorio al frontend

### ESTA SEMANA:
- [ ] Actualizar TODOS los conectores
- [ ] Corregir lenguaje en frontend (palabras prohibidas)
- [ ] Cambiar visualizaciones a wireframes
- [ ] Rotar credenciales
- [ ] Crear `.env.example`

### PRÓXIMAS 2 SEMANAS:
- [ ] Separar `inference/` de `interpretation/`
- [ ] Renombrar tests → experiments
- [ ] Crear suite de tests real
- [ ] Documentar esquema DB (vivo vs aspiracional)
- [ ] Auditoría de commits (credenciales)

---

**Fecha de auditoría**: 2026-01-26  
**Auditor**: Kiro AI Assistant (bajo instrucción del usuario)  
**Severidad**: 🔴 CRÍTICA  
**Acción requerida**: INMEDIATA

---

**Este documento es un llamado de madurez científica, no una crítica destructiva.**
**Es exactamente el tipo de auditoría que salva proyectos antes de volverse ridículos o peligrosos.**
