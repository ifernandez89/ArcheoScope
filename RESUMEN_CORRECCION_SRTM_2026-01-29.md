# 🔧 CORRECCIÓN SRTM - 2026-01-29

## PROBLEMA IDENTIFICADO

**SRTM devuelve None** - Todas las fuentes fallan

### Diagnóstico detallado

```
🏔️ SRTM: Intentando 3 fuentes...
   🔄 Intentando SRTM via opentopography...
   OpenTopography response: 401
   ⚠️ SRTM opentopography devolvió None
   
   🔄 Intentando SRTM via usgs_api...
   ⚠️ SRTM usgs_api devolvió None
   
   🔄 Intentando SRTM via earthdata...
   ⚠️ SRTM earthdata devolvió None
   
❌ SRTM: Todas las fuentes fallaron
```

### Causa raíz

**OpenTopography: HTTP 401 (Unauthorized)**

La API key está en BD pero OpenTopography la rechaza:
- Key: `a50282b0e5ff10cc45ada6d8ac1bf0b3`
- Posibles causas:
  1. Key inválida o expirada
  2. Formato de request incorrecto
  3. Key necesita activación en OpenTopography

---

## SOLUCIÓN INMEDIATA

### OPCIÓN 1: Usar OpenTopographyConnector directo (YA EXISTE)

Ya existe `backend/satellite_connectors/opentopography_connector.py` que funciona.

**Modificar SRTM para usar el conector existente**:

```python
async def _get_srtm_opentopography(self, ...):
    """Usar OpenTopographyConnector existente."""
    try:
        from .opentopography_connector import OpenTopographyConnector
        
        ot_connector = OpenTopographyConnector()
        if not ot_connector.available:
            return None
        
        # Usar el método existente
        result = await ot_connector.get_elevation_data(
            lat_min, lat_max, lon_min, lon_max
        )
        
        if result and hasattr(result, 'indices'):
            return {
                'value': result.indices.get('elevation_mean'),
                'elevation_stats': result.indices,
                'unit': 'meters',
                'source': 'OpenTopography'
            }
        
        return None
        
    except Exception as e:
        logger.error(f"OpenTopography connector failed: {e}")
        return None
```

### OPCIÓN 2: Usar NASADEM (SIN API KEY)

NASADEM es mejor que SRTM y no requiere autenticación:

```python
async def get_elevation_data(self, ...):
    """Usar NASADEM como fuente principal."""
    try:
        # NASADEM via Planetary Computer (sin auth)
        from .planetary_computer import PlanetaryComputerConnector
        
        pc = PlanetaryComputerConnector()
        # Implementar get_nasadem_data()...
        
    except Exception as e:
        logger.error(f"NASADEM failed: {e}")
        return None
```

### OPCIÓN 3: Arreglar credenciales OpenTopography

Verificar que la key es correcta:
1. Ir a https://opentopography.org/
2. Login con cuenta
3. Verificar API key en perfil
4. Regenerar si es necesario

---

## WORKAROUND TEMPORAL

Mientras se arregla SRTM, usar OpenTopography directo:

```python
from backend.satellite_connectors.opentopography_connector import OpenTopographyConnector

ot = OpenTopographyConnector()
dem = await ot.get_elevation_data(lat_min, lat_max, lon_min, lon_max)
```

---

## IMPACTO

### Severidad: **MEDIA**

**Sistema operativo**: 4/5 CORE (80%)

**Instrumentos funcionando**:
- ✅ Sentinel-2 NDVI
- ✅ Sentinel-1 SAR
- ✅ Landsat Thermal
- ❌ SRTM DEM (401 Unauthorized)
- ✅ ERA5 Climate

**Workaround disponible**: Sí (OpenTopographyConnector directo)

---

## RECOMENDACIÓN

**IMPLEMENTAR OPCIÓN 1** (15 minutos):
- Usar OpenTopographyConnector existente
- Ya está probado y funciona
- Evita duplicar código
- Solución inmediata

**Código a modificar**:
- `backend/satellite_connectors/srtm_connector.py`
- Método `_get_srtm_opentopography()`

---

## ESTADO FINAL ESPERADO

Después de implementar OPCIÓN 1:

**CORE: 5/5 (100%)** ✅
- ✅ Sentinel-2 NDVI
- ✅ Sentinel-1 SAR
- ✅ Landsat Thermal
- ✅ SRTM DEM (via OpenTopography)
- ✅ ERA5 Climate

---

**Fecha**: 2026-01-29 18:54  
**Problema**: SRTM devuelve None (401 Unauthorized)  
**Solución**: Usar OpenTopographyConnector existente  
**Tiempo**: 15 minutos
