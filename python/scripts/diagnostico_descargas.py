#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico de la carpeta de descargas
Script para verificar por qué no se encuentran archivos
"""

import os
from pathlib import Path
import sys

def diagnosticar_descargas():
    """Diagnostica problemas con la carpeta de descargas"""
    print("🔍 DIAGNÓSTICO DE CARPETA DE DESCARGAS")
    print("=" * 50)
    
    # Verificar sistema operativo
    print(f"🖥️  Sistema operativo: {sys.platform}")
    
    # Obtener ruta de descargas
    if sys.platform == "win32":
        descargas_path = Path.home() / "Downloads"
    elif sys.platform == "darwin":  # macOS
        descargas_path = Path.home() / "Downloads"
    else:  # Linux
        descargas_path = Path.home() / "Downloads"
    
    print(f"📂 Ruta de descargas: {descargas_path}")
    print(f"📂 Ruta existe: {descargas_path.exists()}")
    
    if not descargas_path.exists():
        print("❌ La carpeta de descargas no existe")
        return
    
    # Verificar permisos
    try:
        test_file = descargas_path / "test_permissions.txt"
        with open(test_file, 'w') as f:
            f.write("test")
        test_file.unlink()
        print("✅ Permisos de escritura: OK")
    except Exception as e:
        print(f"❌ Error de permisos: {e}")
        return
    
    # Listar contenido
    print(f"\n📋 Contenido de la carpeta:")
    print("-" * 30)
    
    archivos_encontrados = []
    carpetas_encontradas = []
    
    try:
        for item in descargas_path.iterdir():
            if item.is_file():
                archivos_encontrados.append(item)
                print(f"📄 {item.name}")
            elif item.is_dir():
                carpetas_encontradas.append(item)
                print(f"📁 {item.name}/")
    except Exception as e:
        print(f"❌ Error listando contenido: {e}")
        return
    
    print(f"\n📊 Resumen:")
    print(f"   📄 Archivos: {len(archivos_encontrados)}")
    print(f"   📁 Carpetas: {len(carpetas_encontradas)}")
    
    if len(archivos_encontrados) == 0:
        print("\n⚠️  No se encontraron archivos en la carpeta de descargas")
        print("💡 Posibles causas:")
        print("   - Los archivos están en subcarpetas")
        print("   - La ruta de descargas no es la correcta")
        print("   - Los archivos están ocultos")
        
        # Buscar en subcarpetas
        print(f"\n🔍 Buscando archivos en subcarpetas...")
        archivos_en_subcarpetas = []
        for carpeta in carpetas_encontradas:
            try:
                for item in carpeta.iterdir():
                    if item.is_file():
                        archivos_en_subcarpetas.append(item)
                        print(f"   📄 {carpeta.name}/{item.name}")
            except Exception as e:
                print(f"   ❌ Error accediendo a {carpeta.name}: {e}")
        
        if archivos_en_subcarpetas:
            print(f"\n✅ Se encontraron {len(archivos_en_subcarpetas)} archivos en subcarpetas")
        else:
            print("\n❌ No se encontraron archivos en subcarpetas")
    
    # Verificar rutas alternativas de descargas
    print(f"\n🔍 Verificando rutas alternativas de descargas:")
    rutas_alternativas = [
        Path.home() / "Downloads",
        Path.home() / "Descargas",
        Path.home() / "Desktop" / "Downloads",
        Path("C:/Users") / os.getenv('USERNAME', '') / "Downloads",
        Path("D:/Contenedor/Users/jdiazl/Downloads")  # Ruta específica vista en las imágenes
    ]
    
    for ruta in rutas_alternativas:
        if ruta.exists():
            archivos_count = len([f for f in ruta.iterdir() if f.is_file()])
            print(f"   📂 {ruta}: {archivos_count} archivos")
            if archivos_count > 0:
                print(f"      ✅ Esta ruta tiene archivos!")
                # Mostrar algunos archivos de ejemplo
                for i, archivo in enumerate(ruta.iterdir()):
                    if archivo.is_file() and i < 5:
                        print(f"         📄 {archivo.name}")

if __name__ == "__main__":
    diagnosticar_descargas()
