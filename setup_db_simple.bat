@echo off
echo ========================================
echo ArcheoScope - Setup PostgreSQL Database
echo ========================================
echo.
echo Creando base de datos 'archeoscope' en PostgreSQL 18 (puerto 5433)
echo.
echo Ingresa la contrasena de PostgreSQL cuando se solicite...
echo.

"C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres -p 5433 archeoscope

echo.
echo ========================================
echo DATABASE_URL configurada:
echo postgresql://postgres:TU_PASSWORD@localhost:5433/archeoscope
echo ========================================
echo.
echo Proximos pasos:
echo 1. npm install
echo 2. npx prisma generate  
echo 3. npx prisma db push
echo 4. python scripts/migrate_harvested_to_postgres.py
echo.
pause
