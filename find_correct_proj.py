#!/usr/bin/env python3
"""
Encontrar la ubicación correcta de proj.db
"""

import os
from pathlib import Path

print("="*60)
print("🔍 BUSCANDO PROJ.DB CORRECTO")
print("="*60)
print()

# Opción 1: PROJ de rasterio
try:
    import rasterio
    proj_path = Path(rasterio.__file__).parent / 'proj_data'
    print(f"📍 Rasterio proj_data: {proj_path}")
    print(f"   Existe: {proj_path.exists()}")
    
    if proj_path.exists():
        db_files = list(proj_path.glob("*.db"))
        print(f"   Archivos .db: {len(db_files)}")
        for db in db_files:
            print(f"     - {db.name}")
    print()
except Exception as e:
    print(f"❌ Error con rasterio: {e}")
    print()

# Opción 2: PROJ del sistema
try:
    import pyproj
    proj_datadir = pyproj.datadir.get_data_dir()
    print(f"📍 PyProj data dir: {proj_datadir}")
    
    if proj_datadir and Path(proj_datadir).exists():
        db_files = list(Path(proj_datadir).glob("*.db"))
        print(f"   Archivos .db: {len(db_files)}")
        for db in db_files[:5]:  # Primeros 5
            print(f"     - {db.name}")
    print()
except Exception as e:
    print(f"⚠️ PyProj no disponible: {e}")
    print()

# Opción 3: Buscar en site-packages
try:
    import site
    site_packages = site.getsitepackages()
    print(f"📍 Site packages:")
    for sp in site_packages:
        print(f"   - {sp}")
        
        # Buscar proj.db en cada site-package
        sp_path = Path(sp)
        if sp_path.exists():
            proj_dbs = list(sp_path.rglob("proj.db"))
            if proj_dbs:
                print(f"     ✅ Encontrado proj.db:")
                for db in proj_dbs[:3]:
                    print(f"       {db}")
    print()
except Exception as e:
    print(f"❌ Error buscando: {e}")
    print()

print("="*60)
