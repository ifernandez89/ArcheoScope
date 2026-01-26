# Fix PROJ Conflict - Renombrar proj.db de PostgreSQL
# EJECUTAR COMO ADMINISTRADOR (Click derecho -> Ejecutar como administrador)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "FIX PROJ CONFLICT - ArcheoScope" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$projPath = "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db"
$backupPath = "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db.backup"

# Verificar si existe
if (Test-Path $projPath) {
    Write-Host "✓ Encontrado: $projPath" -ForegroundColor Green
    Write-Host ""
    
    # Intentar renombrar
    try {
        Rename-Item $projPath $backupPath -ErrorAction Stop
        Write-Host "✅ ÉXITO: proj.db renombrado a proj.db.backup" -ForegroundColor Green
        Write-Host ""
        Write-Host "Los instrumentos satelitales deberían funcionar ahora." -ForegroundColor Green
        Write-Host ""
        Write-Host "Para verificar, ejecuta:" -ForegroundColor Yellow
        Write-Host "  python test_proj_fix.py" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Para revertir (si necesitas PostGIS):" -ForegroundColor Cyan
        Write-Host "  Rename-Item '$backupPath' '$projPath'" -ForegroundColor Cyan
    }
    catch {
        Write-Host "❌ ERROR: No se pudo renombrar el archivo" -ForegroundColor Red
        Write-Host "Razón: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Asegúrate de ejecutar este script como Administrador:" -ForegroundColor Yellow
        Write-Host "  Click derecho -> Ejecutar como administrador" -ForegroundColor Yellow
    }
}
else {
    Write-Host "⚠️ No se encontró: $projPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Posibles razones:" -ForegroundColor Yellow
    Write-Host "  1. PostgreSQL no está instalado en esa ubicación" -ForegroundColor Yellow
    Write-Host "  2. Ya fue renombrado anteriormente" -ForegroundColor Yellow
    Write-Host "  3. PostGIS no está instalado" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
