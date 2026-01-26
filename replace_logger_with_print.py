#!/usr/bin/env python3
"""
Reemplazar logger.info/warning por prints en métodos de medición
"""

import re

file_path = 'backend/core_anomaly_detector.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar el método _measure_with_instruments
start_marker = 'async def _measure_with_instruments'
end_marker = 'async def _get_real_instrument_measurement'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print("ERROR: No se encontraron los métodos")
    exit(1)

# Extraer el método
before = content[:start_idx]
method = content[start_idx:end_idx]
after = content[end_idx:]

# Reemplazar logger por print en el método
method = method.replace('logger.info(f"', 'print(f"')
method = method.replace('logger.info(f\'', 'print(f\'')
method = method.replace('logger.info("', 'print("')
method = method.replace('logger.info(\'', 'print(\'')
method = method.replace('logger.warning(f"', 'print(f"')
method = method.replace('logger.warning(f\'', 'print(f\'')

# Agregar flush=True a todos los prints
method = re.sub(r'print\(([^)]+)\)', r'print(\1, flush=True)', method)

# Reconstruir
new_content = before + method + after

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("OK - logger reemplazado por print en _measure_with_instruments")
