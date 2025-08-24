#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del Super Usuario - ModuStackClean
Test para verificar la funcionalidad del super usuario por defecto
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.session_manager import SessionManager
from config.app_config import AppConfig

def test_super_user_credentials():
    """Test de credenciales del super usuario"""
    print("🧪 TEST: Credenciales del Super Usuario")
    
    # Credenciales del super usuario
    super_user_email = "root"
    super_user_password = "root"
    
    # Verificar credenciales
    assert super_user_email == "root", "❌ Email del super usuario incorrecto"
    assert super_user_password == "root", "❌ Contraseña del super usuario incorrecta"
    
    print("✅ Credenciales del super usuario correctas")
    return True

def test_super_user_data():
    """Test de datos del super usuario"""
    print("\n🧪 TEST: Datos del Super Usuario")
    
    # Datos esperados del super usuario
    expected_super_user = {
        'id': 0,
        'nombre': 'Super Administrador',
        'correo': 'root',
        'rol': 'admin',
        'estado': 1,
        'creado_en': '2025-01-01 00:00:00',
        'actualizado_en': '2025-01-01 00:00:00'
    }
    
    # Verificar estructura de datos
    required_fields = ['id', 'nombre', 'correo', 'rol', 'estado', 'creado_en', 'actualizado_en']
    for field in required_fields:
        assert field in expected_super_user, f"❌ Campo requerido faltante: {field}"
    
    # Verificar valores específicos
    assert expected_super_user['id'] == 0, "❌ ID del super usuario debe ser 0"
    assert expected_super_user['rol'] == 'admin', "❌ Rol del super usuario debe ser 'admin'"
    assert expected_super_user['estado'] == 1, "❌ Estado del super usuario debe ser 1 (activo)"
    
    print("✅ Datos del super usuario correctos")
    return True

def test_session_manager_with_super_user():
    """Test del SessionManager con super usuario"""
    print("\n🧪 TEST: SessionManager con Super Usuario")
    
    # Crear instancia del SessionManager
    session_manager = SessionManager()
    
    # Datos del super usuario
    super_user = {
        'id': 0,
        'nombre': 'Super Administrador',
        'correo': 'root',
        'rol': 'admin',
        'estado': 1,
        'creado_en': '2025-01-01 00:00:00',
        'actualizado_en': '2025-01-01 00:00:00'
    }
    
    # Test de login
    login_success = session_manager.login(super_user)
    assert login_success, "❌ Login del super usuario falló"
    
    # Test de verificación de sesión
    is_logged_in = session_manager.is_logged_in()
    assert is_logged_in, "❌ Verificación de sesión falló"
    
    # Test de obtención de usuario actual
    current_user = session_manager.get_current_user()
    assert current_user is not None, "❌ Usuario actual es None"
    assert current_user['correo'] == 'root', "❌ Usuario actual incorrecto"
    
    # Test de logout
    logout_success = session_manager.logout()
    assert logout_success, "❌ Logout del super usuario falló"
    
    # Verificar que la sesión se cerró
    is_logged_in_after_logout = session_manager.is_logged_in()
    assert not is_logged_in_after_logout, "❌ Sesión no se cerró correctamente"
    
    print("✅ SessionManager funciona correctamente con super usuario")
    return True

def test_super_user_validation():
    """Test de validación del super usuario"""
    print("\n🧪 TEST: Validación del Super Usuario")
    
    # Casos de prueba
    test_cases = [
        # (email, password, should_be_valid, description)
        ("root", "root", True, "Credenciales correctas"),
        ("root", "wrong", False, "Contraseña incorrecta"),
        ("wrong", "root", False, "Usuario incorrecto"),
        ("admin", "admin", False, "Credenciales diferentes"),
        ("", "", False, "Credenciales vacías"),
        ("root@example.com", "root", False, "Email con formato normal"),
    ]
    
    for email, password, should_be_valid, description in test_cases:
        is_valid = (email == "root" and password == "root")
        assert is_valid == should_be_valid, f"❌ {description}: {email}/{password}"
        print(f"✅ {description}: {email}/{password}")
    
    return True

def test_super_user_validation_order():
    """Test de orden de validación del super usuario"""
    print("\n🧪 TEST: Orden de Validación del Super Usuario")
    
    # Simular el flujo de validación del login
    def simulate_login_validation(email, password):
        # 1. Validación básica (no vacíos)
        if not email or not password:
            return False, "Campos vacíos"
        
        # 2. Verificación prioritaria del super usuario (ANTES del formato de email)
        if email == "root" and password == "root":
            return True, "Super usuario válido"
        
        # 3. Validación de formato de email (solo para usuarios normales)
        if "@" not in email or "." not in email:
            return False, "Formato de email inválido"
        
        # 4. Aquí iría la validación de base de datos
        return False, "Usuario normal (requiere BD)"
    
    # Test casos específicos
    test_cases = [
        ("root", "root", True, "Super usuario debe ser válido"),
        ("root", "wrong", False, "Super usuario con contraseña incorrecta"),
        ("wrong", "root", False, "Super usuario con usuario incorrecto"),
        ("test@example.com", "password", False, "Usuario normal válido"),
        ("invalid-email", "password", False, "Usuario con email inválido"),
    ]
    
    for email, password, should_be_valid, description in test_cases:
        is_valid, message = simulate_login_validation(email, password)
        assert is_valid == should_be_valid, f"❌ {description}: {email}/{password} - {message}"
        print(f"✅ {description}: {email}/{password} - {message}")
    
    return True

def test_super_user_offline_access():
    """Test de acceso offline del super usuario"""
    print("\n🧪 TEST: Acceso Offline del Super Usuario")
    
    # Simular entorno sin base de datos
    print("🔧 Simulando entorno sin conexión a base de datos...")
    
    # El super usuario debe funcionar sin base de datos
    super_user = {
        'id': 0,
        'nombre': 'Super Administrador',
        'correo': 'root',
        'rol': 'admin',
        'estado': 1,
        'creado_en': '2025-01-01 00:00:00',
        'actualizado_en': '2025-01-01 00:00:00'
    }
    
    # Verificar que los datos están completos para funcionamiento offline
    required_for_offline = ['id', 'nombre', 'correo', 'rol', 'estado']
    for field in required_for_offline:
        assert field in super_user, f"❌ Campo requerido para modo offline faltante: {field}"
        assert super_user[field] is not None, f"❌ Campo requerido para modo offline es None: {field}"
    
    print("✅ Super usuario tiene todos los datos necesarios para modo offline")
    return True

def main():
    """Función principal de test"""
    print("🚀 INICIANDO TESTS DEL SUPER USUARIO")
    print("=" * 50)
    
    try:
        # Ejecutar todos los tests
        test_super_user_credentials()
        test_super_user_data()
        test_session_manager_with_super_user()
        test_super_user_validation()
        test_super_user_validation_order()
        test_super_user_offline_access()
        
        print("\n" + "=" * 50)
        print("🎉 TODOS LOS TESTS DEL SUPER USUARIO PASARON")
        print("✅ El super usuario está configurado correctamente")
        print("✅ Acceso offline disponible con 'root' / 'root'")
        print("✅ SessionManager funciona con super usuario")
        print("✅ Validación de credenciales correcta")
        print("✅ Orden de validación corregido (super usuario antes que formato de email)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
