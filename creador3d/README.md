# 🎨 Creador3D - API de Generación 3D Experimental

## Descripción

API secundaria separada de ArcheoScope científico para explorar nuevas funcionalidades de generación 3D sin comprometer el rigor científico del sistema principal.

---

## 🎯 Propósito

**Separación de Responsabilidades**:
- **ArcheoScope (puerto 8003)**: API científica con rigor arqueológico
- **Creador3D (puerto 8004)**: API experimental para exploración libre

**Ventajas**:
- ✅ Experimentación sin comprometer ciencia
- ✅ Diferentes tipos de datos de entrada
- ✅ Funcionalidades creativas sin restricciones
- ✅ Reutiliza lógica de generación existente

---

## 🚀 Inicio Rápido

### Iniciar API
```bash
python run_creador3d.py
```

La API estará disponible en: `http://localhost:8004`

### Ejecutar Tests
```bash
python test_creador3d.py
```

---

## 📡 Endpoints

### 1. Status y Información

#### GET /
Información general de la API
```bash
curl http://localhost:8004/
```

#### GET /status
Estado del sistema
```bash
curl http://localhost:8004/status
```

#### GET /morphologies
Listar clases morfológicas disponibles
```bash
curl http://localhost:8004/morphologies
```

---

### 2. Generación de Modelos

#### POST /generate/parameters
Generar desde parámetros geométricos directos

**Request**:
```json
{
  "height_m": 30.0,
  "width_m": 50.0,
  "depth_m": 50.0,
  "shape_type": "pyramid",
  "output_name": "mi_piramide",
  "color": "#D4A574"
}
```

**Shape Types**:
- `pyramid`: Pirámide escalonada
- `statue`: Estatua vertical
- `platform`: Plataforma horizontal
- `moai`: Moai de Rapa Nui
- `sphinx`: Esfinge egipcia

**Response**:
```json
{
  "success": true,
  "png_filename": "mi_piramide.png",
  "obj_filename": "mi_piramide.obj",
  "volume_m3": 15000.0,
  "dimensions": {
    "height_m": 30.0,
    "width_m": 50.0,
    "depth_m": 50.0
  }
}
```

**Ejemplo**:
```bash
curl -X POST http://localhost:8004/generate/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "height_m": 30,
    "width_m": 50,
    "shape_type": "pyramid"
  }'
```

---

#### POST /generate/morphology
Generar desde clase morfológica conocida

**Request**:
```json
{
  "morphological_class": "moai",
  "scale_factor": 1.5,
  "output_name": "moai_grande"
}
```

**Clases Disponibles**:
- `moai`: Moai de Rapa Nui
- `sphinx`: Esfinge egipcia
- `egyptian_statue`: Estatua egipcia
- `colossus`: Coloso egipcio
- `pyramid_mesoamerican`: Pirámide mesoamericana
- `temple_platform`: Plataforma ceremonial
- `stela_maya`: Estela maya

**Response**:
```json
{
  "success": true,
  "png_filename": "moai_grande.png",
  "obj_filename": "moai_grande.obj",
  "morphological_class": "moai",
  "cultural_origin": "Rapa Nui (Easter Island)",
  "volume_m3": 150.0,
  "scale_factor": 1.5
}
```

**Ejemplo**:
```bash
curl -X POST http://localhost:8004/generate/morphology \
  -H "Content-Type: application/json" \
  -d '{
    "morphological_class": "sphinx",
    "scale_factor": 2.0
  }'
```

---

#### POST /generate/custom
Generar desde geometría completamente custom

**Request**:
```json
{
  "vertices": [
    [0, 0, 0],
    [10, 0, 0],
    [10, 10, 0],
    [0, 10, 0],
    [5, 5, 15]
  ],
  "faces": [
    [0, 1, 4],
    [1, 2, 4],
    [2, 3, 4],
    [3, 0, 4],
    [0, 2, 1],
    [0, 3, 2]
  ],
  "output_name": "mi_geometria"
}
```

**Response**:
```json
{
  "success": true,
  "png_filename": "mi_geometria.png",
  "obj_filename": "mi_geometria.obj",
  "vertices_count": 5,
  "faces_count": 6,
  "volume_m3": 500.0
}
```

---

#### POST /generate/description
Generar desde descripción textual (EN DESARROLLO)

**Request**:
```json
{
  "description": "Una pirámide alta con escalinata frontal",
  "style": "realistic"
}
```

**Status**: No implementado aún (placeholder)

---

### 3. Descarga de Modelos

#### GET /model/{filename}
Descargar archivo PNG o OBJ generado

**Ejemplo**:
```bash
# Descargar PNG
curl http://localhost:8004/model/mi_piramide.png -o mi_piramide.png

# Descargar OBJ
curl http://localhost:8004/model/mi_piramide.obj -o mi_piramide.obj
```

---

## 📁 Estructura de Archivos

```
creador3d/
├── __init__.py              # Módulo Python
├── api_creador3d.py         # API FastAPI
└── README.md                # Esta documentación

creador3d_models/            # Modelos generados
├── *.png                    # Imágenes renderizadas
└── *.obj                    # Geometría 3D exportada

run_creador3d.py             # Script de inicio
test_creador3d.py            # Suite de tests
```

---

## 🔧 Configuración

### Puerto
Por defecto: `8004`

Para cambiar, editar `run_creador3d.py`:
```python
uvicorn.run(
    "creador3d.api_creador3d:app",
    port=8004  # Cambiar aquí
)
```

### Directorio de Salida
Por defecto: `creador3d_models/`

Para cambiar, editar `api_creador3d.py`:
```python
OUTPUT_DIR = project_root / "creador3d_models"  # Cambiar aquí
```

---

## 🎨 Ejemplos de Uso

### Ejemplo 1: Pirámide Custom
```python
import requests

response = requests.post(
    "http://localhost:8004/generate/parameters",
    json={
        "height_m": 40.0,
        "width_m": 60.0,
        "shape_type": "pyramid",
        "color": "#A0826D"
    }
)

result = response.json()
print(f"Generado: {result['png_filename']}")
```

### Ejemplo 2: Moai Escalado
```python
import requests

response = requests.post(
    "http://localhost:8004/generate/morphology",
    json={
        "morphological_class": "moai",
        "scale_factor": 2.0
    }
)

result = response.json()
print(f"Moai generado: {result['volume_m3']:.2f} m³")
```

### Ejemplo 3: Geometría Custom
```python
import requests

# Tetraedro simple
vertices = [
    [0, 0, 0],
    [10, 0, 0],
    [5, 10, 0],
    [5, 5, 10]
]

faces = [
    [0, 1, 2],
    [0, 1, 3],
    [1, 2, 3],
    [2, 0, 3]
]

response = requests.post(
    "http://localhost:8004/generate/custom",
    json={
        "vertices": vertices,
        "faces": faces,
        "output_name": "tetraedro"
    }
)

result = response.json()
print(f"Generado: {result['png_filename']}")
```

---

## 🆚 Diferencias con ArcheoScope

| Aspecto | ArcheoScope (8003) | Creador3D (8004) |
|---------|-------------------|------------------|
| **Propósito** | Científico/arqueológico | Experimental/creativo |
| **Entrada** | Coordenadas geográficas | Parámetros/geometría |
| **Rigor** | Absoluto | Flexible |
| **Clasificación** | Automática cultural | Manual por usuario |
| **Restricciones** | Paradigma científico | Sin restricciones |
| **Uso** | Investigación | Exploración/prototipado |

---

## 🚀 Próximas Funcionalidades

### En Desarrollo
- [ ] Generación desde descripción textual (IA)
- [ ] Más tipos de formas (cilindros, esferas, custom)
- [ ] Texturas procedurales
- [ ] Iluminación avanzada
- [ ] Animaciones simples

### Planeadas
- [ ] Batch generation (múltiples modelos)
- [ ] Variaciones automáticas
- [ ] Export a más formatos (STL, FBX, GLTF)
- [ ] API de composición (combinar modelos)
- [ ] Biblioteca de templates

---

## 🐛 Troubleshooting

### API no inicia
```bash
# Verificar que el puerto 8004 esté libre
netstat -ano | findstr :8004

# Verificar dependencias
pip install fastapi uvicorn trimesh matplotlib numpy
```

### Error al generar modelo
```bash
# Verificar logs en consola
# Verificar que creador3d_models/ exista
# Verificar permisos de escritura
```

### Archivo no se descarga
```bash
# Verificar que el archivo exista
ls creador3d_models/

# Verificar nombre de archivo en response
```

---

## 📚 Documentación API

Documentación interactiva disponible en:
- Swagger UI: `http://localhost:8004/docs`
- ReDoc: `http://localhost:8004/redoc`

---

## 🤝 Contribuir

Esta API es experimental y está en desarrollo activo. 

**Ideas bienvenidas para**:
- Nuevos tipos de generación
- Formatos de entrada
- Funcionalidades creativas
- Optimizaciones

---

## 📄 Licencia

Parte del proyecto ArcheoScope.

---

## ✨ Créditos

Reutiliza la lógica de generación geométrica de:
- `backend/culturally_constrained_mig.py`
- `backend/morphological_repository.py`
- `backend/geometric_inference_engine.py`

Manteniendo separación clara entre ciencia y experimentación.
