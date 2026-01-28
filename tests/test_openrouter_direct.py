#!/usr/bin/env python3
"""
Test directo de OpenRouter API para diagnosticar problemas
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar .env.local
load_dotenv('.env.local')

def test_openrouter():
    """Test directo de OpenRouter sin el sistema completo"""
    
    print("="*80)
    print("🧪 TEST DIRECTO DE OPENROUTER API")
    print("="*80)
    
    # Leer configuración
    api_key = os.getenv('OPENROUTER_API_KEY')
    model = os.getenv('OPENROUTER_MODEL', 'google/gemini-2.0-flash-exp:free')
    
    print(f"\n📋 CONFIGURACIÓN:")
    print(f"   API Key: {'✅ Configurada' if api_key else '❌ NO configurada'}")
    if api_key:
        print(f"   API Key (primeros 20 chars): {api_key[:20]}...")
        print(f"   API Key (longitud): {len(api_key)} caracteres")
    print(f"   Modelo: {model}")
    
    if not api_key:
        print("\n❌ ERROR: OPENROUTER_API_KEY no está configurada en .env.local")
        return False
    
    # Preparar request
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://archeoscope.app",
        "X-Title": "ArcheoScope"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Responde en UNA SOLA FRASE: ¿Qué es arqueología remota?"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    print(f"\n📡 LLAMANDO A OPENROUTER...")
    print(f"   URL: {url}")
    print(f"   Modelo: {model}")
    print(f"   Timeout: 30 segundos")
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\n📊 RESPUESTA:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ ÉXITO!")
            print(f"\n📝 Respuesta completa:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0]['message']['content']
                print(f"\n💬 Mensaje de IA:")
                print(f"   {message}")
            
            print(f"\n✅ OPENROUTER FUNCIONA CORRECTAMENTE")
            return True
            
        else:
            print(f"\n❌ ERROR HTTP {response.status_code}")
            print(f"\n📄 Respuesta del servidor:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(response.text)
            
            # Diagnóstico específico por código de error
            if response.status_code == 401:
                print(f"\n🔍 DIAGNÓSTICO:")
                print(f"   ❌ API Key inválida o expirada")
                print(f"   💡 Solución:")
                print(f"      1. Ve a https://openrouter.ai/keys")
                print(f"      2. Verifica que tu API key sea válida")
                print(f"      3. Genera una nueva si es necesario")
                print(f"      4. Actualiza OPENROUTER_API_KEY en .env.local")
                
            elif response.status_code == 404:
                print(f"\n🔍 DIAGNÓSTICO:")
                print(f"   ❌ Modelo '{model}' no encontrado")
                print(f"   💡 Solución:")
                print(f"      1. Ve a https://openrouter.ai/models")
                print(f"      2. Verifica que el modelo existe")
                print(f"      3. Modelos recomendados:")
                print(f"         - google/gemini-2.0-flash-exp:free (Gratuito)")
                print(f"         - google/gemini-flash-1.5 (Alternativa)")
                print(f"      4. Actualiza OPENROUTER_MODEL en .env.local")
                
            elif response.status_code == 429:
                print(f"\n🔍 DIAGNÓSTICO:")
                print(f"   ❌ Rate limit excedido")
                print(f"   💡 Solución: Espera unos minutos y vuelve a intentar")
                
            elif response.status_code == 402:
                print(f"\n🔍 DIAGNÓSTICO:")
                print(f"   ❌ Créditos insuficientes")
                print(f"   💡 Solución:")
                print(f"      1. Ve a https://openrouter.ai/credits")
                print(f"      2. Agrega créditos a tu cuenta")
                print(f"      3. O usa un modelo gratuito: google/gemini-2.0-flash-exp:free")
            
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n❌ TIMEOUT")
        print(f"   La petición tardó más de 30 segundos")
        print(f"\n🔍 DIAGNÓSTICO:")
        print(f"   ❌ Conexión muy lenta o servicio no responde")
        print(f"   💡 Solución:")
        print(f"      1. Verifica tu conexión a internet")
        print(f"      2. Intenta de nuevo en unos minutos")
        print(f"      3. Verifica https://status.openrouter.ai/")
        return False
        
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ ERROR DE CONEXIÓN")
        print(f"   {e}")
        print(f"\n🔍 DIAGNÓSTICO:")
        print(f"   ❌ No se puede conectar a OpenRouter")
        print(f"   💡 Solución:")
        print(f"      1. Verifica tu conexión a internet")
        print(f"      2. Verifica que no haya firewall bloqueando")
        print(f"      3. Intenta: ping openrouter.ai")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {e}")
        return False

def test_model_availability():
    """Verificar qué modelos están disponibles"""
    
    print("\n" + "="*80)
    print("🔍 VERIFICANDO MODELOS DISPONIBLES")
    print("="*80)
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ No se puede verificar sin API key")
        return
    
    url = "https://openrouter.ai/api/v1/models"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"📡 Consultando modelos disponibles...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            models_data = response.json()
            
            # Filtrar modelos de Gemini
            gemini_models = [
                m for m in models_data.get('data', [])
                if 'gemini' in m.get('id', '').lower()
            ]
            
            print(f"\n✅ Modelos Gemini disponibles ({len(gemini_models)}):")
            for model in gemini_models[:10]:  # Mostrar primeros 10
                model_id = model.get('id', 'unknown')
                pricing = model.get('pricing', {})
                prompt_price = pricing.get('prompt', 'N/A')
                
                is_free = prompt_price == '0' or prompt_price == 0
                free_tag = " 🆓 GRATUITO" if is_free else ""
                
                print(f"   - {model_id}{free_tag}")
            
            # Verificar si el modelo configurado existe
            configured_model = os.getenv('OPENROUTER_MODEL', 'google/gemini-2.0-flash-exp:free')
            model_exists = any(m.get('id') == configured_model for m in models_data.get('data', []))
            
            print(f"\n📋 Modelo configurado: {configured_model}")
            if model_exists:
                print(f"   ✅ Modelo existe y está disponible")
            else:
                print(f"   ❌ Modelo NO encontrado en la lista")
                print(f"   💡 Considera cambiar a: google/gemini-2.0-flash-exp:free")
        else:
            print(f"❌ Error consultando modelos: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🚀 Iniciando diagnóstico de OpenRouter...\n")
    
    # Test 1: Llamada básica
    success = test_openrouter()
    
    # Test 2: Verificar modelos disponibles
    if not success:
        test_model_availability()
    
    print("\n" + "="*80)
    if success:
        print("✅ DIAGNÓSTICO COMPLETO: OpenRouter funciona correctamente")
        print("   El problema debe estar en otra parte del sistema")
    else:
        print("❌ DIAGNÓSTICO COMPLETO: OpenRouter tiene problemas")
        print("   Revisa las soluciones sugeridas arriba")
    print("="*80 + "\n")
