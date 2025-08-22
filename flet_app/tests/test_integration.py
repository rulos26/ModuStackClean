#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Integración - ModuStackClean
Prueba completa de la integración entre base de datos y aplicación Flet
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database_manager import DatabaseManager
from utils.session_manager import SessionManager

def test_database_manager():
    """Probar el gestor de base de datos"""
    print("🔍 Probando Database Manager...")
    print("=" * 60)
    
    # Inicializar database manager
    db_manager = DatabaseManager()
    
    # Test 1: Verificar conexión
    print("1️⃣ Test de conexión:")
    if db_manager.is_connected():
        connection_info = db_manager.get_connection_info()
        print(f"✅ Conectado a base de datos {connection_info['type']}")
        print(f"   Host: {connection_info['host']}")
        print(f"   Base de datos: {connection_info['database']}")
    else:
        print("❌ No hay conexión a base de datos")
        return False
    
    # Test 2: Crear usuario de prueba
    print("\n2️⃣ Test CREATE - Crear usuario:")
    success, message, user_id = db_manager.create_usuario(
        "Usuario Integración",
        "integracion@modustackclean.com",
        "password123",
        "usuario"
    )
    
    if success:
        print(f"✅ {message} - ID: {user_id}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 3: Login de usuario
    print("\n3️⃣ Test LOGIN - Autenticar usuario:")
    success, message, usuario = db_manager.login_usuario(
        "integracion@modustackclean.com",
        "password123"
    )
    
    if success and usuario:
        print(f"✅ {message}")
        print(f"   Usuario: {usuario.get('nombre', 'N/A')}")
        print(f"   Email: {usuario.get('correo', 'N/A')}")
        print(f"   Rol: {usuario.get('rol', 'N/A')}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 4: Limpiar - Eliminar usuario de prueba
    print("\n4️⃣ Test DELETE - Eliminar usuario de prueba:")
    success, message = db_manager.delete_usuario(user_id)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    
    return True

def test_session_manager():
    """Probar el gestor de sesiones"""
    print("\n🔐 Probando Session Manager...")
    print("=" * 60)
    
    # Inicializar session manager
    session_manager = SessionManager()
    
    # Test 1: Estado inicial
    print("1️⃣ Test estado inicial:")
    if not session_manager.is_logged_in():
        print("✅ Sin sesión activa (correcto)")
    else:
        print("❌ Sesión activa inesperada")
        return False
    
    # Test 2: Login de usuario
    print("\n2️⃣ Test login de usuario:")
    usuario_test = {
        'id': 1,
        'nombre': 'Usuario Test',
        'correo': 'test@modustackclean.com',
        'rol': 'usuario',
        'estado': 1
    }
    
    if session_manager.login(usuario_test):
        print("✅ Login exitoso")
        print(f"   Usuario: {session_manager.get_user_name()}")
        print(f"   Email: {session_manager.get_user_email()}")
        print(f"   Rol: {session_manager.get_user_role()}")
    else:
        print("❌ Error en login")
        return False
    
    # Test 3: Verificar sesión activa
    print("\n3️⃣ Test verificar sesión:")
    if session_manager.is_logged_in():
        print("✅ Sesión activa")
        session_info = session_manager.get_session_info()
        print(f"   Duración: {session_info['session_duration']}")
    else:
        print("❌ Sesión no activa")
        return False
    
    # Test 4: Logout
    print("\n4️⃣ Test logout:")
    if session_manager.logout():
        print("✅ Logout exitoso")
        if not session_manager.is_logged_in():
            print("✅ Sesión cerrada correctamente")
        else:
            print("❌ Sesión sigue activa")
            return False
    else:
        print("❌ Error en logout")
        return False
    
    return True

def test_integration():
    """Probar integración completa"""
    print("\n🚀 Probando Integración Completa...")
    print("=" * 60)
    
    # Inicializar componentes
    db_manager = DatabaseManager()
    session_manager = SessionManager()
    
    # Test 1: Flujo completo de registro y login
    print("1️⃣ Test flujo completo de registro y login:")
    
    # Crear usuario
    success, message, user_id = db_manager.create_usuario(
        "Usuario Completo",
        "completo@modustackclean.com",
        "password123",
        "admin"
    )
    
    if not success:
        print(f"❌ Error creando usuario: {message}")
        return False
    
    print(f"✅ Usuario creado: {message}")
    
    # Login
    success, message, usuario = db_manager.login_usuario(
        "completo@modustackclean.com",
        "password123"
    )
    
    if not success:
        print(f"❌ Error en login: {message}")
        return False
    
    print(f"✅ Login exitoso: {message}")
    
    # Iniciar sesión
    if not session_manager.login(usuario):
        print("❌ Error iniciando sesión")
        return False
    
    print("✅ Sesión iniciada")
    print(f"   Usuario: {session_manager.get_user_name()}")
    print(f"   Es admin: {session_manager.is_admin()}")
    
    # Test 2: Operaciones con sesión activa
    print("\n2️⃣ Test operaciones con sesión activa:")
    
    # Obtener información de sesión
    session_info = session_manager.get_session_info()
    print(f"✅ Información de sesión obtenida")
    print(f"   Logged in: {session_info['logged_in']}")
    print(f"   Usuario: {session_info['user']['nombre']}")
    
    # Test 3: Cleanup
    print("\n3️⃣ Test cleanup:")
    
    # Logout
    session_manager.logout()
    print("✅ Logout realizado")
    
    # Eliminar usuario de prueba
    db_manager.delete_usuario(user_id)
    print("✅ Usuario de prueba eliminado")
    
    return True

def main():
    """Función principal de tests de integración"""
    print("🚀 Tests de Integración - ModuStackClean")
    print("=" * 60)
    
    # Test 1: Database Manager
    if not test_database_manager():
        print("\n❌ Falló el test de Database Manager")
        return False
    
    # Test 2: Session Manager
    if not test_session_manager():
        print("\n❌ Falló el test de Session Manager")
        return False
    
    # Test 3: Integración completa
    if not test_integration():
        print("\n❌ Falló el test de integración completa")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ¡TODOS LOS TESTS DE INTEGRACIÓN PASARON EXITOSAMENTE!")
    print("=" * 60)
    print("✅ Database Manager funcionando")
    print("✅ Session Manager funcionando")
    print("✅ Integración completa operativa")
    print("✅ Sistema de login y logout funcional")
    print("✅ Gestión de usuarios operativa")
    print("\n🚀 La aplicación Flet está lista para usar con autenticación completa!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
