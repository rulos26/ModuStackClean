<?php
// Test simple para verificar que PHP funciona
echo "PHP está funcionando correctamente!";
echo "<br>";
echo "Versión de PHP: " . PHP_VERSION;
echo "<br>";
echo "Sistema Operativo: " . PHP_OS_FAMILY;
echo "<br>";
echo "Directorio actual: " . __DIR__;
echo "<br>";
echo "Archivos en el directorio:";
echo "<ul>";

$archivos = scandir(__DIR__);
foreach ($archivos as $archivo) {
    if ($archivo !== '.' && $archivo !== '..') {
        echo "<li>$archivo</li>";
    }
}
echo "</ul>";
?>
