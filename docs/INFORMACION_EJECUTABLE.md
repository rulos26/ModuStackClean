# ModuStackClean - Ejecutable Generado

## 📋 Información del Ejecutable
- **Archivo**: ModuStackClean.exe
- **Tamaño**: 27 MB
- **Fecha de creación**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **Versión**: 1.0
- **Plataforma**: Windows 10/11 (64-bit)

## 🚀 Instrucciones de Uso

### Instalación
1. **No requiere instalación** - Es un ejecutable portable
2. **No requiere Python** - Incluye todas las dependencias
3. **Ejecutar directamente** - Doble clic en `ModuStackClean.exe`

### Primer Uso
1. Ejecuta `ModuStackClean.exe`
2. La aplicación se conectará automáticamente a la base de datos
3. Si no hay conexión remota, usará la base de datos local (XAMPP)
4. Registra un nuevo usuario o inicia sesión

## 🔧 Requisitos del Sistema

### Mínimos
- **Sistema Operativo**: Windows 10 o superior (64-bit)
- **Memoria RAM**: 4 GB mínimo
- **Espacio en disco**: 100 MB libres
- **Conexión a internet**: Para base de datos remota

### Recomendados
- **Sistema Operativo**: Windows 11
- **Memoria RAM**: 8 GB o más
- **Espacio en disco**: 500 MB libres
- **Conexión a internet**: Estable

### Opcional
- **XAMPP**: Para base de datos local
- **Antivirus**: Configurado para permitir la aplicación

## 🗄️ Base de Datos

### Configuración Automática
- **Conexión Remota**: 82.197.82.130 (automática)
- **Conexión Local**: localhost (fallback)
- **Base de datos**: modustackclean
- **Tabla**: usuarios

### Fallback Automático
1. Intenta conexión remota primero
2. Si falla, usa conexión local
3. Muestra estado de conexión en la interfaz

## 🔐 Funcionalidades

### Autenticación
- ✅ **Registro de usuarios** con validación
- ✅ **Inicio de sesión** seguro
- ✅ **Gestión de sesiones** automática
- ✅ **Cerrar sesión** con confirmación

### Interfaz de Usuario
- ✅ **Diseño moderno** con Material Design 3
- ✅ **Responsive** y adaptable
- ✅ **Gradientes** y efectos visuales
- ✅ **Iconografía** intuitiva

### Base de Datos
- ✅ **CRUD completo** de usuarios
- ✅ **Encriptación** de contraseñas (SHA-256)
- ✅ **Validación** de datos
- ✅ **Manejo de errores** robusto

## 🛠️ Solución de Problemas

### El ejecutable no inicia
1. **Verificar Windows Defender**:
   - Agregar a exclusiones si es necesario
   - Permitir en SmartScreen

2. **Verificar antivirus**:
   - Agregar a lista blanca
   - Permitir ejecución

3. **Verificar permisos**:
   - Ejecutar como administrador si es necesario
   - Verificar permisos de carpeta

### Problemas de conexión
1. **Base de datos remota**:
   - Verificar conexión a internet
   - Verificar firewall
   - Contactar administrador del servidor

2. **Base de datos local**:
   - Verificar que XAMPP esté ejecutándose
   - Verificar que MySQL esté activo
   - Verificar puerto 3306

### Errores de memoria
1. **Cerrar otras aplicaciones**
2. **Reiniciar el sistema**
3. **Verificar espacio en disco**

## 📁 Estructura de Archivos

```
dist/
├── ModuStackClean.exe          # Ejecutable principal
└── INFORMACION_EJECUTABLE.md   # Este archivo

build/                          # Archivos temporales (se puede eliminar)
├── ModuStackClean/
└── ModuStackClean.spec
```

## 🔄 Actualizaciones

### Versión Actual
- **Versión**: 1.0
- **Fecha**: $(Get-Date -Format "yyyy-MM-dd")
- **Características**: Sistema completo de autenticación

### Próximas Versiones
- Gestión de perfiles de usuario
- Configuración avanzada
- Reportes y estadísticas
- Integración con APIs externas

## 📞 Soporte

### Información de Contacto
- **Desarrollador**: RuloSoluciones
- **Año**: 2025
- **Derechos**: Todos los derechos reservados

### Reportar Problemas
1. Documentar el error específico
2. Incluir pasos para reproducir
3. Adjuntar capturas de pantalla
4. Especificar versión del sistema operativo

## 🎯 Características Técnicas

### Tecnologías Utilizadas
- **Frontend**: Flet (Python)
- **Backend**: Python
- **Base de datos**: MySQL
- **Encriptación**: SHA-256
- **Empaquetado**: PyInstaller

### Arquitectura
- **Patrón MVC**: Modelo-Vista-Controlador
- **Modular**: Componentes reutilizables
- **Escalable**: Fácil extensión
- **Mantenible**: Código bien estructurado

## 📊 Rendimiento

### Optimizaciones
- ✅ **Conexión pooling** para base de datos
- ✅ **Lazy loading** de componentes
- ✅ **Caché** de configuraciones
- ✅ **Manejo eficiente** de memoria

### Métricas Esperadas
- **Tiempo de inicio**: < 5 segundos
- **Uso de memoria**: < 100 MB
- **Tiempo de respuesta**: < 1 segundo
- **Estabilidad**: 99.9% uptime

---

**© 2025 RuloSoluciones. Todos los derechos reservados.**
