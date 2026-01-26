#!/usr/bin/env python3
"""
Test Earthdata Credentials
===========================
Verifica que las credenciales estén correctamente configuradas
"""

import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

print("="*80)
print("🔐 Verificación de Credenciales Earthdata")
print("="*80)
print()

username = os.getenv('EARTHDATA_USERNAME')
password = os.getenv('EARTHDATA_PASSWORD')
token = os.getenv('EARTHDATA_TOKEN')

print(f"EARTHDATA_USERNAME: {'✅ Configurado' if username else '❌ No encontrado'}")
if username:
    print(f"   Valor: {username}")

print(f"EARTHDATA_PASSWORD: {'✅ Configurado' if password else '❌ No encontrado'}")
if password:
    print(f"   Valor: {'*' * len(password)}")

print(f"EARTHDATA_TOKEN: {'✅ Configurado' if token else '❌ No encontrado'}")
if token:
    print(f"   Valor: {token[:50]}...")

print()

if username and password:
    print("✅ Credenciales completas - Probando autenticación...")
    print()
    
    try:
        import earthaccess
        
        # Intentar login
        auth = earthaccess.login(strategy="environment")
        
        if auth:
            print("✅ AUTENTICACIÓN EXITOSA con NASA Earthdata")
            print("✅ ICESat-2, MODIS y SMAP deberían funcionar")
        else:
            print("❌ Autenticación falló")
    
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ Faltan credenciales")
    print("   Agrega EARTHDATA_USERNAME y EARTHDATA_PASSWORD al .env")
