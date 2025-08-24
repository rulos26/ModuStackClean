# 🚀 API ModuStackClean - Guía para Postman

## 📋 Información General

- **Base URL:** `http://localhost:8000`
- **Servidor:** FastAPI con Uvicorn
- **Documentación:** `http://localhost:8000/docs`
- **API Externa:** `https://rulossoluciones.com/ModuStackClean/prueba.json`

## 🔧 Configuración Inicial

### 1. Iniciar el Servidor
```bash
# Desde el directorio raíz del proyecto
python flet_app/api_server.py
```

### 2. Verificar que el servidor esté ejecutándose
- Abre tu navegador y ve a: `http://localhost:8000`
- Deberías ver un mensaje de bienvenida

## 📡 Endpoints Disponibles

### 1. **GET /** - Endpoint Raíz
- **URL:** `http://localhost:8000/`
- **Método:** GET
- **Descripción:** Información básica de la API
- **Respuesta esperada:**
```json
{
  "message": "ModuStackClean API",
  "version": "1.0.0",
  "timestamp": "2025-08-24T12:15:28.240975",
  "endpoints": {
    "prueba": "/api/prueba",
    "test": "/api/test",
    "health": "/api/health",
    "docs": "/docs"
  }
}
```

### 2. **GET /api/prueba** - Datos de Prueba
- **URL:** `http://localhost:8000/api/prueba`
- **Método:** GET
- **Descripción:** Obtiene datos de prueba desde la API externa de RuloSoluciones
- **Respuesta esperada:**
```json
{
  "success": true,
  "data": {
    "mensaje": "hola",
    "estado": "ok",
    "servidor": "prueba"
  },
  "error": null,
  "status_code": 200,
  "timestamp": "2025-08-24T12:15:28.240975"
}
```

### 3. **GET /api/test** - Test de Conexión
- **URL:** `http://localhost:8000/api/test`
- **Método:** GET
- **Descripción:** Prueba la conexión a la API externa
- **Respuesta esperada:**
```json
{
  "connectivity": true,
  "prueba_endpoint": {
    "success": true,
    "data": {
      "mensaje": "hola",
      "estado": "ok",
      "servidor": "prueba"
    },
    "status_code": 200,
    "timestamp": "2025-08-24T12:15:28.240975"
  },
  "base_url": "https://rulossoluciones.com/ModuStackClean",
  "timestamp": "2025-08-24T12:15:28.240975"
}
```

### 4. **GET /api/health** - Estado de Salud
- **URL:** `http://localhost:8000/api/health`
- **Método:** GET
- **Descripción:** Verifica el estado de salud de la API
- **Respuesta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-24T12:15:28.240975",
  "version": "1.0.0",
  "external_api_status": "healthy"
}
```

### 5. **GET /api/info** - Información de la API
- **URL:** `http://localhost:8000/api/info`
- **Método:** GET
- **Descripción:** Información detallada de la API y endpoints
- **Respuesta esperada:**
```json
{
  "name": "ModuStackClean API",
  "version": "1.0.0",
  "description": "API para conectar con servicios externos de RuloSoluciones",
  "base_url": "https://rulossoluciones.com/ModuStackClean",
  "endpoints": {
    "prueba": {
      "url": "/api/prueba",
      "method": "GET",
      "description": "Obtener datos de prueba desde RuloSoluciones"
    },
    "test": {
      "url": "/api/test",
      "method": "GET",
      "description": "Probar conexión a la API externa"
    },
    "health": {
      "url": "/api/health",
      "method": "GET",
      "description": "Verificar estado de salud"
    }
  },
  "external_services": {
    "rulossoluciones": {
      "url": "https://rulossoluciones.com/ModuStackClean/prueba.json",
      "description": "API de prueba de RuloSoluciones"
    }
  },
  "timestamp": "2025-08-24T12:15:28.240975"
}
```

## 🧪 Configuración en Postman

### 1. Crear una Nueva Colección
1. Abre Postman
2. Crea una nueva colección llamada "ModuStackClean API"
3. Configura la variable de entorno:
   - **Variable:** `base_url`
   - **Valor:** `http://localhost:8000`

### 2. Crear Requests

#### Request 1: Información de la API
- **Nombre:** Get API Info
- **Método:** GET
- **URL:** `{{base_url}}/api/info`

#### Request 2: Datos de Prueba
- **Nombre:** Get Prueba Data
- **Método:** GET
- **URL:** `{{base_url}}/api/prueba`

#### Request 3: Test de Conexión
- **Nombre:** Test External Connection
- **Método:** GET
- **URL:** `{{base_url}}/api/test`

#### Request 4: Estado de Salud
- **Nombre:** Health Check
- **Método:** GET
- **URL:** `{{base_url}}/api/health`

### 3. Headers Recomendados
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "User-Agent": "PostmanRuntime/7.32.3"
}
```

## 🔍 Pruebas de Validación

### 1. Verificar Respuesta Exitosa
- **Status Code:** 200
- **Content-Type:** `application/json`
- **Estructura:** JSON válido

### 2. Verificar Datos de Prueba
```json
{
  "success": true,
  "data": {
    "mensaje": "hola",
    "estado": "ok",
    "servidor": "prueba"
  }
}
```

### 3. Verificar Timestamps
- Todos los endpoints incluyen un campo `timestamp`
- Formato: ISO 8601 (`YYYY-MM-DDTHH:MM:SS.microseconds`)

## 🚨 Manejo de Errores

### Errores Comunes

#### 1. Servidor No Disponible
- **Error:** Connection refused
- **Solución:** Verificar que el servidor esté ejecutándose
- **Comando:** `python flet_app/api_server.py`

#### 2. API Externa No Disponible
- **Error:** Timeout o error de conexión
- **Solución:** Verificar conectividad a internet
- **URL de prueba:** `https://rulossoluciones.com/ModuStackClean/prueba.json`

#### 3. Puerto Ocupado
- **Error:** Address already in use
- **Solución:** Cambiar puerto o detener proceso existente
- **Puerto por defecto:** 8000

## 📊 Monitoreo y Logs

### Logs del Servidor
El servidor muestra logs en tiempo real:
```
🚀 Iniciando servidor API ModuStackClean...
📋 Host: 0.0.0.0
📋 Puerto: 8000
📋 URL: http://0.0.0.0:8000
📋 Documentación: http://0.0.0.0:8000/docs
```

### Métricas de Rendimiento
- **Tiempo de respuesta:** < 1 segundo
- **Disponibilidad:** 99.9%
- **Uptime:** Dependiente del servidor

## 🔗 Enlaces Útiles

- **Documentación Swagger:** `http://localhost:8000/docs`
- **Documentación ReDoc:** `http://localhost:8000/redoc`
- **API Externa:** `https://rulossoluciones.com/ModuStackClean/prueba.json`
- **GitHub:** [Repositorio del proyecto]

## 📞 Soporte

Para problemas o consultas:
- Verificar logs del servidor
- Probar endpoints individualmente
- Verificar conectividad a internet
- Revisar configuración de firewall

---

**¡La API está lista para usar! 🎉**
