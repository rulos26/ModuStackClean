#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vista Home - ModuStackClean
Vista principal de la aplicación con diseño moderno y estructurado
"""

import flet as ft
from utils.ui_components import create_gradient_container, create_feature_card

class HomeView(ft.Container):
    """Vista principal de la aplicación"""
    
    def __init__(self, page: ft.Page, config, session_manager=None, on_logout=None):
        self.page = page
        self.config = config
        self.session_manager = session_manager
        self.on_logout = on_logout
        super().__init__(
            width=self.config.WINDOW_WIDTH,
            height=self.config.WINDOW_HEIGHT,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    # Header con gradiente
                    self._build_header(),
                    
                    # Contenido principal
                    self._build_main_content(),
                    
                    # Footer
                    self._build_footer()
                ]
            )
        )
    
    def _build_header(self):
        """Construir el header de la aplicación"""
        # Obtener información del usuario si está logueado
        user_info = None
        if self.session_manager and self.session_manager.is_logged_in():
            user_info = self.session_manager.get_current_user()
        
        return create_gradient_container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    # Barra superior con información del usuario
                    self._build_user_bar() if user_info else ft.Container(height=10),
                    
                    # Logo y título principal
                    ft.Container(
                        margin=ft.margin.only(top=20, bottom=20),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Text(
                                    "🚀",
                                    size=80,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    self.config.APP_TITLE,
                                    size=48,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    f"v{self.config.APP_VERSION}",
                                    size=16,
                                    color="white",
                                    weight=ft.FontWeight.W_500
                                )
                            ]
                        )
                    ),
                    
                    # Subtítulo personalizado
                    ft.Container(
                        margin=ft.margin.only(bottom=40),
                        content=ft.Text(
                            f"Bienvenido, {user_info.get('nombre', 'Usuario')}" if user_info else self.config.SUBTITLE_MESSAGE,
                            size=20,
                            color="white",
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_500
                        )
                    )
                ]
            )
        )
    
    def _build_user_bar(self):
        """Construir barra de información del usuario"""
        if not self.session_manager or not self.session_manager.is_logged_in():
            return ft.Container()
        
        user_info = self.session_manager.get_current_user()
        user_name = user_info.get('nombre', 'Usuario')
        user_email = user_info.get('correo', '')
        user_role = user_info.get('rol', 'usuario')
        
        return ft.Container(
            width=self.config.WINDOW_WIDTH - 40,
            margin=ft.margin.only(top=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # Información del usuario
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon("account_circle", color="white", size=24),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        user_name,
                                        color="white",
                                        size=14,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        f"{user_email} ({user_role})",
                                        color="white",
                                        size=10,
                                        opacity=0.8
                                    )
                                ]
                            )
                        ]
                    ),
                    # Botón de logout
                    ft.ElevatedButton(
                        text="Cerrar Sesión",
                        icon="logout",
                        style=ft.ButtonStyle(
                            bgcolor="red",
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=5)
                        ),
                        on_click=self._handle_logout
                    )
                ]
            )
        )
    
    def _handle_logout(self, e):
        """Manejar logout de usuario"""
        if self.session_manager:
            self.session_manager.logout()
        
        if self.on_logout:
            self.on_logout()
    
    def _build_main_content(self):
        """Construir el contenido principal"""
        return ft.Container(
            expand=True,
            bgcolor=self.config.BACKGROUND_COLOR,
            padding=ft.padding.all(40),
            content=ft.Column(
                expand=True,
                spacing=40,
                controls=[
                    # Título de características
                    ft.Container(
                        content=ft.Text(
                            self.config.FEATURES_TITLE,
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color="black",
                            text_align=ft.TextAlign.CENTER
                        )
                    ),
                    
                    # Grid de características
                    self._build_features_grid(),
                    
                    # Botón de comenzar
                    self._build_get_started_button()
                ]
            )
        )
    
    def _build_features_grid(self):
        """Construir el grid de características"""
        feature_cards = []
        
        for feature in self.config.FEATURES:
            card = create_feature_card(
                icon=feature["icon"],
                title=feature["title"],
                description=feature["description"],
                config=self.config
            )
            feature_cards.append(card)
        
        return ft.Container(
            content=ft.GridView(
                expand=True,
                runs_count=2,
                max_extent=300,
                spacing=20,
                run_spacing=20,
                controls=feature_cards
            )
        )
    
    def _build_get_started_button(self):
        """Construir el botón de comenzar"""
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.ElevatedButton(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Icon("play_arrow", color="white"),
                        ft.Text(
                            self.config.GET_STARTED_TEXT,
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="white"
                        )
                    ]
                ),
                style=ft.ButtonStyle(
                    bgcolor=self.config.PRIMARY_COLOR,
                    shape=ft.RoundedRectangleBorder(
                        radius=self.config.BUTTON_RADIUS
                    ),
                    padding=ft.padding.all(20)
                ),
                on_click=self._on_get_started_click
            )
        )
    
    def _build_footer(self):
        """Construir el footer de la aplicación"""
        return ft.Container(
            bgcolor="black",
            padding=ft.padding.all(20),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        self.config.COPYRIGHT,
                        size=14,
                        color="white",
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            )
        )
    
    def _on_get_started_click(self, e):
        """Manejar el clic del botón comenzar"""
        # Aquí puedes agregar la lógica para navegar a la siguiente vista
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("¡Bienvenido a ModuStackClean!"),
                action="OK"
            )
        )
