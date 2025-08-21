#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Automático para Gestor de Archivos de Descargas
Detecta y inicia automáticamente el servidor PHP si es necesario
"""

import os
import sys
import time
import socket
import subprocess
import threading
import webbrowser
from pathlib import Path

class ServidorAutomatico:
    def __init__(self):
        self.puerto_xampp = 80
        self.puerto_alternativo = 8000
        self.directorio_actual = Path(__file__).parent
        self.archivo_principal = "index_simple.php"
        
    def verificar_puerto(self, puerto):
        """Verifica si un puerto está en uso"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                resultado = s.connect_ex(('localhost', puerto))
                return resultado == 0
        except:
            return False
    
    def verificar_xampp(self):
        """Verifica si XAMPP está ejecutándose"""
        return self.verificar_puerto(self.puerto_xampp)
    
    def verificar_servidor_php(self):
        """Verifica si hay un servidor PHP ejecutándose"""
        return self.verificar_puerto(self.puerto_alternativo)
    
    def iniciar_xampp(self):
        """Intenta iniciar XAMPP"""
        print("🔄 Intentando iniciar XAMPP...")
        
        # Rutas comunes de XAMPP
        rutas_xampp = [
            r"C:\xampp\xampp-control.exe",
            r"C:\xampp\apache_start.bat",
            r"C:\xampp\start_apache.bat"
        ]
        
        for ruta in rutas_xampp:
            if os.path.exists(ruta):
                try:
                    if ruta.endswith('.exe'):
                        subprocess.Popen([ruta], shell=True)
                    else:
                        subprocess.Popen([ruta], shell=True)
                    print(f"✅ XAMPP iniciado desde: {ruta}")
                    return True
                except Exception as e:
                    print(f"❌ Error iniciando XAMPP desde {ruta}: {e}")
        
        print("❌ No se pudo iniciar XAMPP automáticamente")
        return False
    
    def iniciar_servidor_php(self):
        """Inicia un servidor PHP en el puerto alternativo"""
        print(f"🔄 Iniciando servidor PHP en puerto {self.puerto_alternativo}...")
        
        try:
            # Cambiar al directorio actual
            os.chdir(self.directorio_actual)
            
            # Comando para iniciar servidor PHP
            comando = f'php -S localhost:{self.puerto_alternativo}'
            
            # Iniciar en segundo plano
            proceso = subprocess.Popen(
                comando,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Esperar un momento para que inicie
            time.sleep(2)
            
            if proceso.poll() is None:
                print(f"✅ Servidor PHP iniciado en puerto {self.puerto_alternativo}")
                return True
            else:
                print("❌ Error iniciando servidor PHP")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando servidor PHP: {e}")
            return False
    
    def abrir_navegador(self, puerto):
        """Abre el navegador con la interfaz web"""
        url = f"http://localhost:{puerto}/{self.archivo_principal}"
        print(f"🌐 Abriendo navegador: {url}")
        
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"❌ Error abriendo navegador: {e}")
            return False
    
    def mostrar_estado(self):
        """Muestra el estado actual de los servidores"""
        print("\n" + "="*50)
        print("🔍 VERIFICANDO ESTADO DE SERVIDORES")
        print("="*50)
        
        xampp_activo = self.verificar_xampp()
        php_activo = self.verificar_servidor_php()
        
        print(f"📊 XAMPP (Puerto {self.puerto_xampp}): {'✅ Activo' if xampp_activo else '❌ Inactivo'}")
        print(f"📊 Servidor PHP (Puerto {self.puerto_alternativo}): {'✅ Activo' if php_activo else '❌ Inactivo'}")
        
        return xampp_activo, php_activo
    
    def ejecutar(self):
        """Ejecuta la lógica principal del servidor automático"""
        print("🚀 INICIANDO SERVIDOR AUTOMÁTICO")
        print("="*50)
        
        # Verificar estado actual
        xampp_activo, php_activo = self.mostrar_estado()
        
        # Si XAMPP está activo, usar puerto 80
        if xampp_activo:
            print("\n✅ XAMPP está activo. Usando puerto 80...")
            self.abrir_navegador(80)
            return True
        
        # Si no hay XAMPP pero hay servidor PHP, usar puerto alternativo
        elif php_activo:
            print(f"\n✅ Servidor PHP está activo. Usando puerto {self.puerto_alternativo}...")
            self.abrir_navegador(self.puerto_alternativo)
            return True
        
        # Si no hay ningún servidor, intentar iniciar uno
        else:
            print("\n❌ No hay servidores activos. Intentando iniciar...")
            
            # Primero intentar XAMPP
            if self.iniciar_xampp():
                print("⏳ Esperando que XAMPP inicie...")
                for i in range(10):  # Esperar hasta 10 segundos
                    time.sleep(1)
                    if self.verificar_xampp():
                        print("✅ XAMPP iniciado correctamente")
                        self.abrir_navegador(80)
                        return True
                
                print("⚠️ XAMPP no respondió en el tiempo esperado")
            
            # Si XAMPP falla, intentar servidor PHP
            print("🔄 Intentando servidor PHP alternativo...")
            if self.iniciar_servidor_php():
                time.sleep(2)
                if self.verificar_servidor_php():
                    self.abrir_navegador(self.puerto_alternativo)
                    return True
            
            print("❌ No se pudo iniciar ningún servidor")
            return False
    
    def modo_monitoreo(self):
        """Modo que monitorea continuamente el servidor"""
        print("👁️ MODO MONITOREO ACTIVO")
        print("Presiona Ctrl+C para salir")
        
        try:
            while True:
                xampp_activo, php_activo = self.mostrar_estado()
                
                if not xampp_activo and not php_activo:
                    print("⚠️ No hay servidores activos. Reiniciando...")
                    self.ejecutar()
                
                time.sleep(30)  # Verificar cada 30 segundos
                
        except KeyboardInterrupt:
            print("\n👋 Monitoreo detenido")

def main():
    servidor = ServidorAutomatico()
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "monitor":
            servidor.modo_monitoreo()
        elif comando == "status":
            servidor.mostrar_estado()
        elif comando == "xampp":
            if servidor.iniciar_xampp():
                print("✅ XAMPP iniciado")
            else:
                print("❌ Error iniciando XAMPP")
        elif comando == "php":
            if servidor.iniciar_servidor_php():
                print("✅ Servidor PHP iniciado")
            else:
                print("❌ Error iniciando servidor PHP")
        else:
            print("Comandos disponibles:")
            print("  python servidor_automatico.py          - Inicio automático")
            print("  python servidor_automatico.py monitor  - Modo monitoreo")
            print("  python servidor_automatico.py status   - Ver estado")
            print("  python servidor_automatico.py xampp    - Iniciar XAMPP")
            print("  python servidor_automatico.py php      - Iniciar servidor PHP")
    else:
        servidor.ejecutar()

if __name__ == "__main__":
    main()
