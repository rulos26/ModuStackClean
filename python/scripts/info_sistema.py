#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Información del Sistema - Gestor de Descargas
Script para obtener información detallada del hardware y software del sistema
"""

import os
import sys
import platform
import psutil
import subprocess
import json
import datetime
from pathlib import Path

class InfoSistema:
    def __init__(self):
        self.info = {}
        
    def obtener_info_completa(self):
        """Obtiene toda la información del sistema"""
        self.info = {
            'sistema_operativo': self.obtener_info_so(),
            'hardware': self.obtener_info_hardware(),
            'memoria': self.obtener_info_memoria(),
            'disco': self.obtener_info_disco(),
            'red': self.obtener_info_red(),
            'procesos': self.obtener_info_procesos(),
            'python': self.obtener_info_python(),
            'tiempo': self.obtener_info_tiempo(),
            'usuarios': self.obtener_info_usuarios()
        }
        return self.info
    
    def obtener_info_so(self):
        """Información del sistema operativo"""
        return {
            'nombre': platform.system(),
            'version': platform.version(),
            'release': platform.release(),
            'arquitectura': platform.architecture()[0],
            'maquina': platform.machine(),
            'procesador': platform.processor(),
            'hostname': platform.node(),
            'plataforma': platform.platform()
        }
    
    def obtener_info_hardware(self):
        """Información del hardware"""
        hardware = {}
        
        # CPU
        try:
            cpu_info = {
                'nucleos_fisicos': psutil.cpu_count(logical=False),
                'nucleos_logicos': psutil.cpu_count(logical=True),
                'frecuencia_actual': psutil.cpu_freq().current if psutil.cpu_freq() else None,
                'frecuencia_max': psutil.cpu_freq().max if psutil.cpu_freq() else None,
                'porcentaje_uso': psutil.cpu_percent(interval=1),
                'porcentaje_por_nucleo': psutil.cpu_percent(interval=1, percpu=True)
            }
            
            # Información adicional de CPU según el sistema operativo
            if platform.system() == "Windows":
                cpu_info.update(self.obtener_info_cpu_windows())
            elif platform.system() == "Linux":
                cpu_info.update(self.obtener_info_cpu_linux())
            elif platform.system() == "Darwin":  # macOS
                cpu_info.update(self.obtener_info_cpu_macos())
                
            hardware['cpu'] = cpu_info
        except Exception as e:
            hardware['cpu'] = {'error': str(e)}
        
        # GPU
        try:
            hardware['gpu'] = self.obtener_info_gpu()
        except Exception as e:
            hardware['gpu'] = [{'error': str(e)}]
        
        return hardware
    
    def obtener_info_cpu_windows(self):
        """Información específica de CPU en Windows"""
        try:
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'name,numberofcores,numberoflogicalprocessors', '/format:csv'],
                capture_output=True, text=True, shell=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    data = lines[1].split(',')
                    if len(data) >= 4:
                        return {
                            'nombre': data[2].strip(),
                            'nucleos_fisicos': int(data[3].strip()),
                            'nucleos_logicos': int(data[4].strip())
                        }
        except Exception:
            pass
        return {}
    
    def obtener_info_cpu_linux(self):
        """Información específica de CPU en Linux"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            
            # Buscar modelo de CPU
            for line in cpuinfo.split('\n'):
                if line.startswith('model name'):
                    return {'nombre': line.split(':')[1].strip()}
        except Exception:
            pass
        return {}
    
    def obtener_info_cpu_macos(self):
        """Información específica de CPU en macOS"""
        try:
            result = subprocess.run(
                ['sysctl', '-n', 'machdep.cpu.brand_string'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return {'nombre': result.stdout.strip()}
        except Exception:
            pass
        return {}
    
    def obtener_info_gpu(self):
        """Información de tarjetas gráficas"""
        gpus = []
        
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                ['wmic', 'path', 'win32_VideoController', 'get', 'name,adapterram', '/format:csv'],
                capture_output=True, text=True, shell=True
            )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[1:]:
                        if line.strip():
                            data = line.split(',')
                            if len(data) >= 3:
                                gpu_info = {
                                    'nombre': data[2].strip(),
                                    'memoria': self.formatear_tamaño(int(data[3].strip())) if data[3].strip().isdigit() else 'Desconocida'
                                }
                                gpus.append(gpu_info)
            except Exception:
                pass
                
        elif platform.system() == "Linux":
            try:
                result = subprocess.run(
                    ['lspci', '|', 'grep', '-i', 'vga'],
                    capture_output=True, text=True, shell=True
                )
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            gpus.append({'nombre': line.strip()})
            except Exception:
                pass
                
        elif platform.system() == "Darwin":  # macOS
            try:
                result = subprocess.run(
                    ['system_profiler', 'SPDisplaysDataType'],
                capture_output=True, text=True
            )
                if result.returncode == 0:
                    # Parsear la salida de system_profiler
                    for line in result.stdout.split('\n'):
                        if 'Chipset Model:' in line:
                            gpu_name = line.split(':')[1].strip()
                            gpus.append({'nombre': gpu_name})
            except Exception:
                pass
        
        return gpus if gpus else [{'nombre': 'No detectada'}]
    
    def obtener_info_memoria(self):
        """Información de memoria RAM"""
        try:
            memoria = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total': self.formatear_tamaño(memoria.total),
                'disponible': self.formatear_tamaño(memoria.available),
                'usada': self.formatear_tamaño(memoria.used),
                'porcentaje_uso': memoria.percent,
                'swap_total': self.formatear_tamaño(swap.total),
                'swap_usado': self.formatear_tamaño(swap.used),
                'swap_porcentaje': swap.percent
            }
        except Exception as e:
            return {'error': str(e)}
    
    def obtener_info_disco(self):
        """Información de discos"""
        discos = []
        
        try:
            for particion in psutil.disk_partitions():
                try:
                    uso = psutil.disk_usage(particion.mountpoint)
                    disco_info = {
                        'dispositivo': particion.device,
                        'punto_montaje': particion.mountpoint,
                        'sistema_archivos': particion.fstype,
                        'total': self.formatear_tamaño(uso.total),
                        'usado': self.formatear_tamaño(uso.used),
                        'libre': self.formatear_tamaño(uso.free),
                        'porcentaje_uso': uso.percent
                    }
                    discos.append(disco_info)
                except Exception:
                    continue
        except Exception as e:
            discos = [{'error': str(e)}]
        
        return discos
    
    def obtener_info_red(self):
        """Información de red"""
        try:
            # Interfaces de red
            interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == psutil.AF_INET:  # IPv4
                        interfaces[interface] = {
                            'ip': addr.address,
                            'mascara': addr.netmask,
                            'broadcast': addr.broadcast
                        }
                        break
            
            # Estadísticas de red
            net_io = psutil.net_io_counters()
            
            return {
                'interfaces': interfaces,
                'bytes_enviados': self.formatear_tamaño(net_io.bytes_sent),
                'bytes_recibidos': self.formatear_tamaño(net_io.bytes_recv),
                'paquetes_enviados': net_io.packets_sent,
                'paquetes_recibidos': net_io.packets_recv
            }
        except Exception as e:
            return {'error': str(e)}
    
    def obtener_info_procesos(self):
        """Información de procesos"""
        try:
            procesos = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                        procesos.append({
                        'pid': proc.info['pid'],
                        'nombre': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Ordenar por uso de CPU y tomar los top 10
            procesos.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return procesos[:10]
        except Exception as e:
            return {'error': str(e)}
    
    def obtener_info_python(self):
        """Información de Python"""
        return {
            'version': sys.version,
            'version_info': {
                'major': sys.version_info.major,
                'minor': sys.version_info.minor,
                'micro': sys.version_info.micro
            },
            'ejecutable': sys.executable,
            'plataforma': sys.platform,
            'modulos_cargados': list(sys.modules.keys())
        }
    
    def obtener_info_tiempo(self):
        """Información de tiempo"""
        try:
            # Uptime del sistema
            uptime_seconds = time.time() - psutil.boot_time()
            uptime = str(datetime.timedelta(seconds=int(uptime_seconds)))
            
            return {
                'fecha_actual': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'zona_horaria': datetime.datetime.now().astimezone().tzname(),
                'uptime_sistema': uptime,
                'timestamp': time.time()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def obtener_info_usuarios(self):
        """Información de usuarios"""
        try:
            usuarios = []
            for user in psutil.users():
                usuarios.append({
                    'nombre': user.name,
                    'terminal': user.terminal,
                    'host': user.host,
                    'inicio_sesion': datetime.datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S')
                })
            return usuarios
        except Exception as e:
            return {'error': str(e)}
    
    def formatear_tamaño(self, bytes):
        """Formatea bytes en formato legible"""
        for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unidad}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
    
    def generar_reporte_texto(self):
        """Genera un reporte en formato texto"""
        if not self.info:
            self.obtener_info_completa()
        
        reporte = []
        reporte.append("=" * 60)
        reporte.append("INFORMACIÓN DEL SISTEMA - GESTOR DE DESCARGAS")
        reporte.append("=" * 60)
        reporte.append("")
        
        # Sistema Operativo
        reporte.append("SISTEMA OPERATIVO:")
        reporte.append("-" * 20)
        so = self.info['sistema_operativo']
        reporte.append(f"Nombre: {so['nombre']}")
        reporte.append(f"Versión: {so['version']}")
        reporte.append(f"Release: {so['release']}")
        reporte.append(f"Arquitectura: {so['arquitectura']}")
        reporte.append(f"Hostname: {so['hostname']}")
        reporte.append("")
        
        # Hardware
        reporte.append("HARDWARE:")
        reporte.append("-" * 20)
        hw = self.info['hardware']
        
        if 'cpu' in hw and 'error' not in hw['cpu']:
            cpu = hw['cpu']
            reporte.append(f"CPU: {cpu.get('nombre', 'Desconocido')}")
            reporte.append(f"Núcleos físicos: {cpu.get('nucleos_fisicos', 'N/A')}")
            reporte.append(f"Núcleos lógicos: {cpu.get('nucleos_logicos', 'N/A')}")
            if cpu.get('frecuencia_actual'):
                reporte.append(f"Frecuencia: {cpu['frecuencia_actual']:.2f} MHz")
            reporte.append(f"Uso actual: {cpu.get('porcentaje_uso', 0):.1f}%")
        
        if 'gpu' in hw:
            reporte.append("GPU:")
            for gpu in hw['gpu']:
                reporte.append(f"  - {gpu.get('nombre', 'Desconocida')}")
                if 'memoria' in gpu:
                    reporte.append(f"    Memoria: {gpu['memoria']}")
        reporte.append("")
        
        # Memoria
        reporte.append("MEMORIA:")
        reporte.append("-" * 20)
        mem = self.info['memoria']
        if 'error' not in mem:
            reporte.append(f"Total: {mem['total']}")
            reporte.append(f"Usada: {mem['usada']} ({mem['porcentaje_uso']:.1f}%)")
            reporte.append(f"Disponible: {mem['disponible']}")
            reporte.append(f"Swap: {mem['swap_usado']} / {mem['swap_total']}")
        reporte.append("")
        
        # Disco
        reporte.append("ALMACENAMIENTO:")
        reporte.append("-" * 20)
        for disco in self.info['disco']:
            if 'error' not in disco:
                reporte.append(f"Dispositivo: {disco['dispositivo']}")
                reporte.append(f"Punto de montaje: {disco['punto_montaje']}")
                reporte.append(f"Total: {disco['total']}")
                reporte.append(f"Usado: {disco['usado']} ({disco['porcentaje_uso']:.1f}%)")
                reporte.append(f"Libre: {disco['libre']}")
                reporte.append("")
        
        # Red
        reporte.append("RED:")
        reporte.append("-" * 20)
        red = self.info['red']
        if 'error' not in red:
            for interface, info in red['interfaces'].items():
                reporte.append(f"Interfaz: {interface}")
                reporte.append(f"  IP: {info['ip']}")
                reporte.append(f"  Máscara: {info['mascara']}")
            reporte.append(f"Bytes enviados: {red['bytes_enviados']}")
            reporte.append(f"Bytes recibidos: {red['bytes_recibidos']}")
        reporte.append("")
        
        # Python
        reporte.append("PYTHON:")
        reporte.append("-" * 20)
        py = self.info['python']
        reporte.append(f"Versión: {py['version']}")
        if 'ejecutable' in py:
            reporte.append(f"Ejecutable: {py['ejecutable']}")
        reporte.append(f"Plataforma: {py['plataforma']}")
        reporte.append("")
        
        # Tiempo
        reporte.append("TIEMPO:")
        reporte.append("-" * 20)
        tiempo = self.info['tiempo']
        if 'error' not in tiempo:
            reporte.append(f"Fecha actual: {tiempo['fecha_actual']}")
            reporte.append(f"Zona horaria: {tiempo['zona_horaria']}")
            reporte.append(f"Uptime del sistema: {tiempo['uptime_sistema']}")
        reporte.append("")
        
        # Usuarios
        reporte.append("USUARIOS CONECTADOS:")
        reporte.append("-" * 20)
        for usuario in self.info['usuarios']:
            if 'error' not in usuario:
                reporte.append(f"Usuario: {usuario['nombre']}")
                reporte.append(f"  Terminal: {usuario['terminal']}")
                reporte.append(f"  Host: {usuario['host']}")
                reporte.append(f"  Inicio de sesión: {usuario['inicio_sesion']}")
        reporte.append("")
        
        # Procesos
        reporte.append("PROCESOS (Top 10 por CPU):")
        reporte.append("-" * 20)
        for proc in self.info['procesos']:
            if 'error' not in proc:
                reporte.append(f"{proc['nombre']} (PID: {proc['pid']})")
                reporte.append(f"  CPU: {proc['cpu_percent']:.1f}% | RAM: {proc['memory_percent']:.1f}%")
        reporte.append("")
        
        reporte.append("=" * 60)
        reporte.append("Reporte generado el: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        reporte.append("=" * 60)
        
        return '\n'.join(reporte)
    
    def guardar_reporte(self, ruta_archivo=None):
        """Guarda el reporte en un archivo"""
        if not ruta_archivo:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            ruta_archivo = f"informacion_sistema_{timestamp}.txt"
        
        reporte = self.generar_reporte_texto()
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(reporte)
            return True, f"Reporte guardado en: {ruta_archivo}"
        except Exception as e:
            return False, f"Error al guardar reporte: {str(e)}"

def main():
    """Función principal"""
    # Configurar codificación para Windows
    import sys
    import os
    
    # Intentar configurar UTF-8 para Windows
    if sys.platform.startswith('win'):
        try:
            # Configurar la consola para UTF-8
            os.system('chcp 65001 >nul 2>&1')
            # Configurar stdout para UTF-8
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass  # Si falla, continuar sin emojis
    
    print("Obteniendo información del sistema...")
    
    # Crear instancia
    info_sistema = InfoSistema()
    
    # Obtener información
    info = info_sistema.obtener_info_completa()
    
    # Mostrar resumen
    print("\nRESUMEN DEL SISTEMA:")
    print("-" * 30)
    print(f"Sistema: {info['sistema_operativo']['nombre']} {info['sistema_operativo']['release']}")
    print(f"Arquitectura: {info['sistema_operativo']['arquitectura']}")
    print(f"Hostname: {info['sistema_operativo']['hostname']}")
    
    if 'cpu' in info['hardware'] and 'error' not in info['hardware']['cpu']:
        cpu = info['hardware']['cpu']
        print(f"CPU: {cpu.get('nombre', 'Desconocido')}")
        print(f"Núcleos: {cpu.get('nucleos_fisicos', 'N/A')} físicos, {cpu.get('nucleos_logicos', 'N/A')} lógicos")
    
    if 'error' not in info['memoria']:
        print(f"RAM: {info['memoria']['total']} (Usado: {info['memoria']['porcentaje_uso']:.1f}%)")
    
    print(f"Python: {info['python']['version_info']['major']}.{info['python']['version_info']['minor']}.{info['python']['version_info']['micro']}")
    
    # Preguntar si guardar reporte
    respuesta = input("\n¿Deseas guardar un reporte completo? (s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        success, mensaje = info_sistema.guardar_reporte()
        print(f"\n{mensaje}")
        
        if success:
            print("El reporte incluye información detallada de:")
            print("  - Sistema operativo")
            print("  - Hardware (CPU, GPU, RAM)")
            print("  - Almacenamiento")
            print("  - Red")
            print("  - Procesos")
            print("  - Usuarios")
            print("  - Tiempo del sistema")
    
    print("\nInformación del sistema obtenida exitosamente.")

if __name__ == "__main__":
    import time
    main()
