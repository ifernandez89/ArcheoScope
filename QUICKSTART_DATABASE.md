# 🚀 QuickStart - Base de Datos ArcheoScope

## Setup en 3 Pasos

### 1️⃣ Instalar PostgreSQL

**Opción A: Supabase (Recomendado - Gratis)**
```
1. Ve a https://supabase.com
2. Crea cuenta gratis
3. New Project → Crea proyecto
4. Settings → Database → Connection string
5. Copia "URI" (empieza con postgresql://)
```

**Opción B: Railway (Gratis)**
```
1. Ve a https://railway.app
2. New Project → Provision PostgreSQL
3. Copia DATABASE_URL
```

**Opción C: Local con Docker**
```bash
docker run --name archeoscope-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=archeoscope_db \
  -p 5432:5432 \
  -d postgres:15
```

### 2️⃣ Configurar .env

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y pegar tu DATABASE_URL
# Ejemplo Supabase:
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres"

# Ejemplo local:
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/archeoscope_db"
```

### 3️⃣ Ejecutar Setup

**Windows (PowerShell):**
```powershell
.\setup_database.ps1
```

**Mac/Linux:**
```bash
chmod +x setup_database.sh
./setup_database.sh
```

**Manual (si los scripts fallan):**
```bash
# 1. Instalar dependencias
npm install

# 2. Generar cliente Prisma
npx prisma generate

# 3. Crear tablas
npx prisma migrate dev --name init

# 4. Poblar con datos iniciales
npx prisma db seed

# 5. Migrar JSON a PostgreSQL
python scripts/migrate_json_to_postgres.py
```

---

## ✅ Verificar Instalación

```bash
# Abrir Prisma Studio (UI visual)
npm run db:studio

# Se abrirá en http://localhost:5555
```

Deberías ver:
- ✅ 7 sitios de referencia (Giza, Angkor Wat, Ötzi, Port Royal, Machu Picchu, Petra, Stonehenge)
- ✅ 4 sitios de control (Atacama, Amazon, Greenland, Pacific)
- ✅ Características, fuentes de datos, calibración, etc.

---

## 🐛 Troubleshooting

### Error: "Can't reach database server"

**Solución:**
1. Verifica que PostgreSQL está corriendo
2. Verifica DATABASE_URL en .env
3. Prueba conexión: `npx prisma db pull`

### Error: "Database does not exist"

**Solución:**
```bash
# Crear base de datos
createdb archeoscope_db

# O con psql:
psql -U postgres -c "CREATE DATABASE archeoscope_db;"
```

### Error: "Prisma Client not generated"

**Solución:**
```bash
npx prisma generate
```

### Error en migración Python

**Solución:**
```bash
# Instalar dependencias Python
pip install asyncpg python-dotenv

# Ejecutar migración
python scripts/migrate_json_to_postgres.py
```

---

## 📊 Comandos Útiles

```bash
# Ver datos en UI visual
npm run db:studio

# Generar cliente después de cambios
npm run prisma:generate

# Crear nueva migración
npm run prisma:migrate

# Reset completo (CUIDADO: borra datos)
npm run prisma:reset

# Re-poblar datos
npm run prisma:seed
```

---

## 🎯 Próximos Pasos

1. ✅ Setup completado
2. 🔍 Explora datos en Prisma Studio
3. 🔌 Integra con backend Python
4. 📈 Agrega más sitios arqueológicos

---

## 📚 Documentación Completa

- **DATABASE_SETUP.md** - Guía detallada paso a paso
- **DATABASE_SUMMARY.md** - Resumen ejecutivo
- **prisma/schema.prisma** - Schema completo documentado

---

## 💡 Tips

- Usa Supabase para desarrollo (gratis, fácil)
- Prisma Studio es tu mejor amigo para explorar datos
- Backups automáticos en Supabase/Railway
- PostGIS para búsquedas geoespaciales avanzadas

---

**¿Necesitas ayuda?** Revisa DATABASE_SETUP.md o abre Prisma Studio para explorar.
