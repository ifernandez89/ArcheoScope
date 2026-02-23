# 🚀 GUÍA DE TESTING - OPTIMIZACIONES DE PERFORMANCE

## INICIO RÁPIDO

### 1. Iniciar el servidor de desarrollo
```bash
cd viewer3d
npm run dev
```

### 2. Abrir en navegador
```
http://localhost:3000
```

---

## 🎮 ESCENARIO DE PRUEBA

### Paso 1: Ir a Machu Picchu
1. Hacer clic en el globo en las coordenadas de Machu Picchu
2. O usar el input de coordenadas: `-13.1631, -72.5450`
3. Esperar a que cargue la escena

### Paso 2: Activar Clima Extremo
1. Abrir el panel de clima (esquina superior derecha)
2. Activar en este orden:
   - ☁️ Nubes
   - 🌧️ Lluvia Pesada (Heavy)
   - 💨 Viento
   - 🌫️ Niebla (opcional)

### Paso 3: Moverse por la escena
1. Usar WASD para moverte
2. Usar mouse para mirar alrededor
3. Presionar SHIFT + mover mouse arriba/abajo para volar

### Paso 4: Observar Performance
**Buscar:**
- ❌ Pantallazos negros (freezes)
- ❌ Pantallazos verdes (glitches)
- ✅ Movimiento fluido
- ✅ FPS estable

---

## 📊 MONITOREO DE PERFORMANCE

### Abrir Consola del Navegador
**Chrome/Edge**: F12 → Console
**Firefox**: F12 → Console

### Ver Métricas en Tiempo Real
Los logs se imprimen automáticamente cada 2 segundos:
```
📊 PERFORMANCE METRICS
🎯 FPS: 60.0 (min: 58.5) [GOOD]
⏱️ Frame Time: 16.67ms (max: 17.30ms) [GOOD]
🎨 Draw Calls: 64
🔺 Triangles: 1.58M
💾 Memory: 196MB
```

### Generar Snapshot Manual
```javascript
window.perfMonitor.createSnapshot("Machu Picchu", "Heavy Rain + Clouds + Wind", 1)
```

### Ver Reporte Completo
```javascript
window.perfMonitor.printReport()
```

---

## 🎯 MÉTRICAS OBJETIVO

| Métrica | Objetivo | Crítico |
|---------|----------|---------|
| FPS | >30 | <25 |
| Frame Time | <33ms | >40ms |
| Draw Calls | <200 | >300 |
| Memory | <400MB | >600MB |

### Estados de Performance
- 🟢 **GOOD**: Todo normal
- 🟡 **WARNING**: Cerca del límite
- 🔴 **CRITICAL**: Problema de performance

---

## 📝 LOGS AUTOMÁTICOS

Los logs se guardan automáticamente en:
```
viewer3d/PERFORMANCE_LOGS.txt
```

**Estos logs son para que YO (el agente) los lea después.**
No necesitas hacer nada con ellos.

---

## ⚠️ QUÉ REPORTAR

### Si ves pantallazos negros:
1. Anotar cuándo ocurren (con qué clima activo)
2. Anotar duración aproximada
3. Decirme: "Hay pantallazos negros con [clima]"

### Si ves pantallazos verdes:
1. Anotar cuándo ocurren
2. Anotar si es al moverse o estático
3. Decirme: "Hay pantallazos verdes cuando [acción]"

### Si todo va bien:
1. Decirme: "Todo fluido, sin problemas"
2. Opcionalmente: Copiar las últimas líneas de la consola

---

## 🔧 CAMBIOS REALIZADOS

### Optimizaciones Principales:
1. **Lluvia**: Reducida de 18,000 → 1,500 partículas (-91.7%)
2. **Nubes**: Textura reducida de 1024x512 → 512x256 (-75%)
3. **Renderer Info**: Corregida lectura de métricas
4. **PostProcessing**: Corregido error de carga

### Resultado Esperado:
- ✅ Sin pantallazos negros
- ✅ Frame time <40ms con clima extremo
- ✅ Movimiento fluido
- ✅ Métricas correctas en logs

---

## 🚨 TROUBLESHOOTING

### Si el servidor no inicia:
```bash
npm install
npm run dev
```

### Si hay error de puerto ocupado:
```bash
# Matar proceso en puerto 3000
npx kill-port 3000
npm run dev
```

### Si la página no carga:
1. Limpiar caché del navegador (Ctrl+Shift+Delete)
2. Recargar con Ctrl+F5

---

## ✅ CHECKLIST DE TESTING

- [ ] Servidor iniciado correctamente
- [ ] Página carga sin errores
- [ ] Puedo navegar al globo
- [ ] Puedo teletransportarme a Machu Picchu
- [ ] Puedo activar clima (nubes, lluvia, viento)
- [ ] Puedo moverme con WASD
- [ ] Veo logs de performance en consola
- [ ] NO hay pantallazos negros
- [ ] NO hay pantallazos verdes
- [ ] Movimiento es fluido

---

**¡Listo para probar!** 🎮

Cuando termines, solo dime cómo fue la experiencia.
