#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup de Base de Datos - ModuStackClean
Script para configurar y verificar la conexión a la base de datos
"""

import sys
import os
import socket
import time

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database_config import DatabaseConfig

def check_internet_connection():
    """Verificar conexión a internet"""
    print("🌐 Verificando conexión a internet...")
    try:
        # Intentar conectar a Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ Conexión a internet disponible")
        return True
    except OSError:
        print("❌ No hay conexión a internet")
        return False

def check_mysql_server():
    """Verificar si el servidor MySQL está accesible"""
    print("\n🔍 Verificando servidor MySQL...")
    
    db_config = DatabaseConfig()
    connection_info = db_config.get_connection_info()
    
    print(f"📋 Configuración actual:")
    print(f"   Host: {connection_info['host']}")
    print(f"   Puerto: {connection_info['port']}")
    print(f"   Base de datos: {connection_info['database']}")
    print(f"   Usuario: {connection_info['user']}")
    print(f"   Timeout: {connection_info['timeout']} segundos")
    
    # Probar conectividad de red
    if db_config.test_network_connection():
        print("✅ Servidor MySQL accesible")
        return True
    else:
        print("❌ Servidor MySQL no accesible")
        return False

def test_database_connection():
    """Probar conexión completa a la base de datos"""
    print("\n🔗 Probando conexión a la base de datos...")
    
    db_config = DatabaseConfig()
    
    if db_config.test_connection():
        print("✅ Conexión a la base de datos exitosa")
        return True
    else:
        print("❌ Error en la conexión a la base de datos")
        return False

def create_database_tables():
    """Crear las tablas necesarias"""
    print("\n📋 Creando/verificando tablas...")
    
    db_config = DatabaseConfig()
    
    if db_config.create_tables():
        print("✅ Tablas creadas/verificadas correctamente")
        return True
    else:
        print("❌ Error creando tablas")
        return False

def show_troubleshooting_guide():
    """Mostrar guía de solución de problemas"""
    print("\n" + "=" * 60)
    print("🔧 GUÍA DE SOLUCIÓN DE PROBLEMAS")
    print("=" * 60)
    
    print("\n📋 Problemas comunes y soluciones:")
    
    print("\n1️⃣ **Error: Can't connect to MySQL server**")
    print("   Causas posibles:")
    print("   - El servidor MySQL no está ejecutándose")
    print("   - El puerto 3306 está bloqueado por firewall")
    print("   - El servidor no permite conexiones remotas")
    print("   Soluciones:")
    print("   - Verifica que el servidor esté activo")
    print("   - Configura el firewall para permitir puerto 3306")
    print("   - Verifica configuración de MySQL para conexiones remotas")
    
    print("\n2️⃣ **Error: Access denied**")
    print("   Causas posibles:")
    print("   - Credenciales incorrectas")
    print("   - Usuario sin permisos para la base de datos")
    print("   - Host no autorizado")
    print("   Soluciones:")
    print("   - Verifica usuario y contraseña")
    print("   - Asegúrate de que el usuario tenga permisos")
    print("   - Verifica que el host esté autorizado")
    
    print("\n3️⃣ **Error: Unknown database**")
    print("   Causas posibles:")
    print("   - La base de datos no existe")
    print("   - Nombre de base de datos incorrecto")
    print("   Soluciones:")
    print("   - Crea la base de datos si no existe")
    print("   - Verifica el nombre de la base de datos")
    
    print("\n4️⃣ **Error: Connection timeout**")
    print("   Causas posibles:")
    print("   - Red lenta o inestable")
    print("   - Servidor sobrecargado")
    print("   - Firewall bloqueando conexiones")
    print("   Soluciones:")
    print("   - Verifica tu conexión a internet")
    print("   - Aumenta el timeout de conexión")
    print("   - Verifica configuración de firewall")
    
    print("\n💡 **Comandos útiles para verificar:**")
    print("   - ping 82.197.82.130")
    print("   - telnet 82.197.82.130 3306")
    print("   - nmap -p 3306 82.197.82.130")

def main():
    """Función principal de configuración"""
    print("🚀 Setup de Base de Datos - ModuStackClean")
    print("=" * 60)
    
    # Verificar conexión a internet
    if not check_internet_connection():
        print("\n❌ No se puede continuar sin conexión a internet")
        show_troubleshooting_guide()
        return False
    
    # Verificar servidor MySQL
    if not check_mysql_server():
        print("\n❌ El servidor MySQL no está accesible")
        show_troubleshooting_guide()
        return False
    
    # Probar conexión a la base de datos
    if not test_database_connection():
        print("\n❌ No se pudo conectar a la base de datos")
        show_troubleshooting_guide()
        return False
    
    # Crear tablas
    if not create_database_tables():
        print("\n❌ Error creando las tablas")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print("✅ Conexión a internet verificada")
    print("✅ Servidor MySQL accesible")
    print("✅ Conexión a la base de datos establecida")
    print("✅ Tablas creadas/verificadas")
    print("\n🚀 La base de datos está lista para usar con la aplicación Flet!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ La configuración no se completó correctamente")
        print("💡 Revisa la guía de solución de problemas arriba")
    sys.exit(0 if success else 1)
