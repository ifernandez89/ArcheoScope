#!/usr/bin/env python3
"""
Reemplazar TODOS los logger por prints en métodos críticos
"""

import re

files_to_fix = [
    ('backend/core_anomaly_detector.py', [
        '_measure_with_instruments',
        '_get_real_instrument_measurement'
    ]),
    ('backend/satellite_connectors/real_data_integrator.py', [
        'get_instrument_measurement'
    ])
]

for file_path, methods in files_to_fix:
    print(f"\nProcesando: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Reemplazar logger por print
    content = re.sub(r'logger\.info\(', 'print(', content)
    content = re.sub(r'logger\.warning\(', 'print(', content)
    content = re.sub(r'logger\.error\(', 'print(', content)
    content = re.sub(r'logger\.debug\(', 'print(', content)
    
    # Agregar flush=True a prints que no lo tienen
    # Buscar print( que no termina con flush=True)
    content = re.sub(r'print\(([^)]+)\)(?!\s*,\s*flush=True)', r'print(\1, flush=True)', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] Reemplazados loggers por prints")
    else:
        print(f"  [SKIP] Sin cambios")

print("\nListo!")
