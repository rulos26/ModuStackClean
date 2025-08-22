#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para desplegar ModuStackClean como aplicación web
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def deploy_web_app():
    """Desplegar aplicación como web"""
    
    print("🌐 Iniciando despliegue web de ModuStackClean...")
    
    # Verificar que estamos en el directorio correcto
    if not Path("main.py").exists():
        print("❌ Error: No se encontró main.py")
        return False
    
    print("📱 Configurando aplicación para dispositivos móviles...")
    
    # Comando para ejecutar Flet en modo web
    cmd = [
        "python", "-m", "flet", "run", "main.py",
        "--web-port", "8550",  # Puerto para web
        "--web-host", "0.0.0.0"  # Accesible desde cualquier IP
    ]
    
    try:
        print("🚀 Iniciando servidor web...")
        print(f"Comando: {' '.join(cmd)}")
        print("\n📋 Instrucciones:")
        print("1. La aplicación se abrirá en tu navegador")
        print("2. Para acceder desde móvil, usa la IP de tu PC")
        print("3. Ejemplo: http://192.168.1.100:8550")
        print("4. Presiona Ctrl+C para detener el servidor")
        
        # Ejecutar el servidor web
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

def get_local_ip():
    """Obtener IP local para acceso móvil"""
    import socket
    
    try:
        # Conectar a un servidor externo para obtener IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def create_mobile_config():
    """Crear configuración optimizada para móvil"""
    
    print("📱 Creando configuración para dispositivos móviles...")
    
    # Crear archivo de configuración móvil
    mobile_config = """
# Configuración para dispositivos móviles
MOBILE_OPTIMIZED = True
TOUCH_FRIENDLY = True
RESPONSIVE_DESIGN = True
WEB_PORT = 8550
WEB_HOST = "0.0.0.0"
"""
    
    with open("config/mobile_config.py", "w", encoding="utf-8") as f:
        f.write(mobile_config)
    
    print("✅ Configuración móvil creada")

def main():
    """Función principal"""
    print("=" * 60)
    print("📱 DESPLIEGUE MÓVIL - MODUSTACKCLEAN")
    print("=" * 60)
    
    # Obtener IP local
    local_ip = get_local_ip()
    
    print(f"🌐 Tu IP local: {local_ip}")
    print(f"📱 URL para móvil: http://{local_ip}:8550")
    
    # Crear configuración móvil
    create_mobile_config()
    
    # Desplegar aplicación web
    if deploy_web_app():
        print("\n🎉 ¡Aplicación web iniciada exitosamente!")
        print(f"\n📱 Para acceder desde móvil:")
        print(f"   URL: http://{local_ip}:8550")
        print(f"   Asegúrate de que tu móvil esté en la misma red WiFi")
    else:
        print("\n❌ Error durante el despliegue")

if __name__ == "__main__":
    main()
