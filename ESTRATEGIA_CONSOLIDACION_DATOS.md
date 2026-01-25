# Estrategia de Consolidación de Datos Arqueológicos

## 🎯 Objetivo

Crear una base de datos arqueológica consolidada y enriquecida usando múltiples fuentes públicas con validación cruzada.

## 📊 Estado Actual

**Base de datos PostgreSQL:**
- **80,457 sitios arqueológicos** migrados
- Fuentes: OpenStreetMap (69,531) + Wikidata (7,844)
- Deduplicación por grid (~1km)
- Confianza asignada por fuente

## 🏗️ Estrategia de Consolidación (Recomendada)

### 1. OpenStreetMap como Base Principal ✅

**Ventajas:**
- Cobertura global masiva (69,531 sitios)
- Datos geoespaciales precisos
- Actualización continua por comunidad
- API Overpass robusta y gratuita

**Implementación:**
```python
# Ya implementado en scripts/harvest_complete.py
# Extracción por Overpass API con tags arqueológicos
```

**Campos obtenidos:**
- Coordenadas precisas (lat/lon)
- Nombre del sitio
- Tipo de sitio (archaeological_site, ruins, etc.)
- País/región
- Tags adicionales (period, culture, etc.)

### 2. Enriquecimiento con Wikidata 🔄

**Ventajas:**
- Datos estructurados y enlazados
- Referencias académicas
- Imágenes y multimedia
- Conexión con Wikipedia
- IDs únicos para cross-reference

**Implementación:**
```bash
# Nuevo script de enriquecimiento
python scripts/enrich_archaeological_data.py
```

**Campos agregados:**
- `period_detailed`: Período arqueológico detallado
- `culture`: Cultura asociada
- `date_established`: Fecha de establecimiento
- `image_url`: URL de imagen representativa
- `heritage_designation`: Designación patrimonial
- `wikipedia_url`: Artículo de Wikipedia
- `wikidata_enriched`: Flag de enriquecimiento

**Query SPARQL ejemplo:**
```sparql
SELECT ?item ?period ?culture ?inception ?image ?heritage
WHERE {
  VALUES ?item { wd:Q146861 }  # Wikidata ID del sitio
  OPTIONAL { ?item wdt:P2348 ?period. }      # Período
  OPTIONAL { ?item wdt:P2596 ?culture. }     # Cultura
  OPTIONAL { ?item wdt:P571 ?inception. }    # Fecha
  OPTIONAL { ?item wdt:P18 ?image. }         # Imagen
  OPTIONAL { ?item wdt:P1435 ?heritage. }    # Patrimonio
}
```

### 3. Validación con UNESCO 🏛️

**Ventajas:**
- Máxima autoridad en patrimonio mundial
- Datos verificados por expertos
- Criterios de valor universal excepcional
- Referencias oficiales

**Implementación:**
```python
# Validación contra lista UNESCO
# Campos agregados:
- unesco_status: inscribed | tentative | not_listed
- unesco_year: Año de inscripción
- unesco_criteria: Criterios UNESCO (i-x)
- unesco_ref: Número de referencia oficial
```

**Fuentes UNESCO:**
- World Heritage List API
- Tentative Lists
- Documentos de nominación

### 4. Registros Nacionales (Opcional) 🌍

**Por país/región:**
- **USA**: National Register of Historic Places
- **UK**: Historic England
- **France**: Base Mérimée
- **Italy**: Ministero della Cultura
- **Spain**: Patrimonio Histórico Español
- **Mexico**: INAH
- **Peru**: Ministerio de Cultura

## 🔄 Flujo de Trabajo Completo

```
┌─────────────────────────────────────────────────────────┐
│ 1. EXTRACCIÓN BASE (OSM)                                │
│    ├─ Overpass API                                      │
│    ├─ Tags arqueológicos                                │
│    └─ 69,531 sitios                                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. ENRIQUECIMIENTO (Wikidata)                           │
│    ├─ Buscar por coordenadas + nombre                   │
│    ├─ Obtener Wikidata ID                               │
│    ├─ Query SPARQL para detalles                        │
│    └─ Agregar: período, cultura, imágenes, refs         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 3. VALIDACIÓN (UNESCO)                                  │
│    ├─ Verificar contra World Heritage List              │
│    ├─ Marcar sitios UNESCO                              │
│    └─ Agregar: status, año, criterios                   │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 4. VALIDACIÓN NACIONAL (Opcional)                       │
│    ├─ APIs de registros nacionales                      │
│    ├─ Cross-reference por coordenadas                   │
│    └─ Agregar: designación nacional, protección         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 5. CONSOLIDACIÓN FINAL                                  │
│    ├─ Deduplicación avanzada                            │
│    ├─ Resolución de conflictos                          │
│    ├─ Asignación de confianza                           │
│    └─ Migración a PostgreSQL                            │
└─────────────────────────────────────────────────────────┘
```

## 📋 Esquema de Base de Datos Enriquecida

```sql
-- Campos base (OSM)
name VARCHAR(500)
latitude DECIMAL(10, 8)
longitude DECIMAL(11, 8)
country VARCHAR(100)
site_type VARCHAR(100)
osm_id VARCHAR(50)

-- Campos enriquecidos (Wikidata)
wikidata_id VARCHAR(50)
period_detailed VARCHAR(200)
culture VARCHAR(200)
date_established VARCHAR(100)
image_url TEXT
heritage_designation VARCHAR(200)
wikipedia_url TEXT
wikidata_enriched BOOLEAN

-- Campos validados (UNESCO)
unesco_id VARCHAR(50)
unesco_status VARCHAR(50)  -- inscribed | tentative | not_listed
unesco_year INTEGER
unesco_criteria VARCHAR(50)
unesco_validated BOOLEAN

-- Campos nacionales (Opcional)
national_registry VARCHAR(100)
national_ref VARCHAR(100)
protection_status VARCHAR(100)

-- Metadatos
confidence_level VARCHAR(50)  -- high | medium | low
data_quality_score DECIMAL(3, 2)
last_verified TIMESTAMP
enriched_at TIMESTAMP
```

## 🚀 Comandos de Ejecución

### Paso 1: Enriquecer datos existentes
```bash
# Enriquecer primeros 100 sitios (prueba)
python scripts/enrich_archaeological_data.py

# Enriquecer todos los sitios con Wikidata ID (~7,844)
# (Toma varias horas - ejecutar en lotes)
```

### Paso 2: Actualizar base de datos
```bash
# Migrar datos enriquecidos a PostgreSQL
python scripts/update_db_with_enriched_data.py
```

### Paso 3: Verificar resultados
```bash
# Test de endpoint
python test_endpoint.py

# Verificar estadísticas
python test_db_connection.py
```

## 📊 Métricas de Calidad

### Cobertura esperada:
- **OSM base**: 100% (69,531 sitios)
- **Wikidata enriquecimiento**: ~10-15% (7,000-10,000 sitios)
- **UNESCO validación**: ~1-2% (1,000-1,500 sitios)
- **Registros nacionales**: Variable por país

### Niveles de confianza:
- **Alta**: UNESCO + Wikidata + OSM (triple validación)
- **Media**: Wikidata + OSM (doble validación)
- **Baja**: Solo OSM (validación simple)

## 🎯 Próximos Pasos

1. ✅ **Completado**: Migración base OSM + Wikidata (80,457 sitios)
2. 🔄 **En progreso**: Script de enriquecimiento Wikidata
3. ⏳ **Pendiente**: Validación UNESCO automática
4. ⏳ **Pendiente**: Integración registros nacionales
5. ⏳ **Pendiente**: Sistema de actualización continua

## 📚 Referencias

- **OpenStreetMap**: https://wiki.openstreetmap.org/wiki/Tag:historic=archaeological_site
- **Wikidata**: https://www.wikidata.org/wiki/Q839954 (archaeological site)
- **UNESCO**: https://whc.unesco.org/en/list/
- **Overpass API**: https://overpass-api.de/
- **SPARQL Wikidata**: https://query.wikidata.org/

## 🔐 Consideraciones Éticas

- Todos los datos son de fuentes públicas
- Respeto a rate limits de APIs
- Atribución correcta de fuentes
- No redistribución comercial sin permiso
- Uso académico y científico prioritario

---

**Última actualización**: 2026-01-25  
**Estado**: Base migrada, enriquecimiento en desarrollo  
**Contacto**: ArcheoScope Project
