#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración de la Organización Automática de Archivos
Este script crea archivos de ejemplo y demuestra la nueva funcionalidad
"""

from gestor_descargas import GestorDescargas
import os
import random

def crear_archivos_ejemplo_organizacion():
    """Crea archivos de ejemplo de diferentes tipos para demostrar la organización"""
    print("🎯 DEMOSTRACIÓN DE ORGANIZACIÓN AUTOMÁTICA")
    print("=" * 60)
    
    gestor = GestorDescargas()
    
    # Archivos de ejemplo por categoría
    archivos_ejemplo = {
        "imagenes": [
            "foto_vacaciones.jpg",
            "logo_empresa.png",
            "icono_app.ico",
            "dibujo_arte.svg",
            "captura_pantalla.png"
        ],
        "documentos": [
            "informe_2024.pdf",
            "presupuesto.xlsx",
            "presentacion_ventas.pptx",
            "notas_importantes.txt",
            "datos_clientes.csv"
        ],
        "videos": [
            "tutorial_python.mp4",
            "video_familiar.avi",
            "conferencia_online.webm",
            "musica_video.m4v"
        ],
        "audio": [
            "mi_cancion_favorita.mp3",
            "podcast_tecnologia.wav",
            "sonido_notificacion.ogg",
            "musica_flac.flac"
        ],
        "comprimidos": [
            "backup_datos.zip",
            "archivos_importantes.rar",
            "proyecto_completo.7z",
            "sistema_operativo.iso"
        ],
        "ejecutables": [
            "instalador_programa.exe",
            "actualizacion_sistema.msi",
            "script_automatizacion.bat",
            "aplicacion_mac.dmg"
        ],
        "otros": [
            "archivo_desconocido.xyz",
            "datos_binarios.bin",
            "configuracion.cfg"
        ]
    }
    
    print("📝 Creando archivos de ejemplo...")
    archivos_creados = 0
    
    for categoria, archivos in archivos_ejemplo.items():
        for archivo in archivos:
            ruta_archivo = gestor.descargas_path / archivo
            if not ruta_archivo.exists():
                try:
                    # Crear contenido de ejemplo
                    contenido = f"Este es un archivo de ejemplo de tipo {categoria}: {archivo}\n"
                    contenido += f"Fecha de creación: {gestor.descargas_path}\n"
                    contenido += "=" * 50 + "\n"
                    
                    with open(ruta_archivo, 'w', encoding='utf-8') as f:
                        f.write(contenido)
                    
                    print(f"  ✅ Creado: {archivo}")
                    archivos_creados += 1
                except Exception as e:
                    print(f"  ❌ Error creando {archivo}: {e}")
            else:
                print(f"  ⚠️ Ya existe: {archivo}")
    
    print(f"\n📊 Total de archivos creados: {archivos_creados}")
    return archivos_creados

def mostrar_antes_despues():
    """Muestra el estado antes y después de la organización"""
    gestor = GestorDescargas()
    
    print("\n📋 ESTADO ANTES DE LA ORGANIZACIÓN:")
    print("-" * 40)
    gestor.mostrar_archivos()
    
    print("\n" + "=" * 60)
    print("🎯 EJECUTANDO ORGANIZACIÓN AUTOMÁTICA...")
    print("=" * 60)
    
    # Ejecutar organización automática
    gestor.organizacion_automatica_completa()
    
    print("\n📋 ESTADO DESPUÉS DE LA ORGANIZACIÓN:")
    print("-" * 40)
    gestor.mostrar_archivos()

def mostrar_estructura_final():
    """Muestra la estructura final de carpetas creadas"""
    gestor = GestorDescargas()
    
    print("\n📁 ESTRUCTURA FINAL DE CARPETAS:")
    print("=" * 40)
    
    for categoria in gestor.categorias.keys():
        carpeta = gestor.descargas_path / categoria
        if carpeta.exists():
            archivos = [f for f in carpeta.iterdir() if f.is_file()]
            if archivos:
                print(f"\n📂 {categoria.upper()}/")
                for archivo in archivos:
                    tamaño = gestor.formatear_tamaño(archivo.stat().st_size)
                    print(f"  📄 {archivo.name} ({tamaño})")

def main():
    """Función principal de la demostración"""
    print("🚀 DEMOSTRACIÓN DE ORGANIZACIÓN AUTOMÁTICA")
    print("=" * 60)
    print("Este script demostrará cómo funciona la nueva opción")
    print("de organización automática completa.")
    print("=" * 60)
    
    # Crear archivos de ejemplo
    archivos_creados = crear_archivos_ejemplo_organizacion()
    
    if archivos_creados == 0:
        print("\n❌ No se pudieron crear archivos de ejemplo")
        return
    
    # Mostrar proceso completo
    mostrar_antes_despues()
    
    # Mostrar estructura final
    mostrar_estructura_final()
    
    print("\n" + "=" * 60)
    print("🎉 ¡DEMOSTRACIÓN COMPLETADA!")
    print("=" * 60)
    print("💡 Características de la nueva organización automática:")
    print("   ✅ Organiza automáticamente por tipo de archivo")
    print("   ✅ Muestra información detallada antes de organizar")
    print("   ✅ Confirma la acción antes de proceder")
    print("   ✅ Proporciona un resumen completo")
    print("   ✅ Maneja errores de forma segura")
    print("   ✅ Crea carpetas automáticamente")
    print("\n🔧 Para usar esta función en el programa principal:")
    print("   Ejecuta: python gestor_descargas.py")
    print("   Selecciona la opción 6: 🎯 Organización automática completa")

if __name__ == "__main__":
    main()
