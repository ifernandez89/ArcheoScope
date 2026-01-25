#!/usr/bin/env python3
"""
Verificador de Estado de API Keys de OpenRouter
Verifica validez, límites, créditos y fecha de expiración
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar .env.local
load_dotenv('.env.local')

def check_api_key_status(api_key: str, key_name: str):
    """
    Verificar estado completo de una API key de OpenRouter
    
    Información que obtenemos:
    - Validez de la key
    - Límites de uso (rate limits)
    - Créditos disponibles
    - Información de la cuenta
    """
    
    print("="*80)
    print(f"🔑 VERIFICANDO: {key_name}")
    print("="*80)
    
    if not api_key:
        print(f"❌ {key_name} no está configurada")
        return None
    
    print(f"📋 API Key: {api_key[:20]}...{api_key[-10:]}")
    print(f"📏 Longitud: {len(api_key)} caracteres")
    
    # Test 1: Verificar validez con llamada simple
    print(f"\n🧪 TEST 1: Verificando validez de la key...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://archeoscope.app",
        "X-Title": "ArcheoScope"
    }
    
    # Llamada de prueba mínima
    test_payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 5
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=test_payload,
            timeout=15
        )
        
        if response.status_code == 200:
            print(f"✅ API Key VÁLIDA y FUNCIONAL")
            
            # Extraer información de headers
            print(f"\n📊 INFORMACIÓN DE USO:")
            
            # Rate limits (si están disponibles en headers)
            rate_limit_requests = response.headers.get('x-ratelimit-limit-requests')
            rate_limit_remaining = response.headers.get('x-ratelimit-remaining-requests')
            rate_limit_reset = response.headers.get('x-ratelimit-reset-requests')
            
            if rate_limit_requests:
                print(f"   Límite de requests: {rate_limit_requests}")
                print(f"   Requests restantes: {rate_limit_remaining}")
                if rate_limit_reset:
                    reset_time = datetime.fromtimestamp(int(rate_limit_reset))
                    print(f"   Reset en: {reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Información de la respuesta
            result = response.json()
            
            # Uso de tokens
            usage = result.get('usage', {})
            if usage:
                print(f"\n💰 USO EN ESTA LLAMADA:")
                print(f"   Tokens prompt: {usage.get('prompt_tokens', 0)}")
                print(f"   Tokens completion: {usage.get('completion_tokens', 0)}")
                print(f"   Tokens totales: {usage.get('total_tokens', 0)}")
            
            # Modelo usado
            model_used = result.get('model', 'unknown')
            print(f"\n🤖 Modelo usado: {model_used}")
            
            return {
                "valid": True,
                "status_code": 200,
                "rate_limit": {
                    "limit": rate_limit_requests,
                    "remaining": rate_limit_remaining,
                    "reset": rate_limit_reset
                },
                "usage": usage,
                "model": model_used
            }
            
        elif response.status_code == 401:
            print(f"❌ API Key INVÁLIDA o EXPIRADA")
            error_data = response.json()
            print(f"   Error: {error_data.get('error', {}).get('message', 'Unknown')}")
            print(f"\n💡 SOLUCIÓN:")
            print(f"   1. Ve a https://openrouter.ai/keys")
            print(f"   2. Verifica que la key existe")
            print(f"   3. Genera una nueva si es necesario")
            return {"valid": False, "status_code": 401, "error": "Invalid or expired"}
            
        elif response.status_code == 402:
            print(f"⚠️ SIN CRÉDITOS SUFICIENTES")
            error_data = response.json()
            print(f"   Error: {error_data.get('error', {}).get('message', 'Unknown')}")
            print(f"\n💡 SOLUCIÓN:")
            print(f"   1. Ve a https://openrouter.ai/credits")
            print(f"   2. Agrega créditos a tu cuenta")
            print(f"   3. O usa modelos gratuitos: google/gemini-2.0-flash-exp:free")
            return {"valid": True, "status_code": 402, "error": "Insufficient credits"}
            
        elif response.status_code == 429:
            print(f"⚠️ RATE LIMIT EXCEDIDO")
            error_data = response.json()
            print(f"   Error: {error_data.get('error', {}).get('message', 'Unknown')}")
            print(f"\n💡 SOLUCIÓN:")
            print(f"   Espera unos minutos antes de volver a intentar")
            return {"valid": True, "status_code": 429, "error": "Rate limit exceeded"}
            
        else:
            print(f"❌ ERROR HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Response: {response.text[:200]}")
            return {"valid": False, "status_code": response.status_code}
            
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT - La petición tardó demasiado")
        return {"valid": None, "error": "Timeout"}
        
    except requests.exceptions.ConnectionError:
        print(f"❌ ERROR DE CONEXIÓN - No se puede conectar a OpenRouter")
        return {"valid": None, "error": "Connection error"}
        
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        return {"valid": None, "error": str(e)}

def get_account_info(api_key: str):
    """
    Obtener información de la cuenta (créditos, límites, etc.)
    Nota: OpenRouter puede no exponer toda esta info públicamente
    """
    
    print(f"\n🔍 Intentando obtener información de la cuenta...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Intentar obtener info de créditos (endpoint puede no estar disponible)
    try:
        # Este endpoint puede no existir o requerir permisos especiales
        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Información de cuenta obtenida:")
            print(json.dumps(data, indent=2))
            return data
        else:
            print(f"⚠️ No se pudo obtener información de cuenta (HTTP {response.status_code})")
            print(f"   Esto es normal - OpenRouter no siempre expone esta información")
            return None
            
    except Exception as e:
        print(f"⚠️ No se pudo obtener información de cuenta: {e}")
        print(f"   Esto es normal - OpenRouter no siempre expone esta información")
        return None

def check_model_availability(api_key: str, model: str):
    """Verificar si un modelo específico está disponible"""
    
    print(f"\n🤖 Verificando disponibilidad del modelo: {model}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://archeoscope.app",
        "X-Title": "ArcheoScope"
    }
    
    test_payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Test"}],
        "max_tokens": 5
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=test_payload,
            timeout=15
        )
        
        if response.status_code == 200:
            print(f"✅ Modelo '{model}' DISPONIBLE y FUNCIONAL")
            return True
        elif response.status_code == 404:
            print(f"❌ Modelo '{model}' NO ENCONTRADO")
            print(f"   Verifica el nombre en: https://openrouter.ai/models")
            return False
        else:
            print(f"⚠️ Error verificando modelo: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Verificar todas las API keys configuradas"""
    
    print("\n" + "="*80)
    print("🔐 VERIFICADOR DE ESTADO DE API KEYS - OPENROUTER")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Leer configuración
    api_key1 = os.getenv('OPENROUTER_API_KEY')
    api_key2 = os.getenv('OPENROUTER_API_KEY2')
    model1 = os.getenv('OPENROUTER_MODEL', 'google/gemini-2.0-flash-exp:free')
    model2 = os.getenv('OPENROUTER_MODEL2', 'qwen/qwen3-coder:free')
    
    results = {}
    
    # Verificar API Key 1
    if api_key1:
        print(f"\n{'='*80}")
        print(f"API KEY 1 (Principal)")
        print(f"{'='*80}")
        results['key1'] = check_api_key_status(api_key1, "OPENROUTER_API_KEY")
        
        if results['key1'] and results['key1'].get('valid'):
            # Verificar modelo configurado
            check_model_availability(api_key1, model1)
            
            # Intentar obtener info de cuenta
            get_account_info(api_key1)
    else:
        print(f"\n⚠️ OPENROUTER_API_KEY no configurada")
    
    # Verificar API Key 2
    if api_key2:
        print(f"\n{'='*80}")
        print(f"API KEY 2 (Secundaria)")
        print(f"{'='*80}")
        results['key2'] = check_api_key_status(api_key2, "OPENROUTER_API_KEY2")
        
        if results['key2'] and results['key2'].get('valid'):
            # Verificar modelo configurado
            check_model_availability(api_key2, model2)
            
            # Intentar obtener info de cuenta
            get_account_info(api_key2)
    else:
        print(f"\n⚠️ OPENROUTER_API_KEY2 no configurada")
    
    # Resumen final
    print(f"\n{'='*80}")
    print(f"📊 RESUMEN FINAL")
    print(f"{'='*80}")
    
    if api_key1:
        key1_status = results.get('key1', {})
        if key1_status.get('valid') == True:
            print(f"✅ API KEY 1: VÁLIDA y FUNCIONAL")
            print(f"   Modelo: {model1}")
        elif key1_status.get('valid') == False:
            print(f"❌ API KEY 1: INVÁLIDA o CON PROBLEMAS")
        else:
            print(f"⚠️ API KEY 1: NO SE PUDO VERIFICAR")
    
    if api_key2:
        key2_status = results.get('key2', {})
        if key2_status.get('valid') == True:
            print(f"✅ API KEY 2: VÁLIDA y FUNCIONAL")
            print(f"   Modelo: {model2}")
        elif key2_status.get('valid') == False:
            print(f"❌ API KEY 2: INVÁLIDA o CON PROBLEMAS")
        else:
            print(f"⚠️ API KEY 2: NO SE PUDO VERIFICAR")
    
    # Información sobre expiración
    print(f"\n{'='*80}")
    print(f"⏰ INFORMACIÓN SOBRE EXPIRACIÓN DE API KEYS")
    print(f"{'='*80}")
    print(f"")
    print(f"📌 IMPORTANTE:")
    print(f"   - Las API keys de OpenRouter NO tienen fecha de expiración automática")
    print(f"   - Las keys son válidas hasta que TÚ las revokes manualmente")
    print(f"   - Puedes revocar keys en: https://openrouter.ai/keys")
    print(f"")
    print(f"⚠️ LÍMITES:")
    print(f"   - Rate limits: Dependen de tu plan (free/paid)")
    print(f"   - Créditos: Si usas modelos de pago, necesitas créditos")
    print(f"   - Modelos gratuitos: Sin límite de créditos, solo rate limits")
    print(f"")
    print(f"💡 RECOMENDACIÓN:")
    print(f"   - Ejecuta este script periódicamente para verificar estado")
    print(f"   - Monitorea tus créditos en: https://openrouter.ai/credits")
    print(f"   - Usa modelos gratuitos para desarrollo")
    print(f"")
    print(f"🔄 PRÓXIMA VERIFICACIÓN RECOMENDADA:")
    print(f"   - Ejecuta este script cada semana")
    print(f"   - O cuando notes problemas con la IA")
    print(f"")
    print(f"="*80)
    
    return results

if __name__ == "__main__":
    results = main()
    
    # Guardar resultados en archivo
    output_file = f"api_keys_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    print(f"="*80 + "\n")
