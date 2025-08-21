<?php
/**
 * ModuStackClean - Sistema Principal
 * Archivo de entrada principal con sistema de enrutamiento
 */

// Configuración básica
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Obtener la URL solicitada
$request_uri = $_SERVER['REQUEST_URI'];
$base_path = '/ModuStackClean/';

// Extraer la ruta después del directorio base
$path = str_replace($base_path, '', $request_uri);
$path = parse_url($path, PHP_URL_PATH);

// Limpiar la ruta
$path = trim($path, '/');

// Si no hay ruta específica, usar la ruta por defecto
if (empty($path)) {
    $path = 'index';
}

// Mapeo de rutas a archivos
$routes = [
    'index' => 'web/backend/navegacion.php',
    'index.php' => 'web/backend/navegacion.php',
    'navegacion' => 'web/backend/navegacion.php',
    'navegacion.php' => 'web/backend/navegacion.php',
    'principal' => 'web/backend/index.php',
    'principal.php' => 'web/backend/index.php',
    'index_automatico' => 'web/backend/index_automatico.php',
    'index_automatico.php' => 'web/backend/index_automatico.php',
    'index_simple' => 'web/backend/index_simple.php',
    'index_simple.php' => 'web/backend/index_simple.php',
    'funciones' => 'web/backend/funciones.php',
    'funciones.php' => 'web/backend/funciones.php',
    'funciones_simple' => 'web/backend/funciones_simple.php',
    'funciones_simple.php' => 'web/backend/funciones_simple.php'
];

// Verificar si la ruta existe
if (isset($routes[$path])) {
    $file_path = $routes[$path];
    
    if (file_exists($file_path)) {
        // Incluir el archivo correspondiente
        include_once $file_path;
    } else {
        // Archivo no encontrado
        echo "<h1>ModuStackClean - Error 404</h1>";
        echo "<p>El archivo <code>$file_path</code> no existe.</p>";
        echo "<p>Ruta solicitada: <code>$path</code></p>";
        echo "<h2>Rutas disponibles:</h2>";
        echo "<ul>";
        foreach ($routes as $route => $file) {
            echo "<li><a href='$base_path$route'>$route</a> → $file</li>";
        }
        echo "</ul>";
    }
} else {
    // Ruta no encontrada
    echo "<h1>ModuStackClean - Error 404</h1>";
    echo "<p>La ruta <code>$path</code> no existe.</p>";
    echo "<h2>Rutas disponibles:</h2>";
    echo "<ul>";
    foreach ($routes as $route => $file) {
        echo "<li><a href='$base_path$route'>$route</a> → $file</li>";
    }
    echo "</ul>";
    
    echo "<h2>Información de Debug:</h2>";
    echo "<ul>";
    echo "<li>URL solicitada: " . htmlspecialchars($request_uri) . "</li>";
    echo "<li>Ruta extraída: " . htmlspecialchars($path) . "</li>";
    echo "<li>Directorio base: " . htmlspecialchars($base_path) . "</li>";
    echo "<li>Directorio actual: " . getcwd() . "</li>";
    echo "</ul>";
}
?>
