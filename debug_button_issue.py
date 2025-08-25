#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico del Problema del Botón - ModuStackClean
Script para identificar por qué el botón no funciona en el ejecutable
"""

import os
import platform
import sys
import traceback

def check_system_permissions():
    """Verificar permisos del sistema"""
    print("🔍 VERIFICANDO PERMISOS DEL SISTEMA")
    print("=" * 50)
    
    try:
        # Verificar acceso a disco C:
        c_drive = "C:\\"
        if os.path.exists(c_drive):
            print(f"✅ Acceso a {c_drive}: PERMITIDO")
            
            # Intentar listar archivos
            try:
                files = os.listdir(c_drive)
                print(f"✅ Listado de archivos en {c_drive}: {len(files)} archivos")
            except PermissionError:
                print(f"❌ Listado de archivos en {c_drive}: DENEGADO")
        else:
            print(f"❌ Acceso a {c_drive}: NO EXISTE")
        
        # Verificar rutas estándar
        standard_paths = [
            "C:\\Users\\Public\\Desktop",
            "C:\\Users\\Public\\Downloads",
            "C:\\Users\\Public\\Documents"
        ]
        
        for path in standard_paths:
            if os.path.exists(path):
                print(f"✅ Ruta {path}: EXISTE")
                try:
                    files = os.listdir(path)
                    print(f"  📁 Archivos: {len(files)}")
                except PermissionError:
                    print(f"  ❌ Acceso denegado")
            else:
                print(f"❌ Ruta {path}: NO EXISTE")
                
    except Exception as e:
        print(f"❌ Error verificando permisos: {e}")

def check_file_operations():
    """Verificar operaciones de archivos"""
    print("\n🔍 VERIFICANDO OPERACIONES DE ARCHIVOS")
    print("=" * 50)
    
    try:
        # Simular búsqueda de archivos
        test_path = "C:\\"
        found_files = []
        
        print(f"🔍 Buscando archivos en {test_path}...")
        
        for root, dirs, files in os.walk(test_path):
            for file in files:
                file_lower = file.lower()
                if any(file_lower.endswith(ext) for ext in ['.exe', '.zip', '.rar']):
                    found_files.append(os.path.join(root, file))
                    if len(found_files) >= 5:  # Solo los primeros 5
                        break
            if len(found_files) >= 5:
                break
        
        print(f"✅ Archivos encontrados: {len(found_files)}")
        for i, file in enumerate(found_files, 1):
            print(f"  {i}. {file}")
            
    except Exception as e:
        print(f"❌ Error en operaciones de archivos: {e}")
        traceback.print_exc()

def check_threading_issues():
    """Verificar problemas de threading"""
    print("\n🔍 VERIFICANDO PROBLEMAS DE THREADING")
    print("=" * 50)
    
    try:
        import threading
        import time
        
        def test_function():
            print("  🧵 Hilo de prueba ejecutándose...")
            time.sleep(1)
            print("  ✅ Hilo de prueba completado")
        
        print("🧵 Creando hilo de prueba...")
        thread = threading.Thread(target=test_function)
        thread.daemon = True
        thread.start()
        
        print("⏳ Esperando hilo...")
        thread.join(timeout=3)
        
        if thread.is_alive():
            print("❌ Hilo no se completó en tiempo")
        else:
            print("✅ Hilo funcionó correctamente")
            
    except Exception as e:
        print(f"❌ Error en threading: {e}")
        traceback.print_exc()

def check_flet_components():
    """Verificar componentes Flet"""
    print("\n🔍 VERIFICANDO COMPONENTES FLET")
    print("=" * 50)
    
    try:
        import flet as ft
        
        # Test de creación de botón
        button = ft.ElevatedButton(
            text="Test Button",
            on_click=lambda e: print("  ✅ Botón clickeado")
        )
        print("✅ Botón Flet creado correctamente")
        
        # Test de callback
        print("🧪 Simulando clic en botón...")
        # Simular el evento de clic
        class MockEvent:
            pass
        
        event = MockEvent()
        button.on_click(event)
        
        print("✅ Callback del botón funcionó")
        
    except Exception as e:
        print(f"❌ Error en componentes Flet: {e}")
        traceback.print_exc()

def check_executable_environment():
    """Verificar entorno del ejecutable"""
    print("\n🔍 VERIFICANDO ENTORNO DEL EJECUTABLE")
    print("=" * 50)
    
    print(f"🖥️ Sistema Operativo: {platform.system()}")
    print(f"📋 Versión: {platform.version()}")
    print(f"🏗️ Arquitectura: {platform.machine()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🔧 Ejecutando como ejecutable: {getattr(sys, 'frozen', False)}")
    
    # Verificar variables de entorno
    print(f"🏠 HOME: {os.environ.get('HOME', 'No definido')}")
    print(f"👤 USER: {os.environ.get('USER', 'No definido')}")
    print(f"👤 USERNAME: {os.environ.get('USERNAME', 'No definido')}")

def main():
    """Función principal de diagnóstico"""
    print("🚀 INICIANDO DIAGNÓSTICO DEL PROBLEMA DEL BOTÓN")
    print("=" * 60)
    
    # Verificar entorno del ejecutable
    check_executable_environment()
    
    # Verificar permisos del sistema
    check_system_permissions()
    
    # Verificar operaciones de archivos
    check_file_operations()
    
    # Verificar problemas de threading
    check_threading_issues()
    
    # Verificar componentes Flet
    check_flet_components()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    print("✅ Si todos los tests pasaron, el problema puede ser:")
    print("   - Configuración específica del ejecutable")
    print("   - Problema de timing en la UI")
    print("   - Conflicto con antivirus")
    print("   - Permisos específicos del ejecutable")
    
    print("\n💡 SOLUCIONES SUGERIDAS:")
    print("   1. Ejecutar como administrador")
    print("   2. Desactivar temporalmente el antivirus")
    print("   3. Verificar logs del sistema")
    print("   4. Usar versión de desarrollo (python main.py)")

if __name__ == "__main__":
    main()
