# Configurar PROJ_LIB permanentemente para el usuario actual
# NO requiere permisos de administrador

$projPath = "C:\Users\xiphos-pc1\AppData\Roaming\Python\Python311\site-packages\pyproj\proj_dir\share\proj"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CONFIGURAR PROJ_LIB - ArcheoScope" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configurando PROJ_LIB para usuario actual..." -ForegroundColor Yellow
Write-Host "Ruta: $projPath" -ForegroundColor Yellow
Write-Host ""

try {
    # Configurar variable de entorno para el usuario
    [System.Environment]::SetEnvironmentVariable("PROJ_LIB", $projPath, [System.EnvironmentVariableTarget]::User)
    [System.Environment]::SetEnvironmentVariable("PROJ_DATA", $projPath, [System.EnvironmentVariableTarget]::User)
    
    # También configurar para la sesión actual
    $env:PROJ_LIB = $projPath
    $env:PROJ_DATA = $projPath
    
    Write-Host "✅ ÉXITO: PROJ_LIB configurado" -ForegroundColor Green
    Write-Host ""
    Write-Host "Variables configuradas:" -ForegroundColor Green
    Write-Host "  PROJ_LIB = $projPath" -ForegroundColor Green
    Write-Host "  PROJ_DATA = $projPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️ IMPORTANTE: Cierra y reabre todas las terminales/PowerShell" -ForegroundColor Yellow
    Write-Host "   para que los cambios tomen efecto." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Después, ejecuta:" -ForegroundColor Cyan
    Write-Host "  python test_proj_fix.py" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ ERROR: No se pudo configurar la variable" -ForegroundColor Red
    Write-Host "Razón: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
