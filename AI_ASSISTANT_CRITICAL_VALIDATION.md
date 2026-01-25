# Validación Crítica del Asistente de IA - ArcheoScope

## Fecha: 24 de Enero de 2026

---

## PROBLEMA IDENTIFICADO

El asistente de IA **ES CRÍTICO** para el análisis arqueológico, pero el sistema no informaba claramente al usuario cuando fallaba la conexión.

### Síntomas Anteriores
```
WARNING:ai.archaeological_assistant:❌ Ningún proveedor de IA disponible
INFO:ai.archaeological_assistant:  - Disponible: ❌
```

El sistema continuaba funcionando pero generaba errores HTTP 500 sin explicación clara.

---

## SOLUCIÓN IMPLEMENTADA

### 1. Mensajes de Error Mejorados en `archaeological_assistant.py`

**ANTES**:
```python
logger.warning("⚠️ Ningún proveedor de IA disponible")
logger.info("💡 El sistema detecta anomalías sin IA")
return False
```

**DESPUÉS**:
```python
logger.error("❌ CRÍTICO: Ningún proveedor de IA disponible")
logger.error("❌ El asistente de IA es NECESARIO para análisis arqueológico riguroso")
logger.error("❌ Por favor verifica:")
logger.error("   1. OPENROUTER_API_KEY está configurada en .env.local")
logger.error("   2. El modelo está disponible en OpenRouter")
logger.error("   3. Tienes conexión a internet")
logger.error("   4. O inicia Ollama con: ollama run phi4-mini-reasoning")
return False
```

### 2. Validación en Inicialización del Sistema (`main.py`)

Agregado en `initialize_system()`:

```python
# VALIDACIÓN CRÍTICA: Verificar que la IA está disponible
if not system_components['ai_assistant'].is_available:
    logger.error("="*80)
    logger.error("❌ CRÍTICO: ASISTENTE DE IA NO DISPONIBLE")
    logger.error("="*80)
    logger.error("El asistente de IA es NECESARIO para análisis arqueológico riguroso.")
    logger.error("")
    logger.error("SOLUCIONES:")
    logger.error("  1. Verifica OPENROUTER_API_KEY en .env.local")
    logger.error("  2. Verifica que el modelo esté disponible en OpenRouter")
    logger.error("  3. Verifica conexión a internet")
    logger.error("  4. O inicia Ollama: ollama run phi4-mini-reasoning")
    logger.error("")
    logger.error("El sistema continuará pero las explicaciones arqueológicas serán limitadas.")
    logger.error("="*80)
else:
    logger.info("✅ Asistente de IA disponible y funcionando correctamente")
```

### 3. Validación en Endpoint `/analyze`

Agregado al inicio del endpoint:

```python
# ⚠️ VALIDACIÓN CRÍTICA: Verificar que la IA está disponible
ai_assistant = system_components.get('ai_assistant')
if not ai_assistant or not ai_assistant.is_available:
    logger.error("=" * 80)
    logger.error("❌ CRÍTICO: ASISTENTE DE IA NO DISPONIBLE")
    logger.error("=" * 80)
    logger.error("El análisis arqueológico requiere el asistente de IA para interpretaciones rigurosas.")
    logger.error("")
    logger.error("SOLUCIONES:")
    logger.error("  1. Verifica OPENROUTER_API_KEY en .env.local")
    logger.error("  2. Verifica que el modelo esté disponible")
    logger.error("  3. Verifica conexión a internet")
    logger.error("  4. O inicia Ollama: ollama run phi4-mini-reasoning")
    logger.error("=" * 80)
    
    raise HTTPException(
        status_code=503,
        detail={
            "error": "AI_ASSISTANT_UNAVAILABLE",
            "message": "El asistente de IA no está disponible. El análisis arqueológico requiere IA para interpretaciones científicas rigurosas.",
            "solutions": [
                "Verifica OPENROUTER_API_KEY en .env.local",
                "Verifica que el modelo esté disponible en OpenRouter",
                "Verifica conexión a internet",
                "O inicia Ollama: ollama run phi4-mini-reasoning"
            ],
            "impact": "No se pueden generar explicaciones arqueológicas científicas sin IA"
        }
    )
```

### 4. Mensajes de Diagnóstico Mejorados

El método `_check_availability()` ahora proporciona diagnósticos específicos:

```python
if response.status_code == 200:
    logger.info(f"✅ OpenRouter disponible con {self.openrouter_model}")
    return True
elif response.status_code == 401:
    logger.warning(f"⚠️ OpenRouter: API key inválida o expirada")
elif response.status_code == 404:
    logger.warning(f"⚠️ OpenRouter: Modelo {self.openrouter_model} no encontrado")
else:
    logger.warning(f"⚠️ OpenRouter error: HTTP {response.status_code}")
```

Y para errores de conexión:

```python
except requests.exceptions.Timeout:
    logger.warning(f"⚠️ OpenRouter: Timeout (red lenta o servicio no responde)")
except requests.exceptions.ConnectionError:
    logger.warning(f"⚠️ OpenRouter: Error de conexión (sin internet?)")
```

---

## CONFIGURACIÓN CORRECTA

### Archivo `.env.local`

```bash
# OpenRouter API Configuration
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx

# Modelo recomendado - Gemini 2.0 Flash Experimental (gratuito)
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free

# Configuración de providers
OLLAMA_ENABLED=false
OPENROUTER_ENABLED=true

# Configuración de timeouts
AI_TIMEOUT_SECONDS=30
AI_MAX_TOKENS=300
```

### Modelos Recomendados en OpenRouter

1. **google/gemini-2.0-flash-exp:free** (Recomendado - Gratuito)
2. **google/gemini-flash-1.5** (Alternativa)
3. **anthropic/claude-3-haiku** (Alternativa de pago)

---

## RESULTADO

### Mensajes Claros al Usuario

**Al iniciar el sistema**:
```
================================================================================
❌ CRÍTICO: ASISTENTE DE IA NO DISPONIBLE
================================================================================
El asistente de IA es NECESARIO para análisis arqueológico riguroso.

SOLUCIONES:
  1. Verifica OPENROUTER_API_KEY en .env.local
  2. Verifica que el modelo esté disponible en OpenRouter
  3. Verifica conexión a internet
  4. O inicia Ollama: ollama run phi4-mini-reasoning

El sistema continuará pero las explicaciones arqueológicas serán limitadas.
================================================================================
```

**Al intentar analizar sin IA**:
```
HTTP 503 Service Unavailable
{
  "error": "AI_ASSISTANT_UNAVAILABLE",
  "message": "El asistente de IA no está disponible...",
  "solutions": [...],
  "impact": "No se pueden generar explicaciones arqueológicas científicas sin IA"
}
```

---

## VERIFICACIÓN

### Paso 1: Verificar Estado de la IA

```bash
python run_archeoscope.py
```

Buscar en los logs:
- ✅ `✅ OpenRouter disponible con google/gemini-2.0-flash-exp:free`
- ✅ `✅ Asistente de IA disponible y funcionando correctamente`

O:
- ❌ `❌ CRÍTICO: ASISTENTE DE IA NO DISPONIBLE`

### Paso 2: Probar Endpoint

```bash
curl -X POST http://localhost:8002/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "lat_min": 29.97,
    "lat_max": 29.98,
    "lon_min": 31.13,
    "lon_max": 31.14,
    "region_name": "Test Giza"
  }'
```

**Si IA no disponible**: HTTP 503 con mensaje claro
**Si IA disponible**: HTTP 200 con análisis completo

---

## CAUSAS COMUNES DE FALLO

### 1. API Key Inválida o Expirada
**Síntoma**: `⚠️ OpenRouter: API key inválida o expirada`
**Solución**: Regenerar API key en https://openrouter.ai/keys

### 2. Modelo No Encontrado
**Síntoma**: `⚠️ OpenRouter: Modelo google/gemini-xxx no encontrado`
**Solución**: Cambiar a modelo disponible en `.env.local`

### 3. Sin Conexión a Internet
**Síntoma**: `⚠️ OpenRouter: Error de conexión (sin internet?)`
**Solución**: Verificar conexión de red

### 4. Timeout
**Síntoma**: `⚠️ OpenRouter: Timeout (red lenta o servicio no responde)`
**Solución**: Aumentar `AI_TIMEOUT_SECONDS` en `.env.local`

### 5. Ollama No Corriendo
**Síntoma**: `⚠️ Ollama: No está corriendo en http://localhost:11434`
**Solución**: `ollama run phi4-mini-reasoning`

---

## IMPACTO

### SIN IA (Antes)
- ❌ Errores HTTP 500 sin explicación
- ❌ Usuario confundido sobre qué falló
- ❌ Sistema parecía roto

### CON IA (Después)
- ✅ Mensajes de error claros y accionables
- ✅ Usuario sabe exactamente qué hacer
- ✅ Sistema informa estado correctamente

---

## ARCHIVOS MODIFICADOS

1. `backend/ai/archaeological_assistant.py`
   - Mensajes de error mejorados
   - Diagnósticos específicos por tipo de error

2. `backend/api/main.py`
   - Validación en `initialize_system()`
   - Validación en endpoint `/analyze`
   - HTTP 503 con detalles cuando IA no disponible

3. `.env.local`
   - Modelo actualizado a `google/gemini-2.0-flash-exp:free`

---

## CONCLUSIÓN

El asistente de IA es **CRÍTICO** para ArcheoScope. Ahora el sistema:

1. ✅ Informa claramente cuando la IA no está disponible
2. ✅ Proporciona soluciones específicas al usuario
3. ✅ Bloquea análisis si la IA no funciona (HTTP 503)
4. ✅ Muestra diagnósticos detallados en logs

**El usuario siempre sabrá por qué falla y cómo solucionarlo.**

---

**Última actualización**: 2026-01-24  
**Versión**: 1.0.0  
**Estado**: ✅ VALIDACIÓN CRÍTICA IMPLEMENTADA
