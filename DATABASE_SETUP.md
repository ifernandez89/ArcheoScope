# 🗄️ ArcheoScope Database Setup

Base de datos PostgreSQL con Prisma ORM para gestionar sitios arqueológicos.

## 📋 Requisitos

- Node.js 18+ y npm
- PostgreSQL 14+
- Git

## 🚀 Setup Rápido

### 1. Instalar Dependencias

```bash
npm install
```

### 2. Configurar Base de Datos

#### Opción A: PostgreSQL Local

```bash
# Instalar PostgreSQL (si no lo tienes)
# Windows: https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Crear base de datos
createdb archeoscope_db

# O usando psql:
psql -U postgres
CREATE DATABASE archeoscope_db;
\q
```

#### Opción B: PostgreSQL con Docker

```bash
# Crear contenedor PostgreSQL
docker run --name archeoscope-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=archeoscope_db \
  -p 5432:5432 \
  -d postgres:15

# Verificar que está corriendo
docker ps
```

#### Opción C: Servicios en la Nube (Recomendado)

**Supabase (Gratis):**
1. Ir a https://supabase.com
2. Crear nuevo proyecto
3. Copiar "Connection string" desde Settings > Database
4. Usar en `.env`

**Railway (Gratis):**
1. Ir a https://railway.app
2. New Project > Provision PostgreSQL
3. Copiar DATABASE_URL
4. Usar en `.env`

**Render (Gratis):**
1. Ir a https://render.com
2. New > PostgreSQL
3. Copiar External Database URL
4. Usar en `.env`

### 3. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tu DATABASE_URL
# Ejemplo local:
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/archeoscope_db"

# Ejemplo Supabase:
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres"
```

### 4. Ejecutar Migraciones y Seed

```bash
# Setup completo (genera cliente, migra y puebla BD)
npm run db:setup

# O paso por paso:
npm run prisma:generate  # Genera cliente Prisma
npm run prisma:migrate   # Crea tablas en BD
npm run prisma:seed      # Puebla con datos iniciales
```

### 5. Verificar Instalación

```bash
# Abrir Prisma Studio (UI visual para la BD)
npm run db:studio

# Se abrirá en http://localhost:5555
```

---

## 📊 Estructura de la Base de Datos

### Tablas Principales

#### `archaeological_sites`
Sitios arqueológicos con toda su información.

**Campos clave:**
- `name`, `alternateNames`, `slug`
- `environmentType` (DESERT, FOREST, GLACIER, etc.)
- `siteType` (MONUMENTAL_COMPLEX, TEMPLE_COMPLEX, etc.)
- `latitude`, `longitude`, `elevation`
- `country`, `region`
- `unescoId`, `unescoStatus`
- `isReferencesite`, `isControlSite`

#### `calibration_data`
Firmas instrumentales esperadas para cada sitio.

**Campos:**
- `thermalDeltaK` - Anomalía térmica (Kelvin)
- `sarBackscatterDb` - Backscatter SAR (dB)
- `ndviDelta` - Delta NDVI
- `lidarHeightM` - Altura LiDAR (metros)
- `elevationTerracingM` - Terrazas (metros)
- `magneticAnomalyNt` - Anomalía magnética (nT)

#### `detection_history`
Historial de detecciones de ArcheoScope.

**Campos:**
- `regionName`, coordenadas
- `environmentDetected`
- `archaeologicalProbability`
- `instrumentsConverging`
- `siteRecognized`
- `measurements` (JSON)

#### `anomaly_signatures`
Firmas de anomalías por tipo de ambiente.

**Campos:**
- `environmentType`
- `primaryInstruments`, `secondaryInstruments`
- `minimumConvergence`
- `indicators` (JSON con umbrales)

### Relaciones

```
ArchaeologicalSite
  ├── features[] (ArchaeologicalFeature)
  ├── dataSources[] (DataSource)
  ├── dataAvailability[] (SiteDataAvailability)
  ├── threats[] (SiteThreat)
  ├── researchQuestions[] (ResearchQuestion)
  ├── calibrationData (CalibrationData)
  └── detectionHistory[] (DetectionHistory)
```

---

## 🎯 Datos Iniciales (Seed)

El seed crea automáticamente:

### 7 Sitios de Referencia Arqueológicos

1. **Giza Pyramids** (Egypt) - DESERT
2. **Angkor Wat** (Cambodia) - FOREST
3. **Ötzi the Iceman** (Alps) - GLACIER
4. **Port Royal** (Jamaica) - SHALLOW_SEA
5. **Machu Picchu** (Peru) - MOUNTAIN
6. **Petra** (Jordan) - DESERT
7. **Stonehenge** (UK) - GRASSLAND

### 4 Sitios de Control (Negativos)

1. **Atacama Desert** - DESERT (sin arqueología)
2. **Amazon Rainforest** - FOREST (sin arqueología)
3. **Greenland Ice Sheet** - POLAR_ICE (sin arqueología)
4. **Pacific Ocean** - DEEP_OCEAN (sin arqueología)

### 8 Firmas de Anomalías

Una por cada tipo de ambiente principal.

---

## 🔧 Comandos Útiles

### Desarrollo

```bash
# Abrir Prisma Studio (UI visual)
npm run db:studio

# Generar cliente Prisma después de cambios en schema
npm run prisma:generate

# Crear nueva migración
npm run prisma:migrate

# Ver estado de migraciones
npx prisma migrate status

# Aplicar migraciones pendientes
npx prisma migrate deploy
```

### Mantenimiento

```bash
# Reset completo (CUIDADO: borra todos los datos)
npm run prisma:reset

# Re-seed (volver a poblar)
npm run prisma:seed

# Formatear schema
npx prisma format

# Validar schema
npx prisma validate
```

### Producción

```bash
# Generar cliente para producción
npx prisma generate

# Aplicar migraciones en producción
npx prisma migrate deploy

# No usar migrate dev en producción!
```

---

## 📝 Uso desde Python (Backend)

### Opción 1: API REST con FastAPI

Crear endpoints que consulten la BD:

```python
# backend/api/database.py
import asyncpg
import os

async def get_archaeological_sites():
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    sites = await conn.fetch('''
        SELECT * FROM archaeological_sites 
        WHERE "isReferencesite" = true
    ''')
    await conn.close()
    return sites
```

### Opción 2: Prisma Client Python

```bash
pip install prisma
```

```python
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()
    
    sites = await db.archaeologicalsite.find_many(
        where={'isReferencesite': True}
    )
    
    await db.disconnect()
```

### Opción 3: SQLAlchemy

```python
from sqlalchemy import create_engine
import os

engine = create_engine(os.getenv('DATABASE_URL'))

# Usar con pandas
import pandas as pd
df = pd.read_sql('SELECT * FROM archaeological_sites', engine)
```

---

## 🌐 Integración con Backend Actual

### 1. Migrar desde JSON a PostgreSQL

```python
# scripts/migrate_json_to_postgres.py
import json
import asyncpg
import asyncio

async def migrate():
    # Leer JSON actual
    with open('data/archaeological_sites_database.json') as f:
        data = json.load(f)
    
    # Conectar a PostgreSQL
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    # Insertar sitios
    for site_id, site_data in data['reference_sites'].items():
        await conn.execute('''
            INSERT INTO archaeological_sites (...)
            VALUES (...)
        ''')
    
    await conn.close()

asyncio.run(migrate())
```

### 2. Actualizar Validator

```python
# backend/validation/postgresql_validator.py
import asyncpg

class PostgreSQLArchaeologicalValidator:
    def __init__(self, database_url):
        self.database_url = database_url
    
    async def validate_region(self, lat_min, lat_max, lon_min, lon_max):
        conn = await asyncpg.connect(self.database_url)
        
        sites = await conn.fetch('''
            SELECT * FROM archaeological_sites
            WHERE latitude BETWEEN $1 AND $2
            AND longitude BETWEEN $3 AND $4
            AND "isReferencesite" = true
        ''', lat_min, lat_max, lon_min, lon_max)
        
        await conn.close()
        return sites
```

---

## 🔍 Queries Útiles

### Buscar sitios por ambiente

```sql
SELECT name, country, "environmentType"
FROM archaeological_sites
WHERE "environmentType" = 'DESERT'
AND "isReferencesite" = true;
```

### Sitios con datos LiDAR disponibles

```sql
SELECT s.name, s.country
FROM archaeological_sites s
JOIN site_data_availability sda ON s.id = sda."siteId"
WHERE sda."dataType" = 'LIDAR'
AND sda.available = true;
```

### Sitios por nivel de amenaza

```sql
SELECT s.name, st."threatType", st.severity
FROM archaeological_sites s
JOIN site_threats st ON s.id = st."siteId"
WHERE st.severity = 'critical'
ORDER BY s.name;
```

### Datos de calibración por ambiente

```sql
SELECT 
    s.name,
    s."environmentType",
    cd."thermalDeltaK",
    cd."sarBackscatterDb",
    cd."calibrationConfidence"
FROM archaeological_sites s
JOIN calibration_data cd ON s.id = cd."siteId"
WHERE s."isReferencesite" = true
ORDER BY s."environmentType";
```

---

## 📈 Escalabilidad

### Ventajas de PostgreSQL vs JSON

✅ **Performance:**
- Queries indexados (milisegundos vs segundos)
- Búsquedas geoespaciales con PostGIS
- Joins eficientes entre tablas

✅ **Escalabilidad:**
- Millones de sitios sin problemas
- Historial completo de detecciones
- Análisis estadísticos complejos

✅ **Integridad:**
- Constraints y validaciones
- Transacciones ACID
- Relaciones garantizadas

✅ **Concurrencia:**
- Múltiples usuarios simultáneos
- Locks automáticos
- Backups incrementales

### Agregar PostGIS (Geoespacial)

```sql
-- Habilitar extensión PostGIS
CREATE EXTENSION postgis;

-- Agregar columna geométrica
ALTER TABLE archaeological_sites
ADD COLUMN geom geometry(Point, 4326);

-- Actualizar con coordenadas
UPDATE archaeological_sites
SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);

-- Crear índice espacial
CREATE INDEX idx_sites_geom ON archaeological_sites USING GIST(geom);

-- Buscar sitios en radio de 50km
SELECT name, ST_Distance(geom, ST_MakePoint(-72.5450, -13.1631)::geography) / 1000 as distance_km
FROM archaeological_sites
WHERE ST_DWithin(geom, ST_MakePoint(-72.5450, -13.1631)::geography, 50000)
ORDER BY distance_km;
```

---

## 🐛 Troubleshooting

### Error: "Can't reach database server"

```bash
# Verificar que PostgreSQL está corriendo
# Windows:
services.msc  # Buscar "postgresql"

# Mac/Linux:
pg_isready

# Docker:
docker ps | grep postgres
```

### Error: "Database does not exist"

```bash
# Crear base de datos
createdb archeoscope_db

# O con psql:
psql -U postgres -c "CREATE DATABASE archeoscope_db;"
```

### Error: "Migration failed"

```bash
# Reset y volver a intentar
npm run prisma:reset
npm run db:setup
```

### Error: "Prisma Client not generated"

```bash
npm run prisma:generate
```

---

## 📚 Recursos

- [Prisma Docs](https://www.prisma.io/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [PostGIS Docs](https://postgis.net/documentation/)
- [Supabase](https://supabase.com)
- [Railway](https://railway.app)

---

## 🎉 Próximos Pasos

1. ✅ Setup inicial completado
2. 🔄 Migrar datos desde JSON
3. 🔌 Integrar con backend Python
4. 📊 Agregar más sitios arqueológicos
5. 🗺️ Implementar búsquedas geoespaciales con PostGIS
6. 📈 Dashboard de estadísticas
7. 🔐 Sistema de autenticación
8. 🌐 API GraphQL (opcional)

---

**¿Necesitas ayuda?** Revisa los logs con `npx prisma studio` o consulta la documentación oficial.
