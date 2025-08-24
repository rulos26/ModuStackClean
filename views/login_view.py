#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vista de Login - ModuStackClean
Vista de autenticación de usuarios
"""

import flet as ft
from utils.ui_components import create_gradient_container

class LoginView(ft.Container):
    """Vista de login de usuarios"""
    
    def __init__(self, page: ft.Page, config, api_manager, session_manager, on_login_success=None):
        self.page = page
        self.config = config
        self.api_manager = api_manager
        self.session_manager = session_manager
        self.on_login_success = on_login_success
        
        # Campos del formulario
        self.email_field = ft.TextField(
            label="Correo Electrónico",
            hint_text="Ingresa tu correo",
            prefix_icon="email",
            width=350,
            border_radius=10,
            filled=True,
            bgcolor="white",
            border_color="blue",
            focused_border_color="blue",
            keyboard_type=ft.KeyboardType.EMAIL
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            hint_text="Ingresa tu contraseña",
            prefix_icon="lock",
            width=350,
            border_radius=10,
            filled=True,
            bgcolor="white",
            border_color="blue",
            focused_border_color="blue",
            password=True,
            can_reveal_password=True
        )
        
        # Mensaje de estado
        self.status_message = ft.Text(
            "",
            color="red",
            size=14,
            text_align=ft.TextAlign.CENTER,
            width=350
        )
        
        # Botón de login
        self.login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            icon="login",
            width=350,
            height=50,
            style=ft.ButtonStyle(
                bgcolor="blue",
                color="white",
                elevation=5,
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=self.handle_login
        )
        
        # Botón de registro
        self.register_button = ft.TextButton(
            text="¿No tienes cuenta? Regístrate",
            width=350,
            style=ft.ButtonStyle(
                color="blue"
            ),
            on_click=self.show_register_form
        )
        
        # Información de conexión
        self.connection_info = ft.Text(
            "",
            color="gray",
            size=12,
            text_align=ft.TextAlign.CENTER,
            width=350
        )
        
        # Nota sobre super usuario
        self.super_user_note = ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
                controls=[
                    ft.Text(
                        "🔑 Acceso de Emergencia",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color="orange",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Usuario: root | Contraseña: root",
                        size=12,
                        color="gray",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Para uso cuando no hay conexión a BD",
                        size=10,
                        color="gray",
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            ),
            bgcolor="orange50",
            border_radius=8,
            padding=ft.padding.all(10),
            margin=ft.margin.only(top=10),
            visible=False  # Solo visible cuando no hay conexión
        )
        
        # Actualizar información de conexión
        self.update_connection_info()
        
        super().__init__(
            width=self.config.WINDOW_WIDTH,
            height=self.config.WINDOW_HEIGHT,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=0,
                controls=[
                    self._build_header(),
                    self._build_login_form(),
                    self._build_footer()
                ]
            )
        )
    
    def _build_header(self):
        """Construir header con gradiente"""
        return create_gradient_container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon("account_circle", size=80, color="white"),
                    ft.Text(
                        "Bienvenido a ModuStackClean",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Inicia sesión para continuar",
                        size=16,
                        color="white",
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            ),
            height=250
        )
    
    def _build_login_form(self):
        """Construir formulario de login"""
        return ft.Container(
            expand=True,
            bgcolor="white",
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                ft.Text(
                                    "Iniciar Sesión",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="black",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                self.email_field,
                                self.password_field,
                                self.status_message,
                                self.login_button,
                                self.register_button,
                                ft.Divider(height=1, color="gray"),
                                self.connection_info,
                                self.super_user_note
                            ]
                        ),
                        padding=ft.padding.all(30),
                        bgcolor="white",
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color="gray",
                            offset=ft.Offset(0, 2)
                        ),
                        width=450
                    )
                ]
            )
        )
    
    def _build_footer(self):
        """Construir footer"""
        return ft.Container(
            height=60,
            bgcolor="black",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        self.config.COPYRIGHT,
                        color="white",
                        size=12,
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            )
        )
    
    def update_connection_info(self):
        """Actualizar información de conexión"""
        try:
            info = self.api_manager.get_connection_info()
            if info["status"] == "connected":
                self.connection_info.value = f"🔗 Conectado a API ({info['url']})"
                self.connection_info.color = "green"
                self.super_user_note.visible = False  # Ocultar nota cuando hay conexión
            else:
                self.connection_info.value = "❌ Sin conexión a API - 💡 Usa 'root' / 'root' para acceso offline"
                self.connection_info.color = "orange"
                self.super_user_note.visible = True  # Mostrar nota cuando no hay conexión
        except Exception as e:
            self.connection_info.value = f"⚠️ Error de conexión: {str(e)[:50]}\n💡 Usa 'root' / 'root' para acceso offline"
            self.connection_info.color = "orange"
            self.super_user_note.visible = True  # Mostrar nota cuando hay error
    
    def show_success_message(self, message: str):
        """Mostrar mensaje de éxito"""
        self.status_message.value = message
        self.status_message.color = "green"
        self.page.update()
    
    def show_error_message(self, message: str):
        """Mostrar mensaje de error"""
        self.status_message.value = message
        self.status_message.color = "red"
        self.page.update()
    
    def clear_form(self):
        """Limpiar formulario"""
        self.email_field.value = ""
        self.password_field.value = ""
        self.status_message.value = ""
        self.page.update()
    
    def handle_login(self, e):
        """Manejar intento de login"""
        try:
            # Validar campos
            email = self.email_field.value.strip()
            password = self.password_field.value.strip()
            
            if not email:
                self.show_error_message("Por favor ingresa tu correo electrónico")
                return
            
            if not password:
                self.show_error_message("Por favor ingresa tu contraseña")
                return
            
            # Mostrar mensaje de carga
            self.status_message.value = "🔄 Iniciando sesión..."
            self.status_message.color = "blue"
            self.login_button.disabled = True
            self.page.update()
            
            # Verificar si es el super usuario por defecto (ANTES de validar formato de email)
            if email == "root" and password == "root":
                # Super usuario por defecto
                super_user = {
                    'id': 0,
                    'nombre': 'Super Administrador',
                    'correo': 'root',
                    'rol': 'admin',
                    'estado': 1,
                    'creado_en': '2025-01-01 00:00:00',
                    'actualizado_en': '2025-01-01 00:00:00'
                }
                
                # Iniciar sesión como super usuario
                if self.session_manager.login(super_user):
                    self.show_success_message("✅ Bienvenido Super Administrador (Modo Offline)")
                    
                    # Callback de éxito
                    if self.on_login_success:
                        self.on_login_success(super_user)
                else:
                    self.show_error_message("❌ Error iniciando sesión como super usuario")
                return
            
            # Solo validar formato de email para usuarios normales (NO para super usuario)
            if "@" not in email or "." not in email:
                self.show_error_message("Por favor ingresa un correo válido")
                return
            
            # Intentar login normal con API
            try:
                success, message, usuario = self.api_manager.login_usuario(email, password)
                
                if success and usuario:
                    # Iniciar sesión
                    if self.session_manager.login(usuario):
                        self.show_success_message(f"✅ Bienvenido, {usuario.get('nombre', 'Usuario')}!")
                        
                        # Callback de éxito
                        if self.on_login_success:
                            self.on_login_success(usuario)
                    else:
                        self.show_error_message("❌ Error iniciando sesión")
                else:
                    self.show_error_message(f"❌ {message}")
                    
            except Exception as api_error:
                # Si hay error de API, sugerir usar super usuario
                self.show_error_message(f"❌ Error de conexión a API: {str(api_error)[:50]}\n💡 Usa 'root' / 'root' para acceso offline")
            
        except Exception as ex:
            self.show_error_message(f"❌ Error inesperado: {str(ex)}")
        
        finally:
            self.login_button.disabled = False
            self.page.update()
    
    def show_register_form(self, e):
        """Mostrar formulario de registro"""
        # Crear vista de registro
        register_view = RegisterView(
            self.page,
            self.config,
            self.api_manager,
            on_register_success=self.on_register_success,
            on_back_to_login=self.on_back_to_login
        )
        
        # Reemplazar contenido
        self.page.clean()
        self.page.add(register_view)
        self.page.update()
    
    def on_register_success(self, usuario):
        """Callback cuando el registro es exitoso"""
        # Volver al login y mostrar mensaje de éxito
        self.page.clean()
        self.page.add(self)
        self.show_success_message(f"✅ Usuario {usuario.get('nombre', '')} registrado exitosamente")
        self.email_field.value = usuario.get('correo', '')
        self.page.update()
    
    def on_back_to_login(self):
        """Callback para volver al login"""
        self.page.clean()
        self.page.add(self)
        self.page.update()


class RegisterView(ft.Container):
    """Vista de registro de usuarios"""
    
    def __init__(self, page: ft.Page, config, api_manager, on_register_success=None, on_back_to_login=None):
        self.page = page
        self.config = config
        self.api_manager = api_manager
        self.on_register_success = on_register_success
        self.on_back_to_login = on_back_to_login
        
        # Campos del formulario
        self.name_field = ft.TextField(
            label="Nombre Completo",
            hint_text="Ingresa tu nombre",
            prefix_icon="person",
            width=350,
            border_radius=10,
            filled=True,
            bgcolor="white",
            border_color="blue",
            focused_border_color="blue"
        )
        
        self.email_field = ft.TextField(
            label="Correo Electrónico",
            hint_text="Ingresa tu correo",
            prefix_icon="email",
            width=350,
            border_radius=10,
            filled=True,
            bgcolor="white",
            border_color="blue",
            focused_border_color="blue",
            keyboard_type=ft.KeyboardType.EMAIL
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            hint_text="Ingresa tu contraseña",
            prefix_icon="lock",
            width=350,
            border_radius=10,
            filled=True,
            bgcolor="white",
            border_color="blue",
            focused_border_color="blue",
            password=True,
            can_reveal_password=True
        )
        
        self.confirm_password_field = ft.TextField(
            label="Confirmar Contraseña",
            hint_text="Confirma tu contraseña",
            prefix_icon="lock",
            width=350,
            border_radius=10,
            filled=True,
            bgcolor="white",
            border_color="blue",
            focused_border_color="blue",
            password=True
        )
        
        # Mensaje de estado
        self.status_message = ft.Text(
            "",
            color="red",
            size=14,
            text_align=ft.TextAlign.CENTER,
            width=350
        )
        
        # Botón de registro
        self.register_button = ft.ElevatedButton(
            text="Registrarse",
            icon="person_add",
            width=350,
            height=50,
            style=ft.ButtonStyle(
                bgcolor="green",
                color="white",
                elevation=5,
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=self.handle_register
        )
        
        # Botón de volver
        self.back_button = ft.TextButton(
            text="← Volver al Login",
            width=350,
            style=ft.ButtonStyle(
                color="blue"
            ),
            on_click=self.handle_back
        )
        
        super().__init__(
            width=self.config.WINDOW_WIDTH,
            height=self.config.WINDOW_HEIGHT,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=0,
                controls=[
                    self._build_header(),
                    self._build_register_form(),
                    self._build_footer()
                ]
            )
        )
    
    def _build_header(self):
        """Construir header con gradiente"""
        return create_gradient_container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon("person_add", size=80, color="white"),
                    ft.Text(
                        "Registro de Usuario",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Crea tu cuenta en ModuStackClean",
                        size=16,
                        color="white",
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            ),
            height=250
        )
    
    def _build_register_form(self):
        """Construir formulario de registro"""
        return ft.Container(
            expand=True,
            bgcolor="white",
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                ft.Text(
                                    "Crear Cuenta",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="black",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                self.name_field,
                                self.email_field,
                                self.password_field,
                                self.confirm_password_field,
                                self.status_message,
                                self.register_button,
                                self.back_button
                            ]
                        ),
                        padding=ft.padding.all(30),
                        bgcolor="white",
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color="gray",
                            offset=ft.Offset(0, 2)
                        ),
                        width=450
                    )
                ]
            )
        )
    
    def _build_footer(self):
        """Construir footer"""
        return ft.Container(
            height=60,
            bgcolor="black",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        self.config.COPYRIGHT,
                        color="white",
                        size=12,
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            )
        )
    
    def show_success_message(self, message: str):
        """Mostrar mensaje de éxito"""
        self.status_message.value = message
        self.status_message.color = "green"
        self.page.update()
    
    def show_error_message(self, message: str):
        """Mostrar mensaje de error"""
        self.status_message.value = message
        self.status_message.color = "red"
        self.page.update()
    
    def handle_register(self, e):
        """Manejar registro de usuario"""
        try:
            # Validar campos
            name = self.name_field.value.strip()
            email = self.email_field.value.strip()
            password = self.password_field.value.strip()
            confirm_password = self.confirm_password_field.value.strip()
            
            if not name:
                self.show_error_message("Por favor ingresa tu nombre")
                return
            
            if not email:
                self.show_error_message("Por favor ingresa tu correo electrónico")
                return
            
            if not password:
                self.show_error_message("Por favor ingresa tu contraseña")
                return
            
            if not confirm_password:
                self.show_error_message("Por favor confirma tu contraseña")
                return
            
            # Validar formato de email
            if "@" not in email or "." not in email:
                self.show_error_message("Por favor ingresa un correo válido")
                return
            
            # Validar que las contraseñas coincidan
            if password != confirm_password:
                self.show_error_message("Las contraseñas no coinciden")
                return
            
            # Validar longitud de contraseña
            if len(password) < 6:
                self.show_error_message("La contraseña debe tener al menos 6 caracteres")
                return
            
            # Mostrar mensaje de carga
            self.status_message.value = "🔄 Registrando usuario..."
            self.status_message.color = "blue"
            self.register_button.disabled = True
            self.page.update()
            
            # Intentar registro
            success, message, user_id = self.api_manager.create_usuario(name, email, password)
            
            if success and user_id:
                self.show_success_message(f"✅ Usuario registrado exitosamente!")
                
                # Callback de éxito
                if self.on_register_success:
                    usuario = {'id': user_id, 'nombre': name, 'correo': email}
                    self.on_register_success(usuario)
            else:
                self.show_error_message(f"❌ {message}")
            
        except Exception as ex:
            self.show_error_message(f"❌ Error inesperado: {str(ex)}")
        
        finally:
            self.register_button.disabled = False
            self.page.update()
    
    def handle_back(self, e):
        """Manejar volver al login"""
        if self.on_back_to_login:
            self.on_back_to_login()
