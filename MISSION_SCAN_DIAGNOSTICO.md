# Diagnóstico: mission_real_data_scan.py

## Problemas Identificados

### 1. ⏱️ Sin Timeouts
**Problema**: Las llamadas async no tienen timeout, pueden quedarse colgadas indefinidamente.
**Solución**: ✅ Agregado timeout de 10 minutos por zona

### 2. 📊 Falta de Logs de Progreso
**Problema**: No hay feedback durante el procesamiento, parece que está colgado.
**Solución**: ✅ Agregados logs de:
- Tiempo estimado por zona
- Tamaño del grid esperado
- Progreso entre zonas
- Tiempo total transcurrido

### 3. 🗺️ Zonas Muy Grandes
**Problema**: Algunas zonas tienen 1-2 grados de extensión (100-200 km²)
- Puerto Rico North: ~0.6° x 0.8° = ~4,400 km²
- SE Sargasso Sea: 1° x 2° = ~24,000 km²

Con resolución de 50m, esto genera grids enormes:
- 4,400 km² @ 50m = ~1,760,000 píxeles
- 24,000 km² @ 50m = ~9,600,000 píxeles

**Solución Recomendada**:
- Reducir tamaño de zonas a < 0.1° x 0.1° (~100 km²)
- O aumentar resolución a 100-200m para zonas grandes

### 4. 🔌 Posibles Problemas de Conectores
**Problema**: 15 conectores satelitales, algunos pueden fallar o ser lentos
**Solución**: ✅ Creado script de diagnóstico `debug_mission_scan.py`

## Mejoras Implementadas

### ✅ mission_real_data_scan.py

```python
# 1. Timeout por zona (10 minutos)
result = await asyncio.wait_for(
    self.engine.analyze_territory(...),
    timeout=600.0
)

# 2. Logs de progreso
print(f"⏳ Starting analysis at {start_time}...")
print(f"   Expected grid size: ~{pixels_x} x {pixels_y}")
print(f"   This may take several minutes...")

# 3. Tiempo transcurrido
elapsed = (datetime.now() - start_time).total_seconds()
print(f"✅ Analysis completed in {elapsed:.1f}s")

# 4. Progreso global
print(f"📊 Progress: {idx}/{len(SCAN_ZONES)} zones completed")
print(f"   Estimated remaining: {remaining/60:.1f} minutes")
```

## Cómo Usar

### Opción 1: Ejecutar con Mejoras
```bash
python mission_real_data_scan.py
```

Ahora verás:
- Tamaño estimado del grid
- Tiempo por zona
- Progreso entre zonas
- Timeouts si una zona tarda >10 minutos

### Opción 2: Diagnóstico Rápido
```bash
python debug_mission_scan.py
```

Este script:
1. Prueba inicialización de conectores
2. Ejecuta análisis en zona micro (500m x 500m)
3. Identifica cuellos de botella específicos
4. Timeout de 2 minutos para test rápido

## Recomendaciones

### 🚀 Para Ejecución Inmediata

1. **Ejecutar diagnóstico primero**:
   ```bash
   python debug_mission_scan.py
   ```

2. **Si el diagnóstico pasa**, ejecutar misión completa:
   ```bash
   python mission_real_data_scan.py
   ```

3. **Monitorear logs** para ver progreso real

### 🎯 Para Mejorar Performance

1. **Reducir zonas grandes**:
   ```python
   # Antes (24,000 km²)
   {
       "lat_min": 30.0,
       "lat_max": 31.0,  # 1 grado
       "lon_min": -64.0,
       "lon_max": -62.0,  # 2 grados
   }
   
   # Después (100 km²)
   {
       "lat_min": 30.0,
       "lat_max": 30.1,  # 0.1 grados
       "lon_min": -64.0,
       "lon_max": -63.9,  # 0.1 grados
   }
   ```

2. **Aumentar resolución para zonas grandes**:
   ```python
   resolution_m=100.0  # En vez de 50.0
   ```

3. **Procesar zonas en lotes**:
   ```python
   # Dividir SCAN_ZONES en grupos de 2-3 zonas
   # Ejecutar cada lote por separado
   ```

### 🔍 Si Sigue Lento

Verificar:
1. **Credenciales de APIs** en la base de datos
2. **Conectividad de red** a servicios satelitales
3. **Logs del backend** para errores específicos
4. **Caché de datos** - puede estar descargando repetidamente

## Tiempos Esperados

Con las mejoras:

| Zona | Tamaño | Resolución | Tiempo Estimado |
|------|--------|------------|-----------------|
| Bermuda (0.01° x 0.01°) | ~1 km² | 50m | 30-60s |
| Puerto Rico (0.6° x 0.8°) | ~4,400 km² | 50m | 5-10 min |
| Sargasso (1° x 2°) | ~24,000 km² | 50m | **20-30 min** ⚠️ |

**Total estimado**: 30-45 minutos para las 4 zonas

## Próximos Pasos

1. ✅ Ejecutar `debug_mission_scan.py` para verificar sistema
2. ⏳ Si pasa, ejecutar `mission_real_data_scan.py` con logs mejorados
3. 📊 Monitorear progreso en tiempo real
4. 🎯 Ajustar tamaños de zona según resultados

## Logs Mejorados - Ejemplo

```
================================================================================
📍 ZONE: SE Sargasso Sea Margin (Silent Zone)
   Type: SCIENTIFIC_PRIORITY
   Rationale: Ancient oceanic floor, slow sedimentation
   Bounds: [30.000, 31.000] x [-64.000, -62.000]
   Approximate Area: 24000.0 km²
================================================================================
⏳ Starting analysis at 14:23:15...
   Resolution: 50m
   Expected grid size: ~2220 x 4440 pixels
   This may take several minutes for large areas...

✅ Analysis completed in 847.3s

✅ SCAN COMPLETE (took 847.3s)
   🎯 Territorial Coherence (G1): 0.723
   🔬 Scientific Rigor: 0.856
   📊 3D Coherence (ETP): 0.681
   🧬 TAS Score: 0.745
   🔬 DIL Score: 0.692

📊 Progress: 3/4 zones completed
   Total elapsed: 18.5 minutes
   Estimated remaining: 6.2 minutes
```
