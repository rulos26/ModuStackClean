# 📁 Gestor de Archivos de Descargas

Un programa completo en Python para gestionar y organizar archivos en tu carpeta de descargas.

## 🚀 Características

- **📋 Ver archivos**: Lista todos los archivos con información detallada
- **🔍 Buscar archivos**: Encuentra archivos por nombre
- **🗂️ Organizar archivos**: Clasifica archivos por tipo en subcarpetas
- **🧹 Limpiar archivos**: Elimina archivos antiguos automáticamente
- **📊 Estadísticas**: Muestra información sobre tipos y tamaños de archivos

## 📋 Requisitos

- Python 3.6 o superior
- No se requieren librerías adicionales (usa solo módulos estándar de Python)

## 🛠️ Instalación

1. **Descarga el programa**:
   - Guarda el archivo `gestor_descargas.py` en tu computadora

2. **Verifica que tienes Python instalado**:
   ```bash
   python --version
   # o
   python3 --version
   ```

3. **Ejecuta el programa**:
   ```bash
   python gestor_descargas.py
   # o
   python3 gestor_descargas.py
   ```

## 📖 Tutorial de Uso

### 🎯 Paso 1: Ejecutar el Programa

1. Abre tu terminal o línea de comandos
2. Navega hasta la carpeta donde guardaste `gestor_descargas.py`
3. Ejecuta el comando:
   ```bash
   python gestor_descargas.py
   ```

### 🎯 Paso 2: Explorar el Menú Principal

Al ejecutar el programa, verás un menú con 7 opciones:

```
==================================================
📁 GESTOR DE ARCHIVOS DE DESCARGAS
==================================================
1. 📋 Ver todos los archivos
2. 🔍 Buscar archivos
3. 🗂️ Organizar archivos por tipo
4. 🧹 Limpiar archivos antiguos
5. 📊 Ver estadísticas
6. 🎯 Organización automática completa
7. ❌ Salir
==================================================
```

### 🎯 Paso 3: Usar las Funciones

#### 📋 Opción 1: Ver todos los archivos
- Selecciona `1` y presiona Enter
- El programa te preguntará si quieres mostrar archivos ocultos
- Verás una lista completa con:
  - Nombre del archivo
  - Tamaño (en formato legible)
  - Fecha de modificación
  - Tipo de archivo
  - Estadísticas generales

#### 🔍 Opción 2: Buscar archivos
- Selecciona `2` y presiona Enter
- Escribe el término que quieres buscar
- El programa encontrará todos los archivos que contengan ese término en el nombre

#### 🗂️ Opción 3: Organizar archivos por tipo
- Selecciona `3` y presiona Enter
- Confirma la operación escribiendo `s`
- El programa creará carpetas automáticamente:
  - `imagenes/` (jpg, png, gif, etc.)
  - `documentos/` (pdf, doc, txt, etc.)
  - `videos/` (mp4, avi, mov, etc.)
  - `audio/` (mp3, wav, flac, etc.)
  - `comprimidos/` (zip, rar, 7z, etc.)
  - `ejecutables/` (exe, msi, dmg, etc.)
  - `otros/` (archivos no clasificados)

#### 🎯 Opción 6: Organización automática completa (NUEVA)
- Selecciona `6` y presiona Enter
- **Esta es la opción más completa y recomendada**
- El programa te mostrará:
  - Lista detallada de todos los archivos que se organizarán
  - Categoría a la que irá cada archivo
  - Confirmación antes de proceder
  - Progreso en tiempo real
  - Resumen completo al final
  - Estructura de carpetas creadas

#### 🧹 Opción 4: Limpiar archivos antiguos
- Selecciona `4` y presiona Enter
- Ingresa el número de días (por defecto 30)
- Confirma la operación
- El programa eliminará archivos más antiguos que el número de días especificado

#### 📊 Opción 5: Ver estadísticas
- Selecciona `5` y presiona Enter
- Verás información detallada sobre:
  - Total de archivos
  - Tamaño total ocupado
  - Cantidad de archivos por tipo

#### ❌ Opción 7: Salir
- Selecciona `7` y presiona Enter
- El programa se cerrará

## 🔧 Funciones Avanzadas

### 📁 Tipos de Archivos Soportados

El programa reconoce automáticamente estos tipos de archivos:

- **Imágenes**: jpg, jpeg, png, gif, bmp, svg, webp, tiff, tif, ico, psd, ai, eps
- **Documentos**: pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx, csv, xml, json
- **Videos**: mp4, avi, mov, wmv, flv, mkv, webm, m4v, 3gp, mpg, mpeg, ts
- **Audio**: mp3, wav, flac, aac, ogg, wma, m4a, opus, aiff, mid, midi
- **Comprimidos**: zip, rar, 7z, tar, gz, bz2, xz, cab, iso
- **Ejecutables**: exe, msi, dmg, pkg, deb, rpm, app, bat, cmd, sh, dll, sys

### 🛡️ Características de Seguridad

- **Confirmación antes de eliminar**: El programa siempre pide confirmación antes de eliminar archivos
- **Manejo de errores**: Si un archivo no se puede mover o eliminar, el programa continúa con los demás
- **Archivos duplicados**: Si ya existe un archivo con el mismo nombre, el programa te avisa

## 🎯 Nueva Funcionalidad: Organización Automática Completa

### ⭐ Características de la Opción 6

La **Opción 6: Organización automática completa** es la función más avanzada y recomendada para mantener tu carpeta de descargas ordenada:

#### 🔍 **Vista Previa Detallada**
- Muestra todos los archivos que se van a organizar
- Indica exactamente a qué carpeta irá cada archivo
- Te permite revisar antes de confirmar

#### 🛡️ **Seguridad Mejorada**
- Confirmación obligatoria antes de proceder
- Manejo de errores individual por archivo
- No se detiene si un archivo falla

#### 📊 **Información Completa**
- Progreso en tiempo real
- Resumen detallado al final
- Estructura de carpetas creadas
- Estadísticas de archivos organizados

#### 🎯 **Tipos de Archivos Soportados**
El programa reconoce automáticamente **más de 50 tipos de archivos** diferentes:

**🖼️ Imágenes (13 tipos):** jpg, jpeg, png, gif, bmp, svg, webp, tiff, tif, ico, psd, ai, eps
**📄 Documentos (12 tipos):** pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx, csv, xml, json
**🎬 Videos (12 tipos):** mp4, avi, mov, wmv, flv, mkv, webm, m4v, 3gp, mpg, mpeg, ts
**🎵 Audio (10 tipos):** mp3, wav, flac, aac, ogg, wma, m4a, opus, aiff, mid, midi
**📦 Comprimidos (9 tipos):** zip, rar, 7z, tar, gz, bz2, xz, cab, iso
**⚙️ Ejecutables (12 tipos):** exe, msi, dmg, pkg, deb, rpm, app, bat, cmd, sh, dll, sys

## 💡 Consejos de Uso

### 🎯 Para Principiantes
1. **Empieza con la opción 1**: Ve qué archivos tienes antes de organizar
2. **Usa la opción 6**: Es la más completa y segura para organizar
3. **Revisa la vista previa**: Siempre revisa qué archivos se van a mover
4. **Organiza gradualmente**: No organices todo de una vez, revisa los resultados

### 🎯 Para Usuarios Avanzados
1. **Limpieza automática**: Usa la función de limpiar archivos antiguos regularmente
2. **Personalización**: Puedes modificar las categorías en el código
3. **Automatización**: Puedes ejecutar el programa desde scripts

## 🔧 Personalización

Si quieres modificar el programa, puedes editar estas secciones en el código:

### Agregar Nuevos Tipos de Archivo
```python
self.categorias = {
    "imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"],
    # Agrega aquí tus nuevas extensiones
}
```

### Cambiar la Carpeta de Descargas
```python
self.descargas_path = Path("C:/Mi/Carpeta/Personalizada")
```

## ❓ Preguntas Frecuentes

### ¿El programa elimina archivos permanentemente?
Sí, cuando usas la función "Limpiar archivos antiguos", los archivos se eliminan permanentemente. Siempre se pide confirmación antes de eliminar.

### ¿Puedo recuperar archivos organizados?
Sí, los archivos organizados se mueven a subcarpetas dentro de tu carpeta de descargas. Puedes moverlos de vuelta manualmente.

### ¿Funciona en Windows/Mac/Linux?
Sí, el programa detecta automáticamente tu sistema operativo y usa la carpeta de descargas correcta.

### ¿Necesito instalar algo más?
No, el programa usa solo módulos estándar de Python que vienen incluidos.

## 🐛 Solución de Problemas

### Error: "No se puede encontrar Python"
- Instala Python desde [python.org](https://python.org)
- Asegúrate de que Python esté en tu PATH

### Error: "Permiso denegado"
- Ejecuta el programa como administrador
- Verifica que tienes permisos en la carpeta de descargas

### Error: "Carpeta no encontrada"
- El programa creará automáticamente la carpeta de descargas si no existe
- Verifica que la ruta sea correcta para tu sistema

## 📞 Soporte

Si tienes problemas o sugerencias:
1. Revisa la sección de solución de problemas
2. Verifica que estás usando Python 3.6 o superior
3. Asegúrate de que tienes permisos en la carpeta de descargas

## 📄 Licencia

Este programa es de código abierto y puedes modificarlo libremente para tus necesidades.

---

¡Disfruta organizando tus archivos! 🎉
