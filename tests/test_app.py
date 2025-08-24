#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para ModuStackClean Flet App
Verifica que todos los componentes funcionen correctamente
"""

import sys
import os

def test_imports():
    """Probar que todos los módulos se pueden importar"""
    print("🔍 Probando importaciones...")
    
    try:
        import flet as ft
        print("✅ Flet importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Flet: {e}")
        return False
    
    try:
        from config.app_config import AppConfig
        print("✅ AppConfig importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando AppConfig: {e}")
        return False
    
    try:
        from views.home_view import HomeView
        print("✅ HomeView importado correctamente")
    except Exception as e:
        print(f"❌ Error importando HomeView: {e}")
        return False
    
    try:
        from utils.ui_components import create_gradient_container, create_feature_card
        print("✅ UI Components importados correctamente")
    except ImportError as e:
        print(f"❌ Error importando UI Components: {e}")
        return False
    
    return True

def test_config():
    """Probar la configuración de la aplicación"""
    print("\n⚙️ Probando configuración...")
    
    try:
        from config.app_config import AppConfig
        config = AppConfig()
        
        # Verificar información básica
        assert config.APP_TITLE == "ModuStackClean", "Título incorrecto"
        assert config.APP_VERSION == "1.0", "Versión incorrecta"
        assert "RuloSoluciones" in config.COPYRIGHT, "Copyright incorrecto"
        
        print("✅ Configuración básica correcta")
        
        # Verificar características
        assert len(config.FEATURES) == 4, "Número incorrecto de características"
        print("✅ Características configuradas correctamente")
        
        # Verificar colores
        assert config.PRIMARY_COLOR.startswith("#"), "Color primario incorrecto"
        print("✅ Colores configurados correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_ui_components():
    """Probar los componentes de UI"""
    print("\n🎨 Probando componentes de UI...")
    
    try:
        from utils.ui_components import create_gradient_container, create_feature_card
        from config.app_config import AppConfig
        
        config = AppConfig()
        
        # Probar creación de contenedor con gradiente
        container = create_gradient_container("Test")
        assert container is not None, "Error creando contenedor con gradiente"
        print("✅ Contenedor con gradiente creado correctamente")
        
        # Probar creación de tarjeta de característica
        card = create_feature_card("📁", "Test", "Descripción", config)
        assert card is not None, "Error creando tarjeta de característica"
        print("✅ Tarjeta de característica creada correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en componentes de UI: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Pruebas de ModuStackClean Flet App")
    print("=" * 50)
    
    # Cambiar al directorio de la aplicación
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"📂 Directorio de trabajo: {os.getcwd()}")
    
    # Ejecutar pruebas
    tests = [
        test_imports,
        test_config,
        test_ui_components
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print("📋 RESULTADOS DE PRUEBAS")
    print("=" * 50)
    
    if passed == total:
        print(f"✅ Todas las pruebas pasaron ({passed}/{total})")
        print("🎉 La aplicación está lista para usar")
        print("\n💡 Para ejecutar la aplicación:")
        print("   python main.py")
        print("   o")
        print("   install.bat")
        return True
    else:
        print(f"❌ {total - passed} pruebas fallaron ({passed}/{total})")
        print("⚠️  Revisa los errores antes de ejecutar la aplicación")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
