import requests
import json

# Test del modelo específico configurado
api_key = "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"
model = "google/gemini-2.5-flash-preview-09-2025"

print(f"Testing configured model: {model}")

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
            "content": "Analiza brevemente: se detectaron anomalías espaciales persistentes en una región. ¿Interpretación arqueológica?"
        }
    ],
    "max_tokens": 100,
    "temperature": 0.3
}

try:
    print("Sending request...")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print(f"✅ SUCCESS!")
            print(f"Response: {content}")
            
            if 'usage' in result:
                usage = result['usage']
                print(f"Tokens used: {usage.get('total_tokens', 'N/A')}")
        else:
            print(f"No content in response: {result}")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Si falla, probar con Gemini 3 Flash Preview
        print(f"\nTrying alternative: google/gemini-3-flash-preview")
        payload['model'] = "google/gemini-3-flash-preview"
        
        response2 = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Alternative Status: {response2.status_code}")
        if response2.status_code == 200:
            result2 = response2.json()
            if 'choices' in result2:
                content2 = result2['choices'][0]['message']['content']
                print(f"✅ Alternative SUCCESS!")
                print(f"Response: {content2}")

except Exception as e:
    print(f"Error: {e}")

print("Test completed.")