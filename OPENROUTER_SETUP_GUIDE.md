# Guía de Configuración de OpenRouter para ArcheoScope

## Fecha: 24 de Enero de 2026

---

## ⚠️ PROBLEMA ACTUAL

```
❌ ERROR HTTP 401
{
  "error": {
    "message": "User not found.",
    "code": 401
  }
}
```

**Diagnóstico**: La API key de OpenRouter es **inválida o expirada**.

---

## 🔧 SOLUCIÓN: Configurar OpenRouter Correctamente

### Paso 1: Crear Cuenta en OpenRouter

1. Ve a: https://openrouter.ai/
2. Haz clic en "Sign Up" (o "Sign In" si ya tienes cuenta)
3. Crea tu cuenta (puedes usar Google, GitHub, etc.)

### Paso 2: Generar API Key

1. Una vez logueado, ve a: https://openrouter.ai/keys
2. Haz clic en "Create Key"
3. Dale un nombre descriptivo: "ArcheoScope"
4. **COPIA LA API KEY** (solo se muestra una vez)
   - Formato: `sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Longitud: ~73 caracteres

### Paso 3: Agregar Créditos (Opcional)

**IMPORTANTE**: Algunos modelos son gratuitos, otros requieren créditos.

#### Modelos Gratuitos Recomendados:
- ✅ `google/gemini-2.0-flash-exp:free` (Recomendado)
- ✅ `google/gemini-flash-1.5:free`
- ✅ `meta-llama/llama-3.2-3b-instruct:free`

#### Si quieres usar modelos de pago:
1. Ve a: https://openrouter.ai/credits
2. Agrega créditos ($5 mínimo recomendado)
3. Usa modelos premium como `google/gemini-2.5-flash`

### Paso 4: Configurar `.env.local`

Abre el archivo `.env.local` en la raíz del proyecto y actualiza:

```bash
# OpenRouter API Configuration
OPENROUTER_API_KEY=sk-or-v1-TU_API_KEY_AQUI

# Modelo recomendado - Gemini 2.0 Flash Experimental (GRATUITO)
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free

# Configuración de providers
OLLAMA_ENABLED=false
OPENROUTER_ENABLED=true

# Configuración de timeouts
AI_TIMEOUT_SECONDS=30
AI_MAX_TOKENS=300
```

**⚠️ IMPORTANTE**: 
- Reemplaza `TU_API_KEY_AQUI` con tu API key real
- NO compartas tu API key con nadie
- NO hagas commit de `.env.local` (ya está en `.gitignore`)

### Paso 5: Verificar Configuración

Ejecuta el test de diagnóstico:

```bash
python test_openrouter_direct.py
```

**Resultado esperado**:
```
✅ ÉXITO!
💬 Mensaje de IA:
   La arqueología remota es el estudio de sitios arqueológicos...
✅ OPENROUTER FUNCIONA CORRECTAMENTE
```

### Paso 6: Reiniciar Backend

```bash
# Detener backend actual (Ctrl+C)
# Iniciar backend
python run_archeoscope.py
```

**Buscar en logs**:
```
✅ OpenRouter disponible con google/gemini-2.0-flash-exp:free
✅ Asistente de IA disponible y funcionando correctamente
```

---

## 🧪 TESTS DISPONIBLES

### Test 1: Diagnóstico Directo de OpenRouter
```bash
python test_openrouter_direct.py
```

**Qué hace**:
- Verifica API key
- Prueba conexión a OpenRouter
- Lista modelos disponibles
- Hace llamada de prueba
- Proporciona diagnóstico detallado

### Test 2: Endpoint de Test de IA
```bash
# Con backend corriendo
curl http://localhost:8002/test-ai
```

**Qué hace**:
- Verifica estado del asistente de IA
- Muestra configuración actual
- Hace llamada de prueba
- Proporciona diagnóstico si falla

### Test 3: Test de Calibración Completo
```bash
python test_calibration_4_reference_sites.py
```

**Qué hace**:
- Prueba análisis en 4 sitios de referencia
- Verifica que la IA genera explicaciones
- Valida todo el sistema end-to-end

---

## 🔍 DIAGNÓSTICO DE PROBLEMAS COMUNES

### Error 401: "User not found"
**Causa**: API key inválida o expirada
**Solución**: 
1. Ve a https://openrouter.ai/keys
2. Genera nueva API key
3. Actualiza `.env.local`

### Error 404: "Model not found"
**Causa**: Modelo no existe o nombre incorrecto
**Solución**:
1. Ve a https://openrouter.ai/models
2. Verifica nombre exacto del modelo
3. Usa modelo recomendado: `google/gemini-2.0-flash-exp:free`

### Error 402: "Insufficient credits"
**Causa**: Sin créditos para modelo de pago
**Solución**:
1. Usa modelo gratuito: `google/gemini-2.0-flash-exp:free`
2. O agrega créditos en https://openrouter.ai/credits

### Error 429: "Rate limit exceeded"
**Causa**: Demasiadas peticiones
**Solución**: Espera 1-2 minutos y vuelve a intentar

### Timeout
**Causa**: Conexión lenta o servicio no responde
**Solución**:
1. Verifica conexión a internet
2. Aumenta timeout en `.env.local`: `AI_TIMEOUT_SECONDS=60`
3. Verifica https://status.openrouter.ai/

### Connection Error
**Causa**: Sin internet o firewall bloqueando
**Solución**:
1. Verifica conexión: `ping openrouter.ai`
2. Verifica firewall/proxy
3. Intenta desde otra red

---

## 📊 MODELOS RECOMENDADOS

### Para Desarrollo (Gratuitos)
1. **google/gemini-2.0-flash-exp:free** ⭐ RECOMENDADO
   - Rápido
   - Gratuito
   - Buena calidad

2. **google/gemini-flash-1.5:free**
   - Alternativa estable
   - Gratuito

### Para Producción (De Pago)
1. **google/gemini-2.5-flash**
   - Más rápido
   - Mejor calidad
   - ~$0.075 por 1M tokens

2. **google/gemini-2.5-pro**
   - Máxima calidad
   - Más caro
   - ~$1.25 por 1M tokens

---

## 🔐 SEGURIDAD

### ✅ HACER:
- Mantener API key en `.env.local`
- Agregar `.env.local` a `.gitignore`
- Regenerar API key si se expone
- Usar modelos gratuitos para desarrollo

### ❌ NO HACER:
- Compartir API key públicamente
- Hacer commit de `.env.local`
- Hardcodear API key en código
- Usar API key de producción en desarrollo

---

## 📝 EJEMPLO DE `.env.local` COMPLETO

```bash
# ArcheoScope - Configuración de APIs
# NUNCA commitear este archivo - está en .gitignore

# OpenRouter API Configuration
OPENROUTER_API_KEY=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

# Modelo preferido - Gemini 2.0 Flash Experimental (GRATUITO)
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free

# Configuración de providers (cambiar a true para activar OpenRouter)
OLLAMA_ENABLED=false
OPENROUTER_ENABLED=true

# Configuración de timeouts
AI_TIMEOUT_SECONDS=30
AI_MAX_TOKENS=300

# Ollama Configuration (opcional - solo si usas Ollama local)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=phi4-mini-reasoning
```

---

## 🚀 FLUJO COMPLETO DE CONFIGURACIÓN

```bash
# 1. Generar API key en OpenRouter
# Ve a: https://openrouter.ai/keys

# 2. Actualizar .env.local
# Edita el archivo y pega tu API key

# 3. Test de diagnóstico
python test_openrouter_direct.py

# 4. Si el test pasa, reiniciar backend
python run_archeoscope.py

# 5. Verificar en logs
# Buscar: "✅ OpenRouter disponible"

# 6. Test del endpoint
curl http://localhost:8002/test-ai

# 7. Test completo del sistema
python test_calibration_4_reference_sites.py
```

---

## 📞 SOPORTE

### OpenRouter
- Documentación: https://openrouter.ai/docs
- Status: https://status.openrouter.ai/
- Discord: https://discord.gg/openrouter

### ArcheoScope
- Logs del backend: Buscar mensajes con "❌" o "ERROR"
- Test de diagnóstico: `python test_openrouter_direct.py`
- Endpoint de test: `curl http://localhost:8002/test-ai`

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] Cuenta creada en OpenRouter
- [ ] API key generada
- [ ] API key copiada a `.env.local`
- [ ] Modelo configurado (recomendado: `google/gemini-2.0-flash-exp:free`)
- [ ] `OPENROUTER_ENABLED=true` en `.env.local`
- [ ] Test de diagnóstico ejecutado: `python test_openrouter_direct.py`
- [ ] Test pasa con ✅ ÉXITO
- [ ] Backend reiniciado
- [ ] Logs muestran "✅ OpenRouter disponible"
- [ ] Endpoint `/test-ai` responde correctamente
- [ ] Sistema completo funciona

---

**Última actualización**: 2026-01-24  
**Versión**: 1.0.0  
**Estado**: 📋 GUÍA COMPLETA DE CONFIGURACIÓN
