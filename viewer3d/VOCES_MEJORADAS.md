# 🎙️ Sistema de Voces Mejorado

## ✅ Mejoras Implementadas (Gratis - Web Speech API)

### 1. Selección Inteligente de Voces
El sistema ahora busca automáticamente las mejores voces disponibles en tu sistema:

**Prioridad de voces:**
1. **Google** (mejor calidad si está disponible)
   - Google español
   - Google español de Estados Unidos
   - Google español de España
   - Google español de México

2. **Microsoft** (buena calidad en Windows)
   - Microsoft Helena - Spanish (Spain)
   - Microsoft Pablo - Spanish (Spain)
   - Microsoft Sabina - Spanish (Mexico)
   - Microsoft Raul - Spanish (Mexico)

3. **Apple** (buena calidad en macOS/iOS)
   - Monica, Jorge, Juan, Diego, Paulina

### 2. Procesamiento de Texto para Mejor Prosodia
- **Pausas naturales** después de puntuación (., , ; :)
- **Énfasis** en palabras clave (ancestral, piedra, viento, mar, tiempo, sabiduría)
- **Limpieza** de espacios múltiples

### 3. Parámetros Optimizados
- **Rate:** 0.9 (ligeramente más lento, más contemplativo)
- **Pitch:** 0.85 (grave pero natural)
- **Volume:** 1.0 (volumen completo)

### 4. Logging de Voces
Abre la consola del navegador (F12) para ver qué voz está usando:
```
🎙️ Voz: Microsoft Pablo - Spanish (Spain) (es-ES)
```

## 🚀 Cómo Mejorar Aún Más (Opcional)

### Opción 1: Instalar Voces de Mejor Calidad en tu Sistema

**Windows:**
1. Ve a Configuración → Hora e idioma → Idioma
2. Agrega "Español" si no lo tienes
3. Click en Español → Opciones
4. Descarga "Voz" (Microsoft Pablo o Helena son excelentes)

**macOS:**
1. Ve a Preferencias del Sistema → Accesibilidad → Contenido Hablado
2. Click en "Voz del sistema"
3. Descarga voces en español (Monica, Jorge, Juan son muy buenas)

**Linux:**
1. Instala `espeak-ng` o `festival` con voces en español
2. O usa Google Chrome que tiene voces integradas

### Opción 2: Usar ElevenLabs (Voz Premium de IA) 🌟

ElevenLabs ofrece las voces más realistas del mercado, indistinguibles de humanos reales.

**Pasos:**

1. **Crear cuenta en ElevenLabs:**
   - Ve a https://elevenlabs.io
   - Regístrate (tienen plan gratuito con 10,000 caracteres/mes)
   - Copia tu API Key

2. **Configurar en el código:**
   ```typescript
   // En ConversationalAvatar.tsx, reemplaza la inicialización de voz:
   
   import { VoiceSystem, ELEVENLABS_VOICES } from '@/ai/voice-system'
   
   const voiceSystem = new VoiceSystem({
     engine: 'elevenlabs',
     elevenLabsApiKey: 'tu-api-key-aqui',
     elevenLabsVoiceId: ELEVENLABS_VOICES.ADAM // Voz grave y autoritaria
   })
   
   // Usar en lugar de speak():
   await voiceSystem.speak(text, 
     () => setIsSpeaking(true),
     () => setIsSpeaking(false)
   )
   ```

3. **Voces recomendadas para el Moai:**
   - **ADAM:** Masculina, grave, autoritaria (mejor para Moai)
   - **ANTONI:** Masculina, cálida, narrativa
   - **ARNOLD:** Masculina, profunda, resonante
   - **CALLUM:** Masculina, suave, contemplativa
   - **JOSEPH:** Masculina, madura, sabia

**Costo:**
- Plan gratuito: 10,000 caracteres/mes (~100 mensajes)
- Plan Starter: $5/mes - 30,000 caracteres
- Plan Creator: $22/mes - 100,000 caracteres

## 🎯 Resultado Esperado

Con las mejoras implementadas, la voz debería sonar:
- ✅ Más fluida (mejor selección de voz)
- ✅ Más natural (pausas y énfasis)
- ✅ Menos robótica (parámetros optimizados)
- ✅ Más contemplativa (rate y pitch ajustados)

## 🐛 Troubleshooting

**Si la voz sigue sonando robótica:**
1. Verifica en la consola qué voz está usando
2. Instala voces de mejor calidad en tu sistema (ver arriba)
3. Prueba en diferentes navegadores (Chrome suele tener mejores voces)
4. Considera usar ElevenLabs para calidad profesional

**Si no hay voz:**
1. Verifica que el botón 🔊 esté activado (no 🔇)
2. Verifica que Ollama esté conectado (botón verde)
3. Revisa la consola del navegador para errores
4. Asegúrate de que tu navegador tenga permisos de audio
