# 🚀 Configuración de OpenRouter para el Avatar Conversacional

## ¿Qué es OpenRouter?

OpenRouter es una API unificada que te da acceso a múltiples modelos de IA (GPT-4, Claude, Gemini, Llama, Qwen, etc.) con una sola API key.

**Ventajas sobre Ollama:**
- ✅ No necesitas instalar nada localmente
- ✅ Modelos más potentes y rápidos
- ✅ Funciona desde cualquier dispositivo
- ✅ Tiene modelos GRATUITOS excelentes
- ✅ Respuestas más rápidas (servidores en la nube)

## 📝 Paso 1: Obtener API Key (GRATIS)

1. Ve a https://openrouter.ai
2. Haz clic en "Sign In" (puedes usar Google/GitHub)
3. Ve a https://openrouter.ai/keys
4. Haz clic en "Create Key"
5. Copia tu API key (empieza con `sk-or-v1-...`)

**Plan Gratuito incluye:**
- Modelos gratuitos ilimitados (Qwen, Llama, Mistral, etc.)
- $5 de crédito inicial para probar modelos premium
- Sin tarjeta de crédito requerida

## ⚙️ Paso 2: Configurar en el Proyecto

1. **Crea el archivo `.env.local` en la carpeta `viewer3d/`:**
   ```bash
   cd viewer3d
   cp .env.local.example .env.local
   ```

2. **Edita `.env.local` y agrega tu API key:**
   ```env
   NEXT_PUBLIC_OPENROUTER_API_KEY=sk-or-v1-tu-api-key-aqui
   ```

3. **Reinicia el servidor de desarrollo:**
   ```bash
   npm run dev
   ```

## 🎯 Paso 3: Probar el Avatar

1. Abre http://localhost:3000
2. Haz hard refresh: `Ctrl + Shift + R`
3. El botón 🗿 debería estar **verde** (conectado)
4. Abre el chat y habla con el Moai
5. Abre la consola (F12) para ver logs:
   ```
   ✅ OpenRouter conectado automáticamente
   🗿 Avatar conversacional inicializado con OpenRouter
   ```

## 📊 Modelos Disponibles

### Modelos GRATUITOS (Recomendados para empezar)

| Modelo | Descripción | Velocidad | Calidad |
|--------|-------------|-----------|---------|
| `qwen/qwen-2.5-7b-instruct:free` | **Por defecto** - Excelente balance | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| `meta-llama/llama-3.1-8b-instruct:free` | Muy bueno para conversación | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| `mistralai/mistral-7b-instruct:free` | Rápido y eficiente | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| `google/gemini-2.0-flash-exp:free` | Gratis temporalmente, muy potente | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ |

### Modelos de PAGO (Si quieres la mejor calidad)

| Modelo | Costo | Descripción |
|--------|-------|-------------|
| `openai/gpt-4o-mini` | $0.15/1M tokens | Excelente calidad/precio |
| `anthropic/claude-3.5-haiku` | $0.80/1M tokens | Muy rápido y preciso |
| `qwen/qwen-2.5-72b-instruct` | $0.35/1M tokens | Muy potente |

## 🔧 Cambiar de Modelo

Edita `viewer3d/components/ConversationalAvatar.tsx`:

```typescript
const llm = new OpenRouterIntegration({
  apiKey: openrouterApiKey,
  model: OPENROUTER_MODELS.GEMINI_2_FLASH, // Cambiar aquí
  temperature: 0.7,
  maxTokens: 300
})
```

O agrega en `.env.local`:
```env
NEXT_PUBLIC_OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free
```

## ⚡ Comparación de Tiempos de Respuesta

**Ollama (local):**
- Primera respuesta: ~3-5 segundos
- Respuestas siguientes: ~2-3 segundos
- Depende de tu hardware

**OpenRouter (nube):**
- Primera respuesta: ~1-2 segundos
- Respuestas siguientes: ~0.5-1 segundo
- Consistente, no depende de tu hardware

## 🐛 Troubleshooting

### Error: "OpenRouter no está disponible"
1. Verifica que tu API key esté correcta en `.env.local`
2. Asegúrate de que empiece con `sk-or-v1-`
3. Reinicia el servidor: `npm run dev`
4. Haz hard refresh en el navegador: `Ctrl + Shift + R`

### Error: "Rate limit exceeded"
- Estás usando demasiado el modelo gratuito
- Espera unos minutos o cambia a otro modelo gratuito
- Considera agregar créditos en OpenRouter

### El botón 🗿 está rojo
1. Abre la consola del navegador (F12)
2. Busca errores relacionados con OpenRouter
3. Verifica que `.env.local` exista y tenga la API key
4. Verifica tu conexión a internet

## 💰 Costos (Opcional)

Los modelos gratuitos son ilimitados, pero si quieres usar modelos premium:

**Ejemplo de uso típico:**
- 100 mensajes/día con GPT-4o-mini
- ~50,000 tokens/día
- Costo: ~$0.0075/día = $0.23/mes

**Muy económico** comparado con ChatGPT Plus ($20/mes)

## 🔐 Seguridad

**IMPORTANTE:** 
- Nunca compartas tu API key
- No la subas a GitHub (`.env.local` está en `.gitignore`)
- Si la expones accidentalmente, revócala en https://openrouter.ai/keys

## 📚 Recursos

- Documentación: https://openrouter.ai/docs
- Modelos disponibles: https://openrouter.ai/models
- Dashboard: https://openrouter.ai/activity
- Precios: https://openrouter.ai/models (ver columna "Price")

## ✅ Próximos Pasos

Una vez que funcione con OpenRouter:
1. Prueba diferentes modelos gratuitos
2. Compara tiempos de respuesta
3. Evalúa la calidad de las respuestas
4. Prueba las mejoras de voz implementadas
5. Si te gusta, considera agregar $5 para probar GPT-4o-mini
