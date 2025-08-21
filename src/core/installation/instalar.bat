@echo off
echo ========================================
echo   GESTOR DE ARCHIVOS DE DESCARGAS
echo ========================================
echo.

echo Verificando si Python esta instalado...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor instala Python desde: https://python.org
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo Python encontrado!
python --version
echo.

echo Ejecutando el Gestor de Archivos de Descargas...
echo.
python gestor_descargas.py

echo.
echo Programa terminado.
pause
