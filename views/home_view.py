#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vista Home - ModuStackClean
Vista principal con diseño moderno, profesional y responsive
"""

import flet as ft
from utils.ui_components import create_gradient_container

class HomeView(ft.Container):
    """Vista principal con menú lateral y diseño moderno"""
    
    def __init__(self, page: ft.Page, config, session_manager=None, on_logout=None, on_navigate_to_path=None):
        self.page = page
        self.config = config
        self.session_manager = session_manager
        self.on_logout = on_logout
        self.on_navigate_to_path = on_navigate_to_path
        self.current_user = None
        
        # Obtener información del usuario
        if self.session_manager and self.session_manager.is_logged_in():
            self.current_user = self.session_manager.get_current_user()
        
        # Estado del menú lateral
        self.sidebar_expanded = True
        
        # Componentes del menú lateral
        self.sidebar = self._build_sidebar()
        self.main_content = self._build_main_content()
        
        super().__init__(
            width=self.config.WINDOW_WIDTH,
            height=self.config.WINDOW_HEIGHT,
            content=ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    # Menú lateral
                    self.sidebar,
                    
                    # Contenido principal
                    self.main_content
                ]
            )
        )
    
    def _build_sidebar(self):
        """Construir menú lateral responsive"""
        return ft.Container(
            width=280 if self.sidebar_expanded else 70,
            bgcolor="#1a1a1a",
            border=ft.border.only(right=ft.border.BorderSide(1, "#333333")),
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    # Header del sidebar
                    self._build_sidebar_header(),
                    
                    # Menú de navegación
                    self._build_navigation_menu(),
                    
                    # Footer del sidebar
                    self._build_sidebar_footer()
                ]
            )
        )
    
    def _build_sidebar_header(self):
        """Construir header del sidebar"""
        return ft.Container(
            height=80,
            bgcolor="#2d2d2d",
            padding=ft.padding.all(20),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # Logo y título
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Icon(
                                "dashboard",
                                color="white",
                                size=30
                            ),
                            ft.Text(
                                "ModuStack" if self.sidebar_expanded else "",
                                color="white",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            )
                        ]
                    ),
                    
                    # Botón toggle sidebar
                    ft.IconButton(
                        icon="menu" if self.sidebar_expanded else "menu_open",
                        icon_color="white",
                        on_click=self._toggle_sidebar
                    )
                ]
            )
        )
    
    def _build_navigation_menu(self):
        """Construir menú de navegación"""
        menu_items = [
            {
                "icon": "home",
                "label": "Inicio",
                "active": True,
                "on_click": self._on_menu_item_click
            },
            {
                "icon": "folder",
                "label": "Path",
                "active": False,
                "on_click": self._on_menu_item_click
            },
            {
                "icon": "settings",
                "label": "Configuración",
                "active": False,
                "on_click": self._on_menu_item_click
            },
            {
                "icon": "analytics",
                "label": "Estadísticas",
                "active": False,
                "on_click": self._on_menu_item_click
            },
            {
                "icon": "help",
                "label": "Ayuda",
                "active": False,
                "on_click": self._on_menu_item_click
            }
        ]
        
        menu_controls = []
        for item in menu_items:
            menu_controls.append(
                ft.Container(
                    height=50,
                    bgcolor="#2d2d2d" if item["active"] else "transparent",
                    border=ft.border.only(
                        left=ft.border.BorderSide(3, "#4facfe" if item["active"] else "transparent")
                    ),
                    content=ft.ListTile(
                        leading=ft.Icon(
                            item["icon"],
                            color="#4facfe" if item["active"] else "white",
                            size=20
                        ),
                        title=ft.Text(
                            item["label"],
                            color="#4facfe" if item["active"] else "white",
                            size=14,
                            weight=ft.FontWeight.W_500
                        ) if self.sidebar_expanded else None,
                        on_click=item["on_click"],
                        data=item
                    )
                )
            )
        
        return ft.Container(
            expand=True,
            padding=ft.padding.only(top=20),
            content=ft.Column(
                spacing=5,
                controls=menu_controls
            )
        )
    
    def _build_sidebar_footer(self):
        """Construir footer del sidebar"""
        if not self.current_user:
            return ft.Container(height=0)
        
        return ft.Container(
            height=120,
            bgcolor="#2d2d2d",
            padding=ft.padding.all(15),
            content=ft.Column(
                spacing=10,
                controls=[
                    # Información del usuario
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.CircleAvatar(
                                content=ft.Text(
                                    self.current_user.get('nombre', 'U')[0].upper(),
                                    color="white",
                                    weight=ft.FontWeight.BOLD
                                ),
                                bgcolor="#4facfe",
                                radius=20
                            ),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        self.current_user.get('nombre', 'Usuario'),
                                        color="white",
                                        size=12,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        f"Rol: {self.current_user.get('rol', 'usuario').title()}",
                                        color="white",
                                        size=10,
                                        opacity=0.7
                                    ),
                                    ft.Text(
                                        self.current_user.get('correo', ''),
                                        color="white",
                                        size=9,
                                        opacity=0.6
                                    )
                                ]
                            ) if self.sidebar_expanded else ft.Container()
                        ]
                    ),
                    
                    # Botón de logout
                    ft.Container(
                        margin=ft.margin.only(top=5),
                        content=ft.ElevatedButton(
                            text="Cerrar Sesión" if self.sidebar_expanded else "",
                            icon=ft.Icon("power_settings_new"),
                            style=ft.ButtonStyle(
                                bgcolor="#6c757d",
                                color="white",
                                shape=ft.RoundedRectangleBorder(radius=5)
                            ),
                            on_click=self._handle_logout
                        )
                    )
                ]
            )
        )
    
    def _build_main_content(self):
        """Construir contenido principal"""
        return ft.Container(
            expand=True,
            bgcolor="#f8f9fa",
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    # Header principal
                    self._build_main_header(),
                    
                    # Contenido del dashboard
                    self._build_dashboard_content(),
                    
                    # Footer principal
                    self._build_main_footer()
                ]
            )
        )
    
    def _build_main_header(self):
        """Construir header principal"""
        return ft.Container(
            height=80,
            bgcolor="white",
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#e9ecef")),
            padding=ft.padding.all(20),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # Título de la página
                    ft.Text(
                        "Dashboard",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#2d2d2d"
                    ),
                    
                    # Información del usuario conectado
                    ft.Row(
                        spacing=15,
                        controls=[
                            # Información del usuario
                            ft.Container(
                                content=ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(
                                            f"Conectado como: {self.current_user.get('nombre', 'Usuario') if self.current_user else 'Invitado'}",
                                            size=12,
                                            color="#6c757d",
                                            weight=ft.FontWeight.W_500
                                        ),
                                        ft.Text(
                                            f"Rol: {self.current_user.get('rol', 'usuario').title() if self.current_user else 'N/A'}",
                                            size=10,
                                            color="#6c757d"
                                        )
                                    ]
                                )
                            ),
                            
                            # Botón de sesión/logout
                            ft.ElevatedButton(
                                text="Cerrar Sesión",
                                icon=ft.Icon("power_settings_new"),
                                style=ft.ButtonStyle(
                                    bgcolor="#6c757d",
                                    color="white",
                                    shape=ft.RoundedRectangleBorder(radius=5)
                                ),
                                on_click=self._handle_logout
                            )
                        ]
                    )
                ]
            )
        )
    
    def _build_dashboard_content(self):
        """Construir contenido del dashboard"""
        return ft.Container(
            expand=True,
            padding=ft.padding.all(30),
            content=ft.Column(
                expand=True,
                spacing=30,
                controls=[
                    # Contenido principal
                    self._build_welcome_section(),
                    
                    # Características del sistema
                    self._build_features_section()
                ]
            )
        )
    
    def _build_welcome_section(self):
        """Construir sección de bienvenida"""
        return ft.Container(
            bgcolor="white",
            border_radius=12,
            padding=ft.padding.all(30),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color="#00000010",
                offset=ft.Offset(0, 2)
            ),
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Text(
                        f"¡Bienvenido, {self.current_user.get('nombre', 'Usuario')}! 👋",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#2d2d2d"
                    ),
                    ft.Text(
                        "ModuStackClean está listo para ayudarte a organizar y gestionar tus archivos de manera eficiente. Comienza explorando las características disponibles.",
                        size=16,
                        color="#6c757d",
                        text_align=ft.TextAlign.START
                    ),
                    ft.ElevatedButton(
                        text="Comenzar",
                        icon=ft.Icon("play_arrow"),
                        style=ft.ButtonStyle(
                            bgcolor="#4facfe",
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                        on_click=self._on_get_started_click
                    )
                ]
            )
        )
    
    def _build_features_section(self):
        """Construir sección de características"""
        features = [
            {
                "icon": "🤖",
                "title": "Organización Automática",
                "description": "Organiza automáticamente tus archivos de descargas"
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
        
        feature_cards = []
        for feature in features:
            feature_cards.append(
                ft.Container(
                    expand=True,
                    bgcolor="white",
                    border_radius=12,
                    padding=ft.padding.all(25),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color="#00000010",
                        offset=ft.Offset(0, 2)
                    ),
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            ft.Text(
                                feature["icon"],
                                size=40
                            ),
                            ft.Text(
                                feature["title"],
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#2d2d2d"
                            ),
                            ft.Text(
                                feature["description"],
                                size=14,
                                color="#6c757d",
                                text_align=ft.TextAlign.START
                            )
                        ]
                    )
                )
            )
        
        return ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    "Características Principales",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#2d2d2d"
                ),
                ft.Row(
                    spacing=20,
                    controls=feature_cards
                )
            ]
        )
    
    def _build_main_footer(self):
        """Construir footer principal"""
        return ft.Container(
            height=60,
            bgcolor="white",
            border=ft.border.only(top=ft.border.BorderSide(1, "#e9ecef")),
            padding=ft.padding.all(20),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        self.config.COPYRIGHT,
                        size=12,
                        color="#6c757d",
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            )
        )
    
    def _toggle_sidebar(self, e):
        """Alternar estado del sidebar"""
        self.sidebar_expanded = not self.sidebar_expanded
        
        # Limpiar la página y reconstruir todo
        self.page.clean()
        
        # Reconstruir los componentes con el nuevo estado
        self.sidebar = self._build_sidebar()
        self.main_content = self._build_main_content()
        
        # Agregar los componentes reconstruidos
        self.page.add(
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    self.sidebar,
                    self.main_content
                ]
            )
        )
        
        # Actualizar la página
        self.page.update()
    
    def _on_menu_item_click(self, e):
        """Manejar clic en elementos del menú"""
        item = e.control.data
        
        if item["label"] == "Path" and self.on_navigate_to_path:
            self.on_navigate_to_path()
        else:
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Navegando a: {item['label']}"),
                    action="OK"
                )
            )
    
    def _handle_logout(self, e):
        """Manejar logout de usuario"""
        if self.session_manager:
            self.session_manager.logout()
        
        if self.on_logout:
            self.on_logout()
    
    def _on_get_started_click(self, e):
        """Manejar clic en botón comenzar"""
        if self.on_navigate_to_path:
            self.on_navigate_to_path()
    
    def update_responsive_layout(self):
        """Actualizar layout para ser responsive"""
        # Ajustar sidebar según el tamaño de la ventana
        if self.config.WINDOW_WIDTH < 1000:
            self.sidebar_expanded = False
        else:
            self.sidebar_expanded = True
        
        # Limpiar la página y reconstruir todo
        self.page.clean()
        
        # Reconstruir los componentes con el nuevo estado
        self.sidebar = self._build_sidebar()
        self.main_content = self._build_main_content()
        
        # Agregar los componentes reconstruidos
        self.page.add(
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    self.sidebar,
                    self.main_content
                ]
            )
        )
        
        if self.page:
            self.page.update()
