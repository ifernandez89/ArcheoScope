#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test OpenTopography - Simple sin emojis
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

# Configurar PROJ
proj_path = Path(r"C:\Users\xiphos-pc1\AppData\Roaming\Python\Python311\site-packages\rasterio\proj_data")
os.environ['PROJ_LIB'] = str(proj_path)
os.environ['PROJ_DATA'] = str(proj_path)

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from satellite_connectors.opentopography_connector import OpenTopographyConnector

async def test_simple():
    """Test simple de OpenTopography"""
    
    print("="*70)
    print("TEST OPENTOPOGRAPHY - TIKAL, GUATEMALA")
    print("="*70)
    print()
    
    connector = OpenTopographyConnector()
    
    print(f"Estado: {'Disponible' if connector.available else 'No disponible'}")
    
    if not connector.available:
        print("ERROR: OpenTopography no disponible")
        print("Verifica OPENTOPOGRAPHY_API_KEY en .env")
        return False
    
    print(f"API Key: {os.getenv('OPENTOPOGRAPHY_API_KEY')[:20]}...")
    print()
    
    # Tikal, Guatemala
    print("Descargando DEM de Tikal...")
    print("Coordenadas: [17.2, 17.25] x [-89.65, -89.6]")
    print()
    
    try:
        data = await connector.get_elevation_data(
            17.20, 17.25,
            -89.65, -89.60,
            dem_type="SRTMGL1"
        )
        
        if data:
            print("EXITO: Datos obtenidos")
            print(f"  Fuente: {data['source']}")
            print(f"  Resolucion: {data['resolution_m']}m")
            print(f"  Confianza: {data['confidence']:.2%}")
            print()
            print("ELEVACION:")
            print(f"  Media: {data['elevation_mean']:.1f}m")
            print(f"  Min: {data['elevation_min']:.1f}m")
            print(f"  Max: {data['elevation_max']:.1f}m")
            print(f"  Rugosidad: {data['roughness']:.3f}")
            print()
            print("DETECCION ARQUEOLOGICA:")
            print(f"  Score: {data['archaeological_score']:.3f}")
            print(f"  Plataformas: {data['platforms_detected']}%")
            print(f"  Monticulos: {data['mounds_detected']}%")
            print(f"  Terrazas: {data['terraces_detected']}%")
            print()
            
            if data['archaeological_score'] > 0.3:
                print("RESULTADO: ALTA PROBABILIDAD ARQUEOLOGICA")
            elif data['archaeological_score'] > 0.15:
                print("RESULTADO: PROBABILIDAD MODERADA")
            else:
                print("RESULTADO: BAJA PROBABILIDAD")
            
            print()
            print("="*70)
            print("TEST EXITOSO - OpenTopography funcionando")
            print("="*70)
            return True
        else:
            print("ERROR: No se obtuvieron datos")
            return False
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple())
    exit(0 if success else 1)
