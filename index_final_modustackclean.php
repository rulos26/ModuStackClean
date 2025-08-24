<?php
// index.php - API ModuStackClean FINAL Y DEFINITIVO
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

// Configuración DB (tu configuración exacta)
$host     = "127.0.0.1";
$usuario  = "u494150416_rulos26";
$clave    = "0382646740Ju*";
$bd       = "u494150416_modustackclean";
$puerto   = 3306;

// Obtener la ruta
$path = $_SERVER['REQUEST_URI'] ?? '';
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

// Función para limpiar ruta
function clean_path($path) {
    $clean = str_replace('/modustackclean', '', $path);
    $clean = rtrim($clean, '/');
    return $clean;
}

$clean_path = clean_path($path);

// Función para responder JSON y terminar ejecución
function respuesta_json($ok, $mensaje, $data = null, $codigo_http = 200) {
    http_response_code($codigo_http);
    echo json_encode([
        "ok"      => $ok,
        "mensaje" => $mensaje,
        "data"    => $data,
        "timestamp" => date('Y-m-d H:i:s')
    ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit; // CRÍTICO: Terminar ejecución aquí
}

// Función para conectar a la BD
function conectar_bd() {
    global $host, $usuario, $clave, $bd, $puerto;
    
    $conexion = @new mysqli($host, $usuario, $clave, $bd, $puerto);
    
    if ($conexion->connect_errno) {
        respuesta_json(false, "Error de conexión a la base de datos", [
            "codigo" => $conexion->connect_errno,
            "detalle" => $conexion->connect_error
        ], 500);
    }
    
    $conexion->set_charset('utf8mb4');
    return $conexion;
}

// Endpoint para ruta base
if ($clean_path === '' || $clean_path === '/') {
    respuesta_json(true, "ModuStackClean API funcionando", [
        "endpoints" => [
            "ping" => "/api/ping",
            "usuarios" => "/api/usuarios",
            "prueba" => "/api/prueba",
            "health" => "/api/health",
            "info" => "/api/info"
        ]
    ]);
}

// Endpoint ping
if ($clean_path === '/api/ping') {
    respuesta_json(true, "pong", [
        "server" => "ModuStackClean API"
    ]);
}

// Endpoint info
if ($clean_path === '/api/info') {
    respuesta_json(true, "Información de la API", [
        "name" => "ModuStackClean API",
        "version" => "1.0.0",
        "endpoints" => [
            "ping" => "/api/ping",
            "usuarios" => "/api/usuarios",
            "prueba" => "/api/prueba",
            "health" => "/api/health",
            "info" => "/api/info"
        ]
    ]);
}

// Endpoint usuarios
if ($clean_path === '/api/usuarios' && $method === 'GET') {
    try {
        $conexion = conectar_bd();
        
        $limit = 50;
        $stmt = $conexion->prepare('SELECT id, nombre, correo, rol, estado, creado_en FROM usuarios LIMIT ?');
        $stmt->bind_param('i', $limit);
        
        if (!$stmt->execute()) {
            throw new Exception('Error ejecutando consulta: ' . $stmt->error);
        }
        
        $res = $stmt->get_result();
        $data = $res->fetch_all(MYSQLI_ASSOC);
        
        respuesta_json(true, "Usuarios obtenidos exitosamente", [
            "usuarios" => $data,
            "count" => count($data)
        ]);
        
    } catch (Exception $e) {
        respuesta_json(false, "Error obteniendo usuarios", [
            "error" => $e->getMessage()
        ], 500);
    } finally {
        if (isset($conexion)) {
            $conexion->close();
        }
    }
}

// Endpoint prueba
if ($clean_path === '/api/prueba' && $method === 'GET') {
    try {
        $conexion = conectar_bd();
        
        $sql = "SELECT 1 as usuarios";
        $resultado = $conexion->query($sql);
        
        if (!$resultado) {
            throw new Exception('Error ejecutando consulta: ' . $conexion->error);
        }
        
        $data = [];
        while ($fila = $resultado->fetch_assoc()) {
            $data[] = $fila;
        }
        
        respuesta_json(true, "Prueba de conexión exitosa", [
            "prueba" => $data
        ]);
        
    } catch (Exception $e) {
        respuesta_json(false, "Error en prueba de conexión", [
            "error" => $e->getMessage()
        ], 500);
    } finally {
        if (isset($conexion)) {
            $conexion->close();
        }
    }
}

// Endpoint health
if ($clean_path === '/api/health' && $method === 'GET') {
    try {
        $conexion = conectar_bd();
        
        $sql = "SELECT 1 as test";
        $resultado = $conexion->query($sql);
        
        if ($resultado) {
            respuesta_json(true, "Estado de salud verificado", [
                "status" => "healthy",
                "database" => "connected",
                "server_info" => $conexion->server_info
            ]);
        } else {
            throw new Exception('Error verificando estado de salud');
        }
        
    } catch (Exception $e) {
        respuesta_json(false, "Error verificando estado de salud", [
            "status" => "unhealthy",
            "database" => "disconnected",
            "error" => $e->getMessage()
        ], 500);
    } finally {
        if (isset($conexion)) {
            $conexion->close();
        }
    }
}

// Endpoint no encontrado
respuesta_json(false, "Endpoint no encontrado", [
    "available_endpoints" => [
        "/api/ping",
        "/api/usuarios",
        "/api/prueba",
        "/api/health",
        "/api/info"
    ]
], 404);
?>
