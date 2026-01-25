#!/usr/bin/env python3
"""
AUDITORÍA COMPLETA DEL SISTEMA - Solución definitiva para IndentationError
"""

import ast
import sys

class CodeAuditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.errors = []
        self.warnings = []
        
    def audit_file(self):
        """Auditoría completa del archivo"""
        print(f"AUDITORÍA: {self.file_path}")
        print("="*60)
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # 1. Verificar sintaxis básica
            print("1. Verificando sintaxis AST...")
            try:
                ast.parse(content)
                print("   ✓ Sintaxis AST correcta")
            except SyntaxError as e:
                print(f"   ❌ Error sintaxis: Línea {e.lineno}: {e.msg}")
                self.errors.append(f"Sintaxis: Línea {e.lineno}: {e.msg}")
            
            # 2. Verificar indentación consistente
            print("2. Verificando indentación...")
            self._check_indentation(lines)
            
            # 3. Verificar definiciones de métodos
            print("3. Verificando definiciones de métodos...")
            self._check_method_definitions(lines)
            
            # 4. Verificar balance de parentesis/llaves
            print("4. Verificando balance de estructuras...")
            self._check_structural_balance(content)
            
            # 5. Detectar caracteres problemáticos
            print("5. Verificando caracteres especiales...")
            self._check_special_characters(content)
            
            # 6. Verificar línea 439 específicamente
            print("6. Revisando línea 439 problemática...")
            self._check_line_439(lines)
            
            return len(self.errors) == 0
            
        except Exception as e:
            print(f"❌ Error auditando: {e}")
            self.errors.append(f"Auditoría: {e}")
            return False
    
    def _check_indentation(self, lines):
        """Verificar indentación consistente"""
        for i, line in enumerate(lines, 1):
            if line.strip():  # Ignorar líneas vacías
                # Contar espacios al inicio
                leading_spaces = len(line) - len(line.lstrip())
                
                # Verificar que sea múltiplo de 4
                if leading_spaces % 4 != 0:
                    print(f"   ⚠️ Línea {i}: Indentación no múltiplo de 4 ({leading_spaces} espacios)")
                    self.warnings.append(f"Línea {i}: Indentación {leading_spaces} (debe ser múltiplo de 4)")
                
                # Verificar que no haya tabs
                if '\t' in line:
                    print(f"   ❌ Línea {i}: Contiene TABs")
                    self.errors.append(f"Línea {i}: Contiene TABs")
    
    def _check_method_definitions(self, lines):
        """Verificar definiciones de métodos"""
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('def '):
                # Verificar formato correcto
                if 'self' not in line and line.strip().startswith('def _'):
                    print(f"   ⚠️ Línea {i}: Método sin 'self' - {stripped[:30]}...")
                    self.warnings.append(f"Línea {i}: Método posible sin 'self'")
                
                # Verificar indentación (debe ser nivel de clase)
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces == 4:
                    print(f"   ✓ Línea {i}: Método a nivel de clase correcto")
                elif leading_spaces == 8:
                    print(f"   ⚠️ Línea {i}: Método anidado (indentación 8)")
                    self.warnings.append(f"Línea {i}: Método anidado")
                else:
                    print(f"   ❌ Línea {i}: Indentación de método incorrecta ({leading_spaces})")
                    self.errors.append(f"Línea {i}: Indentación método {leading_spaces}")
    
    def _check_structural_balance(self, content):
        """Verificar balance de paréntesis, llaves, corchetes"""
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        
        for i, char in enumerate(content):
            if char in brackets:
                stack.append((char, i))
            elif char in brackets.values():
                if not stack:
                    print(f"   ❌ Carácter {char} sin apertura en posición {i}")
                    self.errors.append(f"Carácter {char} sin apertura en pos {i}")
                else:
                    open_char, _ = stack.pop()
                    if brackets[open_char] != char:
                        print(f"   ❌ Mismatch: {open_char} ... {char}")
                        self.errors.append(f"Mismatch {open_char}...{char}")
        
        if stack:
            print(f"   ❌ {len(stack)} caracteres sin cerrar")
            for char, pos in stack:
                self.errors.append(f"Carácter {char} sin cerrar en pos {pos}")
    
    def _check_special_characters(self, content):
        """Detectar caracteres problemáticos"""
        problematic_chars = []
        for i, char in enumerate(content):
            if ord(char) > 127 and char not in '\n\t\r':
                problematic_chars.append((char, ord(char), i))
        
        if problematic_chars:
            print(f"   ⚠️ {len(problematic_chars)} caracteres especiales detectados:")
            for char, code, pos in problematic_chars[:5]:  # Mostrar solo primeros 5
                print(f"      Pos {pos}: '{char}' (U+{code:04X})")
            self.warnings.append(f"{len(problematic_chars)} caracteres especiales")
    
    def _check_line_439(self, lines):
        """Revisión específica de la línea 439"""
        if len(lines) >= 439:
            line_439 = lines[438]  # 0-indexed
            print(f"   Línea 439: '{line_439}'")
            
            # Verificar problemas específicos
            if line_439.strip().startswith('def '):
                leading_spaces = len(line_439) - len(line_439.lstrip())
                print(f"   → Espacios iniciales: {leading_spaces}")
                
                if leading_spaces != 4:
                    print(f"   ❌ ERROR: Debe tener 4 espacios, tiene {leading_spaces}")
                    self.errors.append(f"Línea 439: Indentación {leading_spaces} (debe ser 4)")
                
                # Verificar que no esté dentro de otra función
                # Buscar hacia atrás para encontrar la función contenedora
                for j in range(437, -1, -1):
                    if lines[j].strip().startswith('def ') and j > 0:
                        parent_spaces = len(lines[j]) - len(lines[j].lstrip())
                        if parent_spaces == 4 and leading_spaces == 4:
                            print(f"   ✓ Línea 439: Correctamente a nivel de clase")
                        elif parent_spaces < 4:
                            print(f"   ⚠️ Línea 439: Función huérfana")
                            self.warnings.append("Línea 439: Función huérfana")
                        break
        else:
            print(f"   ⚠️ Archivo tiene menos de 439 líneas")
    
    def generate_fix(self):
        """Generar solución automática"""
        print(f"\nGENERANDO SOLUCIÓN...")
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Fix 1: Corregir indentación de línea 439
            if len(lines) >= 439:
                line_439 = lines[438]
                if line_439.strip().startswith('def _get_site_type'):
                    lines[438] = '    def _get_site_type(self, site_info) -> str:'
                    print("   ✓ Línea 439 arreglada")
            
            # Fix 2: Reemplazar todos los TABs con 4 espacios
            for i, line in enumerate(lines):
                if '\t' in line:
                    lines[i] = line.replace('\t', '    ')
                    print(f"   ✓ TABs reemplazados en línea {i+1}")
            
            # Fix 3: Asegurar consistencia de indentación
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#'):
                    leading_spaces = len(line) - len(line.lstrip())
                    if leading_spaces > 0 and leading_spaces % 4 != 0:
                        # Ajustar al múltiplo más cercano de 4
                        corrected_spaces = (leading_spaces // 4 + 1) * 4
                        lines[i] = ' ' * corrected_spaces + line.lstrip()
                        print(f"   ✓ Indentación corregida línea {i+1}: {leading_spaces} → {corrected_spaces}")
            
            # Escribir archivo corregido
            fixed_content = '\n'.join(lines)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print("   ✓ Archivo corregido y guardado")
            return True
            
        except Exception as e:
            print(f"   ❌ Error generando fix: {e}")
            return False

def main():
    """Función principal de auditoría"""
    file_path = r"C:\Python\ArcheoScope\backend\core_anomaly_detector.py"
    
    print("AUDITORIA COMPLETA DEL SISTEMA")
    print("Resolución IndentationError - CoreAnomalyDetector")
    print("="*70)
    
    auditor = CodeAuditor(file_path)
    
    # Ejecutar auditoría
    success = auditor.audit_file()
    
    print(f"\n📊 RESULTADOS:")
    print(f"   Errores: {len(auditor.errors)}")
    print(f"   Advertencias: {len(auditor.warnings)}")
    
    if auditor.errors:
        print(f"\n❌ ERRORES ENCONTRADOS:")
        for error in auditor.errors:
            print(f"   - {error}")
    
    if auditor.warnings:
        print(f"\n⚠️ ADVERTENCIAS:")
        for warning in auditor.warnings:
            print(f"   - {warning}")
    
    # Generar solución si hay errores
    if auditor.errors:
        print(f"\n🔧 GENERANDO SOLUCIÓN AUTOMÁTICA...")
        if auditor.generate_fix():
            print("✅ Solución aplicada")
            
            # Verificar después del fix
            print("\n🔍 VERIFICANDO SOLUCIÓN...")
            try:
                import py_compile
                py_compile.compile(file_path, doraise=True)
                print("✅ COMPILACIÓN EXITOSA")
                print("\n🎉 BACKEND ARREGLADO")
                print("   Puede iniciar con: python run_archeoscope.py")
                return True
            except Exception as e:
                print(f"❌ Error en compilación final: {e}")
                return False
        else:
            print("❌ No se pudo aplicar solución")
            return False
    else:
        print("\n✅ SIN ERRORES - Archivo OK")
        return True

if __name__ == "__main__":
    main()