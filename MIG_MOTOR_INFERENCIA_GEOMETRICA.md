## 🧠 MIG - Motor de Inferencia Geométrica

**Motor de Inferencia Geométrica para ArcheoScope**

---

## 📋 Resumen Ejecutivo

El **MIG (Motor de Inferencia Geométrica)** convierte datos de coherencia espacial de ArcheoScope en modelos geométricos 3D visualizables.

### Paradigma Fundamental

> **"La IA NO genera vértices. La IA define REGLAS GEOMÉTRICAS. El motor las ejecuta."**

Esto es crítico: no estamos haciendo "IA generativa" que inventa formas. Estamos haciendo **inferencia geométrica** que descarta imposibles y materializa lo plausible.

---

## 🎯 ¿Qué Hace el MIG?

### Input (ArcheoScope Data)
```json
{
  "scale_invariance": 0.995,
  "angular_consistency": 0.910,
  "coherence_3d": 0.886,
  "sar_rigidity": 0.929,
  "stratification_index": 0.375,
  "estimated_area_m2": 10000.0
}
```

### Output (Modelo 3D)
- **PNG**: Visualización 3D isométrica
- **OBJ**: Modelo 3D importable (AutoCAD, Blender, etc.)
- **Metadatos**: Dimensiones, volumen, confianza

---

## 🔄 Pipeline Completo

### Etapa 1: Razonamiento Geométrico

**Entrada**: Métricas de coherencia espacial

**Proceso**:
1. Análisis de invariancia de escala
2. Evaluación de consistencia angular
3. Detección de estratificación
4. Inferencia de clase estructural

**Salida**: Reglas geométricas

```python
GeometricRules(
    structure_class=PYRAMIDAL,
    base_shape="square",
    base_length_m=100.0,
    height_m=50.0,
    symmetry=AXIAL,
    terracing=False,
    confidence=0.85
)
```

### Etapa 2: Generación Procedural

**Entrada**: Reglas geométricas

**Proceso**:
- Generación de vértices según reglas
- Construcción de caras/polígonos
- Cálculo de normales
- Validación geométrica

**Salida**: Mesh 3D (trimesh)

### Etapa 3: Renderizado

**Entrada**: Mesh 3D

**Proceso**:
- Proyección isométrica
- Iluminación y sombreado
- Anotaciones técnicas
- Export a PNG

**Salida**: Imagen PNG

### Etapa 4: Export

**Entrada**: Mesh 3D

**Proceso**:
- Conversión a formato OBJ
- Metadatos embebidos

**Salida**: Archivo OBJ

---

## 🏗️ Clases Estructurales Soportadas

### 1. PYRAMIDAL
**Características**:
- Scale Invariance > 0.9
- Angular Consistency > 0.9
- Stratification < 0.5

**Geometría**:
- Base cuadrada/rectangular
- Ápice central
- Caras triangulares

**Ejemplo**: Pirámide de Giza

### 2. STEPPED_PLATFORM
**Características**:
- Scale Invariance > 0.9
- Angular Consistency > 0.9
- Stratification > 0.5

**Geometría**:
- Múltiples niveles
- Reducción progresiva
- Terrazas horizontales

**Ejemplo**: Pirámides de Teotihuacán

### 3. MOUND_EMBANKMENT
**Características**:
- Coherence 3D > 0.8
- Angular Consistency < 0.7

**Geometría**:
- Forma orgánica
- Perfil suave
- Base irregular

**Ejemplo**: Túmulos, terraplenes

### 4. MEGALITHIC_MONUMENT
**Características**:
- SAR Rigidity > 0.9
- Área pequeña (<1000 m²)

**Geometría**:
- Volumen compacto
- Proporciones verticales
- Simetría bilateral

**Ejemplo**: Moais, menhires

---

## 🔧 Uso del Sistema

### Opción A: Python Directo

```python
from backend.geometric_inference_engine import GeometricInferenceEngine

# Crear motor
mig = GeometricInferenceEngine()

# Datos de ArcheoScope
data = {
    'scale_invariance': 0.995,
    'angular_consistency': 0.910,
    'coherence_3d': 0.886,
    'sar_rigidity': 0.929,
    'stratification_index': 0.375,
    'estimated_area_m2': 10000.0
}

# Ejecutar inferencia completa
result = mig.run_complete_inference(
    archeoscope_data=data,
    output_name="my_structure",
    use_ai=True  # Usar Ollama/Qwen
)

print(f"PNG: {result['png']}")
print(f"OBJ: {result['obj']}")
```

### Opción B: API REST

```bash
# Inferir geometría
curl -X POST http://localhost:8003/api/geometric-inference \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "puerto_rico_north",
    "scale_invariance": 0.995,
    "angular_consistency": 0.910,
    "coherence_3d": 0.886,
    "sar_rigidity": 0.929,
    "stratification_index": 0.375,
    "estimated_area_m2": 10000.0
  }'

# Descargar PNG
curl http://localhost:8003/api/geometric-model/puerto_rico_north/png \
  -o structure.png

# Descargar OBJ
curl http://localhost:8003/api/geometric-model/puerto_rico_north/obj \
  -o structure.obj
```

### Opción C: Test Script

```bash
python test_geometric_inference.py
```

---

## 🤖 Integración con IA (Ollama/Qwen)

### ¿Qué Hace la IA?

La IA **NO dibuja**. La IA **razona**:

1. **Decide qué reglas aplicar**
   - "Scale invariance 0.99 + angular consistency 0.97 → estructura regular"

2. **Valida coherencia**
   - "Stratification 0.7 + rigidity 0.9 → plataforma escalonada de piedra"

3. **Infiere proporciones**
   - "Área 10,000 m² → base ~100m × 100m"

4. **Detecta contradicciones**
   - "Angular consistency 0.001 es incompatible con estructura geométrica"

5. **Ajusta parámetros**
   - "Coherence 3D 0.886 → confianza 0.85"

### Prompt para IA

```
TAREA: Inferencia Geométrica desde Datos de Teledetección

DATOS:
- Scale Invariance: 0.995
- Angular Consistency: 0.910
- Coherencia 3D: 0.886
- SAR Rigidity: 0.929
- Stratification: 0.375

REGLAS:
1. Scale Inv > 0.9 + Angular > 0.9 → Estructura regular
2. Stratification > 0.5 → Escalonada
3. SAR Rigidity > 0.85 → Material compacto

OUTPUT (JSON):
{
  "structure_class": "pyramidal",
  "base_shape": "square",
  "dimensions": {...},
  "confidence": 0.85,
  "reasoning": "..."
}
```

---

## 📊 Metadatos de Salida

### PNG Metadata
- Dimensiones (m)
- Volumen (m³)
- Scale Invariance
- Angular Consistency
- Coherence 3D
- Confianza
- Incertidumbre

### OBJ Metadata
- Vértices
- Caras
- Normales
- Bounding box

---

## 🎨 Visualización

### Estilo Visual
- **Fondo**: Negro (#1a1a1a)
- **Estructura**: Color piedra (#8B7355)
- **Bordes**: Gris oscuro (#2a2a2a)
- **Grid**: Gris transparente
- **Texto**: Blanco/Gris

### Ángulos de Vista
- **Elevación**: 30° (default)
- **Azimut**: 45° (default)
- **Proyección**: Isométrica

---

## 🔬 Validación Científica

### Principios

1. **NO inventar detalles**
   - Solo geometría inferible desde datos físicos

2. **Incertidumbre explícita**
   - Siempre reportar nivel de confianza

3. **Falsificabilidad**
   - Reglas claras, verificables

4. **Reproducibilidad**
   - Mismos datos → mismo modelo

### Limitaciones

❌ **NO genera**:
- Detalles arquitectónicos
- Decoración superficial
- Función cultural
- Afirmaciones históricas

✅ **SÍ genera**:
- Forma geométrica básica
- Escala correcta
- Relaciones espaciales
- Volumen aproximado

---

## 🚀 Próximos Pasos

### Fase 1: Básico (ACTUAL)
- ✅ Geometría procedural simple
- ✅ Render a PNG
- ✅ Export a OBJ
- ✅ API REST

### Fase 2: IA Integrada
- 🔄 Integración Ollama/Qwen
- 🔄 Razonamiento geométrico avanzado
- 🔄 Validación multi-escala con HRM

### Fase 3: Avanzado
- ⏳ OpenCascade (geometría CAD)
- ⏳ Blender headless (render fotorrealista)
- ⏳ OpenVDB (volúmenes)
- ⏳ IFC/BIM export

### Fase 4: Profesional
- ⏳ Texturas procedurales
- ⏳ Iluminación física
- ⏳ Animaciones (rotación, zoom)
- ⏳ VR/AR export

---

## 📁 Estructura de Archivos

```
backend/
├── geometric_inference_engine.py    # Motor principal
└── api/
    └── geometric_inference_endpoint.py  # API REST

geometric_models/                    # Output
├── *.png                           # Visualizaciones
└── *.obj                           # Modelos 3D

test_geometric_inference.py         # Tests
MIG_MOTOR_INFERENCIA_GEOMETRICA.md  # Este documento
```

---

## 🎯 Casos de Uso

### 1. Validación de Hallazgos
**Problema**: "¿Esta anomalía podría ser una estructura?"

**Solución**:
```python
result = mig.run_complete_inference(anomaly_data)
if result['confidence'] > 0.7:
    print("Geometría plausible")
```

### 2. Comparación de Sitios
**Problema**: "¿Estas dos anomalías son similares?"

**Solución**:
- Generar modelos de ambas
- Comparar volúmenes, proporciones
- Analizar diferencias geométricas

### 3. Comunicación Científica
**Problema**: "¿Cómo visualizar el hallazgo?"

**Solución**:
- PNG para papers/presentaciones
- OBJ para análisis 3D detallado

### 4. Integración CAD
**Problema**: "¿Cómo importar a AutoCAD?"

**Solución**:
- Export OBJ
- Import directo en AutoCAD/Blender/etc.

---

## ✅ Ventajas del MIG

1. **Científicamente riguroso**
   - Basado en datos físicos
   - Incertidumbre explícita
   - Falsificable

2. **Técnicamente sólido**
   - Geometría procedural
   - Export estándar (OBJ)
   - API REST

3. **Escalable**
   - Fácil agregar nuevas clases
   - Modular
   - Extensible

4. **Único en el campo**
   - Nadie más hace esto
   - Ventaja competitiva
   - Revolucionario

---

## 📞 Soporte

**Documentación**: Este archivo
**Tests**: `test_geometric_inference.py`
**API**: `/api/geometric-inference`

---

**Generado**: 2026-02-05  
**Versión**: 1.0  
**Estado**: ✅ Funcional - Listo para uso

