# 🏛️ Archeoscope: The Forgotten Relics

**Explora civilizaciones antiguas y descubre reliquias olvidadas**

Un juego inmersivo de exploración arqueológica que te permite viajar por sitios históricos, descubrir artefactos antiguos y desentrañar los misterios de civilizaciones perdidas.

---

## 🚀 Quick Start

### 1. Iniciar API Creador3D
```bash
python run_creador3d.py
```
API disponible en: `http://localhost:8004`

### 2. Iniciar Visualizador 3D
```bash
start_viewer3d.bat
```
Visualizador disponible en: `http://localhost:3000`

---

## 📦 Componentes del Ecosistema

### 🎨 Creador3D API (Puerto 8004)
API REST experimental para generación de modelos 3D.

**Características**:
- Generación desde parámetros geométricos
- Generación desde clases morfológicas
- Generación desde geometría custom
- Export a PNG y OBJ
- Reutiliza lógica de backend científico

**Endpoints**:
- `POST /generate/parameters` - Generar desde parámetros
- `POST /generate/morphology` - Generar desde morfología
- `POST /generate/custom` - Generar geometría custom
- `GET /model/{filename}` - Descargar modelo
- `GET /morphologies` - Listar clases disponibles

**Documentación**: Ver `creador3d/README.md`

---

### 🌐 Visualizador 3D (Puerto 3000)
Visualizador web interactivo con Next.js + React Three Fiber + Core Engine.

**Características**:
- **Core Engine Profesional**: Runtime completo para experiencias 3D
- Carga de modelos .glb/.gltf con progreso
- Sistema de cámara avanzado (orbital + cinematográfico)
- Iluminación dinámica con simulación de hora del día
- Sistema de eventos (click, hover, proximity)
- Timeline interno para eventos temporales
- Postprocessing (Bloom, SSAO)
- Estado global con Zustand
- Auto-rotación con toggle
- Sombras y reflejos realistas
- UI moderna y responsive

**Arquitectura**:
- **CAPA 1**: Core Engine (loader, camera, lighting, events, timeline)
- **CAPA 2**: Motor de Experiencias (scenes, transitions)
- **CAPA 3**: Motor IA (próximamente)
- **CAPA 4**: Motor Astronómico + Geoespacial (próximamente)

**Controles**:
- Click izquierdo + arrastrar: Rotar
- Click derecho + arrastrar: Mover cámara
- Scroll: Zoom
- Click en modelo: Toggle auto-rotación

**Documentación**: 
- Ver `viewer3d/README.md`
- Ver `viewer3d/CORE_ENGINE.md` (arquitectura completa)

---

### 🏛️ Backend Core
Core mínimo del backend para soporte de Creador3D.

**Componentes**:
- `culturally_constrained_mig.py` - Motor de inferencia geométrica
- `morphological_repository.py` - Repositorio de clases morfológicas
- `geometric_inference_engine.py` - Engine de inferencia

**Clases Morfológicas**:
1. MOAI (Rapa Nui)
2. SPHINX (Egipto)
3. EGYPTIAN_STATUE (Egipto)
4. COLOSSUS (Egipto)
5. PYRAMID_MESOAMERICAN (Mesoamérica)
6. TEMPLE_PLATFORM (Mesoamérica)
7. STELA_MAYA (Mesoamérica)

---

## 🎯 Casos de Uso

### 1. Generar Modelo desde Parámetros
```bash
curl -X POST http://localhost:8004/generate/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "height_m": 30,
    "width_m": 50,
    "shape_type": "pyramid",
    "color": "#D4A574"
  }'
```

### 2. Generar Modelo desde Morfología
```bash
curl -X POST http://localhost:8004/generate/morphology \
  -H "Content-Type: application/json" \
  -d '{
    "morphological_class": "moai",
    "scale_factor": 1.5
  }'
```

### 3. Visualizar Modelo
1. Genera un modelo con la API
2. Obtén el nombre del archivo del response
3. Abre el visualizador: `http://localhost:3000`
4. El modelo se carga automáticamente

---

## 📁 Estructura del Proyecto

```
creador3d-ecosystem/
├── creador3d/              # API experimental
│   ├── __init__.py
│   ├── api_creador3d.py   # API FastAPI
│   └── README.md          # Documentación
│
├── viewer3d/              # Visualizador 3D
│   ├── app/               # Next.js App Router
│   ├── components/        # Componentes React
│   ├── core/              # Core Engine (runtime)
│   ├── experience/        # Motor de Experiencias
│   ├── store/             # Estado global (Zustand)
│   ├── public/            # Archivos estáticos
│   ├── README.md          # Documentación
│   └── CORE_ENGINE.md     # Arquitectura del Core Engine
│
├── backend/               # Core mínimo
│   ├── culturally_constrained_mig.py
│   ├── morphological_repository.py
│   └── geometric_inference_engine.py
│
├── models_3d/             # Modelos 3D de entrada
│   └── warrior.glb        # Modelo de prueba
│
├── creador3d_models/      # Modelos generados
│   ├── *.png              # Renders
│   └── *.obj              # Geometría 3D
│
├── run_creador3d.py       # Iniciar API
├── start_viewer3d.bat     # Iniciar visualizador
├── test_creador3d.py      # Tests de la API
└── README.md              # Este archivo
```

---

## 🔧 Instalación

### Requisitos
- Python 3.8+
- Node.js 18+
- npm o yarn

### Backend (Creador3D API)
```bash
pip install fastapi uvicorn trimesh matplotlib numpy pydantic
```

### Frontend (Visualizador 3D)
```bash
cd viewer3d
npm install
```

---

## 🧪 Testing

### Test de la API
```bash
python test_creador3d.py
```

### Test Manual
```bash
# 1. Iniciar API
python run_creador3d.py

# 2. Verificar status
curl http://localhost:8004/status

# 3. Generar modelo de prueba
curl -X POST http://localhost:8004/generate/morphology \
  -H "Content-Type: application/json" \
  -d '{"morphological_class": "moai", "scale_factor": 1.0}'
```

---

## 🎨 Tecnologías

### Backend
- **FastAPI**: Framework web moderno
- **Trimesh**: Procesamiento de geometría 3D
- **Matplotlib**: Rendering de imágenes
- **NumPy**: Cálculos numéricos

### Frontend
- **Next.js 14**: Framework React
- **React Three Fiber**: React renderer para Three.js
- **@react-three/drei**: Helpers 3D
- **@react-three/postprocessing**: Efectos visuales
- **Three.js**: Motor 3D WebGL
- **Zustand**: Estado global
- **TypeScript**: Type safety
- **Core Engine**: Runtime profesional para experiencias 3D

---

## 📚 Documentación

### APIs
- **Creador3D API**: `creador3d/README.md`
- **Visualizador 3D**: `viewer3d/README.md`
- **Core Engine**: `viewer3d/CORE_ENGINE.md` (arquitectura completa)

### Swagger UI
- API Docs: `http://localhost:8004/docs`
- ReDoc: `http://localhost:8004/redoc`

---

## 🔗 Integración

### Cargar Modelos en el Visualizador

**Desde archivo local**:
```tsx
<ModelViewer modelPath="/warrior.glb" />
```

**Desde Creador3D API**:
```tsx
<ModelViewer modelPath="http://localhost:8004/model/moai.glb" />
```

**Workflow completo**:
```javascript
// 1. Generar modelo
const response = await fetch('http://localhost:8004/generate/morphology', {
  method: 'POST',
  body: JSON.stringify({ morphological_class: 'moai' })
})

const result = await response.json()

// 2. Cargar en visualizador
const modelPath = `http://localhost:8004/model/${result.obj_filename}`
```

---

## 🚀 Roadmap

### Corto Plazo
- [x] Core Engine profesional (FASE 1 completa)
- [x] Sistema de iluminación dinámica
- [x] Sistema de eventos y timeline
- [x] Postprocessing (Bloom, SSAO)
- [ ] Selector de modelos en visualizador
- [ ] Panel de control de iluminación avanzado
- [ ] Captura de screenshots
- [ ] Más tipos de formas (cilindros, esferas)

### Mediano Plazo
- [ ] FASE 2: Motor de Experiencias completo
  - [ ] Sistema de escenas multi-escena
  - [ ] Audio reactivo
  - [ ] Texto contextual 3D
  - [ ] Narrativa temporal
- [ ] Galería de modelos con thumbnails
- [ ] Comparación lado a lado
- [ ] Mediciones y anotaciones
- [ ] Texturas procedurales
- [ ] Batch generation

### Largo Plazo
- [ ] FASE 3: Motor IA
  - [ ] Animaciones procedurales
  - [ ] Movimiento reactivo al usuario
  - [ ] Micro-expresiones
  - [ ] Control por LLM
- [ ] FASE 4: Motor Astronómico + Geoespacial
  - [ ] Mapa 3D global (Cesium)
  - [ ] Simulación solar real
  - [ ] Alineamientos astronómicos
  - [ ] Coordenadas geoespaciales
- [ ] Editor 3D interactivo
- [ ] Generación desde descripción textual (IA)
- [ ] Export a más formatos (STL, FBX, GLTF)
- [ ] AR/VR support
- [ ] Colaboración en tiempo real

---

## 🤝 Contribuir

Este es un proyecto experimental. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa y prueba
4. Crea un pull request

---

## 📄 Licencia

MIT License - Ver LICENSE para más detalles

---

## 🎯 Filosofía del Proyecto

**Separación de Responsabilidades**:
- Creador3D: Experimentación libre sin restricciones
- Backend Core: Lógica científica reutilizable
- Visualizador: Presentación profesional

**Principios**:
- Código modular y mantenible
- APIs REST bien documentadas
- Performance optimizado
- Experiencia de usuario fluida

---

## 📞 Soporte

Para preguntas o issues:
- Revisa la documentación en `creador3d/README.md` y `viewer3d/README.md`
- Abre un issue en GitHub
- Consulta los ejemplos en `test_creador3d.py`

---

**¡Disfruta creando y visualizando modelos 3D!** 🎨✨
