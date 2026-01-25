# 🗄️ ArcheoScope Database - Resumen Ejecutivo

## 🎯 Objetivo

Migrar de JSON estático a PostgreSQL con Prisma ORM para:
- ✅ Escalar a miles de sitios arqueológicos
- ✅ Queries rápidos y eficientes
- ✅ Historial completo de detecciones
- ✅ Integridad referencial garantizada
- ✅ Búsquedas geoespaciales avanzadas

---

## 📊 Estructura de la Base de Datos

### Tablas Principales (9)

1. **archaeological_sites** - Sitios arqueológicos (11 sitios iniciales)
2. **calibration_data** - Firmas instrumentales por sitio
3. **detection_history** - Historial de análisis de ArcheoScope
4. **anomaly_signatures** - Umbrales por tipo de ambiente
5. **archaeological_features** - Características de cada sitio
6. **data_sources** - Fuentes de datos (UNESCO, académicas)
7. **site_data_availability** - Disponibilidad de datos (LiDAR, SAR, etc.)
8. **site_threats** - Amenazas a sitios (erosión, turismo, etc.)
9. **research_questions** - Preguntas de investigación abiertas

### Tablas Auxiliares (3)

10. **analysis_sessions** - Seguimiento de sesiones de usuario
11. **system_configuration** - Configuración del sistema
12. **[futuro]** Más tablas según necesidades

---

## 🏛️ Datos Iniciales

### Sitios de Referencia (7)

| Sitio | País | Ambiente | UNESCO | Calibrado |
|-------|------|----------|--------|-----------|
| Giza Pyramids | Egypt | DESERT | ✅ #86 | ✅ |
| Angkor Wat | Cambodia | FOREST | ✅ #668 | ✅ |
| Ötzi the Iceman | Alps | GLACIER | ❌ | ✅ |
| Port Royal | Jamaica | SHALLOW_SEA | ❌ | ✅ |
| Machu Picchu | Peru | MOUNTAIN | ✅ #274 | ✅ |
| Petra | Jordan | DESERT | ✅ #326 | ✅ |
| Stonehenge | UK | GRASSLAND | ✅ #373 | ✅ |

### Sitios de Control (4)

| Sitio | Ambiente | Propósito |
|-------|----------|-----------|
| Atacama Desert | DESERT | Calibrar falsos positivos |
| Amazon Rainforest | FOREST | Calibrar falsos positivos |
| Greenland Ice Sheet | POLAR_ICE | Calibrar falsos positivos |
| Pacific Ocean | DEEP_OCEAN | Calibrar falsos positivos |

**Total:** 11 sitios (7 arqueológicos + 4 control)

---

## 🔧 Tecnologías

### Stack

- **Base de Datos:** PostgreSQL 14+
- **ORM:** Prisma 5.8+
- **Lenguaje:** TypeScript/Node.js
- **Extensiones:** PostGIS (geoespacial, opcional)

### Ventajas de Prisma

✅ **Type-safe:** Autocompletado y validación en tiempo de compilación  
✅ **Migraciones:** Control de versiones de schema  
✅ **Studio:** UI visual para explorar datos  
✅ **Performance:** Queries optimizados automáticamente  
✅ **Multi-lenguaje:** Clientes para Node.js, Python, Go, Rust

---

## 🚀 Setup Rápido

```bash
# 1. Instalar dependencias
npm install

# 2. Configurar .env
cp .env.example .env
# Editar DATABASE_URL

# 3. Setup completo
npm run db:setup

# 4. Abrir Prisma Studio
npm run db:studio
# http://localhost:5555
```

---

## 📈 Comparación: JSON vs PostgreSQL

| Aspecto | JSON Actual | PostgreSQL + Prisma |
|---------|-------------|---------------------|
| **Sitios** | 11 | Ilimitado |
| **Búsqueda** | O(n) lineal | O(log n) indexado |
| **Queries complejos** | ❌ Difícil | ✅ SQL nativo |
| **Relaciones** | ❌ Manual | ✅ Automático |
| **Historial** | ❌ No | ✅ Completo |
| **Concurrencia** | ❌ Locks manuales | ✅ ACID |
| **Backups** | ❌ Manual | ✅ Automático |
| **Geoespacial** | ❌ No | ✅ PostGIS |
| **Escalabilidad** | 100s sitios | Millones |

---

## 🎯 Casos de Uso

### 1. Búsqueda por Coordenadas

**Antes (JSON):**
```python
# Iterar todos los sitios manualmente
for site in sites:
    if lat_min <= site.lat <= lat_max:
        # ...
```

**Ahora (PostgreSQL):**
```sql
SELECT * FROM archaeological_sites
WHERE latitude BETWEEN $1 AND $2
AND longitude BETWEEN $3 AND $4
LIMIT 10;
-- Milisegundos con índice
```

### 2. Sitios por Ambiente

**Antes (JSON):**
```python
# Filtrar manualmente
desert_sites = [s for s in sites if s.environment == 'desert']
```

**Ahora (PostgreSQL):**
```sql
SELECT * FROM archaeological_sites
WHERE "environmentType" = 'DESERT'
AND "isReferencesite" = true;
-- Instantáneo con índice
```

### 3. Historial de Detecciones

**Antes (JSON):**
```python
# Archivo separado, difícil de relacionar
history = json.load('history.json')
```

**Ahora (PostgreSQL):**
```sql
SELECT 
    dh.*,
    s.name as site_name
FROM detection_history dh
LEFT JOIN archaeological_sites s ON dh."siteId" = s.id
WHERE dh."archaeologicalProbability" > 0.5
ORDER BY dh."detectionDate" DESC;
-- Relación automática
```

### 4. Estadísticas

**Antes (JSON):**
```python
# Calcular manualmente
total = len(sites)
by_env = {}
for site in sites:
    by_env[site.env] = by_env.get(site.env, 0) + 1
```

**Ahora (PostgreSQL):**
```sql
SELECT 
    "environmentType",
    COUNT(*) as total,
    AVG("archaeologicalProbability") as avg_prob
FROM detection_history
GROUP BY "environmentType";
-- Agregaciones nativas
```

---

## 🔌 Integración con Backend Python

### Opción 1: asyncpg (Recomendado)

```python
import asyncpg
import os

async def get_sites():
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    sites = await conn.fetch(
        'SELECT * FROM archaeological_sites WHERE "isReferencesite" = true'
    )
    await conn.close()
    return sites
```

### Opción 2: Prisma Client Python

```python
from prisma import Prisma

db = Prisma()
await db.connect()

sites = await db.archaeologicalsite.find_many(
    where={'isReferencesite': True},
    include={'calibrationData': True}
)
```

### Opción 3: SQLAlchemy

```python
from sqlalchemy import create_engine
engine = create_engine(os.getenv('DATABASE_URL'))

import pandas as pd
df = pd.read_sql('SELECT * FROM archaeological_sites', engine)
```

---

## 📊 Schema Highlights

### Enums (Tipos Categóricos)

```prisma
enum EnvironmentType {
  DESERT, FOREST, GLACIER, SHALLOW_SEA, MOUNTAIN,
  GRASSLAND, POLAR_ICE, DEEP_OCEAN, UNKNOWN
}

enum SiteType {
  MONUMENTAL_COMPLEX, TEMPLE_COMPLEX, MOUNTAIN_CITADEL,
  ROCK_CUT_CITY, MEGALITHIC_MONUMENT, SUBMERGED_CITY,
  GLACIER_MUMMY, NATURAL_CONTROL
}

enum ConfidenceLevel {
  CONFIRMED, HIGH, MODERATE, LOW,
  NEGATIVE_CONTROL, CANDIDATE
}
```

### Relaciones

```prisma
model ArchaeologicalSite {
  id String @id @default(uuid())
  
  // Relaciones 1:N
  features ArchaeologicalFeature[]
  dataSources DataSource[]
  threats SiteThreat[]
  
  // Relación 1:1
  calibrationData CalibrationData?
  
  // Relación N:M (a través de DetectionHistory)
  detectionHistory DetectionHistory[]
}
```

### Índices para Performance

```prisma
@@index([environmentType])
@@index([latitude, longitude])
@@index([isReferencesite])
@@index([country])
```

---

## 🌐 Opciones de Hosting

### Gratis (Desarrollo)

1. **Supabase** - 500MB, 2 proyectos
2. **Railway** - 500MB, $5 crédito inicial
3. **Render** - 90 días gratis
4. **Neon** - 3GB, serverless PostgreSQL

### Producción

1. **AWS RDS** - Escalable, $15-50/mes
2. **Google Cloud SQL** - Similar a RDS
3. **DigitalOcean** - $15/mes, simple
4. **Heroku Postgres** - $9-50/mes

### Local

1. **PostgreSQL nativo** - Gratis, completo
2. **Docker** - Portable, fácil setup
3. **pgAdmin** - UI de administración

---

## 📝 Próximos Pasos

### Fase 1: Setup Inicial (Hoy)
- [x] Schema Prisma completo
- [x] Seed con 11 sitios
- [x] Documentación completa
- [ ] Instalar PostgreSQL
- [ ] Ejecutar migraciones
- [ ] Verificar en Prisma Studio

### Fase 2: Migración (Esta Semana)
- [ ] Script de migración JSON → PostgreSQL
- [ ] Actualizar backend Python para usar PostgreSQL
- [ ] Tests de integración
- [ ] Comparar performance JSON vs PostgreSQL

### Fase 3: Expansión (Próximo Mes)
- [ ] Agregar 50+ sitios arqueológicos
- [ ] Implementar PostGIS para búsquedas geoespaciales
- [ ] API GraphQL (opcional)
- [ ] Dashboard de estadísticas

### Fase 4: Producción (Futuro)
- [ ] Deploy en Supabase/Railway
- [ ] Backups automáticos
- [ ] Monitoreo y alertas
- [ ] Documentación API completa

---

## 🎓 Recursos de Aprendizaje

### Prisma
- [Quickstart](https://www.prisma.io/docs/getting-started/quickstart)
- [Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)
- [Prisma Studio](https://www.prisma.io/studio)

### PostgreSQL
- [Tutorial Oficial](https://www.postgresql.org/docs/current/tutorial.html)
- [PostGIS](https://postgis.net/workshops/postgis-intro/)
- [Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)

### Integración Python
- [asyncpg](https://magicstack.github.io/asyncpg/current/)
- [Prisma Python](https://prisma-client-py.readthedocs.io/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)

---

## 💡 Tips

### Performance
- Usar índices en columnas de búsqueda frecuente
- Limitar resultados con `LIMIT`
- Usar `EXPLAIN ANALYZE` para optimizar queries
- Considerar materialized views para agregaciones

### Seguridad
- Nunca commitear `.env` con credenciales
- Usar variables de entorno en producción
- Implementar rate limiting en API
- Validar inputs antes de queries

### Mantenimiento
- Backups diarios automáticos
- Monitorear tamaño de BD
- Vacuum regular para performance
- Actualizar Prisma y PostgreSQL

---

## 📞 Soporte

**Documentación:** `DATABASE_SETUP.md`  
**Schema:** `prisma/schema.prisma`  
**Seed:** `prisma/seed.ts`  
**Prisma Studio:** `npm run db:studio`

---

**Estado:** ✅ Listo para setup  
**Última actualización:** 2026-01-25  
**Versión:** 1.0.0
