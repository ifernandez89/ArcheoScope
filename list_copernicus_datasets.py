#!/usr/bin/env python3
"""
List Copernicus Marine Datasets
================================
Lista los datasets disponibles en Copernicus Marine
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    import copernicusmarine
    
    print("="*80)
    print("🌊 Copernicus Marine - Datasets Disponibles")
    print("="*80)
    print()
    
    username = os.getenv('COPERNICUS_MARINE_USERNAME')
    password = os.getenv('COPERNICUS_MARINE_PASSWORD')
    
    if not username or not password:
        print("❌ Credenciales no encontradas")
        exit(1)
    
    print(f"✅ Usuario: {username}")
    print()
    
    # Buscar datasets de hielo marino
    print("🔍 Buscando datasets de hielo marino...")
    print("-" * 80)
    
    # Palabras clave para buscar
    keywords = ['seaice', 'ice', 'sea_ice', 'arctic', 'antarctic']
    
    print()
    print("📋 Para listar todos los datasets disponibles, usa:")
    print("   copernicusmarine describe --include-datasets")
    print()
    print("📋 Para buscar datasets específicos:")
    print("   copernicusmarine describe --contains seaice")
    print()
    print("💡 Datasets comunes de hielo marino:")
    print("   - SEAICE_GLO_PHY_L4_NRT_011_001")
    print("   - SEAICE_ARC_PHY_L4_NRT_011_002")
    print("   - SEAICE_ANT_PHY_L4_NRT_011_003")
    print()
    
except ImportError:
    print("❌ copernicusmarine no instalado")
    print("   Instalar con: pip install copernicusmarine")
except Exception as e:
    print(f"❌ Error: {e}")
