#!/usr/bin/env python3
"""
Remover TODOS los emojis de los archivos de logging
"""

import re

files_to_fix = [
    'backend/core_anomaly_detector.py',
    'backend/satellite_connectors/real_data_integrator.py'
]

# Mapeo de emojis a texto
emoji_replacements = {
    '🔬': '[MEASURE]',
    '📡': '[API]',
    '✅': '[OK]',
    '❌': '[FAIL]',
    '⚠️': '[WARN]',
    '🎯': '[TARGET]',
    '📊': '[STATS]',
    '🔍': '[SEARCH]',
    '🏛️': '[DB]',
    '📝': '[WRITE]',
    'ℹ️': '[INFO]',
    '°': '',  # Grado celsius
    'Región': 'Region',
    'región': 'region',
    'Medición': 'Medicion',
    'medición': 'medicion',
    'Térmico': 'Termico',
    'térmico': 'termico',
    'Elevación': 'Elevacion',
    'elevación': 'elevacion',
    'Concentración': 'Concentracion',
    'concentración': 'concentracion',
    'térmica': 'termica',
    'Inercia térmica': 'Inercia termica',
    'arqueológica': 'arqueologica',
    'arqueológico': 'arqueologico',
    'anomalías': 'anomalias',
    'Probabilidad arqueológica': 'Probabilidad arqueologica',
}

for filepath in files_to_fix:
    print(f"Procesando: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Reemplazar emojis y acentos
    for emoji, replacement in emoji_replacements.items():
        content = content.replace(emoji, replacement)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] Emojis removidos")
    else:
        print(f"  [SKIP] Sin cambios")

print("\nListo!")
