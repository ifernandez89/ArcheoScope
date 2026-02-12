#!/usr/bin/env python3
"""
Setup de OpenRouter - Agregar API key a la BD
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from credentials_manager import CredentialsManager

def setup_openrouter():
    """Configurar OpenRouter con API key"""
    
    print("\n" + "="*80)
    print("🔧 SETUP DE OPENROUTER")
    print("="*80 + "\n")
    
    # Obtener API key
    api_key = input("Ingresa tu OpenRouter API key (o presiona Enter para usar variable de entorno): ").strip()
    
    if not api_key:
        # Intentar desde .env
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not api_key or api_key == "sk-or-v1-TU_API_KEY_AQUI":
            print("\n❌ No se encontró API key válida")
            print("\n💡 Opciones:")
            print("   1. Obtén una API key gratis en: https://openrouter.ai/keys")
            print("   2. Ejecuta este script de nuevo y pégala cuando se solicite")
            print("   3. O agrégala al .env como OPENROUTER_API_KEY=tu-key-aqui")
            return False
    
    # Validar formato
    if not api_key.startswith("sk-or-v1-"):
        print(f"\n⚠️  Advertencia: La API key no tiene el formato esperado (sk-or-v1-...)")
        confirm = input("¿Continuar de todos modos? (s/n): ").strip().lower()
        if confirm != 's':
            return False
    
    # Guardar en BD
    print(f"\n📦 Guardando API key en BD...")
    print(f"   Key: {api_key[:20]}...{api_key[-10:]}")
    
    manager = CredentialsManager()
    success = manager.store_credential(
        "openrouter", 
        "api_key", 
        api_key, 
        "OpenRouter API key para avatar conversacional"
    )
    
    if success:
        print("\n✅ API key guardada correctamente en BD (encriptada)")
        print("\n🧪 Ahora puedes ejecutar el test:")
        print("   python backend/test_openrouter.py")
        return True
    else:
        print("\n❌ Error guardando API key")
        return False


if __name__ == "__main__":
    success = setup_openrouter()
    sys.exit(0 if success else 1)
