#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para empaquetar ModuStackClean en ejecutable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Construir ejecutable con PyInstaller"""
    
    print("🚀 Iniciando empaquetado de ModuStackClean...")
    
    # Configuración del ejecutable
    app_name = "ModuStackClean"
    main_file = "main.py"
    icon_file = None  # Puedes agregar un icono .ico si lo tienes
    
    # Comando base de PyInstaller
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",  # Un solo archivo ejecutable
        "--windowed",  # Sin consola (aplicación de ventana)
        "--name", app_name,
        "--clean",  # Limpiar archivos temporales
        "--noconfirm",  # No preguntar confirmación
        # "--icon", icon_file,  # Descomenta si tienes un icono
        main_file
    ]
    
    # Agregar datos adicionales si es necesario
    cmd.extend([
        "--add-data", "config;config",
        "--add-data", "models;models",
        "--add-data", "utils;utils",
        "--add-data", "views;views"
    ])
    
    # Agregar módulos ocultos que PyInstaller podría no detectar
    cmd.extend([
        "--hidden-import", "flet",
        "--hidden-import", "flet_core",
        "--hidden-import", "mysql.connector",
        "--hidden-import", "mysql.connector.locales",
        "--hidden-import", "mysql.connector.plugins",
        "--hidden-import", "requests",
        "--hidden-import", "urllib3",
        "--hidden-import", "certifi",
        "--hidden-import", "charset_normalizer",
        "--hidden-import", "idna"
    ])
    
    try:
        print("📦 Ejecutando PyInstaller...")
        print(f"Comando: {' '.join(cmd)}")
        
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Empaquetado completado exitosamente!")
            
            # Verificar que el ejecutable se creó
            exe_path = Path("dist") / f"{app_name}.exe"
            if exe_path.exists():
                print(f"📁 Ejecutable creado en: {exe_path.absolute()}")
                print(f"📏 Tamaño del archivo: {exe_path.stat().st_size / (1024*1024):.2f} MB")
                
                # Crear archivo de información
                create_info_file(exe_path)
                
                return True
            else:
                print("❌ Error: No se encontró el ejecutable generado")
                return False
        else:
            print("❌ Error durante el empaquetado:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def create_info_file(exe_path):
    """Crear archivo de información del ejecutable"""
    info_content = f"""
# ModuStackClean - Ejecutable Generado

## Información del Ejecutable
- **Archivo**: {exe_path.name}
- **Ruta**: {exe_path.absolute()}
- **Tamaño**: {exe_path.stat().st_size / (1024*1024):.2f} MB
- **Fecha de creación**: {exe_path.stat().st_mtime}

## Instrucciones de Uso
1. El ejecutable es completamente independiente
2. No requiere instalación de Python
3. Incluye todas las dependencias necesarias
4. Funciona en cualquier Windows 10/11

## Requisitos del Sistema
- Windows 10 o superior
- Conexión a internet (para base de datos remota)
- XAMPP (opcional, para base de datos local)

## Notas Importantes
- El primer inicio puede tardar unos segundos
- La aplicación se conectará automáticamente a la base de datos
- Si no hay conexión remota, usará la base de datos local

## Solución de Problemas
- Si el ejecutable no inicia, verifica que Windows Defender no lo bloquee
- Agrega el archivo a las exclusiones de antivirus si es necesario
- Para problemas de base de datos, verifica la conexión a internet

## Archivos Generados
- `dist/ModuStackClean.exe` - Ejecutable principal
- `build/` - Archivos temporales de construcción
- `ModuStackClean.spec` - Especificación de PyInstaller

## Limpieza
Para limpiar archivos temporales:
- Eliminar carpeta `build/`
- Eliminar archivo `ModuStackClean.spec`
- Mantener solo `dist/ModuStackClean.exe`
"""
    
    info_file = Path("dist") / "INFORMACION_EJECUTABLE.md"
    with open(info_file, "w", encoding="utf-8") as f:
        f.write(info_content)
    
    print(f"📄 Archivo de información creado: {info_file}")

def clean_build_files():
    """Limpiar archivos temporales de construcción"""
    print("🧹 Limpiando archivos temporales...")
    
    # Archivos y carpetas a eliminar
    to_remove = [
        "build",
        "ModuStackClean.spec",
        "__pycache__"
    ]
    
    for item in to_remove:
        path = Path(item)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"🗑️ Eliminado: {item}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🔧 EMPAQUETADOR DE MODUSTACKCLEAN")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("main.py").exists():
        print("❌ Error: No se encontró main.py")
        print("Asegúrate de ejecutar este script desde el directorio flet_app/")
        return
    
    # Construir ejecutable
    if build_executable():
        print("\n🎉 ¡Empaquetado completado exitosamente!")
        print("\n📋 Próximos pasos:")
        print("1. Ve a la carpeta 'dist/'")
        print("2. Ejecuta 'ModuStackClean.exe'")
        print("3. Prueba todas las funcionalidades")
        print("4. Distribuye el ejecutable según necesites")
        
        # Preguntar si limpiar archivos temporales
        response = input("\n¿Deseas limpiar los archivos temporales? (s/n): ").lower()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            clean_build_files()
            print("✅ Limpieza completada")
    else:
        print("\n❌ Error durante el empaquetado")
        print("Revisa los mensajes de error anteriores")

if __name__ == "__main__":
    main()
