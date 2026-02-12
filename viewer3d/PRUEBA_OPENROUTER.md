# 🧪 Prueba de OpenRouter - Guía Rápida

## 🎯 Objetivo
Probar OpenRouter como alternativa a Ollama para el avatar conversacional y evaluar:
- ⏱️ Tiempos de respuesta
- 🎙️ Calidad de voz mejorada
- 💬 Calidad de respuestas del modelo

## 📋 Pasos para Probar

### 1. Obtener API Key (2 minutos)
1. Ve a https://openrouter.ai
2. Sign in con Google/GitHub
3. Ve a https://openrouter.ai/keys
4. Crea una key
5. Copia la key (empieza con `sk-or-v1-...`)

### 2. Configurar (1 minuto)
```bash
cd viewer3d
cp .env.local.example .env.local
```

Edita `.env.local`:
```env
NEXT_PUBLIC_OPENROUTER_API_KEY=sk-or-v1-tu-api-key-aqui
```

### 3. Prueba Rápida desde Terminal (Opcional)
```bash
# Exportar API key
export OPENROUTER_API_KEY=sk-or-v1-tu-api-key-aqui

# Ejecutar test
node test-openrouter.js
```

Deberías ver:
```
✅ Respuesta recibida!
⏱️  Tiempo: 1234ms
💬 Respuesta del Moai:
────────────────────────────────────────────────────────────
Saludos, viajero. Soy un Moai ancestral...
────────────────────────────────────────────────────────────
```

### 4. Reiniciar Servidor
```bash
# Detener servidor actual (Ctrl+C)
npm run dev
```

### 5. Probar en el Navegador
1. Abre http://localhost:3000
2. Hard refresh: `Ctrl + Shift + R`
3. Verifica que el botón 🗿 esté **verde**
4. Abre la consola (F12) y busca:
   ```
   ✅ OpenRouter conectado automáticamente
   🗿 Avatar conversacional inicializado con OpenRouter
   ```
5. Click en 🗿 → Habla con el Moai
6. Observa:
   - ⏱️ Tiempo de respuesta (debería ser ~1-2 segundos)
   - 🎙️ Calidad de voz (con las mejoras implementadas)
   - 💬 Calidad de respuesta

## 📊 Comparación Esperada

| Métrica | Ollama (local) | OpenRouter (nube) |
|---------|----------------|-------------------|
| Primera respuesta | 3-5 seg | 1-2 seg |
| Respuestas siguientes | 2-3 seg | 0.5-1 seg |
| Requiere instalación | ✅ Sí | ❌ No |
| Funciona offline | ✅ Sí | ❌ No |
| Depende de hardware | ✅ Sí | ❌ No |
| Modelos disponibles | ~10 | 100+ |
| Costo | Gratis | Gratis + Premium |

## 🎙️ Mejoras de Voz Implementadas

Las mejoras de voz funcionan con ambos (Ollama y OpenRouter):

1. **Selección inteligente de voces**
   - Busca automáticamente las mejores voces del sistema
   - Prioriza: Google > Microsoft > Apple

2. **Procesamiento de texto**
   - Pausas naturales después de puntuación
   - Énfasis en palabras clave (ancestral, piedra, viento, etc.)

3. **Parámetros optimizados**
   - Rate: 0.9 (más fluido)
   - Pitch: 0.85 (grave pero natural)
   - Volume: 1.0

4. **Logging**
   - Abre consola (F12) para ver qué voz está usando:
   ```
   🎙️ Voz: Microsoft Pablo - Spanish (Spain) (es-ES)
   ```

## 🐛 Troubleshooting

### Botón 🗿 está rojo
1. Verifica `.env.local` existe y tiene la API key
2. Verifica que la API key sea correcta
3. Reinicia el servidor: `npm run dev`
4. Hard refresh: `Ctrl + Shift + R`
5. Revisa consola (F12) para errores

### Voz sigue sonando robótica
1. Verifica en consola qué voz está usando
2. Instala voces de mejor calidad en tu sistema:
   - Windows: Configuración → Idioma → Español → Opciones → Descargar voz
   - macOS: Preferencias → Accesibilidad → Contenido Hablado
3. Prueba en Chrome (suele tener mejores voces)
4. Considera usar ElevenLabs (ver VOCES_MEJORADAS.md)

### Error: "Rate limit exceeded"
- Estás usando mucho el modelo gratuito
- Espera unos minutos
- O cambia a otro modelo gratuito en el código

## 📝 Feedback a Reportar

Después de probar, reporta:

1. **Tiempos de respuesta:**
   - Primera respuesta: ___ segundos
   - Respuestas siguientes: ___ segundos

2. **Calidad de voz:**
   - ¿Suena más natural? (Sí/No)
   - ¿Qué voz está usando? (ver consola)
   - ¿Sigue sonando robótica? (Sí/No)

3. **Calidad de respuestas:**
   - ¿Las respuestas son coherentes? (Sí/No)
   - ¿Mantiene la personalidad del Moai? (Sí/No)
   - ¿Es mejor/peor que Ollama? (Mejor/Igual/Peor)

4. **Experiencia general:**
   - ¿Prefieres OpenRouter o Ollama? (OpenRouter/Ollama)
   - ¿Por qué?

## 🚀 Próximos Pasos

Si OpenRouter funciona bien:
1. ✅ Mantener como opción por defecto
2. ✅ Agregar selector de modelo en UI
3. ✅ Implementar sistema de credenciales encriptadas en BD
4. ✅ Agregar métricas de uso y costos
5. ✅ Probar modelos premium (GPT-4o-mini, Claude 3.5 Haiku)

## 📚 Documentación Completa

- Setup completo: `OPENROUTER_SETUP.md`
- Mejoras de voz: `VOCES_MEJORADAS.md`
- Actualizar navegador: `ACTUALIZAR_NAVEGADOR.md`
