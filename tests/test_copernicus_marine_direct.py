#!/usr/bin/env python3
"""
Test directo de Copernicus Marine
Diagnóstico de problema de login
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("="*80)
print("DIAGNOSTICO COPERNICUS MARINE")
print("="*80)

# 1. Verificar credenciales
username = os.getenv("COPERNICUS_MARINE_USERNAME")
password = os.getenv("COPERNICUS_MARINE_PASSWORD")

print(f"\n1. CREDENCIALES:")
print(f"   Username: {username}")
print(f"   Password: {'*' * len(password) if password else 'NO CONFIGURADO'}")

if not username or not password:
    print("   [FAIL] Credenciales no configuradas")
    sys.exit(1)
else:
    print("   [OK] Credenciales configuradas")

# 2. Verificar librería instalada
print(f"\n2. LIBRERIA:")
try:
    import copernicusmarine
    print(f"   [OK] copernicusmarine instalado")
    print(f"   Version: {copernicusmarine.__version__ if hasattr(copernicusmarine, '__version__') else 'desconocida'}")
except ImportError as e:
    print(f"   [FAIL] copernicusmarine no instalado")
    print(f"   Error: {e}")
    print(f"   Instalar con: pip install copernicusmarine")
    sys.exit(1)

# 3. Intentar login
print(f"\n3. LOGIN:")
try:
    print(f"   Configurando credenciales via environment...")
    
    # API 2.x usa variables de entorno
    os.environ['COPERNICUSMARINE_SERVICE_USERNAME'] = username
    os.environ['COPERNICUSMARINE_SERVICE_PASSWORD'] = password
    
    print(f"   Intentando login (sin parametros - API 2.x)...")
    
    # API correcta: login() sin parámetros
    copernicusmarine.login()
    
    print(f"   [OK] LOGIN EXITOSO")
    
except Exception as e:
    print(f"   [WARN] LOGIN FALLIDO (puede ser normal)")
    print(f"   Error: {e}")
    print(f"   Tipo: {type(e).__name__}")
    print(f"   [INFO] Se intentara usar credenciales en cada comando")

# 4. Intentar obtener datos
print(f"\n4. TEST DE DATOS:")
try:
    print(f"   Intentando obtener lista de datasets...")
    
    # Listar datasets disponibles
    datasets = copernicusmarine.describe()
    
    print(f"   [OK] Acceso a catalogo exitoso")
    print(f"   Datasets disponibles: {len(datasets) if hasattr(datasets, '__len__') else 'N/A'}")
    
except Exception as e:
    print(f"   [WARN] No se pudo acceder al catalogo")
    print(f"   Error: {e}")
    print(f"   (Esto puede ser normal si el login funciono)")

# 5. Test simple de subset
print(f"\n5. TEST DE SUBSET (Mediterraneo):")
try:
    print(f"   Intentando obtener SST del Mediterraneo...")
    
    from datetime import datetime, timedelta
    
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=1)
    
    # Pasar credenciales explícitamente en el comando
    data = copernicusmarine.subset(
        dataset_id="SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001",
        variables=["analysed_sst"],
        minimum_longitude=10.0,
        maximum_longitude=12.0,
        minimum_latitude=40.0,
        maximum_latitude=42.0,
        start_datetime=start_date.strftime("%Y-%m-%d"),
        end_datetime=end_date.strftime("%Y-%m-%d"),
        username=username,
        password=password
    )
    
    if data:
        sst = float(data["analysed_sst"].mean().item())
        print(f"   [OK] DATOS OBTENIDOS")
        print(f"   SST Mediterraneo: {sst:.1f} C")
    else:
        print(f"   [WARN] No se obtuvieron datos")
    
except Exception as e:
    print(f"   [FAIL] FALLO al obtener datos")
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*80)
print("DIAGNOSTICO COMPLETADO")
print("="*80)

