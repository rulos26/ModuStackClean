#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vista Path - ModuStackClean
Vista para mostrar paths encontrados en el sistema
"""

import flet as ft
import os
import platform
from pathlib import Path

class PathView(ft.Container):
    """Vista para mostrar paths encontrados en el sistema"""
    
    def __init__(self, page: ft.Page, config, session_manager=None, on_logout=None, on_back=None):
        self.page = page
        self.config = config
        self.session_manager = session_manager
        self.on_logout = on_logout
        self.on_back = on_back
        self.current_user = None
        
        # Obtener información del usuario
        if self.session_manager and self.session_manager.is_logged_in():
            self.current_user = self.session_manager.get_current_user()
        
        # Estado del menú lateral
        self.sidebar_expanded = True
        
        # Resultados de la búsqueda
        self.search_results = []
        self.is_searching = False
        
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
                                "folder",
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
                "active": False,
                "on_click": self._on_menu_item_click
            },
            {
                "icon": "folder",
                "label": "Path",
                "active": True,
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
                    
                    # Contenido del path
                    self._build_path_content(),
                    
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
                        "Path - Rutas Encontradas",
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
    
    def _build_path_content(self):
        """Construir contenido del path"""
        return ft.Container(
            expand=True,
            padding=ft.padding.all(30),
            content=ft.Column(
                expand=True,
                spacing=30,
                controls=[
                    # Sección de búsqueda
                    self._build_search_section(),
                    
                    # Resultados de la búsqueda
                    self._build_results_section()
                ]
            )
        )
    
    def _build_search_section(self):
        """Construir sección de búsqueda"""
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
                        "🔍 Búsqueda de Rutas del Sistema",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#2d2d2d"
                    ),
                    ft.Text(
                        "Detecta automáticamente los discos duros y busca archivos en las rutas estándar del usuario.",
                        size=16,
                        color="#6c757d",
                        text_align=ft.TextAlign.START
                    ),
                    ft.ElevatedButton(
                        text="Buscar Rutas" if not self.is_searching else "Buscando...",
                        icon=ft.Icon("search"),
                        style=ft.ButtonStyle(
                            bgcolor="#4facfe",
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                        on_click=self._start_search
                    )
                ]
            )
        )
    
    def _build_results_section(self):
        """Construir sección de resultados con cards bonitas"""
        if not self.search_results:
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
                            "📁 Rutas Encontradas",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="#2d2d2d"
                        ),
                        ft.Text(
                            "Haz clic en 'Buscar Rutas' para comenzar la detección automática.",
                            size=16,
                            color="#6c757d",
                            text_align=ft.TextAlign.CENTER
                        )
                    ]
                )
            )
        
        # Crear grid de cards
        all_cards = []
        
        for result in self.search_results:
            # Crear cards para cada archivo encontrado
            for i, path in enumerate(result['paths']):
                # Obtener información del archivo
                file_name = os.path.basename(path)
                file_dir = os.path.dirname(path)
                file_size = self._get_file_size(path)
                file_icon = self._get_file_icon(file_name)
                
                # Crear card individual
                card = ft.Container(
                    bgcolor="white",
                    border_radius=12,
                    padding=ft.padding.all(20),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color="#00000015",
                        offset=ft.Offset(0, 2)
                    ),
                    border=ft.border.all(1, "#e9ecef"),
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            # Header de la card
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Icon(
                                                file_icon,
                                                color="#4facfe",
                                                size=24
                                            ),
                                            ft.Column(
                                                spacing=2,
                                                controls=[
                                                    ft.Text(
                                                        file_name,
                                                        size=16,
                                                        weight=ft.FontWeight.BOLD,
                                                        color="#2d2d2d",
                                                        max_lines=1,
                                                        overflow=ft.TextOverflow.ELLIPSIS
                                                    ),
                                                    ft.Text(
                                                        f"Tamaño: {file_size}",
                                                        size=12,
                                                        color="#6c757d"
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    ft.IconButton(
                                        icon="more_vert",
                                        icon_color="#6c757d",
                                        tooltip="Más opciones",
                                        on_click=self._on_card_more_click,
                                        data={"path": path, "file_name": file_name}
                                    )
                                ]
                            ),
                            
                            # Ruta del archivo
                            ft.Container(
                                bgcolor="#f8f9fa",
                                border_radius=8,
                                padding=ft.padding.all(12),
                                content=ft.Column(
                                    spacing=5,
                                    controls=[
                                        ft.Text(
                                            "📁 Ubicación:",
                                            size=12,
                                            weight=ft.FontWeight.BOLD,
                                            color="#495057"
                                        ),
                                        ft.Text(
                                            file_dir,
                                            size=12,
                                            color="#6c757d",
                                            font_family="monospace",
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS
                                        )
                                    ]
                                )
                            ),
                            
                            # Botones de acción
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.ElevatedButton(
                                        text="Abrir Ubicación",
                                        icon=ft.Icon("folder_open"),
                                        style=ft.ButtonStyle(
                                            bgcolor="#28a745",
                                            color="white",
                                            shape=ft.RoundedRectangleBorder(radius=6)
                                        ),
                                        on_click=self._on_open_location_click,
                                        data={"path": path}
                                    ),
                                    ft.ElevatedButton(
                                        text="Más Info",
                                        icon=ft.Icon("info"),
                                        style=ft.ButtonStyle(
                                            bgcolor="#17a2b8",
                                            color="white",
                                            shape=ft.RoundedRectangleBorder(radius=6)
                                        ),
                                        on_click=self._on_more_info_click,
                                        data={"path": path, "file_name": file_name}
                                    )
                                ]
                            )
                        ]
                    )
                )
                
                all_cards.append(card)
        
        # Crear grid responsive
        grid_view = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=400,
            child_aspect_ratio=1.2,
            spacing=20,
            run_spacing=20,
            controls=all_cards
        )
        
        return ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    f"📁 Archivos Encontrados ({len(all_cards)} archivos)",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#2d2d2d"
                ),
                grid_view
            ]
        )
    
    def _get_file_size(self, file_path):
        """Obtener tamaño del archivo en formato legible"""
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size / (1024 * 1024):.1f} MB"
            else:
                return f"{size / (1024 * 1024 * 1024):.1f} GB"
        except:
            return "N/A"
    
    def _get_file_icon(self, file_name):
        """Obtener icono según el tipo de archivo"""
        file_lower = file_name.lower()
        
        if file_lower.endswith('.exe'):
            return "play_circle"
        elif file_lower.endswith('.zip'):
            return "archive"
        elif file_lower.endswith('.rar'):
            return "archive"
        elif file_lower.endswith('.msi'):
            return "install_desktop"
        else:
            return "insert_drive_file"
    
    def _on_card_more_click(self, e):
        """Manejar clic en botón más de la card"""
        data = e.control.data
        print(f"🔍 Más opciones para: {data['file_name']}")
        # Por ahora solo muestra en consola, se puede expandir después
    
    def _on_open_location_click(self, e):
        """Manejar clic en abrir ubicación"""
        data = e.control.data
        path = data["path"]
        file_dir = os.path.dirname(path)
        
        try:
            import subprocess
            subprocess.run(["explorer", file_dir], check=True)
            print(f"📁 Abriendo ubicación: {file_dir}")
        except Exception as error:
            print(f"❌ Error abriendo ubicación: {error}")
    
    def _on_more_info_click(self, e):
        """Manejar clic en más información"""
        data = e.control.data
        path = data["path"]
        file_name = data["file_name"]
        
        try:
            # Obtener información detallada del archivo
            file_size = self._get_file_size(path)
            file_dir = os.path.dirname(path)
            created_time = os.path.getctime(path)
            modified_time = os.path.getmtime(path)
            
            import datetime
            created_str = datetime.datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
            modified_str = datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
            
            info_text = f"""
📄 Información del Archivo:
• Nombre: {file_name}
• Tamaño: {file_size}
• Ubicación: {file_dir}
• Creado: {created_str}
• Modificado: {modified_str}
            """
            
            print(info_text)
            
        except Exception as error:
                         print(f"❌ Error obteniendo información: {error}")
    
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
    
    def _start_search(self, e):
        """Iniciar búsqueda de rutas - Versión simplificada para ejecutable"""
        try:
            print("🔍 Iniciando búsqueda de rutas...")
            
            # Verificar que no esté ya buscando
            if self.is_searching:
                print("⚠️ Búsqueda ya en progreso, ignorando clic")
                return
            
            # Cambiar estado inmediatamente
            self.is_searching = True
            self.search_results = []
            
            # Actualizar UI inmediatamente
            self._update_search_ui()
            
            # Mostrar mensaje de búsqueda en progreso (versión compatible)
            if self.page:
                try:
                    # Intentar usar show_snack_bar si está disponible
                    if hasattr(self.page, 'show_snack_bar'):
                        self.page.show_snack_bar(
                            ft.SnackBar(
                                content=ft.Text("🔍 Buscando rutas en el sistema..."),
                                action="OK"
                            )
                        )
                    else:
                        # Alternativa: mostrar mensaje en consola
                        print("🔍 Buscando rutas en el sistema...")
                except Exception as snack_error:
                    print(f"⚠️ Error mostrando snackbar: {snack_error}")
            
            # Ejecutar búsqueda simplificada
            print("🚀 Ejecutando búsqueda simplificada...")
            self._perform_simple_search()
            
        except Exception as e:
            print(f"❌ Error en _start_search: {e}")
            import traceback
            traceback.print_exc()
            self.is_searching = False
            self._update_search_ui()
    
    def _perform_simple_search(self):
        """Realizar búsqueda simplificada para ejecutable"""
        try:
            print("🔍 Iniciando búsqueda simplificada...")
            
            # Detectar solo el disco principal
            drives = ["C:\\"]  # Solo buscar en C: para velocidad
            
            # Obtener el usuario actual del sistema
            current_user = self._get_current_user()
            print(f"👤 Usuario actual detectado: {current_user}")
            
            results = []
            for drive in drives:
                print(f"🔍 Buscando en disco: {drive}")
                
                # Buscar en rutas del usuario actual y también en Public
                search_paths = []
                
                # Rutas del usuario actual
                if current_user:
                    user_paths = [
                        os.path.join(drive, f"Users\\{current_user}\\Desktop"),
                        os.path.join(drive, f"Users\\{current_user}\\Downloads"),
                        os.path.join(drive, f"Users\\{current_user}\\Documents"),
                        os.path.join(drive, f"Users\\{current_user}\\Pictures"),
                        os.path.join(drive, f"Users\\{current_user}\\Music"),
                        os.path.join(drive, f"Users\\{current_user}\\Videos")
                    ]
                    search_paths.extend(user_paths)
                    print(f"📁 Rutas del usuario {current_user}: {user_paths}")
                
                # También buscar en Public como respaldo
                public_paths = [
                    os.path.join(drive, "Users\\Public\\Desktop"),
                    os.path.join(drive, "Users\\Public\\Downloads"),
                    os.path.join(drive, "Users\\Public\\Documents"),
                    os.path.join(drive, "Users\\Public\\Pictures"),
                    os.path.join(drive, "Users\\Public\\Music"),
                    os.path.join(drive, "Users\\Public\\Videos")
                ]
                search_paths.extend(public_paths)
                print(f"📁 Rutas públicas: {public_paths}")
                
                found_files = []
                for path in search_paths:
                    if os.path.exists(path):
                        print(f"📁 Buscando en: {path}")
                        try:
                            # Buscar solo los primeros 10 archivos por ruta
                            count = 0
                            for root, dirs, files in os.walk(path):
                                for file in files:
                                    if count >= 10:  # Límite para velocidad
                                        break
                                    file_lower = file.lower()
                                    # Buscar solo archivos ejecutables y comprimidos
                                    if any(file_lower.endswith(ext) for ext in ['.exe', '.zip', '.rar', '.msi']):
                                        found_files.append(os.path.join(root, file))
                                        count += 1
                                        print(f"  ✅ Encontrado: {file}")
                                if count >= 10:
                                    break
                        except Exception as path_error:
                            print(f"  ⚠️ Error en {path}: {path_error}")
                            continue
                
                if found_files:
                    results.append({
                        'disk': drive,
                        'paths': found_files[:30]  # Limitar a 30 archivos para mostrar
                    })
                    print(f"✅ Disco {drive}: {len(found_files)} archivos encontrados")
                else:
                    print(f"ℹ️ No se encontraron archivos en {drive}")
            
            print(f"✅ Búsqueda simplificada completada: {len(results)} discos")
            self.search_results = results
            
        except Exception as e:
            print(f"❌ Error en búsqueda simplificada: {e}")
            import traceback
            traceback.print_exc()
            self.search_results = []
        
        finally:
            # Marcar búsqueda como completada
            print("🏁 Marcando búsqueda como completada")
            self.is_searching = False
            self._update_search_ui()
    
    def _get_current_user(self):
        """Obtener el nombre del usuario actual del sistema"""
        try:
            # Método 1: Usar la variable de entorno USERNAME
            username = os.environ.get('USERNAME')
            if username:
                print(f"✅ Usuario detectado por USERNAME: {username}")
                return username
            
            # Método 2: Usar la variable de entorno USER
            username = os.environ.get('USER')
            if username:
                print(f"✅ Usuario detectado por USER: {username}")
                return username
            
            # Método 3: Obtener desde el directorio actual
            current_path = os.getcwd()
            if "Users\\" in current_path:
                # Extraer el nombre de usuario del path actual
                parts = current_path.split("Users\\")
                if len(parts) > 1:
                    username = parts[1].split("\\")[0]
                    print(f"✅ Usuario detectado por path actual: {username}")
                    return username
            
            # Método 4: Buscar en el directorio Users
            users_dir = "C:\\Users"
            if os.path.exists(users_dir):
                try:
                    # Listar directorios en Users y encontrar el que no es Public
                    for item in os.listdir(users_dir):
                        if item != "Public" and os.path.isdir(os.path.join(users_dir, item)):
                            print(f"✅ Usuario detectado por directorio: {item}")
                            return item
                except Exception as e:
                    print(f"⚠️ Error listando directorios de usuarios: {e}")
            
            print("⚠️ No se pudo detectar el usuario actual, usando 'Public'")
            return None
            
        except Exception as e:
            print(f"❌ Error detectando usuario: {e}")
            return None
    
    def _perform_search(self):
        """Realizar la búsqueda de rutas (versión con hilos - mantenida para compatibilidad)"""
        try:
            print("🔍 Detectando discos...")
            # Detectar discos
            drives = self._detect_drives()
            print(f"📂 Discos detectados: {drives}")
            
            results = []
            for drive in drives:
                print(f"🔍 Buscando en disco: {drive}")
                # Obtener rutas estándar
                standard_paths = self._get_standard_paths(drive)
                print(f"📁 Rutas estándar en {drive}: {standard_paths}")
                
                # Buscar archivos
                found_files = self._search_files_in_paths(standard_paths)
                print(f"📄 Archivos encontrados en {drive}: {len(found_files)}")
                
                if found_files:
                    results.append({
                        'disk': drive,
                        'paths': found_files
                    })
            
            print(f"✅ Búsqueda completada. Resultados: {len(results)} discos")
            # Actualizar resultados en el hilo principal usando invoke
            self.search_results = results
            
        except Exception as e:
            print(f"❌ Error en la búsqueda: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Marcar búsqueda como completada y actualizar UI en el hilo principal
            self.is_searching = False
            # Usar invoke para actualizar la UI desde el hilo principal
            if self.page:
                self.page.invoke(self._update_search_ui)
    
    def _update_search_ui(self):
        """Actualizar la interfaz de usuario"""
        try:
            print("🔄 Actualizando UI...")
            # Reconstruir el contenido principal
            self.main_content = self._build_main_content()
            
            # Limpiar la página y reconstruir todo
            self.page.clean()
            
            # Reconstruir los componentes con el nuevo estado
            self.sidebar = self._build_sidebar()
            
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
            if self.page:
                self.page.update()
                
            # Mostrar mensaje de completado (versión compatible)
            if not self.is_searching and self.search_results:
                try:
                    if hasattr(self.page, 'show_snack_bar'):
                        self.page.show_snack_bar(
                            ft.SnackBar(
                                content=ft.Text(f"✅ Búsqueda completada. {len(self.search_results)} discos con archivos encontrados."),
                                action="OK"
                            )
                        )
                    else:
                        print(f"✅ Búsqueda completada. {len(self.search_results)} discos con archivos encontrados.")
                except Exception as e:
                    print(f"✅ Búsqueda completada. {len(self.search_results)} discos con archivos encontrados.")
            elif not self.is_searching and not self.search_results:
                try:
                    if hasattr(self.page, 'show_snack_bar'):
                        self.page.show_snack_bar(
                            ft.SnackBar(
                                content=ft.Text("ℹ️ No se encontraron archivos del programa en las rutas estándar."),
                                action="OK"
                            )
                        )
                    else:
                        print("ℹ️ No se encontraron archivos del programa en las rutas estándar.")
                except Exception as e:
                    print("ℹ️ No se encontraron archivos del programa en las rutas estándar.")
            
            print("✅ UI actualizada correctamente")
                
        except Exception as e:
            print(f"❌ Error actualizando UI: {e}")
            import traceback
            traceback.print_exc()
    
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
        
        if item["label"] == "Inicio" and self.on_back:
            self.on_back()
        else:
            try:
                if hasattr(self.page, 'show_snack_bar'):
                    self.page.show_snack_bar(
                        ft.SnackBar(
                            content=ft.Text(f"Navegando a: {item['label']}"),
                            action="OK"
                        )
                    )
                else:
                    print(f"Navegando a: {item['label']}")
            except Exception as e:
                print(f"Navegando a: {item['label']}")
    
    def _handle_logout(self, e):
        """Manejar logout de usuario"""
        if self.session_manager:
            self.session_manager.logout()
        
        if self.on_logout:
            self.on_logout()
    
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
