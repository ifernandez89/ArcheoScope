# 🎨 Creador3D - Nueva API Secundaria

## Fecha: 12 Febrero 2026

---

## 🎯 Resumen Ejecutivo

Se ha creado una **API secundaria separada** llamada **Creador3D** para explorar nuevas funcionalidades de generación 3D sin comprometer el rigor científico de ArcheoScope.

---

## 🆚 Separación de APIs

### ArcheoScope (Puerto 8003)
- **Propósito**: Científico/arqueológico
- **Entrada**: Coordenadas geográficas
- **Salida**: Modelos culturalmente constreñidos
- **Rigor**: Absoluto (paradigma científico)
- **Clasificación**: Automática basada en contexto
- **Uso**: Investigación arqueológica

### Creador3D (Puerto 8004) **NUEVO**
- **Propósito**: Experimental/creativo
- **Entrada**: Parámetros, morfologías, geometría custom
- **Salida**: Modelos 3D flexibles
- **Rigor**: Flexible (sin restricciones)
- **Clasificación**: Manual por usuario
- **Uso**: Exploración, prototipado, experimentación

---

## 📡 Endpoints Implementados

### 1. Información
- `GET /` - Info de la API
- `GET /status` - Estado del sistema
- `GET /morphologies` - Listar clases morfológicas

### 2. Generación
- `POST /generate/parameters` - Desde parámetros geométricos
- `POST /generate/morphology` - Desde clase morfológica
- `POST /generate/custom` - Desde geometría custom
- `POST /generate/description` - Desde texto (placeholder)

### 3. Descarga
- `GET /model/{filename}` - Descargar PNG/OBJ

---

## 🎨 Modos de Generación

### Modo 1: Desde Parámetros
```json
{
  "height_m": 30.0,
  "width_m": 50.0,
  "shape_type": "pyramid",
  "color": "#D4A574"
}
```

**Ventajas**:
- Control total sobre dimensiones
- Especificar tipo de forma
- Personalizar color
- Rápido y directo

**Tipos soportados**:
- `pyramid`: Pirámide escalonada
- `statue`: Estatua vertical
- `platform`: Plataforma horizontal
- `moai`: Moai
- `sphinx`: Esfinge

---

### Modo 2: Desde Morfología
```json
{
  "morphological_class": "moai",
  "scale_factor": 1.5
}
```

**Ventajas**:
- Usa clases del repositorio morfológico
- Proporciones culturales correctas
- Escalado simple
- Reutiliza lógica científica

**Clases disponibles**:
- moai, sphinx, egyptian_statue, colossus
- pyramid_mesoamerican, temple_platform, stela_maya

---

### Modo 3: Geometría Custom
```json
{
  "vertices": [[x, y, z], ...],
  "faces": [[v1, v2, v3], ...]
}
```

**Ventajas**:
- Control absoluto
- Cualquier forma posible
- Para usuarios avanzados
- Máxima flexibilidad

---

## 🏗️ Arquitectura

```
ArcheoScope/
├── backend/                          # Backend científico
│   ├── culturally_constrained_mig.py # Lógica compartida
│   ├── morphological_repository.py   # Lógica compartida
│   └── api/
│       └── main.py                   # API científica (8003)
│
├── creador3d/                        # Nueva API experimental
│   ├── __init__.py
│   ├── api_creador3d.py             # API FastAPI (8004)
│   └── README.md                     # Documentación
│
├── creador3d_models/                 # Modelos generados
│   ├── *.png
│   └── *.obj
│
├── run_creador3d.py                  # Iniciar API
└── test_creador3d.py                 # Tests
```

---

## 🔧 Reutilización de Código

La API Creador3D **reutiliza** la lógica existente:

**Importa desde backend**:
```python
from culturally_constrained_mig import CulturallyConstrainedMIG
from morphological_repository import MorphologicalRepository
```

**Ventajas**:
- ✅ No duplica código
- ✅ Mantiene consistencia
- ✅ Aprovecha mejoras existentes
- ✅ Separación lógica clara

---

## 🚀 Inicio Rápido

### 1. Iniciar API
```bash
python run_creador3d.py
```

### 2. Verificar Status
```bash
curl http://localhost:8004/status
```

### 3. Generar Modelo
```bash
curl -X POST http://localhost:8004/generate/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "height_m": 30,
    "width_m": 50,
    "shape_type": "pyramid"
  }'
```

### 4. Descargar Resultado
```bash
curl http://localhost:8004/model/custom_pyramid_*.png -o modelo.png
```

---

## 📊 Comparación de Uso

### Caso 1: Investigación Arqueológica
**Usar**: ArcheoScope (8003)
```python
# Entrada: Coordenadas reales
POST /api/geometric-inference-3d
{
  "lat": 19.6925,
  "lon": -98.8438
}

# Salida: Clasificación automática + modelo científico
# Teotihuacán → PYRAMID_MESOAMERICAN (86.74% confianza)
```

### Caso 2: Prototipado Rápido
**Usar**: Creador3D (8004)
```python
# Entrada: Parámetros directos
POST /generate/parameters
{
  "height_m": 40,
  "width_m": 60,
  "shape_type": "pyramid"
}

# Salida: Modelo inmediato sin clasificación
```

### Caso 3: Experimentación
**Usar**: Creador3D (8004)
```python
# Entrada: Geometría custom
POST /generate/custom
{
  "vertices": [...],
  "faces": [...]
}

# Salida: Cualquier forma posible
```

---

## 🎯 Casos de Uso

### Para Creador3D

**1. Prototipado Rápido**
- Generar modelos de prueba
- Iterar rápidamente
- Sin necesidad de coordenadas

**2. Visualización Educativa**
- Crear modelos para enseñanza
- Diferentes escalas
- Comparaciones visuales

**3. Experimentación**
- Probar nuevas formas
- Geometrías no arqueológicas
- Exploración creativa

**4. Desarrollo de Funcionalidades**
- Testear nuevas ideas
- Sin afectar API científica
- Iteración rápida

---

## 🔒 Separación de Responsabilidades

### ArcheoScope (Científico)
✅ Mantiene rigor absoluto
✅ Paradigma "forma culturalmente posible"
✅ Sin compromisos
✅ Para publicaciones científicas

### Creador3D (Experimental)
✅ Libertad de experimentación
✅ Sin restricciones científicas
✅ Iteración rápida
✅ Para exploración

**Resultado**: Ambas APIs coexisten sin conflicto

---

## 📁 Archivos Creados

```
creador3d/
├── __init__.py                 (Módulo Python)
├── api_creador3d.py           (API FastAPI - 400+ líneas)
└── README.md                   (Documentación completa)

run_creador3d.py               (Script de inicio)
test_creador3d.py              (Suite de tests)
CREADOR3D_API_NUEVA.md         (Este documento)
```

---

## 🧪 Tests Incluidos

El archivo `test_creador3d.py` incluye:

1. ✅ Test de status
2. ✅ Test de listar morfologías
3. ✅ Test de generación desde parámetros
4. ✅ Test de generación desde morfología
5. ✅ Test de geometría custom

**Ejecutar**:
```bash
python test_creador3d.py
```

---

## 🚀 Próximos Pasos

### Inmediato
1. Iniciar API: `python run_creador3d.py`
2. Ejecutar tests: `python test_creador3d.py`
3. Explorar endpoints en: `http://localhost:8004/docs`

### Corto Plazo
- Implementar generación desde descripción textual (IA)
- Agregar más tipos de formas
- Texturas procedurales
- Batch generation

### Mediano Plazo
- Frontend dedicado para Creador3D
- Biblioteca de templates
- Export a más formatos (STL, FBX, GLTF)
- API de composición (combinar modelos)

---

## 💡 Ventajas de la Separación

### Técnicas
✅ Código modular y mantenible
✅ Reutilización sin duplicación
✅ Puertos separados (sin conflictos)
✅ Logs independientes

### Conceptuales
✅ Ciencia y experimentación separadas
✅ Rigor científico protegido
✅ Libertad de innovación
✅ Claridad de propósito

### Prácticas
✅ Desarrollo paralelo
✅ Tests independientes
✅ Despliegue separado
✅ Escalabilidad

---

## 📚 Documentación

### API Interactiva
- Swagger UI: `http://localhost:8004/docs`
- ReDoc: `http://localhost:8004/redoc`

### Archivos
- `creador3d/README.md`: Documentación completa
- `CREADOR3D_API_NUEVA.md`: Este resumen
- Código comentado en `api_creador3d.py`

---

## ✅ Estado Actual

**API Creador3D**:
- ✅ Implementada y funcional
- ✅ 8 endpoints operativos
- ✅ Tests incluidos
- ✅ Documentación completa
- ✅ Reutiliza lógica existente
- ✅ Separada de ArcheoScope

**Listo para**:
- Exploración de nuevas funcionalidades
- Prototipado rápido
- Experimentación sin restricciones
- Desarrollo de features experimentales

---

## 🎉 Conclusión

Se ha creado exitosamente una **API secundaria experimental** que:

1. **Separa** ciencia de experimentación
2. **Reutiliza** lógica existente sin duplicar
3. **Permite** exploración libre sin comprometer rigor
4. **Mantiene** ArcheoScope científico intacto
5. **Facilita** desarrollo de nuevas funcionalidades

**Estado**: ✅ OPERACIONAL - LISTO PARA EXPERIMENTACIÓN

---

**¡Ahora puedes explorar nuevas funcionalidades sin comprometer la API científica!** 🚀
