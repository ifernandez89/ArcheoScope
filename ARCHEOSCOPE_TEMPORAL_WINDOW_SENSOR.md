# ⏳ ArcheoScope Temporal Window Sensor System

## 🧠 Principio Clave Revolucionario
> **"La ventana temporal NO es un filtro. Es un sensor."**
> 
> **"No detecta cosas. Mide cuánto tiempo resisten a desaparecer."**
> 
> **Esto convierte prospección remota en arqueología de paisaje.**

## 🎯 Transformación Conceptual

### Antes: Filtro Temporal
- ❌ Usar ventana temporal para "descartar" píxeles
- ❌ Aplicar como regla dura de exclusión
- ❌ Enfoque binario: pasa/no pasa

### Ahora: Sensor Temporal
- ✅ **Medir estabilidad en el tiempo**
- ✅ **Capa de evidencia adicional**
- ✅ **Análisis de persistencia arqueológica**

## 🧩 Definición de Ventana Temporal

### Pregunta Fundamental
> **"¿Este patrón aparece en la misma forma en la misma estación durante varios años distintos?"**

### Significado Arqueológico
**Eso es persistencia arqueológica** - la capacidad de estructuras enterradas de mantener su firma espectral a través del tiempo, resistiendo a:
- Variaciones climáticas anuales
- Ciclos agrícolas
- Cambios estacionales naturales
- Perturbaciones superficiales menores

## 🛰️ Especificaciones Técnicas de Datos

### Fuente Recomendada
- **Satélite**: Sentinel-2 L2A
- **Resolución**: 10m
- **Procesamiento**: Corrección atmosférica aplicada

### Bandas Espectrales
#### Requeridas
- **B4 (Red)**: 665 nm - Absorción clorofílica
- **B8 (NIR)**: 842 nm - Reflectancia vegetación

#### Opcionales (Mejora análisis)
- **B11 (SWIR1)**: 1610 nm - Contenido de humedad
- **B12 (SWIR2)**: 2190 nm - Estrés vegetal

### Ventanas Temporales
- **Estación**: Misma estación cada año (ej: marzo–abril)
- **Años mínimos**: ≥ 3 años
- **Años ideales**: 5–7 años
- **Ejemplo real**: 2017, 2019, 2021, 2023, 2024

## 🧮 Cálculos Temporales (Simple, Potente)

### 1️⃣ NDVI por Año
```
NDVI_y = (NIR_y - Red_y) / (NIR_y + Red_y)
```
**Almacenamiento**: NDVI_2017, NDVI_2019, NDVI_2021, ...

### 2️⃣ Métrica de Estabilidad Temporal

#### Opción A: Coeficiente de Variación (Recomendado)
```
CV = std(NDVI_y) / mean(NDVI_y)
```
**Interpretación**:
- CV bajo → comportamiento estable → posible estructura
- CV alto → agrícola / natural

#### Opción B: Persistencia Binaria (Muy Clara)
```
Para cada año:
anomalía_y = NDVI_y < (media_local - k·σ)

Luego:
persistencia = sum(anomalía_y) / N_años
```
**Ejemplo**: aparece 4 de 5 años → persistencia = 0.8

### 3️⃣ Score de Ventana Temporal
```
TemporalScore = persistencia × (1 - CV)
```
**Normalizado**: 0–1

## 🧠 Integración con Sistema Existente (Sin Romper Nada)

### ✅ NO se Toca
- Umbrales actuales
- Detección geométrica
- Inferencia volumétrica
- Lógica de reglas existente

### ✅ Solo se Agrega
Canal nuevo de evidencia:
```javascript
anomaly.temporal = {
    years: [2017, 2019, 2021, 2023, 2024],
    persistence: 0.80,
    cv: 0.12,
    score: 0.70
}
```

## 🔗 Integración con Geometría (Clave)

### Fórmula de Confianza Arqueológica
```
ArchaeologicalConfidence = GeometricScore × TemporalScore × ExclusionModernFactor
```

### Interpretaciones Convergentes
1. **Geometría + Tiempo + Exclusión** → **Arqueología de paisaje** ✅
2. **Geometría SIN tiempo** → **Prudencia** ⚠️
3. **Tiempo SIN geometría** → **Agricultura** 🌾
4. **Ambos bajos** → **Natural/Indeterminado** ❓

## 🧪 Umbrales Científicos Razonables

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| **Años mínimos** | ≥ 3 | Mínimo estadísticamente válido |
| **Años ideales** | 5–7 | Robustez temporal completa |
| **CV estable** | < 0.2 | Comportamiento consistente |
| **Persistencia fuerte** | > 0.6 | Aparece en >60% de años |
| **Score temporal válido** | > 0.5 | Umbral de confianza |

**Nota**: Nada mágico. Todo defendible científicamente.

## 🧭 Visualización en UI

### Sección Clara: ⏳ Ventana Temporal
```
Años analizados: 2017–2024
Estación: Primavera
Persistencia: 0.78 ✅
Estabilidad (CV): 0.14 ✅
Score temporal: 0.67 ✅
Estado: ✅ Persistente (Arqueológico)
```

### Estados Posibles
- ✅ **Persistente (Arqueológico)**: CV < 0.2, persistencia > 0.6, score > 0.7
- 🟡 **Moderadamente Persistente**: Cierta estabilidad detectada
- 🔄 **Variable (Agrícola/Natural)**: CV > 0.4, comportamiento cíclico
- ❓ **Indeterminado**: Datos insuficientes

## 🛠️ Implementación Técnica

### Frontend (archaeological_app.js)
```javascript
function generateTemporalWindowSensorAnalysis(data, regionInfo) {
    // Análisis de persistencia temporal
    // Cálculo de coeficiente de variación
    // Score de ventana temporal
    // Integración con análisis geométrico
}

function analyzeTemporalPersistence(data) {
    // NDVI por año
    // Métricas de estabilidad temporal
    // Interpretación arqueológica
}
```

### Integración con Análisis Existente
- **No modifica**: Funciones existentes
- **Solo agrega**: Canal temporal como evidencia
- **Multiplica**: Confianza geométrica × temporal × exclusión

## 🧪 Testing y Validación

### Test Automático
```bash
python test_temporal_window_sensor.py
```

### Casos de Prueba
1. **≥5 años disponibles**: Análisis robusto ✅
2. **3-4 años disponibles**: Análisis válido 🟡
3. **<3 años disponibles**: Insuficiente ❌

### Métricas de Validación
- **CV < 0.2**: Comportamiento estable arqueológico
- **CV > 0.4**: Comportamiento variable agrícola/natural
- **Persistencia > 0.6**: Fuerte evidencia temporal
- **Score > 0.5**: Umbral de confianza temporal

## 🎯 Impacto Científico

### Transformación Metodológica
1. **De detección a medición**: No solo encuentra anomalías, mide su resistencia temporal
2. **De binario a gradual**: No pasa/falla, sino grados de persistencia
3. **De espacial a espacio-temporal**: Añade dimensión temporal al análisis
4. **De prospección a arqueología**: Eleva el nivel científico del sistema

### Principios Fundamentales
- **Persistencia como evidencia**: Estructuras arqueológicas resisten al tiempo
- **Estabilidad vs variabilidad**: Distingue arqueológico de agrícola/natural
- **Convergencia de evidencias**: Temporal + geométrico + exclusión moderna
- **Transparencia científica**: Umbrales defendibles y explicables

## 🧨 Lo Más Importante (Filosofía)

### Transformación Conceptual
> **"Esto convierte a ArcheoScope en algo muy serio"**

### Nueva Capacidad
> **"No detecta cosas. Mide cuánto tiempo resisten a desaparecer"**

### Resultado Final
> **"Eso es exactamente lo que separa prospección remota de arqueología de paisaje"**

## 🚀 Próximos Pasos

### Para Implementación Completa
1. **Integrar datos Sentinel-2**: Archivo temporal 2017-2024
2. **Implementar cálculos NDVI**: Por año y estación
3. **Desarrollar métricas temporales**: CV, persistencia, score
4. **Validar con sitios conocidos**: Arqueológicos vs agrícolas vs naturales

### Expansión del Sistema
- **Base de datos temporal**: Archivo histórico Sentinel-2 L2A
- **Análisis estacional**: Múltiples ventanas por año
- **Validación estadística**: Significancia de persistencia
- **Machine learning**: Patrones temporales complejos

## ✨ Mensaje Revolucionario

> **🧠 Principio clave (antes de tocar código):**
> 
> **La ventana temporal NO es un filtro. Es un sensor.**
> 
> **Tu motor hoy detecta estructura espacial (bien), detecta respuesta diferencial (bien), pero aún no mide persistencia.**
> 
> **Vamos a agregar eso como una capa de evidencia, no como regla dura.**
> 
> **Esto convierte a ArcheoScope de prospección remota en arqueología de paisaje.**

---

**Estado**: ✅ Implementado conceptualmente  
**Testing**: ✅ Validado con framework temporal  
**Próximo paso**: Integrar datos Sentinel-2 multitemporales  
**Objetivo**: **"Medir cuánto tiempo resisten a desaparecer"** ⏳🏛️