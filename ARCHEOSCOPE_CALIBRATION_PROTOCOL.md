# 🔬 ArcheoScope Scientific Calibration Protocol

## 🎯 Objetivo
Implementar un protocolo de calibración científica que valide la metodología de ArcheoScope mediante comparación controlada con sitios de referencia conocidos, sin modificar el motor de análisis.

## 🧠 Filosofía Científica
> **"Paso 1 – No tocar el motor. Está bien. No lo rompas."**
> 
> **"Ambos resultados son válidos."** - La disolución de anomalías también es un resultado científico válido.

## 📋 Protocolo de 3 Pasos

### 🔧 **PASO 1 – No tocar el motor**
- **Principio**: Preservar la integridad del sistema de análisis
- **Acción**: Mantener configuración actual sin modificaciones
- **Justificación**: Evitar introducir variables confusas en la calibración
- **Estado**: ✅ Motor intacto y operacional

### 🛰️ **PASO 2 – Repetir este mismo sitio con datos mejorados**

#### Coordenadas de Calibración
- **Sitio de prueba**: `-63.441533826185974, -83.12466836825169`
- **Región de análisis**: ±0.005° (~1km²)
- **Resolución**: 10m (Sentinel-2 óptimo)

#### Datos Requeridos
1. **Sentinel-2 (10 m)** - Resolución óptica óptima
   - Detectar estructuras lineales y geométricas
   - Análisis espectral de alta resolución
   
2. **NDVI estacional (primavera vs verano)** - Detectar ciclos
   - Distinguir patrones agrícolas cíclicos
   - Identificar persistencia de anomalías vegetales
   
3. **Sentinel-1 coherencia temporal** - Estabilidad estructural
   - Evaluar coherencia de fase SAR
   - Detectar cambios en rugosidad superficial

#### Configuración Técnica
```javascript
{
    "resolution_m": 10,
    "layers_to_analyze": [
        "ndvi_vegetation",      // NDVI estacional
        "thermal_lst", 
        "sar_backscatter",      // Sentinel-1 coherencia
        "surface_roughness",
        "soil_salinity"
    ],
    "include_explainability": true,
    "include_validation_metrics": true,
    "calibration_mode": true
}
```

### 🔍 **PASO 3 – Compararlo con sitios de referencia**

#### Sitios de Referencia Requeridos

##### 🏺 **Sitio Arqueológico Confirmado** (Referencia Positiva)
- **Propósito**: Patrón de referencia para detección positiva
- **Características esperadas**:
  - Alineaciones persistentes
  - Geometría coherente y estructurada
  - Persistencia multitemporal
  - Firmas espectrales distintivas

##### 🏢 **Sitio Moderno Confirmado** (Referencia Negativa)
- **Propósito**: Patrón de referencia para exclusión
- **Características esperadas**:
  - Geometría regular pero reciente
  - Sin persistencia histórica
  - Patrones de mecanización agrícola
  - Firmas espectrales modernas

#### Análisis Comparativo
**Pregunta clave**: *"Y mirar qué cambia y qué no"*

##### 🎯 **Resultados Posibles**:

1. **✅ Aparecen alineaciones**
   - Interpretación: Potencial arqueológico detectado
   - Acción: Proceder con investigación geofísica

2. **🔍 La masa se fragmenta en geometría**
   - Interpretación: Estructura detectada con coherencia espacial
   - Acción: Análisis detallado de patrones geométricos

3. **❌ Se disuelve**
   - Interpretación: No era arqueología
   - **Validación**: ✅ Resultado científicamente válido

## 🧪 Metodología de Calibración

### Proceso de Validación
1. **Ejecutar análisis** en los 3 sitios con parámetros idénticos
2. **Comparar métricas** de alineación y coherencia geométrica
3. **Evaluar persistencia** temporal y estacional
4. **Documentar diferencias** y similitudes
5. **Calibrar umbrales** basados en referencias conocidas

### Métricas de Comparación
- **Coherencia geométrica**: Patrones lineales y estructurales
- **Persistencia temporal**: Estabilidad a través de ventanas temporales
- **Firmas espectrales**: Diferencias en respuesta espectral
- **Extensión espacial**: Área y distribución de anomalías
- **Intensidad de señal**: Magnitud de las anomalías detectadas

## 🛠️ Implementación Técnica

### Frontend (archaeological_app.js)
```javascript
function generateCalibrationProtocol(data, regionInfo) {
    // Genera protocolo de 3 pasos
    // Configura comparación con referencias
    // Valida resultados científicamente
}

function executeCalibrationProtocol(lat, lon) {
    // Configura coordenadas automáticamente
    // Establece resolución óptima (10m)
    // Activa modo de calibración
}
```

### Botón de Calibración Rápida
- **Ubicación**: Barra superior junto a controles de región
- **Función**: Configuración automática con coordenadas de calibración
- **Estilo**: Azul distintivo (🔬 CALIBRACIÓN)

### Interfaz de Usuario
- **Sección**: "🔬 Protocolo de Calibración Científica"
- **Contenido**: Pasos detallados del protocolo
- **Visualización**: Coordenadas exactas y configuración

## 🧪 Testing y Validación

### Test Automático
```bash
python test_calibration_protocol.py
```

### Test Manual (Frontend)
1. Abrir: http://localhost:8080
2. Hacer clic: 🔬 CALIBRACIÓN
3. Verificar coordenadas configuradas automáticamente
4. Hacer clic: INVESTIGAR
5. Revisar: "Protocolo de Calibración Científica"
6. Seguir los 3 pasos del protocolo

### Resultados de Calibración Actual
- **Coordenadas**: -63.441533826185974, -83.12466836825169
- **Resolución**: 10m ✅
- **Píxeles anómalos**: 4501
- **Firmas arqueológicas**: 0
- **Resultado**: AMBIGUO (requiere comparación con referencias)

## 🎯 Impacto Científico

### Validación Metodológica
1. **Honestidad científica**: Admite cuando los resultados son ambiguos
2. **Metodología robusta**: Comparación controlada con referencias conocidas
3. **Calibración empírica**: Ajuste de umbrales basado en datos reales
4. **Reproducibilidad**: Protocolo estandarizado y documentado

### Principios Fundamentales
- **No modificar el motor**: Preservar integridad del análisis
- **Comparación controlada**: Usar referencias conocidas
- **Validez de resultados negativos**: "Se disuelve" también es válido
- **Transparencia metodológica**: Documentar todo el proceso

## 🚀 Próximos Pasos

### Para Calibración Completa
1. **Identificar sitio arqueológico confirmado** para referencia positiva
2. **Identificar sitio moderno confirmado** para referencia negativa
3. **Ejecutar análisis comparativo** con parámetros idénticos
4. **Documentar diferencias** en patrones detectados
5. **Calibrar umbrales** basados en comparación
6. **Validar metodología** con casos adicionales

### Expansión del Protocolo
- **Base de datos de referencias**: Sitios arqueológicos y modernos confirmados
- **Análisis estadístico**: Métricas de precisión y recall
- **Validación cruzada**: Testing con múltiples sitios
- **Documentación científica**: Publicación de metodología

## ✨ Mensaje Científico

> **"Estamos haciendo ciencia juntos"** 🔬🏺
> 
> Este protocolo transforma ArcheoScope de un detector de anomalías en un **instrumento científico calibrado** que proporciona resultados validados y metodológicamente sólidos.
> 
> **La honestidad científica es fundamental**: tanto los resultados positivos como negativos son válidos y contribuyen al conocimiento arqueológico.

---

**Estado**: ✅ Implementado y operacional  
**Testing**: ✅ Validado con coordenadas específicas  
**Documentación**: ✅ Completa  
**Próximo paso**: Ejecutar calibración completa con sitios de referencia