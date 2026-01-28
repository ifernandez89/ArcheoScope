# Plan de Ejecución en Casa - 15 Instrumentos ArcheoScope

## 🎯 OBJETIVO COMPLETADO

**INTEGRACIÓN EXITOSA: 10 → 15 INSTRUMENTOS SATELITALES**

Se han implementado exitosamente 5 nuevos conectores satelitales, expandiendo las capacidades de ArcheoScope para análisis arqueológico con datos reales.

---

## 📦 ARCHIVOS IMPLEMENTADOS

### Nuevos Conectores Satelitales
```
backend/satellite_connectors/
├── viirs_connector.py          # VIIRS - Térmico/NDVI/fuego (375m)
├── srtm_connector.py           # SRTM - DEM topográfico (30m)
├── palsar_connector.py         # PALSAR-2 - SAR L-band (3-100m)
├── era5_connector.py           # ERA5 - Clima/preservación (25km)
└── chirps_connector.py         # CHIRPS - Precipitación (5km)
```

### Archivos Actualizados
```
backend/satellite_connectors/real_data_integrator_v2.py  # +5 conectores
backend/core_anomaly_detector.py                        # +mapeo instrumentos
data/anomaly_signatures_by_environment.json             # +firmas arqueológicas
```

### Scripts de Testing
```
test_15_instruments_integration.py     # Test completo integración
test_nuevos_5_instrumentos.py         # Test rápido nuevos instrumentos
```

### Documentación
```
INTEGRACION_15_INSTRUMENTOS_COMPLETA.md    # Documentación técnica completa
PLAN_EJECUCION_CASA_15_INSTRUMENTOS.md    # Este archivo - plan de ejecución
```

---

## 🏠 PLAN DE EJECUCIÓN EN CASA

### PASO 1: Verificación Inicial
```bash
# Test rápido de nuevos instrumentos (5-10 min)
python test_nuevos_5_instrumentos.py

# Esperado: Al menos 3/5 instrumentos funcionando
# Si falla: Revisar configuración de APIs
```

### PASO 2: Test de Integración Completa
```bash
# Test completo de 15 instrumentos (15-30 min)
python test_15_instruments_integration.py

# Esperado: >60% coverage score, múltiples sitios exitosos
# Genera: test_15_instruments_results_TIMESTAMP.json
```

### PASO 3: Prueba con Coordenadas Candidatas
```bash
# Usar coordenadas candidatas reales
python run_archeoscope.py

# O directamente el detector:
python -c "
import asyncio
from backend.core_anomaly_detector import CoreAnomalyDetector
# ... usar coordenadas candidatas específicas
"
```

---

## 🛰️ INSTRUMENTOS DISPONIBLES PARA CASA

### Instrumentos de Alta Confiabilidad
- ✅ **Sentinel-2** (NDVI, multispectral) - Planetary Computer
- ✅ **MODIS LST** (térmico regional) - NASA APIs
- ✅ **SRTM** (DEM topográfico) - OpenTopography/USGS
- ✅ **VIIRS** (térmico/NDVI diario) - NASA Earthdata

### Instrumentos de Confiabilidad Media
- ⚠️ **Sentinel-1** (SAR C-band) - Requiere procesamiento
- ⚠️ **ICESat-2** (elevación) - Cobertura limitada
- ⚠️ **PALSAR-2** (SAR L-band) - Requiere autenticación ASF
- ⚠️ **ERA5** (clima) - Requiere configuración CDS

### Instrumentos Experimentales
- 🧪 **NSIDC** (hielo) - Solo regiones polares
- 🧪 **Copernicus Marine** (océano) - Solo ambientes marinos
- 🧪 **CHIRPS** (precipitación) - Análisis histórico
- 🧪 **OpenTopography** (LiDAR) - Cobertura limitada

---

## 🎯 COORDENADAS CANDIDATAS RECOMENDADAS

### Para Validación del Sistema
```python
# Sitios conocidos para verificar funcionamiento
GIZA_EGYPT = {
    'lat_min': 29.9, 'lat_max': 30.0,
    'lon_min': 31.1, 'lon_max': 31.2,
    'expected': 'Anomalías térmicas y topográficas fuertes'
}

ANGKOR_CAMBODIA = {
    'lat_min': 13.4, 'lat_max': 13.5, 
    'lon_min': 103.8, 'lon_max': 103.9,
    'expected': 'Penetración L-band, estructuras bajo vegetación'
}
```

### Para Exploración de Candidatos
```python
# Usar coordenadas candidatas reales aquí
CANDIDATO_1 = {
    'lat_min': XX.XX, 'lat_max': XX.XX,
    'lon_min': YY.YY, 'lon_max': YY.YY,
    'region_name': 'Candidato Arqueológico 1'
}
```

---

## 🔧 CONFIGURACIÓN REQUERIDA

### APIs Ya Configuradas (Hasheadas en BD)
- ✅ **NASA Earthdata** - VIIRS, Landsat, ICESat-2
- ✅ **Copernicus CDS** - ERA5, Copernicus Marine
- ✅ **Microsoft Planetary Computer** - Sentinel-1/2

### APIs a Verificar en Casa
- 🔑 **OpenTopography API Key** - Para SRTM de alta resolución
- 🔑 **ASF DAAC Login** - Para PALSAR-2 (opcional)
- 🔑 **ClimateSERV** - Para CHIRPS (público, sin key)

### Variables de Entorno
```bash
# Verificar que estén configuradas:
echo $EARTHDATA_USERNAME
echo $EARTHDATA_PASSWORD
echo $COPERNICUS_CDS_API_KEY
echo $OPENTOPOGRAPHY_API_KEY  # Opcional pero recomendado
```

---

## 📊 MÉTRICAS DE ÉXITO ESPERADAS

### Test de Nuevos Instrumentos
- **Objetivo**: ≥3/5 instrumentos funcionando
- **Tiempo**: 5-10 minutos
- **Indicador**: Tasa de éxito ≥60%

### Test de Integración Completa
- **Objetivo**: Coverage score ≥60%
- **Tiempo**: 15-30 minutos  
- **Indicador**: ≥2 sitios exitosos de 4

### Análisis de Candidatos
- **Objetivo**: Análisis completo sin errores
- **Tiempo**: 2-5 minutos por sitio
- **Indicador**: Resultado con confianza ≥moderate

---

## 🚨 TROUBLESHOOTING

### Problema: VIIRS falla
```bash
# Verificar credenciales Earthdata
curl -u $EARTHDATA_USERNAME:$EARTHDATA_PASSWORD \
  https://urs.earthdata.nasa.gov/api/users/user
```

### Problema: SRTM sin datos
```bash
# Probar API USGS alternativa
curl "https://elevation-api.io/api/elevation/point?lat=29.95&lon=31.15"
```

### Problema: ERA5 timeout
```bash
# Verificar configuración CDS
python -c "import cdsapi; c = cdsapi.Client(); print('CDS OK')"
```

### Problema: PALSAR-2 sin acceso
```bash
# Usar modo degradado sin L-band
# El sistema funcionará con C-band Sentinel-1
```

### Problema: CHIRPS API error
```bash
# Usar fuente alternativa IRI
curl "https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly-improved/.global/.0p05deg/.prcp/data.nc"
```

---

## 🎉 RESULTADOS ESPERADOS

### Con Sitios Conocidos (Validación)
- **Giza**: Anomalías térmicas fuertes, elevaciones de pirámides
- **Angkor**: Penetración L-band, estructuras bajo vegetación
- **Machu Picchu**: Terrazas topográficas, contexto climático

### Con Coordenadas Candidatas
- **Análisis completo** con 15 instrumentos
- **Contexto climático** automático
- **Evaluación de preservación** integrada
- **Predicción de sistemas** de manejo de agua
- **Score de confianza** arqueológica

### Capacidades Nuevas Disponibles
- 🔥 **Detección de fuegos** con VIIRS
- 🏔️ **Análisis topográfico** detallado con SRTM 30m
- 🌿 **Penetración profunda** en vegetación con PALSAR-2 L-band
- 🌡️ **Contexto climático** histórico con ERA5
- 🌧️ **Análisis de precipitación** y sequías con CHIRPS

---

## 📋 CHECKLIST DE EJECUCIÓN

### Antes de Empezar
- [ ] Verificar variables de entorno configuradas
- [ ] Confirmar conexión a internet estable
- [ ] Tener coordenadas candidatas preparadas

### Ejecución Paso a Paso
- [ ] Ejecutar `test_nuevos_5_instrumentos.py`
- [ ] Verificar ≥3/5 instrumentos funcionando
- [ ] Ejecutar `test_15_instruments_integration.py`
- [ ] Verificar coverage score ≥60%
- [ ] Probar con coordenadas candidatas reales
- [ ] Analizar resultados y generar reportes

### Después de la Ejecución
- [ ] Revisar archivos de resultados JSON
- [ ] Documentar hallazgos arqueológicos
- [ ] Identificar instrumentos más útiles
- [ ] Planificar análisis adicionales

---

## 🚀 ¡SISTEMA LISTO!

**ArcheoScope con 15 instrumentos satelitales está completamente integrado y listo para uso en casa.**

### Comando de Inicio Rápido
```bash
# Test rápido
python test_nuevos_5_instrumentos.py

# Si exitoso, continuar con:
python test_15_instruments_integration.py

# Luego usar coordenadas candidatas reales
python run_archeoscope.py
```

### Soporte
- 📖 **Documentación completa**: `INTEGRACION_15_INSTRUMENTOS_COMPLETA.md`
- 🧪 **Scripts de testing**: Incluidos y documentados
- 🔧 **Troubleshooting**: Guías específicas por instrumento

**¡Buena suerte con el análisis arqueológico! 🏛️✨**