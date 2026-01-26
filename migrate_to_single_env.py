#!/usr/bin/env python3
"""
Script de migración: .env.local → .env

Migra la configuración de .env.local a .env unificado.
"""

import os
import shutil
from pathlib import Path

def migrate_env():
    """Migrar de .env.local a .env"""
    
    print("=" * 60)
    print("🔄 MIGRACIÓN: .env.local → .env")
    print("=" * 60)
    print()
    
    env_local = Path('.env.local')
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    # 1. Verificar si existe .env.local
    if env_local.exists():
        print(f"✅ Encontrado: {env_local}")
        
        # Hacer backup
        backup = Path('.env.local.backup')
        shutil.copy(env_local, backup)
        print(f"💾 Backup creado: {backup}")
        
        # Copiar a .env
        shutil.copy(env_local, env_file)
        print(f"✅ Migrado a: {env_file}")
        print()
        
        print("⚠️  IMPORTANTE:")
        print(f"   - Tu configuración está ahora en: {env_file}")
        print(f"   - Backup guardado en: {backup}")
        print(f"   - Puedes eliminar {env_local} si todo funciona")
        print()
        
    elif env_file.exists():
        print(f"✅ Ya existe: {env_file}")
        print("   No se requiere migración")
        print()
        
    else:
        print(f"⚠️  No existe ni .env.local ni .env")
        
        if env_example.exists():
            print(f"📝 Creando {env_file} desde {env_example}...")
            shutil.copy(env_example, env_file)
            print(f"✅ Creado: {env_file}")
            print()
            print("⚠️  IMPORTANTE: Edita .env y configura tus API keys")
            print()
        else:
            print(f"❌ No se encontró {env_example}")
            print("   Crea .env manualmente")
            return False
    
    # 2. Verificar .gitignore
    print("🔒 Verificando seguridad...")
    gitignore = Path('.gitignore')
    
    if gitignore.exists():
        content = gitignore.read_text()
        
        if '.env' in content or '.env\n' in content:
            print("✅ .env está en .gitignore")
        else:
            print("⚠️  .env NO está en .gitignore")
            print("   Agregando...")
            
            with open(gitignore, 'a') as f:
                f.write('\n# Environment variables\n.env\n')
            
            print("✅ .env agregado a .gitignore")
    else:
        print("⚠️  No existe .gitignore")
    
    print()
    
    # 3. Verificar que .env no esté en Git
    print("🔍 Verificando Git...")
    
    result = os.system('git ls-files --error-unmatch .env > nul 2>&1')
    
    if result == 0:
        print("❌ PELIGRO: .env está siendo trackeado por Git!")
        print()
        print("   SOLUCIÓN:")
        print("   1. git rm --cached .env")
        print("   2. git commit -m 'Remove .env from tracking'")
        print("   3. Verifica que .env esté en .gitignore")
        print()
    else:
        print("✅ .env NO está en Git (correcto)")
    
    print()
    
    # 4. Resumen
    print("=" * 60)
    print("✅ MIGRACIÓN COMPLETADA")
    print("=" * 60)
    print()
    print("📋 PRÓXIMOS PASOS:")
    print()
    print("1. Verifica tu configuración:")
    print("   - Abre .env")
    print("   - Confirma que tus API keys están ahí")
    print()
    print("2. Habilita OpenCode (si quieres):")
    print("   - OPENCODE_ENABLED=true")
    print("   - Inicia: python opencode_mock_server.py")
    print()
    print("3. Prueba el sistema:")
    print("   - python test_opencode_validator.py")
    print("   - python run_archeoscope.py")
    print()
    print("4. NUNCA subas .env a Git!")
    print("   - Solo comparte .env.example")
    print()
    
    return True

if __name__ == '__main__':
    success = migrate_env()
    exit(0 if success else 1)
