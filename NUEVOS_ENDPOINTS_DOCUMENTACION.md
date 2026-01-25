# Nuevos Endpoints de ArcheoScope

**Fecha**: 2026-01-25
**Versión**: 1.1.0

## Resumen

Se agregaron dos nuevos endpoints REST API para acceder a la información de sitios arqueológicos:

1. **GET /archaeological-sites/known** - Sitios arqueológicos conocidos oficialmente
2. **GET /archaeological-sites/candidates** - Sitios candidatos detectados por ArcheoScope

---

## 1. Endpoint: Sitios Arqueológicos Conocidos

### GET /archaeological-sites/known

Retorna la base de datos completa de sitios arqueológicos oficialmente documentados y verificados.

#### URL
```
GET http://localhost:8002/archaeological-sites/known
```

#### Respuesta Exitosa (200 OK)

```json
{
  "metadata": {
    "version": "2.0.0",
    "last_updated": "2026-01-24",
    "total_sites": 8,
    "description": "Reference archaeological sites for ArcheoScope calibration",
    "sources": [
      "UNESCO World Heritage Centre (whc.unesco.org)",
      "South Tyrol Museum of Archaeology (iceman.it)",
      "Woods Hole Oceanographic Institution (whoi.edu)",
      "Scientific publications (peer-reviewed)"
    ]
  },
  "reference_sites": {
    "giza_pyramids": {
      "name": "Giza Pyramids Complex",
      "environment_type": "desert",
      "coordinates": {"lat": 29.9792, "lon": 31.1342},
      "country": "Egypt",
      "site_type": "monumental_complex",
      "period": "Old Kingdom Egypt",
      "date_range": {"start": -2580, "end": -2560, "unit": "BCE"},
      "area_km2": 2.5,
      "unesco_id": 86,
      "confidence_level": "confirmed",
      "data_available": {
        "lidar": true,
        "satellite_multispectral": true,
        "satellite_thermal": true,
        "sar": true
      }
    },
    "angkor_wat": { ... },
    "otzi_iceman": { ... },
    "port_royal": { ... }
  },
  "control_sites": {
    "atacama_desert_control": { ... },
    "amazon_rainforest_control": { ... },
    "greenland_ice_control": { ... },
    "pacific_ocean_control": { ... }
  },
  "total_sites": 8,
  "sources": [...],
  "last_updated": "2026-01-24",
  "data_quality": "All sites verified against multiple authoritative sources"
}
```

#### Campos Principales

- **metadata**: Información sobre la base de datos
  - `version`: Versión de la BD
  - `total_sites`: Número total de sitios
  - `sources`: Fuentes de datos oficiales
  - `last_updated`: Fecha de última actualización

- **reference_sites**: Sitios arqueológicos confirmados (4 sitios)
  - Giza Pyramids (desert)
  - Angkor Wat (forest)
  - Ötzi the Iceman (glacier)
  - Port Royal (shallow_sea)

- **control_sites**: Sitios de control sin arqueología (4 sitios)
  - Atacama Desert (desert control)
  - Amazon Rainforest (forest control)
  - Greenland Ice Sheet (ice control)
  - Pacific Ocean (water control)

#### Ejemplo de Uso

**cURL:**
```bash
curl http://localhost:8002/archaeological-sites/known
```

**Python:**
```python
import requests

response = requests.get("http://localhost:8002/archaeological-sites/known")
data = response.json()

print(f"Total sitios: {data['total_sites']}")
for site_id, site_data in data['reference_sites'].items():
    print(f"- {site_data['name']} ({site_data['environment_type']})")
```

**JavaScript:**
```javascript
fetch('http://localhost:8002/archaeological-sites/known')
  .then(response => response.json())
  .then(data => {
    console.log(`Total sitios: ${data.total_sites}`);
    Object.values(data.reference_sites).forEach(site => {
      console.log(`- ${site.name} (${site.environment_type})`);
    });
  });
```

---

## 2. Endpoint: Sitios Candidatos de ArcheoScope

### GET /archaeological-sites/candidates

Retorna sitios candidatos detectados por ArcheoScope que requieren validación arqueológica.

#### URL
```
GET http://localhost:8002/archaeological-sites/candidates
```

#### Criterios de Selección

Un sitio es considerado "candidato" si cumple:
1. ✅ Probabilidad arqueológica > 0.5
2. ✅ Convergencia instrumental (mínimo 2 instrumentos)
3. ✅ NO está en la base de datos de sitios conocidos
4. ✅ Requiere validación en terreno

#### Respuesta Exitosa (200 OK)

```json
{
  "candidates": [
    {
      "region_name": "Anomalía Amazónica Norte",
      "coordinates": {
        "lat_range": [-3.5, -3.4],
        "lon_range": [-62.3, -62.2]
      },
      "environment_type": "forest",
      "archaeological_probability": 0.78,
      "confidence_level": "high",
      "instruments_converging": 3,
      "detection_date": "2026-01-25T10:30:00",
      "measurements": [
        {
          "instrument": "lidar_elevation_anomalies",
          "value": 5.2,
          "threshold": 2.0,
          "exceeds_threshold": true,
          "confidence": "high"
        },
        {
          "instrument": "ndvi_canopy_gaps",
          "value": 0.35,
          "threshold": 0.25,
          "exceeds_threshold": true,
          "confidence": "moderate"
        }
      ],
      "explanation": "Análisis en ambiente forest. 3 de 3 instrumentos detectaron anomalías...",
      "recommended_validation": [
        "LiDAR aerotransportado crítico para confirmar",
        "Validación en terreno con arqueólogos profesionales"
      ],
      "false_positive_risks": [
        "Termiteros, formaciones naturales",
        "Claros naturales, agricultura"
      ]
    }
  ],
  "total_candidates": 1,
  "detection_criteria": {
    "minimum_probability": 0.5,
    "requires_convergence": true,
    "excludes_known_sites": true,
    "description": "Sitios con múltiples instrumentos convergentes y alta probabilidad arqueológica"
  },
  "recommended_validation": [
    "Validación en terreno con arqueólogos profesionales",
    "Análisis LIDAR de alta resolución si disponible",
    "Excavación exploratoria en áreas de alta probabilidad",
    "Consulta con autoridades arqueológicas locales",
    "Documentación fotográfica y topográfica detallada"
  ],
  "disclaimer": "Estos son candidatos potenciales basados en análisis remoto. Se requiere validación profesional antes de cualquier excavación.",
  "last_updated": "2026-01-25T11:00:00"
}
```

#### Campos Principales

- **candidates**: Array de sitios candidatos ordenados por probabilidad
  - `region_name`: Nombre de la región analizada
  - `coordinates`: Coordenadas del área
  - `environment_type`: Tipo de ambiente (desert, forest, glacier, etc.)
  - `archaeological_probability`: Probabilidad arqueológica (0.0-1.0)
  - `confidence_level`: Nivel de confianza (high, moderate, low)
  - `instruments_converging`: Número de instrumentos que detectaron anomalías
  - `measurements`: Mediciones instrumentales detalladas
  - `recommended_validation`: Métodos recomendados para validar
  - `false_positive_risks`: Riesgos de falsos positivos identificados

- **total_candidates**: Número total de candidatos detectados

- **detection_criteria**: Criterios usados para clasificar como candidato

- **disclaimer**: Aviso importante sobre validación profesional

#### Ejemplo de Uso

**cURL:**
```bash
curl http://localhost:8002/archaeological-sites/candidates
```

**Python:**
```python
import requests

response = requests.get("http://localhost:8002/archaeological-sites/candidates")
data = response.json()

print(f"Total candidatos: {data['total_candidates']}")

for candidate in data['candidates']:
    print(f"\n🎯 {candidate['region_name']}")
    print(f"   Probabilidad: {candidate['archaeological_probability']:.2%}")
    print(f"   Ambiente: {candidate['environment_type']}")
    print(f"   Instrumentos: {candidate['instruments_converging']}")
```

**JavaScript:**
```javascript
fetch('http://localhost:8002/archaeological-sites/candidates')
  .then(response => response.json())
  .then(data => {
    console.log(`Total candidatos: ${data.total_candidates}`);
    
    data.candidates.forEach(candidate => {
      console.log(`\n🎯 ${candidate.region_name}`);
      console.log(`   Probabilidad: ${(candidate.archaeological_probability * 100).toFixed(1)}%`);
      console.log(`   Ambiente: ${candidate.environment_type}`);
    });
  });
```

---

## Notas Importantes

### Fuente de Datos

- **Sitios Conocidos**: `data/archaeological_sites_database.json`
- **Candidatos**: `archeoscope_permanent_history.json` (generado por análisis)

### Generación de Candidatos

Los candidatos se generan automáticamente cuando se ejecuta el endpoint `/analyze`. Para generar candidatos:

1. Ejecutar análisis en una región: `POST /analyze`
2. El sistema detecta anomalías con convergencia instrumental
3. Si prob > 0.5 y no es sitio conocido → se guarda como candidato
4. Consultar candidatos: `GET /archaeological-sites/candidates`

### Validación Científica

⚠️ **IMPORTANTE**: Los candidatos son detecciones basadas en análisis remoto. Se requiere:
- Validación por arqueólogos profesionales
- Permisos de autoridades locales
- Excavación exploratoria controlada
- Documentación científica rigurosa

### Integración con Frontend

Estos endpoints están diseñados para ser consumidos por el frontend de ArcheoScope:

```javascript
// Cargar sitios conocidos al iniciar
async function loadKnownSites() {
  const response = await fetch('/archaeological-sites/known');
  const data = await response.json();
  displayKnownSitesOnMap(data.reference_sites);
}

// Cargar candidatos para mostrar en panel
async function loadCandidates() {
  const response = await fetch('/archaeological-sites/candidates');
  const data = await response.json();
  displayCandidatesPanel(data.candidates);
}
```

---

## Changelog

### v1.1.0 (2026-01-25)

**Agregado:**
- ✅ Endpoint GET /archaeological-sites/known
- ✅ Endpoint GET /archaeological-sites/candidates
- ✅ Documentación completa de endpoints
- ✅ Ejemplos de uso en múltiples lenguajes

**Configuración:**
- ✅ Configurado para usar OLLAMA_MODEL1 desde .env.local
- ✅ Soporte para modelos alternativos (OLLAMA_MODEL2)

---

## Testing

Para probar los endpoints:

```bash
# Test sitios conocidos
curl http://localhost:8002/archaeological-sites/known | jq '.total_sites'

# Test candidatos
curl http://localhost:8002/archaeological-sites/candidates | jq '.total_candidates'

# Test completo
python test_new_endpoints.py
```

---

## Soporte

Para reportar problemas o sugerencias:
- Revisar logs del backend
- Verificar que la BD existe en `data/archaeological_sites_database.json`
- Verificar que el historial existe en `archeoscope_permanent_history.json`
