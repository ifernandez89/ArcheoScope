# 🚫 APIs Deshabilitadas - ArcheoScope

**Fecha:** 26 de Enero de 2026  
**Decisión:** Deshabilitar MODIS y SMAP temporalmente

---

## ❌ MODIS - DESHABILITADO

### Razón
- Requiere implementación compleja de AppEEARS API
- Procesamiento asíncrono (tareas que tardan minutos/horas)
- Simulación actual funciona bien y es determinística
- No es prioritario para operación actual

### Estado Actual
- **Conector:** Existe pero marcado como `available = False`
- **Simulación:** Funcionando en core detector
- **Datos:** Basados en latitud y clima (científicamente razonables)
- **Confianza:** 0.6 (marcado como simulado)

### Cuándo Reactivar
- Cuando se necesite publicar en journal científico
- Cuando haya tiempo para implementar AppEEARS (4-6 horas)
- Cuando se requieran series temporales reales

### Implementación Futura
```python
# TODO: Implementar AppEEARS API
# 1. POST /api/task - Crear tarea
# 2. GET /api/task/{id} - Polling hasta done
# 3. GET /api/bundle/{id} - Descargar resultado
# 4. Extraer LST del archivo
```

---

## ❌ SMAP - DESHABILITADO

### Razón
- Requiere procesamiento complejo de archivos HDF5
- Descarga de granules grandes
- Simulación actual funciona bien y es determinística
- No es prioritario para operación actual

### Estado Actual
- **Conector:** Existe pero marcado como `available = False`
- **Simulación:** Funcionando en core detector
- **Datos:** Basados en latitud y clima (científicamente razonables)
- **Confianza:** 0.6 (marcado como simulado)

### Cuándo Reactivar
- Cuando se necesite publicar en journal científico
- Cuando haya tiempo para implementar procesamiento HDF5 (4-6 horas)
- Cuando se requieran datos de humedad reales

### Implementación Futura
```python
# TODO: Implementar earthaccess + HDF5
# 1. earthaccess.search_data(short_name="SPL3SMP")
# 2. earthaccess.download(results)
# 3. h5py.File() - Extraer soil_moisture
# 4. Filtrar por región y calcular stats
```

---

## ✅ APIS ACTIVAS (5)

### Datos Reales
1. **Sentinel-2** - NDVI, multispectral (10m)
2. **Sentinel-1** - SAR backscatter (10m)
3. **Landsat** - Térmico LST (30m)
4. **NSIDC** - Hielo marino

### Simulación en Core Detector
5. **ICESat-2** - Elevación (datos reales con overflow)
6. **MODIS** - LST (simulación basada en latitud) ❌ DESHABILITADO
7. **SMAP** - Soil moisture (simulación basada en latitud) ❌ DESHABILITADO

---

## 📊 IMPACTO DE LA DECISIÓN

### Antes
- APIs disponibles: 7/11 (63.6%)
- APIs con datos reales: 4/11 (36.4%)
- APIs con simulación: 3/11 (27.3%)

### Después
- APIs disponibles: 5/11 (45.5%)
- APIs con datos reales: 4/11 (36.4%)
- APIs con simulación en core: 2/11 (18.2%)

### Ventajas
- ✅ Código más limpio (menos conectores "fake")
- ✅ Logs más claros (no dice "MODIS initialized")
- ✅ Simulación en core detector es más honesta
- ✅ Menos confusión sobre qué es real vs simulado

### Desventajas
- ❌ Menos APIs "disponibles" en reportes
- ❌ Requiere reactivar si se necesitan datos reales

---

## 🔄 CÓMO REACTIVAR

### MODIS
1. Implementar AppEEARS API en `modis_connector.py`
2. Cambiar `self.available = False` a lógica de credenciales
3. Actualizar tests
4. Documentar uso

### SMAP
1. Implementar procesamiento HDF5 en `smap_connector.py`
2. Cambiar `self.available = False` a lógica de earthaccess
3. Actualizar tests
4. Documentar uso

---

## 💡 ALTERNATIVAS

### Si se necesitan datos térmicos reales:
- ✅ Usar **Landsat** (ya funciona)
- ✅ Usar **Sentinel-2** para NDVI (correlación con temperatura)

### Si se necesitan datos de humedad:
- ✅ Inferir de NDVI (vegetación indica humedad)
- ✅ Usar clasificación de terreno (desert = seco, forest = húmedo)

---

## 📝 NOTAS TÉCNICAS

### Simulación en Core Detector
El core detector tiene su propia lógica de simulación determinística:
- Usa hash de coordenadas como seed
- Ajusta por tipo de sitio (conocido vs desconocido)
- Aplica multiplicadores por ambiente
- Marca confianza apropiadamente

**Esta simulación es MEJOR que tener conectores "fake" porque:**
1. Es determinística (reproducible)
2. Está integrada en el flujo principal
3. Se ajusta por contexto arqueológico
4. No pretende ser datos reales

---

## ✅ DECISIÓN FINAL

**MODIS y SMAP quedan DESHABILITADOS hasta que:**
1. Se necesiten para publicación científica
2. Haya tiempo para implementar correctamente
3. Se requieran series temporales reales

**El sistema funciona perfectamente sin ellos usando:**
- 4 APIs con datos reales
- Simulación determinística en core detector
- Fallback inteligente

---

**Decisión tomada:** 26 de Enero de 2026  
**Implementado por:** Sistema ArcheoScope  
**Estado:** ✅ DESHABILITADOS CORRECTAMENTE
