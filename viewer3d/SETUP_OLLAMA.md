# 🤖 Setup Ollama para Avatar Conversacional

## 📥 Instalación de Ollama

### Windows
```bash
# Opción 1: Con winget
winget install Ollama.Ollama

# Opción 2: Descargar instalador
# https://ollama.ai/download
```

### Verificar instalación
```bash
ollama --version
```

---

## 🚀 Iniciar Ollama

```bash
# Iniciar servicio (dejar corriendo en una terminal)
ollama serve
```

**Importante**: Dejar esta terminal abierta mientras usas el avatar.

---

## 📦 Descargar Modelo Qwen3:1.7b

```bash
# Descargar modelo ultra-ligero (1.7B parámetros)
ollama pull qwen3:1.7b
```

### ¿Por qué Qwen3:1.7b?

✅ **Ultra-ligero**: Solo 1.7B parámetros (~1GB)  
✅ **Muy rápido**: Respuestas en <1 segundo  
✅ **Bajo consumo**: Funciona en laptops sin GPU  
✅ **Buena calidad**: Optimizado para conversación  
✅ **Multilenguaje**: Excelente en español  

### Comparación de modelos

| Modelo | Tamaño | RAM | Velocidad | Calidad |
|--------|--------|-----|-----------|---------|
| qwen3:1.7b | ~1.4GB | 2-4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| phi-2 | ~1.7GB | 4GB | ⚡⚡ | ⭐⭐⭐ |
| mistral:7b | ~4GB | 8GB | ⚡ | ⭐⭐⭐⭐ |
| llama3:8b | ~4.7GB | 8GB | ⚡ | ⭐⭐⭐⭐⭐ |

---

## ✅ Verificar que funciona

```bash
# Listar modelos instalados
ollama list

# Debería mostrar:
# NAME                ID              SIZE      MODIFIED
# qwen3:1.7b          abc123def       1.4 GB    2 minutes ago

# Probar el modelo
ollama run qwen3:1.7b "Hola, ¿cómo estás?"
```

---

## 🗿 Usar con el Avatar

1. **Iniciar Ollama**:
   ```bash
   ollama serve
   ```

2. **Abrir el visualizador**:
   ```bash
   cd viewer3d
   npm run dev
   ```

3. **En el navegador**:
   - Click en botón 🗿 (bottom-right)
   - Click en "Conectar"
   - ¡Habla con el Moai!

---

## 🔧 Troubleshooting

### Error: "Ollama no está disponible"

**Solución**:
```bash
# Verificar que Ollama está corriendo
curl http://localhost:11434/api/tags

# Si no responde, iniciar:
ollama serve
```

### Error: "Model not found"

**Solución**:
```bash
# Descargar el modelo
ollama pull qwen2.5:1.7b

# Verificar que se descargó
ollama list
```

### Respuestas muy lentas

**Solución**:
```bash
# Usar modelo más pequeño
ollama pull qwen2.5:0.5b

# O ajustar temperatura en el código
# temperature: 0.5  (más rápido, menos creativo)
```

### Respuestas en inglés

**Solución**: El system prompt ya está en español. Si responde en inglés:
```bash
# Probar con:
ollama run qwen2.5:1.7b "Responde siempre en español: ¿Qué es un Moai?"
```

---

## 🎯 Modelos Alternativos

Si `qwen2.5:1.7b` no funciona bien, prueba:

### Opción 1: Phi-2 (Microsoft)
```bash
ollama pull phi-2
```
- Tamaño: ~1.7GB
- Muy bueno para conversación
- Rápido en CPU

### Opción 2: Gemma:2b (Google)
```bash
ollama pull gemma:2b
```
- Tamaño: ~1.4GB
- Optimizado para diálogo
- Excelente en español

### Opción 3: TinyLlama
```bash
ollama pull tinyllama
```
- Tamaño: ~637MB
- El más ligero
- Calidad básica pero funcional

---

## 📊 Uso de Recursos

### Qwen2.5:1.7b
- **RAM**: 2-4GB
- **CPU**: Cualquier procesador moderno
- **GPU**: No requerida (pero ayuda)
- **Disco**: ~1GB

### Durante conversación
- **RAM adicional**: +500MB
- **CPU**: 20-40% (picos durante respuesta)
- **Latencia**: 500ms - 2s por respuesta

---

## 🚀 Optimización

### Para máxima velocidad
```bash
# Usar modelo más pequeño
ollama pull qwen2.5:0.5b

# O ajustar parámetros en código:
# temperature: 0.3  (menos creativo, más rápido)
# maxTokens: 100    (respuestas más cortas)
```

### Para mejor calidad
```bash
# Usar modelo más grande
ollama pull mistral:7b

# O ajustar parámetros:
# temperature: 0.8  (más creativo)
# maxTokens: 300    (respuestas más elaboradas)
```

---

## 📝 Comandos Útiles

```bash
# Ver modelos instalados
ollama list

# Eliminar modelo
ollama rm qwen2.5:1.7b

# Ver uso de recursos
ollama ps

# Detener Ollama
# Ctrl+C en la terminal donde corre ollama serve
```

---

## 🎓 Recursos

- [Ollama Website](https://ollama.ai/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Qwen2.5 Model Card](https://ollama.ai/library/qwen2.5)
- [Lista completa de modelos](https://ollama.ai/library)

---

## ✅ Checklist de Setup

- [ ] Ollama instalado (`ollama --version`)
- [ ] Ollama corriendo (`ollama serve`)
- [ ] Modelo descargado (`ollama list`)
- [ ] Modelo probado (`ollama run qwen2.5:1.7b "test"`)
- [ ] Visualizador corriendo (`npm run dev`)
- [ ] Avatar conectado (botón 🗿 → Conectar)
- [ ] Primera conversación exitosa

---

**¡Listo para conversar con el Moai!** 🗿✨
