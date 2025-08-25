#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ModuStackClean - Aplicación Principal
Sistema de gestión y organización de archivos
"""

import flet as ft
from config.app_config import AppConfig
from config.api_manager import APIManager
from utils.session_manager import SessionManager
from views.login_view import LoginView
from views.home_view import HomeView
from views.path_view import PathView

class ModuStackCleanApp:
    """Aplicación principal ModuStackClean"""
    
    def __init__(self):
        self.config = AppConfig()
        self.api_manager = APIManager()
        self.session_manager = SessionManager()
        self.current_page = None
        self.current_view = None
    
    def main(self, page: ft.Page):
        """Configurar y ejecutar la aplicación principal"""
        self.current_page = page
        
        # Configuración de la página
        page.title = self.config.APP_TITLE
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = self.config.WINDOW_WIDTH
        page.window_height = self.config.WINDOW_HEIGHT
        page.window_resizable = True
        page.window_min_width = self.config.WINDOW_MIN_WIDTH
        page.window_min_height = self.config.WINDOW_MIN_HEIGHT
        page.padding = 0
        page.spacing = 0
        
        # Agregar listener para cambios de tamaño de ventana
        page.on_resize = self.on_window_resize
        
        # Mostrar vista de login inicialmente
        self.show_login_view()
        
        # Ejecutar la aplicación
        page.update()
    
    def show_login_view(self, e=None):
        """Mostrar vista de login"""
        self.current_view = LoginView(
            page=self.current_page,
            config=self.config,
            api_manager=self.api_manager,
            session_manager=self.session_manager,
            on_login_success=self.show_home_view
        )
        
        self.current_page.clean()
        self.current_page.add(self.current_view)
        self.current_page.update()
    
    def show_home_view(self, e=None):
        """Mostrar vista principal"""
        self.current_view = HomeView(
            page=self.current_page,
            config=self.config,
            session_manager=self.session_manager,
            on_logout=self.show_login_view,
            on_navigate_to_path=self.show_path_view
        )
        
        self.current_page.clean()
        self.current_page.add(self.current_view)
        self.current_page.update()
    
    def show_path_view(self, e=None):
        """Mostrar vista de paths"""
        self.current_view = PathView(
            page=self.current_page,
            config=self.config,
            session_manager=self.session_manager,
            on_logout=self.show_login_view,
            on_back=self.show_home_view
        )
        
        self.current_page.clean()
        self.current_page.add(self.current_view)
        self.current_page.update()
    
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
        
        # Actualizar vista actual específicamente
        if hasattr(self, 'current_view') and self.current_view:
            if hasattr(self.current_view, 'update_responsive_layout'):
                self.current_view.update_responsive_layout()
        
        print(f"🔄 Ventana redimensionada a: {e.width}x{e.height}")

def main():
    """Función principal de la aplicación"""
    app = ModuStackCleanApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()