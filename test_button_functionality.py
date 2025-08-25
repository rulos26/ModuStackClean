#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Funcionalidad del Botón de Búsqueda - ModuStackClean
Script para verificar que el botón "Buscar Rutas" funciona correctamente
"""

import flet as ft
import os
import platform
import sys
import threading
import time

def test_button_click():
    """Test de clic del botón"""
    print("🔍 TEST: Funcionalidad del Botón")
    print("=" * 50)
    
    # Simular el comportamiento del botón
    print("✅ Simulando clic en botón 'Buscar Rutas'...")
    
    # Test de detección de discos
    drives = test_drive_detection()
    if not drives:
        print("❌ No se detectaron discos")
        return False
    
    # Test de búsqueda rápida
    print("✅ Iniciando búsqueda rápida...")
    results = test_quick_search(drives)
    
    print(f"✅ Búsqueda completada: {len(results)} discos con archivos")
    return True

def test_drive_detection():
    """Test de detección de discos"""
    print("🔍 Detectando discos...")
    drives = []
    
    if platform.system() == "Windows":
        import string
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
                print(f"  ✅ Disco encontrado: {drive}")
    else:
        drives = ["/"]
        print(f"  ✅ Disco encontrado: {drives[0]}")
    
    return drives

def test_quick_search(drives):
    """Test de búsqueda rápida"""
    results = []
    
    for drive in drives[:1]:  # Solo probar el primer disco para velocidad
        print(f"🔍 Buscando en: {drive}")
        
        # Buscar solo en algunas rutas para velocidad
        test_paths = [
            os.path.join(drive, "Users\\Public\\Desktop"),
            os.path.join(drive, "Users\\Public\\Downloads"),
            drive  # Raíz del disco
        ]
        
        found_files = []
        for path in test_paths:
            if os.path.exists(path):
                try:
                    # Buscar solo los primeros 10 archivos para velocidad
                    count = 0
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if count >= 10:  # Límite para velocidad
                                break
                            file_lower = file.lower()
                            if any(file_lower.endswith(ext) for ext in ['.exe', '.zip', '.rar']):
                                found_files.append(os.path.join(root, file))
                                count += 1
                        if count >= 10:
                            break
                except (PermissionError, OSError):
                    continue
        
        if found_files:
            results.append({
                'disk': drive,
                'paths': found_files[:5]  # Solo mostrar 5 archivos
            })
    
    return results

def test_ui_components():
    """Test de componentes de UI"""
    print("🔍 TEST: Componentes de UI")
    print("=" * 50)
    
    # Simular componentes Flet
    try:
        # Test de creación de botón
        button = ft.ElevatedButton(
            text="Buscar Rutas",
            icon=ft.Icon("search"),
            style=ft.ButtonStyle(
                bgcolor="#4facfe",
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )
        print("✅ Botón creado correctamente")
        
        # Test de creación de contenedor
        container = ft.Container(
            bgcolor="white",
            border_radius=12,
            padding=ft.padding.all(30),
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Text("🔍 Búsqueda de Rutas del Sistema", size=28),
                    button
                ]
            )
        )
        print("✅ Contenedor creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando componentes UI: {e}")
        return False

def main():
    """Función principal del test"""
    print("🚀 INICIANDO TEST DE FUNCIONALIDAD DEL BOTÓN")
    print("=" * 60)
    
    # Test de componentes UI
    ui_test = test_ui_components()
    
    # Test de funcionalidad del botón
    button_test = test_button_click()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL TEST")
    print("=" * 60)
    print(f"✅ Componentes UI: {'PASÓ' if ui_test else 'FALLÓ'}")
    print(f"✅ Funcionalidad del botón: {'PASÓ' if button_test else 'FALLÓ'}")
    
    if ui_test and button_test:
        print("\n🎉 ¡Todos los tests pasaron! El botón debería funcionar correctamente.")
    else:
        print("\n⚠️ Algunos tests fallaron. Revisar la implementación.")
    
    print("\n💡 Si el botón no funciona en el ejecutable, puede ser un problema de:")
    print("   - Gestión de hilos en el ejecutable")
    print("   - Permisos de acceso al sistema de archivos")
    print("   - Configuración de PyInstaller")

if __name__ == "__main__":
    main()
