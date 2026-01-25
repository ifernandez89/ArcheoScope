# 🚀 Swagger UI - Guía Rápida

## Acceso a la Documentación Interactiva

### 1. Iniciar el Backend
```bash
python run_archeoscope.py
```

El backend se iniciará en: `http://localhost:8002`

### 2. Abrir Swagger UI

**Opción 1: Swagger UI (Interactivo)**
```
http://localhost:8002/docs
```
- Interfaz interactiva completa
- Prueba endpoints directamente desde el navegador
- Formularios automáticos para parámetros
- Respuestas en tiempo real

**Opción 2: ReDoc (Documentación)**
```
http://localhost:8002/redoc
```
- Documentación estática elegante
- Mejor para lectura y referencia
- Navegación por secciones

**Opción 3: OpenAPI JSON**
```
http://localhost:8002/openapi.json
```
- Schema JSON completo
- Para integración con herramientas
- Generación de clientes automática

---

## 🎯 Endpoints Principales para Probar

### 1. Verificar Estado del Sistema
**Endpoint:** `GET /status`

En Swagger UI:
1. Expandir sección "Status"
2. Click en `GET /status`
3. Click en "Try it out"
4. Click en "Execute"

**Respuesta esperada:**
```json
{
  "backend_status": "operational",
  "ai_status": "available",
  "available_rules": [...],
  "supported_regions": ["global"]
}
```

---

### 2. Ver Sitios Arqueológicos Conocidos
**Endpoint:** `GET /archaeological-sites/known`

En Swagger UI:
1. Expandir sección "Database"
2. Click en `GET /archaeological-sites/known`
3. Click en "Try it out"
4. Click en "Execute"

**Respuesta esperada:**
```json
{
  "metadata": {
    "version": "2.1.0",
    "total_sites": 8,
    "environment_coverage": {...}
  },
  "reference_sites": {
    "giza_pyramids": {...},
    "angkor_wat": {...},
    "machu_picchu": {...},
    "petra": {...},
    "stonehenge": {...},
    ...
  },
  "control_sites": {...},
  "total_sites": 12
}
```

**Sitios incluidos:**
- ✅ Giza Pyramids (Egypt) - desert
- ✅ Angkor Wat (Cambodia) - forest
- ✅ Ötzi the Iceman (Alps) - glacier
- ✅ Port Royal (Jamaica) - shallow_sea
- ✅ Machu Picchu (Peru) - mountain
- ✅ Petra (Jordan) - desert
- ✅ Stonehenge (UK) - grassland
- ✅ 4 sitios de control (negativos)

---

### 3. Analizar una Región (Ejemplo: Giza)
**Endpoint:** `POST /analyze`

En Swagger UI:
1. Expandir sección "Analysis"
2. Click en `POST /analyze`
3. Click en "Try it out"
4. Modificar el JSON de ejemplo:

```json
{
  "lat_min": 29.97,
  "lat_max": 29.99,
  "lon_min": 31.12,
  "lon_max": 31.14,
  "region_name": "Giza Pyramids Test",
  "resolution_m": 1000
}
```

5. Click en "Execute"

**Respuesta esperada:**
```json
{
  "analysis_id": "...",
  "region_name": "Giza Pyramids Test",
  "environment_classification": {
    "environment_type": "desert",
    "confidence": 0.95
  },
  "archaeological_results": {
    "result_type": "archaeological",
    "archaeological_probability": 0.80,
    "confidence": "moderate",
    "site_recognized": true,
    "known_site_name": "Giza Pyramids Complex"
  },
  "instrumental_measurements": [
    {
      "instrument": "thermal_anomalies",
      "value": 8.39,
      "unit": "K",
      "threshold": 4.50,
      "exceeds_threshold": true,
      "confidence": "high"
    },
    ...
  ],
  "convergence_analysis": {
    "instruments_converging": 2,
    "minimum_required": 2,
    "convergence_met": true
  },
  "ai_explanations": {
    "ai_available": true,
    "explanation": "...",
    "confidence": 0.85
  }
}
```

---

### 4. Ver Sitios Candidatos Detectados
**Endpoint:** `GET /archaeological-sites/candidates`

En Swagger UI:
1. Expandir sección "Database"
2. Click en `GET /archaeological-sites/candidates`
3. Click en "Try it out"
4. Click en "Execute"

**Respuesta esperada:**
```json
{
  "candidates": [
    {
      "region_name": "...",
      "coordinates": {...},
      "environment_type": "...",
      "archaeological_probability": 0.65,
      "confidence_level": "moderate",
      "instruments_converging": 2,
      "detection_date": "2026-01-25T...",
      "explanation": "...",
      "recommended_validation": [...]
    }
  ],
  "total_candidates": 0,
  "detection_criteria": {...}
}
```

---

## 🧪 Ejemplos de Prueba

### Ejemplo 1: Analizar Angkor Wat
```json
{
  "lat_min": 13.40,
  "lat_max": 13.42,
  "lon_min": 103.86,
  "lon_max": 103.88,
  "region_name": "Angkor Wat Test",
  "resolution_m": 1000
}
```

**Ambiente esperado:** `forest`  
**Instrumentos:** LiDAR, NDVI, SAR L-band

---

### Ejemplo 2: Analizar Machu Picchu
```json
{
  "lat_min": -13.17,
  "lat_max": -13.15,
  "lon_min": -72.55,
  "lon_max": -72.53,
  "region_name": "Machu Picchu Test",
  "resolution_m": 1000
}
```

**Ambiente esperado:** `mountain`  
**Instrumentos:** Elevation terracing, Slope anomalies, SAR structural

---

### Ejemplo 3: Analizar Port Royal (Submarino)
```json
{
  "lat_min": 17.93,
  "lat_max": 17.95,
  "lon_min": -76.85,
  "lon_max": -76.83,
  "region_name": "Port Royal Test",
  "resolution_m": 1000
}
```

**Ambiente esperado:** `shallow_sea`  
**Instrumentos:** Multibeam sonar, Magnetometer, Bathymetry

---

### Ejemplo 4: Analizar Área Desconocida
```json
{
  "lat_min": 40.0,
  "lat_max": 40.02,
  "lon_min": -3.7,
  "lon_max": -3.68,
  "region_name": "Madrid Test",
  "resolution_m": 1000
}
```

**Ambiente esperado:** `agricultural` o `unknown`  
**Resultado esperado:** Baja probabilidad arqueológica

---

## 📊 Interpretación de Resultados

### Probabilidad Arqueológica
- **> 70%**: Alta probabilidad - Sitio arqueológico muy probable
- **50-70%**: Probabilidad moderada - Requiere validación adicional
- **30-50%**: Baja probabilidad - Posible falso positivo
- **< 30%**: Muy baja - Probablemente natural

### Nivel de Confianza
- **high**: 2+ instrumentos con señal fuerte (>180% umbral)
- **moderate**: 2+ instrumentos exceden umbral
- **low**: 1-2 instrumentos con señal débil
- **none**: No hay convergencia instrumental

### Convergencia Instrumental
- **2/2 o más**: Convergencia alcanzada ✅
- **1/2**: Convergencia parcial ⚠️
- **0/2**: Sin convergencia ❌

---

## 🔍 Ambientes Soportados

| Ambiente | Instrumentos Principales | Ejemplo |
|----------|-------------------------|---------|
| `desert` | Thermal, SAR, NDVI | Giza, Petra |
| `forest` | LiDAR, NDVI, SAR L-band | Angkor Wat |
| `glacier` | ICESat-2, SAR polarimetric | Ötzi |
| `shallow_sea` | Sonar, Magnetometer | Port Royal |
| `mountain` | Elevation, Slope, SAR | Machu Picchu |
| `grassland` | Generic anomalies | Stonehenge |
| `polar_ice` | ICESat-2, SAR | Antártida |
| `unknown` | Generic sensors | Áreas no clasificadas |

---

## 💡 Tips para Usar Swagger UI

### 1. Autenticación
- No se requiere autenticación para endpoints públicos
- Todos los endpoints son accesibles sin API key

### 2. Formato de Coordenadas
- Usar grados decimales (no grados/minutos/segundos)
- Latitud: -90 a 90 (negativo = sur)
- Longitud: -180 a 180 (negativo = oeste)

### 3. Tamaño de Región
- Mínimo: 0.01° x 0.01° (~1km x 1km)
- Recomendado: 0.02° x 0.02° (~2km x 2km)
- Máximo: 0.5° x 0.5° (~50km x 50km)

### 4. Tiempo de Respuesta
- Análisis simple: 5-10 segundos
- Análisis con IA: 20-30 segundos
- Análisis complejo: 30-60 segundos

### 5. Errores Comunes
- **503 Service Unavailable**: Backend no está corriendo
- **400 Bad Request**: Coordenadas inválidas
- **500 Internal Server Error**: Error en análisis (revisar logs)

---

## 🎓 Recursos Adicionales

### Documentación Completa
- `SESION_2026-01-25_CALIBRACION_Y_SWAGGER.md` - Análisis técnico completo
- `REPORTE_FINAL_TEST_5_SITIOS.md` - Resultados de calibración
- `PARAMETROS_IA_ANALISIS.md` - Configuración de IA

### Archivos de Configuración
- `data/anomaly_signatures_by_environment.json` - Umbrales por ambiente
- `data/archaeological_sites_database.json` - Base de datos de sitios
- `.env.local` - Configuración de API keys (crear si no existe)

### Tests Disponibles
```bash
# Test de 5 sitios arqueológicos
python test_5_archaeological_sites.py

# Test de calibración
python test_calibration_4_reference_sites.py

# Test rápido
python quick_test.py
```

---

## 🚨 Solución de Problemas

### Backend no inicia
```bash
# Verificar dependencias
pip install -r backend/requirements.txt

# Verificar puerto
netstat -ano | findstr :8002

# Reiniciar backend
python run_archeoscope.py
```

### Swagger UI no carga
1. Verificar que el backend está corriendo
2. Abrir http://localhost:8002/docs en navegador
3. Revisar consola del navegador (F12) para errores
4. Verificar CORS en backend/api/main.py

### IA no disponible
1. Verificar que Ollama está corriendo: `curl http://localhost:11434/api/tags`
2. Verificar modelo instalado: `ollama list`
3. Revisar configuración en `.env.local`
4. El sistema funciona sin IA (explicaciones limitadas)

---

## 📞 Soporte

Para reportar problemas o sugerencias:
1. Revisar logs del backend
2. Verificar configuración en `.env.local`
3. Consultar documentación en `/docs`
4. Crear issue en GitHub

---

**Última actualización:** 2026-01-25  
**Versión API:** 1.1.0  
**Estado:** Operacional ✅
