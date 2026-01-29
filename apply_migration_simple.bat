@echo off
echo ================================================================================
echo APLICANDO MIGRACION: instrument_measurements
echo ================================================================================
echo.

REM Aplicar migración usando psql
psql -h localhost -p 5433 -U postgres -d archeoscope -f prisma/migrations/20260129_add_instrument_measurements.sql

echo.
echo ================================================================================
echo VERIFICANDO TABLA
echo ================================================================================
echo.

REM Verificar tabla
psql -h localhost -p 5433 -U postgres -d archeoscope -c "\dt instrument_measurements"
psql -h localhost -p 5433 -U postgres -d archeoscope -c "\d instrument_measurements"

echo.
echo ================================================================================
echo MIGRACION COMPLETADA
echo ================================================================================
pause
