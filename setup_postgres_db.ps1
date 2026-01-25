# Script para crear la base de datos ArcheoScope en PostgreSQL
# Ejecutar como: .\setup_postgres_db.ps1

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║   ArcheoScope - Setup PostgreSQL Database                   ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuración
$POSTGRES_PATH = "C:\Program Files\PostgreSQL\18\bin"
$PSQL = "$POSTGRES_PATH\psql.exe"
$CREATEDB = "$POSTGRES_PATH\createdb.exe"

# Verificar que PostgreSQL existe
if (-not (Test-Path $PSQL)) {
    Write-Host "❌ PostgreSQL no encontrado en: $POSTGRES_PATH" -ForegroundColor Red
    Write-Host "   Buscando en PostgreSQL 15..." -ForegroundColor Yellow
    $POSTGRES_PATH = "C:\Program Files\PostgreSQL\15\bin"
    $PSQL = "$POSTGRES_PATH\psql.exe"
    $CREATEDB = "$POSTGRES_PATH\createdb.exe"
    
    if (-not (Test-Path $PSQL)) {
        Write-Host "❌ PostgreSQL no encontrado" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ PostgreSQL encontrado: $POSTGRES_PATH" -ForegroundColor Green
Write-Host ""

# Solicitar contraseña
Write-Host "🔐 Ingresa la contraseña de PostgreSQL (usuario: postgres):" -ForegroundColor Yellow
$PGPASSWORD = Read-Host -AsSecureString
$env:PGPASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($PGPASSWORD))

Write-Host ""
Write-Host "📊 Verificando conexión a PostgreSQL..." -ForegroundColor Cyan

# Verificar conexión
$testConnection = & $PSQL -U postgres -c "SELECT version();" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error de conexión. Verifica la contraseña." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Conexión exitosa" -ForegroundColor Green
Write-Host ""

# Verificar si la base de datos ya existe
Write-Host "🔍 Verificando si la base de datos 'archeoscope' existe..." -ForegroundColor Cyan
$dbExists = & $PSQL -U postgres -lqt 2>&1 | Select-String -Pattern "archeoscope"

if ($dbExists) {
    Write-Host "⚠️  La base de datos 'archeoscope' ya existe" -ForegroundColor Yellow
    Write-Host "   ¿Deseas eliminarla y recrearla? (s/n): " -NoNewline -ForegroundColor Yellow
    $response = Read-Host
    
    if ($response -eq "s" -or $response -eq "S") {
        Write-Host "🗑️  Eliminando base de datos existente..." -ForegroundColor Yellow
        & $PSQL -U postgres -c "DROP DATABASE archeoscope;" 2>&1 | Out-Null
        Write-Host "✅ Base de datos eliminada" -ForegroundColor Green
    } else {
        Write-Host "✅ Usando base de datos existente" -ForegroundColor Green
        Write-Host ""
        Write-Host "🎯 Siguiente paso:" -ForegroundColor Cyan
        Write-Host "   npm install" -ForegroundColor White
        Write-Host "   npx prisma generate" -ForegroundColor White
        Write-Host "   npx prisma db push" -ForegroundColor White
        exit 0
    }
}

# Crear base de datos
Write-Host "🏗️  Creando base de datos 'archeoscope'..." -ForegroundColor Cyan
& $PSQL -U postgres -c "CREATE DATABASE archeoscope;" 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Base de datos 'archeoscope' creada exitosamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error al crear la base de datos" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Configurando usuario y permisos..." -ForegroundColor Cyan

# Crear usuario archeoscope si no existe
& $PSQL -U postgres -c "DO `$`$ BEGIN IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'archeoscope') THEN CREATE USER archeoscope WITH PASSWORD 'password'; END IF; END `$`$;" 2>&1 | Out-Null

# Otorgar permisos
& $PSQL -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE archeoscope TO archeoscope;" 2>&1 | Out-Null
& $PSQL -U postgres -d archeoscope -c "GRANT ALL ON SCHEMA public TO archeoscope;" 2>&1 | Out-Null

Write-Host "✅ Usuario y permisos configurados" -ForegroundColor Green
Write-Host ""

# Verificar puerto
Write-Host "🔌 Verificando puerto..." -ForegroundColor Cyan
$portCheck = & $PSQL -U postgres -c "SHOW port;" 2>&1 | Select-String -Pattern "5432"
if ($portCheck) {
    Write-Host "✅ PostgreSQL corriendo en puerto 5432" -ForegroundColor Green
} else {
    Write-Host "⚠️  PostgreSQL no está en puerto 5432" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETADO" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 DATABASE_URL configurada en .env.local:" -ForegroundColor Cyan
Write-Host "   postgresql://archeoscope:password@localhost:5432/archeoscope" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. npm install" -ForegroundColor White
Write-Host "   2. npx prisma generate" -ForegroundColor White
Write-Host "   3. npx prisma db push" -ForegroundColor White
Write-Host "   4. python scripts/migrate_harvested_to_postgres.py" -ForegroundColor White
Write-Host ""

# Limpiar contraseña del entorno
$env:PGPASSWORD = $null
