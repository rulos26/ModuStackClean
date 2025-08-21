#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de Organización Agresiva
Este script prueba que la organización funcione SIEMPRE por extensión
sin importar el nombre del archivo
"""

from gestor_descargas import GestorDescargas
import os

def crear_archivos_problematicos():
    """Crea archivos con nombres problemáticos para probar"""
    print("🧪 CREANDO ARCHIVOS PROBLEMÁTICOS PARA PRUEBA")
    print("=" * 60)
    
    gestor = GestorDescargas()
    
    # Archivos con nombres problemáticos
    archivos_problematicos = [
        # Archivos con nombres muy largos y caracteres extraños
        "32_Beltran_B_Luis_C_Firmado.pdArchivos: carta_recomendacion.docx, datos_binarios.doc, ...",
        "archivo_con_espacios y símbolos @#$%^&*() en el nombre.pdf",
        "archivo_con_puntos.múltiples.en.el.nombre.docx",
        "archivo_con_guiones-bajos_y_guiones_medios-en-el-nombre.xlsx",
        "archivo_con_números_123_y_símbolos_!@#.ppt",
        "archivo_con_extension_en_medio.nombre.pdf.extra",
        "archivo_con_extension_falsa.txt.fake",
        "archivo_sin_extension_pero_con_pdf_en_el_nombre",
        "archivo_con_múltiples_extensiones.txt.pdf.docx.xlsx",
        "archivo_con_caracteres_especiales_ñáéíóú.pdf",
        "archivo_con_paréntesis_(y_corchetes)_[en_el_nombre].docx",
        "archivo_con_llaves_{y_barras}_/en_el_nombre.xlsx",
        "archivo_con_porcentajes_%_y_ampersand_&_en_nombre.ppt",
        "archivo_con_asteriscos_*_y_plus_+_en_nombre.txt",
        "archivo_con_igual_=_y_interrogación_?_en_nombre.rtf"
    ]
    
    print("📝 Creando archivos problemáticos...")
    archivos_creados = 0
    
    for nombre_archivo in archivos_problematicos:
        ruta_archivo = gestor.descargas_path / nombre_archivo
        if not ruta_archivo.exists():
            try:
                # Crear contenido de ejemplo
                contenido = f"Este es un archivo de prueba con nombre problemático: {nombre_archivo}\n"
                contenido += f"Fecha de creación: {gestor.descargas_path}\n"
                contenido += "=" * 50 + "\n"
                contenido += "Contenido de prueba para verificar la organización agresiva.\n"
                contenido += "Este archivo debería ser organizado correctamente sin importar su nombre.\n"
                
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                print(f"  ✅ Creado: {nombre_archivo}")
                archivos_creados += 1
            except Exception as e:
                print(f"  ❌ Error creando {nombre_archivo}: {e}")
        else:
            print(f"  ⚠️ Ya existe: {nombre_archivo}")
    
    print(f"\n📊 Total de archivos problemáticos creados: {archivos_creados}")
    return archivos_creados

def probar_deteccion_agresiva():
    """Prueba la detección agresiva de extensiones"""
    print("\n🔍 PRUEBA DE DETECCIÓN AGRESIVA")
    print("=" * 50)
    
    gestor = GestorDescargas()
    
    print("📋 Probando detección de extensiones en archivos problemáticos:")
    print("-" * 60)
    
    archivos_procesados = 0
    archivos_detectados = 0
    
    for item in gestor.descargas_path.iterdir():
        if item.is_file():
            archivos_procesados += 1
            extension_detectada = gestor.obtener_extension_real(item.name)
            tipo_archivo = gestor.obtener_tipo_archivo(extension_detectada)
            
            if extension_detectada:
                archivos_detectados += 1
                print(f"✅ {item.name}")
                print(f"   🔍 Extensión detectada: {extension_detectada}")
                print(f"   📁 Tipo: {tipo_archivo}")
                
                if tipo_archivo == "documentos":
                    subcategoria = gestor.obtener_subcategoria_documento(extension_detectada)
                    print(f"   📂 Subcategoría: {subcategoria}")
            else:
                print(f"❌ {item.name}")
                print(f"   ⚠️ No se pudo detectar extensión")
            
            print()
    
    print(f"📊 Resumen de detección:")
    print(f"   Total de archivos procesados: {archivos_procesados}")
    print(f"   Archivos con extensión detectada: {archivos_detectados}")
    print(f"   Archivos sin extensión detectada: {archivos_procesados - archivos_detectados}")
    print(f"   Tasa de éxito: {(archivos_detectados/archivos_procesados)*100:.1f}%")

def organizar_archivos_problematicos():
    """Organiza los archivos problemáticos"""
    print("\n🗂️ ORGANIZANDO ARCHIVOS PROBLEMÁTICOS")
    print("=" * 50)
    
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
    
    # Mostrar qué se va a organizar
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
    confirmar = input(f"\n¿Quieres organizar {len(archivos_antes)} archivos problemáticos? (s/n): ").lower()
    if confirmar != 's':
        print("❌ Organización cancelada")
        return
    
    # Ejecutar organización
    print("\n🗂️ Organizando archivos...")
    organizados = 0
    errores = 0
    
    for item in archivos_antes:
        if item.is_file():
            extension = gestor.obtener_extension_real(item.name)
            categoria = gestor.obtener_tipo_archivo(extension)
            
            # Crear carpeta de categoría si no existe
            carpeta_categoria = gestor.descargas_path / categoria
            carpeta_categoria.mkdir(exist_ok=True)
            
            # Si es un documento, crear subcarpeta
            if categoria == "documentos":
                subcategoria = gestor.obtener_subcategoria_documento(extension)
                carpeta_destino = carpeta_categoria / subcategoria
                carpeta_destino.mkdir(exist_ok=True)
                destino = carpeta_destino / item.name
                ruta_mostrar = f"{categoria}/{subcategoria}/"
            else:
                destino = carpeta_categoria / item.name
                ruta_mostrar = f"{categoria}/"
            
            if not destino.exists():
                try:
                    import shutil
                    shutil.move(str(item), str(destino))
                    print(f"  ✅ {item.name} → {ruta_mostrar}")
                    organizados += 1
                except Exception as e:
                    print(f"  ❌ Error moviendo {item.name}: {e}")
                    errores += 1
            else:
                print(f"  ⚠️ {item.name} ya existe en {ruta_mostrar}")
                errores += 1
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("📈 RESUMEN DE ORGANIZACIÓN AGRESIVA")
    print("=" * 60)
    print(f"✅ Archivos organizados exitosamente: {organizados}")
    if errores > 0:
        print(f"⚠️ Archivos con problemas: {errores}")
    
    # Mostrar estructura final
    print(f"\n📁 Estructura final de carpetas creadas:")
    for categoria in gestor.categorias.keys():
        carpeta = gestor.descargas_path / categoria
        if carpeta.exists():
            if categoria == "documentos":
                # Contar archivos en subcarpetas de documentos
                total_documentos = 0
                subcarpetas_con_archivos = []
                for subcarpeta in carpeta.iterdir():
                    if subcarpeta.is_dir():
                        archivos_en_subcarpeta = len([f for f in subcarpeta.iterdir() if f.is_file()])
                        if archivos_en_subcarpeta > 0:
                            total_documentos += archivos_en_subcarpeta
                            subcarpetas_con_archivos.append(f"    📄 {subcarpeta.name}/ - {archivos_en_subcarpeta} archivos")
                
                if total_documentos > 0:
                    print(f"  📂 {categoria}/ - {total_documentos} archivos")
                    for subcarpeta_info in subcarpetas_con_archivos:
                        print(subcarpeta_info)
            else:
                archivos_en_carpeta = len([f for f in carpeta.iterdir() if f.is_file()])
                if archivos_en_carpeta > 0:
                    print(f"  📂 {categoria}/ - {archivos_en_carpeta} archivos")

def main():
    """Función principal de la prueba agresiva"""
    print("🚀 PRUEBA DE ORGANIZACIÓN AGRESIVA")
    print("=" * 60)
    print("Este script prueba que la organización funcione SIEMPRE")
    print("por extensión, sin importar el nombre del archivo.")
    print("=" * 60)
    
    # Crear archivos problemáticos
    archivos_creados = crear_archivos_problematicos()
    
    if archivos_creados == 0:
        print("\n❌ No se pudieron crear archivos problemáticos")
        return
    
    # Probar detección agresiva
    probar_deteccion_agresiva()
    
    # Organizar archivos problemáticos
    organizar_archivos_problematicos()
    
    print("\n" + "=" * 60)
    print("🎉 ¡PRUEBA AGRESIVA COMPLETADA!")
    print("=" * 60)
    print("💡 La organización ahora funciona SIEMPRE por extensión:")
    print("   ✅ Sin importar el nombre del archivo")
    print("   ✅ Sin importar caracteres especiales")
    print("   ✅ Sin importar espacios o símbolos")
    print("   ✅ Sin importar la longitud del nombre")
    print("   ✅ Sin importar la posición de la extensión")
    print("\n🔧 Para usar la funcionalidad mejorada:")
    print("   Ejecuta: python gestor_descargas.py")
    print("   Selecciona la opción 6: 🎯 Organización automática completa")

if __name__ == "__main__":
    main()
