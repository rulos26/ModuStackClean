<?php
header('Content-Type: application/json; charset=utf-8');

// Configuración
$descargas_path = obtener_ruta_descargas();
$categorias = [
    'documentos' => ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'xls', 'xlsx', 'ppt', 'pptx', 'csv'],
    'imagenes' => ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg', 'webp'],
    'videos' => ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v'],
    'musica' => ['mp3', 'wav', 'flac', 'aac', 'ogg', 'wma', 'm4a'],
    'comprimidos' => ['zip', 'rar', '7z', 'tar', 'gz', 'bz2'],
    'ejecutables' => ['exe', 'msi', 'dmg', 'pkg', 'deb', 'rpm', 'app'],
    'otros' => []
];

// Obtener la acción solicitada
$accion = $_POST['accion'] ?? '';

try {
    switch ($accion) {
        case 'estadisticas':
            echo json_encode(obtener_estadisticas());
            break;
            
        case 'listar_archivos':
            echo json_encode(listar_archivos());
            break;
            
        case 'buscar_archivos':
            $busqueda = $_POST['busqueda'] ?? '';
            echo json_encode(buscar_archivos($busqueda));
            break;
            
        case 'organizar_archivos':
            echo json_encode(organizar_archivos());
            break;
            
        case 'limpiar_archivos':
            $dias = intval($_POST['dias'] ?? 30);
            echo json_encode(limpiar_archivos($dias));
            break;
            
        case 'estadisticas_detalladas':
            echo json_encode(obtener_estadisticas_detalladas());
            break;
            
        case 'ejecutar_python':
            echo json_encode(ejecutar_script_python());
            break;
            
        case 'info_sistema':
            echo json_encode(obtener_info_sistema());
            break;
            
        default:
            echo json_encode(['error' => 'Acción no válida: ' . $accion]);
    }
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}

function obtener_ruta_descargas() {
    $sistema = PHP_OS_FAMILY;
    
    if ($sistema === 'Windows') {
        $userprofile = $_SERVER['USERPROFILE'] ?? getenv('USERPROFILE');
        if (!$userprofile) {
            $userprofile = 'C:\\Users\\' . get_current_user();
        }
        return $userprofile . '\\Downloads';
    } elseif ($sistema === 'Darwin') { // macOS
        return $_SERVER['HOME'] . '/Downloads';
    } else { // Linux
        return $_SERVER['HOME'] . '/Downloads';
    }
}

function obtener_estadisticas() {
    global $descargas_path;
    
    if (!is_dir($descargas_path)) {
        return ['error' => 'Carpeta de descargas no encontrada: ' . $descargas_path];
    }
    
    $total_archivos = 0;
    $tamaño_total = 0;
    $archivos_recientes = 0;
    $hace_7_dias = time() - (7 * 24 * 60 * 60);
    
    try {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($descargas_path, RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $total_archivos++;
                $tamaño_total += $file->getSize();
                
                if ($file->getMTime() > $hace_7_dias) {
                    $archivos_recientes++;
                }
            }
        }
    } catch (Exception $e) {
        // Fallback para versiones antiguas de PHP
        $total_archivos = contar_archivos_fallback($descargas_path);
        $tamaño_total = calcular_tamaño_fallback($descargas_path);
    }
    
    // Calcular uso de disco
    $uso_disco = '0%';
    if (function_exists('disk_free_space') && function_exists('disk_total_space')) {
        $espacio_libre = disk_free_space($descargas_path);
        $espacio_total = disk_total_space($descargas_path);
        if ($espacio_total > 0) {
            $uso_disco = round((($espacio_total - $espacio_libre) / $espacio_total) * 100, 1) . '%';
        }
    }
    
    return [
        'total_archivos' => $total_archivos,
        'tamaño_total' => formatear_tamaño($tamaño_total),
        'archivos_recientes' => $archivos_recientes,
        'uso_disco' => $uso_disco
    ];
}

function listar_archivos() {
    global $descargas_path;
    
    if (!is_dir($descargas_path)) {
        return [];
    }
    
    $archivos = [];
    
    try {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($descargas_path, RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $archivos[] = [
                    'nombre' => $file->getFilename(),
                    'tamaño' => formatear_tamaño($file->getSize()),
                    'fecha' => date('Y-m-d H:i:s', $file->getMTime())
                ];
            }
        }
    } catch (Exception $e) {
        // Fallback
        $archivos = listar_archivos_fallback($descargas_path);
    }
    
    // Ordenar por fecha (más recientes primero)
    usort($archivos, function($a, $b) {
        return strtotime($b['fecha']) - strtotime($a['fecha']);
    });
    
    return array_slice($archivos, 0, 30); // Limitar a 30 archivos
}

function buscar_archivos($busqueda) {
    global $descargas_path;
    
    if (!is_dir($descargas_path) || empty($busqueda)) {
        return [];
    }
    
    $archivos = [];
    $busqueda_lower = strtolower($busqueda);
    
    try {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($descargas_path, RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $nombre = $file->getFilename();
                if (strpos(strtolower($nombre), $busqueda_lower) !== false) {
                    $archivos[] = [
                        'nombre' => $nombre,
                        'tamaño' => formatear_tamaño($file->getSize()),
                        'fecha' => date('Y-m-d H:i:s', $file->getMTime())
                    ];
                }
            }
        }
    } catch (Exception $e) {
        // Fallback
        $archivos = buscar_archivos_fallback($descargas_path, $busqueda);
    }
    
    return array_slice($archivos, 0, 15); // Limitar a 15 resultados
}

function organizar_archivos() {
    global $descargas_path, $categorias;
    
    if (!is_dir($descargas_path)) {
        return ['error' => 'Carpeta de descargas no encontrada'];
    }
    
    $organizados = 0;
    $errores = 0;
    $duplicados = 0;
    
    try {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($descargas_path, RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $resultado = mover_archivo_a_categoria($file, $categorias);
                if ($resultado === 'organizado') {
                    $organizados++;
                } elseif ($resultado === 'duplicado') {
                    $duplicados++;
                } else {
                    $errores++;
                }
            }
        }
    } catch (Exception $e) {
        $errores++;
    }
    
    return [
        'organizados' => $organizados,
        'errores' => $errores,
        'duplicados' => $duplicados
    ];
}

function limpiar_archivos($dias) {
    global $descargas_path;
    
    if (!is_dir($descargas_path)) {
        return ['error' => 'Carpeta de descargas no encontrada'];
    }
    
    $eliminados = 0;
    $espacio_liberado = 0;
    $fecha_limite = time() - ($dias * 24 * 60 * 60);
    
    try {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($descargas_path, RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile() && $file->getMTime() < $fecha_limite) {
                $tamaño = $file->getSize();
                if (unlink($file->getPathname())) {
                    $eliminados++;
                    $espacio_liberado += $tamaño;
                }
            }
        }
    } catch (Exception $e) {
        // Error silencioso
    }
    
    return [
        'eliminados' => $eliminados,
        'espacio_liberado' => formatear_tamaño($espacio_liberado)
    ];
}

function obtener_estadisticas_detalladas() {
    global $descargas_path, $categorias;
    
    if (!is_dir($descargas_path)) {
        return ['error' => 'Carpeta de descargas no encontrada'];
    }
    
    $categorias_count = array_fill_keys(array_keys($categorias), 0);
    $extensiones = [];
    
    try {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($descargas_path, RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $extension = strtolower(pathinfo($file->getFilename(), PATHINFO_EXTENSION));
                
                // Contar extensiones
                if (!empty($extension)) {
                    $extensiones[$extension] = ($extensiones[$extension] ?? 0) + 1;
                }
                
                // Categorizar
                $categoria_encontrada = false;
                foreach ($categorias as $categoria => $exts) {
                    if (in_array($extension, $exts)) {
                        $categorias_count[$categoria]++;
                        $categoria_encontrada = true;
                        break;
                    }
                }
                
                if (!$categoria_encontrada) {
                    $categorias_count['otros']++;
                }
            }
        }
    } catch (Exception $e) {
        // Error silencioso
    }
    
    return [
        'categorias' => $categorias_count,
        'top_extensiones' => array_slice($extensiones, 0, 10, true)
    ];
}

function ejecutar_script_python() {
    $script_path = __DIR__ . '/gestor_descargas.py';
    
    if (!file_exists($script_path)) {
        return ['error' => 'Script Python no encontrado'];
    }
    
    $comando = 'python "' . $script_path . '" --version 2>&1';
    $output = shell_exec($comando);
    
    if ($output === null) {
        return ['error' => 'No se pudo ejecutar el script Python'];
    }
    
    return ['output' => $output];
}

function obtener_info_sistema() {
    $info = [];
    
    // Información básica del sistema
    $info['Sistema Operativo'] = PHP_OS_FAMILY;
    $info['Versión PHP'] = PHP_VERSION;
    
    // Memoria
    if (function_exists('memory_get_usage')) {
        $info['Memoria PHP'] = formatear_tamaño(memory_get_usage(true));
    }
    
    // Información del servidor
    $info['Directorio Actual'] = __DIR__;
    $info['Carpeta Descargas'] = obtener_ruta_descargas();
    
    return $info;
}

function mover_archivo_a_categoria($file, $categorias) {
    global $descargas_path;
    
    $extension = strtolower(pathinfo($file->getFilename(), PATHINFO_EXTENSION));
    $categoria_destino = 'otros';
    
    // Determinar categoría
    foreach ($categorias as $categoria => $exts) {
        if (in_array($extension, $exts)) {
            $categoria_destino = $categoria;
            break;
        }
    }
    
    // Crear directorio de categoría
    $dir_categoria = $descargas_path . '/' . $categoria_destino;
    if (!is_dir($dir_categoria)) {
        if (!mkdir($dir_categoria, 0755, true)) {
            return 'error';
        }
    }
    
    // Para documentos, crear subcarpetas por extensión
    if ($categoria_destino === 'documentos' && !empty($extension)) {
        $subdir = $dir_categoria . '/' . $extension;
        if (!is_dir($subdir)) {
            if (!mkdir($subdir, 0755, true)) {
                return 'error';
            }
        }
        $dir_categoria = $subdir;
    }
    
    $archivo_origen = $file->getPathname();
    $archivo_destino = $dir_categoria . '/' . $file->getFilename();
    
    // Manejar duplicados
    if (file_exists($archivo_destino)) {
        $nombre_base = pathinfo($file->getFilename(), PATHINFO_FILENAME);
        $extension_archivo = pathinfo($file->getFilename(), PATHINFO_EXTENSION);
        $contador = 1;
        
        do {
            $nuevo_nombre = $nombre_base . '_v' . $contador . '.' . $extension_archivo;
            $archivo_destino = $dir_categoria . '/' . $nuevo_nombre;
            $contador++;
        } while (file_exists($archivo_destino));
        
        return 'duplicado';
    }
    
    // Mover archivo
    if (rename($archivo_origen, $archivo_destino)) {
        return 'organizado';
    }
    
    return 'error';
}

function formatear_tamaño($bytes) {
    $unidades = ['B', 'KB', 'MB', 'GB', 'TB'];
    $bytes = max($bytes, 0);
    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
    $pow = min($pow, count($unidades) - 1);
    
    $bytes /= pow(1024, $pow);
    
    return round($bytes, 2) . ' ' . $unidades[$pow];
}

// Funciones de fallback para versiones antiguas de PHP
function contar_archivos_fallback($directorio) {
    $contador = 0;
    $archivos = scandir($directorio);
    
    foreach ($archivos as $archivo) {
        if ($archivo !== '.' && $archivo !== '..') {
            $ruta = $directorio . '/' . $archivo;
            if (is_file($ruta)) {
                $contador++;
            } elseif (is_dir($ruta)) {
                $contador += contar_archivos_fallback($ruta);
            }
        }
    }
    
    return $contador;
}

function calcular_tamaño_fallback($directorio) {
    $tamaño = 0;
    $archivos = scandir($directorio);
    
    foreach ($archivos as $archivo) {
        if ($archivo !== '.' && $archivo !== '..') {
            $ruta = $directorio . '/' . $archivo;
            if (is_file($ruta)) {
                $tamaño += filesize($ruta);
            } elseif (is_dir($ruta)) {
                $tamaño += calcular_tamaño_fallback($ruta);
            }
        }
    }
    
    return $tamaño;
}

function listar_archivos_fallback($directorio) {
    $archivos = [];
    $items = scandir($directorio);
    
    foreach ($items as $item) {
        if ($item !== '.' && $item !== '..') {
            $ruta = $directorio . '/' . $item;
            if (is_file($ruta)) {
                $archivos[] = [
                    'nombre' => $item,
                    'tamaño' => formatear_tamaño(filesize($ruta)),
                    'fecha' => date('Y-m-d H:i:s', filemtime($ruta))
                ];
            }
        }
    }
    
    return $archivos;
}

function buscar_archivos_fallback($directorio, $busqueda) {
    $archivos = [];
    $busqueda_lower = strtolower($busqueda);
    $items = scandir($directorio);
    
    foreach ($items as $item) {
        if ($item !== '.' && $item !== '..') {
            $ruta = $directorio . '/' . $item;
            if (is_file($ruta)) {
                if (strpos(strtolower($item), $busqueda_lower) !== false) {
                    $archivos[] = [
                        'nombre' => $item,
                        'tamaño' => formatear_tamaño(filesize($ruta)),
                        'fecha' => date('Y-m-d H:i:s', filemtime($ruta))
                    ];
                }
            }
        }
    }
    
    return $archivos;
}
?>
