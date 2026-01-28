# 🗺️ Cómo Ver la Capa de Sitios Arqueológicos

## ✅ Todo está listo!

La capa de sitios arqueológicos está **completamente implementada** y funcionando. Aquí está cómo verla:

## 🚀 Pasos para Visualizar

### 1. Asegurar que el Backend está Corriendo

```bash
python run_archeoscope.py
```

Deberías ver:
```
✅ Backend is running on http://localhost:8002
```

### 2. Abrir el Frontend

**Opción A: Directamente (más simple)**
```bash
# Navegar a la carpeta frontend
cd frontend

# Abrir index.html en tu navegador
# Windows:
start index.html

# O simplemente hacer doble-click en frontend/index.html
```

**Opción B: Con servidor local (recomendado)**
```bash
cd frontend
python -m http.server 8080
```

Luego abrir en navegador: `http://localhost:8080`

### 3. Activar la Capa de Sitios

Una vez que el mapa esté cargado:

1. **Buscar el panel "🗺️ Capas Arqueológicas"** en la esquina superior derecha
2. **Click en "📍 Mostrar Sitios Conocidos"**
3. Esperar unos segundos mientras carga los sitios
4. ¡Verás miles de puntos en el mapa!

### 4. Explorar los Sitios

- **Click en cualquier punto** para ver información del sitio
- **Colores**:
  - 🟢 Verde = Alta confianza (HIGH)
  - 🟡 Amarillo = Confianza moderada (MODERATE)
  - 🔴 Rojo = Baja confianza (LOW)
  - 🟠 Naranja = Candidato (CANDIDATE)

### 5. Ver Candidatos

1. **Click en "🔍 Mostrar Candidatos"**
2. Los candidatos aparecen con **animación pulsante naranja**
3. Click en un candidato para ver:
   - Métricas de origen antropogénico
   - Métricas de actividad actual
   - Anomalía instrumental
   - ESS (Explanatory Strangeness Score)

### 6. Filtrar Sitios

1. **Click en "⚙️ Filtros Avanzados"**
2. Seleccionar:
   - Nivel de confianza (HIGH, MODERATE, LOW, CANDIDATE)
   - País (ej: Egypt, Peru, Mexico)
3. **Click en "✅ Aplicar"**
4. La capa se recarga con solo los sitios filtrados

### 7. Investigar Alrededores de un Sitio

1. Click en cualquier sitio en el mapa
2. En el popup, **click en "🔍 Investigar Alrededores"**
3. El mapa se centra automáticamente en el sitio
4. Las coordenadas se pre-configuran en el panel izquierdo
5. Click en "🔬 Analizar Región" para ejecutar análisis detallado

## 🎯 Qué Esperar

### Sitios Conocidos (80,655 en total)

- **África**: 15,577 sitios
- **Europa**: ~20,000 sitios
- **Asia**: ~15,000 sitios
- **América**: ~10,000 sitios
- **Oceanía**: ~5,000 sitios

### Candidatos

Los candidatos son sitios detectados por ArcheoScope que requieren validación. Tienen:
- **Origen antropogénico**: 70-95% (fueron creados por humanos)
- **Actividad actual**: 0-20% (no hay actividad humana actual)
- **Anomalía instrumental**: 0-5% (no hay anomalías detectables)
- **ESS**: HIGH/VERY_HIGH (alta extrañeza explicativa)

## 🐛 Si Algo No Funciona

### "No veo el panel de capas"

**Solución**: El panel se crea automáticamente. Espera unos segundos después de cargar la página.

### "No se cargan los sitios"

**Verificar**:
1. Backend corriendo: `http://localhost:8002/status`
2. Consola del navegador (F12) para ver errores
3. Logs del backend

### "Los marcadores no aparecen"

**Posibles causas**:
1. Zoom muy alejado (hacer zoom in)
2. Filtros muy restrictivos (limpiar filtros)
3. Capa no activada (verificar botón está en rojo "Ocultar")

## 📊 Estadísticas Actuales

Ejecutar para ver estadísticas:
```bash
python test_sites_layer_frontend.py
```

Verás:
- Total de sitios: 80,655
- Sitios de control: 29
- Distribución por país
- Distribución por tipo de ambiente

## 🎨 Características Visuales

### Animaciones
- **Candidatos**: Pulsan suavemente (2s loop)
- **Hover**: Los marcadores crecen 1.3x
- **Toast notifications**: Aparecen en top-right

### Popups
- **Sitios históricos**: Muestran métricas separadas
- **Candidatos**: Destacan con fondo amarillo
- **Botón investigar**: Animación al activar

## 📝 Notas Importantes

1. **Primera carga puede ser lenta**: 10K sitios toman ~5-10 segundos
2. **Usar filtros para mejor rendimiento**: Filtrar por país reduce la carga
3. **Los candidatos son pocos**: Solo ~100 candidatos vs 80K sitios conocidos
4. **Métricas en descripciones**: Las métricas se extraen del campo `description`

## 🎉 ¡Disfruta Explorando!

Ahora puedes:
- ✅ Ver 80,655+ sitios arqueológicos en el mapa
- ✅ Filtrar por confianza, tipo y país
- ✅ Ver candidatos con métricas separadas
- ✅ Investigar alrededores de cualquier sitio
- ✅ Explorar visualmente la distribución global de sitios

## 📸 Capturas de Pantalla Esperadas

### Vista Global
- Mapa mundial con miles de puntos
- Concentración en Europa, África, Asia
- Panel de controles en top-right

### Vista de Sitio Individual
- Popup con información detallada
- Métricas separadas (Origen, Actividad, Anomalía, ESS)
- Botón "Investigar Alrededores"

### Vista de Candidatos
- Puntos naranjas con animación pulse
- Métricas destacadas en popup
- Menor cantidad que sitios conocidos

## 🔗 Archivos Relevantes

- `frontend/known_sites_layer.js` - Módulo principal
- `frontend/index.html` - Integración
- `backend/api/scientific_endpoint.py` - Endpoints (líneas 800-914)
- `test_sites_layer_frontend.py` - Tests
- `test_sites_layer_ui.html` - Test standalone

## 💡 Tips

1. **Zoom regional**: Hacer zoom a una región específica antes de cargar
2. **Filtrar por país**: Más rápido que cargar todos los sitios
3. **Candidatos primero**: Ver candidatos es más rápido (solo ~100)
4. **Usar "Investigar"**: Forma rápida de analizar alrededores de sitios conocidos

---

**¿Preguntas?** Revisa `SITES_LAYER_IMPLEMENTATION.md` para detalles técnicos completos.
