#!/usr/bin/env python3
"""Verificar credenciales Earthdata en BD"""

import sys
sys.path.insert(0, 'backend')

from credentials_manager import CredentialsManager

cm = CredentialsManager()

username = cm.get_credential('earthdata', 'username')
password = cm.get_credential('earthdata', 'password')

print("="*80)
print("VERIFICACIÓN DE CREDENCIALES EARTHDATA")
print("="*80)

if username:
    print(f"✅ Username encontrado: {username[:10]}...")
else:
    print("❌ Username NO encontrado")

if password:
    print(f"✅ Password encontrado: {'*' * len(password)}")
else:
    print("❌ Password NO encontrado")

print("="*80)

if username and password:
    print("✅ CREDENCIALES COMPLETAS - VIIRS debería funcionar")
else:
    print("❌ CREDENCIALES FALTANTES - VIIRS no funcionará")
    print("\nPara agregar credenciales:")
    print("  python backend/credentials_manager.py")
    print("  Seleccionar: earthdata")
    print("  Ingresar username y password de NASA Earthdata")

print("="*80)
