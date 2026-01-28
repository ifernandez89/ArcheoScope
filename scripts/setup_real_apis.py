#!/usr/bin/env python3
"""
Setup Real APIs - ArcheoScope
Instalar dependencias y configurar APIs reales
"""

import os
import subprocess
import sys

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def install_dependencies():
    """Instalar dependencias de APIs reales"""
    print_header("📦 Instalando Dependencias de APIs Reales")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements-satellite-real.txt"
        ])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def check_env_file():
    """Verificar archivo .env.local"""
    print_header("🔑 Verificando Configuración de API Keys")
    
    env_file = ".env.local"
    
    if not os.path.exists(env_file):
        print(f"⚠️  Archivo {env_file} no encontrado")
        print("Creando desde plantilla...")
        
        if os.path.exists(".env.local.example"):
            with open(".env.local.example", 'r', encoding='utf-8') as src:
                with open(env_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"✅ Archivo {env_file} creado")
        else:
            print(f"❌ Plantilla .env.local.example no encontrada")
            return False
    
    # Verificar API keys
    required_keys = [
        "EARTHDATA_USERNAME",
        "EARTHDATA_PASSWORD",
        "COPERNICUS_MARINE_USERNAME",
        "COPERNICUS_MARINE_PASSWORD",
        "OPENTOPOGRAPHY_API_KEY",
        "CDS_API_KEY"
    ]
    
    missing_keys = []
    
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
        for key in required_keys:
            if f"{key}=" not in content or f"{key}=your_" in content or f"{key}=tu_" in content:
                missing_keys.append(key)
    
    if missing_keys:
        print("\n⚠️  API Keys faltantes o no configuradas:")
        for key in missing_keys:
            print(f"   - {key}")
        
        print("\n📝 Instrucciones para obtener API keys:")
        print("\n1. NASA Earthdata (ICESat-2, MODIS, SMAP):")
        print("   https://urs.earthdata.nasa.gov/users/new")
        print("   Variables: EARTHDATA_USERNAME, EARTHDATA_PASSWORD")
        
        print("\n2. Copernicus Marine (Hielo marino):")
        print("   https://marine.copernicus.eu/register")
        print("   Variables: COPERNICUS_MARINE_USERNAME, COPERNICUS_MARINE_PASSWORD")
        
        print("\n3. OpenTopography (DEM):")
        print("   https://portal.opentopography.org/newUser")
        print("   Variable: OPENTOPOGRAPHY_API_KEY")
        
        print("\n4. Copernicus CDS (SMOS):")
        print("   https://cds.climate.copernicus.eu/user/register")
        print("   Variable: CDS_API_KEY")
        
        print(f"\n📝 Edita {env_file} con tus API keys")
        return False
    
    print("✅ Todas las API keys configuradas")
    return True

def test_connectors():
    """Probar conectores de APIs reales"""
    print_header("🧪 Probando Conectores de APIs Reales")
    
    try:
        from backend.satellite_connectors.real_data_integrator import RealDataIntegrator
        
        integrator = RealDataIntegrator()
        status = integrator.get_status_report()
        
        print(f"Total instrumentos: {status['total_instruments']}")
        print(f"Instrumentos activos: {status['active_instruments']}")
        print(f"Cobertura: {status['coverage_percent']:.1f}%")
        print(f"Sin simulaciones: {'✅ SÍ' if status['no_simulations'] else '❌ NO'}")
        
        print("\nEstado por instrumento:")
        for instrument, available in status['instruments'].items():
            status_icon = "✅" if available else "❌"
            print(f"  {status_icon} {instrument}")
        
        if status['coverage_percent'] >= 50:
            print("\n✅ Sistema listo para usar datos reales")
            return True
        else:
            print("\n⚠️  Configura más API keys para mejor cobertura")
            return False
    
    except Exception as e:
        print(f"❌ Error probando conectores: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_cache_dirs():
    """Crear directorios de caché"""
    print_header("📁 Creando Directorios de Caché")
    
    cache_dirs = [
        "cache/icesat2",
        "cache/opentopography",
        "cache/copernicus_marine",
        "cache/planetary_computer"
    ]
    
    for dir_path in cache_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ {dir_path}")
    
    return True

def main():
    """Ejecutar setup completo"""
    print_header("🚀 ArcheoScope - Setup de APIs Reales")
    
    print("Este script configurará TODAS las APIs reales gratuitas")
    print("para reemplazar las simulaciones en ArcheoScope.\n")
    
    steps = [
        ("Instalar dependencias", install_dependencies),
        ("Crear directorios de caché", create_cache_dirs),
        ("Verificar API keys", check_env_file),
        ("Probar conectores", test_connectors)
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"❌ Error en {step_name}: {e}")
            results.append((step_name, False))
    
    # Resumen final
    print_header("📊 Resumen de Setup")
    
    for step_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {step_name}")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    print(f"\nPasos completados: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 ¡Setup completado exitosamente!")
        print("\n🚀 Próximos pasos:")
        print("1. python run_archeoscope.py  # Iniciar backend")
        print("2. Probar con coordenadas reales")
        print("3. Verificar que NO hay simulaciones")
    else:
        print("\n⚠️  Setup incompleto")
        print("Revisa los errores arriba y configura las API keys faltantes")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
