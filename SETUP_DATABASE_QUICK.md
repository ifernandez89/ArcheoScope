# 🚀 Setup Rápido de Base de Datos PostgreSQL

## Opción 1: Supabase (RECOMENDADO - Gratis y Rápido)

### Paso 1: Crear cuenta en Supabase
1. Ve a https://supabase.com
2. Crea una cuenta gratis
3. Crea un nuevo proyecto:
   - Nombre: `archeoscope`
   - Database Password: (guarda esta contraseña)
   - Region: Elige la más cercana

### Paso 2: Obtener DATABASE_URL
1. En tu proyecto, ve a **Settings** → **Database**
2. Busca **Connection string** → **URI**
3. Copia la URL (se ve así):
   ```
   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
   ```

### Paso 3: Configurar .env.local
Reemplaza la línea DATABASE_URL en `.env.local` con tu URL de Supabase:

```bash
DATABASE_URL="postgresql://postgres.xxxxx:[TU-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
```

### Paso 4: Ejecutar migraciones
```bash
npm install
npx prisma generate
npx prisma db push
```

### Paso 5: Migrar datos
```bash
# Primero los sitios de referencia
python scripts/migrate_json_to_postgres.py

# Luego los 75,595 sitios recopilados
python scripts/migrate_harvested_to_postgres.py
```

---

## Opción 2: Railway (También Gratis)

### Paso 1: Crear cuenta
1. Ve a https://railway.app
2. Crea cuenta con GitHub
3. New Project → Provision PostgreSQL

### Paso 2: Obtener DATABASE_URL
1. Click en PostgreSQL
2. Variables → DATABASE_URL
3. Copia la URL

### Paso 3: Configurar y migrar
Igual que Supabase (pasos 3-5)

---

## Opción 3: PostgreSQL Local (Requiere instalación)

### Windows:
1. Descargar PostgreSQL: https://www.postgresql.org/download/windows/
2. Instalar con contraseña `password`
3. Crear base de datos:
   ```bash
   createdb archeoscope_db
   ```
4. Usar DATABASE_URL del .env.local actual
5. Ejecutar migraciones (pasos 4-5 de Supabase)

---

## ✅ Verificar que funciona

```bash
# Verificar conexión
npx prisma db pull

# Ver datos
npx prisma studio
```

---

## 🎯 Siguiente Paso

Una vez configurada la base de datos, ejecutar:

```bash
python scripts/migrate_harvested_to_postgres.py
```

Esto migrará los **75,595 sitios arqueológicos** a PostgreSQL.
