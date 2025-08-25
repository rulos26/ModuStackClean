#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de Base de Datos - ModuStackClean
Configuración para conexión a MySQL
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import socket

class DatabaseConfig:
    """Configuración de la base de datos MySQL"""
    
    def __init__(self):
        # Configuración de la base de datos
        self.DB_CONFIG = {
            'host': '82.197.82.130',
            'database': 'u494150416_modustackclean',
            'user': 'u494150416_rulos26',
            'password': '0382646740Ju*',
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True,
            'pool_name': 'modustackclean_pool',
            'pool_size': 5,
            'connect_timeout': 10,  # Timeout de conexión en segundos
            'use_unicode': True,
            'get_warnings': True
        }
        
        # Configuración de la API
        self.API_BASE_URL = "http://localhost:8000/api"
        self.API_ENDPOINTS = {
            'usuarios': '/usuarios',
            'login': '/auth/login',
            'register': '/auth/register',
            'test': '/test'
        }
    
    def test_network_connection(self):
        """Probar conectividad de red al servidor MySQL"""
        try:
            print(f"🔍 Probando conectividad a {self.DB_CONFIG['host']}:3306...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.DB_CONFIG['host'], 3306))
            sock.close()
            
            if result == 0:
                print("✅ Puerto 3306 está abierto y accesible")
                return True
            else:
                print("❌ Puerto 3306 no está accesible")
                return False
        except Exception as e:
            print(f"❌ Error probando conectividad: {e}")
            return False
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        try:
            print(f"🔗 Intentando conectar a MySQL en {self.DB_CONFIG['host']}...")
            connection = mysql.connector.connect(**self.DB_CONFIG)
            if connection.is_connected():
                print("✅ Conexión a MySQL establecida correctamente")
                return connection
        except Error as e:
            print(f"❌ Error conectando a MySQL: {e}")
            
            # Proporcionar sugerencias de solución
            if "Can't connect to MySQL server" in str(e):
                print("\n💡 Sugerencias para solucionar el problema:")
                print("1. Verifica que el servidor MySQL esté ejecutándose")
                print("2. Verifica que el puerto 3306 esté abierto")
                print("3. Verifica que el firewall permita conexiones al puerto 3306")
                print("4. Verifica que el host sea accesible desde tu red")
                print("5. Verifica las credenciales de acceso")
                print("6. Si es un servidor remoto, verifica que permita conexiones remotas")
            
            return None
    
    def test_connection(self):
        """Probar la conexión a la base de datos"""
        try:
            # Primero probar conectividad de red
            if not self.test_network_connection():
                print("⚠️ Problema de conectividad de red detectado")
                print("💡 Verifica tu conexión a internet y la accesibilidad del servidor")
                return False
            
            connection = self.get_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"✅ Conexión exitosa. Versión de MySQL: {version[0]}")
                
                # Verificar si la tabla usuarios existe
                cursor.execute("SHOW TABLES LIKE 'usuarios'")
                table_exists = cursor.fetchone()
                if table_exists:
                    print("✅ Tabla 'usuarios' encontrada")
                else:
                    print("⚠️ Tabla 'usuarios' no encontrada")
                
                cursor.close()
                connection.close()
                return True
            return False
        except Error as e:
            print(f"❌ Error en test de conexión: {e}")
            return False
    
    def create_tables(self):
        """Crear las tablas necesarias"""
        try:
            connection = self.get_connection()
            if connection:
                cursor = connection.cursor()
                
                # Crear tabla usuarios
                create_usuarios_table = """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(150) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    rol ENUM('admin', 'usuario') DEFAULT 'usuario',
                    estado TINYINT(1) DEFAULT 1,
                    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                """
                
                cursor.execute(create_usuarios_table)
                print("✅ Tabla 'usuarios' creada/verificada correctamente")
                
                connection.commit()
                cursor.close()
                connection.close()
                return True
            return False
        except Error as e:
            print(f"❌ Error creando tablas: {e}")
            return False
    
    def get_connection_info(self):
        """Obtener información de la configuración de conexión"""
        return {
            'host': self.DB_CONFIG['host'],
            'database': self.DB_CONFIG['database'],
            'user': self.DB_CONFIG['user'],
            'port': 3306,
            'timeout': self.DB_CONFIG['connect_timeout']
        }
