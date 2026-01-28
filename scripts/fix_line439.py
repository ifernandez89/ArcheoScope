#!/usr/bin/env python3
"""
Fix específico para línea 439 - IndentationError
"""

# Leer el archivo
file_path = r"C:\Python\ArcheoScope\backend\core_anomaly_detector.py"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix específico línea 439 (índice 438)
if len(lines) > 438:
    # Reemplazar la línea problemática con indentación correcta
    lines[438] = '    def _get_site_type(self, site_info) -> str:\n'
    print("Linea 439 arreglada")

# Escribir de vuelta
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Archivo arreglado - probando compilación...")