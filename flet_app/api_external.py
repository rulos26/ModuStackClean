#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Externa - ModuStackClean
API para conectar con servicios externos de RuloSoluciones
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

class ExternalAPI:
    """API para conectar con servicios externos"""
    
    def __init__(self):
        self.base_url = "https://rulossoluciones.com/ModuStackClean"
        self.timeout = 10
        self.headers = {
            'User-Agent': 'ModuStackClean/1.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def get_prueba_data(self) -> Dict[str, Any]:
        """Obtener datos de prueba desde la API externa"""
        try:
            url = f"{self.base_url}/prueba.json"
            print(f"🔗 Conectando a: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Datos obtenidos exitosamente")
                return {
                    "success": True,
                    "data": data,
                    "status_code": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "status_code": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
                
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión")
            return {
                "success": False,
                "error": "Error de conexión",
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.Timeout:
            print("❌ Timeout de conexión")
            return {
                "success": False,
                "error": "Timeout de conexión",
                "timestamp": datetime.now().isoformat()
            }
        except json.JSONDecodeError:
            print("❌ Error decodificando JSON")
            return {
                "success": False,
                "error": "Error decodificando JSON",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """Probar conexión a la API externa"""
        print("🧪 Probando conexión a API externa...")
        
        # Test 1: Conectividad básica
        try:
            response = requests.get(self.base_url, timeout=5)
            connectivity = response.status_code < 400
        except:
            connectivity = False
        
        # Test 2: Obtener datos de prueba
        prueba_data = self.get_prueba_data()
        
        return {
            "connectivity": connectivity,
            "prueba_endpoint": prueba_data,
            "base_url": self.base_url,
            "timestamp": datetime.now().isoformat()
        }

# Instancia global
external_api = ExternalAPI()
