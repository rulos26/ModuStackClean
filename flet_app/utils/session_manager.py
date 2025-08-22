#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Manager - ModuStackClean
Gestor de sesiones de usuario
"""

import json
from datetime import datetime, timedelta
from typing import Optional, Dict

class SessionManager:
    """Gestor de sesiones de usuario"""
    
    def __init__(self):
        self.current_user = None
        self.login_time = None
        self.session_timeout = timedelta(hours=24)  # 24 horas de sesión
    
    def login(self, usuario: Dict) -> bool:
        """Iniciar sesión de usuario"""
        try:
            self.current_user = usuario.copy()
            self.login_time = datetime.now()
            
            # Remover información sensible
            if 'password' in self.current_user:
                del self.current_user['password']
            
            print(f"✅ Sesión iniciada para: {self.current_user.get('nombre', 'Usuario')}")
            return True
        except Exception as e:
            print(f"❌ Error iniciando sesión: {e}")
            return False
    
    def logout(self) -> bool:
        """Cerrar sesión de usuario"""
        try:
            if self.current_user:
                nombre = self.current_user.get('nombre', 'Usuario')
                print(f"👋 Sesión cerrada para: {nombre}")
            
            self.current_user = None
            self.login_time = None
            return True
        except Exception as e:
            print(f"❌ Error cerrando sesión: {e}")
            return False
    
    def is_logged_in(self) -> bool:
        """Verificar si hay un usuario logueado"""
        if not self.current_user or not self.login_time:
            return False
        
        # Verificar si la sesión ha expirado
        if datetime.now() - self.login_time > self.session_timeout:
            print("⏰ Sesión expirada")
            self.logout()
            return False
        
        return True
    
    def get_current_user(self) -> Optional[Dict]:
        """Obtener usuario actual si está logueado"""
        if self.is_logged_in():
            return self.current_user.copy()
        return None
    
    def get_user_id(self) -> Optional[int]:
        """Obtener ID del usuario actual"""
        if self.is_logged_in():
            return self.current_user.get('id')
        return None
    
    def get_user_name(self) -> Optional[str]:
        """Obtener nombre del usuario actual"""
        if self.is_logged_in():
            return self.current_user.get('nombre')
        return None
    
    def get_user_email(self) -> Optional[str]:
        """Obtener email del usuario actual"""
        if self.is_logged_in():
            return self.current_user.get('correo')
        return None
    
    def get_user_role(self) -> Optional[str]:
        """Obtener rol del usuario actual"""
        if self.is_logged_in():
            return self.current_user.get('rol')
        return None
    
    def is_admin(self) -> bool:
        """Verificar si el usuario actual es administrador"""
        if self.is_logged_in():
            return self.current_user.get('rol') == 'admin'
        return False
    
    def update_user_info(self, usuario: Dict) -> bool:
        """Actualizar información del usuario en sesión"""
        try:
            if self.is_logged_in():
                # Mantener información de sesión
                login_time = self.login_time
                
                # Actualizar información del usuario
                self.current_user = usuario.copy()
                
                # Remover información sensible
                if 'password' in self.current_user:
                    del self.current_user['password']
                
                # Restaurar tiempo de login
                self.login_time = login_time
                
                return True
            return False
        except Exception as e:
            print(f"❌ Error actualizando información de usuario: {e}")
            return False
    
    def get_session_info(self) -> Dict:
        """Obtener información de la sesión actual"""
        if not self.is_logged_in():
            return {
                'logged_in': False,
                'user': None,
                'login_time': None,
                'session_duration': None
            }
        
        session_duration = datetime.now() - self.login_time
        
        return {
            'logged_in': True,
            'user': self.current_user.copy(),
            'login_time': self.login_time.isoformat(),
            'session_duration': str(session_duration).split('.')[0],  # Sin microsegundos
            'expires_at': (self.login_time + self.session_timeout).isoformat()
        }
    
    def extend_session(self) -> bool:
        """Extender la sesión actual"""
        try:
            if self.is_logged_in():
                self.login_time = datetime.now()
                print("🔄 Sesión extendida")
                return True
            return False
        except Exception as e:
            print(f"❌ Error extendiendo sesión: {e}")
            return False
