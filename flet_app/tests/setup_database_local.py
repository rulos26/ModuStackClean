#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup de Base de Datos Local - ModuStackClean
Script para configurar y verificar la conexión a MySQL local (XAMPP)
"""

import sys
import os
import socket
import time

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database_config_local import DatabaseConfigLocal

def check_xampp_mysql():
    """Verificar si XAMPP MySQL está ejecutándose"""
    print("🔍 Verificando XAMPP MySQL...")
    
    try:
        # Probar conectividad al puerto 3306
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', 3306))
        sock.close()
        
        if result == 0:
            print("✅ XAMPP MySQL está ejecutándose")
            return True
        else:
            print("❌ XAMPP MySQL no está ejecutándose")
            print("💡 Inicia XAMPP y activa el servicio MySQL")
            return False
    except Exception as e:
        print(f"❌ Error verificando XAMPP: {e}")
        return False

def setup_local_database():
    """Configurar base de datos local"""
    print("\n🔧 Configurando base de datos local...")
    
    db_config = DatabaseConfigLocal()
    connection_info = db_config.get_connection_info()
    
    print(f"📋 Configuración local:")
    print(f"   Host: {connection_info['host']}")
    print(f"   Puerto: {connection_info['port']}")
    print(f"   Base de datos: {connection_info['database']}")
    print(f"   Usuario: {connection_info['user']}")
    print(f"   Timeout: {connection_info['timeout']} segundos")
    
    # Crear base de datos
    print("\n📋 Creando base de datos...")
    if db_config.create_database():
        print("✅ Base de datos creada/verificada")
    else:
        print("❌ Error creando base de datos")
        return False
    
    # Crear tablas
    print("\n📋 Creando tablas...")
    if db_config.create_tables():
        print("✅ Tablas creadas/verificadas")
    else:
        print("❌ Error creando tablas")
        return False
    
    return True

def test_local_connection():
    """Probar conexión a la base de datos local"""
    print("\n🔗 Probando conexión a la base de datos local...")
    
    db_config = DatabaseConfigLocal()
    
    if db_config.test_connection():
        print("✅ Conexión a la base de datos local exitosa")
        return True
    else:
        print("❌ Error en la conexión a la base de datos local")
        return False

def show_xampp_instructions():
    """Mostrar instrucciones para configurar XAMPP"""
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES PARA CONFIGURAR XAMPP")
    print("=" * 60)
    
    print("\n1️⃣ **Iniciar XAMPP:**")
    print("   - Abre el Panel de Control de XAMPP")
    print("   - Haz clic en 'Start' junto a MySQL")
    print("   - Verifica que el estado sea 'Running'")
    
    print("\n2️⃣ **Acceder a phpMyAdmin:**")
    print("   - Abre tu navegador")
    print("   - Ve a: http://localhost/phpmyadmin")
    print("   - Usuario: root (sin contraseña por defecto)")
    
    print("\n3️⃣ **Crear base de datos manualmente (opcional):**")
    print("   - En phpMyAdmin, haz clic en 'Nueva'")
    print("   - Nombre: modustackclean")
    print("   - Cotejamiento: utf8mb4_unicode_ci")
    print("   - Haz clic en 'Crear'")
    
    print("\n4️⃣ **Verificar configuración:**")
    print("   - El puerto 3306 debe estar disponible")
    print("   - El usuario 'root' debe tener permisos")
    print("   - No debe haber otros servicios MySQL ejecutándose")

def main():
    """Función principal de configuración local"""
    print("🚀 Setup de Base de Datos Local - ModuStackClean")
    print("=" * 60)
    
    # Verificar XAMPP MySQL
    if not check_xampp_mysql():
        print("\n❌ XAMPP MySQL no está ejecutándose")
        show_xampp_instructions()
        return False
    
    # Configurar base de datos local
    if not setup_local_database():
        print("\n❌ Error configurando la base de datos local")
        return False
    
    # Probar conexión
    if not test_local_connection():
        print("\n❌ Error en la conexión local")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ¡CONFIGURACIÓN LOCAL COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print("✅ XAMPP MySQL ejecutándose")
    print("✅ Base de datos local creada")
    print("✅ Tablas creadas/verificadas")
    print("✅ Conexión local establecida")
    print("\n🚀 La base de datos local está lista para usar!")
    print("\n💡 Para usar la base de datos remota, ejecuta:")
    print("   python setup_database.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ La configuración local no se completó correctamente")
        print("💡 Sigue las instrucciones de XAMPP arriba")
    sys.exit(0 if success else 1)
