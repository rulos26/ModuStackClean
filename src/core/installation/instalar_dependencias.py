#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para instalar dependencias del Gestor de Descargas
Instala las librerías necesarias para el funcionamiento completo
"""

import subprocess
import sys
import os

def instalar_paquete(paquete, nombre_mostrado=None):
    """Instala un paquete usando pip"""
    if nombre_mostrado is None:
        nombre_mostrado = paquete
    
    print(f"📦 Instalando {nombre_mostrado}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"✅ {nombre_mostrado} instalado correctamente")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Error al instalar {nombre_mostrado}")
        return False

def verificar_paquete(paquete):
    """Verifica si un paquete está instalado"""
    try:
        __import__(paquete)
        return True
    except ImportError:
        return False

def main():
    print("🔧 INSTALADOR DE DEPENDENCIAS - GESTOR DE DESCARGAS")
    print("=" * 60)
    print()
    
    # Lista de paquetes necesarios
    paquetes = [
        ("psutil", "psutil (Información del sistema)"),
        ("reportlab", "ReportLab (Generación de PDFs)"),
        ("matplotlib", "Matplotlib (Gráficos)"),
        ("numpy", "NumPy (Cálculos numéricos)")
    ]
    
    print("📋 Verificando paquetes instalados...")
    print()
    
    paquetes_faltantes = []
    
    for paquete, nombre in paquetes:
        if verificar_paquete(paquete):
            print(f"✅ {nombre} - Ya instalado")
        else:
            print(f"❌ {nombre} - No instalado")
            paquetes_faltantes.append((paquete, nombre))
    
    print()
    
    if not paquetes_faltantes:
        print("🎉 ¡Todos los paquetes están instalados!")
        print("✅ El Gestor de Descargas está listo para usar")
        return
    
    print(f"📦 Se encontraron {len(paquetes_faltantes)} paquetes faltantes")
    print()
    
    # Preguntar si instalar
    respuesta = input("¿Deseas instalar los paquetes faltantes? (s/n): ").lower().strip()
    
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Instalación cancelada")
        return
    
    print()
    print("🚀 Iniciando instalación...")
    print()
    
    # Instalar paquetes faltantes
    exitosos = 0
    fallidos = 0
    
    for paquete, nombre in paquetes_faltantes:
        if instalar_paquete(paquete, nombre):
            exitosos += 1
        else:
            fallidos += 1
        print()
    
    # Resumen
    print("=" * 60)
    print("📊 RESUMEN DE INSTALACIÓN:")
    print(f"✅ Paquetes instalados exitosamente: {exitosos}")
    print(f"❌ Paquetes con errores: {fallidos}")
    print()
    
    if fallidos == 0:
        print("🎉 ¡Instalación completada exitosamente!")
        print("✅ El Gestor de Descargas está listo para usar")
    else:
        print("⚠️  Algunos paquetes no se pudieron instalar")
        print("💡 Puedes intentar instalarlos manualmente:")
        print("   pip install psutil reportlab matplotlib numpy")
    
    print()
    print("📝 FUNCIONALIDADES DISPONIBLES:")
    print("  🔧 info_sistema.py - Información detallada del sistema")
    print("  📁 gestor_descargas.py - Gestión de archivos de descarga")
    print("  🌐 index.php - Interfaz web")
    print()
    print("🚀 Para usar el script de información del sistema:")
    print("   python info_sistema.py")

if __name__ == "__main__":
    main()
