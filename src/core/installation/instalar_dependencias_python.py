#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para instalar dependencias de Python para el Gestor de Descargas
"""

import subprocess
import sys
import os

def instalar_paquete(paquete, nombre_mostrado=None):
    """Instalar un paquete usando pip"""
    if nombre_mostrado is None:
        nombre_mostrado = paquete
    
    print(f"📦 Instalando {nombre_mostrado}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"✅ {nombre_mostrado} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar {nombre_mostrado}: {e}")
        return False

def verificar_paquete(paquete):
    """Verificar si un paquete está instalado"""
    try:
        __import__(paquete)
        return True
    except ImportError:
        return False

def main():
    print("🔧 Instalador de Dependencias - Gestor de Descargas")
    print("=" * 60)
    
    # Lista de paquetes necesarios
    paquetes = [
        ("psutil", "psutil (Información del sistema)"),
        ("reportlab", "ReportLab (Generación de PDFs)")
    ]
    
    print("📋 Verificando dependencias...")
    
    paquetes_faltantes = []
    for paquete, nombre in paquetes:
        if verificar_paquete(paquete):
            print(f"✅ {nombre} ya está instalado")
        else:
            print(f"❌ {nombre} no está instalado")
            paquetes_faltantes.append((paquete, nombre))
    
    if not paquetes_faltantes:
        print("\n🎉 ¡Todas las dependencias están instaladas!")
        print("💡 Puedes ejecutar: python info_sistema.py")
        return
    
    print(f"\n📦 Se encontraron {len(paquetes_faltantes)} paquetes faltantes")
    
    # Preguntar si instalar
    respuesta = input("\n¿Deseas instalar los paquetes faltantes? (s/n): ").lower().strip()
    
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Instalación cancelada")
        return
    
    print("\n🚀 Iniciando instalación...")
    
    # Instalar paquetes faltantes
    exitosos = 0
    for paquete, nombre in paquetes_faltantes:
        if instalar_paquete(paquete, nombre):
            exitosos += 1
        print()  # Línea en blanco
    
    print("=" * 60)
    print(f"📊 Resumen de instalación:")
    print(f"✅ Paquetes instalados: {exitosos}")
    print(f"❌ Paquetes fallidos: {len(paquetes_faltantes) - exitosos}")
    
    if exitosos == len(paquetes_faltantes):
        print("\n🎉 ¡Todas las dependencias se instalaron correctamente!")
        print("💡 Ahora puedes ejecutar: python info_sistema.py")
    else:
        print("\n⚠️  Algunos paquetes no se pudieron instalar.")
        print("💡 Intenta instalarlos manualmente:")
        for paquete, nombre in paquetes_faltantes:
            print(f"   pip install {paquete}")

if __name__ == "__main__":
    main()
