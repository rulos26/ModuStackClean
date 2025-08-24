@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🚀 ModuStackClean - Instalación Flet
echo ========================================
echo.

echo 📦 Instalando dependencias...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error: No se pudieron instalar las dependencias
    echo 💡 Verifica que Python esté instalado y en el PATH
    pause
    exit /b 1
)

echo.
echo ✅ Dependencias instaladas correctamente
echo.
echo 🚀 Iniciando aplicación ModuStackClean...
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error: No se pudo iniciar la aplicación
    echo 💡 Verifica que todas las dependencias estén instaladas
    pause
    exit /b 1
)

echo.
echo ✅ Aplicación cerrada correctamente
pause
