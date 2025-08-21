#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de Manejo de Archivos Duplicados
Este script crea archivos duplicados y prueba la nueva funcionalidad
"""

from gestor_descargas import GestorDescargas
import os

def crear_archivos_duplicados():
    """Crea archivos duplicados para probar la funcionalidad"""
    print("🧪 CREANDO ARCHIVOS DUPLICADOS PARA PRUEBA")
    print("=" * 60)
    
    gestor = GestorDescargas()
    
    # Archivos que vamos a crear (algunos duplicados)
    archivos_duplicados = [
        "documento_importante.pdf",
        "documento_importante.pdf",  # Duplicado
        "presentacion_ventas.pptx",
        "presentacion_ventas.pptx",  # Duplicado
        "datos_clientes.xlsx",
        "datos_clientes.xlsx",       # Duplicado
        "datos_clientes.xlsx",       # Triplicado
        "notas_reunion.txt",
        "notas_reunion.txt",         # Duplicado
        "imagen_producto.jpg",
        "imagen_producto.jpg",       # Duplicado
        "archivo_unico.docx"         # Único
    ]
    
    print("📝 Creando archivos duplicados...")
    archivos_creados = 0
    
    for i, nombre_archivo in enumerate(archivos_duplicados):
        ruta_archivo = gestor.descargas_path / nombre_archivo
        if not ruta_archivo.exists():
            try:
                # Crear contenido de ejemplo
                contenido = f"Este es el archivo: {nombre_archivo}\n"
                contenido += f"Índice de creación: {i + 1}\n"
                contenido += f"Fecha de creación: {gestor.descargas_path}\n"
                contenido += "=" * 50 + "\n"
                contenido += "Contenido de prueba para verificar el manejo de duplicados.\n"
                contenido += "Este archivo será organizado y el programa debería manejar los duplicados.\n"
                
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                print(f"  ✅ Creado: {nombre_archivo}")
                archivos_creados += 1
            except Exception as e:
                print(f"  ❌ Error creando {nombre_archivo}: {e}")
        else:
            print(f"  ⚠️ Ya existe: {nombre_archivo}")
    
    print(f"\n📊 Total de archivos creados: {archivos_creados}")
    return archivos_creados

def probar_generacion_nombres():
    """Prueba la generación de nombres únicos"""
    print("\n🔍 PRUEBA DE GENERACIÓN DE NOMBRES ÚNICOS")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    # Crear algunos archivos de prueba en una carpeta temporal
    carpeta_test = gestor.descargas_path / "test_duplicados"
    carpeta_test.mkdir(exist_ok=True)
    
    # Crear archivos existentes
    archivos_existentes = [
        "documento.pdf",
        "documento_v1.pdf",
        "documento_v2.pdf",
        "presentacion.pptx",
        "presentacion_v1.pptx"
    ]
    
    print("📝 Creando archivos existentes para la prueba:")
    for archivo in archivos_existentes:
        ruta_archivo = carpeta_test / archivo
        with open(ruta_archivo, 'w') as f:
            f.write(f"Archivo existente: {archivo}")
        print(f"  ✅ Creado: {archivo}")
    
    # Probar generación de nombres únicos
    nombres_prueba = [
        "documento.pdf",
        "presentacion.pptx",
        "nuevo_archivo.docx"
    ]
    
    print("\n🔍 Probando generación de nombres únicos:")
    for nombre in nombres_prueba:
        nuevo_nombre = gestor.generar_nombre_unico(nombre, carpeta_test)
        print(f"  📄 {nombre} → {nuevo_nombre}")
    
    # Limpiar carpeta de prueba
    import shutil
    shutil.rmtree(carpeta_test)
    print("\n🧹 Carpeta de prueba eliminada")

def demostrar_organizacion_con_duplicados():
    """Demuestra la organización con archivos duplicados"""
    print("\n🗂️ DEMOSTRACIÓN DE ORGANIZACIÓN CON DUPLICADOS")
    print("=" * 60)
    
    gestor = GestorDescargas()
    
    # Contar archivos antes de organizar
    archivos_antes = []
    for item in gestor.descargas_path.iterdir():
        if item.is_file():
            archivos_antes.append(item)
    
    if not archivos_antes:
        print("📭 No hay archivos para organizar")
        return
    
    print(f"📊 Archivos encontrados: {len(archivos_antes)}")
    
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
    confirmar = input(f"\n¿Quieres organizar {len(archivos_antes)} archivos (incluyendo duplicados)? (s/n): ").lower()
    if confirmar != 's':
        print("❌ Organización cancelada")
        return
    
    # Ejecutar organización
    print("\n🗂️ Organizando archivos...")
    print("💡 Cuando encuentre duplicados, te preguntará qué hacer:")
    print("   1. 📝 Cambiar nombre automáticamente (agregar versión)")
    print("   2. 🔄 Sobrescribir el archivo existente")
    print("   3. ❌ Saltar este archivo")
    print()
    
    gestor.organizar_archivos()

def main():
    """Función principal de la prueba de duplicados"""
    print("🚀 PRUEBA DE MANEJO DE ARCHIVOS DUPLICADOS")
    print("=" * 60)
    print("Este script prueba la nueva funcionalidad de manejo")
    print("de archivos duplicados durante la organización.")
    print("=" * 60)
    
    # Crear archivos duplicados
    archivos_creados = crear_archivos_duplicados()
    
    if archivos_creados == 0:
        print("\n❌ No se pudieron crear archivos duplicados")
        return
    
    # Probar generación de nombres únicos
    probar_generacion_nombres()
    
    # Demostrar organización con duplicados
    demostrar_organizacion_con_duplicados()
    
    print("\n" + "=" * 60)
    print("🎉 ¡PRUEBA DE DUPLICADOS COMPLETADA!")
    print("=" * 60)
    print("💡 La nueva funcionalidad maneja duplicados de forma inteligente:")
    print("   ✅ Detecta archivos duplicados automáticamente")
    print("   ✅ Pregunta qué hacer con cada duplicado")
    print("   ✅ Opción 1: Cambia nombre automáticamente (ej: documento_v1.pdf)")
    print("   ✅ Opción 2: Sobrescribe el archivo existente")
    print("   ✅ Opción 3: Salta el archivo duplicado")
    print("   ✅ Genera nombres únicos incrementales (v1, v2, v3, etc.)")
    print("\n🔧 Para usar la funcionalidad mejorada:")
    print("   Ejecuta: python gestor_descargas.py")
    print("   Selecciona la opción 3: 🗂️ Organizar archivos por tipo")
    print("   O la opción 6: 🎯 Organización automática completa")

if __name__ == "__main__":
    main()
