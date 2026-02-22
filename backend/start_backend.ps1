# Script de inicio del backend ArcheoScope
# Ejecutar desde la raíz del proyecto: .\backend\start_backend.ps1

Write-Host "🚀 Iniciando ArcheoScope Backend..." -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "backend/api/main.py")) {
    Write-Host "❌ Error: Ejecuta este script desde la raíz del proyecto" -ForegroundColor Red
    exit 1
}

# Activar entorno virtual si existe
if (Test-Path ".venv/Scripts/Activate.ps1") {
    Write-Host "📦 Activando entorno virtual..." -ForegroundColor Yellow
    & .venv/Scripts/Activate.ps1
} else {
    Write-Host "⚠️ No se encontró entorno virtual en .venv/" -ForegroundColor Yellow
}

# Verificar que uvicorn está instalado
try {
    $null = Get-Command uvicorn -ErrorAction Stop
    Write-Host "✅ uvicorn encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ uvicorn no encontrado. Instalando..." -ForegroundColor Red
    pip install uvicorn fastapi
}

# Cambiar al directorio backend
Set-Location backend

# Iniciar servidor
Write-Host ""
Write-Host "🌐 Iniciando servidor en http://localhost:8003" -ForegroundColor Green
Write-Host "📚 Documentación API: http://localhost:8003/docs" -ForegroundColor Cyan
Write-Host "🗺️ Terrain API: http://localhost:8003/api/terrain/info" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Ejecutar uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8003 --reload
