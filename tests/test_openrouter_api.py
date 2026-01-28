#!/usr/bin/env python3
"""
Test directo de la API de OpenRouter
"""

import requests
import json
import time

def test_openrouter_direct():
    """Test directo de OpenRouter API."""
    
    print("🤖 TESTING OPENROUTER API DIRECTLY")
    print("=" * 50)
    
    # Configuración desde .env.local
    api_key = os.getenv('OPENROUTER_API_KEY', 'sk-or-v1-CONFIGURE_YOUR_KEY_IN_ENV_LOCAL')
    model = "google/gemini-2.5-flash-preview-09-2025"
    
    print(f"🔑 API Key: {api_key[:20]}...{api_key[-10:]}")
    print(f"🤖 Modelo: {model}")
    
    # Test 1: Verificar modelos disponibles
    print("\n1. 🔍 Verificando modelos disponibles...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            models_data = response.json()
            available_models = [m['id'] for m in models_data.get('data', [])]
            
            print(f"✅ Modelos disponibles: {len(available_models)}")
            
            # Buscar nuestro modelo específico
            if model in available_models:
                print(f"✅ Modelo {model} DISPONIBLE")
            else:
                print(f"❌ Modelo {model} NO DISPONIBLE")
                
                # Buscar modelos Gemini alternativos
                gemini_models = [m for m in available_models if 'gemini' in m.lower()]
                print(f"🔍 Modelos Gemini disponibles: {gemini_models[:5]}")
                
                if gemini_models:
                    model = gemini_models[0]  # Usar el primero disponible
                    print(f"🔄 Cambiando a modelo: {model}")
        else:
            print(f"❌ Error obteniendo modelos: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Probar chat completion
    print(f"\n2. 💬 Probando chat completion con {model}...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un arqueólogo experto especializado en teledetección arqueológica."
                },
                {
                    "role": "user",
                    "content": "Analiza brevemente: se detectaron anomalías espaciales en una región de 1 km² con persistencia temporal y coherencia geométrica. ¿Qué interpretación arqueológica darías?"
                }
            ],
            "max_tokens": 150,
            "temperature": 0.3
        }
        
        print("📡 Enviando request...")
        start_time = time.time()
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        response_time = time.time() - start_time
        print(f"⏱️ Tiempo de respuesta: {response_time:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"✅ RESPUESTA EXITOSA:")
                print(f"📝 Contenido: {content[:200]}...")
                
                # Verificar uso de tokens
                if 'usage' in result:
                    usage = result['usage']
                    print(f"🔢 Tokens usados: {usage.get('total_tokens', 'N/A')}")
                
                return True
            else:
                print(f"❌ Respuesta sin contenido: {result}")
                return False
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en chat completion: {e}")
        return False

def test_alternative_models():
    """Probar modelos alternativos si el principal falla."""
    
    print("\n3. 🔄 Probando modelos alternativos...")
    
    api_key = os.getenv('OPENROUTER_API_KEY', 'sk-or-v1-CONFIGURE_YOUR_KEY_IN_ENV_LOCAL')
    
    # Modelos alternativos a probar
    alternative_models = [
        "google/gemini-flash-1.5",
        "google/gemini-pro",
        "anthropic/claude-3-haiku",
        "openai/gpt-3.5-turbo"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for model in alternative_models:
        print(f"\n🧪 Probando {model}...")
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "Test: responde solo 'OK' si me entiendes."
                }
            ],
            "max_tokens": 10,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    print(f"✅ {model}: {content.strip()}")
                    return model  # Retornar el primer modelo que funcione
                else:
                    print(f"⚠️ {model}: Sin contenido")
            else:
                print(f"❌ {model}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {model}: {e}")
    
    return None

if __name__ == "__main__":
    print("🤖 OPENROUTER API TEST")
    print("=" * 30)
    
    success = test_openrouter_direct()
    
    if not success:
        print("\n🔄 Probando modelos alternativos...")
        working_model = test_alternative_models()
        
        if working_model:
            print(f"\n✅ MODELO FUNCIONAL ENCONTRADO: {working_model}")
            print(f"💡 Actualizar .env.local con: OPENROUTER_MODEL={working_model}")
        else:
            print(f"\n❌ NINGÚN MODELO FUNCIONAL ENCONTRADO")
    
    print(f"\n📋 RESULTADO FINAL:")
    print(f"   OpenRouter API: {'✅ FUNCIONANDO' if success else '❌ PROBLEMAS'}")
    print(f"   Recomendación: {'Usar configuración actual' if success else 'Cambiar modelo o verificar API key'}")