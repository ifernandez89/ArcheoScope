# 🗺️ ¿Qué Falta? - Roadmap ArcheoScope

**Fecha**: 2026-01-26  
**Status Actual**: Sistema operacional con limitaciones

---

## ✅ LO QUE TENEMOS (Completado)

### 1. Backend Core
- ✅ FastAPI con 50+ endpoints
- ✅ PostgreSQL con 80,457 sitios arqueológicos
- ✅ Clasificador de ambientes (7 tipos)
- ✅ Detector de anomalías multi-ambiente
- ✅ Sistema de confianza de sitios (pesos probabilísticos)
- ✅ Validación contra sitios conocidos
- ✅ IA integrada (Ollama + OpenRouter)

### 2. Sistema de Zonas Prioritarias
- ✅ 3 estrategias (buffer, gradient, gaps)
- ✅ Optimización bayesiana (5-15% territorio → 80% candidatos)
- ✅ Scoring multi-criterio (5 factores)
- ✅ Clases LiDAR (GOLD, SILVER, BRONZE, WATER)

### 3. Enriquecimiento Multi-Instrumental
- ✅ 10 tipos de instrumentos soportados
- ✅ Convergencia multi-instrumental
- ✅ Persistencia temporal (lo humano persiste, lo natural fluctúa)
- ✅ Scoring ponderado por confiabilidad
- ✅ Interpretación de señales por instrumento

### 4. Base de Datos de Candidatas
- ✅ Tabla `archaeological_candidates` con 23 campos
- ✅ 11 índices para búsquedas eficientes
- ✅ 2 vistas (priority_candidates, candidates_statistics)
- ✅ 7 endpoints para CRUD de candidatas
- ✅ Seguimiento de estados (pending → analyzing → analyzed → field_validated)

### 5. Frontend
- ✅ Mapa interactivo Leaflet
- ✅ Visualización de zonas prioritarias
- ✅ Regiones predefinidas (Petén, Amazonia, Angkor, Egipto, Perú)
- ✅ Estadísticas en tiempo real
- ✅ Lista de zonas GOLD CLASS

### 6. Testing y Validación
- ✅ 100+ scripts de test
- ✅ Validación con sitios conocidos
- ✅ Tests de determinismo
- ✅ Análisis de cobertura geográfica

---

## ❌ LO QUE FALTA (Crítico)

### 1. 🔴 DATOS INSTRUMENTALES REALES

**Problema**: Actualmente usamos **datos simulados** para todos los instrumentos.

**Falta**:
- ❌ Integración con APIs reales de Sentinel-1 (SAR)
- ❌ Integración con APIs reales de Sentinel-2 (Multiespectral)
- ❌ Integración con APIs reales de Landsat-8 (Térmico)
- ❌ Integración con APIs reales de LiDAR (OpenTopography, USGS)
- ❌ Análisis multitemporal con archivos históricos

**Impacto**: 🔴 CRÍTICO - Sin datos reales, el sistema es solo una demostración

**Solución**:
```python
# Actualmente (simulado):
available_data = enrichment_system._simulate_instrumental_data(zone)

# Necesitamos:
available_data = {
    'sar': await sentinel1_api.get_backscatter(lat, lon, date_range),
    'multispectral': await sentinel2_api.get_ndvi(lat, lon, date_range),
    'thermal': await landsat8_api.get_lst(lat, lon, date_range),
    'lidar': await opentopography_api.get_dem(lat, lon),
    'multitemporal': await analyze_temporal_persistence(lat, lon, years=10)
}
```

**APIs a integrar**:
1. **Copernicus Open Access Hub** (Sentinel-1, Sentinel-2) - GRATIS
2. **USGS Earth Explorer** (Landsat-8) - GRATIS
3. **OpenTopography** (LiDAR) - GRATIS con registro
4. **Google Earth Engine** (Multitemporal) - GRATIS académico
5. **ASF DAAC** (SAR avanzado) - GRATIS

---

### 2. 🟠 EVALUACIÓN IA DE COHERENCIA ARQUEOLÓGICA

**Problema**: La IA está integrada pero **NO se usa** en el scoring de zonas prioritarias.

**Falta**:
- ❌ Implementar `evaluate_archaeological_coherence()` en el flujo
- ❌ Llamar a IA ANTES del análisis instrumental
- ❌ Usar coherencia IA en el scoring (peso 25%)

**Impacto**: 🟠 ALTO - Perdemos el 25% del scoring más importante

**Código actual**:
```python
# En calculate_zone_priority_score():
ai_coherence: Optional[Dict[str, Any]] = None  # ❌ Siempre None
```

**Necesitamos**:
```python
# Evaluar coherencia IA para cada zona
ai_coherence = await site_confidence_system.evaluate_archaeological_coherence(
    zone, nearby_sites, ai_assistant
)

# Usar en scoring
scoring = calculate_zone_priority_score(
    zone, 
    lidar_available=True,
    ai_coherence=ai_coherence  # ✅ Ahora sí se usa
)
```

---

### 3. 🟠 MAPA INTERACTIVO CON CANDIDATAS ENRIQUECIDAS

**Problema**: El mapa usa el sistema BASE sin enriquecimiento multi-instrumental.

**Falta**:
- ❌ Actualizar mapa para usar `/enriched-candidates`
- ❌ Mostrar convergencia de instrumentos
- ❌ Mostrar persistencia temporal
- ❌ Mostrar interpretación de señales
- ❌ Botón "Analizar Zona" funcional

**Impacto**: 🟠 ALTO - Los usuarios ven scores más bajos de lo real

**Solución**:
```javascript
// Cambiar de:
const url = `${API_BASE}/archaeological-sites/recommended-zones-geojson?...`;

// A:
const url = `${API_BASE}/archaeological-sites/enriched-candidates?...`;

// Y agregar visualización de:
- Convergencia: 5/5 instrumentos ✅
- Persistencia: 11 años ✅
- Señales: SAR, Térmico, NDVI, Multitemporal
```

---

### 4. 🟡 HARVESTING DE SITIOS SUDAMERICANOS

**Problema**: Solo 748 sitios sudamericanos, 0 en Amazonía Occidental.

**Falta**:
- ❌ Mejorar harvesting de Wikidata (filtro geográfico)
- ❌ Agregar sitios de OSM con tags arqueológicos
- ❌ Importar catálogos nacionales (INAH México, IPHAN Brasil, etc.)
- ❌ Enriquecer metadatos de país (90% sin país)

**Impacto**: 🟡 MEDIO - Limita uso en regiones amazónicas

**Regiones sin cobertura**:
- Amazonía Occidental (Brasil)
- Amazonía Peruana
- Amazonía Colombiana
- Amazonía Ecuatoriana

**Solución**:
```python
# Agregar filtros geográficos al harvesting
harvest_sites(
    regions=['South America', 'Central America'],
    countries=['Brazil', 'Peru', 'Colombia', 'Ecuador', 'Bolivia'],
    min_confidence='LOW'  # Incluir más sitios
)
```

---

### 5. 🟡 ANÁLISIS INSTRUMENTAL COMPLETO

**Problema**: El endpoint `/analyze` existe pero no usa el sistema multi-instrumental.

**Falta**:
- ❌ Integrar enriquecimiento multi-instrumental en `/analyze`
- ❌ Retornar señales de todos los instrumentos
- ❌ Guardar resultados en `analysis_results` de candidatas
- ❌ Actualizar estado a 'analyzed' automáticamente

**Impacto**: 🟡 MEDIO - No hay flujo completo de análisis

**Flujo deseado**:
```
1. Usuario selecciona zona prioritaria
2. Sistema genera candidata enriquecida
3. Usuario hace clic en "Analizar Zona"
4. Sistema ejecuta análisis instrumental completo
5. Resultados se guardan en BD
6. Estado cambia a 'analyzed'
7. Usuario puede marcar como 'field_validated'
```

---

### 6. 🟢 EXPORTACIÓN Y REPORTES

**Falta**:
- ❌ Exportar candidatas a KML (Google Earth)
- ❌ Exportar candidatas a Shapefile (QGIS)
- ❌ Exportar candidatas a CSV
- ❌ Generar reportes PDF con mapas
- ❌ Generar reportes académicos (LaTeX)

**Impacto**: 🟢 BAJO - Nice to have

---

### 7. 🟢 VALIDACIÓN DE CAMPO

**Falta**:
- ❌ Formulario para registrar validación de campo
- ❌ Subir fotos de campo
- ❌ Registrar coordenadas GPS reales
- ❌ Comparar predicción vs realidad
- ❌ Métricas de precisión del sistema

**Impacto**: 🟢 BAJO - Para uso avanzado

---

### 8. 🟢 OPTIMIZACIONES

**Falta**:
- ❌ Cache de resultados instrumentales
- ❌ Pre-procesamiento de regiones populares
- ❌ Paralelización de análisis
- ❌ Compresión de datos históricos
- ❌ CDN para tiles de mapa

**Impacto**: 🟢 BAJO - Performance

---

## 🎯 PRIORIDADES (Orden de Implementación)

### 🔴 CRÍTICO (Hacer YA)

**1. Integración de Datos Instrumentales Reales**
- Tiempo estimado: 2-3 semanas
- Complejidad: Alta
- Impacto: Transforma el sistema de demo a producción

**Pasos**:
1. Registrarse en Copernicus Open Access Hub
2. Implementar cliente para Sentinel-1 (SAR)
3. Implementar cliente para Sentinel-2 (Multiespectral)
4. Implementar cliente para Landsat-8 (Térmico)
5. Implementar análisis multitemporal
6. Reemplazar `_simulate_instrumental_data()` con datos reales

---

### 🟠 ALTO (Hacer Pronto)

**2. Evaluación IA de Coherencia**
- Tiempo estimado: 3-5 días
- Complejidad: Media
- Impacto: Mejora scoring en 25%

**3. Mapa con Candidatas Enriquecidas**
- Tiempo estimado: 2-3 días
- Complejidad: Baja
- Impacto: Mejor UX y visualización

---

### 🟡 MEDIO (Hacer Después)

**4. Harvesting Sudamericano**
- Tiempo estimado: 1 semana
- Complejidad: Media
- Impacto: Expande cobertura geográfica

**5. Análisis Instrumental Completo**
- Tiempo estimado: 1 semana
- Complejidad: Media
- Impacto: Flujo completo de trabajo

---

### 🟢 BAJO (Nice to Have)

**6. Exportación y Reportes**
- Tiempo estimado: 1 semana
- Complejidad: Baja
- Impacto: Conveniencia

**7. Validación de Campo**
- Tiempo estimado: 2 semanas
- Complejidad: Media
- Impacto: Métricas de precisión

**8. Optimizaciones**
- Tiempo estimado: Continuo
- Complejidad: Variable
- Impacto: Performance

---

## 📊 Estado Actual del Sistema

### Funcionalidad: 70%
- ✅ Arquitectura completa
- ✅ Base de datos operacional
- ✅ APIs implementadas
- ✅ Frontend básico
- ❌ Datos instrumentales reales
- ❌ IA coherencia integrada

### Usabilidad: 60%
- ✅ Mapa interactivo
- ✅ Regiones predefinidas
- ✅ Estadísticas
- ❌ Candidatas enriquecidas en mapa
- ❌ Análisis on-demand
- ❌ Exportación

### Precisión: 40%
- ✅ Algoritmos correctos
- ✅ Scoring multi-criterio
- ✅ Convergencia instrumental
- ❌ Datos simulados (no reales)
- ❌ Sin validación de campo
- ❌ Sin métricas de precisión

### Cobertura: 50%
- ✅ 80,457 sitios globales
- ✅ Europa bien cubierta
- ✅ Algunas regiones sudamericanas
- ❌ Amazonía Occidental sin sitios
- ❌ 90% sitios sin país
- ❌ Sesgado hacia Europa

---

## 🚀 Roadmap Sugerido

### Fase 1: DATOS REALES (Crítico)
**Objetivo**: Transformar de demo a producción

1. Integrar Sentinel-1 (SAR)
2. Integrar Sentinel-2 (Multiespectral)
3. Integrar Landsat-8 (Térmico)
4. Implementar multitemporal
5. Validar con sitios conocidos

**Resultado**: Sistema con datos reales, scores precisos

---

### Fase 2: IA Y UX (Alto)
**Objetivo**: Mejorar scoring y experiencia de usuario

1. Implementar evaluación IA coherencia
2. Actualizar mapa con candidatas enriquecidas
3. Agregar análisis on-demand
4. Mejorar visualización de señales

**Resultado**: Scoring completo (100%), mejor UX

---

### Fase 3: COBERTURA (Medio)
**Objetivo**: Expandir geográficamente

1. Mejorar harvesting sudamericano
2. Agregar catálogos nacionales
3. Enriquecer metadatos
4. Validar cobertura por región

**Resultado**: Cobertura global equilibrada

---

### Fase 4: PRODUCCIÓN (Bajo)
**Objetivo**: Sistema completo para uso real

1. Exportación (KML, Shapefile, CSV)
2. Reportes académicos
3. Validación de campo
4. Métricas de precisión
5. Optimizaciones

**Resultado**: Sistema production-ready

---

## 💡 Conclusión

**¿Qué falta?**

**Lo más crítico**:
1. 🔴 **Datos instrumentales reales** (sin esto, es solo una demo)
2. 🟠 **IA coherencia integrada** (perdemos 25% del scoring)
3. 🟠 **Mapa con candidatas enriquecidas** (mejor visualización)

**Lo importante**:
4. 🟡 **Harvesting sudamericano** (más cobertura)
5. 🟡 **Análisis instrumental completo** (flujo end-to-end)

**Lo deseable**:
6. 🟢 **Exportación y reportes** (conveniencia)
7. 🟢 **Validación de campo** (métricas)
8. 🟢 **Optimizaciones** (performance)

**Estado actual**: Sistema **70% funcional** con arquitectura sólida pero **datos simulados**.

**Próximo paso crítico**: **Integrar APIs de datos satelitales reales** (Sentinel-1, Sentinel-2, Landsat-8).

---

**Desarrollado**: 2026-01-26  
**Sistema**: ArcheoScope - Archaeological Remote Sensing Engine  
**Versión**: 1.3.0
