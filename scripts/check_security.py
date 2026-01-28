#!/usr/bin/env python3
"""
Script de Verificación de Seguridad - ArcheoScope

Verifica que no haya API keys expuestas en el código fuente.
"""

import os
import re
import sys
from pathlib import Path

def check_api_keys():
    """Verificar que no haya API keys reales expuestas."""
    
    print("🔍 Verificando seguridad de API keys...")
    
    # Patrones de API keys a buscar
    patterns = [
        r'sk-or-v1-[a-zA-Z0-9]{64,}',  # OpenRouter keys reales
        r'sk-[a-zA-Z0-9]{48,}',        # Otras keys que empiecen con sk-
        r'API_KEY.*=.*["\'][a-zA-Z0-9]{20,}["\']',  # API_KEY con valores largos
    ]
    
    # Archivos a excluir (seguros)
    exclude_patterns = [
        '*.example',
        'SECURITY_GUIDELINES.md',
        'check_security.py',
        '.git/*',
        '__pycache__/*',
        '*.pyc'
    ]
    
    # Extensiones de archivos a verificar
    include_extensions = ['.py', '.js', '.ts', '.md', '.json', '.yml', '.yaml', '.env']
    
    issues_found = []
    
    # Recorrer todos los archivos
    for root, dirs, files in os.walk('.'):
        # Excluir directorios
        dirs[:] = [d for d in dirs if not d.startswith('.git') and d != '__pycache__']
        
        for file in files:
            file_path = Path(root) / file
            
            # Verificar extensión
            if not any(file.endswith(ext) for ext in include_extensions):
                continue
            
            # Verificar exclusiones
            if any(file.endswith(pattern.replace('*', '')) for pattern in exclude_patterns):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Buscar patrones
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Verificar que no sea un placeholder
                        matched_text = match.group()
                        if not any(placeholder in matched_text.upper() for placeholder in [
                            'XXXXX', 'TU_API_KEY', 'CONFIGURE', 'PLACEHOLDER', 'EXAMPLE'
                        ]):
                            issues_found.append({
                                'file': str(file_path),
                                'line': content[:match.start()].count('\n') + 1,
                                'match': matched_text[:20] + '...' if len(matched_text) > 20 else matched_text,
                                'pattern': pattern
                            })
            
            except Exception as e:
                print(f"⚠️ Error leyendo {file_path}: {e}")
    
    return issues_found

def check_gitignore():
    """Verificar que .gitignore protege archivos sensibles."""
    
    print("🔍 Verificando .gitignore...")
    
    required_patterns = [
        '.env.local',
        '*.key',
        'mcp.json.local'
    ]
    
    try:
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in gitignore_content:
                missing_patterns.append(pattern)
        
        return missing_patterns
    
    except FileNotFoundError:
        return required_patterns  # Todos faltan si no existe .gitignore

def check_env_files():
    """Verificar configuración de archivos de entorno."""
    
    print("🔍 Verificando archivos de configuración...")
    
    issues = []
    
    # Verificar que existe .env.local.example
    if not Path('.env.local.example').exists():
        issues.append("Falta archivo .env.local.example")
    
    # Verificar que NO existe .env.local en Git (debería estar en .gitignore)
    if Path('.env.local').exists():
        # Verificar si está en .gitignore usando git ls-files
        try:
            result = os.system('git ls-files --error-unmatch .env.local > /dev/null 2>&1')
            if result == 0:  # Está siendo trackeado por Git
                issues.append(".env.local existe y ESTÁ siendo trackeado por Git (debería estar en .gitignore)")
        except:
            pass
    
    # Verificar mcp.json
    if Path('mcp.json').exists():
        try:
            with open('mcp.json', 'r') as f:
                content = f.read()
                if 'sk-or-v1-' in content and 'CONFIGURE' not in content.upper():
                    issues.append("mcp.json contiene posibles API keys reales")
        except:
            pass
    
    return issues

def main():
    """Función principal."""
    
    print("🛡️ VERIFICACIÓN DE SEGURIDAD - ARCHEOSCOPE")
    print("=" * 60)
    
    all_good = True
    
    # 1. Verificar API keys
    api_key_issues = check_api_keys()
    if api_key_issues:
        print("❌ API KEYS EXPUESTAS ENCONTRADAS:")
        for issue in api_key_issues:
            print(f"   📁 {issue['file']}:{issue['line']}")
            print(f"      🔑 {issue['match']}")
        all_good = False
    else:
        print("✅ No se encontraron API keys expuestas")
    
    # 2. Verificar .gitignore
    missing_gitignore = check_gitignore()
    if missing_gitignore:
        print("❌ PATRONES FALTANTES EN .gitignore:")
        for pattern in missing_gitignore:
            print(f"   📝 {pattern}")
        all_good = False
    else:
        print("✅ .gitignore configurado correctamente")
    
    # 3. Verificar archivos de entorno
    env_issues = check_env_files()
    if env_issues:
        print("❌ PROBLEMAS DE CONFIGURACIÓN:")
        for issue in env_issues:
            print(f"   ⚠️ {issue}")
        all_good = False
    else:
        print("✅ Archivos de configuración seguros")
    
    print("=" * 60)
    
    if all_good:
        print("🎉 ¡VERIFICACIÓN DE SEGURIDAD EXITOSA!")
        print("   El repositorio está seguro para commit/push")
        return 0
    else:
        print("🚨 PROBLEMAS DE SEGURIDAD ENCONTRADOS")
        print("   Corrige los problemas antes de hacer commit/push")
        print("\n💡 SOLUCIONES:")
        print("   1. Mueve API keys reales a .env.local")
        print("   2. Usa placeholders en código y documentación")
        print("   3. Actualiza .gitignore si es necesario")
        print("   4. Lee SECURITY_GUIDELINES.md para más detalles")
        return 1

if __name__ == "__main__":
    sys.exit(main())