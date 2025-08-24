# 🚨 REEMPLAZO URGENTE - API LOGIN

## ❌ **PROBLEMA DETECTADO:**

El endpoint `/api/login` está devolviendo **404 Not Found**, lo que significa que el archivo `index_final_modustackclean.php` **NO está siendo ejecutado** en el servidor.

## 🔧 **SOLUCIÓN INMEDIATA:**

### **PASO 1: Descargar el archivo correcto**
```bash
# El archivo index_final_modustackclean.php contiene el endpoint /api/login
# Necesitas reemplazar completamente el index.php del servidor
```

### **PASO 2: Reemplazar en el servidor**
1. **Accede a tu servidor** (FTP, cPanel, etc.)
2. **Ve a la carpeta:** `/modustackclean/`
3. **Elimina el archivo actual:** `index.php`
4. **Sube el archivo:** `index_final_modustackclean.php` como `index.php`

### **PASO 3: Verificar el reemplazo**
El archivo `index.php` en el servidor debe contener **TODOS** estos endpoints:

```php
// Endpoints disponibles:
- "/api/ping"
- "/api/usuarios" 
- "/api/login"        ← ESTE ES EL QUE FALTA
- "/api/prueba"
- "/api/health"
- "/api/info"
```

## 📋 **CONTENIDO DEL ARCHIVO CORRECTO:**

El archivo `index.php` en el servidor debe contener **EXACTAMENTE** el contenido de `index_final_modustackclean.php`, que incluye:

```php
// Endpoint login
if ($clean_path === '/api/login' && $method === 'POST') {
    try {
        // Obtener datos del POST
        $input = json_decode(file_get_contents('php://input'), true);
        
        if (!$input) {
            respuesta_json(false, "Datos de entrada inválidos", [], 400);
        }
        
        $correo = $input['correo'] ?? '';
        $password = $input['password'] ?? '';
        
        if (empty($correo) || empty($password)) {
            respuesta_json(false, "Correo y contraseña son requeridos", [], 400);
        }
        
        $conexion = conectar_bd();
        
        // Buscar usuario por correo
        $stmt = $conexion->prepare('SELECT id, nombre, correo, rol, estado, creado_en FROM usuarios WHERE correo = ?');
        $stmt->bind_param('s', $correo);
        
        if (!$stmt->execute()) {
            throw new Exception('Error ejecutando consulta: ' . $stmt->error);
        }
        
        $res = $stmt->get_result();
        $usuario = $res->fetch_assoc();
        
        if (!$usuario) {
            respuesta_json(false, "Usuario no encontrado", [], 401);
        }
        
        // Verificar estado del usuario
        if ($usuario['estado'] != 1) {
            respuesta_json(false, "Usuario inactivo", [], 401);
        }
        
        respuesta_json(true, "Login exitoso", [
            "usuario" => $usuario
        ]);
        
    } catch (Exception $e) {
        respuesta_json(false, "Error en login", [
            "error" => $e->getMessage()
        ], 500);
    } finally {
        if (isset($conexion)) {
            $conexion->close();
        }
    }
}
```

## 🧪 **PRUEBA DESPUÉS DEL REEMPLAZO:**

```bash
python test_login_api.py
```

**Resultado esperado:**
```
3️⃣ Probando login con usuario: juan@test.com
📊 Status Code: 200
✅ Login exitoso: Juan Carlos Díaz
```

## 🚨 **IMPORTANTE:**

- **NO** subas el archivo como `index_final_modustackclean.php`
- **SÍ** súbelo como `index.php` (reemplazando el existente)
- **Verifica** que el archivo se subió correctamente
- **Prueba** el endpoint `/api/login` después del reemplazo

## ✅ **VERIFICACIÓN FINAL:**

Después del reemplazo, ejecuta:
```bash
python cliente_api_fixed.py
```

Deberías ver que **TODOS** los endpoints funcionan, incluyendo `/api/login`.

**¡El problema se resolverá inmediatamente después del reemplazo!** 🚀
