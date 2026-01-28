# 🔬 TEST CANDIDATO 743 - RESULTADOS COMPLETOS

**Fecha**: 28 de Enero de 2026  
**Sistema**: ArcheoScope v2.2  
**Pipeline**: Científico Determinístico (7 Fases)

---

## 📍 CANDIDATO TESTEADO

- **ID**: d5ecd7fd-109c-4e29-9dcd-4ffcdb53b0d0
- **Nombre**: 山田の凱旋門 (Yamada no Gaisen-mon)
- **País**: China
- **Coordenadas**: 31.7737506°N, 130.6142744°E
- **Tipo**: URBAN_SETTLEMENT
- **Ambiente**: FOREST
- **Confianza**: MODERATE

---

## 🔬 ANÁLISIS EJECUTADO

### Componentes Inicializados ✅

1. **ScientificPipeline**: Pipeline científico de 7 fases
2. **RealArchaeologicalValidator**: Validador con 10 sitios conocidos
3. **EnvironmentClassifier**: Clasificador de ambientes
4. **RealDataIntegrator**: Integrador de datos satelitales (8/11 APIs = 72.7%)

### APIs Disponibles

- ✅ Sentinel-2 (NDVI)
- ✅ Sentinel-1 (SAR)
- ✅ Landsat 8 (NDVI)
- ✅ ICESat-2
- ✅ NSIDC
- ✅ MODIS LST
- ✅ Copernicus Marine
- ✅ OpenTopography (DEM/LiDAR)
- ❌ Earthdata (credenciales no configuradas)
- ❌ Copernicus Marine (credenciales no configuradas)
- ❌ OpenTopography API key (inválida)

---

## 📊 RESULTADOS CIENTÍFICOS

### 🎯 Métricas Separadas (4 Métricas Independientes)

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Origen Antropogénico** | 35.0% | Probabilidad de origen humano |
| **Actividad Antropogénica** | 0.0% | Sin evidencia de actividad humana reciente |
| **Anomalía Instrumental** | 0.0% | Sin anomalías detectadas por instrumentos |
| **Confianza del Modelo** | LOW | Baja confianza debido a cobertura limitada |

### 🔮 ESS (Explanatory Strangeness Score)

- **Nivel**: NONE
- **Score**: 0.00
- **Razón**: Ajustado por alta incertidumbre epistemológica

### 🛰️ Cobertura Instrumental

| Métrica | Valor | Detalle |
|---------|-------|---------|
| **Instrumentos Medidos** | 3/5 | 60% de cobertura raw |
| **Cobertura Raw** | 60.0% | 3 instrumentos de 5 disponibles |
| **Cobertura Normalizada** | 0.0% | Ponderada por importancia de instrumentos |
| **Cobertura Efectiva** | 0.0% | Instrumentos críticos faltantes |

### 📡 Mediciones Instrumentales Exitosas

1. **Sentinel-2 NDVI**: 0.360
   - Fuente: Planetary Computer
   - Modo: Real data
   - Estado: ✅ Exitoso

2. **Landsat 8 NDVI**: 0.360
   - Fuente: Planetary Computer
   - Modo: Real data
   - Estado: ✅ Exitoso

3. **Sentinel-1 SAR**: 0.133 dB (VV)
   - Fuente: Planetary Computer
   - Modo: Real data (cached)
   - Escenas: 17 encontradas
   - Fecha: 2026-01-22
   - Estado: ✅ Exitoso (con cache)

### ❌ Mediciones Fallidas

1. **MODIS LST**: Error de conexión
2. **OpenTopography**: API key inválida

---

## 🌍 CONTEXTO AMBIENTAL

- **Tipo de Ambiente**: AGRICULTURAL
- **Confianza**: 50%
- **Visibilidad Arqueológica**: Media
- **Potencial de Preservación**: Medio

---

## 🔬 PIPELINE CIENTÍFICO - FASES EJECUTADAS

### Fase 0: Enriquecimiento con BD
- ✅ Ejecutada
- Resultado: No hay mediciones históricas en la zona

### Fase A: Normalización
- ✅ Ejecutada
- Features normalizadas: 6
- Instrumentos: Landsat 8 NDVI, Sentinel-2 NDVI, Sentinel-1 SAR

### Fase B: Detección de Anomalía Pura
- ✅ Ejecutada
- Anomaly Score: 0.000
- Outliers: 0
- Confianza: LOW

### Fase C: Análisis Morfológico
- ✅ Ejecutada
- Simetría: 1.000 (alta)
- Regularidad: 0.000
- Planaridad: 1.000 (superficie plana)
- Indicadores: `alta_simetria`, `superficie_plana`
- Geomorfología: `terrain_general`

### Fase D: Inferencia Antropogénica
- ✅ Ejecutada
- ⚠️ **ALTA INCERTIDUMBRE EPISTEMOLÓGICA**: 70.0%
- Probabilidad antropogénica: 0.350 [0.25, 0.45]
- Inference confidence: LOW (basada en evidencia)
- System confidence: HIGH (determinístico, reproducible)
- Razonamiento:
  - ⚠️ Alta incertidumbre: cobertura 0% (instrumentos críticos faltantes)
  - Alta simetría detectada
  - Superficie plana no erosiva
  - Indicadores: alta_simetria, superficie_plana

### Fase E: Verificación de Anti-patrones
- ✅ Ejecutada
- Resultado: No se detectaron anti-patrones

### Fase F: Validación contra Sitios Conocidos
- ✅ Ejecutada
- Sitios solapados: 0
- Sitios cercanos: 0
- Resultado: No hay sitios conocidos cercanos

### Fase G: Salida Científica
- ✅ Ejecutada
- Umbral de decisión: 0.50 (ambiente agricultural)
- ⚠️ Probabilidad 0.350 por debajo de umbral 0.50
- Acción: **MONITORING_PASSIVE**

---

## 💡 RECOMENDACIÓN FINAL

| Campo | Valor |
|-------|-------|
| **Acción Recomendada** | MONITORING_PASSIVE |
| **Tipo de Candidato** | UNCERTAIN |
| **Tipo de Descarte** | NONE |
| **Confianza Científica** | MEDIUM_HIGH |
| **Prioridad** | 0.00 |

### Notas

> Sin anomalía detectable (score=0.000); probabilidad antropogénica moderada (0.350) bajo alta incertidumbre - monitoreo pasivo recomendado

---

## 🔬 ETIQUETADO EPISTEMOLÓGICO

| Propiedad | Valor |
|-----------|-------|
| **Modo Epistémico** | deterministic_scientific |
| **IA Utilizada** | FALSE ❌ |
| **Reproducible** | TRUE ✅ |
| **Transparencia Metodológica** | FULL ✅ |

---

## ✅ VERIFICACIÓN DE FEATURES

### 1. Métricas Separadas ✅
- ✅ Origen antropogénico: 35.0%
- ✅ Actividad antropogénica: 0.0%
- ✅ Anomalía instrumental: 0.0%
- ✅ Confianza del modelo: LOW

### 2. ESS (Explanatory Strangeness Score) ✅
- ✅ Implementado y calculado
- ✅ Nivel: NONE (ajustado por incertidumbre)
- ✅ Score: 0.00

### 3. Cobertura Instrumental ✅
- ✅ Medidos: 3/5 instrumentos
- ✅ Cobertura raw: 60.0%
- ✅ Cobertura normalizada: 0.0%
- ✅ Cobertura efectiva: 0.0%

### 4. Contexto Ambiental ✅
- ✅ Tipo: AGRICULTURAL
- ✅ Confianza: 50%
- ✅ Visibilidad arqueológica: Media

### 5. Pipeline Científico Determinístico ✅
- ✅ 7 Fases ejecutadas (0, A-F, G)
- ✅ 100% Determinístico
- ✅ 0% IA en decisiones
- ✅ Reproducible

### 6. Mediciones Instrumentales Reales ✅
- ✅ Sentinel-2: Datos reales de Planetary Computer
- ✅ Landsat 8: Datos reales de Planetary Computer
- ✅ Sentinel-1 SAR: Datos reales (17 escenas, cached)

### 7. Endpoints Verificados ✅
- ✅ `/status`: Funcionando
- ✅ `/test-analyze`: Funcionando (test de conectividad)
- ✅ Pipeline científico: Funcionando (llamada directa)
- ⚠️ `/api/scientific/analyze`: No disponible en API actual

---

## 🚀 CONCLUSIONES

### ✅ Éxitos

1. **Pipeline científico funcionando correctamente** con 7 fases
2. **Métricas separadas implementadas** (origen vs actividad)
3. **ESS calculado** y ajustado por incertidumbre
4. **Cobertura instrumental reportada** con detalle
5. **Mediciones reales** de Sentinel-2, Landsat 8, Sentinel-1
6. **Sistema 100% determinístico** sin IA en decisiones
7. **Etiquetado epistemológico completo**
8. **Cache de SAR funcionando** (optimización)

### ⚠️ Limitaciones Detectadas

1. **Cobertura instrumental limitada**: Solo 3/5 instrumentos (60%)
2. **Instrumentos críticos faltantes**: DEM, MODIS LST
3. **Alta incertidumbre epistemológica**: 70%
4. **Credenciales faltantes**: Earthdata, Copernicus Marine
5. **API key inválida**: OpenTopography
6. **Endpoint `/api/scientific/analyze` no disponible** en API actual

### 🔧 Recomendaciones

1. **Configurar credenciales faltantes**:
   - Earthdata (NASA)
   - Copernicus Marine
   - OpenTopography API key

2. **Mejorar cobertura instrumental**:
   - Activar DEM (OpenTopography)
   - Solucionar MODIS LST
   - Integrar instrumentos adicionales (HydroSHEDS, USGS Geology, ERA5)

3. **Exponer endpoint científico**:
   - Verificar inclusión de `/api/scientific/analyze` en API
   - Documentar endpoint en OpenAPI

4. **Expandir a 15 instrumentos**:
   - Implementar plan de integración de 5 datasets adicionales
   - Seguir roadmap de 2 semanas

---

## 📁 ARCHIVOS GENERADOS

- `candidato_743_results_20260128_144043.json`: Resultados completos en JSON
- `backend/test_candidato_743_backend.py`: Script de test
- `TEST_CANDIDATO_743_RESULTADOS.md`: Este documento

---

**Estado**: ✅ TEST COMPLETADO CON ÉXITO  
**Duración**: ~1 minuto  
**Sistema**: ArcheoScope v2.2 - Pipeline Científico Determinístico
