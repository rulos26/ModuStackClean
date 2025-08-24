#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de Usuario - ModuStackClean
Operaciones CRUD para la tabla usuarios
"""

import mysql.connector
from mysql.connector import Error
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class UsuarioModel:
    """Modelo para manejar operaciones CRUD de usuarios"""
    
    def __init__(self, db_config):
        self.db_config = db_config
    
    def _hash_password(self, password: str) -> str:
        """Encriptar contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        return self._hash_password(password) == hashed_password
    
    def create_usuario(self, nombre: str, correo: str, password: str, rol: str = 'usuario') -> Tuple[bool, str, Optional[int]]:
        """Crear un nuevo usuario (CREATE)"""
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return False, "Error de conexión a la base de datos", None
            
            cursor = connection.cursor()
            
            # Verificar si el correo ya existe
            cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
            if cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "El correo ya está registrado", None
            
            # Encriptar contraseña
            hashed_password = self._hash_password(password)
            
            # Insertar nuevo usuario
            insert_query = """
            INSERT INTO usuarios (nombre, correo, password, rol) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (nombre, correo, hashed_password, rol))
            
            # Obtener el ID del usuario creado
            user_id = cursor.lastrowid
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True, "Usuario creado exitosamente", user_id
            
        except Error as e:
            return False, f"Error creando usuario: {str(e)}", None
    
    def get_usuario_by_id(self, user_id: int) -> Tuple[bool, str, Optional[Dict]]:
        """Obtener usuario por ID (READ)"""
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return False, "Error de conexión a la base de datos", None
            
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT id, nombre, correo, rol, estado, creado_en, actualizado_en FROM usuarios WHERE id = %s", (user_id,))
            usuario = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if usuario:
                return True, "Usuario encontrado", usuario
            else:
                return False, "Usuario no encontrado", None
                
        except Error as e:
            return False, f"Error obteniendo usuario: {str(e)}", None
    
    def get_usuario_by_email(self, correo: str) -> Tuple[bool, str, Optional[Dict]]:
        """Obtener usuario por correo electrónico"""
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return False, "Error de conexión a la base de datos", None
            
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            usuario = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if usuario:
                return True, "Usuario encontrado", usuario
            else:
                return False, "Usuario no encontrado", None
                
        except Error as e:
            return False, f"Error obteniendo usuario: {str(e)}", None
    
    def get_all_usuarios(self) -> Tuple[bool, str, List[Dict]]:
        """Obtener todos los usuarios (READ)"""
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return False, "Error de conexión a la base de datos", []
            
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT id, nombre, correo, rol, estado, creado_en, actualizado_en FROM usuarios ORDER BY creado_en DESC")
            usuarios = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return True, f"Se encontraron {len(usuarios)} usuarios", usuarios
                
        except Error as e:
            return False, f"Error obteniendo usuarios: {str(e)}", []
    
    def update_usuario(self, user_id: int, nombre: str = None, correo: str = None, 
                      password: str = None, rol: str = None, estado: int = None) -> Tuple[bool, str]:
        """Actualizar usuario (UPDATE)"""
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return False, "Error de conexión a la base de datos"
            
            cursor = connection.cursor()
            
            # Verificar si el usuario existe
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "Usuario no encontrado"
            
            # Construir query de actualización dinámicamente
            update_fields = []
            values = []
            
            if nombre is not None:
                update_fields.append("nombre = %s")
                values.append(nombre)
            
            if correo is not None:
                # Verificar si el correo ya existe en otro usuario
                cursor.execute("SELECT id FROM usuarios WHERE correo = %s AND id != %s", (correo, user_id))
                if cursor.fetchone():
                    cursor.close()
                    connection.close()
                    return False, "El correo ya está en uso por otro usuario"
                update_fields.append("correo = %s")
                values.append(correo)
            
            if password is not None:
                hashed_password = self._hash_password(password)
                update_fields.append("password = %s")
                values.append(hashed_password)
            
            if rol is not None:
                update_fields.append("rol = %s")
                values.append(rol)
            
            if estado is not None:
                update_fields.append("estado = %s")
                values.append(estado)
            
            if not update_fields:
                cursor.close()
                connection.close()
                return False, "No se proporcionaron campos para actualizar"
            
            # Agregar el ID al final de los valores
            values.append(user_id)
            
            # Ejecutar actualización
            update_query = f"UPDATE usuarios SET {', '.join(update_fields)} WHERE id = %s"
            cursor.execute(update_query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True, "Usuario actualizado exitosamente"
            
        except Error as e:
            return False, f"Error actualizando usuario: {str(e)}"
    
    def delete_usuario(self, user_id: int) -> Tuple[bool, str]:
        """Eliminar usuario (DELETE)"""
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return False, "Error de conexión a la base de datos"
            
            cursor = connection.cursor()
            
            # Verificar si el usuario existe
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "Usuario no encontrado"
            
            # Eliminar usuario
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True, "Usuario eliminado exitosamente"
            
        except Error as e:
            return False, f"Error eliminando usuario: {str(e)}"
    
    def login_usuario(self, correo: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Autenticar usuario"""
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return False, "Error de conexión a la base de datos", None
            
            cursor = connection.cursor(dictionary=True)
            
            # Buscar usuario por correo
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND estado = 1", (correo,))
            usuario = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not usuario:
                return False, "Usuario no encontrado o inactivo", None
            
            # Verificar contraseña
            if not self._verify_password(password, usuario['password']):
                return False, "Contraseña incorrecta", None
            
            # Remover contraseña del resultado
            usuario.pop('password', None)
            
            return True, "Login exitoso", usuario
            
        except Error as e:
            return False, f"Error en login: {str(e)}", None
    
    def count_usuarios(self) -> Tuple[bool, str, int]:
        """Contar total de usuarios"""
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return False, "Error de conexión a la base de datos", 0
            
            cursor = connection.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            count = cursor.fetchone()[0]
            
            cursor.close()
            connection.close()
            
            return True, f"Total de usuarios: {count}", count
                
        except Error as e:
            return False, f"Error contando usuarios: {str(e)}", 0
