#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Componentes de UI - ModuStackClean
Componentes reutilizables para la interfaz de usuario
"""

import flet as ft

def create_gradient_container(content, height=None, **kwargs):
    """Crear un contenedor con gradiente de fondo"""
    container_kwargs = {
        "gradient": ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                "#4facfe",
                "#00f2fe"
            ]
        ),
        "padding": ft.padding.all(40),
        "content": content
    }
    
    # Agregar altura si se especifica
    if height is not None:
        container_kwargs["height"] = height
    
    # Agregar otros parámetros si se proporcionan
    container_kwargs.update(kwargs)
    
    return ft.Container(**container_kwargs)

def create_feature_card(icon, title, description, config):
    """Crear una tarjeta de característica"""
    return ft.Card(
        elevation=8,
        shape=ft.RoundedRectangleBorder(
            radius=config.CARD_RADIUS
        ),
        content=ft.Container(
            padding=ft.padding.all(24),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    # Icono
                    ft.Container(
                        width=80,
                        height=80,
                        border_radius=40,
                        bgcolor=config.PRIMARY_COLOR,
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            icon,
                            size=40,
                            color="white"
                        )
                    ),
                    
                    # Título
                    ft.Text(
                        title,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="black",
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                    # Descripción
                    ft.Text(
                        description,
                        size=14,
                        color="gray",
                        text_align=ft.TextAlign.CENTER,
                        max_lines=3,
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
                ]
            )
        )
    )

def create_info_card(title, content, icon=None, config=None):
    """Crear una tarjeta de información"""
    controls = []
    
    if icon:
        controls.append(
            ft.Icon(
                icon,
                size=24,
                color=config.PRIMARY_COLOR if config else "blue"
            )
        )
    
    controls.extend([
        ft.Text(
            title,
            size=16,
            weight=ft.FontWeight.BOLD,
            color="black"
        ),
        ft.Text(
            content,
            size=14,
            color="gray"
        )
    ])
    
    return ft.Card(
        elevation=4,
        shape=ft.RoundedRectangleBorder(
            radius=8
        ),
        content=ft.Container(
            padding=ft.padding.all(16),
            content=ft.Column(
                spacing=8,
                controls=controls
            )
        )
    )

def create_action_button(text, icon, on_click, config, color=None):
    """Crear un botón de acción"""
    return ft.ElevatedButton(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(icon, color="white"),
                ft.Text(
                    text,
                    color="white",
                    weight=ft.FontWeight.W_500
                )
            ]
        ),
        style=ft.ButtonStyle(
            bgcolor=color or config.PRIMARY_COLOR,
            shape=ft.RoundedRectangleBorder(
                radius=config.BUTTON_RADIUS
            ),
            padding=ft.padding.all(16)
        ),
        on_click=on_click
    )

def create_status_indicator(status, text):
    """Crear un indicador de estado"""
    color = "green" if status else "red"
    icon = "check_circle" if status else "error"
    
    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
        controls=[
            ft.Icon(
                icon,
                color=color,
                size=20
            ),
            ft.Text(
                text,
                color=color,
                weight=ft.FontWeight.W_500
            )
        ]
    )
