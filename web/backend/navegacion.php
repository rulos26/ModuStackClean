<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ModuStackClean - Navegación Principal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section h2 {
            color: #333;
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 3px solid #4facfe;
            padding-bottom: 10px;
        }
        
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .menu-item {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: #333;
            display: block;
        }
        
        .menu-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.15);
            border-color: #4facfe;
            background: #fff;
        }
        
        .menu-item h3 {
            font-size: 1.4em;
            margin-bottom: 15px;
            color: #4facfe;
        }
        
        .menu-item p {
            color: #666;
            line-height: 1.6;
        }
        
        .menu-item .icon {
            font-size: 2.5em;
            margin-bottom: 15px;
            display: block;
        }
        
        .status-bar {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            background: #28a745;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
        }
        
        .quick-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .quick-link {
            background: #4facfe;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .quick-link:hover {
            background: #3a8bfd;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 ModuStackClean</h1>
            <p>Sistema de Organización y Gestión de Archivos</p>
        </div>
        
        <div class="content">
            <div class="status-bar">
                <span class="status-indicator"></span>
                <strong>Sistema Operativo</strong> - Todas las funcionalidades disponibles
            </div>
            
            <div class="section">
                <h2>🌐 Interfaces Web</h2>
                <div class="menu-grid">
                    <a href="index.php" class="menu-item">
                        <span class="icon">🏠</span>
                        <h3>Sistema Principal</h3>
                        <p>Interfaz principal del sistema con todas las funcionalidades básicas</p>
                    </a>
                    
                    <a href="index_automatico.php" class="menu-item">
                        <span class="icon">🤖</span>
                        <h3>Sistema Automático</h3>
                        <p>Detección automática y gestión inteligente de archivos de descargas</p>
                    </a>
                    
                    <a href="index_simple.php" class="menu-item">
                        <span class="icon">📱</span>
                        <h3>Sistema Simplificado</h3>
                        <p>Versión simplificada para uso rápido y fácil</p>
                    </a>
                </div>
            </div>
            
            <div class="section">
                <h2>🛠️ Herramientas y Utilidades</h2>
                <div class="menu-grid">
                    <a href="funciones.php" class="menu-item">
                        <span class="icon">⚙️</span>
                        <h3>Funciones Principales</h3>
                        <p>Biblioteca completa de funciones del sistema</p>
                    </a>
                    
                    <a href="funciones_simple.php" class="menu-item">
                        <span class="icon">🔧</span>
                        <h3>Funciones Simplificadas</h3>
                        <p>Versión simplificada de las funciones principales</p>
                    </a>
                </div>
            </div>
            
            <div class="section">
                <h2>📚 Documentación y Recursos</h2>
                <div class="menu-grid">
                    <div class="menu-item">
                        <span class="icon">📖</span>
                        <h3>Documentación</h3>
                        <p>Guías de uso, instrucciones y documentación técnica</p>
                        <div class="quick-links">
                            <a href="../docs/ESTRUCTURA_ORGANIZADA.md" class="quick-link" target="_blank">Estructura</a>
                            <a href="../docs/README.md" class="quick-link" target="_blank">README</a>
                        </div>
                    </div>
                    
                    <div class="menu-item">
                        <span class="icon">🧪</span>
                        <h3>Pruebas y Verificación</h3>
                        <p>Herramientas de verificación y pruebas del sistema</p>
                        <div class="quick-links">
                            <a href="../utils/tools/verificar_flujo.py" class="quick-link">Verificador</a>
                            <a href="../tests/unit/" class="quick-link">Pruebas</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>ModuStackClean v1.0.0</strong> - Sistema completamente organizado y verificado</p>
            <p>📂 Estructura optimizada | 🔄 Flujo de trabajo verificado | 🚀 Listo para usar</p>
        </div>
    </div>
</body>
</html>
