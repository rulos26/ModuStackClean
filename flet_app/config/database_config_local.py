#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de Base de Datos Local - ModuStackClean
Configuración para desarrollo con MySQL local
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import socket

class DatabaseConfigLocal:
    """Configuración de la base de datos MySQL local para desarrollo"""
    
    def __init__(self):
        # Configuración para MySQL local (XAMPP)
        self.DB_CONFIG = {
            'host': 'localhost',
            'database': 'modustackclean',
            'user': 'root',
            'password': '',  # Sin contraseña por defecto en XAMPP
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True,
            'pool_name': 'modustackclean_local_pool',
            'pool_size': 5,
            'connect_timeout': 10,
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
        """Probar conectividad de red al servidor MySQL local"""
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
                print("💡 Asegúrate de que XAMPP esté ejecutándose y MySQL esté activo")
                return False
        except Exception as e:
            print(f"❌ Error probando conectividad: {e}")
            return False
    
    def get_connection(self):
        """Obtener conexión a la base de datos local"""
        try:
            print(f"🔗 Intentando conectar a MySQL local en {self.DB_CONFIG['host']}...")
            connection = mysql.connector.connect(**self.DB_CONFIG)
            if connection.is_connected():
                print("✅ Conexión a MySQL local establecida correctamente")
                # Seleccionar la base de datos
                cursor = connection.cursor()
                cursor.execute("USE modustackclean")
                cursor.close()
                return connection
        except Error as e:
            print(f"❌ Error conectando a MySQL local: {e}")
            
            # Proporcionar sugerencias de solución para local
            if "Can't connect to MySQL server" in str(e):
                print("\n💡 Sugerencias para solucionar el problema:")
                print("1. Verifica que XAMPP esté ejecutándose")
                print("2. Verifica que el servicio MySQL esté activo en XAMPP")
                print("3. Verifica que el puerto 3306 esté disponible")
                print("4. Verifica que no haya otro MySQL ejecutándose")
                print("5. Reinicia el servicio MySQL en XAMPP")
            elif "Access denied" in str(e):
                print("\n💡 Sugerencias para solucionar el problema:")
                print("1. Verifica que el usuario 'root' no tenga contraseña")
                print("2. O configura la contraseña correcta en la configuración")
                print("3. Verifica los permisos del usuario en phpMyAdmin")
            elif "Unknown database" in str(e):
                print("\n💡 Sugerencias para solucionar el problema:")
                print("1. Crea la base de datos 'modustackclean' en phpMyAdmin")
                print("2. O ejecuta el script de creación de base de datos")
            
            return None
    
    def test_connection(self):
        """Probar la conexión a la base de datos local"""
        try:
            # Primero probar conectividad de red
            if not self.test_network_connection():
                print("⚠️ Problema de conectividad de red detectado")
                print("💡 Verifica que XAMPP esté ejecutándose")
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
    
    def create_database(self):
        """Crear la base de datos si no existe"""
        try:
            # Conectar sin especificar base de datos
            config_without_db = self.DB_CONFIG.copy()
            config_without_db.pop('database', None)
            
            connection = mysql.connector.connect(**config_without_db)
            if connection.is_connected():
                cursor = connection.cursor()
                
                # Crear base de datos si no existe
                cursor.execute("CREATE DATABASE IF NOT EXISTS modustackclean CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print("✅ Base de datos 'modustackclean' creada/verificada")
                
                connection.commit()
                cursor.close()
                connection.close()
                return True
            return False
        except Error as e:
            print(f"❌ Error creando base de datos: {e}")
            return False
    
    def create_tables(self):
        """Crear las tablas necesarias"""
        try:
            # Primero crear la base de datos si no existe
            if not self.create_database():
                return False
            
            # Luego conectar a la base de datos específica
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
