#!/usr/bin/env python3
"""
Script para iniciar el backend de ArcheoScope en puerto 8003
"""

import sys
import os
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    print("🏺 Iniciando ArcheoScope Backend...")
    print(f"📁 Directorio backend: {backend_dir}")
    
    # Cambiar al directorio backend
    os.chdir(backend_dir)
    
    # Importar y ejecutar
    import uvicorn
    from api.main import app
    
    print("✅ Módulos importados correctamente")
    print("🚀 Iniciando servidor en puerto 8003...")
    
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Instalando dependencias...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "numpy", "scipy"])
    
except Exception as e:
    print(f"❌ Error iniciando backend: {e}")
    sys.exit(1)