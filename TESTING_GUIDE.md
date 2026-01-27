# 🧪 ArcheoScope - Guía de Pruebas
## Frontend Integrado v2.2

**Fecha**: 27 de Enero, 2026  
**Status**: ✅ Sistema listo para pruebas

---

## 🚀 **INICIO RÁPIDO**

### 1. Abrir el Frontend
```
http://localhost:8080
```

El navegador se abrirá automáticamente con el nuevo frontend integrado.

---

## 🎯 **FLUJO DE USO (SIMPLIFICADO)**

### **Paso 1: Ingresar Coordenadas**
Tienes 2 opciones:

**Opción A: Escribir manualmente**
- Lat: `64.2`
- Lon: `-51.7`
- Región: `Nuuk, Groenlandia`

**Opción B: Click en el mapa**
- Haz click en cualquier punto del mapa
- Las coordenadas se llenan automáticamente

### **Paso 2: Analizar**
- Click en el botón **"🔬 Analizar Región"**
- Espera 5-10 segundos

### **Paso 3: Ver Resultados**
El sistema muestra automáticamente:
- ✅ Resultados científicos (probabilidad, anomalía, acción)
- ✅ Explicación IA (o determinística si IA no disponible)
- ✅ Mediciones instrumentales (8 sensores)
- ✅ Contexto ambiental
- ✅ Pipeline científico (7 fases)

---

## 🧪 **CASOS DE PRUEBA**

### **Caso 1: Nuuk, Groenlandia** (Negativo - Glacial)
```
Lat: 64.2
Lon: -51.7
Región: Nuuk, Groenlandia
```

**Resultado Esperado**:
- Probabilidad antropogénica: ~32%
- Anomalía: ~75%
- Acción: `discard`
- Ambiente: `glacial`
- Explicación: "Glacial outwash plain - procesos naturales"

---

### **Caso 2: Acre, Brasil** (Geoglifos Amazónicos)
```
Lat: -9.8
Lon: -67.8
Región: Acre, Brasil - Geoglifos
```

**Resultado Esperado**:
- Probabilidad antropogénica: ~40%
- Anomalía: ~75%
- Acción: `monitoring_passive`
- Ambiente: `forest`
- Explicación: "Cobertura limitada - requiere más datos"

---

### **Caso 3: Rub al Khali, Arabia** (Paleocauces)
```
Lat: 22.5
Lon: 46.5
Región: Rub al Khali - Paleocauces
```

**Resultado Esperado**:
- Probabilidad antropogénica: ~40%
- Anomalía: ~75%
- Acción: `monitoring_targeted`
- Ambiente: `desert`
- Explicación: "Patrones prometedores - requiere SAR/LiDAR"

---

### **Caso 4: Patagonia** (Montaña Árida)
```
Lat: -46.5
Lon: -71.0
Región: Patagonia - Lago Buenos Aires
```

**Resultado Esperado**:
- Probabilidad antropogénica: ~40%
- Anomalía: ~75%
- Acción: `discard`
- Ambiente: `mountain_arid`
- Explicación: "Terreno montañoso - sin indicadores artificiales"

---

### **Caso 5: Doggerland** (Mar del Norte)
```
Lat: 54.5
Lon: 2.5
Región: Doggerland - Mar del Norte
```

**Resultado Esperado**:
- Probabilidad antropogénica: ~30%
- Anomalía: ~75%
- Acción: `instrument_upgrade_required`
- Ambiente: `shallow_sea`
- Cobertura: 0% efectiva
- Explicación: "Requiere sonar multihaz y magnetómetro"

---

## 🎨 **QUÉ OBSERVAR EN LA UI**

### **Panel Izquierdo - Controles**
- ✅ Status indicators (Backend ● IA ●)
  - Verde = Online
  - Rojo = Offline
- ✅ Badges epistemológicos principales
- ✅ Inputs de coordenadas
- ✅ Botón de análisis
- ✅ Acciones adicionales (Historial, Snapshot, Performance)

### **Panel Central - Mapa**
- ✅ Mapa interactivo (Leaflet)
- ✅ Click para seleccionar coordenadas
- ✅ Marcador en ubicación seleccionada

### **Panel Derecho - Resultados**
- ✅ **Resultados Científicos**
  - Badges de colores (verde/amarillo/naranja)
  - Probabilidad antropogénica
  - Anomaly score
  - Cobertura efectiva
  - Acción recomendada

- ✅ **Explicación IA**
  - Badge: `🤖 AI-ASSISTED` (si IA disponible)
  - Badge: `🧮 DETERMINISTIC` (si IA no disponible)
  - Texto explicativo en lenguaje natural
  - Modelo usado y timestamp

- ✅ **Mediciones Instrumentales**
  - Badge verde: `📡 MEASURED`
  - Lista de 8 instrumentos
  - Valores, modo (real/simulated), fuente

- ✅ **Contexto Ambiental**
  - Tipo de ambiente
  - Visibilidad arqueológica
  - Potencial de preservación

- ✅ **Pipeline Científico**
  - 7 fases (0, A-F, G)
  - Cada fase con badge amarillo: `🧮 INFERRED`

---

## 🔍 **BADGES EPISTEMOLÓGICOS**

### **Colores y Significados**
- 🟢 **Verde** (#27ae60): `📡 MEASURED` - Medición directa satelital
- 🟡 **Amarillo** (#f39c12): `🧮 INFERRED` - Calculado por pipeline
- 🟠 **Naranja** (#e67e22): `🤖 AI-ASSISTED` - Explicación generada por IA
- 🔴 **Rojo** (#e74c3c): `⚠️ SIMULATED` - Dato simulado (solo testing)

### **Badge Principal (arriba izquierda)**
```
🔬 Deterministic Scientific
🤖 AI: No
♻️ Reproducible: Yes
📊 Transparency: Full
```

---

## 🤖 **EXPLICACIONES CON IA**

### **Si Ollama está corriendo**
- El sistema usa `phi4-mini-reasoning`
- Genera explicación en lenguaje natural
- Badge: `🤖 AI-ASSISTED`
- Timeout: 30 segundos

### **Si Ollama NO está disponible**
- El sistema usa explicaciones determinísticas
- Basadas en reglas científicas
- Badge: `🧮 DETERMINISTIC`
- **Mismo resultado científico** (IA solo explica, no decide)

### **Verificar IA**
Mira el status indicator arriba a la izquierda:
- `● AI` verde = IA disponible
- `● AI` rojo = IA no disponible (usará fallback)

---

## 🔧 **FUNCIONES ADICIONALES**

### **Ver Historial**
- Click en "📋 Ver Historial"
- Muestra todos los análisis previos
- Click en entrada para cargar snapshot

### **Exportar Snapshot**
- Click en "💾 Exportar Snapshot"
- Descarga JSON con análisis completo
- Incluye: coordenadas, resultados, mediciones, timestamp
- Reproducible al 100%

### **Performance Stats**
- Click en "📊 Performance Stats"
- Muestra: FPS, uso de memoria, modo degradado
- Útil para debugging

---

## 🐛 **TROUBLESHOOTING**

### **Backend no responde**
```bash
# Verificar que el backend esté corriendo
curl http://localhost:8002/status
```

Si no responde:
```bash
python run_archeoscope.py
```

### **Frontend no carga**
```bash
# Verificar que el frontend esté corriendo
curl http://localhost:8080
```

Si no responde:
```bash
python start_frontend.py
```

### **IA no disponible**
```bash
# Verificar Ollama
curl http://localhost:11434/api/tags
```

Si no responde:
```bash
ollama serve
```

Luego:
```bash
ollama pull phi4-mini-reasoning
```

### **Errores en consola del navegador**
- Abre DevTools (F12)
- Mira la pestaña Console
- Busca errores en rojo
- Los módulos logean todo con `[ModuleName]`

---

## 📊 **VERIFICAR QUE TODO FUNCIONA**

### **Checklist de Prueba Completa**

- [ ] Frontend carga en http://localhost:8080
- [ ] Status Backend está verde (●)
- [ ] Puedo ingresar coordenadas
- [ ] Puedo hacer click en el mapa
- [ ] Botón "Analizar Región" funciona
- [ ] Loading spinner aparece
- [ ] Resultados se muestran después de 5-10 seg
- [ ] Badges epistemológicos aparecen
- [ ] Explicación IA/Determinística aparece
- [ ] Mediciones instrumentales se muestran
- [ ] Contexto ambiental se muestra
- [ ] Puedo exportar snapshot
- [ ] Puedo ver historial

---

## 🎯 **FLUJO COMPLETO ESPERADO**

```
1. Usuario ingresa coordenadas (64.2, -51.7)
   ↓
2. Click en "Analizar Región"
   ↓
3. Loading spinner (5-10 seg)
   ↓
4. Backend:
   - Clasifica ambiente → glacial
   - Mide con 8 instrumentos → valores reales
   - Ejecuta pipeline de 7 fases
   - Calcula probabilidad → 32%
   - Recomienda acción → discard
   ↓
5. Frontend:
   - Actualiza Scientific State (inmutable)
   - Emite evento ANALYSIS_COMPLETED
   - IA genera explicación (o fallback)
   - Renderiza resultados con badges
   - Guarda en historial
   ↓
6. Usuario ve:
   - Probabilidad: 32.7%
   - Anomalía: 75.0%
   - Acción: discard
   - Explicación: "Glacial outwash plain..."
   - 8 mediciones instrumentales
   - Badges epistemológicos
```

---

## 📝 **NOTAS IMPORTANTES**

1. **Un solo botón**: No hay "medir" y "analizar" separados. Todo es automático.

2. **IA es opcional**: Si no está disponible, el sistema funciona igual con explicaciones determinísticas.

3. **Reproducibilidad**: Cada análisis genera un snapshot exportable.

4. **Performance**: El sistema monitorea FPS y memoria automáticamente.

5. **Etiquetado epistemológico**: Todo está etiquetado (medición vs inferencia vs IA).

---

## 🚀 **PRUEBA RÁPIDA (30 SEGUNDOS)**

1. Abre: http://localhost:8080
2. Deja coordenadas por defecto (64.2, -51.7)
3. Click "🔬 Analizar Región"
4. Espera 10 segundos
5. ¡Mira los resultados!

**¿Funciona?** ✅ Sistema operativo  
**¿No funciona?** ❌ Revisa troubleshooting arriba

---

**Última actualización**: 27 de Enero, 2026  
**Versión**: 2.2  
**Status**: ✅ Production Ready
