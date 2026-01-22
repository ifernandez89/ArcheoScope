#!/usr/bin/env python3
"""
Test de importación del módulo volumétrico
"""

import sys
from pathlib import Path

# Agregar el backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

try:
    print("🔧 Probando importación del motor volumétrico...")
    from backend.volumetric.lidar_fusion_engine import LidarFusionEngine
    print("✅ LidarFusionEngine importado correctamente")
    
    print("🔧 Probando importación del router volumétrico...")
    from backend.api.volumetric_lidar_api import volumetric_router
    print("✅ volumetric_router importado correctamente")
    
    print("🔧 Probando inicialización del motor...")
    engine = LidarFusionEngine()
    print("✅ Motor inicializado correctamente")
    
    print("🔧 Probando carga del catálogo...")
    catalog_path = Path(__file__).parent / "data" / "lidar_sites_catalog.json"
    if catalog_path.exists():
        success = engine.load_sites_catalog(str(catalog_path))
        if success:
            print(f"✅ Catálogo cargado: {len(engine.sites_catalog)} sitios")
        else:
            print("❌ Error cargando catálogo")
    else:
        print(f"❌ Catálogo no encontrado en: {catalog_path}")
    
    print("🔧 Probando endpoints del router...")
    print(f"   - Rutas disponibles: {[route.path for route in volumetric_router.routes]}")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Error general: {e}")
    import traceback
    traceback.print_exc()