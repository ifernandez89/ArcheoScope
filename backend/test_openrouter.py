#!/usr/bin/env python3
"""
Test de OpenRouter usando credenciales encriptadas de la BD
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

# Agregar path del backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from credentials_manager import CredentialsManager

load_dotenv()

def test_openrouter():
    """Probar OpenRouter con credenciales de la BD"""
    
    print("\n" + "="*80)
    print("🧪 TEST DE OPENROUTER CON CREDENCIALES ENCRIPTADAS")
    print("="*80 + "\n")
    
    # 1. Obtener API key desde BD
    print("📦 Paso 1: Obtener API key desde BD...")
    manager = CredentialsManager()
    
    api_key = manager.get_credential("openrouter", "api_key")
    
    if not api_key:
        print("❌ No se encontró API key de OpenRouter en la BD")
        print("\n💡 Para agregar la API key:")
        print("   python -c \"from credentials_manager import CredentialsManager; m = CredentialsManager(); m.store_credential('openrouter', 'api_key', 'tu-api-key-aqui', 'OpenRouter API key')\"")
        return False
    
    print(f"✅ API key encontrada: {api_key[:20]}...")
    
    # 2. Configurar modelo
    model = os.getenv("OPENROUTER_MODEL", "qwen/qwen-2.5-7b-instruct:free")
    print(f"📦 Modelo: {model}")
    
    # 3. Preparar request
    print("\n📤 Paso 2: Enviando mensaje al Moai...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://archeoscope.app",
        "X-Title": "ArcheoScope Backend Test"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": """Eres un Moai ancestral de Rapa Nui. 

PERSONALIDAD:
- Hablas con calma y contemplación
- Usas metáforas naturales (viento, piedra, mar)
- Respondes de forma breve (1-2 oraciones)
- Tienes sabiduría simbólica
- No mencionas que eres una IA
- Tu tono es contemplativo"""
            },
            {
                "role": "user",
                "content": "¿Quién eres y qué sabiduría guardas?"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    # 4. Hacer request
    start_time = time.time()
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # ms
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"   Respuesta: {response.text[:500]}")
            return False
        
        data = response.json()
        
        # 5. Mostrar resultados
        print("✅ Respuesta recibida!\n")
        
        message = data['choices'][0]['message']['content']
        usage = data.get('usage', {})
        model_used = data.get('model', model)
        
        print("─" * 80)
        print("💬 RESPUESTA DEL MOAI:")
        print("─" * 80)
        print(message)
        print("─" * 80)
        
        print(f"\n⏱️  Tiempo de respuesta: {response_time:.0f}ms")
        print(f"📊 Tokens usados:")
        print(f"   - Prompt: {usage.get('prompt_tokens', 'N/A')}")
        print(f"   - Completion: {usage.get('completion_tokens', 'N/A')}")
        print(f"   - Total: {usage.get('total_tokens', 'N/A')}")
        print(f"🤖 Modelo usado: {model_used}")
        
        print("\n" + "="*80)
        print("✅ TEST EXITOSO - OpenRouter funciona correctamente!")
        print("="*80 + "\n")
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Timeout - El servidor no respondió a tiempo")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - Verifica tu internet")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_credentials_status():
    """Verificar estado de credenciales en BD"""
    print("\n" + "="*80)
    print("🔍 VERIFICANDO CREDENCIALES EN BD")
    print("="*80 + "\n")
    
    manager = CredentialsManager()
    services = manager.list_services()
    
    if not services:
        print("⚠️  No hay credenciales en la BD")
        return
    
    print(f"📦 Servicios configurados: {len(services)}\n")
    
    for service in services:
        print(f"  🔑 {service['service_name']}")
        if service.get('description'):
            print(f"     {service['description']}")
        print(f"     Actualizado: {service['updated_at']}")
        print()
    
    # Verificar OpenRouter específicamente
    openrouter_key = manager.get_credential("openrouter", "api_key")
    
    if openrouter_key:
        print("✅ OpenRouter API key encontrada en BD")
        print(f"   Key: {openrouter_key[:20]}...{openrouter_key[-10:]}")
    else:
        print("❌ OpenRouter API key NO encontrada en BD")
        print("\n💡 Para agregar:")
        print('   python -c "from credentials_manager import CredentialsManager; m = CredentialsManager(); m.store_credential(\'openrouter\', \'api_key\', \'sk-or-v1-tu-key-aqui\', \'OpenRouter API key\')"')


if __name__ == "__main__":
    # Verificar estado de credenciales
    check_credentials_status()
    
    # Ejecutar test
    success = test_openrouter()
    
    sys.exit(0 if success else 1)
