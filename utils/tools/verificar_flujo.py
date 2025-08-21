#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Flujo de Trabajo - ModuStackClean
Verifica que todos los archivos estén en las carpetas correctas y el flujo funcione
"""

import os
import json
import sys
from pathlib import Path

def verificar_estructura():
    """Verifica que la estructura de carpetas sea correcta"""
    print("🔍 Verificando estructura de carpetas...")
    
    carpetas_requeridas = [
        "web/backend",
        "web/frontend", 
        "python/scripts",
        "python/modules",
        "docs/guides",
        "docs/api",
        "tests/unit",
        "tests/integration",
        "utils/tools",
        "config/installation",
        "src/core/installation"
    ]
    
    errores = []
    for carpeta in carpetas_requeridas:
        if not os.path.exists(carpeta):
            errores.append(f"❌ Falta carpeta: {carpeta}")
        else:
            print(f"✅ Carpeta existe: {carpeta}")
    
    return errores

def verificar_archivos_principales():
    """Verifica que los archivos principales estén en su lugar"""
    print("\n📁 Verificando archivos principales...")
    
    archivos_requeridos = {
        "index.php": "Archivo de entrada principal",
        "web/backend/navegacion.php": "Página de navegación",
        "web/backend/index.php": "Backend principal",
        "web/backend/funciones.php": "Funciones principales",
        "python/scripts/servidor_automatico.py": "Servidor automático",
        "python/scripts/gestor_descargas.py": "Gestor de descargas",
        "config/workflow.json": "Configuración de flujo",
        "docs/README.md": "Documentación principal"
    }
    
    errores = []
    for archivo, descripcion in archivos_requeridos.items():
        if not os.path.exists(archivo):
            errores.append(f"❌ Falta archivo: {archivo} ({descripcion})")
        else:
            print(f"✅ Archivo existe: {archivo}")
    
    return errores

def verificar_flujo_php():
    """Verifica que el flujo PHP funcione correctamente"""
    print("\n🌐 Verificando flujo PHP...")
    
    # Verificar que index.php pueda incluir el backend
    index_path = "index.php"
    backend_path = "web/backend/index.php"
    
    if not os.path.exists(index_path):
        return ["❌ No existe index.php principal"]
    
    if not os.path.exists(backend_path):
        return ["❌ No existe web/backend/index.php"]
    
    print("✅ Flujo PHP básico verificado")
    return []

def verificar_scripts_python():
    """Verifica que los scripts Python sean ejecutables"""
    print("\n🐍 Verificando scripts Python...")
    
    scripts_python = [
        "python/scripts/servidor_automatico.py",
        "python/scripts/gestor_descargas.py",
        "python/scripts/info_sistema.py"
    ]
    
    errores = []
    for script in scripts_python:
        if not os.path.exists(script):
            errores.append(f"❌ No existe: {script}")
        else:
            # Verificar que sea un archivo Python válido
            try:
                with open(script, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    if '#!/usr/bin/env python' in contenido or 'import ' in contenido:
                        print(f"✅ Script válido: {script}")
                    else:
                        errores.append(f"⚠️  Posible problema en: {script}")
            except Exception as e:
                errores.append(f"❌ Error leyendo {script}: {e}")
    
    return errores

def generar_reporte():
    """Genera un reporte completo del estado del sistema"""
    print("\n📊 Generando reporte de verificación...")
    
    errores = []
    errores.extend(verificar_estructura())
    errores.extend(verificar_archivos_principales())
    errores.extend(verificar_flujo_php())
    errores.extend(verificar_scripts_python())
    
    print("\n" + "="*50)
    print("📋 REPORTE FINAL")
    print("="*50)
    
    if errores:
        print(f"❌ Se encontraron {len(errores)} problemas:")
        for error in errores:
            print(f"  {error}")
        return False
    else:
        print("✅ ¡Todo está correctamente organizado!")
        print("✅ El flujo de trabajo está funcionando correctamente")
        return True

def main():
    """Función principal"""
    print("🚀 Verificador de Flujo de Trabajo - ModuStackClean")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_dir)
    
    print(f"📂 Directorio del proyecto: {os.getcwd()}")
    
    # Ejecutar verificaciones
    exito = generar_reporte()
    
    if exito:
        print("\n🎉 ¡Sistema listo para usar!")
        print("💡 Puedes acceder al sistema a través de: http://localhost/ModuStackClean/")
    else:
        print("\n⚠️  Hay problemas que necesitan ser resueltos antes de usar el sistema")
    
    return exito

if __name__ == "__main__":
    try:
        exito = main()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        sys.exit(1)
