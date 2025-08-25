#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Manager - ModuStackClean
Gestor de API con fallback automático a modo offline
"""

import requests
import json
from typing import Optional, Tuple, Dict, Any
from datetime import datetime

class APIManager:
    """Gestor de API con fallback automático"""
    
    def __init__(self):
        self.api_base_url = "https://rulossoluciones.com/modustackclean"
        self.timeout = 10
        self.session = requests.Session()
        self.connection_status = "unknown"
        
        # Probar conexión al inicializar
        self.test_connection()
    
    def test_connection(self) -> bool:
        """Probar conexión a la API"""
        try:
            response = self.session.get(f"{self.api_base_url}/api/ping", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and data.get('mensaje') == 'pong':
                    self.connection_status = "connected"
                    print("✅ API conectada exitosamente")
                    return True
        except Exception as e:
            print(f"❌ Error conectando a API: {str(e)[:50]}")
        
        self.connection_status = "disconnected"
        print("❌ API no disponible - Modo offline activado")
        return False
    
    def is_connected(self) -> bool:
        """Verificar si hay conexión a la API"""
        return self.connection_status == "connected"
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Obtener información de la conexión"""
        if self.is_connected():
            return {
                "status": "connected",
                "type": "api",
                "url": self.api_base_url,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "disconnected",
                "type": "offline",
                "url": None,
                "timestamp": datetime.now().isoformat()
            }
    
    def make_api_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Tuple[bool, str, Optional[Dict]]:
        """Realizar petición a la API"""
        if not self.is_connected():
            return False, "API no disponible", None
        
        try:
            url = f"{self.api_base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = self.session.get(url, timeout=self.timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=self.timeout)
            else:
                return False, f"Método {method} no soportado", None
            
            if response.status_code == 200:
                try:
                    api_data = response.json()
                    if api_data.get('ok'):
                        return True, api_data.get('mensaje', 'Operación exitosa'), api_data.get('data')
                    else:
                        return False, api_data.get('mensaje', 'Error en la API'), None
                except json.JSONDecodeError:
                    return False, "Respuesta JSON inválida", None
            else:
                return False, f"Error HTTP {response.status_code}", None
                
        except requests.RequestException as e:
            return False, f"Error de conexión: {str(e)}", None
        except Exception as e:
            return False, f"Error inesperado: {str(e)}", None
    
    def login_usuario(self, correo: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Autenticar usuario a través de la API"""
        if not self.is_connected():
            return False, "API no disponible - Usa 'root'/'root' para acceso offline", None
        
        try:
            # Usar el endpoint de login
            login_data = {
                'correo': correo,
                'password': password
            }
            
            success, message, data = self.make_api_request("/api/login", method="POST", data=login_data)
            
            if success and data:
                usuario = data.get('usuario')
                if usuario:
                    return True, "Login exitoso", usuario
                else:
                    return False, "Datos de usuario no válidos", None
            else:
                return False, message, None
                
        except Exception as e:
            return False, f"Error en login: {str(e)}", None
    
    def create_usuario(self, nombre: str, correo: str, password: str, rol: str = 'usuario') -> Tuple[bool, str, Optional[int]]:
        """Crear usuario a través de la API"""
        if not self.is_connected():
            return False, "API no disponible", None
        
        # Por ahora, como la API no tiene endpoint de creación, simulamos
        # En una implementación real, agregarías el endpoint en la API PHP
        return False, "Endpoint de creación no implementado en la API", None
    
    def get_all_usuarios(self) -> Tuple[bool, str, list]:
        """Obtener todos los usuarios de la API"""
        success, message, data = self.make_api_request("/api/usuarios")
        
        if success and data:
            return True, "Usuarios obtenidos exitosamente", data.get('usuarios', [])
        else:
            return False, f"Error obteniendo usuarios: {message}", []
    
    def get_usuario_by_id(self, user_id: int) -> Tuple[bool, str, Optional[Dict]]:
        """Obtener usuario por ID de la API"""
        success, message, data = self.make_api_request("/api/usuarios")
        
        if success and data:
            usuarios = data.get('usuarios', [])
            for usuario in usuarios:
                if usuario.get('id') == user_id:
                    return True, "Usuario encontrado", usuario
            
            return False, "Usuario no encontrado", None
        else:
            return False, f"Error obteniendo usuarios: {message}", None
    
    def count_usuarios(self) -> Tuple[bool, str, int]:
        """Contar usuarios de la API"""
        success, message, data = self.make_api_request("/api/usuarios")
        
        if success and data:
            count = data.get('count', 0)
            return True, "Conteo exitoso", count
        else:
            return False, f"Error contando usuarios: {message}", 0
    
    def test_database_connection(self) -> Tuple[bool, str]:
        """Probar conexión a la base de datos a través de la API"""
        success, message, data = self.make_api_request("/api/prueba")
        
        if success:
            return True, "Conexión a base de datos exitosa"
        else:
            return False, f"Error de conexión a BD: {message}"
    
    def get_health_status(self) -> Tuple[bool, str, Optional[Dict]]:
        """Obtener estado de salud de la API"""
        return self.make_api_request("/api/health")
    
    def get_api_info(self) -> Tuple[bool, str, Optional[Dict]]:
        """Obtener información de la API"""
        return self.make_api_request("/api/info")
