#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Funcionalidad de Búsqueda de Rutas - ModuStackClean
Script para probar la detección de discos y búsqueda de archivos
"""

import os
import platform
import sys

def test_drive_detection():
    """Test de detección de discos"""
    print("🔍 TEST: Detección de Discos")
    print("=" * 50)
    
    drives = []
    
    if platform.system() == "Windows":
        import string
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
                print(f"✅ Disco encontrado: {drive}")
    else:
        # Para sistemas Unix/Linux
        drives = ["/"]
        print(f"✅ Disco encontrado: {drives[0]}")
    
    print(f"\n📊 Total de discos detectados: {len(drives)}")
    print(f"📂 Discos: {drives}")
    return drives

def test_standard_paths(drive):
    """Test de rutas estándar"""
    print(f"\n🔍 TEST: Rutas Estándar en {drive}")
    print("=" * 50)
    
    standard_paths = []
    
    if platform.system() == "Windows":
        # Rutas estándar de Windows
        user_paths = [
            "Users\\Public\\Desktop",
            "Users\\Public\\Documents",
            "Users\\Public\\Downloads",
            "Users\\Public\\Pictures",
            "Users\\Public\\Music",
            "Users\\Public\\Videos"
        ]
        
        for path in user_paths:
            full_path = os.path.join(drive, path)
            if os.path.exists(full_path):
                standard_paths.append(full_path)
                print(f"✅ Ruta encontrada: {full_path}")
            else:
                print(f"❌ Ruta no existe: {full_path}")
        
        # También buscar en el directorio raíz del disco
        if os.path.exists(drive):
            standard_paths.append(drive)
            print(f"✅ Ruta raíz: {drive}")
    else:
        # Rutas estándar de Unix/Linux
        standard_paths = [
            "/home",
            "/usr",
            "/var",
            "/tmp"
        ]
        for path in standard_paths:
            if os.path.exists(path):
                print(f"✅ Ruta encontrada: {path}")
            else:
                print(f"❌ Ruta no existe: {path}")
    
    print(f"\n📊 Total de rutas estándar: {len(standard_paths)}")
    return standard_paths

def test_file_search(paths):
    """Test de búsqueda de archivos"""
    print(f"\n🔍 TEST: Búsqueda de Archivos")
    print("=" * 50)
    
    found_paths = []
    
    # Extensiones de archivos comunes del programa
    program_extensions = ['.exe', '.msi', '.zip', '.rar', '.7z', '.dmg', '.pkg']
    program_names = ['modustack', 'modustackclean', 'cleaner', 'organizer']
    
    print(f"🔍 Buscando archivos con extensiones: {program_extensions}")
    print(f"🔍 Buscando archivos con nombres: {program_names}")
    
    for path in paths:
        try:
            if os.path.exists(path):
                print(f"\n📁 Buscando en: {path}")
                file_count = 0
                
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_lower = file.lower()
                        
                        # Verificar por extensión
                        if any(file_lower.endswith(ext) for ext in program_extensions):
                            found_path = os.path.join(root, file)
                            found_paths.append(found_path)
                            print(f"  ✅ Encontrado (extensión): {found_path}")
                            file_count += 1
                        
                        # Verificar por nombre
                        elif any(name in file_lower for name in program_names):
                            found_path = os.path.join(root, file)
                            found_paths.append(found_path)
                            print(f"  ✅ Encontrado (nombre): {found_path}")
                            file_count += 1
                        
                        # Limitar la búsqueda para evitar que sea muy lenta
                        if len(found_paths) > 100:
                            print(f"  ⚠️ Límite de 100 archivos alcanzado")
                            break
                    
                    if len(found_paths) > 100:
                        break
                
                if file_count == 0:
                    print(f"  ℹ️ No se encontraron archivos relevantes")
                    
        except (PermissionError, OSError) as e:
            print(f"  ❌ Error de acceso: {e}")
            continue
    
    print(f"\n📊 Total de archivos encontrados: {len(found_paths)}")
    return found_paths

def test_system_info():
    """Test de información del sistema"""
    print("🔍 TEST: Información del Sistema")
    print("=" * 50)
    
    print(f"🖥️ Sistema Operativo: {platform.system()}")
    print(f"📋 Versión: {platform.version()}")
    print(f"🏗️ Arquitectura: {platform.machine()}")
    print(f"🐍 Python: {sys.version}")

def main():
    """Función principal del test"""
    print("🚀 INICIANDO TEST DE BÚSQUEDA DE RUTAS")
    print("=" * 60)
    
    # Test de información del sistema
    test_system_info()
    
    # Test de detección de discos
    drives = test_drive_detection()
    
    if not drives:
        print("❌ No se detectaron discos. Test fallido.")
        return
    
    # Test de rutas estándar para cada disco
    all_standard_paths = []
    for drive in drives:
        standard_paths = test_standard_paths(drive)
        all_standard_paths.extend(standard_paths)
    
    if not all_standard_paths:
        print("❌ No se encontraron rutas estándar. Test fallido.")
        return
    
    # Test de búsqueda de archivos
    found_files = test_file_search(all_standard_paths)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL TEST")
    print("=" * 60)
    print(f"✅ Discos detectados: {len(drives)}")
    print(f"✅ Rutas estándar encontradas: {len(all_standard_paths)}")
    print(f"✅ Archivos del programa encontrados: {len(found_files)}")
    
    if found_files:
        print("\n📄 Archivos encontrados:")
        for i, file_path in enumerate(found_files[:10], 1):  # Mostrar solo los primeros 10
            print(f"  {i}. {file_path}")
        if len(found_files) > 10:
            print(f"  ... y {len(found_files) - 10} archivos más")
    else:
        print("\nℹ️ No se encontraron archivos del programa en las rutas estándar.")
        print("💡 Esto es normal si no hay archivos con las extensiones o nombres buscados.")
    
    print("\n🎉 Test completado exitosamente!")

if __name__ == "__main__":
    main()
