#!/usr/bin/env python3
"""
Script para configurar DATABASE_URL en .env
"""

import getpass
import os

print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ArcheoScope - Configurar DATABASE_URL                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

print("Este script te ayudará a configurar la conexión a PostgreSQL.\n")

# Solicitar información
print("Información de conexión a PostgreSQL:")
print("-" * 60)

host = input("Host [localhost]: ").strip() or "localhost"
port = input("Puerto [5433]: ").strip() or "5433"
database = input("Base de datos [archeoscope]: ").strip() or "archeoscope"
user = input("Usuario [postgres]: ").strip() or "postgres"
password = getpass.getpass("Contraseña: ")

# Construir DATABASE_URL
database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}?schema=public"

print("\n" + "=" * 60)
print("DATABASE_URL generada:")
print("=" * 60)
# Mostrar con contraseña oculta
safe_url = f"postgresql://{user}:****@{host}:{port}/{database}?schema=public"
print(safe_url)
print()

# Confirmar
confirm = input("¿Guardar en .env? (s/n): ").strip().lower()

if confirm == 's':
    # Escribir .env
    with open('.env', 'w', encoding='utf-8') as f:
        f.write("# ArcheoScope Database Configuration\n")
        f.write(f"# PostgreSQL en {host}:{port}\n")
        f.write(f'DATABASE_URL="{database_url}"\n')
    
    print("\n✅ Archivo .env actualizado correctamente")
    print("\nPróximos pasos:")
    print("  1. npx prisma db push")
    print("  2. python scripts/migrate_harvested_to_postgres.py")
else:
    print("\n❌ Cancelado. No se guardaron cambios.")
