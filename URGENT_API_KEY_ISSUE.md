# 🚨 URGENTE: Ambas API Keys Inválidas

## Fecha: 25 de Enero de 2026 - 01:40

---

## ❌ PROBLEMA CRÍTICO

**AMBAS API keys de OpenRouter están inválidas**:

### API KEY 1
```
Error: "User not found"
Estado: ❌ INVÁLIDA
```

### API KEY 2  
```
Error: "User not found"
Estado: ❌ INVÁLIDA
```

---

## 🔍 DIAGNÓSTICO

**Respuesta de OpenRouter**: `"User not found"`

Esto significa que:
1. ❌ Las cuentas asociadas fueron eliminadas
2. ❌ Las keys fueron revocadas
3. ❌ Las keys eran temporales y expiraron

---

## ✅ SOLUCIÓN INMEDIATA

### Opción 1: Generar Nueva API Key en OpenRouter (RECOMENDADO)

1. **Ve a**: https://openrouter.ai/
2. **Crea cuenta** (o inicia sesión)
3. **Ve a**: https://openrouter.ai/keys
4. **Crea nueva key**: Click en "Create Key"
5. **Copia la key** (formato: `sk-or-v1-xxxxx...`)
6. **Actualiza `.env.local`**:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-TU_NUEVA_KEY_AQUI
   OPENROUTER_MODEL=qwen/qwen3-coder:free
   ```
7. **Reinicia backend**: `python run_archeoscope.py`

### Opción 2: Usar Ollama Local (ALTERNATIVA)

Si no quieres usar OpenRouter, puedes usar Ollama localmente:

1. **Inicia Ollama**:
   ```bash
   ollama run phi4-mini-reasoning
   ```

2. **Actualiza `.env.local`**:
   ```bash
   OLLAMA_ENABLED=true
   OPENROUTER_ENABLED=false
   OLLAMA_MODEL=phi4-mini-reasoning
   OLLAMA_URL=http://localhost:11434
   ```

3. **Reinicia backend**: `python run_archeoscope.py`

---

## 🔧 CAMBIO TEMPORAL APLICADO

**Para que el sistema funcione AHORA**, he deshabilitado el bloqueo por IA:

- ✅ El sistema **SÍ funciona** sin IA
- ⚠️ Las explicaciones serán **limitadas** (sin interpretación de IA)
- ✅ La detección de anomalías **SÍ funciona**
- ✅ Los instrumentos **SÍ se recomiendan**
- ⚠️ NO habrá explicaciones arqueológicas detalladas

### Qué funciona SIN IA:
- ✅ Clasificación de ambientes
- ✅ Detección de anomalías espaciales
- ✅ Recomendación de instrumentos
- ✅ Análisis de persistencia temporal
- ✅ Coherencia geométrica
- ✅ Reconocimiento de sitios conocidos

### Qué NO funciona SIN IA:
- ❌ Explicaciones arqueológicas detalladas
- ❌ Interpretación científica de anomalías
- ❌ Razonamiento contextual
- ❌ Evaluación de confianza interpretativa

---

## 🚀 REINICIAR BACKEND

El backend se reiniciará automáticamente y ahora mostrará:

```
⚠️ ADVERTENCIA: ASISTENTE DE IA NO DISPONIBLE
El análisis continuará con explicaciones limitadas.
```

**En lugar de**:
```
❌ CRÍTICO: ASISTENTE DE IA NO DISPONIBLE
HTTP 503 Service Unavailable
```

---

## 📊 VERIFICAR ESTADO

### 1. Backend debe estar corriendo
```bash
# Verificar logs
# Buscar: "Application startup complete"
```

### 2. Probar análisis
- Ve al frontend
- Selecciona una región
- Click en "INVESTIGAR REGIÓN"
- **Debe funcionar** (sin error 503)

### 3. Verificar que funciona
```bash
curl -X POST http://localhost:8002/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "lat_min": 29.97,
    "lat_max": 29.98,
    "lon_min": 31.13,
    "lon_max": 31.14,
    "region_name": "Test"
  }'
```

**Debe responder HTTP 200** (no 503)

---

## 🎯 PRÓXIMOS PASOS

### URGENTE: Generar Nueva API Key

1. **Ahora mismo**: Ve a https://openrouter.ai/keys
2. **Genera nueva key**
3. **Actualiza `.env.local`**
4. **Reinicia backend**
5. **Verifica**: `python test_openrouter_direct.py`

### Resultado esperado:
```
✅ ÉXITO!
💬 Mensaje de IA:
   La arqueología remota es...
✅ OPENROUTER FUNCIONA CORRECTAMENTE
```

---

## 📝 RESUMEN

### Estado Actual:
- ❌ API KEY 1: Inválida ("User not found")
- ❌ API KEY 2: Inválida ("User not found")
- ✅ Sistema funcionando SIN IA (explicaciones limitadas)
- ✅ Detección de anomalías funcional
- ✅ Frontend accesible

### Acción Requerida:
1. **Generar nueva API key en OpenRouter**
2. **Actualizar `.env.local`**
3. **Reiniciar backend**
4. **Verificar con test**

### Tiempo Estimado:
- 5 minutos para generar nueva key
- 1 minuto para actualizar configuración
- 30 segundos para reiniciar backend
- **Total: ~7 minutos**

---

## 🔗 ENLACES ÚTILES

- **OpenRouter Keys**: https://openrouter.ai/keys
- **OpenRouter Modelos**: https://openrouter.ai/models
- **OpenRouter Docs**: https://openrouter.ai/docs

---

**Última actualización**: 2026-01-25 01:40  
**Estado**: 🚨 URGENTE - AMBAS API KEYS INVÁLIDAS  
**Sistema**: ✅ Funcionando sin IA (limitado)  
**Acción**: Generar nueva API key AHORA
