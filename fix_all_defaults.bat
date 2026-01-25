@echo off
echo Arreglando defaults de la tabla...
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 -d archeoscope_db -c "ALTER TABLE archaeological_sites ALTER COLUMN \"updatedAt\" SET DEFAULT CURRENT_TIMESTAMP;"
echo.
echo Listo! Ahora ejecuta: python scripts/migrate_harvested_to_postgres.py
pause
