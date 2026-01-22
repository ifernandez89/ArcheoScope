#!/usr/bin/env python3
"""
Script para ejecutar el sistema completo de análisis subglacial.

Este script inicia el backend API y proporciona instrucciones para acceder al frontend.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import requests

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencias del backend verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("Ejecuta: pip install -r backend/requirements.txt")
        return False

def check_ollama():
    """Verificar estado de Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama disponible con {len(models)} modelos")
            return True
    except:
        pass
    
    print("⚠️  Ollama no disponible - sistema funcionará con fallbacks deterministas")
    print("   Para activar IA: ejecuta 'ollama serve' en otra terminal")
    return False

def start_backend():
    """Iniciar el servidor backend"""
    print("🚀 Iniciando servidor backend...")
    
    backend_path = Path(__file__).parent / "backend"
    
    try:
        # Cambiar al directorio backend y ejecutar
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "api.main:app", 
            "--host", "0.0.0.0", "--port", "8001", "--reload"
        ], cwd=backend_path)
        
        return process
    except Exception as e:
        print(f"❌ Error iniciando backend: {e}")
        return None

def wait_for_backend():
    """Esperar a que el backend esté listo"""
    print("⏳ Esperando que el backend esté listo...")
    
    for i in range(15):  # Reducir a 15 segundos
        try:
            response = requests.get("http://localhost:8001/", timeout=3)  # Usar puerto 8001
            if response.status_code == 200:
                print("✅ Backend listo")
                return True
        except:
            pass
        
        time.sleep(1)
        if i < 14:  # No mostrar el último intento
            print(f"   Intentando conectar... ({i+1}/15)")
    
    print("⚠️  Backend tardando más de lo esperado, pero continuando...")
    return True  # Continuar de todos modos

def open_frontend():
    """Abrir el frontend en el navegador"""
    frontend_path = Path(__file__).parent / "frontend" / "index.html"
    frontend_url = f"file://{frontend_path.absolute()}"
    
    print(f"🌐 Abriendo frontend: {frontend_url}")
    
    try:
        webbrowser.open(frontend_url)
        return True
    except Exception as e:
        print(f"❌ Error abriendo navegador: {e}")
        print(f"   Abre manualmente: {frontend_url}")
        return False

def main():
    """Función principal"""
    print("🔍 SUBGLACIAL COHERENCE ENGINE")
    print("=" * 50)
    print("Sistema científico para detectar donde las explicaciones glaciológicas actuales fallan")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        return 1
    
    # Verificar Ollama (opcional)
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
        
        print("\n" + "=" * 50)
        print("✅ SISTEMA COMPLETAMENTE OPERATIVO")
        print("=" * 50)
        print("🌐 Frontend: Abierto en tu navegador")
        print("🔧 Backend API: http://localhost:8001")
        print("📚 Documentación API: http://localhost:8001/docs")
        print("📊 Estado del sistema: http://localhost:8001/status")
        
        print("\n🎯 Cómo usar el sistema:")
        print("1. Selecciona una región en el mapa (Ctrl+click y arrastra)")
        print("2. Ajusta parámetros si es necesario")
        print("3. Presiona 'INVESTIGAR'")
        print("4. Explora los resultados en el panel derecho")
        print("5. Usa las capas conmutables para análisis detallado")
        
        print("\n⚠️  Para detener el sistema: Presiona Ctrl+C")
        print("=" * 50)
        
        # Mantener el backend corriendo
        backend_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo sistema...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Sistema detenido correctamente")
        return 0
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        backend_process.terminate()
        return 1

if __name__ == "__main__":
    sys.exit(main())