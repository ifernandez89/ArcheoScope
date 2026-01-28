#!/usr/bin/env python3
"""
Test simple para verificar que PROJ está configurado correctamente
"""

import os
from pathlib import Path

# Configurar PROJ
import rasterio
proj_path = Path(rasterio.__file__).parent / 'proj_data'
os.environ['PROJ_LIB'] = str(proj_path)
os.environ['PROJ_DATA'] = str(proj_path)

print(f"✅ PROJ configurado: {proj_path}")
print()

# Intentar crear un CRS
try:
    from rasterio.crs import CRS
    crs = CRS.from_epsg(4326)
    print(f"✅ CRS creado exitosamente: {crs}")
    print(f"✅ PROJ funcionando correctamente")
    print()
    print("🎉 FIX DE PROJ EXITOSO - Los instrumentos satelitales deberían funcionar ahora")
except Exception as e:
    print(f"❌ Error creando CRS: {e}")
    print(f"❌ PROJ aún tiene problemas")
