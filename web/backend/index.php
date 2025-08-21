<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestor de Archivos de Descargas - Redirección Automática</title>
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
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
            text-align: center;
            max-width: 600px;
            margin: 20px;
        }
        
        .header {
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            color: #666;
        }
        
        .loading {
            margin: 30px 0;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #4facfe;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .option-card {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            text-decoration: none;
            color: #333;
            transition: all 0.3s ease;
        }
        
        .option-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-color: #4facfe;
        }
        
        .option-card h3 {
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        
        .option-card p {
            color: #666;
            font-size: 0.9em;
        }
        
        .icon {
            font-size: 2em;
            margin-bottom: 10px;
            display: block;
        }
        
        .auto-redirect {
            background: #e3f2fd;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        
        .auto-redirect p {
            color: #1976d2;
            font-weight: 500;
        }
        
        .countdown {
            font-size: 1.2em;
            font-weight: bold;
            color: #4facfe;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 Gestor de Archivos de Descargas</h1>
            <p>Selecciona tu interfaz preferida</p>
        </div>
        
        <div class="auto-redirect">
            <p>🔄 Redirección automática en <span class="countdown" id="countdown">5</span> segundos...</p>
        </div>
        
        <div class="loading">
            <div class="spinner"></div>
            <p>Detectando servidor y preparando interfaz...</p>
        </div>
        
        <div class="options">
            <a href="index_automatico.php" class="option-card">
                <span class="icon">🚀</span>
                <h3>Interfaz Automática</h3>
                <p>Detección automática de servidor y estado en tiempo real</p>
            </a>
            
            <a href="index_simple.php" class="option-card">
                <span class="icon">📋</span>
                <h3>Interfaz Simple</h3>
                <p>Interfaz web simplificada y funcional</p>
            </a>
            
            <a href="gestor_descargas.py" class="option-card">
                <span class="icon">🐍</span>
                <h3>Script Python</h3>
                <p>Ejecutar directamente el script de Python</p>
            </a>
        </div>
    </div>

    <script>
        // Contador regresivo
        let countdown = 5;
        const countdownElement = document.getElementById('countdown');
        
        const timer = setInterval(() => {
            countdown--;
            countdownElement.textContent = countdown;
            
            if (countdown <= 0) {
                clearInterval(timer);
                // Intentar redirigir automáticamente
                window.location.href = 'index_automatico.php';
            }
        }, 1000);
        
        // Detectar si hay servidor activo
        async function detectarServidor() {
            try {
                // Verificar XAMPP (puerto 80)
                const response = await fetch('test_web_simple.php', { 
                    method: 'GET',
                    mode: 'no-cors'
                });
                console.log('Servidor detectado en puerto 80');
                return true;
            } catch (e) {
                console.log('No se detectó servidor en puerto 80');
                return false;
            }
        }
        
        // Ejecutar detección al cargar
        document.addEventListener('DOMContentLoaded', function() {
            detectarServidor();
        });
    </script>
</body>
</html>
