#!/usr/bin/env python3
"""
Arreglar errores de indentación en core_anomaly_detector.py
"""

import re

def fix_indentation():
    """Fix indentation issues in the problematic file"""
    
    file_path = r"C:\Python\ArcheoScope\backend\core_anomaly_detector.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Archivo leído, buscando errores...")
        
        # Fix 1: Replace tabs with 4 spaces
        content = content.replace('\t', '    ')
        
        # Fix 2: Fix the specific line 439 issue
        # Look for problematic function definition
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if i == 438:  # Line 439 (0-indexed)
                print(f"Línea {i+1}: '{line}'")
                # Fix indentation to exactly 4 spaces for method definition
                if line.strip().startswith('def _get_site_type'):
                    lines[i] = '    def _get_site_type(self, site_info) -> str:'
                    print(f"Arreglado a: '{lines[i]}'")
        
        content = '\n'.join(lines)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Archivo arreglado")
        
        # Test compilation
        import subprocess
        result = subprocess.run([
            'python', '-m', 'py_compile', file_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Compilación exitosa")
            return True
        else:
            print(f"❌ Error de compilación: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Arreglando IndentationError en core_anomaly_detector.py")
    print("="*60)
    
    success = fix_indentation()
    
    if success:
        print("\n✅ Backend arreglado - puede iniciar con: python run_archeoscope.py")
    else:
        print("\n❌ Requiere revisión manual del archivo")