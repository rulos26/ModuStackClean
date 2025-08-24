#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente Python para API ModuStackClean - Versión Corregida
"""

import requests
import json

def test_api_modustackclean():
    """Probar la API de ModuStackClean con nueva configuración"""
    
    print("🧪 Test API ModuStackClean - Versión Corregida")
    print("=" * 60)
    
    # URL base
    BASE_URL = "https://rulossoluciones.com/modustackclean"
    
    print(f"📋 URL Base: {BASE_URL}")
    
    # Test 1: Ruta base
    print("\n1️⃣ Probando ruta base...")
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Respuesta completa: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Ruta base exitosa: {data.get('mensaje', 'N/A')}")
                if 'data' in data and 'endpoints' in data['data']:
                    print(f"📋 Endpoints disponibles: {list(data['data']['endpoints'].keys())}")
            except json.JSONDecodeError as e:
                print(f"❌ Error JSON: {e}")
                print(f"📄 Contenido: {response.text}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: Ping
    print("\n2️⃣ Probando ping...")
    try:
        response = requests.get(f"{BASE_URL}/api/ping", timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Respuesta completa: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Ping exitoso: {data.get('mensaje', 'N/A')}")
            except json.JSONDecodeError as e:
                print(f"❌ Error JSON: {e}")
                print(f"📄 Contenido: {response.text}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: Info
    print("\n3️⃣ Probando información...")
    try:
        response = requests.get(f"{BASE_URL}/api/info", timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Respuesta completa: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                name = data.get('data', {}).get('name', 'N/A')
                version = data.get('data', {}).get('version', 'N/A')
                print(f"✅ API: {name}")
                print(f"✅ Versión: {version}")
            except json.JSONDecodeError as e:
                print(f"❌ Error JSON: {e}")
                print(f"📄 Contenido: {response.text}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 4: Prueba BD
    print("\n4️⃣ Probando conexión a BD...")
    try:
        response = requests.get(f"{BASE_URL}/api/prueba", timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Respuesta completa: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Conexión BD exitosa: {data.get('mensaje', 'N/A')}")
                if 'data' in data and 'prueba' in data['data']:
                    print(f"📊 Datos de prueba: {data['data']['prueba']}")
            except json.JSONDecodeError as e:
                print(f"❌ Error JSON: {e}")
                print(f"📄 Contenido: {response.text}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 5: Usuarios
    print("\n5️⃣ Probando usuarios...")
    try:
        response = requests.get(f"{BASE_URL}/api/usuarios", timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Respuesta completa: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                count = data.get('data', {}).get('count', 0)
                print(f"✅ Usuarios obtenidos: {count}")
                if 'data' in data and 'usuarios' in data['data']:
                    usuarios = data['data']['usuarios']
                    if usuarios:
                        print(f"📋 Primer usuario: {usuarios[0].get('nombre', 'N/A')}")
            except json.JSONDecodeError as e:
                print(f"❌ Error JSON: {e}")
                print(f"📄 Contenido: {response.text}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 6: Health
    print("\n6️⃣ Probando estado de salud...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Respuesta completa: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                status = data.get('data', {}).get('status', 'N/A')
                db_status = data.get('data', {}).get('database', 'N/A')
                print(f"✅ Estado general: {status}")
                print(f"✅ Base de datos: {db_status}")
            except json.JSONDecodeError as e:
                print(f"❌ Error JSON: {e}")
                print(f"📄 Contenido: {response.text}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 60)
    print("🏁 Prueba completada")

if __name__ == "__main__":
    test_api_modustackclean()
