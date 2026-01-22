#!/usr/bin/env python3
"""
Servidor web simple para el frontend de ArcheoScope.
"""

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