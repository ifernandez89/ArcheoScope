#!/usr/bin/env python3
"""
Test Real APIs Integration - Simple Version
============================================

Verifica que el sistema esté configurado correctamente para usar APIs reales
"""

import asyncio
import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent))

from backend.satellite_connectors.real_data_integrator import RealDataIntegrator


async def test_real_apis_simple():
    """Test simple de disponibilidad de APIs"""
    
    print("="*80)
    print("🧪 TEST: Disponibilidad de APIs Reales")
    print("="*80)
    print()
    
    # Inicializar integrador
    print("📦 Inicializando RealDataIntegrator...")
    integrator = RealDataIntegrator()
    print("✅ Integrador inicializado")
    print()
    
    # Verificar estado de APIs
    print("📊 Estado de APIs:")
    print("-" * 80)
    
    status = integrator.get_status_report()
    
    print(f"Total de instrumentos: {status['total_instruments']}")
    print(f"Instrumentos activos: {status['active_instruments']}")
    print(f"Cobertura: {status['coverage_percent']:.1f}%")
    print()
    
    print("Detalle por instrumento:")
    for instrument, available in status['instruments'].items():
        status_icon = "✅" if available else "❌"
        print(f"  {status_icon} {instrument}: {'Disponible' if available else 'No disponible'}")
    print()
    
    # Resumen
    print("="*80)
    print("📊 RESUMEN")
    print("="*80)
    
    if status['active_instruments'] > 0:
        print(f"✅ {status['active_instruments']} APIs disponibles")
        print("✅ Sistema configurado para usar datos reales")
        print("✅ Fallback a simulación disponible si API falla")
        print()
        print("🎯 PRÓXIMOS PASOS:")
        print("   1. Configurar API keys faltantes en .env.local")
        print("   2. Instalar dependencias faltantes (ver mensajes arriba)")
        print("   3. Ejecutar test completo: python test_real_apis_integration.py")
    else:
        print("⚠️ ADVERTENCIA: Ninguna API disponible")
        print("   Sistema funcionará solo con simulaciones")
        print()
        print("🔧 CONFIGURACIÓN REQUERIDA:")
        print("   1. Copiar .env.local.example a .env.local")
        print("   2. Agregar API keys necesarias")
        print("   3. Instalar dependencias: pip install -r requirements-satellite-real.txt")
    
    print()
    
    return status['active_instruments'] > 0


if __name__ == "__main__":
    try:
        success = asyncio.run(test_real_apis_simple())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
