#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de la aplicación ModuStackClean
"""

class AppConfig:
    """Clase de configuración de la aplicación"""
    
    def __init__(self):
        # Información de la aplicación
        self.APP_TITLE = "ModuStackClean"
        self.APP_VERSION = "1.0"
        self.APP_DESCRIPTION = "Sistema de Organización y Gestión de Archivos"
        self.COPYRIGHT = "© 2025 RuloSoluciones. Todos los derechos reservados."
        
        # Colores del tema
        self.PRIMARY_COLOR = "#4facfe"
        self.SECONDARY_COLOR = "#00f2fe"
        self.ACCENT_COLOR = "#667eea"
        self.BACKGROUND_COLOR = "#f8f9fa"
        self.SURFACE_COLOR = "#ffffff"
        
        # Configuración de la interfaz
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 800
        self.WINDOW_MIN_WIDTH = 800
        self.WINDOW_MIN_HEIGHT = 600
        self.CARD_RADIUS = 12
        self.BUTTON_RADIUS = 8
        
        # Textos de la aplicación
        self.WELCOME_MESSAGE = "Bienvenido a ModuStackClean"
        self.SUBTITLE_MESSAGE = "Sistema de Organización y Gestión de Archivos"
        self.FEATURES_TITLE = "Características Principales"
        self.GET_STARTED_TEXT = "Comenzar"
        
        # Características del sistema
        self.FEATURES = [
            {
                "icon": "📁",
                "title": "Organización Automática",
                "description": "Organiza automáticamente tus archivos de descargas"
            },
            {
                "icon": "🤖",
                "title": "Detección Inteligente",
                "description": "Detecta y clasifica archivos de manera inteligente"
            },
            {
                "icon": "⚡",
                "title": "Rendimiento Optimizado",
                "description": "Procesamiento rápido y eficiente de archivos"
            },
            {
                "icon": "🛡️",
                "title": "Seguridad Garantizada",
                "description": "Mantén tus archivos seguros y organizados"
            }
        ]
