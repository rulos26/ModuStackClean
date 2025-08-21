@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🚀 ModuStackClean - Inicio Rápido
echo ========================================
echo.

echo 📂 Verificando estructura del sistema...
python utils\tools\verificar_flujo.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error: El sistema no está correctamente configurado
    echo 💡 Revisa la documentación en docs/ESTRUCTURA_ORGANIZADA.md
    pause
    exit /b 1
)

echo.
echo ✅ Sistema verificado correctamente
echo.
echo 🌐 Para acceder al sistema web:
echo    http://localhost/ModuStackClean/
echo.
echo 🐍 Para ejecutar scripts Python:
echo    cd python\scripts\
echo    python servidor_automatico.py
echo.
echo 📚 Documentación disponible en:
echo    docs/ESTRUCTURA_ORGANIZADA.md
echo.
echo 🛠️  Herramientas de verificación:
echo    python utils\tools\verificar_flujo.py
echo.
echo ========================================
echo    ¡Sistema listo para usar!
echo ========================================
echo.
pause
