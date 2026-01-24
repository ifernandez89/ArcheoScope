#!/usr/bin/env python3
"""
Backend ArcheoScope con CORS forzado
Versión simplificada para asegurar CORS funcione
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ArcheoScope - CORS Fixed")

# CORS middleware FORZADO y simplificado
class ForceCORS(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Headers CORS explícitos para TODAS las respuestas
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept, Origin, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "false"
        response.headers["Access-Control-Max-Age"] = "86400"
        
        # Log para debug
        origin = request.headers.get("origin", "unknown")
        logger.info(f"CORS: Request from {origin} - Headers aplicados")
        
        # Manejar preflight
        if request.method == "OPTIONS":
            logger.info("CORS: Preflight request")
            return response
        
        return response

# Aplicar CORS FORZADO primero
app.add_middleware(ForceCORS)

# Middleware CORS estándar como doble seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    allow_credentials=False
)

@app.get("/")
async def root():
    return {"message": "ArcheoScope CORS Fixed - Test endpoint"}

@app.get("/status")
async def status():
    return {
        "backend_status": "operational",
        "cors_status": "FORCED_ENABLED",
        "test_mode": True
    }

@app.post("/analyze")
async def analyze_endpoint(request):
    logger.info(f"Analyze endpoint called from {request.headers.get('origin', 'unknown')}")
    
    try:
        data = await request.json()
        logger.info(f"Analysis data received: {data.get('region_name', 'unknown')}")
        
        # Respuesta con headers CORS forzados
        return {
            "analysis_id": "test_cors_fixed",
            "status": "success",
            "message": "CORS test successful",
            "cors_headers_applied": True,
            "received_data": {
                "region_name": data.get("region_name"),
                "coordinates": {
                    "lat_min": data.get("lat_min"),
                    "lat_max": data.get("lat_max"),
                    "lon_min": data.get("lon_min"),
                    "lon_max": data.get("lon_max")
                }
            }
        }
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {e}")
        return {
            "analysis_id": "error",
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    print("Iniciando ArcheoScope CORS FORZADO")
    print("Backend corriendo en: http://localhost:8002")
    print("CORS headers forzados para TODAS las respuestas")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,
        log_level="info",
        access_log=True
    )