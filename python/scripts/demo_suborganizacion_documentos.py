#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración de la Suborganización de Documentos
Este script crea archivos de ejemplo de diferentes tipos de documentos
y demuestra la nueva funcionalidad de suborganización
"""

from gestor_descargas import GestorDescargas
import os

def crear_documentos_ejemplo():
    """Crea archivos de ejemplo de diferentes tipos de documentos"""
    print("📄 DEMOSTRACIÓN DE SUBORGANIZACIÓN DE DOCUMENTOS")
    print("=" * 60)
    
    gestor = GestorDescargas()
    
    # Documentos de ejemplo por subcategoría
    documentos_ejemplo = {
        "pdf": [
            "informe_anual_2024.pdf",
            "manual_usuario.pdf",
            "presentacion_ventas.pdf",
            "contrato_servicios.pdf",
            "certificado_curso.pdf"
        ],
        "word": [
            "memorando_importante.docx",
            "propuesta_proyecto.doc",
            "carta_recomendacion.docx",
            "informe_tecnico.doc",
            "plantilla_contrato.docx"
        ],
        "excel": [
            "presupuesto_2024.xlsx",
            "inventario_productos.xls",
            "datos_ventas.xlsx",
            "planilla_horas.xls",
            "estadisticas_empresa.xlsx"
        ],
        "powerpoint": [
            "presentacion_ventas.pptx",
            "capacitacion_empleados.ppt",
            "proyecto_final.pptx",
            "reunion_equipo.ppt",
            "conferencia_tecnica.pptx"
        ],
        "texto": [
            "notas_importantes.txt",
            "configuracion_sistema.rtf",
            "log_errores.txt",
            "instrucciones_uso.odt",
            "resumen_reunion.txt"
        ],
        "datos": [
            "clientes.csv",
            "configuracion.xml",
            "datos_api.json",
            "productos.csv",
            "configuracion_app.json"
        ],
        "otros": [
            "documento_especial.odt",
            "archivo_formato_rar.txt",
            "datos_binarios.doc"
        ]
    }
    
    print("📝 Creando documentos de ejemplo...")
    documentos_creados = 0
    
    for subcategoria, archivos in documentos_ejemplo.items():
        for archivo in archivos:
            ruta_archivo = gestor.descargas_path / archivo
            if not ruta_archivo.exists():
                try:
                    # Crear contenido de ejemplo
                    contenido = f"Este es un documento de ejemplo de tipo {subcategoria}: {archivo}\n"
                    contenido += f"Fecha de creación: {gestor.descargas_path}\n"
                    contenido += f"Subcategoría: {subcategoria}\n"
                    contenido += "=" * 50 + "\n"
                    contenido += "Contenido de ejemplo para demostrar la suborganización de documentos.\n"
                    contenido += "Este archivo será organizado automáticamente en la carpeta correspondiente.\n"
                    
                    with open(ruta_archivo, 'w', encoding='utf-8') as f:
                        f.write(contenido)
                    
                    print(f"  ✅ Creado: {archivo} (tipo: {subcategoria})")
                    documentos_creados += 1
                except Exception as e:
                    print(f"  ❌ Error creando {archivo}: {e}")
            else:
                print(f"  ⚠️ Ya existe: {archivo}")
    
    print(f"\n📊 Total de documentos creados: {documentos_creados}")
    return documentos_creados

def mostrar_estructura_documentos():
    """Muestra la estructura de subcarpetas de documentos"""
    gestor = GestorDescargas()
    
    print("\n📁 ESTRUCTURA DE SUBCARPETAS DE DOCUMENTOS:")
    print("=" * 50)
    
    carpeta_documentos = gestor.descargas_path / "documentos"
    if carpeta_documentos.exists():
        subcategorias = {
            "pdf": "📄 Archivos PDF",
            "word": "📝 Archivos Word (.doc, .docx)",
            "excel": "📊 Archivos Excel (.xls, .xlsx)",
            "powerpoint": "📋 Archivos PowerPoint (.ppt, .pptx)",
            "texto": "📝 Archivos de texto (.txt, .rtf, .odt)",
            "datos": "📊 Archivos de datos (.csv, .xml, .json)",
            "otros": "📁 Otros documentos"
        }
        
        for subcategoria, descripcion in subcategorias.items():
            subcarpeta = carpeta_documentos / subcategoria
            if subcarpeta.exists():
                archivos = [f for f in subcarpeta.iterdir() if f.is_file()]
                if archivos:
                    print(f"\n{descripcion}:")
                    print(f"  📂 documentos/{subcategoria}/ - {len(archivos)} archivos")
                    for archivo in archivos[:3]:  # Mostrar solo los primeros 3
                        tamaño = gestor.formatear_tamaño(archivo.stat().st_size)
                        print(f"    📄 {archivo.name} ({tamaño})")
                    if len(archivos) > 3:
                        print(f"    ... y {len(archivos) - 3} archivos más")
    else:
        print("❌ No se encontró la carpeta de documentos")

def demostrar_organizacion():
    """Demuestra el proceso completo de organización"""
    gestor = GestorDescargas()
    
    print("\n🎯 DEMOSTRANDO ORGANIZACIÓN CON SUBORGANIZACIÓN DE DOCUMENTOS")
    print("=" * 70)
    
    # Mostrar archivos antes de organizar
    print("\n📋 Archivos antes de la organización:")
    archivos_antes = []
    for item in gestor.descargas_path.iterdir():
        if item.is_file():
            archivos_antes.append(item)
            extension = item.suffix.lower()
            tipo = gestor.obtener_tipo_archivo(extension)
            
            if tipo == "documentos":
                subcategoria = gestor.obtener_subcategoria_documento(extension)
                print(f"  📄 {item.name} → documentos/{subcategoria}/")
            else:
                print(f"  📄 {item.name} → {tipo}/")
    
    if not archivos_antes:
        print("📭 No hay archivos para organizar")
        return
    
    # Confirmar organización
    confirmar = input(f"\n¿Quieres organizar {len(archivos_antes)} archivos? (s/n): ").lower()
    if confirmar != 's':
        print("❌ Organización cancelada")
        return
    
    # Ejecutar organización
    gestor.organizacion_automatica_completa()
    
    # Mostrar estructura final
    mostrar_estructura_documentos()

def main():
    """Función principal de la demostración"""
    print("🚀 DEMOSTRACIÓN DE SUBORGANIZACIÓN DE DOCUMENTOS")
    print("=" * 60)
    print("Este script demostrará cómo funciona la nueva funcionalidad")
    print("de suborganización automática de documentos por extensión.")
    print("=" * 60)
    
    # Crear documentos de ejemplo
    documentos_creados = crear_documentos_ejemplo()
    
    if documentos_creados == 0:
        print("\n❌ No se pudieron crear documentos de ejemplo")
        return
    
    # Demostrar organización
    demostrar_organizacion()
    
    print("\n" + "=" * 60)
    print("🎉 ¡DEMOSTRACIÓN COMPLETADA!")
    print("=" * 60)
    print("💡 Características de la suborganización de documentos:")
    print("   ✅ Organiza automáticamente por tipo de documento")
    print("   ✅ Crea subcarpetas específicas para cada extensión")
    print("   ✅ Mantiene una estructura clara y organizada")
    print("   ✅ Facilita la búsqueda de documentos específicos")
    print("   ✅ Funciona con todos los tipos de documentos comunes")
    print("\n📁 Estructura creada:")
    print("   documentos/pdf/        - Archivos PDF")
    print("   documentos/word/       - Archivos Word")
    print("   documentos/excel/      - Archivos Excel")
    print("   documentos/powerpoint/ - Archivos PowerPoint")
    print("   documentos/texto/      - Archivos de texto")
    print("   documentos/datos/      - Archivos de datos")
    print("   documentos/otros/      - Otros documentos")
    print("\n🔧 Para usar esta función en el programa principal:")
    print("   Ejecuta: python gestor_descargas.py")
    print("   Selecciona la opción 6: 🎯 Organización automática completa")

if __name__ == "__main__":
    main()
