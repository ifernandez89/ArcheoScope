#!/usr/bin/env python3
"""
Test usando PROJ de rasterio directamente
"""

import os
from pathlib import Path

# Configurar PROJ_LIB a rasterio
proj_path = Path(r"C:\Users\xiphos-pc1\AppData\Roaming\Python\Python311\site-packages\rasterio\proj_data")
os.environ['PROJ_LIB'] = str(proj_path)
os.environ['PROJ_DATA'] = str(proj_path)

print(f"✅ PROJ_LIB configurado: {proj_path}")
print(f"✅ Existe: {proj_path.exists()}")
print(f"✅ proj.db existe: {(proj_path / 'proj.db').exists()}")
print()

try:
    from rasterio.crs import CRS
    crs = CRS.from_epsg(4326)
    print(f"✅ CRS creado exitosamente: {crs}")
    print()
    print("🎉 PROJ FUNCIONANDO CON RASTERIO")
except Exception as e:
    print(f"❌ Error: {e}")
