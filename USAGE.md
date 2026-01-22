# 🔍 Subglacial Coherence Engine - Guía de Uso

> "Este sistema no detecta estructuras. Detecta lugares donde las explicaciones actuales fallan."

## Inicio Rápido

### 1. Ejecutar el Sistema Completo

```bash
python run_system.py
```

Este comando:
- ✅ Verifica dependencias
- 🚀 Inicia el servidor backend (puerto 8001)
- 🌐 Abre el frontend en tu navegador
- 📊 Muestra el estado del sistema

### 2. Usar la Interfaz Científica

#### 🔍 Verificación del Sistema
Antes de usar la interfaz, verifica que todo funciona:

```bash
# Verificar estado del backend
curl http://localhost:8001/status

# En Windows PowerShell:
Invoke-WebRequest -Uri "http://localhost:8001/status" -UseBasicParsing

# Probar análisis completo
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "lat_min": -75.5,
    "lat_max": -74.5, 
    "lon_min": -110.0,
    "lon_max": -108.0,
    "region_name": "Test Region"
  }'
```

#### 🧭 Selección de Región
- **Método 1**: Mantén `Ctrl` y arrastra en el mapa para seleccionar región
- **Método 2**: Ingresa coordenadas manualmente (lat/lon)
- **Método 3**: Usa regiones predefinidas

#### ⚙️ Parámetros Explícitos
- **Resolución**: 500m, 1km, 2km (recomendado: 1km)
- **Capas**: Velocidad, espesor, topografía basal
- **Reglas físicas**: Consistencia velocidad, espesor-topografía, deslizamiento basal

#### 🔍 Investigación
1. Presiona el botón **"INVESTIGAR"**
2. El sistema ejecuta automáticamente:
   - Carga/generación de datos
   - Análisis estadístico multi-capa
   - Evaluación de reglas físicas
   - Explicación IA (si disponible)
   - Generación de visualizaciones

#### 📊 Resultados
- **Panel derecho**: Anomalías, contradicciones, explicaciones
- **Mapa**: Visualización de regiones anómalas
- **Capas conmutables**: Alternar entre diferentes visualizaciones

## Interpretación Científica

### 🔴 Anomalías Estadísticas
- **Qué son**: Regiones donde las correlaciones esperadas fallan
- **Ejemplos**: Velocidad alta sin pendiente, espesor inconsistente con topografía
- **Significado**: Procesos glaciológicos no estándar

### 🟡 Contradicciones Físicas
- **Qué son**: Violaciones de reglas glaciológicas conocidas
- **Ejemplos**: Deslizamiento basal extenso, velocidades >3x esperadas
- **Significado**: Condiciones especiales que requieren investigación

### 🤖 Explicaciones IA
- **Disponible**: Narrativas contextualizadas de anomalías
- **No disponible**: Explicaciones deterministas estructuradas
- **Siempre**: Trazabilidad completa de la fuente

## Flujo de Trabajo Científico

### 1. Exploración Inicial
```
Seleccionar región → Investigar → Revisar anomalías generales
```

### 2. Análisis Detallado
```
Activar/desactivar capas → Examinar correlaciones → Identificar patrones
```

### 3. Investigación Específica
```
Ajustar parámetros → Re-investigar → Comparar resultados
```

### 4. Documentación
```
Exportar reporte → Guardar visualizaciones → Citar metodología
```

## Casos de Uso Típicos

### 🌊 Detección de Ice Streams
- **Buscar**: Velocidades altas sin justificación topográfica
- **Reglas**: Activar consistencia velocidad-pendiente
- **Resultado**: Identificación de corrientes de hielo activas

### 🏊 Lagos Subglaciales
- **Buscar**: Espesor anómalo vs topografía del lecho
- **Reglas**: Activar consistencia espesor-topografía
- **Resultado**: Evidencia de lagos o cavidades subglaciales

### 🛷 Deslizamiento Basal
- **Buscar**: Velocidades extremas vs deformación esperada
- **Reglas**: Activar detección deslizamiento basal
- **Resultado**: Zonas de lubricación basal activa

## Limitaciones y Consideraciones

### 📊 Datos Actuales
- **Fuente**: Sintéticos para demostración
- **Producción**: Requiere integración con datos reales (Sentinel, ICESat, BEDMAP)
- **Calidad**: Dependiente de resolución y cobertura temporal

### 🤖 IA Local
- **Disponible**: Explicaciones contextualizadas con Ollama
- **No disponible**: Fallbacks deterministas mantienen funcionalidad
- **Recomendación**: Usar modelos qwen2.5:3b-instruct o similares

### 🔬 Interpretación Científica
- **Sistema**: Detecta inconsistencias, no hace descubrimientos
- **Usuario**: Debe interpretar resultados con conocimiento glaciológico
- **Validación**: Siempre verificar con datos de campo cuando sea posible

## Solución de Problemas

### ❌ Backend no inicia
```bash
# Verificar dependencias
pip install -r backend/requirements.txt

# Verificar puerto disponible
netstat -an | grep 8001
```

### ❌ Frontend no carga
- Verificar que el archivo `frontend/index.html` existe
- Usar servidor HTTP local si hay problemas de CORS
- Verificar consola del navegador para errores

### ❌ IA no disponible
```bash
# Iniciar Ollama
ollama serve

# Verificar modelos disponibles
ollama list

# Descargar modelo recomendado
ollama pull qwen2.5:3b-instruct
```

### ❌ Análisis falla
- Verificar coordenadas válidas (latitud: -90 a 90, longitud: -180 a 180)
- Verificar que al menos una capa esté seleccionada
- Revisar logs del backend para errores específicos

## API Endpoints

### Información del Sistema
- `GET /`: Información básica
- `GET /status`: Estado de componentes
- `GET /docs`: Documentación interactiva

### Análisis Principal
- `POST /analyze`: Ejecutar análisis completo

```json
{
  "lat_min": -75.5,
  "lat_max": -74.5,
  "lon_min": -110.0,
  "lon_max": -108.0,
  "resolution_m": 1000,
  "layers_to_analyze": ["ice_velocity", "ice_thickness", "bedrock_elevation"],
  "active_rules": ["all"],
  "region_name": "Pine Island Glacier"
}
```

## Desarrollo y Extensión

### Agregar Nuevas Reglas Físicas
1. Crear clase heredando de `PhysicsRule`
2. Implementar método `evaluate()`
3. Agregar al `RulesEngine`

### Integrar Datos Reales
1. Modificar `RasterLoader` para soportar GeoTIFF
2. Actualizar `create_synthetic_region_data()` en API
3. Agregar validación de coordenadas reales

### Personalizar Visualizaciones
1. Modificar `app.js` para nuevos tipos de capas
2. Agregar controles en `index.html`
3. Actualizar estilos CSS según necesidades

---

**Principio Fundamental**: Este sistema es un instrumento científico para detectar donde las explicaciones glaciológicas actuales son insuficientes, no un generador de conclusiones automáticas.