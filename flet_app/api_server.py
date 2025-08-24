#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor API REST - ModuStackClean
Servidor FastAPI para exponer endpoints de API externa
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
from datetime import datetime

# Importar la API externa
from api_external import ExternalAPI

# Crear aplicación FastAPI
app = FastAPI(
    title="ModuStackClean API",
    description="API para conectar con servicios externos de RuloSoluciones",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia de la API externa
external_api = ExternalAPI()

# Modelos Pydantic
class PruebaResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    timestamp: str

class TestResponse(BaseModel):
    connectivity: bool
    prueba_endpoint: Dict[str, Any]
    base_url: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    external_api_status: str

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "ModuStackClean API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "prueba": "/api/prueba",
            "test": "/api/test",
            "health": "/api/health",
            "docs": "/docs"
        }
    }

@app.get("/api/prueba", response_model=PruebaResponse, tags=["External API"])
async def get_prueba_data():
    """Obtener datos de prueba desde la API externa"""
    try:
        result = external_api.get_prueba_data()
        return PruebaResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test", response_model=TestResponse, tags=["External API"])
async def test_external_connection():
    """Probar conexión a la API externa"""
    try:
        result = external_api.test_connection()
        return TestResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Verificar estado de salud de la API"""
    try:
        # Probar conexión externa
        test_result = external_api.test_connection()
        external_status = "healthy" if test_result["connectivity"] else "unhealthy"
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            external_api_status=external_status
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            external_api_status="error"
        )

@app.get("/api/info", tags=["Info"])
async def get_api_info():
    """Obtener información de la API"""
    return {
        "name": "ModuStackClean API",
        "version": "1.0.0",
        "description": "API para conectar con servicios externos de RuloSoluciones",
        "base_url": external_api.base_url,
        "endpoints": {
            "prueba": {
                "url": "/api/prueba",
                "method": "GET",
                "description": "Obtener datos de prueba desde RuloSoluciones"
            },
            "test": {
                "url": "/api/test",
                "method": "GET",
                "description": "Probar conexión a la API externa"
            },
            "health": {
                "url": "/api/health",
                "method": "GET",
                "description": "Verificar estado de salud"
            }
        },
        "external_services": {
            "rulossoluciones": {
                "url": "https://rulossoluciones.com/ModuStackClean/prueba.json",
                "description": "API de prueba de RuloSoluciones"
            }
        },
        "timestamp": datetime.now().isoformat()
    }

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Iniciar el servidor API"""
    print("🚀 Iniciando servidor API ModuStackClean...")
    print(f"📋 Host: {host}")
    print(f"📋 Puerto: {port}")
    print(f"📋 URL: http://{host}:{port}")
    print(f"📋 Documentación: http://{host}:{port}/docs")
    print(f"📋 Endpoints disponibles:")
    print(f"   - GET /api/prueba - Obtener datos de prueba")
    print(f"   - GET /api/test - Probar conexión externa")
    print(f"   - GET /api/health - Estado de salud")
    print(f"   - GET /api/info - Información de la API")
    print("\n🔄 Servidor iniciado. Presiona Ctrl+C para detener.")
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
