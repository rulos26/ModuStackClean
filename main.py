#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ModuStackClean - Aplicación Flet
Aplicación principal con sistema de login y gestión de API
"""

import flet as ft
from views.home_view import HomeView
from views.login_view import LoginView
from config.app_config import AppConfig
from config.api_manager import APIManager
from utils.session_manager import SessionManager

class ModuStackCleanApp:
    def __init__(self):
        self.config = AppConfig()
        self.api_manager = APIManager()
        self.session_manager = SessionManager()
        self.current_page = None
        
    def main(self, page: ft.Page):
        self.current_page = page
        
        # Configurar página
        page.title = self.config.APP_TITLE
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = ft.Theme(
            color_scheme_seed="blue",
            use_material3=True,
        )
        page.window_width = self.config.WINDOW_WIDTH
        page.window_height = self.config.WINDOW_HEIGHT
        page.window_resizable = True
        page.window_min_width = self.config.WINDOW_MIN_WIDTH
        page.window_min_height = self.config.WINDOW_MIN_HEIGHT
        page.padding = 0
        page.spacing = 0
        
        # Agregar listener para cambios de tamaño de ventana
        page.on_resize = self.on_window_resize
        
        # Mostrar información de conexión
        self.show_connection_status()
        
        # Verificar si hay usuario logueado
        if self.session_manager.is_logged_in():
            self.show_home_view()
        else:
            self.show_login_view()
    
    def show_connection_status(self):
        """Mostrar estado de conexión a la API"""
        if self.api_manager.is_connected():
            connection_info = self.api_manager.get_connection_info()
            print(f"✅ Conectado a API: {connection_info['url']}")
        else:
            print("❌ Sin conexión a API - Modo offline activado")
    
    def show_login_view(self):
        """Mostrar vista de login"""
        self.current_page.clean()
        login_view = LoginView(
            self.current_page,
            self.config,
            self.api_manager,
            self.session_manager,
            on_login_success=self.on_login_success
        )
        self.current_page.add(login_view)
        self.current_page.update()
    
    def show_home_view(self):
        """Mostrar vista home"""
        self.current_page.clean()
        home_view = HomeView(
            self.current_page,
            self.config,
            self.session_manager,
            on_logout=self.on_logout
        )
        self.current_page.add(home_view)
        self.current_page.update()
    
    def on_login_success(self, usuario):
        """Callback cuando el login es exitoso"""
        print(f"🎉 Login exitoso para: {usuario.get('nombre', 'Usuario')}")
        # Esperar un momento para mostrar el mensaje de éxito
        import time
        time.sleep(1)
        self.show_home_view()
    
    def on_logout(self):
        """Callback cuando se hace logout"""
        print("👋 Logout realizado")
        self.show_login_view()
    
    def on_window_resize(self, e):
        """Manejar cambio de tamaño de ventana"""
        # Actualizar configuración con nuevo tamaño
        self.config.WINDOW_WIDTH = e.width
        self.config.WINDOW_HEIGHT = e.height
        
        # Actualizar layout responsive si es necesario
        if hasattr(self.current_page, 'controls') and self.current_page.controls:
            for control in self.current_page.controls:
                if hasattr(control, 'update_responsive_layout'):
                    control.update_responsive_layout()
        
        # Actualizar vista home específicamente
        if hasattr(self, 'current_page') and self.current_page:
            for control in self.current_page.controls:
                if hasattr(control, 'update_responsive_layout'):
                    control.update_responsive_layout()
        
        print(f"🔄 Ventana redimensionada a: {e.width}x{e.height}")

def main():
    """Punto de entrada de la aplicación"""
    app = ModuStackCleanApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()