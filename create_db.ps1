# Crear base de datos ArcheoScope
$PSQL = "C:\Program Files\PostgreSQL\18\bin\psql.exe"

Write-Host "Creando base de datos archeoscope..." -ForegroundColor Cyan
Write-Host "Ingresa la contrasena de PostgreSQL (usuario: postgres):" -ForegroundColor Yellow

# Crear base de datos
& $PSQL -U postgres -c "CREATE DATABASE archeoscope;"

# Crear usuario
& $PSQL -U postgres -c "CREATE USER archeoscope WITH PASSWORD 'password';"

# Dar permisos
& $PSQL -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE archeoscope TO archeoscope;"

Write-Host ""
Write-Host "Completado! DATABASE_URL:" -ForegroundColor Green
Write-Host "postgresql://archeoscope:password@localhost:5432/archeoscope" -ForegroundColor White
