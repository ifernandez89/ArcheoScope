#!/usr/bin/env python3
"""
Fix PROJ environment - Configurar PROJ antes de cualquier import
"""

import os
import sys
from pathlib import Path

def fix_proj_environment():
    """
    Configurar PROJ_LIB para evitar conflicto con PostgreSQL
    
    Esta función debe llamarse ANTES de importar cualquier librería
    que use GDAL/PROJ (rasterio, geopandas, etc.)
    """
    
    # Encontrar la instalación correcta de PROJ
    try:
        # Opción 1: PROJ de rasterio
        import rasterio
        proj_path = Path(rasterio.__file__).parent / 'proj_data'
        
        if proj_path.exists():
            # Configurar variables de entorno
            os.environ['PROJ_LIB'] = str(proj_path)
            os.environ['PROJ_DATA'] = str(proj_path)
            
            # CRÍTICO: También configurar GDAL_DATA
            gdal_data = Path(rasterio.__file__).parent / 'gdal_data'
            if gdal_data.exists():
                os.environ['GDAL_DATA'] = str(gdal_data)
            
            # CRÍTICO: Limpiar cualquier referencia a PostgreSQL en PATH
            if 'PATH' in os.environ:
                paths = os.environ['PATH'].split(os.pathsep)
                # Filtrar paths de PostgreSQL
                filtered_paths = [p for p in paths if 'PostgreSQL' not in p]
                os.environ['PATH'] = os.pathsep.join(filtered_paths)
            
            print(f"✅ PROJ configurado: {proj_path}")
            print(f"✅ PostgreSQL removido del PATH")
            return True
        else:
            print(f"⚠️ No se encontró proj_data en: {proj_path}")
            return False
            
    except ImportError:
        print("⚠️ rasterio no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error configurando PROJ: {e}")
        return False

# Ejecutar fix inmediatamente al importar este módulo
if __name__ != "__main__":
    fix_proj_environment()

if __name__ == "__main__":
    print("="*60)
    print("🔧 FIX PROJ ENVIRONMENT")
    print("="*60)
    print()
    
    success = fix_proj_environment()
    
    if success:
        print()
        print("Probando PROJ...")
        try:
            from rasterio.crs import CRS
            crs = CRS.from_epsg(4326)
            print(f"✅ CRS creado exitosamente: {crs}")
            print()
            print("🎉 PROJ FUNCIONANDO CORRECTAMENTE")
            print()
            print("Los instrumentos satelitales deberían funcionar ahora.")
        except Exception as e:
            print(f"❌ Error: {e}")
            print()
            print("El conflicto persiste. Necesitas ejecutar:")
            print("  fix_proj_conflict.ps1 (como Administrador)")
    else:
        print()
        print("❌ No se pudo configurar PROJ automáticamente")
