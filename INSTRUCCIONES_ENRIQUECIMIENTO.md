# 📚 Instrucciones para Enriquecimiento de Datos

## 🎯 Objetivo

Enriquecer los 80,457 sitios arqueológicos con datos detallados de Wikidata y validación UNESCO.

---

## ✅ Pre-requisitos

- ✅ PostgreSQL corriendo en puerto 5433
- ✅ Backend funcionando (80,457 sitios migrados)
- ✅ Conexión a internet (para APIs de Wikidata)
- ✅ Python 3.8+ con dependencias instaladas

---

## 🚀 Paso 1: Enriquecimiento de Prueba (Recomendado)

### Ejecutar con 100 sitios primero

```bash
# Desde el directorio raíz de ArcheoScope
python scripts/enrich_archaeological_data.py
```

**Cuando pregunte cuántos sitios enriquecer:**
```
¿Cuántos sitios enriquecer? (Enter para 100): 100
```

### Qué esperar:
```
🏛️ ENRIQUECIMIENTO DE DATOS ARQUEOLÓGICOS
========================================================

Estrategia:
  1. OSM como base principal (69,531 sitios)
  2. Enriquecimiento con Wikidata (IDs)
  3. Validación con UNESCO

📂 Cargando datos desde harvested_complete.json...
✅ Cargados 80,457 sitios

🔍 Sitios con Wikidata ID: 7,844

🚀 Enriqueciendo 100 sitios...
  Procesados: 10/100
  Procesados: 20/100
  ...
  
💾 Guardando resultados en enriched_sites_20260125_HHMMSS.json...
✅ Guardado

📊 ESTADÍSTICAS DE ENRIQUECIMIENTO
========================================================
Total procesados: 100
Enriquecidos con Wikidata: 45
Validados con UNESCO: 3
Errores: 2

Tasa de enriquecimiento Wikidata: 45.0%
Tasa de validación UNESCO: 3.0%
```

### Tiempo estimado:
- **100 sitios**: ~5-10 minutos
- **1,000 sitios**: ~1 hora
- **7,844 sitios** (todos con Wikidata ID): ~8-12 horas

---

## 🔍 Paso 2: Revisar Resultados

### Abrir archivo generado
```bash
# El archivo se llama: enriched_sites_YYYYMMDD_HHMMSS.json
# Ejemplo: enriched_sites_20260125_143022.json
```

### Verificar campos enriquecidos:
```json
{
  "name": "Pompeii",
  "latitude": 40.7489,
  "longitude": 14.4918,
  "country": "Italy",
  
  // Campos enriquecidos de Wikidata:
  "period_detailed": "Roman Empire",
  "culture": "Ancient Roman",
  "date_established": "79 CE",
  "image_url": "https://commons.wikimedia.org/...",
  "heritage_designation": "World Heritage Site",
  "wikipedia_url": "https://en.wikipedia.org/wiki/Pompeii",
  "wikidata_enriched": true,
  
  // Validación UNESCO:
  "unesco_status": "inscribed",
  "unesco_validated": true,
  
  "enriched_at": "2026-01-25T14:30:22"
}
```

---

## 📊 Paso 3: Actualizar Base de Datos

### Una vez satisfecho con los resultados:

```bash
python scripts/update_db_with_enriched_data.py
```

### Qué hace:
1. Busca el archivo más reciente `enriched_sites_*.json`
2. Conecta a PostgreSQL
3. Actualiza sitios por coordenadas + nombre
4. Reporta estadísticas

### Salida esperada:
```
📊 ACTUALIZACIÓN DE BASE DE DATOS CON DATOS ENRIQUECIDOS
========================================================

📂 Usando archivo: enriched_sites_20260125_143022.json
📂 Cargando enriched_sites_20260125_143022.json...
✅ Cargados 100 sitios enriquecidos

🔌 Conectando a PostgreSQL...
✅ Conectado

🔄 Actualizando 100 sitios...
  Actualizados: 10/100
  Actualizados: 20/100
  ...

📊 RESULTADOS DE ACTUALIZACIÓN
========================================================
Sitios procesados: 100
Sitios actualizados: 95
Errores: 5
```

---

## 🎯 Paso 4: Enriquecimiento Completo (Opcional)

### Para enriquecer TODOS los sitios con Wikidata ID:

```bash
python scripts/enrich_archaeological_data.py
```

**Cuando pregunte:**
```
¿Cuántos sitios enriquecer? (Enter para 100): 7844
```

### ⚠️ ADVERTENCIAS:

1. **Tiempo**: Tomará 8-12 horas
2. **Rate limiting**: El script hace pausas automáticas
3. **Errores**: Algunos sitios pueden fallar (normal)
4. **Interrupciones**: Si se interrumpe, puedes reanudar

### Recomendación:
```bash
# Ejecutar en segundo plano (Windows)
start /B python scripts/enrich_archaeological_data.py

# O en lotes de 1000:
# Lote 1: sitios 1-1000
# Lote 2: sitios 1001-2000
# etc.
```

---

## 📈 Paso 5: Verificar Resultados en API

### Test del endpoint:
```bash
python test_endpoint.py
```

### Verificar en navegador:
```
http://localhost:8002/archaeological-sites/known
```

### Debería mostrar:
```json
{
  "metadata": {
    "total_sites": 80457,
    "reference_sites": 0,
    "last_updated": "2026-01-25",
    "data_quality": "High - Multiple verified sources",
    "sources": ["UNESCO", "Wikidata", "OpenStreetMap"],
    "database": "PostgreSQL"
  },
  "top_countries": [...],
  "reference_sites_sample": [...]
}
```

---

## 🔧 Solución de Problemas

### Error: "No se encontró harvested_complete.json"
```bash
# Verificar que existe el archivo
dir harvested_complete.json

# Si no existe, ejecutar cosecha nuevamente
python scripts/harvest_complete.py
```

### Error: "connection refused" (PostgreSQL)
```bash
# Verificar que PostgreSQL está corriendo
# En Windows: Servicios > PostgreSQL 18

# Verificar puerto
python test_db_connection.py
```

### Error: "Rate limit exceeded" (Wikidata)
```bash
# El script ya tiene rate limiting
# Si persiste, aumentar pausas en el código:
# time.sleep(0.1) -> time.sleep(0.5)
```

### Error: "Timeout" (Wikidata API)
```bash
# Aumentar timeout en el código:
# timeout=10 -> timeout=30
```

---

## 📊 Métricas de Calidad Esperadas

### Enriquecimiento Wikidata:
- **Tasa esperada**: 40-60% de sitios con Wikidata ID
- **Campos agregados**: 4-6 por sitio en promedio
- **Calidad**: Alta (datos estructurados)

### Validación UNESCO:
- **Tasa esperada**: 1-3% de sitios
- **Sitios UNESCO**: ~1,000-1,500 globalmente
- **Calidad**: Máxima (fuente oficial)

### Cobertura por país:
- **Europa**: 60-80% enriquecimiento
- **Asia**: 40-60% enriquecimiento
- **América**: 30-50% enriquecimiento
- **África**: 20-40% enriquecimiento
- **Oceanía**: 30-50% enriquecimiento

---

## 🎯 Próximos Pasos Después del Enriquecimiento

1. **Actualizar Frontend**
   - Mostrar imágenes de sitios
   - Filtros por período/cultura
   - Badge UNESCO para sitios validados

2. **Mejorar Búsqueda**
   - Búsqueda por período arqueológico
   - Búsqueda por cultura
   - Filtro UNESCO

3. **Exportar Datos**
   - CSV para análisis
   - GeoJSON para mapas
   - API pública documentada

4. **Actualización Continua**
   - Cron job semanal
   - Nuevos sitios de OSM
   - Actualizaciones de Wikidata

---

## 📚 Referencias

- **Wikidata Query Service**: https://query.wikidata.org/
- **UNESCO World Heritage**: https://whc.unesco.org/en/list/
- **OpenStreetMap**: https://www.openstreetmap.org/
- **SPARQL Tutorial**: https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial

---

## ✅ Checklist

- [ ] Ejecutar enriquecimiento de prueba (100 sitios)
- [ ] Revisar archivo `enriched_sites_*.json`
- [ ] Actualizar base de datos con datos enriquecidos
- [ ] Verificar endpoint `/archaeological-sites/known`
- [ ] Decidir si ejecutar enriquecimiento completo
- [ ] Documentar resultados

---

**¿Listo para empezar?**

```bash
python scripts/enrich_archaeological_data.py
```

**¡Buena suerte con el enriquecimiento! 🚀**
