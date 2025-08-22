@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo 🔧 EMPAQUETADOR DE MODUSTACKCLEAN
echo ============================================================
echo.

echo 🚀 Iniciando proceso de empaquetado...
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo Por favor instala Python y agrégalo al PATH del sistema
    pause
    exit /b 1
)

REM Verificar que PyInstaller esté instalado
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Error: No se pudo instalar PyInstaller
        pause
        exit /b 1
    )
)

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ❌ Error: No se encontró main.py
    echo Asegúrate de ejecutar este script desde el directorio flet_app/
    pause
    exit /b 1
)

echo ✅ Verificaciones completadas
echo.

REM Ejecutar el script de empaquetado
echo 📦 Ejecutando empaquetado...
python build_exe.py

echo.
echo ============================================================
echo 🎉 PROCESO COMPLETADO
echo ============================================================
echo.
echo 📁 El ejecutable se encuentra en la carpeta 'dist/'
echo 📄 Revisa 'dist/INFORMACION_EJECUTABLE.md' para más detalles
echo.
echo 💡 Para probar la aplicación:
echo    1. Ve a la carpeta 'dist/'
echo    2. Ejecuta 'ModuStackClean.exe'
echo    3. Prueba todas las funcionalidades
echo.
pause
