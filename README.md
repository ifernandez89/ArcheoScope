# 🧊 CryoScope - Subglacial Coherence Engine

> **"Un amplificador de hipótesis espaciales para la glaciología moderna"**

[![Status](https://img.shields.io/badge/Status-Production-brightgreen)](https://github.com/ifernandez89/CryoScope)
[![AI](https://img.shields.io/badge/AI-Ollama%20Integrated-blue)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-red)](https://python.org)

## 🎯 **¿Qué es CryoScope?**

CryoScope es un **instrumento científico digital** diseñado para detectar anomalías glaciológicas y contradicciones en modelos físicos establecidos. No pretende ser un "detector de verdades", sino un **amplificador de hipótesis espaciales** que ayuda a los glaciólogos a identificar dónde las explicaciones actuales fallan.

### ✨ **Características Principales**

🤖 **IA Real Integrada** - Ollama + qwen2.5:3b-instruct ejecutándose localmente  
🎯 **Control Espacial Estricto** - Umbrales realistas basados en principios científicos  
🔍 **Indicadores Específicos** - Métricas trazables vinculadas a datos visibles  
⚖️ **Protección Epistemológica** - Rechazo automático de análisis inválidos  
🧩 **Tiles Prioritarios** - Subdivisión automática en zonas candidatas para estudio detallado  
📡 **Capas Alta Resolución** - Acceso a datos satelitales con coordenadas exactas  
🌐 **Interfaz Científica** - Diseñada para glaciólogos, no para marketing  

---

## 🎯 **Posicionamiento Científico**

> **"CryoScope no busca estructuras ocultas. Busca regiones donde los modelos físicos actuales dejan de explicar el comportamiento observado, y además indica cuándo esos resultados no son científicamente válidos por escala o contexto."**

Este es un **amplificador de hipótesis espaciales** que:
- Identifica dónde fallan las explicaciones glaciológicas actuales
- Proporciona tiles prioritarios para investigación detallada  
- Ofrece capas de alta resolución con coordenadas exactas
- Mantiene honestidad científica sobre sus limitaciones  

---

## 🚀 **Inicio Rápido**

### **1. Prerrequisitos**
```bash
# Python 3.11+
python --version

# Ollama (opcional, para IA)
# Instalar desde: https://ollama.ai/
ollama pull qwen2.5:3b-instruct
```

### **2. Instalación**
```bash
# Clonar repositorio
git clone https://github.com/ifernandez89/CryoScope.git
cd CryoScope

# Instalar dependencias básicas
pip install fastapi uvicorn numpy scipy requests

# Iniciar sistema
python demo_server.py
```

### **3. Acceso**
- **Frontend:** Abrir `frontend/index.html` en navegador
- **API:** http://localhost:8001
- **Docs:** http://localhost:8001/docs

---

## 🔬 **Cómo Funciona**

### **Análisis Multi-Escala Inteligente**

| Área | Modo | Comportamiento |
|------|------|----------------|
| ≤ 10 km² | 🎯 **Científico Fino** | Máxima resolución, resultados publicables |
| 10-100 km² | 🔬 **Analítico** | Válido con limitaciones claras |
| > 100 km² | 🚨 **RECHAZADO** | Área demasiado grande, análisis inválido |

### **Indicadores Específicos Detectados**
- 🔴 **Contradicciones Físicas:** Gradiente anómalo de velocidad, desequilibrio térmico
- 🟡 **Anomalías Estadísticas:** Desacople velocidad-topografía, inconsistencias
- 🟢 **Regiones Consistentes:** Comportamiento glaciológico esperado
- 🧩 **Tiles Prioritarios:** Zonas candidatas automáticas para estudio detallado
- 📡 **Capas Alta Resolución:** Datos satelitales exportables con coordenadas exactas

---

## 📊 **Ejemplo de Uso**

```python
# Análisis vía API
import requests

response = requests.post('http://localhost:8001/analyze', json={
    "lat_min": -75.1, "lat_max": -75.0,
    "lon_min": -109.1, "lon_max": -109.0,
    "region_name": "Región Test"
})

result = response.json()
print(f"IA Disponible: {result['ai_explanations']['ai_available']}")
print(f"Modo: {result['ai_explanations']['spatial_context']['analysis_mode']}")
print(f"Explicación: {result['ai_explanations']['explanation']}")
```

**Salida Esperada:**
```
IA Disponible: True
Modo: fine
Explicación: En esta región delimitada, las anomalías detectadas sugieren 
procesos de lubricación basal heterogénea que podrían estar influenciados 
por variaciones en la topografía del lecho rocoso no capturadas por los 
modelos estándar de flujo de hielo.
```

---

## 🛡️ **Protecciones Científicas**

### **Control Automático de Área**
```javascript
// El sistema automáticamente:
if (area > 100_km²) {
    mostrar_advertencia_critica();
    ofrecer_reduccion_automatica();
    rechazar_analisis();
}
```

### **Comunicación Honesta**
- ⚠️ Advertencias claras sobre limitaciones espaciales
- 📊 Indicadores específicos vinculados a métricas reales  
- 🎯 Tono probabilístico, no determinista
- 🔍 Transparencia total en metodología

---

## 🏗️ **Arquitectura**

```
CryoScope/
├── 🖥️  Backend (Python + FastAPI)
│   ├── demo_server.py          # Servidor principal
│   ├── ai/ollama_assistant.py  # Integración IA
│   ├── analysis/comparator.py  # Análisis multi-capa
│   └── rules/physics_rules.py  # Reglas glaciológicas
│
├── 🌐 Frontend (JavaScript + Leaflet)
│   ├── index.html              # Interfaz principal
│   └── simple_app.js           # Lógica científica
│
└── 📚 Documentación
    ├── README.md               # Este archivo
    └── SYSTEM_DOCUMENTATION.md # Documentación completa
```

---

## 🎮 **Interfaz de Usuario**

### **Controles Principales**
- 🗺️ **Selección de Región:** Coordenadas o selección en mapa
- 🔍 **Botón INVESTIGAR:** Ejecuta análisis completo
- 🎯 **Zoom Científico:** Optimización automática de área
- 🛰️ **Inspección Satelital:** Vista detallada de regiones críticas

### **Paneles Informativos**
- 📊 **Resumen de Análisis:** Métricas principales y modo de análisis
- 🎯 **Indicadores Específicos:** Anomalías detectadas con severidad
- 🤖 **Explicación IA:** Interpretación contextualizada (si disponible)
- ⚙️ **Estado del Sistema:** Disponibilidad de IA y componentes

---

## 🔧 **Configuración Avanzada**

### **Parámetros Espaciales**
```python
# En simple_app.js
spatialThresholds = {
    fine: 10,        # km² - Análisis científico fino
    medium: 100,     # km² - Análisis con limitaciones
    exploratory: 100 # km² - Umbral de rechazo
}
```

### **Configuración IA**
```python
# En demo_server.py
ollama_config = {
    "model": "qwen2.5:3b-instruct",
    "timeout": 60,
    "temperature": 0.3,
    "num_predict": 150
}
```

---

## 📈 **Casos de Uso**

### **1. Investigación Glaciológica**
- Detección de procesos subglaciales no modelados
- Identificación de heterogeneidades basales
- Validación de modelos físicos existentes

### **2. Análisis de Datos Satelitales**
- Procesamiento de datos MODIS/Landsat
- Detección de anomalías en velocidad de hielo
- Análisis de coherencia multi-temporal

### **3. Educación Científica**
- Herramienta didáctica para glaciología
- Demostración de principios físicos
- Entrenamiento en análisis espacial

---

## 🤝 **Contribuir**

### **Áreas de Desarrollo**
- 🔬 **Algoritmos:** Mejoras en detección de anomalías
- 🤖 **IA:** Optimización de prompts científicos
- 🌐 **Interfaz:** Nuevas funcionalidades de visualización
- 📊 **Datos:** Integración con fuentes reales

### **Proceso de Contribución**
1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📜 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para detalles.

---

## 🙏 **Agradecimientos**

- **Kiro AI** - Asistencia excepcional en desarrollo
- **Comunidad Ollama** - IA local accesible
- **Leaflet** - Mapas interactivos científicos
- **FastAPI** - Framework web moderno

---

## 📞 **Contacto**

- **Issues:** [GitHub Issues](https://github.com/ifernandez89/CryoScope/issues)
- **Discusiones:** [GitHub Discussions](https://github.com/ifernandez89/CryoScope/discussions)
- **Email:** [Contacto del proyecto]

---

## 🏆 **Estado del Proyecto**

✅ **Completado:** IA integrada, control espacial, indicadores específicos  
🚧 **En desarrollo:** Integración datos reales, algoritmos avanzados  
📋 **Planeado:** Exportación científica, validación de campo  

---

*"La ciencia avanza no solo descubriendo lo que sabemos, sino reconociendo honestamente lo que no sabemos."*

**CryoScope - Donde la glaciología encuentra la inteligencia artificial responsable** 🧊🤖

---

[![Made with ❤️ and 🧠](https://img.shields.io/badge/Made%20with-❤️%20and%20🧠-red)](https://github.com/ifernandez89/CryoScope)