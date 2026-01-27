# Plan de Ejecución en Casa - ArcheoScope Candidatos Estratégicos

## 🎯 OBJETIVO

Ejecutar captura de datos de **5 candidatos estratégicos** en casa con acceso completo a credenciales de instrumentos satelitales, guardar en BD PostgreSQL y analizar con asistentes IA.

## 📋 PREPARATIVOS PREVIOS

### 1. Verificar Entorno
```bash
# Verificar que todo esté actualizado
git pull origin main

# Verificar dependencias críticas
python test_critical_fixes_complete.py

# Verificar conexión a BD
python -c "import psycopg2; from dotenv import load_dotenv; import os; load_dotenv(); print('BD OK' if os.getenv('DATABASE_URL') else 'BD NO CONFIG')"
```

### 2. Verificar Credenciales de Instrumentos
```bash
# Verificar que las credenciales estén disponibles
python backend/credentials_manager.py --list

# Debería mostrar:
# ✅ earthdata (ICESat-2, NSIDC)
# ✅ planetary_computer (Sentinel-1/2, Landsat)
# ✅ copernicus_marine (SST, hielo marino)
# ✅ modis_lst (MODIS térmico)
```

## 🌍 CANDIDATOS ESTRATÉGICOS (5 seleccionados)

### 1. 🧊 Groenlandia - Márgenes Glaciares Retraídos
```json
{
  "candidate_id": "groenlandia_glaciar",
  "name": "Groenlandia - Márgenes Glaciares Retraídos",
  "terrain": "polar_ice",
  "coordinates": {"lat_min": 72.58, "lat_max": 72.59, "lon_min": -38.46, "lon_max": -38.45},
  "scientific_value": "ALTÍSIMO",
  "target_features": ["alineamientos lineales", "terrazas costeras antiguas", "estructuras fuera del hielo"],
  "instruments": ["icesat2", "nsidc_sea_ice", "sar_backscatter", "modis_lst"],
  "advantages": ["bajo ruido moderno", "series NSIDC desde 1970s", "excavación puntual viable"]
}
```

### 2. 🌿 Amazonia Occidental - Selva Densa
```json
{
  "candidate_id": "amazonia_occidental", 
  "name": "Amazonia Occidental - Selva Densa",
  "terrain": "forest",
  "coordinates": {"lat_min": -8.12, "lat_max": -8.11, "lon_min": -74.02, "lon_max": -74.01},
  "scientific_value": "ALTO",
  "target_features": ["patrones geométricos persistentes", "caminos elevados", "manejo hidráulico antiguo"],
  "instruments": ["sentinel_2_ndvi", "sar_backscatter", "icesat2", "modis_lst"],
  "advantages": ["excavación digital vs física", "LiDAR fragmentado disponible"]
}
```

### 3. 🏜️ Desierto de Arabia - Rub' al Khali
```json
{
  "candidate_id": "desierto_arabia",
  "name": "Desierto de Arabia - Rub' al Khali", 
  "terrain": "desert",
  "coordinates": {"lat_min": 21.50, "lat_max": 21.51, "lon_min": 51.00, "lon_max": 51.01},
  "scientific_value": "ALTO",
  "target_features": ["paleocauces", "asentamientos efímeros", "nodos logísticos antiguos"],
  "instruments": ["landsat_thermal", "sentinel_2_ndvi", "sar_backscatter", "icesat2"],
  "advantages": ["SAR + térmico + humedad histórica", "infraestructura moderna mínima"]
}
```

### 4. 🏔️ Patagonia Austral - Estepas + Glaciares
```json
{
  "candidate_id": "patagonia_austral",
  "name": "Patagonia Austral - Estepas + Glaciares",
  "terrain": "mountain_steppe", 
  "coordinates": {"lat_min": -50.20, "lat_max": -50.19, "lon_min": -72.30, "lon_max": -72.29},
  "scientific_value": "ALTO",
  "target_features": ["sitios ocupación temprana", "estructuras de abrigo", "patrones de movilidad"],
  "instruments": ["icesat2", "sentinel_2_ndvi", "sar_backscatter", "modis_lst"],
  "advantages": ["ventaja local + técnica", "acceso campo difícil → ventaja digital"]
}
```

### 5. 🌊 Plataforma Continental - Mar del Norte
```json
{
  "candidate_id": "plataforma_continental",
  "name": "Plataforma Continental - Mar del Norte",
  "terrain": "shallow_marine",
  "coordinates": {"lat_min": 55.68, "lat_max": 55.69, "lon_min": 2.58, "lon_max": 2.59},
  "scientific_value": "MEDIO-ALTO", 
  "target_features": ["paleopaisajes", "rutas humanas", "asentamientos costeros sumergidos"],
  "instruments": ["sar_backscatter", "modis_lst", "copernicus_sst", "sentinel_2_ndvi"],
  "advantages": ["excavación física carísima", "sistema brilla como filtro"]
}
```

## 🚀 SECUENCIA DE EJECUCIÓN

### PASO 1: Preparación del Entorno (5 min)
```bash
# 1. Activar entorno y verificar dependencias
cd /path/to/ArcheoScope
source venv/bin/activate  # o el entorno que uses

# 2. Verificar que el integrador V2 esté disponible
python -c "from backend.satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2; print('✅ Integrador V2 OK')"

# 3. Verificar conexión a BD
python -c "import psycopg2; from dotenv import load_dotenv; import os; load_dotenv(); conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('✅ BD PostgreSQL OK'); conn.close()"
```

### PASO 2: Ejecutar Captura de Candidatos Estratégicos (15-20 min)
```bash
# Ejecutar el test de 5 candidatos estratégicos
python test_5_candidatos_estrategicos.py

# Esto generará:
# - candidatos_estrategicos_mediciones_YYYYMMDD_HHMMSS.json
# - test_5_candidatos_YYYYMMDD_HHMMSS.log
# - Datos en BD PostgreSQL (tablas: analysis_candidates, raw_measurements)
```

### PASO 3: Verificar Captura de Datos (2 min)
```bash
# Verificar que los datos se guardaron en BD
python -c "
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM raw_measurements WHERE analysis_version = \'v2.1\'')
count = cur.fetchone()[0]
print(f'✅ Mediciones capturadas: {count}')
cur.execute('SELECT COUNT(*) FROM analysis_candidates WHERE analysis_status = \'COMPLETED\'')
candidates = cur.fetchone()[0] 
print(f'✅ Candidatos completados: {candidates}')
conn.close()
"
```

### PASO 4: Análisis Científico con IA (10-15 min)
```bash
# Ejecutar análisis científico sobre datos capturados
python analyze_scientific_dataset.py

# Esto generará:
# - analysis_results_YYYYMMDD_HHMMSS/
#   ├── normalized_measurements.csv
#   ├── archaeological_ranking.csv
#   ├── terrain_summary.csv
#   ├── outliers.csv
#   ├── correlations/
#   └── analysis_report.json
```

## 📊 ESTRUCTURA DE DATOS ESPERADA

### Formato de Medición Individual
```json
{
  "candidate_id": "groenlandia_glaciar",
  "candidate_name": "Groenlandia - Márgenes Glaciares Retraídos",
  "terrain": "polar_ice",
  "country": "Greenland",
  "coordinates": {
    "lat_min": 72.58, "lat_max": 72.59,
    "lon_min": -38.46, "lon_max": -38.45
  },
  "instrument": "ICESat-2",
  "measurement_type": "elevation",
  "value": 1234.56,
  "unit": "m",
  "confidence": 0.85,
  "status": "SUCCESS",
  "source": "ICESat-2 (NASA)",
  "measured_at": "2026-01-27T15:30:00Z",
  "analysis_version": "v2.1",
  "reason": null,
  "processing_time_seconds": 45.2,
  "raw_response": { /* respuesta completa de la API */ }
}
```

### Estados Posibles por Instrumento
- **SUCCESS**: Datos válidos obtenidos
- **DEGRADED**: Datos parciales o baja calidad  
- **FAILED**: No se pudieron obtener datos
- **UNAVAILABLE**: API/servicio no disponible
- **INVALID**: Datos inválidos (inf/nan)
- **TIMEOUT**: Timeout en la consulta
- **NO_DATA**: Sin datos para la región/fecha

## 🔍 DIAGNÓSTICO DE FALLOS ESPERADOS

### Fallos Comunes y Soluciones

#### 1. ICESat-2 - "INSUFFICIENT_VALID_POINTS"
```bash
# Causa: Región sin cobertura ICESat-2 o pocos puntos
# Solución: Normal para algunas regiones, usar otros instrumentos
# Estado: DEGRADED o NO_DATA (no es error crítico)
```

#### 2. Sentinel-1 SAR - "COG_TILE_READ_ERROR" 
```bash
# Causa: Descarga de COG grande (200-400 MB)
# Solución: Usar cache, aumentar timeout
# Estado: TIMEOUT → retry automático
```

#### 3. NSIDC - "AUTHENTICATION_FAILED"
```bash
# Causa: Credenciales Earthdata
# Solución: Verificar backend/credentials_manager.py
python backend/credentials_manager.py --test earthdata
```

#### 4. Copernicus Marine - "SERVICE_UNAVAILABLE"
```bash
# Causa: Servicio temporalmente no disponible
# Solución: Retry automático, estado UNAVAILABLE
```

## 📈 MÉTRICAS DE ÉXITO ESPERADAS

### Objetivos Mínimos
- **Candidatos exitosos**: ≥ 4/5 (80%)
- **Coverage score promedio**: ≥ 40%
- **Mediciones totales**: ≥ 15 (3 por candidato promedio)
- **Instrumentos funcionando**: ≥ 60%

### Objetivos Ideales  
- **Candidatos exitosos**: 5/5 (100%)
- **Coverage score promedio**: ≥ 60%
- **Mediciones totales**: ≥ 20 (4 por candidato promedio)
- **Instrumentos funcionando**: ≥ 80%

## 🧠 ANÁLISIS CON ASISTENTES IA

### Prompts Sugeridos para IA

#### 1. Análisis de Patrones por Terreno
```
"Analiza las mediciones de ArcheoScope por terreno. 
Datos: [cargar CSV normalized_measurements.csv]
Pregunta: ¿Qué patrones instrumentales son únicos por terreno? 
¿Qué correlaciones inesperadas encuentras?"
```

#### 2. Ranking Arqueológico
```
"Revisa el ranking arqueológico generado.
Datos: [cargar CSV archaeological_ranking.csv]  
Pregunta: ¿Los candidatos con mayor anomaly_score tienen sentido arqueológico?
¿Qué candidatos merecen investigación prioritaria?"
```

#### 3. Fallos de Instrumentos
```
"Analiza los fallos de instrumentos por región.
Datos: [instrument_failures del JSON]
Pregunta: ¿Hay patrones geográficos en los fallos?
¿Qué instrumentos son más confiables por terreno?"
```

#### 4. Correlaciones Cruzadas
```
"Examina las correlaciones entre instrumentos.
Datos: [archivos correlations/*.csv]
Pregunta: ¿Qué combinaciones de instrumentos son más predictivas?
¿Hay redundancias que podemos eliminar?"
```

## 🔄 FLUJO POST-ANÁLISIS

### 1. Refinamiento de Algoritmos
```python
# Basado en patrones reales encontrados:
# - Ajustar pesos por terreno
# - Refinar umbrales de anomalía  
# - Optimizar selección de instrumentos
# - Mejorar filtros de calidad
```

### 2. Validación Cruzada
```python
# Correlacionar con BD arqueológica existente:
# - ¿Los top candidatos coinciden con sitios conocidos?
# - ¿Hay falsos positivos sistemáticos?
# - ¿Qué terrenos son más predictivos?
```

### 3. Preparación de Paper Científico
```markdown
# Estructura sugerida:
## Abstract: ArcheoScope como sistema reproducible
## Methods: Integración multi-instrumental robusta  
## Results: Análisis de 5 candidatos estratégicos
## Discussion: Patrones por terreno, limitaciones
## Conclusion: Escalabilidad del sistema
```

## 📁 ARCHIVOS DE SALIDA ESPERADOS

```
/ArcheoScope/
├── candidatos_estrategicos_mediciones_20260127_HHMMSS.json  # Datos crudos
├── test_5_candidatos_20260127_HHMMSS.log                   # Log detallado
├── analysis_results_20260127_HHMMSS/                       # Análisis científico
│   ├── normalized_measurements.csv                         # Datos normalizados
│   ├── archaeological_ranking.csv                          # Ranking final
│   ├── terrain_summary.csv                                 # Resumen por terreno
│   ├── outliers.csv                                        # Outliers detectados
│   ├── correlations/                                       # Correlaciones por terreno
│   │   ├── polar_ice_correlations.csv
│   │   ├── forest_correlations.csv
│   │   ├── desert_correlations.csv
│   │   ├── mountain_steppe_correlations.csv
│   │   └── shallow_marine_correlations.csv
│   └── analysis_report.json                                # Reporte completo
└── PostgreSQL Database                                      # Datos persistentes
    ├── analysis_candidates (5 registros)
    └── raw_measurements (~20 registros)
```

## ⏱️ CRONOGRAMA ESTIMADO

| Fase | Tiempo | Actividad |
|------|--------|-----------|
| **Preparación** | 5 min | Verificar entorno, credenciales, BD |
| **Captura** | 15-20 min | Ejecutar test_5_candidatos_estrategicos.py |
| **Verificación** | 2 min | Confirmar datos en BD |
| **Análisis** | 10-15 min | Ejecutar analyze_scientific_dataset.py |
| **Revisión IA** | 30-60 min | Análisis con asistentes, insights |
| **Total** | **60-90 min** | **Sesión completa** |

## 🎯 CRITERIOS DE ÉXITO

### ✅ Éxito Completo
- 5/5 candidatos procesados exitosamente
- Coverage score promedio > 60%
- Todos los terrenos representados
- Patrones claros por terreno identificados
- Ranking arqueológico coherente

### ✅ Éxito Parcial  
- 4/5 candidatos procesados exitosamente
- Coverage score promedio > 40%
- Mayoría de terrenos representados
- Algunos patrones identificados

### ⚠️ Requiere Revisión
- < 4/5 candidatos exitosos
- Coverage score promedio < 40%
- Fallos sistemáticos de instrumentos
- Patrones no claros

## 🚀 COMANDOS DE EJECUCIÓN RÁPIDA

```bash
# Secuencia completa en una sola sesión
cd /path/to/ArcheoScope

# 1. Verificación rápida
python -c "from backend.satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2; print('✅ OK')"

# 2. Captura de datos (15-20 min)
python test_5_candidatos_estrategicos.py

# 3. Análisis científico (10-15 min)  
python analyze_scientific_dataset.py

# 4. Verificar resultados
ls -la candidatos_estrategicos_mediciones_*.json
ls -la analysis_results_*/
```

---

## 🎉 RESULTADO ESPERADO

Al final de esta sesión tendrás:

1. **Dataset Científico Robusto**: 5 candidatos estratégicos con datos reales
2. **Base de Datos Poblada**: PostgreSQL con mediciones versionadas  
3. **Análisis Reproducible**: Correlaciones, ranking, outliers
4. **Insights Arqueológicos**: Patrones por terreno, candidatos prioritarios
5. **Sistema Validado**: ArcheoScope funcionando como sistema científico

**¡ArcheoScope estará oficialmente transformado en un sistema científico reproducible de clase mundial!** 🏆