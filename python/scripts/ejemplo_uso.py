#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso del Gestor de Archivos de Descargas
Este script demuestra cómo usar las funciones del programa
"""

from gestor_descargas import GestorDescargas
import os

def ejemplo_basico():
    """Ejemplo básico de uso del gestor"""
    print("🚀 EJEMPLO BÁSICO DE USO")
    print("=" * 50)
    
    # Crear instancia del gestor
    gestor = GestorDescargas()
    
    print(f"📂 Carpeta de descargas: {gestor.descargas_path}")
    
    # Mostrar archivos
    print("\n1️⃣ Mostrando archivos en la carpeta de descargas:")
    gestor.mostrar_archivos()
    
    # Buscar archivos
    print("\n2️⃣ Buscando archivos que contengan 'documento':")
    gestor.buscar_archivos("documento")
    
    # Mostrar estadísticas
    print("\n3️⃣ Mostrando estadísticas:")
    archivos = []
    for item in gestor.descargas_path.iterdir():
        if item.is_file():
            archivos.append({
                'extension': item.suffix.lower(),
                'tamaño': item.stat().st_size
            })
    gestor.mostrar_estadisticas(archivos)

def ejemplo_organizacion():
    """Ejemplo de organización de archivos"""
    print("\n🗂️ EJEMPLO DE ORGANIZACIÓN")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    print("Antes de organizar:")
    gestor.mostrar_archivos()
    
    print("\nOrganizando archivos...")
    # Nota: En un ejemplo real, esto movería los archivos
    # gestor.organizar_archivos()
    print("✅ Archivos organizados (simulado)")

def ejemplo_limpieza():
    """Ejemplo de limpieza de archivos"""
    print("\n🧹 EJEMPLO DE LIMPIEZA")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    print("Limpiando archivos más antiguos de 7 días...")
    # Nota: En un ejemplo real, esto eliminaría archivos
    # gestor.limpiar_archivos_antiguos(7)
    print("✅ Limpieza completada (simulado)")

def crear_archivos_ejemplo():
    """Crea algunos archivos de ejemplo para demostrar"""
    print("\n📝 CREANDO ARCHIVOS DE EJEMPLO")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    # Crear algunos archivos de ejemplo
    archivos_ejemplo = [
        "documento_ejemplo.txt",
        "imagen_ejemplo.jpg",
        "video_ejemplo.mp4",
        "audio_ejemplo.mp3",
        "comprimido_ejemplo.zip"
    ]
    
    for archivo in archivos_ejemplo:
        ruta_archivo = gestor.descargas_path / archivo
        if not ruta_archivo.exists():
            try:
                with open(ruta_archivo, 'w') as f:
                    f.write(f"Este es un archivo de ejemplo: {archivo}")
                print(f"✅ Creado: {archivo}")
            except Exception as e:
                print(f"❌ Error creando {archivo}: {e}")
        else:
            print(f"⚠️ Ya existe: {archivo}")

def main():
    """Función principal del ejemplo"""
    print("🎯 EJEMPLOS DE USO DEL GESTOR DE DESCARGAS")
    print("=" * 60)
    
    # Crear archivos de ejemplo
    crear_archivos_ejemplo()
    
    # Ejecutar ejemplos
    ejemplo_basico()
    ejemplo_organizacion()
    ejemplo_limpieza()
    
    print("\n" + "=" * 60)
    print("🎉 ¡Ejemplos completados!")
    print("💡 Para usar el programa completo, ejecuta: python gestor_descargas.py")

if __name__ == "__main__":
    main()
