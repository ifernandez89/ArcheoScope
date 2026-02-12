@echo off
echo ================================================================================
echo 🏛️ ArcheoScope 3D Viewer - Iniciando
echo ================================================================================
echo.
echo 📋 Información:
echo    • Puerto: 3000
echo    • URL: http://localhost:3000
echo    • Modelo: warrior.glb
echo.
echo 🔧 Verificando dependencias...
cd viewer3d

if not exist "node_modules" (
    echo.
    echo 📦 Instalando dependencias por primera vez...
    echo    Esto puede tomar unos minutos...
    echo.
    call npm install
    echo.
    echo ✅ Dependencias instaladas
    echo.
)

echo.
echo 🚀 Iniciando servidor de desarrollo...
echo ================================================================================
echo.

call npm run dev
