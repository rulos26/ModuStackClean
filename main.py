#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ModuStackClean - Aplicación Flet
Aplicación principal con sistema de login y gestión de base de datos
"""

import flet as ft
from views.home_view import HomeView
from views.login_view import LoginView
from config.app_config import AppConfig
from config.database_manager import DatabaseManager
from utils.session_manager import SessionManager

class ModuStackCleanApp:
    def __init__(self):
        self.config = AppConfig()
        self.db_manager = DatabaseManager()
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
        page.window_resizable = False
        page.padding = 0
        page.spacing = 0
        
        # Mostrar información de conexión
        self.show_connection_status()
        
        # Verificar si hay usuario logueado
        if self.session_manager.is_logged_in():
            self.show_home_view()
        else:
            self.show_login_view()
    
    def show_connection_status(self):
        """Mostrar estado de conexión a base de datos"""
        if self.db_manager.is_connected():
            connection_info = self.db_manager.get_connection_info()
            db_type = "Remota" if connection_info["type"] == "remote" else "Local"
            print(f"✅ Conectado a base de datos {db_type}")
        else:
            print("❌ Sin conexión a base de datos")
    
    def show_login_view(self):
        """Mostrar vista de login"""
        self.current_page.clean()
        login_view = LoginView(
            self.current_page,
            self.config,
            self.db_manager,
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

def main():
    """Punto de entrada de la aplicación"""
    app = ModuStackCleanApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()