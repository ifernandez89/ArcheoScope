import requests
import json

# Test simple de OpenRouter
api_key = "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"

print("Testing OpenRouter API...")

# Test 1: Verificar modelos
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
    print(f"Models API Status: {response.status_code}")
    
    if response.status_code == 200:
        models = response.json()
        model_ids = [m['id'] for m in models.get('data', [])]
        print(f"Total models: {len(model_ids)}")
        
        # Buscar modelos Gemini
        gemini_models = [m for m in model_ids if 'gemini' in m.lower()]
        print(f"Gemini models: {gemini_models[:3]}")
        
        # Verificar modelo específico
        target_model = "google/gemini-2.5-flash-preview-09-2025"
        if target_model in model_ids:
            print(f"✅ Target model {target_model} available")
        else:
            print(f"❌ Target model {target_model} NOT available")
            if gemini_models:
                print(f"💡 Alternative: {gemini_models[0]}")
    else:
        print(f"Error: {response.text[:200]}")

except Exception as e:
    print(f"Error: {e}")

# Test 2: Chat completion simple
print("\nTesting chat completion...")

payload = {
    "model": "google/gemini-flash-1.5",  # Modelo más común
    "messages": [
        {"role": "user", "content": "Say 'Hello' in Spanish"}
    ],
    "max_tokens": 10
}

try:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=15
    )
    
    print(f"Chat API Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result:
            content = result['choices'][0]['message']['content']
            print(f"✅ Response: {content}")
        else:
            print(f"No choices in response: {result}")
    else:
        print(f"Error: {response.text[:200]}")
        
except Exception as e:
    print(f"Error: {e}")

print("Test completed.")