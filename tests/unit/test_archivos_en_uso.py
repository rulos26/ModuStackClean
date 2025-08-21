#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de Manejo de Archivos en Uso
Este script prueba la nueva funcionalidad de cerrar procesos
y reintentar mover archivos que están siendo utilizados
"""

from gestor_descargas import GestorDescargas
import os
import time
import subprocess
import sys

def crear_archivo_y_abrir(gestor, nombre_archivo):
    """Crea un archivo y lo abre con el programa predeterminado"""
    gestor = GestorDescargas()
    ruta_archivo = gestor.descargas_path / nombre_archivo
    
    # Crear contenido de ejemplo
    contenido = f"Este es el archivo: {nombre_archivo}\n"
    contenido += "Este archivo está siendo usado por otro programa.\n"
    contenido += "El gestor debería intentar cerrar el proceso y moverlo.\n"
    contenido += "=" * 50 + "\n"
    
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"  ✅ Creado: {nombre_archivo}")
    
    # Intentar abrir el archivo con el programa predeterminado
    try:
        if sys.platform == "win32":
            os.startfile(ruta_archivo)
        else:
            subprocess.run(['xdg-open', str(ruta_archivo)], capture_output=True)
        print(f"  🔄 Abierto: {nombre_archivo}")
        return True
    except Exception as e:
        print(f"  ⚠️ No se pudo abrir: {nombre_archivo} - {e}")
        return False

def probar_cierre_procesos():
    """Prueba la función de cierre de procesos"""
    print("\n🔍 PRUEBA DE CIERRE DE PROCESOS")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    # Crear archivos de prueba
    archivos_prueba = [
        "documento_en_uso.pdf",
        "imagen_en_uso.jpg",
        "texto_en_uso.txt"
    ]
    
    print("📝 Creando archivos de prueba...")
    archivos_abiertos = []
    
    for archivo in archivos_prueba:
        if crear_archivo_y_abrir(gestor, archivo):
            archivos_abiertos.append(archivo)
    
    if not archivos_abiertos:
        print("❌ No se pudieron abrir archivos para la prueba")
        return
    
    print(f"\n📊 Archivos abiertos: {len(archivos_abiertos)}")
    print("💡 Los archivos están abiertos en sus programas predeterminados")
    
    # Esperar un poco para que se abran los archivos
    print("⏳ Esperando 3 segundos para que se abran los archivos...")
    time.sleep(3)
    
    # Probar la función de cierre de procesos
    print("\n🔍 Probando cierre de procesos...")
    for archivo in archivos_abiertos:
        ruta_archivo = gestor.descargas_path / archivo
        print(f"\n📄 Probando: {archivo}")
        
        if gestor.intentar_cerrar_procesos_archivo(str(ruta_archivo)):
            print(f"  ✅ Procesos cerrados para: {archivo}")
        else:
            print(f"  ⚠️ No se encontraron procesos para: {archivo}")
    
    # Limpiar archivos de prueba
    print("\n🧹 Limpiando archivos de prueba...")
    for archivo in archivos_prueba:
        ruta_archivo = gestor.descargas_path / archivo
        if ruta_archivo.exists():
            try:
                ruta_archivo.unlink()
                print(f"  🗑️ Eliminado: {archivo}")
            except Exception as e:
                print(f"  ❌ Error eliminando {archivo}: {e}")

def probar_movimiento_con_reintentos():
    """Prueba la función de movimiento con reintentos"""
    print("\n🔄 PRUEBA DE MOVIMIENTO CON REINTENTOS")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    # Crear un archivo de prueba
    archivo_prueba = "archivo_para_mover.txt"
    ruta_archivo = gestor.descargas_path / archivo_prueba
    
    # Crear contenido
    contenido = "Este archivo será movido con reintentos.\n"
    contenido += "Primero se abrirá para simular que está en uso.\n"
    
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"  ✅ Creado: {archivo_prueba}")
    
    # Abrir el archivo
    try:
        if sys.platform == "win32":
            os.startfile(ruta_archivo)
        else:
            subprocess.run(['xdg-open', str(ruta_archivo)], capture_output=True)
        print(f"  🔄 Abierto: {archivo_prueba}")
    except Exception as e:
        print(f"  ⚠️ No se pudo abrir: {archivo_prueba}")
    
    # Esperar un poco
    print("⏳ Esperando 2 segundos...")
    time.sleep(2)
    
    # Crear carpeta de destino
    carpeta_destino = gestor.descargas_path / "test_movimiento"
    carpeta_destino.mkdir(exist_ok=True)
    
    destino = carpeta_destino / archivo_prueba
    
    print(f"\n🔄 Intentando mover: {archivo_prueba} → test_movimiento/")
    
    # Probar movimiento con reintentos
    if gestor.mover_archivo_con_reintentos(ruta_archivo, destino):
        print(f"  ✅ Movimiento exitoso: {archivo_prueba}")
    else:
        print(f"  ❌ No se pudo mover: {archivo_prueba}")
    
    # Limpiar
    if carpeta_destino.exists():
        import shutil
        shutil.rmtree(carpeta_destino)
        print("  🧹 Carpeta de prueba eliminada")

def demostrar_organizacion_con_archivos_en_uso():
    """Demuestra la organización con archivos en uso"""
    print("\n🗂️ DEMOSTRACIÓN DE ORGANIZACIÓN CON ARCHIVOS EN USO")
    print("=" * 60)
    
    gestor = GestorDescargas()
    
    # Crear archivos que estarán en uso
    archivos_en_uso = [
        "documento_abierto.pdf",
        "imagen_abierta.jpg",
        "texto_abierto.txt"
    ]
    
    print("📝 Creando archivos que estarán en uso...")
    for archivo in archivos_en_uso:
        crear_archivo_y_abrir(gestor, archivo)
    
    # Esperar un poco
    print("⏳ Esperando 3 segundos para que se abran los archivos...")
    time.sleep(3)
    
    # Contar archivos antes de organizar
    archivos_antes = []
    for item in gestor.descargas_path.iterdir():
        if item.is_file():
            archivos_antes.append(item)
    
    if not archivos_antes:
        print("📭 No hay archivos para organizar")
        return
    
    print(f"\n📊 Archivos encontrados: {len(archivos_antes)}")
    
    # Mostrar archivos que se van a organizar
    print("\n📋 Archivos que se organizarán:")
    for archivo in archivos_antes:
        extension = gestor.obtener_extension_real(archivo.name)
        tipo = gestor.obtener_tipo_archivo(extension)
        
        if tipo == "documentos":
            subcategoria = gestor.obtener_subcategoria_documento(extension)
            print(f"  📄 {archivo.name} → {tipo}/{subcategoria}/")
        else:
            print(f"  📄 {archivo.name} → {tipo}/")
    
    # Confirmar organización
    confirmar = input(f"\n¿Quieres organizar {len(archivos_antes)} archivos (algunos pueden estar en uso)? (s/n): ").lower()
    if confirmar != 's':
        print("❌ Organización cancelada")
        return
    
    # Ejecutar organización
    print("\n🗂️ Organizando archivos...")
    print("💡 Si algún archivo está en uso, el programa intentará:")
    print("   1. 🔄 Cerrar los procesos que lo usan")
    print("   2. ⏳ Esperar 2 segundos")
    print("   3. 🔄 Reintentar el movimiento")
    print("   4. ❌ Si falla después de 3 intentos, lo reporta")
    print()
    
    gestor.organizar_archivos()

def main():
    """Función principal de la prueba de archivos en uso"""
    print("🚀 PRUEBA DE MANEJO DE ARCHIVOS EN USO")
    print("=" * 60)
    print("Este script prueba la nueva funcionalidad de manejo")
    print("de archivos que están siendo utilizados por otros programas.")
    print("=" * 60)
    
    # Probar cierre de procesos
    probar_cierre_procesos()
    
    # Probar movimiento con reintentos
    probar_movimiento_con_reintentos()
    
    # Demostrar organización con archivos en uso
    demostrar_organizacion_con_archivos_en_uso()
    
    print("\n" + "=" * 60)
    print("🎉 ¡PRUEBA DE ARCHIVOS EN USO COMPLETADA!")
    print("=" * 60)
    print("💡 La nueva funcionalidad maneja archivos en uso de forma inteligente:")
    print("   ✅ Detecta cuando un archivo está siendo usado")
    print("   ✅ Intenta cerrar los procesos que lo usan")
    print("   ✅ Espera un tiempo para que se libere")
    print("   ✅ Reintenta el movimiento hasta 3 veces")
    print("   ✅ Reporta claramente si no se puede mover")
    print("\n🔧 Para usar la funcionalidad mejorada:")
    print("   Ejecuta: python gestor_descargas.py")
    print("   Selecciona la opción 3: 🗂️ Organizar archivos por tipo")
    print("   O la opción 6: 🎯 Organización automática completa")

if __name__ == "__main__":
    main()
