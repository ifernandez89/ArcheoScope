#!/usr/bin/env python3
"""
Iniciar API Creador3D
======================

API experimental de generación 3D separada de ArcheoScope científico.
Puerto: 8004
"""

import uvicorn
import sys
from pathlib import Path

# Agregar paths
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    print("="*80)
    print("🎨 CREADOR3D - API de Generación 3D Experimental")
    print("="*80)
    print("\n📋 Información:")
    print("   • Puerto: 8004")
    print("   • Separada de ArcheoScope (puerto 8003)")
    print("   • Permite experimentación sin comprometer rigor científico")
    print("\n🔗 Endpoints disponibles:")
    print("   • GET  /                      - Info de la API")
    print("   • GET  /status                - Estado del sistema")
    print("   • GET  /morphologies          - Listar clases morfológicas")
    print("   • POST /generate/description  - Generar desde texto")
    print("   • POST /generate/parameters   - Generar desde parámetros")
    print("   • POST /generate/morphology   - Generar desde morfología")
    print("   • POST /generate/custom       - Generar geometría custom")
    print("   • GET  /model/{filename}      - Descargar modelo")
    print("\n📁 Modelos se guardan en: creador3d_models/")
    print("\n🚀 Iniciando servidor...")
    print("="*80)
    print()
    
    uvicorn.run(
        "creador3d.api_creador3d:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
        log_level="info"
    )
