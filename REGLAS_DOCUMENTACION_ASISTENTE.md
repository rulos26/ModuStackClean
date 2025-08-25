# 📋 REGLAS DE DOCUMENTACIÓN PARA EL ASISTENTE

## 🎯 **REGLAS OBLIGATORIAS**

### **✅ REGLA PRINCIPAL**
**TODA la documentación del proyecto ModuStackClean DEBE ser agregada ÚNICAMENTE en el archivo `flet_app/docs/DOCUMENTACION_COMPLETA.md`**

### **❌ PROHIBIDO ABSOLUTAMENTE**
- ❌ Crear archivos de documentación separados
- ❌ Crear archivos `.md` adicionales con información del proyecto
- ❌ Crear archivos de resumen o índices separados
- ❌ Documentar en múltiples archivos
- ❌ Crear archivos como `RESUMEN_*.md`, `GUIA_*.md`, etc.

### **✅ PERMITIDO**
- ✅ Agregar información al archivo `DOCUMENTACION_COMPLETA.md`
- ✅ Actualizar secciones existentes
- ✅ Agregar nuevas secciones al índice
- ✅ Mantener archivos de configuración y scripts
- ✅ Mantener archivos de test en carpeta `tests/`

---

## 📁 **ESTRUCTURA PERMITIDA**

### **Archivos de Documentación Únicos:**
```
flet_app/docs/
├── 📖 DOCUMENTACION_COMPLETA.md      # ✅ ÚNICO archivo de documentación
├── 📋 INDICE_DOCUMENTACION.md        # ✅ Solo navegación (sin contenido)
├── 🚀 README.md                      # ✅ Solo descripción básica
└── 📦 INFORMACION_EJECUTABLE.md      # ✅ Solo para usuarios finales
```

### **Carpetas de Tests (Permitidas):**
```
flet_app/tests/
├── 📋 INDICE_TESTS.md                # ✅ Solo navegación de tests
└── [archivos de test]                # ✅ Scripts de prueba
```

---

## 🔧 **PROCESO OBLIGATORIO**

### **Para Cualquier Nueva Información:**
1. **SIEMPRE** abrir `flet_app/docs/DOCUMENTACION_COMPLETA.md`
2. **Identificar** sección apropiada o crear nueva
3. **Agregar** información en la sección correspondiente
4. **Actualizar** índice general si es necesario
5. **NUNCA** crear archivos separados

### **Para Actualizaciones:**
1. **Buscar** sección específica en `DOCUMENTACION_COMPLETA.md`
2. **Modificar** contenido existente
3. **Mantener** estructura y formato
4. **Verificar** consistencia

---

## 🚨 **VIOLACIONES COMUNES A EVITAR**

### **❌ NO HACER:**
- Crear `RESUMEN_*.md`
- Crear `GUIA_*.md`
- Crear `INSTRUCCIONES_*.md`
- Crear archivos de documentación en la raíz
- Crear archivos de documentación en subcarpetas

### **✅ HACER:**
- Agregar al archivo principal
- Actualizar secciones existentes
- Mantener estructura organizada
- Seguir el formato establecido

---

## 📊 **BENEFICIOS DE LA REGLA**

### **Para el Proyecto:**
- ✅ **Un solo lugar** para toda la información
- ✅ **Sin redundancias** ni archivos duplicados
- ✅ **Mantenimiento fácil** de documentación
- ✅ **Búsqueda eficiente** de información
- ✅ **Estructura limpia** y profesional

---

**© 2025 RuloSoluciones. Todos los derechos reservados.**

*Esta regla es OBLIGATORIA para mantener la documentación centralizada y evitar redundancias.*
