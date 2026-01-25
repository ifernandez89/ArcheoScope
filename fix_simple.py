#!/usr/bin/env python3
"""
SOLUCIÓN MANUAL - Reconstrucción del archivo
"""

def fix_simple():
    """Fix simple y directo"""
    file_path = r"C:\Python\ArcheoScope\backend\core_anomaly_detector.py"
    
    print("SOLUCIÓN MANUAL SIMPLE")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Fix general: limpiar todas las líneas
    fixed_lines = []
    for i, line in enumerate(lines):
        # Remover tabs
        clean_line = line.replace('\t', '    ')
        
        # Fix específicos
        if i == 247:  # línea 248
            clean_line = '        return measurements\n'
        elif i == 248 and clean_line.strip().startswith('def _simulate_instrument_measurement'):
            clean_line = '    def _simulate_instrument_measurement(self, indicator_name: str, \n'
        elif i == 438 and clean_line.strip().startswith('def _get_site_type'):
            clean_line = '    def _get_site_type(self, site_info) -> str:\n'
        
        fixed_lines.append(clean_line)
    
    # Guardar
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Archivo limpiado y guardado")
    
    # Test compilación
    try:
        import py_compile
        py_compile.compile(file_path, doraise=True)
        print("COMPILACION EXITOSA!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if fix_simple():
        print("EXITO!")
    else:
        print("FALLO!")