# 🚀 FRONTEND TIMT ACTUALIZADO - v3.0

**Fecha**: 28 de Enero 2026  
**Sistema**: ArcheoScope TIMT (Territorial Inferential Multi-modal Tomography)

---

## 🎯 CAMBIOS PRINCIPALES

### Nuevo Frontend Completo
- **Archivo**: `frontend/index_timt.html`
- **JavaScript**: `frontend/archeoscope_timt.js`
- **Endpoint**: `/timt/analyze` (en lugar de `/analyze`)

### Sistema de 3 Capas Implementado

#### 🧩 CAPA 0: TCP (Territorial Context Profile)
**Visible en Tab "TCP"**
- Perfil territorial completo
- Hipótesis territoriales con scores de plausibilidad
- Estrategia instrumental dirigida
- Contexto geológico, hidrográfico, arqueológico

#### 🔬 CAPA 1: ETP (Environmental Tomographic Profile)
**Visible en Tab "ETP"**
- Perfil tomográfico 3D/4D
- Anomalías volumétricas
- ESS superficial y subsuperficial
- Coherencia 3D
- Visualización de capas tomográficas

#### ✅ CAPA 2: Validación + Transparencia
**Visible en Tab "Validación"**
- Validación de hipótesis territoriales
- Reporte de transparencia del sistema
- Comunicación multinivel (4 niveles)
- Limitaciones conocidas
- Fronteras del sistema

---

## 📊 FEATURES NUEVAS EN EL UI

### Panel Izquierdo - Configuración Avanzada
1. **Coordenadas** (lat/lon min/max)
2. **Nombre del territorio**
3. **Objetivo del análisis**:
   - 🔍 Exploratorio
   - ✅ Validación
   - 🎓 Académico
   - 📊 Monitoreo
4. **Radio de análisis** (1-50 km)
5. **Resolución** (10-1000 m)
6. **Nivel de comunicación**:
   - 👔 Ejecutivo
   - 🔧 Técnico
   - 🔬 Científico
   - 📚 Educativo

### Panel Central - Mapa Interactivo
- Click en mapa para seleccionar coordenadas
- Visualización del área de análisis
- Marcadores con información del territorio

### Panel Derecho - Resultados con Tabs

#### Tab "Resumen"
- **4 Métricas Separadas**:
  - 🎯 Origen Antropogénico
  - ⚡ Actividad Antropogénica
  - 📡 Anomalía Instrumental
  - 🔮 ESS Score
- **Métricas Adicionales**:
  - Coherencia Territorial
  - Rigor Científico
- **Cobertura Instrumental**:
  - Instrumentos utilizados vs disponibles
  - Barra de progreso visual
  - Lista de instrumentos con estado
- **Recomendación**:
  - Acción recomendada
  - Tipo de candidato
  - Confianza del modelo

#### Tab "TCP"
- **Perfil Territorial**:
  - TCP ID único
  - Objetivo del análisis
  - Potencial de preservación
  - Bioma histórico
  - Litología dominante
  - Características hidrográficas
  - Sitios arqueológicos externos
  - Trazas humanas conocidas
- **Hipótesis Territoriales**:
  - Cards con tipo de hipótesis
  - Score de plausibilidad
  - Explicación detallada
  - Instrumentos recomendados
  - Clasificación visual (validada/incierta/rechazada)
- **Estrategia Instrumental**:
  - Instrumentos prioritarios
  - Resolución recomendada
  - Lista de instrumentos seleccionados

#### Tab "ETP"
- **Perfil Tomográfico**:
  - Territory ID
  - Resolución del análisis
  - ESS superficial
  - ESS subsuperficial
  - Coherencia 3D
  - Número de capas tomográficas
- **Anomalías Volumétricas**:
  - Cards por cada anomalía
  - Tipo de anomalía
  - Volumen en m³
  - Rango de profundidad
  - Confianza
- **Visualización 3D**:
  - Placeholder para visor 3D (próximamente)

#### Tab "Validación"
- **Validación de Hipótesis**:
  - Cards por cada hipótesis validada
  - Resultado (validada/rechazada/incierta)
  - Evidencia de soporte
  - Contradicciones
  - Confianza de validación
  - Explicación detallada
- **Reporte de Transparencia**:
  - Hipótesis evaluadas
  - Hipótesis descartadas
  - Limitaciones conocidas
  - Fronteras del sistema
  - Lista de limitaciones
- **Comunicación Multinivel**:
  - **Nivel 1**: Qué se midió
  - **Nivel 2**: Por qué se midió
  - **Nivel 3**: Qué se infiere
  - **Nivel 4**: Qué NO se puede afirmar

---

## 🎨 DISEÑO VISUAL

### Tema Oscuro Moderno
- Fondo: Gradiente oscuro (#1a1a2e → #16213e)
- Paneles: Glass morphism con blur
- Colores de acento: Marrón arqueológico (#8B4513, #D2691E)

### Componentes Visuales
- **Badges**: success, warning, danger, info
- **Progress bars**: Animadas con gradiente
- **Cards**: Con bordes de color según estado
- **Tabs**: Navegación fluida entre secciones
- **Metrics**: Filas con labels y valores coloreados

### Estados Visuales
- ✅ **Success**: Verde (#2ecc71)
- ⚠️ **Warning**: Naranja (#f39c12)
- ❌ **Danger**: Rojo (#e74c3c)
- ℹ️ **Info**: Azul (#3498db)

---

## 🔌 INTEGRACIÓN CON BACKEND

### Endpoint Principal
```javascript
POST http://localhost:8002/timt/analyze
```

### Request Body
```json
{
  "lat_min": 31.76,
  "lat_max": 31.78,
  "lon_min": 130.60,
  "lon_max": 130.62,
  "territory_name": "Territorio Test",
  "analysis_objective": "exploratory",
  "analysis_radius_km": 5.0,
  "resolution_m": 30,
  "communication_level": "technical"
}
```

### Response Structure
```json
{
  "analysis_id": "...",
  "territorial_context": { /* TCP */ },
  "tomographic_profile": { /* ETP */ },
  "hypothesis_validations": [ /* Validaciones */ ],
  "transparency_report": { /* Transparencia */ },
  "multilevel_communication": { /* Comunicación */ },
  "anthropic_origin_probability": 0.35,
  "anthropic_activity_probability": 0.0,
  "instrumental_anomaly_probability": 0.0,
  "ess_score": 0.0,
  "territorial_coherence_score": 0.85,
  "scientific_rigor_score": 0.92,
  "recommended_action": "monitoring_passive",
  "candidate_type": "uncertain",
  "model_confidence": "low"
}
```

---

## 🚀 CÓMO USAR

### 1. Iniciar Backend
```bash
python run_archeoscope.py
# Backend en http://localhost:8002
```

### 2. Iniciar Frontend
```bash
python start_frontend.py
# Frontend en http://localhost:8080
# Abre automáticamente index_timt.html
```

### 3. Realizar Análisis
1. Ingresa coordenadas o haz click en el mapa
2. Configura parámetros (objetivo, radio, resolución)
3. Click en "🚀 Iniciar Análisis TIMT"
4. Espera 30-60 segundos
5. Explora resultados en los 4 tabs

---

## ✅ VERIFICACIÓN DE FEATURES

### CAPA 0 - TCP ✅
- [x] Perfil territorial completo
- [x] Hipótesis territoriales
- [x] Estrategia instrumental
- [x] Contexto geológico
- [x] Contexto hidrográfico
- [x] Sitios arqueológicos externos
- [x] Trazas humanas

### CAPA 1 - ETP ✅
- [x] Perfil tomográfico 3D
- [x] ESS superficial/subsuperficial
- [x] Coherencia 3D
- [x] Anomalías volumétricas
- [x] Capas tomográficas
- [ ] Visualización 3D interactiva (próximamente)

### CAPA 2 - Validación ✅
- [x] Validación de hipótesis
- [x] Reporte de transparencia
- [x] Comunicación multinivel (4 niveles)
- [x] Limitaciones conocidas
- [x] Fronteras del sistema
- [x] Hipótesis descartadas

### Métricas Científicas ✅
- [x] 4 métricas separadas (origen, actividad, anomalía, confianza)
- [x] ESS Score
- [x] Coherencia territorial
- [x] Rigor científico
- [x] Cobertura instrumental

---

## 📁 ARCHIVOS NUEVOS

1. `frontend/index_timt.html` - Frontend TIMT completo
2. `frontend/archeoscope_timt.js` - Controlador JavaScript
3. `FRONTEND_TIMT_ACTUALIZADO.md` - Esta documentación

## 📝 ARCHIVOS MODIFICADOS

1. `start_frontend.py` - Ahora abre `index_timt.html` por defecto

---

## 🔄 COMPARACIÓN: ANTES vs AHORA

| Feature | Antes (v2.2) | Ahora (v3.0 TIMT) |
|---------|--------------|-------------------|
| **Endpoint** | `/analyze` | `/timt/analyze` |
| **Contexto Territorial** | ❌ | ✅ TCP completo |
| **Hipótesis** | ❌ | ✅ Múltiples con validación |
| **Perfil Tomográfico** | ❌ | ✅ ETP 3D/4D |
| **Anomalías** | 2D | 3D volumétricas |
| **Métricas** | 1 score | 4 métricas + ESS |
| **Transparencia** | Básica | Completa con limitaciones |
| **Comunicación** | 1 nivel | 4 niveles |
| **Validación** | Sitios conocidos | Hipótesis + evidencia |
| **UI** | 1 panel | 4 tabs organizados |

---

## 🎯 PRÓXIMOS PASOS

1. **Visualización 3D**: Implementar visor Three.js para ETP
2. **Exportación**: Botones para exportar resultados (JSON, PDF)
3. **Historial**: Guardar análisis previos
4. **Comparación**: Comparar múltiples análisis
5. **Integración 15 instrumentos**: Cuando se complete el plan

---

**Estado**: ✅ FRONTEND TIMT v3.0 COMPLETADO  
**Compatibilidad**: Backend TIMT completo  
**Listo para**: Producción y testing científico
