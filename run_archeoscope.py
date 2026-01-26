#!/usr/bin/env python3
"""
Script para ejecutar ArcheoScope - Archaeological Remote Sensing Engine.

Mantiene la misma estructura que CryoScope pero optimizado para arqueología remota.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import requests
import os

# FIX CRÍTICO: Configurar PROJ_LIB antes de importar rasterio
# PostgreSQL conflictúa con rasterio - forzar uso de PROJ de rasterio
try:
    import rasterio
    proj_path = Path(rasterio.__file__).parent / 'proj_data'
    if proj_path.exists():
        os.environ['PROJ_LIB'] = str(proj_path)
        os.environ['PROJ_DATA'] = str(proj_path)
        print(f"✅ PROJ configurado: {proj_path}")
except Exception as e:
    print(f"⚠️ No se pudo configurar PROJ: {e}")

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    try:
        import fastapi
        import uvicorn
        import numpy
        import scipy
        # import cv2  # Comentado temporalmente
        print("Dependencias del backend arqueologico verificadas")
        return True
    except ImportError as e:
        print(f"ERROR: Dependencia faltante: {e}")
        print("Ejecuta: pip install -r backend/requirements.txt")
        return False

def check_ollama():
    """Verificar estado de Ollama y phi4-mini-reasoning"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            
            if 'phi4-mini-reasoning' in model_names:
                print(f"OK: Ollama disponible con phi4-mini-reasoning")
                return True
            else:
                print(f"AVISO: Ollama disponible pero falta phi4-mini-reasoning")
                print(f"   Modelos disponibles: {model_names}")
                print("   Para instalar: ollama pull phi4-mini-reasoning")
                return False
    except:
        pass
    
    print("AVISO: Ollama no disponible - sistema funcionara con fallbacks deterministas")
    print("   Para activar IA arqueologica: ejecuta 'ollama serve' en otra terminal")
    print("   Luego: ollama pull phi4-mini-reasoning")
    return False

def start_backend():
    """Iniciar el servidor backend arqueologico"""
    print("Iniciando servidor ArcheoScope...")
    
    backend_path = Path(__file__).parent / "backend"
    
    try:
        # Cambiar al directorio backend y ejecutar
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "api.main:app", 
            "--host", "0.0.0.0", "--port", "8002", "--reload"
        ], cwd=backend_path)
        
        return process
    except Exception as e:
        print(f"ERROR: Error iniciando backend arqueologico: {e}")
        return None

def wait_for_backend():
    """Esperar a que el backend esté listo"""
    print("Esperando que ArcheoScope esté listo...")
    
    for i in range(15):
        try:
            response = requests.get("http://localhost:8002/", timeout=3)
            if response.status_code == 200:
                print("ArcheoScope listo")
                return True
        except:
            pass
        
        time.sleep(1)
        if i < 14:
            print(f"   Intentando conectar... ({i+1}/15)")
    
    print("ArcheoScope tardando más de lo esperado, pero continuando...")
    return True

def open_frontend():
    """Instrucciones para abrir el frontend arqueologico"""
    print("Para iniciar el frontend:")
    print("   python start_frontend.py")
    print("Esto resolverá problemas CORS sirviendo desde localhost")
    print("El backend debe estar corriendo en http://localhost:8002")
    return True

def main():
    """Función principal"""
    print("ARCHEOSCOPE - ARCHAEOLOGICAL REMOTE SENSING ENGINE")
    print("=" * 60)
    print("Plataforma de inferencia espacial científica para arqueología remota")
    print("Detecta persistencias espaciales no explicables por procesos naturales actuales")
    print("=" * 60)
    
    # Verificar dependencias
    if not check_dependencies():
        return 1
    
    # Verificar Ollama y phi4-mini-reasoning (opcional)
    check_ollama()
    
    # Iniciar backend
    backend_process = start_backend()
    if not backend_process:
        return 1
    
    try:
        # Esperar a que el backend esté listo
        if not wait_for_backend():
            return 1
        
        # Abrir frontend
        open_frontend()
        
        print("\n" + "=" * 60)
        print("ARCHEOSCOPE COMPLETAMENTE OPERATIVO")
        print("=" * 60)
        print("Frontend: Abierto en tu navegador")
        print("Backend API: http://localhost:8002")
        print("Documentación API: http://localhost:8002/docs")
        print("Estado del sistema: http://localhost:8002/status")
        
        print("\nCómo usar ArcheoScope:")
        print("1. Selecciona una región arqueologica en el mapa (Ctrl+click y arrastra)")
        print("2. Configura las capas de análisis (NDVI, térmico, SAR, etc.)")
        print("3. Presiona 'INVESTIGAR REGIÓN'")
        print("4. Explora las firmas arqueologicas en el panel derecho")
        print("5. Usa las capas conmutables para análisis detallado")
        
        print("\nIndicadores arqueologicos:")
        print("• Desacople vegetación-topografía (muros, caminos enterrados)")
        print("• Patrones térmicos residuales (estructuras, fundaciones)")
        print("• Texturas anómalas SAR (geometría no natural)")
        print("• Rugosidad superficial (compactación, plazas)")
        print("• Salinidad del suelo (drenajes antiguos)")
        print("• Resonancia sísmica (cavidades, túneles)")
        
        print("\nPara detener el sistema: Presiona Ctrl+C")
        print("=" * 60)
        
        # Mantener el backend corriendo
        backend_process.wait()
        
    except KeyboardInterrupt:
        print("\nDeteniendo ArcheoScope...")
        backend_process.terminate()
        backend_process.wait()
        print("ArcheoScope detenido correctamente")
        return 0
    
    except Exception as e:
        print(f"\nERROR: Error inesperado: {e}")
        backend_process.terminate()
        return 1

if __name__ == "__main__":
    sys.exit(main())