#!/usr/bin/env python3
"""
Instalador de Dependencias para Datos Satelitales
Instala y verifica todas las dependencias necesarias
"""

import subprocess
import sys


def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n{'='*80}")
    print(f"📦 {description}")
    print(f"{'='*80}")
    print(f"Comando: {cmd}\n")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"✅ {description} - EXITOSO")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FALLÓ")
        print(f"Error: {e.stderr}")
        return False


def check_import(module_name, package_name=None):
    """Verificar si un módulo se puede importar"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"   ✅ {package_name}")
        return True
    except ImportError:
        print(f"   ❌ {package_name} - NO DISPONIBLE")
        return False


def main():
    print("\n" + "="*80)
    print("🛰️  INSTALADOR DE DEPENDENCIAS - DATOS SATELITALES REALES")
    print("="*80)
    
    # Paso 1: Instalar dependencias
    success = run_command(
        f"{sys.executable} -m pip install -r requirements-satellite.txt",
        "Instalando dependencias satelitales"
    )
    
    if not success:
        print("\n❌ Error instalando dependencias")
        return False
    
    # Paso 2: Verificar imports
    print("\n" + "="*80)
    print("🔍 VERIFICANDO INSTALACIÓN")
    print("="*80)
    
    modules_to_check = [
        ('pystac_client', 'pystac-client'),
        ('planetary_computer', 'planetary-computer'),
        ('rasterio', 'rasterio'),
        ('stackstac', 'stackstac'),
        ('numpy', 'numpy'),
        ('xarray', 'xarray'),
        ('dask', 'dask')
    ]
    
    all_ok = True
    for module, package in modules_to_check:
        if not check_import(module, package):
            all_ok = False
    
    # Paso 3: Verificar conectores
    print("\n" + "="*80)
    print("🔌 VERIFICANDO CONECTORES")
    print("="*80)
    
    try:
        from backend.satellite_connectors import PlanetaryComputerConnector
        print("   ✅ PlanetaryComputerConnector")
        
        from backend.satellite_cache import satellite_cache
        print("   ✅ SatelliteCache")
        
        from backend.async_satellite_processor import async_satellite_processor
        print("   ✅ AsyncSatelliteProcessor")
        
    except ImportError as e:
        print(f"   ❌ Error importando conectores: {e}")
        all_ok = False
    
    # Resultado final
    print("\n" + "="*80)
    if all_ok:
        print("✅ INSTALACIÓN COMPLETA Y VERIFICADA")
        print("="*80)
        print("\n🚀 Próximo paso:")
        print("   python test_real_satellite_data.py")
        return True
    else:
        print("❌ INSTALACIÓN INCOMPLETA")
        print("="*80)
        print("\n⚠️  Algunos módulos no están disponibles")
        print("   Intenta instalar manualmente:")
        print("   pip install pystac-client planetary-computer stackstac rasterio")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
