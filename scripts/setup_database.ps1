# ArcheoScope Database Setup Script (PowerShell)
# ================================================

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║   ArcheoScope - Setup de Base de Datos PostgreSQL           ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar Node.js
Write-Host "🔍 Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no está instalado" -ForegroundColor Red
    Write-Host "   Instala Node.js desde: https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Verificar npm
try {
    $npmVersion = npm --version
    Write-Host "✅ npm $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm no está instalado" -ForegroundColor Red
    exit 1
}

# Instalar dependencias
Write-Host ""
Write-Host "📦 Instalando dependencias de Node.js..." -ForegroundColor Yellow
npm install

# Verificar .env
Write-Host ""
Write-Host "🔧 Verificando configuración..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Write-Host "⚠️  Archivo .env no encontrado" -ForegroundColor Yellow
    Write-Host "   Copiando .env.example a .env..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  IMPORTANTE: Edita .env y configura tu DATABASE_URL" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Opciones:" -ForegroundColor Cyan
    Write-Host "   1. PostgreSQL local: postgresql://postgres:postgres@localhost:5432/archeoscope_db"
    Write-Host "   2. Supabase: https://supabase.com (gratis)"
    Write-Host "   3. Railway: https://railway.app (gratis)"
    Write-Host ""
    Read-Host "   Presiona Enter después de configurar .env"
}

# Verificar DATABASE_URL
$envContent = Get-Content .env -Raw
if (-not ($envContent -match 'DATABASE_URL=') -or ($envContent -match 'DATABASE_URL="postgresql://archeoscope:password@localhost:5432/archeoscope_db')) {
    Write-Host "❌ DATABASE_URL no configurada correctamente en .env" -ForegroundColor Red
    Write-Host "   Edita .env y configura tu DATABASE_URL" -ForegroundColor Red
    exit 1
}

Write-Host "✅ DATABASE_URL configurada" -ForegroundColor Green

# Generar cliente Prisma
Write-Host ""
Write-Host "🔨 Generando cliente Prisma..." -ForegroundColor Yellow
npx prisma generate

# Ejecutar migraciones
Write-Host ""
Write-Host "🗄️  Ejecutando migraciones de base de datos..." -ForegroundColor Yellow
npx prisma migrate dev --name init

# Ejecutar seed
Write-Host ""
Write-Host "🌱 Poblando base de datos con datos iniciales..." -ForegroundColor Yellow
npx prisma db seed

# Migrar JSON a PostgreSQL
Write-Host ""
Write-Host "📂 Migrando datos del JSON a PostgreSQL..." -ForegroundColor Yellow
python scripts/migrate_json_to_postgres.py

# Resumen
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                              ║" -ForegroundColor Green
Write-Host "║   ✅ Setup Completado Exitosamente                           ║" -ForegroundColor Green
Write-Host "║                                                              ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 La base de datos está lista para usar!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Próximos pasos:" -ForegroundColor Yellow
Write-Host "   1. Abre Prisma Studio: npm run db:studio"
Write-Host "   2. Explora los datos en: http://localhost:5555"
Write-Host "   3. Integra con el backend Python"
Write-Host ""
Write-Host "📚 Documentación:" -ForegroundColor Yellow
Write-Host "   - DATABASE_SETUP.md: Guía completa"
Write-Host "   - DATABASE_SUMMARY.md: Resumen ejecutivo"
Write-Host ""
