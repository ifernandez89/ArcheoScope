# Cómo Leer los Logs Automáticamente

## ✅ Sistema Implementado

Los logs se guardan automáticamente en:
1. **localStorage** del navegador (cada 10 segundos)
2. **Archivo descargable** (cuando ejecutas `perf.download()`)

---

## 🎮 Instrucciones para el Usuario

### Opción 1: Descargar Logs (RECOMENDADO)

1. Juega normalmente
2. Cuando termines, abre DevTools (F12)
3. En la consola, escribe:
   ```javascript
   perf.download()
   ```
4. Se descargará un archivo `.txt` con todos los logs
5. Sube ese archivo aquí para que yo lo lea

### Opción 2: Copiar desde localStorage

1. Abre DevTools (F12)
2. Ve a la pestaña "Application" o "Almacenamiento"
3. En el menú izquierdo: Local Storage → http://localhost:3000
4. Busca la clave que empieza con `archeoscope-logs-`
5. Copia el valor completo
6. Pégalo aquí

---

## 📊 Qué se Loggea Automáticamente

- ✅ Inicio de sesión
- ✅ Llegada a ubicaciones (Machu Picchu, etc.)
- ✅ Métricas de performance cada 2 segundos
- ✅ Snapshots automáticos
- ✅ Warnings de performance
- ✅ Cambios de clima (próximamente)

---

## 🔍 Para Kiro (Leer Logs)

Cuando el usuario suba el archivo o pegue los logs, buscar:

### Formato de Logs:
```
[timestamp_ms] [CATEGORY] Message | {data}
```

### Categorías:
- `SESSION_START` - Inicio de sesión
- `PERF_INIT` - Inicialización del monitor
- `LOCATION` - Llegada a ubicación
- `PERF_METRICS` - Métricas cada 2s
- `SNAPSHOT` - Snapshot capturado
- `PERF_WARNING` - Warnings de performance
- `SNAPSHOT_WARNING` - Warnings en snapshot

### Análisis de Pantallazos Verdes:

Buscar en los logs:
1. **Spikes en frameTime** (>40ms)
2. **Cambios bruscos en drawCalls**
3. **Picos de memoria**
4. **Timestamps donde ocurren los problemas**

---

## 💡 Comandos Disponibles

```javascript
perf.help()      // Ver ayuda
perf.download()  // Descargar logs
perf.logs()      // Ver logs en consola
perf.snapshot("Location", "Weather", anomalies)  // Capturar snapshot
perf.report()    // Ver reporte completo
perf.clear()     // Limpiar snapshots
```

---

## 🎯 Próximos Pasos

1. Usuario juega y descarga logs con `perf.download()`
2. Usuario sube archivo aquí
3. Kiro lee y analiza automáticamente
4. Kiro genera diagnóstico y recomendaciones
