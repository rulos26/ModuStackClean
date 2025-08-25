#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Base de Datos Local - ModuStackClean
Script de prueba para verificar conexión y operaciones CRUD en MySQL local
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database_config_local import DatabaseConfigLocal
from models.usuario_model import UsuarioModel

def test_local_database_connection():
    """Probar conexión a la base de datos local"""
    print("🔍 Probando conexión a la base de datos local...")
    print("=" * 60)
    
    db_config = DatabaseConfigLocal()
    
    # Test 1: Conexión básica
    print("1️⃣ Test de conexión básica:")
    if db_config.test_connection():
        print("✅ Conexión exitosa")
    else:
        print("❌ Error en la conexión")
        return False
    
    # Test 2: Crear tablas
    print("\n2️⃣ Test de creación de tablas:")
    if db_config.create_tables():
        print("✅ Tablas creadas/verificadas correctamente")
    else:
        print("❌ Error creando tablas")
        return False
    
    return True

def test_local_crud_operations():
    """Probar operaciones CRUD en base de datos local"""
    print("\n🔧 Probando operaciones CRUD locales...")
    print("=" * 60)
    
    db_config = DatabaseConfigLocal()
    usuario_model = UsuarioModel(db_config)
    
    # Datos de prueba
    test_user = {
        'nombre': 'Usuario Local de Prueba',
        'correo': 'test.local@modustackclean.com',
        'password': 'password123',
        'rol': 'usuario'
    }
    
    # Test 1: CREATE - Crear usuario
    print("1️⃣ Test CREATE - Crear usuario:")
    success, message, user_id = usuario_model.create_usuario(
        test_user['nombre'], 
        test_user['correo'], 
        test_user['password'], 
        test_user['rol']
    )
    
    if success:
        print(f"✅ {message} - ID: {user_id}")
        test_user['id'] = user_id
    else:
        print(f"❌ {message}")
        return False
    
    # Test 2: READ - Obtener usuario por ID
    print("\n2️⃣ Test READ - Obtener usuario por ID:")
    success, message, usuario = usuario_model.get_usuario_by_id(user_id)
    
    if success:
        print(f"✅ {message}")
        print(f"   📋 Datos: {usuario}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 3: READ - Obtener usuario por email
    print("\n3️⃣ Test READ - Obtener usuario por email:")
    success, message, usuario = usuario_model.get_usuario_by_email(test_user['correo'])
    
    if success:
        print(f"✅ {message}")
        print(f"   📧 Email encontrado: {usuario['correo']}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 4: UPDATE - Actualizar usuario
    print("\n4️⃣ Test UPDATE - Actualizar usuario:")
    success, message = usuario_model.update_usuario(
        user_id, 
        nombre="Usuario Local Actualizado",
        correo="actualizado.local@modustackclean.com"
    )
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return False
    
    # Verificar actualización
    success, message, usuario_actualizado = usuario_model.get_usuario_by_id(user_id)
    if success:
        print(f"   📋 Datos actualizados: {usuario_actualizado}")
    
    # Test 5: READ - Obtener todos los usuarios
    print("\n5️⃣ Test READ - Obtener todos los usuarios:")
    success, message, usuarios = usuario_model.get_all_usuarios()
    
    if success:
        print(f"✅ {message}")
        print(f"   👥 Total de usuarios: {len(usuarios)}")
        for i, user in enumerate(usuarios[:3], 1):  # Mostrar solo los primeros 3
            print(f"   {i}. {user['nombre']} ({user['correo']})")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 6: Login - Autenticar usuario
    print("\n6️⃣ Test LOGIN - Autenticar usuario:")
    success, message, usuario_login = usuario_model.login_usuario(
        "actualizado.local@modustackclean.com", 
        "password123"
    )
    
    if success:
        print(f"✅ {message}")
        print(f"   👤 Usuario autenticado: {usuario_login['nombre']}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 7: Contar usuarios
    print("\n7️⃣ Test COUNT - Contar usuarios:")
    success, message, count = usuario_model.count_usuarios()
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return False
    
    # Test 8: DELETE - Eliminar usuario de prueba
    print("\n8️⃣ Test DELETE - Eliminar usuario de prueba:")
    success, message = usuario_model.delete_usuario(user_id)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return False
    
    # Verificar eliminación
    success, message, usuario_eliminado = usuario_model.get_usuario_by_id(user_id)
    if not success:
        print(f"✅ Usuario eliminado correctamente (no encontrado)")
    
    return True

def test_local_error_handling():
    """Probar manejo de errores en base de datos local"""
    print("\n⚠️ Probando manejo de errores locales...")
    print("=" * 60)
    
    db_config = DatabaseConfigLocal()
    usuario_model = UsuarioModel(db_config)
    
    # Test 1: Crear usuario con correo duplicado
    print("1️⃣ Test - Correo duplicado:")
    
    # Crear primer usuario
    success1, message1, user_id1 = usuario_model.create_usuario(
        "Usuario Local 1", 
        "duplicado.local@test.com", 
        "password123"
    )
    
    if success1:
        print(f"✅ Usuario 1 creado: {message1}")
        
        # Intentar crear segundo usuario con mismo correo
        success2, message2, user_id2 = usuario_model.create_usuario(
            "Usuario Local 2", 
            "duplicado.local@test.com", 
            "password456"
        )
        
        if not success2:
            print(f"✅ Error manejado correctamente: {message2}")
        else:
            print(f"❌ Error: Se permitió correo duplicado")
        
        # Limpiar - eliminar usuario de prueba
        usuario_model.delete_usuario(user_id1)
    
    # Test 2: Obtener usuario inexistente
    print("\n2️⃣ Test - Usuario inexistente:")
    success, message, usuario = usuario_model.get_usuario_by_id(99999)
    
    if not success:
        print(f"✅ Error manejado correctamente: {message}")
    else:
        print(f"❌ Error: Se encontró usuario inexistente")
    
    # Test 3: Login con credenciales incorrectas
    print("\n3️⃣ Test - Login con credenciales incorrectas:")
    success, message, usuario = usuario_model.login_usuario(
        "inexistente.local@test.com", 
        "password123"
    )
    
    if not success:
        print(f"✅ Error manejado correctamente: {message}")
    else:
        print(f"❌ Error: Login exitoso con credenciales incorrectas")
    
    return True

def main():
    """Función principal de pruebas locales"""
    print("🚀 Test de Base de Datos Local - ModuStackClean")
    print("=" * 60)
    
    # Test de conexión local
    if not test_local_database_connection():
        print("\n❌ Falló el test de conexión local. Verifica XAMPP.")
        return False
    
    # Test de operaciones CRUD locales
    if not test_local_crud_operations():
        print("\n❌ Falló el test de operaciones CRUD locales.")
        return False
    
    # Test de manejo de errores locales
    if not test_local_error_handling():
        print("\n❌ Falló el test de manejo de errores locales.")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ¡TODOS LOS TESTS LOCALES PASARON EXITOSAMENTE!")
    print("=" * 60)
    print("✅ Conexión a MySQL local establecida")
    print("✅ Tabla 'usuarios' creada/verificada")
    print("✅ Operaciones CRUD funcionando")
    print("✅ Manejo de errores correcto")
    print("✅ Sistema de autenticación operativo")
    print("\n🚀 La base de datos local está lista para usar con la aplicación Flet!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
