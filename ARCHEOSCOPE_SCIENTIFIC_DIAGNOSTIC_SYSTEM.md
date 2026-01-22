# ArcheoScope Scientific Data Diagnostic System

## 🔬 Sistema de Diagnóstico Científico Implementado

### Objetivo
Transformar ArcheoScope de un detector de anomalías a un **instrumento científico honesto** que evalúa la calidad de los datos disponibles y proporciona retroalimentación transparente sobre sus capacidades interpretativas.

## 🎯 Filosofía Científica

> **"El sistema no dijo: 'no funciona'. Dijo: 'necesito ver mejor para hablar'. Eso es exactamente lo que hace un geofísico, un arqueólogo de paisaje, un instrumento científico honesto."**

## 📊 Niveles de Diagnóstico

### 🔴 NIVEL 1 - DATOS CRÍTICOS PARA INTERPRETACIÓN

#### 1. Resolución Espacial
- **Problema**: "Viendo el paisaje como una manta desde un satélite"
- **Solución**: "Necesitas ver las costuras"
- **Requerimientos**:
  - Sentinel-2 a 10m (óptico) ✅
  - Sentinel-1 SAR a 10m ✅
  - Landsat solo como apoyo temporal
- **Habilita**:
  - Detectar alineaciones
  - Medir rectilinealidad
  - Calcular persistencia geométrica
  - Distinguir parche vs estructura

#### 2. Ventanas Temporales Comparables
- **Problema**: "Persistencia multitemporal: no disponible" (no es error, es verdad)
- **Requerimientos**:
  - Mismas fechas estacionales
  - Al menos 3-5 años
  - Mismas bandas/sensores
- **Habilita**:
  - Distinguir: agrícola cíclico ❌ vs natural episódico ❌ vs antrópico persistente ✅
  - Activa la innovación: **"Tiempo como sensor"**

### 🟠 NIVEL 2 - DATOS QUE DESBLOQUEAN LA INTERPRETACIÓN

#### 3. Contexto Geomorfológico Explícito
- **Problema**: "Detecta anomalías pero no sabe contra qué geología compite"
- **Datos útiles**:
  - Mapas geológicos
  - Suelos (FAO/ISRIC)
  - Hidrología histórica
- **Habilita**:
  - Descartar: abanicos aluviales, coluviones, terrazas naturales
  - Reforzar anomalías "inexplicables"
  - **Reduce falsos positivos sin tocar umbrales**

#### 4. Huella Humana Moderna Formal
- **Mejoras**:
  - Límites parcelarios actuales
  - Catastros históricos
  - Infraestructuras del siglo XX
  - Patrones de mecanización agrícola
- **Habilita**:
  - Decir: "esto fue alterado, pero no es arqueología"
  - **Eso es ciencia, no fracaso**

### 🟡 NIVEL 3 - DATOS QUE TRANSFORMAN EL SISTEMA

#### 5. Ground Truth Indirecto (sin excavación)
- **No necesitas palas**:
  - Sitios arqueológicos conocidos
  - Otros confirmadamente no arqueológicos
- **Para entrenar**:
  - Umbrales
  - Pesos bayesianos
  - Explicabilidad
- **Resultado**: Convierte ArcheoScope en **instrumento calibrado, no solo detector**

#### 6. Microtopografía Real
- **No SRTM**:
  - LiDAR (cuando exista)
  - Fotogrametría
  - DEM local
- **Habilita**:
  - Distinguir micro-relieves antrópicos de ondulaciones naturales

## 🚦 Estados de Diagnóstico

### 🔴 CRÍTICO - Datos Insuficientes
- **Condición**: Resolución > 30m O ventanas temporales < 3
- **Mensaje**: "DATOS INSUFICIENTES PARA INTERPRETACIÓN CIENTÍFICA"
- **Acción**: No proceder con interpretación hasta resolver datos críticos

### 🟠 LIMITADO - Interpretación Básica
- **Condición**: Datos críticos OK, pero faltan datos de contexto
- **Mensaje**: "INTERPRETACIÓN LIMITADA - DATOS BÁSICOS DISPONIBLES"
- **Acción**: Proceder con cautela científica

### 🟡 VÁLIDO - Interpretación Confiable
- **Condición**: Niveles 1 y 2 completos, falta optimización
- **Mensaje**: "INTERPRETACIÓN VÁLIDA - OPTIMIZACIÓN POSIBLE"
- **Acción**: Interpretación confiable con recomendaciones de mejora

### ✅ ÓPTIMO - Interpretación Científica Completa
- **Condición**: Todos los niveles completos
- **Mensaje**: "DATOS ÓPTIMOS PARA INTERPRETACIÓN CIENTÍFICA"
- **Acción**: Interpretación completa y confiable

## 🛠️ Implementación Técnica

### Frontend (archaeological_app.js)
```javascript
function generateDataDiagnostic(data, regionInfo) {
    // Evalúa resolución, series temporales, contexto geomorfológico
    // Genera diagnóstico honesto con recomendaciones específicas
    // Retorna estado clasificado (crítico/limitado/válido/óptimo)
}
```

### HTML (index.html)
```html
<div class="controls-section">
    <h3>🔬 Diagnóstico Científico de Datos</h3>
    <div id="dataDiagnostic">
        <!-- Diagnóstico dinámico aquí -->
    </div>
</div>
```

### Estilos CSS
- `.data-diagnostic.critical` - Fondo rojo para datos insuficientes
- `.data-diagnostic.limited` - Fondo naranja para interpretación limitada
- `.data-diagnostic.valid` - Fondo amarillo para interpretación válida
- `.data-diagnostic.optimal` - Fondo verde para datos óptimos

## 🧪 Testing

### Tests Automáticos
- `test_diagnostic_system.py` - Test backend del diagnóstico
- `test_frontend_diagnostic.html` - Test interactivo del frontend

### Casos de Prueba
1. **Resolución 500m**: Debería mostrar 🔴 CRÍTICO
2. **Resolución 10m**: Debería mostrar 🟡 VÁLIDO
3. **Datos completos**: Debería mostrar ✅ ÓPTIMO

## 📋 Resumen Ejecutivo

### Para que ArcheoScope interprete, necesita:
- 🔴 **Resolución 10–30m** (crítico)
- 🔴 **Series temporales comparables** (crítico)
- 🟠 **Contexto geomorfológico** (importante)
- 🟠 **Huella humana moderna explícita** (importante)
- 🟡 **Sitios de referencia** (optimización)

### Mensaje Clave
**No más "datos". Datos correctos, en el orden correcto.**

## 🎯 Impacto Científico

1. **Honestidad Científica**: El sistema admite sus limitaciones
2. **Educación del Usuario**: Explica qué datos necesita y por qué
3. **Reducción de Falsos Positivos**: Contextualiza las detecciones
4. **Calibración Instrumental**: Convierte detector en instrumento científico
5. **Transparencia Metodológica**: Explica el proceso de toma de decisiones

## 🚀 Estado Actual

- ✅ **Implementado**: Sistema completo de diagnóstico
- ✅ **Operativo**: Frontend y backend funcionando
- ✅ **Documentado**: Guías de uso y testing
- ✅ **Probado**: Tests automáticos y manuales

### URLs de Acceso
- **Frontend Principal**: http://localhost:8080
- **Test Diagnóstico**: http://localhost:8080/test_frontend_diagnostic.html
- **Backend API**: http://localhost:8004

El sistema ahora proporciona retroalimentación científica honesta sobre la calidad de los datos y sus capacidades interpretativas, transformando ArcheoScope en un verdadero instrumento científico.