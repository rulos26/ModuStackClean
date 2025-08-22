@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo 📱 INICIADOR MÓVIL - MODUSTACKCLEAN
echo ============================================================
echo.

echo 🚀 Iniciando ModuStackClean para dispositivos móviles...
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    pause
    exit /b 1
)

REM Verificar que Flet esté instalado
python -c "import flet" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando Flet...
    pip install flet
)

echo ✅ Verificaciones completadas
echo.

REM Obtener IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do (
    set IP=%%a
    goto :found_ip
)
:found_ip
set IP=%IP: =%

echo 🌐 Tu IP local: %IP%
echo 📱 URL para móvil: http://%IP%:8550
echo.

echo 📋 Instrucciones:
echo    1. La aplicación se abrirá en tu navegador
echo    2. Para acceder desde móvil, usa la URL de arriba
echo    3. Asegúrate de que tu móvil esté en la misma red WiFi
echo    4. Presiona Ctrl+C para detener el servidor
echo.

echo ⏳ Iniciando servidor web...
python -m flet run main.py --web-port 8550 --web-host 0.0.0.0

echo.
echo 🛑 Servidor detenido
pause
