<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestor de Archivos de Descargas - Detección Automática</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .content {
            padding: 30px;
        }
        
        .status-section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .status-indicator {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
        }
        
        .status-online {
            background: #28a745;
        }
        
        .status-offline {
            background: #dc3545;
        }
        
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .menu-item {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .menu-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-color: #4facfe;
        }
        
        .menu-item.disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .menu-item h3 {
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        
        .icon {
            font-size: 2em;
            margin-bottom: 10px;
            display: block;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 5px;
        }
        
        .btn-primary {
            background: #4facfe;
            color: white;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-warning {
            background: #ffc107;
            color: #212529;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .result-section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            display: none;
        }
        
        .result-section.show {
            display: block;
        }
        
        .file-list {
            max-height: 300px;
            overflow-y: auto;
            background: white;
            border-radius: 5px;
            padding: 15px;
            margin-top: 10px;
        }
        
        .file-item {
            padding: 8px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
        }
        
        .error {
            background: #ffe6e6;
            color: #d63031;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .success {
            background: #e6ffe6;
            color: #00b894;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .warning {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .server-info {
            background: #e3f2fd;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        
        @media (max-width: 768px) {
            .menu-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 Gestor de Archivos de Descargas</h1>
            <p>Detección Automática de Servidor</p>
        </div>
        
        <div class="content">
            <!-- Sección de Estado del Servidor -->
            <div class="status-section" id="status-section">
                <h3>🔍 Estado del Servidor</h3>
                <div id="server-status">
                    <span class="status-indicator status-offline" id="status-indicator"></span>
                    <span id="status-text">Verificando servidor...</span>
                </div>
                <div id="server-info" class="server-info" style="display: none;">
                    <p><strong>Servidor detectado:</strong> <span id="server-type">-</span></p>
                    <p><strong>Puerto:</strong> <span id="server-port">-</span></p>
                    <p><strong>URL:</strong> <span id="server-url">-</span></p>
                </div>
            </div>
            
            <!-- Menú Principal -->
            <div class="menu-grid" id="menu-grid">
                <div class="menu-item" onclick="verArchivos()" id="menu-ver">
                    <span class="icon">📋</span>
                    <h3>Ver Archivos</h3>
                    <p>Lista todos los archivos en descargas</p>
                </div>
                
                <div class="menu-item" onclick="buscarArchivos()" id="menu-buscar">
                    <span class="icon">🔍</span>
                    <h3>Buscar Archivos</h3>
                    <p>Busca archivos por nombre</p>
                </div>
                
                <div class="menu-item" onclick="organizarArchivos()" id="menu-organizar">
                    <span class="icon">🗂️</span>
                    <h3>Organizar Archivos</h3>
                    <p>Organiza por categorías</p>
                </div>
                
                <div class="menu-item" onclick="limpiarArchivos()" id="menu-limpiar">
                    <span class="icon">🧹</span>
                    <h3>Limpiar Archivos</h3>
                    <p>Elimina archivos antiguos</p>
                </div>
                
                <div class="menu-item" onclick="verEstadisticas()" id="menu-estadisticas">
                    <span class="icon">📊</span>
                    <h3>Estadísticas</h3>
                    <p>Ver estadísticas detalladas</p>
                </div>
                
                <div class="menu-item" onclick="ejecutarPython()" id="menu-python">
                    <span class="icon">🐍</span>
                    <h3>Ejecutar Python</h3>
                    <p>Ejecutar script Python</p>
                </div>
            </div>
            
            <!-- Botones de Acción -->
            <div style="text-align: center; margin: 20px 0;">
                <button class="btn btn-primary" onclick="actualizarEstadisticas()" id="btn-actualizar">🔄 Actualizar</button>
                <button class="btn btn-success" onclick="infoSistema()" id="btn-sistema">💻 Sistema</button>
                <button class="btn btn-warning" onclick="iniciarServidor()" id="btn-iniciar">🚀 Iniciar Servidor</button>
                <button class="btn btn-danger" onclick="limpiarResultados()" id="btn-limpiar">🗑️ Limpiar</button>
            </div>
            
            <!-- Sección de Resultados -->
            <div class="result-section" id="result-section">
                <h3 id="result-title">Resultados</h3>
                <div id="result-content"></div>
            </div>
        </div>
    </div>

    <script>
        let servidorActivo = false;
        let puertoActivo = null;
        let tipoServidor = null;
        
        // Verificar estado del servidor al cargar
        document.addEventListener('DOMContentLoaded', function() {
            verificarServidor();
        });
        
        async function verificarServidor() {
            const statusIndicator = document.getElementById('status-indicator');
            const statusText = document.getElementById('status-text');
            const serverInfo = document.getElementById('server-info');
            
            // Verificar XAMPP (puerto 80)
            try {
                const response80 = await fetch('http://localhost:80/test_web_simple.php', { 
                    method: 'GET',
                    mode: 'no-cors'
                });
                servidorActivo = true;
                puertoActivo = 80;
                tipoServidor = 'XAMPP';
                actualizarEstado(true, 'XAMPP', 80);
                return;
            } catch (e) {
                // XAMPP no está activo
            }
            
            // Verificar servidor PHP (puerto 8000)
            try {
                const response8000 = await fetch('http://localhost:8000/test_web_simple.php', { 
                    method: 'GET',
                    mode: 'no-cors'
                });
                servidorActivo = true;
                puertoActivo = 8000;
                tipoServidor = 'Servidor PHP';
                actualizarEstado(true, 'Servidor PHP', 8000);
                return;
            } catch (e) {
                // Servidor PHP no está activo
            }
            
            // Ningún servidor está activo
            servidorActivo = false;
            actualizarEstado(false);
        }
        
        function actualizarEstado(activo, tipo = null, puerto = null) {
            const statusIndicator = document.getElementById('status-indicator');
            const statusText = document.getElementById('status-text');
            const serverInfo = document.getElementById('server-info');
            const menuItems = document.querySelectorAll('.menu-item');
            const buttons = document.querySelectorAll('.btn');
            
            if (activo) {
                statusIndicator.className = 'status-indicator status-online';
                statusText.textContent = `✅ ${tipo} activo en puerto ${puerto}`;
                serverInfo.style.display = 'block';
                document.getElementById('server-type').textContent = tipo;
                document.getElementById('server-port').textContent = puerto;
                document.getElementById('server-url').textContent = `http://localhost:${puerto}/index_simple.php`;
                
                // Habilitar menú y botones
                menuItems.forEach(item => item.classList.remove('disabled'));
                buttons.forEach(btn => btn.disabled = false);
                
                // Cargar estadísticas automáticamente
                actualizarEstadisticas();
            } else {
                statusIndicator.className = 'status-indicator status-offline';
                statusText.textContent = '❌ No hay servidor activo';
                serverInfo.style.display = 'none';
                
                // Deshabilitar menú y botones
                menuItems.forEach(item => item.classList.add('disabled'));
                buttons.forEach(btn => {
                    if (!btn.id.includes('iniciar')) {
                        btn.disabled = true;
                    }
                });
                
                mostrarResultado('⚠️ Servidor No Disponible', 
                    '<div class="warning">' +
                    '<p><strong>No hay servidor PHP activo.</strong></p>' +
                    '<p>Opciones para solucionar:</p>' +
                    '<ul>' +
                    '<li>1. Ejecutar: <code>python servidor_automatico.py</code></li>' +
                    '<li>2. Iniciar XAMPP manualmente</li>' +
                    '<li>3. Ejecutar: <code>php -S localhost:8000</code></li>' +
                    '</ul>' +
                    '<p>Luego recarga esta página.</p>' +
                    '</div>');
            }
        }
        
        async function iniciarServidor() {
            mostrarResultado('🚀 Iniciando Servidor', 
                '<div class="loading">' +
                '<p>Intentando iniciar servidor automáticamente...</p>' +
                '<p>Si no funciona, ejecuta manualmente:</p>' +
                '<p><code>python servidor_automatico.py</code></p>' +
                '</div>');
            
            // Intentar abrir el script de servidor automático
            try {
                window.open('servidor_automatico.py', '_blank');
            } catch (e) {
                console.log('No se pudo abrir el archivo automáticamente');
            }
        }
        
        function mostrarResultado(titulo, contenido) {
            const resultSection = document.getElementById('result-section');
            const resultTitle = document.getElementById('result-title');
            const resultContent = document.getElementById('result-content');
            
            resultTitle.textContent = titulo;
            resultContent.innerHTML = contenido;
            resultSection.classList.add('show');
            resultSection.scrollIntoView({ behavior: 'smooth' });
        }
        
        function mostrarError(mensaje) {
            mostrarResultado('❌ Error', `<div class="error">${mensaje}</div>`);
        }
        
        function mostrarExito(mensaje) {
            mostrarResultado('✅ Éxito', `<div class="success">${mensaje}</div>`);
        }
        
        function mostrarCargando() {
            mostrarResultado('⏳ Procesando...', '<div class="loading">Cargando, por favor espera...</div>');
        }
        
        async function hacerPeticion(accion, datos = {}) {
            if (!servidorActivo) {
                mostrarError('No hay servidor activo. Inicia el servidor primero.');
                return null;
            }
            
            try {
                mostrarCargando();
                
                const formData = new FormData();
                formData.append('accion', accion);
                
                for (const [key, value] of Object.entries(datos)) {
                    formData.append(key, value);
                }
                
                const url = puertoActivo === 80 ? 'funciones_simple.php' : `http://localhost:${puertoActivo}/funciones_simple.php`;
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                
                const resultado = await response.text();
                return resultado;
                
            } catch (error) {
                mostrarError(`Error de conexión: ${error.message}`);
                return null;
            }
        }
        
        async function actualizarEstadisticas() {
            if (!servidorActivo) {
                verificarServidor();
                return;
            }
            
            const resultado = await hacerPeticion('estadisticas');
            if (resultado) {
                try {
                    const stats = JSON.parse(resultado);
                    mostrarExito(`Estadísticas actualizadas: ${stats.total_archivos || 0} archivos, ${stats.tamaño_total || '0 B'}`);
                } catch (e) {
                    mostrarError('Error al procesar estadísticas');
                }
            }
        }
        
        async function verArchivos() {
            if (!servidorActivo) {
                mostrarError('Servidor no disponible');
                return;
            }
            
            const resultado = await hacerPeticion('listar_archivos');
            if (resultado) {
                try {
                    const archivos = JSON.parse(resultado);
                    let html = '<div class="file-list">';
                    
                    if (archivos.length === 0) {
                        html += '<p>No se encontraron archivos</p>';
                    } else {
                        archivos.forEach(archivo => {
                            html += `
                                <div class="file-item">
                                    <span>${archivo.nombre}</span>
                                    <span>${archivo.tamaño}</span>
                                </div>
                            `;
                        });
                    }
                    
                    html += '</div>';
                    mostrarResultado('📋 Lista de Archivos', html);
                } catch (e) {
                    mostrarError('Error al procesar la lista de archivos');
                }
            }
        }
        
        async function buscarArchivos() {
            if (!servidorActivo) {
                mostrarError('Servidor no disponible');
                return;
            }
            
            const busqueda = prompt('Ingresa el nombre del archivo a buscar:');
            if (busqueda) {
                const resultado = await hacerPeticion('buscar_archivos', { busqueda });
                if (resultado) {
                    try {
                        const archivos = JSON.parse(resultado);
                        let html = '<div class="file-list">';
                        
                        if (archivos.length === 0) {
                            html += '<p>No se encontraron archivos</p>';
                        } else {
                            archivos.forEach(archivo => {
                                html += `
                                    <div class="file-item">
                                        <span>${archivo.nombre}</span>
                                        <span>${archivo.tamaño}</span>
                                    </div>
                                `;
                            });
                        }
                        
                        html += '</div>';
                        mostrarResultado(`🔍 Búsqueda: "${busqueda}"`, html);
                    } catch (e) {
                        mostrarError('Error al procesar la búsqueda');
                    }
                }
            }
        }
        
        async function organizarArchivos() {
            if (!servidorActivo) {
                mostrarError('Servidor no disponible');
                return;
            }
            
            const resultado = await hacerPeticion('organizar_archivos');
            if (resultado) {
                try {
                    const datos = JSON.parse(resultado);
                    mostrarExito(`Organización completada: ${datos.organizados || 0} archivos organizados`);
                } catch (e) {
                    mostrarError('Error al procesar la organización');
                }
            }
        }
        
        async function limpiarArchivos() {
            if (!servidorActivo) {
                mostrarError('Servidor no disponible');
                return;
            }
            
            const dias = prompt('Días para considerar archivos como antiguos (ej: 30):');
            if (dias && !isNaN(dias)) {
                const resultado = await hacerPeticion('limpiar_archivos', { dias });
                if (resultado) {
                    try {
                        const datos = JSON.parse(resultado);
                        mostrarExito(`Limpieza completada: ${datos.eliminados || 0} archivos eliminados`);
                    } catch (e) {
                        mostrarError('Error al procesar la limpieza');
                    }
                }
            }
        }
        
        async function verEstadisticas() {
            if (!servidorActivo) {
                mostrarError('Servidor no disponible');
                return;
            }
            
            const resultado = await hacerPeticion('estadisticas_detalladas');
            if (resultado) {
                try {
                    const stats = JSON.parse(resultado);
                    let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">';
                    
                    for (const [categoria, cantidad] of Object.entries(stats.categorias || {})) {
                        html += `
                            <div style="background: white; padding: 10px; border-radius: 5px; text-align: center;">
                                <div style="font-size: 1.5em; font-weight: bold; color: #4facfe;">${cantidad}</div>
                                <div style="font-size: 0.9em; color: #666;">${categoria}</div>
                            </div>
                        `;
                    }
                    
                    html += '</div>';
                    mostrarResultado('📊 Estadísticas Detalladas', html);
                } catch (e) {
                    mostrarError('Error al procesar estadísticas');
                }
            }
        }
        
        async function ejecutarPython() {
            if (!servidorActivo) {
                mostrarError('Servidor no disponible');
                return;
            }
            
            const resultado = await hacerPeticion('ejecutar_python');
            if (resultado) {
                mostrarResultado('🐍 Ejecución Python', `<pre>${resultado}</pre>`);
            }
        }
        
        async function infoSistema() {
            if (!servidorActivo) {
                mostrarError('Servidor no disponible');
                return;
            }
            
            const resultado = await hacerPeticion('info_sistema');
            if (resultado) {
                try {
                    const info = JSON.parse(resultado);
                    let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">';
                    
                    for (const [categoria, valor] of Object.entries(info)) {
                        html += `
                            <div style="background: white; padding: 10px; border-radius: 5px; text-align: center;">
                                <div style="font-size: 1.2em; font-weight: bold; color: #4facfe;">${valor}</div>
                                <div style="font-size: 0.9em; color: #666;">${categoria}</div>
                            </div>
                        `;
                    }
                    
                    html += '</div>';
                    mostrarResultado('💻 Información del Sistema', html);
                } catch (e) {
                    mostrarResultado('💻 Información del Sistema', `<pre>${resultado}</pre>`);
                }
            }
        }
        
        function limpiarResultados() {
            document.getElementById('result-section').classList.remove('show');
        }
    </script>
</body>
</html>
