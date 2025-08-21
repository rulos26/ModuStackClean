#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de detección de archivos problemáticos
Este script prueba la nueva funcionalidad de detección de extensiones
"""

from gestor_descargas import GestorDescargas
from pathlib import Path

def probar_deteccion_extension():
    """Prueba la detección de extensiones en archivos problemáticos"""
    print("🔍 PRUEBA DE DETECCIÓN DE EXTENSIONES")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    # Archivos de prueba con nombres problemáticos
    archivos_prueba = [
        "32_Beltran_B_Luis_C_Firmado.pdArchivos: carta_recomendacion.docx, datos_binarios.doc, ...",
        "documento_normal.pdf",
        "archivo_con_espacios en el nombre.txt",
        "archivo_con_puntos.múltiples.en.el.nombre.docx",
        "archivo_sin_extension",
        "archivo_con_extension_falsa.txt.fake",
        "archivo_con_extension_en_medio.nombre.pdf.extra"
    ]
    
    print("📋 Probando detección de extensiones:")
    print("-" * 50)
    
    for nombre_archivo in archivos_prueba:
        extension_detectada = gestor.obtener_extension_real(nombre_archivo)
        tipo_archivo = gestor.obtener_tipo_archivo(extension_detectada)
        
        print(f"📄 {nombre_archivo}")
        print(f"   🔍 Extensión detectada: {extension_detectada}")
        print(f"   📁 Tipo de archivo: {tipo_archivo}")
        
        if tipo_archivo == "documentos":
            subcategoria = gestor.obtener_subcategoria_documento(extension_detectada)
            print(f"   📂 Subcategoría: {subcategoria}")
        
        print()

def probar_archivos_reales():
    """Prueba con archivos reales en la carpeta de descargas"""
    print("🔍 PRUEBA CON ARCHIVOS REALES")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    print("📋 Archivos en la carpeta de descargas:")
    print("-" * 50)
    
    archivos_problematicos = []
    
    for item in gestor.descargas_path.iterdir():
        if item.is_file():
            extension_original = item.suffix.lower()
            extension_detectada = gestor.obtener_extension_real(item.name)
            tipo_archivo = gestor.obtener_tipo_archivo(extension_detectada)
            
            # Verificar si hay diferencia en la detección
            if extension_original != extension_detectada:
                archivos_problematicos.append(item.name)
                print(f"⚠️  ARCHIVO PROBLEMÁTICO DETECTADO:")
                print(f"   📄 Nombre: {item.name}")
                print(f"   🔍 Extensión original: {extension_original}")
                print(f"   🔍 Extensión detectada: {extension_detectada}")
                print(f"   📁 Tipo: {tipo_archivo}")
                if tipo_archivo == "documentos":
                    subcategoria = gestor.obtener_subcategoria_documento(extension_detectada)
                    print(f"   📂 Subcategoría: {subcategoria}")
                print()
            else:
                print(f"✅ {item.name} → {extension_detectada} ({tipo_archivo})")
    
    if archivos_problematicos:
        print(f"\n🎯 Se encontraron {len(archivos_problematicos)} archivos problemáticos:")
        for archivo in archivos_problematicos:
            print(f"   📄 {archivo}")
    else:
        print("\n✅ No se encontraron archivos problemáticos")

def main():
    """Función principal de la prueba"""
    print("🚀 PRUEBA DE DETECCIÓN DE ARCHIVOS PROBLEMÁTICOS")
    print("=" * 60)
    print("Este script prueba la nueva funcionalidad de detección")
    print("de extensiones en archivos con nombres problemáticos.")
    print("=" * 60)
    
    # Probar con archivos de ejemplo
    probar_deteccion_extension()
    
    print("\n" + "=" * 60)
    
    # Probar con archivos reales
    probar_archivos_reales()
    
    print("\n" + "=" * 60)
    print("🎉 ¡PRUEBA COMPLETADA!")
    print("=" * 60)
    print("💡 La nueva funcionalidad debería detectar correctamente")
    print("   archivos con nombres problemáticos como el que viste.")
    print("\n🔧 Para usar la funcionalidad mejorada:")
    print("   Ejecuta: python gestor_descargas.py")
    print("   Selecciona la opción 6: 🎯 Organización automática completa")

if __name__ == "__main__":
    main()
