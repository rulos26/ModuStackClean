# 🚀 ModuStackClean - Aplicación Flet

## 📋 Descripción

Aplicación de escritorio desarrollada con Flet para el sistema ModuStackClean. Esta aplicación proporciona una interfaz moderna y estructurada para la gestión y organización de archivos.

## 🎯 Características

- **Interfaz Moderna**: Diseño limpio y profesional con Material Design 3
- **Estructura Organizada**: Código modular y bien estructurado
- **Responsive**: Adaptable a diferentes tamaños de ventana
- **Tema Personalizado**: Colores y estilos consistentes con la marca

## 📁 Estructura del Proyecto

```
flet_app/
├── main.py                 # Punto de entrada de la aplicación
├── config/
│   └── app_config.py       # Configuración de la aplicación
├── views/
│   └── home_view.py        # Vista principal (Home)
├── utils/
│   └── ui_components.py    # Componentes de UI reutilizables
├── assets/                 # Recursos estáticos
└── requirements.txt        # Dependencias del proyecto
```

## 🚀 Instalación y Uso

### 1. Instalar Dependencias

```bash
cd flet_app
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
python main.py
```

### 3. Alternativa con Flet CLI

```bash
flet run main.py
```

## 🎨 Características de la Interfaz

### Header
- Logo y título principal con emoji 🚀
- Versión de la aplicación (v1.0)
- Subtítulo descriptivo
- Fondo con gradiente azul

### Contenido Principal
- Grid de características del sistema
- 4 tarjetas con iconos y descripciones
- Botón "Comenzar" con animación

### Footer
- Copyright: "© 2025 RuloSoluciones. Todos los derechos reservados."
- Fondo oscuro para contraste

## 🔧 Configuración

La configuración se encuentra en `config/app_config.py`:

- **Información de la aplicación**: Título, versión, descripción
- **Colores del tema**: Paleta de colores personalizada
- **Configuración de UI**: Tamaños, radios, espaciados
- **Características**: Lista de funcionalidades del sistema

## 🎯 Características Mostradas

1. **📁 Organización Automática**: Organiza automáticamente tus archivos de descargas
2. **🤖 Detección Inteligente**: Detecta y clasifica archivos de manera inteligente
3. **⚡ Rendimiento Optimizado**: Procesamiento rápido y eficiente de archivos
4. **🛡️ Seguridad Garantizada**: Mantén tus archivos seguros y organizados

## 🛠️ Desarrollo

### Agregar Nuevas Vistas

1. Crear archivo en `views/`
2. Importar en `main.py`
3. Configurar navegación

### Modificar Estilos

1. Editar `config/app_config.py` para colores y configuración
2. Modificar `utils/ui_components.py` para componentes reutilizables
3. Actualizar vistas específicas según sea necesario

### Agregar Funcionalidades

1. Crear nuevos componentes en `utils/`
2. Implementar lógica en las vistas
3. Actualizar configuración según sea necesario

## 📱 Compatibilidad

- **Sistema Operativo**: Windows, macOS, Linux
- **Python**: 3.8+
- **Flet**: 0.21.0+

## 🎨 Personalización

### Cambiar Colores
Editar en `config/app_config.py`:
```python
self.PRIMARY_COLOR = "#4facfe"
self.SECONDARY_COLOR = "#00f2fe"
self.ACCENT_COLOR = "#667eea"
```

### Modificar Características
Editar la lista `FEATURES` en `config/app_config.py`:
```python
self.FEATURES = [
    {
        "icon": "📁",
        "title": "Nueva Característica",
        "description": "Descripción de la nueva característica"
    }
]
```

## 📄 Licencia

© 2025 RuloSoluciones. Todos los derechos reservados.

---

**¡Disfruta usando ModuStackClean!** 🚀
