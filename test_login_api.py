#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Login API - ModuStackClean
Cliente de prueba para verificar el login con la API
"""

import requests
import json

def test_api_login():
    """Probar el login con la API"""
    
    print("🧪 Test Login API - ModuStackClean")
    print("=" * 50)
    
    # URL base
    BASE_URL = "https://rulossoluciones.com/modustackclean"
    
    print(f"📋 URL Base: {BASE_URL}")
    
    # Test 1: Ping
    print("\n1️⃣ Probando ping...")
    try:
        response = requests.get(f"{BASE_URL}/api/ping", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Ping exitoso: {data.get('mensaje', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Obtener usuarios
    print("\n2️⃣ Obteniendo usuarios...")
    try:
        response = requests.get(f"{BASE_URL}/api/usuarios", timeout=10)
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('data', {}).get('usuarios', [])
            print(f"✅ Usuarios obtenidos: {len(usuarios)}")
            if usuarios:
                print(f"📋 Primer usuario: {usuarios[0].get('nombre', 'N/A')} ({usuarios[0].get('correo', 'N/A')})")
        else:
            print(f"❌ Error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 3: Login con usuario existente
    if usuarios:
        primer_usuario = usuarios[0]
        correo = primer_usuario.get('correo')
        
        print(f"\n3️⃣ Probando login con usuario: {correo}")
        try:
            login_data = {
                'correo': correo,
                'password': 'test123'  # Contraseña de prueba
            }
            
            response = requests.post(f"{BASE_URL}/api/login", json=login_data, timeout=10)
            print(f"📊 Status Code: {response.status_code}")
            print(f"📄 Respuesta: {response.text[:200]}...")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    usuario = data.get('data', {}).get('usuario')
                    print(f"✅ Login exitoso: {usuario.get('nombre', 'N/A')}")
                else:
                    print(f"❌ Login fallido: {data.get('mensaje', 'N/A')}")
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test 4: Login con usuario inexistente
    print(f"\n4️⃣ Probando login con usuario inexistente...")
    try:
        login_data = {
            'correo': 'usuario_inexistente@test.com',
            'password': 'test123'
        }
        
        response = requests.post(f"{BASE_URL}/api/login", json=login_data, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Respuesta: {response.text[:200]}...")
        
        if response.status_code == 401:
            data = response.json()
            print(f"✅ Login rechazado correctamente: {data.get('mensaje', 'N/A')}")
        else:
            print(f"⚠️ Respuesta inesperada: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Prueba completada")

if __name__ == "__main__":
    test_api_login()
