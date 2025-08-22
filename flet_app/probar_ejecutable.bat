@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo 🧪 PROBADOR DE EJECUTABLE MODUSTACKCLEAN
echo ============================================================
echo.

REM Verificar que el ejecutable existe
if not exist "dist\ModuStackClean.exe" (
    echo ❌ Error: No se encontró ModuStackClean.exe
    echo Asegúrate de haber ejecutado el empaquetado primero
    pause
    exit /b 1
)

echo ✅ Ejecutable encontrado: dist\ModuStackClean.exe
echo 📏 Tamaño: 
for %%A in ("dist\ModuStackClean.exe") do echo    %%~zA bytes (%%~zA:~0,-6%.%%~zA:~-6,3 MB)

echo.
echo 🚀 Iniciando prueba del ejecutable...
echo.

REM Ejecutar el ejecutable
echo 📋 Instrucciones de prueba:
echo    1. La aplicación debería abrirse en una nueva ventana
echo    2. Verifica que se conecte a la base de datos
echo    3. Prueba el registro de un nuevo usuario
echo    4. Prueba el inicio de sesión
echo    5. Prueba todas las funcionalidades
echo    6. Cierra la aplicación normalmente
echo.

echo ⏳ Ejecutando ModuStackClean.exe...
start "" "dist\ModuStackClean.exe"

echo.
echo ✅ Ejecutable iniciado correctamente
echo.
echo 📝 Notas importantes:
echo    - La aplicación se ejecuta en segundo plano
echo    - Verifica que Windows Defender no la bloquee
echo    - Si hay problemas, ejecuta como administrador
echo.
echo 🔍 Para monitorear el proceso:
echo    - Abre el Administrador de tareas
echo    - Busca "ModuStackClean.exe" en la lista
echo    - Verifica el uso de memoria y CPU
echo.

pause
