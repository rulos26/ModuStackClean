#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager - ModuStackClean
Gestor de base de datos con fallback automático entre local y remota
"""

import sys
import os
from typing import Optional, Tuple

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database_config import DatabaseConfig
from config.database_config_local import DatabaseConfigLocal
from models.usuario_model import UsuarioModel

class DatabaseManager:
    """Gestor de base de datos con fallback automático"""
    
    def __init__(self):
        self.remote_config = DatabaseConfig()
        self.local_config = DatabaseConfigLocal()
        self.current_config = None
        self.usuario_model = None
        self.connection_type = None
        
        # Intentar conectar automáticamente
        self.initialize_connection()
    
    def test_remote_connection(self) -> bool:
        """Probar conexión remota sin mostrar errores"""
        try:
            return self.remote_config.test_connection()
        except Exception:
            return False
    
    def test_local_connection(self) -> bool:
        """Probar conexión local sin mostrar errores"""
        try:
            return self.local_config.test_connection()
        except Exception:
            return False
    
    def initialize_connection(self) -> Tuple[bool, str]:
        """Inicializar conexión con fallback automático"""
        print("🔗 Inicializando conexión a base de datos...")
        
        # Intentar conexión remota primero
        print("1️⃣ Probando conexión remota...")
        if self.test_remote_connection():
            self.current_config = self.remote_config
            self.connection_type = "remote"
            self.usuario_model = UsuarioModel(self.current_config)
            print("✅ Conectado a base de datos REMOTA")
            return True, "Conectado a base de datos remota"
        else:
            print("⚠️ Base de datos remota no disponible")
        
        # Fallback a conexión local
        print("2️⃣ Probando conexión local (fallback)...")
        if self.test_local_connection():
            self.current_config = self.local_config
            self.connection_type = "local"
            self.usuario_model = UsuarioModel(self.current_config)
            print("✅ Conectado a base de datos LOCAL")
            return True, "Conectado a base de datos local"
        else:
            print("❌ No se pudo conectar a ninguna base de datos")
        
        return False, "No se pudo conectar a ninguna base de datos"
    
    def get_connection_info(self) -> dict:
        """Obtener información de la conexión actual"""
        if not self.current_config:
            return {"status": "disconnected", "type": None}
        
        info = self.current_config.get_connection_info()
        info["status"] = "connected"
        info["type"] = self.connection_type
        return info
    
    def is_connected(self) -> bool:
        """Verificar si hay conexión activa"""
        return self.current_config is not None and self.usuario_model is not None
    
    def reconnect(self) -> Tuple[bool, str]:
        """Intentar reconectar a las bases de datos"""
        print("🔄 Intentando reconectar...")
        self.current_config = None
        self.usuario_model = None
        self.connection_type = None
        return self.initialize_connection()
    
    def create_usuario(self, nombre: str, correo: str, password: str, rol: str = 'usuario') -> Tuple[bool, str, Optional[int]]:
        """Crear usuario usando la conexión activa"""
        if not self.is_connected():
            return False, "No hay conexión a base de datos", None
        
        return self.usuario_model.create_usuario(nombre, correo, password, rol)
    
    def login_usuario(self, correo: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """Autenticar usuario usando la conexión activa"""
        if not self.is_connected():
            return False, "No hay conexión a base de datos", None
        
        return self.usuario_model.login_usuario(correo, password)
    
    def get_usuario_by_id(self, user_id: int) -> Tuple[bool, str, Optional[dict]]:
        """Obtener usuario por ID usando la conexión activa"""
        if not self.is_connected():
            return False, "No hay conexión a base de datos", None
        
        return self.usuario_model.get_usuario_by_id(user_id)
    
    def get_all_usuarios(self) -> Tuple[bool, str, list]:
        """Obtener todos los usuarios usando la conexión activa"""
        if not self.is_connected():
            return False, "No hay conexión a base de datos", []
        
        return self.usuario_model.get_all_usuarios()
    
    def update_usuario(self, user_id: int, **kwargs) -> Tuple[bool, str]:
        """Actualizar usuario usando la conexión activa"""
        if not self.is_connected():
            return False, "No hay conexión a base de datos"
        
        return self.usuario_model.update_usuario(user_id, **kwargs)
    
    def delete_usuario(self, user_id: int) -> Tuple[bool, str]:
        """Eliminar usuario usando la conexión activa"""
        if not self.is_connected():
            return False, "No hay conexión a base de datos"
        
        return self.usuario_model.delete_usuario(user_id)
    
    def count_usuarios(self) -> Tuple[bool, str, int]:
        """Contar usuarios usando la conexión activa"""
        if not self.is_connected():
            return False, "No hay conexión a base de datos", 0
        
        return self.usuario_model.count_usuarios()
