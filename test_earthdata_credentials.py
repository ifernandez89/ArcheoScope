#!/usr/bin/env python3
"""Test directo de credenciales Earthdata"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.credentials_manager import CredentialsManager

cm = CredentialsManager()

print("="*80)
print("TEST EARTHDATA CREDENTIALS")
print("="*80)
print()

# Test individual
username = cm.get_credential("earthdata", "username")
password = cm.get_credential("earthdata", "password")

if username:
    print(f"✅ Username: {username}")
else:
    print(f"❌ Username: NO ENCONTRADO")

if password:
    print(f"✅ Password: {'*' * len(password)}")
else:
    print(f"❌ Password: NO ENCONTRADO")

print()
print("="*80)
