#!/usr/bin/env python3
"""
Script para iniciar servidor frontend ArcheoScope
Resuelve problemas CORS sirviendo desde localhost
"""

import os
import http.server
import socketserver
import webbrowser
import time
import sys
from pathlib import Path

def find_available_port(start_port=8080, max_attempts=10):
    """Encontrar puerto disponible"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as test_server:
                return port
        except OSError:
            continue
    return None

def start_frontend_server():
    """Iniciar servidor local para frontend"""
    
    # Cambiar al directorio frontend
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print(f"ERROR: Directorio frontend no encontrado: {frontend_dir}")
        return False
    
    try:
        os.chdir(frontend_dir)
        print(f"Cambiado al directorio: {os.getcwd()}")
        
        # Encontrar puerto disponible
        frontend_port = find_available_port(8080)
        if not frontend_port:
            print("ERROR: No hay puertos disponibles para el servidor frontend")
            return False
        
        print(f"Iniciando servidor frontend en puerto: {frontend_port}")
        print(f"Sirviendo archivos desde: {frontend_dir.absolute()}")
        print(f"URL: http://localhost:{frontend_port}/index.html")
        
        # Configurar handler simple
        class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                # Reducir logs del servidor
                pass
        
        # Iniciar servidor
        with socketserver.TCPServer(("", frontend_port), QuietHTTPRequestHandler) as httpd:
            print(f"Frontend servidor corriendo en: http://localhost:{frontend_port}")
            print("Para conectar con backend, asegúrate que está corriendo en http://localhost:8002")
            print("Presiona Ctrl+C para detener el servidor")
            
            # Abrir navegador automáticamente
            frontend_url = f"http://localhost:{frontend_port}/index.html"
            try:
                webbrowser.open(frontend_url)
                print(f"Abierto en navegador: {frontend_url}")
            except Exception as e:
                print(f"No se pudo abrir navegador automáticamente: {e}")
                print(f"   Abre manualmente: {frontend_url}")
            
            # Mantener servidor corriendo
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo servidor frontend...")
                return True
                
    except Exception as e:
        print(f"ERROR iniciando servidor frontend: {e}")
        print("Alternativa: Abre manualmente file://{}/frontend/index.html".format(Path(__file__).parent.absolute()))
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("ARCHEOSCOPE - SERVIDOR FRONTAL")
    print("=" * 60)
    print("Iniciando servidor local para resolver problemas CORS")
    print("Esto permite que el frontend se conecte al backend correctamente")
    print("=" * 60)
    
    success = start_frontend_server()
    
    if success:
        print("Servidor frontend detenido correctamente")
    else:
        print("Error al iniciar servidor frontend")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

import http.server
import socketserver
import os
import sys
from pathlib import Path

def start_frontend_server(port=8080):
    """Iniciar servidor web para el frontend."""
    
    # Cambiar al directorio del frontend
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    # Configurar servidor
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Añadir headers CORS para permitir conexión con la API
    class CORSRequestHandler(Handler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    with socketserver.TCPServer(("", port), CORSRequestHandler) as httpd:
        print(f"🌐 ArcheoScope Frontend iniciado en:")
        print(f"   http://localhost:{port}")
        print(f"   http://127.0.0.1:{port}")
        print(f"")
        print(f"🏺 ArcheoScope Archaeological Interface")
        print(f"   - Frontend: http://localhost:{port}")
        print(f"   - API Backend: http://localhost:8003")
        print(f"")
        print(f"Presiona Ctrl+C para detener el servidor")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Servidor frontend detenido")

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    start_frontend_server(port)