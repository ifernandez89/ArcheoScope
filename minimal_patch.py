#!/usr/bin/env python3
"""
RESTAURAR Y APLICAR PATCH MÍNIMO
"""

def minimal_fix():
    """Aplicar el mínimo cambio necesario"""
    file_path = r"C:\Python\ArcheoScope\backend\core_anomaly_detector.py"
    
    # Leer archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the problematic function and fix indentation
    lines = content.split('\n')
    
    # Find line with def _get_site_type that's incorrectly indented
    for i, line in enumerate(lines):
        if 'def _get_site_type(self, site_info) -> str:' in line:
            # Fix indentation to 4 spaces (class level)
            if not line.startswith('    def _get_site_type'):
                lines[i] = '    def _get_site_type(self, site_info) -> str:'
                print(f"Línea {i+1} arreglada: {lines[i]}")
            break
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("Patch aplicado - testeando compilación...")
    
    # Test
    try:
        import py_compile
        py_compile.compile(file_path, doraise=True)
        print("EXITO - Backend arreglado!")
        return True
    except Exception as e:
        print(f"Fallo: {e}")
        return False

if __name__ == "__main__":
    minimal_fix()