#!/usr/bin/env python3
"""
Verificar progreso de la recopilación sin interrumpir el proceso
"""

import json
import os
from datetime import datetime

print("🔍 Verificando progreso de recopilación...\n")

# Verificar archivos existentes
files = [
    'harvested_archaeological_sites.json',
    'harvested_complete.json',
    'harvested_sites.json'
]

for filename in files:
    if os.path.exists(filename):
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        modified = datetime.fromtimestamp(os.path.getmtime(filename))
        
        print(f"📄 {filename}")
        print(f"   Tamaño: {size_mb:.2f} MB")
        print(f"   Modificado: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                total = data.get('metadata', {}).get('total_sites', 0)
                sources = data.get('metadata', {}).get('source_statistics', {})
                
                print(f"   Total sitios: {total:,}")
                print(f"   Fuentes:")
                for source, count in sources.items():
                    print(f"      • {source}: {count:,}")
        except:
            print(f"   ⚠️  Archivo en proceso de escritura o corrupto")
        
        print()

print("✅ Verificación completada")
