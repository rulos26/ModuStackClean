#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Archivos de Descargas
Un programa para gestionar y organizar archivos en la carpeta de descargas
"""

import os
import shutil
import datetime
from pathlib import Path
import sys
import time
import subprocess
import platform
import getpass

class GestorDescargas:
    def __init__(self):
        # Obtener la ruta de la carpeta de descargas según el sistema operativo
        if sys.platform == "win32":
            self.descargas_path = Path.home() / "Downloads"
        elif sys.platform == "darwin":  # macOS
            self.descargas_path = Path.home() / "Downloads"
        else:  # Linux
            self.descargas_path = Path.home() / "Downloads"
        
        # Crear la carpeta si no existe
        self.descargas_path.mkdir(exist_ok=True)
        
        # Extensiones por categoría
        self.categorias = {
            "imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".tif", ".ico", ".psd", ".ai", ".eps"],
            "documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".xml", ".json"],
            "videos": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm", ".m4v", ".3gp", ".mpg", ".mpeg", ".ts"],
            "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".opus", ".aiff", ".mid", ".midi"],
            "comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".cab", ".iso"],
            "ejecutables": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".app", ".bat", ".cmd", ".sh", ".dll", ".sys"],
            "otros": []
        }

    def mostrar_archivos(self, mostrar_ocultos=False):
        """Muestra todos los archivos en la carpeta de descargas"""
        print(f"\n📁 Contenido de la carpeta: {self.descargas_path}")
        print("=" * 60)
        
        if not self.descargas_path.exists():
            print("❌ La carpeta de descargas no existe")
            return
        
        archivos = []
        for item in self.descargas_path.iterdir():
            if not mostrar_ocultos and item.name.startswith('.'):
                continue
            
            if item.is_file():
                tamaño = item.stat().st_size
                fecha_mod = datetime.datetime.fromtimestamp(item.stat().st_mtime)
                archivos.append({
                    'nombre': item.name,
                    'tamaño': tamaño,
                    'fecha': fecha_mod,
                    'extension': self.obtener_extension_real(item.name)
                })
        
        if not archivos:
            print("📭 No hay archivos en la carpeta de descargas")
            return
        
        # Ordenar por fecha de modificación (más recientes primero)
        archivos.sort(key=lambda x: x['fecha'], reverse=True)
        
        print(f"{'Nombre':<30} {'Tamaño':<12} {'Fecha':<20} {'Tipo':<10}")
        print("-" * 80)
        
        for archivo in archivos:
            nombre = archivo['nombre'][:28] + ".." if len(archivo['nombre']) > 30 else archivo['nombre']
            tamaño = self.formatear_tamaño(archivo['tamaño'])
            fecha = archivo['fecha'].strftime("%d/%m/%Y %H:%M")
            tipo = self.obtener_tipo_archivo(archivo['extension'])
            
            print(f"{nombre:<30} {tamaño:<12} {fecha:<20} {tipo:<10}")
        
        print(f"\n📊 Total de archivos: {len(archivos)}")
        self.mostrar_estadisticas(archivos)

    def formatear_tamaño(self, bytes_size):
        """Convierte bytes a formato legible"""
        if bytes_size == 0:
            return "0 B"
        
        unidades = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        while bytes_size >= 1024 and i < len(unidades) - 1:
            bytes_size /= 1024.0
            i += 1
        
        return f"{bytes_size:.1f} {unidades[i]}"

    def obtener_tipo_archivo(self, extension):
        """Determina el tipo de archivo basado en su extensión"""
        for categoria, extensiones in self.categorias.items():
            if extension in extensiones:
                return categoria
        return "otro"

    def obtener_extension_real(self, nombre_archivo):
        """Obtiene la extensión real del archivo, manejando nombres problemáticos"""
        # Primero intentar obtener la extensión al final del nombre
        extension = Path(nombre_archivo).suffix.lower()
        
        # Si no hay extensión o es muy larga, buscar extensiones conocidas en todo el nombre
        if not extension or len(extension) > 10:
            # Lista completa de extensiones conocidas
            extensiones_conocidas = [
                # Documentos
                ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                ".txt", ".rtf", ".odt", ".csv", ".xml", ".json",
                # Imágenes
                ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", 
                ".tiff", ".tif", ".ico", ".psd", ".ai", ".eps",
                # Videos
                ".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm", 
                ".m4v", ".3gp", ".mpg", ".mpeg", ".ts",
                # Audio
                ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", 
                ".opus", ".aiff", ".mid", ".midi",
                # Comprimidos
                ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".cab", ".iso",
                # Ejecutables
                ".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".app", 
                ".bat", ".cmd", ".sh", ".dll", ".sys"
            ]
            
            # Buscar la extensión más larga que aparezca en el nombre
            extension_encontrada = ""
            for ext in extensiones_conocidas:
                if ext in nombre_archivo.lower():
                    # Si encontramos una extensión más larga, la usamos
                    if len(ext) > len(extension_encontrada):
                        extension_encontrada = ext
            
            if extension_encontrada:
                return extension_encontrada
        
        return extension

    def obtener_subcategoria_documento(self, extension):
        """Determina la subcategoría de documento basado en su extensión"""
        subcategorias_documentos = {
            "pdf": [".pdf"],
            "word": [".doc", ".docx"],
            "excel": [".xls", ".xlsx"],
            "powerpoint": [".ppt", ".pptx"],
            "texto": [".txt", ".rtf", ".odt"],
            "datos": [".csv", ".xml", ".json"],
            "otros": []
        }
        
        for subcategoria, extensiones in subcategorias_documentos.items():
            if extension in extensiones:
                return subcategoria
        return "otros"

    def mostrar_estadisticas(self, archivos):
        """Muestra estadísticas de los archivos"""
        if not archivos:
            return
        
        # Contar por tipo
        tipos = {}
        tamaño_total = 0
        
        for archivo in archivos:
            tipo = self.obtener_tipo_archivo(archivo['extension'])
            tipos[tipo] = tipos.get(tipo, 0) + 1
            tamaño_total += archivo['tamaño']
        
        print(f"\n📈 Estadísticas:")
        print(f"Tamaño total: {self.formatear_tamaño(tamaño_total)}")
        print("\nArchivos por tipo:")
        for tipo, cantidad in sorted(tipos.items()):
            print(f"  {tipo.capitalize()}: {cantidad}")

    def buscar_archivos(self, termino):
        """Busca archivos que contengan el término especificado"""
        print(f"\n🔍 Buscando archivos que contengan: '{termino}'")
        print("=" * 60)
        
        encontrados = []
        for item in self.descargas_path.iterdir():
            if item.is_file() and termino.lower() in item.name.lower():
                tamaño = item.stat().st_size
                fecha_mod = datetime.datetime.fromtimestamp(item.stat().st_mtime)
                encontrados.append({
                    'nombre': item.name,
                    'tamaño': tamaño,
                    'fecha': fecha_mod,
                    'ruta': str(item)
                })
        
        if not encontrados:
            print("❌ No se encontraron archivos con ese término")
            return
        
        print(f"✅ Se encontraron {len(encontrados)} archivos:")
        for archivo in encontrados:
            print(f"  📄 {archivo['nombre']} ({self.formatear_tamaño(archivo['tamaño'])})")

    def organizar_archivos(self):
        """Organiza los archivos en subcarpetas por tipo"""
        print("\n🗂️ Organizando archivos por tipo...")
        
        # Buscar archivos en la carpeta raíz y en subcarpetas existentes
        archivos_a_organizar = []
        
        # Buscar en carpeta raíz
        for item in self.descargas_path.iterdir():
            if item.is_file():
                archivos_a_organizar.append(item)
        
        # Buscar en subcarpetas existentes (para reorganizar si es necesario)
        for item in self.descargas_path.iterdir():
            if item.is_dir() and item.name in self.categorias:
                # Solo buscar en carpetas de categorías conocidas
                for subitem in item.iterdir():
                    if subitem.is_file():
                        archivos_a_organizar.append(subitem)
        
        if not archivos_a_organizar:
            print("📭 No hay archivos para organizar")
            return
        
        print(f"📊 Encontrados {len(archivos_a_organizar)} archivos para organizar")
        
        for item in archivos_a_organizar:
            extension = self.obtener_extension_real(item.name)
            categoria = self.obtener_tipo_archivo(extension)
            
            # Crear carpeta de categoría si no existe
            carpeta_categoria = self.descargas_path / categoria
            carpeta_categoria.mkdir(exist_ok=True)
            
            # Mover archivo a la carpeta correspondiente
            destino = carpeta_categoria / item.name
            if not destino.exists():
                if self.mover_archivo_con_reintentos(item, destino):
                    print(f"  ✅ {item.name} → {categoria}/")
                else:
                    print(f"  ❌ No se pudo mover {item.name} (archivo en uso)")
            else:
                # Manejar archivo duplicado
                self.manejar_archivo_duplicado(item, carpeta_categoria, categoria)
        
        print("✅ Organización completada")

    def manejar_archivo_duplicado(self, archivo, carpeta_destino, categoria):
        """Maneja archivos duplicados preguntando al usuario qué hacer"""
        print(f"\n⚠️  ARCHIVO DUPLICADO DETECTADO:")
        print(f"   📄 Archivo: {archivo.name}")
        print(f"   📂 Destino: {categoria}/")
        print(f"   ❌ Ya existe un archivo con el mismo nombre")
        
        print("\n¿Qué quieres hacer?")
        print("1. 📝 Cambiar nombre automáticamente (agregar versión)")
        print("2. 🔄 Sobrescribir el archivo existente")
        print("3. ❌ Saltar este archivo")
        
        while True:
            opcion = input("\nSelecciona una opción (1-3): ").strip()
            
            if opcion == "1":
                # Cambiar nombre automáticamente
                nuevo_nombre = self.generar_nombre_unico(archivo.name, carpeta_destino)
                nuevo_destino = carpeta_destino / nuevo_nombre
                
                if self.mover_archivo_con_reintentos(archivo, nuevo_destino):
                    print(f"  ✅ {archivo.name} → {categoria}/{nuevo_nombre}")
                else:
                    print(f"  ❌ No se pudo mover {archivo.name} (archivo en uso)")
                break
                
            elif opcion == "2":
                # Sobrescribir archivo existente
                confirmar = input("⚠️ ¿Estás seguro de que quieres sobrescribir el archivo existente? (s/n): ").lower()
                if confirmar == 's':
                    if self.mover_archivo_con_reintentos(archivo, carpeta_destino / archivo.name):
                        print(f"  ✅ {archivo.name} → {categoria}/ (sobrescrito)")
                    else:
                        print(f"  ❌ No se pudo mover {archivo.name} (archivo en uso)")
                else:
                    print(f"  ⏭️ Saltando {archivo.name}")
                break
                
            elif opcion == "3":
                # Saltar archivo
                print(f"  ⏭️ Saltando {archivo.name}")
                break
                
            else:
                print("❌ Opción no válida. Por favor selecciona 1, 2 o 3")

    def generar_nombre_unico(self, nombre_original, carpeta_destino):
        """Genera un nombre único para el archivo agregando versión"""
        # Separar nombre y extensión
        nombre_base = Path(nombre_original).stem
        extension = Path(nombre_original).suffix
        
        # Buscar la siguiente versión disponible
        version = 1
        while True:
            nuevo_nombre = f"{nombre_base}_v{version}{extension}"
            if not (carpeta_destino / nuevo_nombre).exists():
                return nuevo_nombre
            version += 1

    def intentar_cerrar_procesos_archivo(self, ruta_archivo):
        """Intenta cerrar procesos que estén usando un archivo específico"""
        try:
            if sys.platform == "win32":
                # En Windows, usar handle.exe para encontrar y cerrar procesos
                nombre_archivo = Path(ruta_archivo).name
                
                # Buscar procesos que estén usando el archivo
                try:
                    # Usar tasklist para encontrar procesos
                    resultado = subprocess.run(
                        ['tasklist', '/FI', f'IMAGENAME eq *'], 
                        capture_output=True, 
                        text=True, 
                        timeout=10
                    )
                    
                    if resultado.returncode == 0:
                        procesos = resultado.stdout.split('\n')
                        procesos_cerrados = []
                        
                        for proceso in procesos:
                            if nombre_archivo.lower() in proceso.lower():
                                # Extraer el nombre del proceso
                                partes = proceso.split()
                                if len(partes) >= 1:
                                    nombre_proceso = partes[0]
                                    if nombre_proceso not in ['IMAGENAME', '=']:
                                        try:
                                            # Intentar cerrar el proceso
                                            subprocess.run(['taskkill', '/F', '/IM', nombre_proceso], 
                                                         capture_output=True, timeout=5)
                                            procesos_cerrados.append(nombre_proceso)
                                        except:
                                            pass
                        
                        if procesos_cerrados:
                            print(f"  🔄 Procesos cerrados: {', '.join(procesos_cerrados)}")
                            return True
                            
                except subprocess.TimeoutExpired:
                    pass
                except Exception as e:
                    pass
                    
            else:
                # En Linux/macOS, usar lsof y kill
                try:
                    resultado = subprocess.run(
                        ['lsof', ruta_archivo], 
                        capture_output=True, 
                        text=True, 
                        timeout=10
                    )
                    
                    if resultado.returncode == 0:
                        lineas = resultado.stdout.strip().split('\n')
                        if len(lineas) > 1:  # Hay procesos usando el archivo
                            for linea in lineas[1:]:  # Saltar la primera línea (header)
                                partes = linea.split()
                                if len(partes) >= 2:
                                    pid = partes[1]
                                    try:
                                        subprocess.run(['kill', '-9', pid], 
                                                     capture_output=True, timeout=5)
                                        print(f"  🔄 Proceso cerrado: PID {pid}")
                                    except:
                                        pass
                            return True
                            
                except subprocess.TimeoutExpired:
                    pass
                except Exception as e:
                    pass
                    
        except Exception as e:
            pass
            
        return False

    def mover_archivo_con_reintentos(self, origen, destino, max_reintentos=3):
        """Mueve un archivo con reintentos si está siendo usado"""
        for intento in range(max_reintentos):
            try:
                shutil.move(str(origen), str(destino))
                return True
            except PermissionError as e:
                if "El proceso no tiene acceso al archivo" in str(e) or "being used by another process" in str(e):
                    if intento < max_reintentos - 1:  # No es el último intento
                        print(f"  ⚠️ Archivo en uso, intentando cerrar procesos... (intento {intento + 1}/{max_reintentos})")
                        
                        # Intentar cerrar procesos que usen el archivo
                        if self.intentar_cerrar_procesos_archivo(str(origen)):
                            print(f"  ⏳ Esperando 2 segundos...")
                            time.sleep(2)  # Esperar un poco
                            continue
                        else:
                            print(f"  ❌ No se pudieron cerrar los procesos que usan el archivo")
                            return False
                    else:
                        print(f"  ❌ No se pudo mover el archivo después de {max_reintentos} intentos")
                        return False
                else:
                    # Otro tipo de PermissionError
                    raise e
            except Exception as e:
                raise e
        
        return False

    def limpiar_archivos_antiguos(self, dias=30):
        """Elimina archivos más antiguos que el número de días especificado"""
        print(f"\n🧹 Limpiando archivos más antiguos de {dias} días...")
        
        fecha_limite = datetime.datetime.now() - datetime.timedelta(days=dias)
        eliminados = 0
        
        for item in self.descargas_path.iterdir():
            if item.is_file():
                fecha_mod = datetime.datetime.fromtimestamp(item.stat().st_mtime)
                if fecha_mod < fecha_limite:
                    try:
                        item.unlink()
                        print(f"  🗑️ Eliminado: {item.name}")
                        eliminados += 1
                    except Exception as e:
                        print(f"  ❌ Error eliminando {item.name}: {e}")
        
        print(f"✅ Se eliminaron {eliminados} archivos")

    def organizacion_automatica_completa(self):
        """Organización automática completa con información detallada"""
        print("\n🎯 ORGANIZACIÓN AUTOMÁTICA COMPLETA")
        print("=" * 60)
        print("📂 Esta función organizará todos los archivos en carpetas por tipo:")
        print("   🖼️  imágenes/     - Fotos y gráficos")
        print("   📄 documentos/    - PDFs, Word, textos (con suborganización)")
        print("   🎵 audio/         - Música y archivos de sonido")
        print("   🎬 videos/        - Películas y clips")
        print("   📦 comprimidos/   - Archivos ZIP, RAR, etc.")
        print("   ⚙️  ejecutables/   - Programas y instaladores")
        print("   📁 otros/         - Archivos no clasificados")
        print("=" * 60)
        print("📋 Los documentos se suborganizarán por extensión:")
        print("   📄 documentos/pdf/     - Archivos PDF")
        print("   📄 documentos/word/    - Archivos Word (.doc, .docx)")
        print("   📄 documentos/excel/   - Archivos Excel (.xls, .xlsx)")
        print("   📄 documentos/powerpoint/ - Archivos PowerPoint (.ppt, .pptx)")
        print("   📄 documentos/texto/   - Archivos de texto (.txt, .rtf)")
        print("   📄 documentos/datos/   - Archivos de datos (.csv, .xml, .json)")
        print("   📄 documentos/otros/   - Otros documentos")
        
        # Contar archivos antes de organizar (incluyendo subcarpetas)
        archivos_antes = []
        
        # Buscar en carpeta raíz
        for item in self.descargas_path.iterdir():
            if item.is_file():
                archivos_antes.append(item)
        
        # Buscar en subcarpetas existentes
        for item in self.descargas_path.iterdir():
            if item.is_dir() and item.name in self.categorias:
                # Solo buscar en carpetas de categorías conocidas
                for subitem in item.iterdir():
                    if subitem.is_file():
                        archivos_antes.append(subitem)
        
        if not archivos_antes:
            print("📭 No hay archivos para organizar en la carpeta de descargas")
            return
        
        print(f"\n📊 Archivos encontrados: {len(archivos_antes)}")
        
        # Mostrar archivos que se van a organizar
        print("\n📋 Archivos que se organizarán:")
        for archivo in archivos_antes:
            extension = self.obtener_extension_real(archivo.name)
            tipo = self.obtener_tipo_archivo(extension)
            
            if tipo == "documentos":
                subcategoria = self.obtener_subcategoria_documento(extension)
                print(f"  📄 {archivo.name} → {tipo}/{subcategoria}/")
            else:
                print(f"  📄 {archivo.name} → {tipo}/")
        
        # Confirmar organización
        confirmar = input(f"\n¿Estás seguro de que quieres organizar {len(archivos_antes)} archivos? (s/n): ").lower()
        if confirmar != 's':
            print("❌ Organización cancelada")
            return
        
        # Realizar la organización
        print("\n🗂️ Organizando archivos...")
        organizados = 0
        errores = 0
        
        for item in archivos_antes:
            if item.is_file():
                extension = self.obtener_extension_real(item.name)
                categoria = self.obtener_tipo_archivo(extension)
                
                # Crear carpeta de categoría si no existe
                carpeta_categoria = self.descargas_path / categoria
                carpeta_categoria.mkdir(exist_ok=True)
                
                # Si es un documento, crear subcarpeta
                if categoria == "documentos":
                    subcategoria = self.obtener_subcategoria_documento(extension)
                    carpeta_destino = carpeta_categoria / subcategoria
                    carpeta_destino.mkdir(exist_ok=True)
                    destino = carpeta_destino / item.name
                    ruta_mostrar = f"{categoria}/{subcategoria}/"
                else:
                    destino = carpeta_categoria / item.name
                    ruta_mostrar = f"{categoria}/"
                
                if not destino.exists():
                    if self.mover_archivo_con_reintentos(item, destino):
                        print(f"  ✅ {item.name} → {ruta_mostrar}")
                        organizados += 1
                    else:
                        print(f"  ❌ No se pudo mover {item.name} (archivo en uso)")
                        errores += 1
                else:
                    # Manejar archivo duplicado en organización automática
                    print(f"\n⚠️  ARCHIVO DUPLICADO: {item.name} ya existe en {ruta_mostrar}")
                    
                    # Preguntar qué hacer con el duplicado
                    print("¿Qué quieres hacer?")
                    print("1. 📝 Cambiar nombre automáticamente (agregar versión)")
                    print("2. 🔄 Sobrescribir el archivo existente")
                    print("3. ❌ Saltar este archivo")
                    
                    while True:
                        opcion = input("Selecciona una opción (1-3): ").strip()
                        
                        if opcion == "1":
                            # Cambiar nombre automáticamente
                            nuevo_nombre = self.generar_nombre_unico(item.name, carpeta_destino)
                            nuevo_destino = carpeta_destino / nuevo_nombre
                            
                            if self.mover_archivo_con_reintentos(item, nuevo_destino):
                                print(f"  ✅ {item.name} → {ruta_mostrar}{nuevo_nombre}")
                                organizados += 1
                            else:
                                print(f"  ❌ No se pudo mover {item.name} (archivo en uso)")
                                errores += 1
                            break
                           
                        elif opcion == "2":
                            # Sobrescribir archivo existente
                            confirmar = input("⚠️ ¿Estás seguro de que quieres sobrescribir el archivo existente? (s/n): ").lower()
                            if confirmar == 's':
                                if self.mover_archivo_con_reintentos(item, destino):
                                    print(f"  ✅ {item.name} → {ruta_mostrar} (sobrescrito)")
                                    organizados += 1
                                else:
                                    print(f"  ❌ No se pudo mover {item.name} (archivo en uso)")
                                    errores += 1
                            else:
                                print(f"  ⏭️ Saltando {item.name}")
                                errores += 1
                            break
                        
                        elif opcion == "3":
                            # Saltar archivo
                            print(f"  ⏭️ Saltando {item.name}")
                            errores += 1
                            break
                            
                        else:
                            print("❌ Opción no válida. Por favor selecciona 1, 2 o 3")
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("📈 RESUMEN DE ORGANIZACIÓN")
        print("=" * 60)
        print(f"✅ Archivos organizados exitosamente: {organizados}")
        if errores > 0:
            print(f"⚠️ Archivos con problemas: {errores}")
        
        # Mostrar estructura final
        print(f"\n📁 Estructura final de carpetas creadas:")
        for categoria in self.categorias.keys():
            carpeta = self.descargas_path / categoria
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
        
        print("\n🎉 ¡Organización completada!")
        print("💡 Los archivos están ahora organizados en carpetas por tipo")
        print("🔍 Puedes usar la opción 1 para ver la nueva estructura")

    def mostrar_info_sistema(self):
        """Muestra información del sistema"""
        print("\n" + "=" * 60)
        print("💻 INFORMACIÓN DEL SISTEMA")
        print("=" * 60)
        
        # Información básica del sistema
        print(f"💻 Sistema Operativo: {platform.system()} {platform.version()}")
        print(f"🏗️  Arquitectura: {platform.machine()}")
        print(f"👤 Usuario: {getpass.getuser()}")
        print(f"🖥️  Hostname: {platform.node()}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        
        # Información de CPU
        try:
            import psutil
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"⚡ CPU: {cpu_count} núcleos - Uso actual: {cpu_percent}%")
        except ImportError:
            print("⚡ CPU: Información no disponible (psutil no instalado)")
        
        # Información de memoria
        try:
            import psutil
            memoria = psutil.virtual_memory()
            print(f"💾 RAM: {self.formatear_tamaño(memoria.total)} - Usado: {memoria.percent}%")
        except ImportError:
            print("💾 RAM: Información no disponible (psutil no instalado)")
        
        # Información de disco
        try:
            import psutil
            disco = psutil.disk_usage(str(self.descargas_path))
            print(f"💿 Disco: {self.formatear_tamaño(disco.total)} - Libre: {self.formatear_tamaño(disco.free)}")
        except ImportError:
            print("💿 Disco: Información no disponible (psutil no instalado)")
        
        # Información de red
        try:
            import socket
            hostname = socket.gethostname()
            ip_local = socket.gethostbyname(hostname)
            print(f"🌐 IP Local: {ip_local}")
        except:
            print("🌐 IP Local: No disponible")
        
        print("\n💡 Para información más detallada, ejecuta: python info_sistema.py")
        print("📦 Para instalar dependencias: python instalar_dependencias_python.py")

def mostrar_menu():
    """Muestra el menú principal del programa"""
    print("\n" + "=" * 50)
    print("📁 GESTOR DE ARCHIVOS DE DESCARGAS")
    print("=" * 50)
    print("1. 📋 Ver todos los archivos")
    print("2. 🔍 Buscar archivos")
    print("3. 🗂️ Organizar archivos por tipo")
    print("4. 🧹 Limpiar archivos antiguos")
    print("5. 📊 Ver estadísticas")
    print("6. 🎯 Organización automática completa")
    print("7. 💻 Información del sistema")
    print("8. ❌ Salir")
    print("=" * 50)

def main():
    """Función principal del programa"""
    gestor = GestorDescargas()
    
    print("🚀 Bienvenido al Gestor de Archivos de Descargas")
    print(f"📂 Carpeta de descargas: {gestor.descargas_path}")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSelecciona una opción (1-8): ").strip()
            
            if opcion == "1":
                mostrar_ocultos = input("¿Mostrar archivos ocultos? (s/n): ").lower() == 's'
                gestor.mostrar_archivos(mostrar_ocultos)
                
            elif opcion == "2":
                termino = input("Ingresa el término de búsqueda: ").strip()
                if termino:
                    gestor.buscar_archivos(termino)
                else:
                    print("❌ Debes ingresar un término de búsqueda")
                    
            elif opcion == "3":
                confirmar = input("¿Estás seguro de que quieres organizar los archivos? (s/n): ").lower()
                if confirmar == 's':
                    gestor.organizar_archivos()
                else:
                    print("❌ Operación cancelada")
                    
            elif opcion == "4":
                try:
                    dias = int(input("Ingresa el número de días (por defecto 30): ") or "30")
                    confirmar = input(f"¿Eliminar archivos más antiguos de {dias} días? (s/n): ").lower()
                    if confirmar == 's':
                        gestor.limpiar_archivos_antiguos(dias)
                    else:
                        print("❌ Operación cancelada")
                except ValueError:
                    print("❌ Debes ingresar un número válido")
                    
            elif opcion == "5":
                gestor.mostrar_archivos()
                
            elif opcion == "6":
                gestor.organizacion_automatica_completa()
                
            elif opcion == "7":
                gestor.mostrar_info_sistema()
                
            elif opcion == "8":
                print("👋 ¡Gracias por usar el Gestor de Archivos de Descargas!")
                break
                
            else:
                print("❌ Opción no válida. Por favor selecciona 1-8")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
