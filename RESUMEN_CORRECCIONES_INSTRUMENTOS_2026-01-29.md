# Resumen de Correcciones de Instrumentos
**Fecha**: 2026-01-29  
**Sesión**: Corrección de bugs en PALSAR, MODIS LST y OpenTopography

---

## 🎯 OBJETIVO

Corregir los 4 instrumentos FAILED para aumentar cobertura instrumental de 67% a 100%:
- ❌ PALSAR: Bug en procesamiento de escenas
- ❌ MODIS LST: Timeout muy corto (30s)
- ❌ OpenTopography: Timeout muy corto (90s)
- ✅ Copernicus SST: Ya corregido (región terrestre = comportamiento correcto)

---

## 📋 CORRECCIONES APLICADAS

### 1. PALSAR-2 Connector (`backend/satellite_connectors/palsar_connector.py`)

#### Problema Original
```python
# Bug 1: Retornaba dict en lugar de InstrumentMeasurement
return {
    'value': backscatter_data['mean_backscatter'],
    'backscatter_stats': backscatter_data['stats'],
    ...
}

# Bug 2: _select_best_scene no validaba que scenes fueran dict
for scene in scenes:
    scene_bounds = scene.get('bbox', []) if isinstance(scene, dict) else []
    # Podía procesar listas como si fueran dict
```

#### Solución Implementada
```python
# ✅ Retorna InstrumentMeasurement
return InstrumentMeasurement.create_success(
    instrument_name="PALSAR-2",
    measurement_type=f"sar_backscatter_{polarization}",
    value=backscatter_data['mean_backscatter'],
    unit='dB',
    confidence=0.85,
    source=f'ASF DAAC PALSAR2 {polarization}',
    acquisition_date=best_scene.get('startTime', '')[:10],
    metadata={...}
)

# ✅ Validación robusta de escenas
valid_scenes = [s for s in scenes if isinstance(s, dict)]
if not valid_scenes:
    logger.warning("No hay escenas válidas (todas son listas o no-dict)")
    return None

# ✅ Validación final antes de retornar
best_scene = scored_scenes[0][1]
if not isinstance(best_scene, dict):
    logger.error(f"Best scene no es dict: {type(best_scene)}")
    return None
```

#### Métodos Actualizados
- ✅ `get_sar_backscatter()` → Retorna `InstrumentMeasurement`
- ✅ `get_forest_penetration()` → Retorna `InstrumentMeasurement`
- ✅ `get_soil_moisture()` → Retorna `InstrumentMeasurement`
- ✅ `_select_best_scene()` → Validación robusta de tipos

#### Credenciales
```python
# ✅ Usa CredentialsManager en lugar de os.getenv()
from credentials_manager import CredentialsManager
creds_manager = CredentialsManager()
self.username = creds_manager.get_credential("earthdata", "username")
self.password = creds_manager.get_credential("earthdata", "password")
```

---

### 2. MODIS LST Connector (`backend/satellite_connectors/modis_lst_connector.py`)

#### Problema Original
```python
# Timeout muy corto para API de NASA
async with httpx.AsyncClient(timeout=30.0) as client:
    # Fallaba con ConnectTimeout en muchas regiones
```

#### Solución Implementada
```python
# ✅ Timeout aumentado a 120s
async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
    # Ahora tiene tiempo suficiente para responder
```

#### Credenciales
```python
# ✅ Usa CredentialsManager
from backend.credentials_manager import CredentialsManager
creds_manager = CredentialsManager()
self.username = creds_manager.get_credential("earthdata", "username")
self.password = creds_manager.get_credential("earthdata", "password")
```

---

### 3. OpenTopography Connector (`backend/satellite_connectors/opentopography_connector.py`)

#### Problema Original
```python
# Timeout de 90s insuficiente para regiones grandes
self.timeout = float(os.getenv("OPENTOPOGRAPHY_TIMEOUT", "90"))
```

#### Solución Implementada
```python
# ✅ Timeout aumentado a 120s
self.timeout = float(os.getenv("OPENTOPOGRAPHY_TIMEOUT", "120"))
```

#### Credenciales
```python
# ✅ Usa CredentialsManager
from credentials_manager import CredentialsManager
creds_manager = CredentialsManager()
self.api_key = creds_manager.get_credential("opentopography", "api_key")
```

---

## 🧪 TESTING

### Script de Test
`test_instrumentos_corregidos.py` - Verifica:
1. PALSAR retorna `InstrumentMeasurement` correctamente
2. MODIS LST usa timeout de 120s
3. OpenTopography usa timeout de 120s

### Resultados Esperados

#### Con Credenciales en BD
```
✅ PALSAR: InstrumentMeasurement.create_success() o create_no_data()
✅ MODIS LST: Datos reales o estimación con timeout adecuado
✅ OpenTopography: DEM con rugosidad como valor principal
```

#### Sin Credenciales
```
✅ PALSAR: InstrumentMeasurement.create_no_data() (comportamiento correcto)
⚠️ MODIS LST: No disponible (requiere credenciales Earthdata)
⚠️ OpenTopography: No disponible (requiere API key)
```

---

## 📊 IMPACTO EN COBERTURA

### Antes de Correcciones
```
Coverage: 67% (8/12 instrumentos usables)
- SUCCESS (6): Sentinel-2, Sentinel-1 SAR, Landsat Thermal, ICESat-2, ERA5, SRTM
- DEGRADED (2): CHIRPS, VIIRS
- FAILED (4): OpenTopography, MODIS LST, Copernicus SST, PALSAR
```

### Después de Correcciones (Esperado)
```
Coverage: 92% (11/12 instrumentos usables)
- SUCCESS (9): Sentinel-2, Sentinel-1 SAR, Landsat Thermal, ICESat-2, ERA5, SRTM, 
               PALSAR, MODIS LST, OpenTopography
- DEGRADED (2): CHIRPS, VIIRS
- CORRECT_BEHAVIOR (1): Copernicus SST (región terrestre)
```

---

## 🔧 REGLAS IMPLEMENTADAS

### Regla 1: InstrumentMeasurement Obligatorio
**TODOS los conectores DEBEN retornar `InstrumentMeasurement`, NO dict o `SatelliteData`**

```python
# ❌ INCORRECTO
return {'value': 123, 'unit': 'dB'}

# ✅ CORRECTO
return InstrumentMeasurement.create_success(
    instrument_name="PALSAR-2",
    measurement_type="sar_backscatter",
    value=123,
    unit='dB',
    confidence=0.85,
    source="ASF DAAC",
    metadata={...}
)
```

### Regla 2: Credenciales desde BD Encriptada
**NUNCA usar `os.getenv()` directamente - SIEMPRE usar `CredentialsManager`**

```python
# ❌ INCORRECTO
self.api_key = os.getenv("OPENTOPOGRAPHY_API_KEY")

# ✅ CORRECTO
from credentials_manager import CredentialsManager
creds_manager = CredentialsManager()
self.api_key = creds_manager.get_credential("opentopography", "api_key")
```

### Regla 3: Timeouts Adecuados
**APIs de NASA y servicios pesados necesitan timeouts >= 120s**

```python
# ❌ INCORRECTO (muy corto)
async with httpx.AsyncClient(timeout=30.0) as client:

# ✅ CORRECTO
async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
```

### Regla 4: Validación de Tipos Robusta
**Validar tipos antes de procesar, especialmente con APIs externas**

```python
# ❌ INCORRECTO (asume que scene es dict)
scene_bounds = scene.get('bbox', [])

# ✅ CORRECTO (valida tipo primero)
if not isinstance(scene, dict):
    logger.error(f"Scene debe ser dict, recibido: {type(scene)}")
    return None
scene_bounds = scene.get('bbox', [])
```

---

## 📁 ARCHIVOS MODIFICADOS

```
backend/satellite_connectors/
├── palsar_connector.py          ✅ Corregido (InstrumentMeasurement + validación)
├── modis_lst_connector.py       ✅ Corregido (timeout 120s + CredentialsManager)
└── opentopography_connector.py  ✅ Corregido (timeout 120s + CredentialsManager)

test_instrumentos_corregidos.py  ✅ Nuevo (script de verificación)
```

---

## 🚀 PRÓXIMOS PASOS

1. **Verificar credenciales en BD**
   ```bash
   python check_earthdata_creds.py
   ```

2. **Ejecutar test de instrumentos**
   ```bash
   python test_instrumentos_corregidos.py
   ```

3. **Test end-to-end con pipeline completo**
   ```bash
   python test_integracion_completa.py
   ```

4. **Verificar cobertura instrumental**
   - Objetivo: 92% (11/12 instrumentos)
   - Esperado: PALSAR, MODIS LST, OpenTopography ahora SUCCESS

---

## ✅ CHECKLIST DE VALIDACIÓN

- [x] PALSAR retorna `InstrumentMeasurement`
- [x] PALSAR valida tipos de escenas robustamente
- [x] PALSAR usa `CredentialsManager`
- [x] MODIS LST timeout aumentado a 120s
- [x] MODIS LST usa `CredentialsManager`
- [x] OpenTopography timeout aumentado a 120s
- [x] OpenTopography usa `CredentialsManager`
- [x] Todos los métodos PALSAR actualizados
- [x] Script de test creado
- [ ] Test ejecutado con credenciales reales
- [ ] Cobertura verificada >= 92%

---

## 📝 NOTAS TÉCNICAS

### PALSAR Scene Selection Bug
El bug original era sutil:
```python
# scored_scenes = [(score1, scene1), (score2, scene2), ...]
scored_scenes.sort(key=lambda x: x[0], reverse=True)
return scored_scenes[0][1]  # Retorna scene1

# PERO: Si scene1 era una lista en lugar de dict, fallaba
# SOLUCIÓN: Filtrar valid_scenes = [s for s in scenes if isinstance(s, dict)]
```

### Timeout Strategy
- **Connect timeout**: 10s (suficiente para establecer conexión)
- **Read timeout**: 120s (suficiente para descargar datos grandes)
- **Total timeout**: 120s (balance entre velocidad y confiabilidad)

### CredentialsManager Pattern
```python
# Patrón robusto con fallback
try:
    from credentials_manager import CredentialsManager
    creds_manager = CredentialsManager()
    api_key = creds_manager.get_credential("service", "key")
except Exception as e:
    logger.warning(f"⚠️ No se pudo cargar desde BD: {e}")
    api_key = os.getenv("SERVICE_API_KEY")  # Fallback
```

---

**Autor**: Kiro AI Assistant  
**Fecha**: 2026-01-29  
**Versión**: 1.0
