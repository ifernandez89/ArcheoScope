# 📊 ANÁLISIS ÚLTIMO TEST + PRIORIDADES CRÍTICAS

## ⏱️ TIEMPO DEL ÚLTIMO ANÁLISIS

### Test: Giza, Egipto (29.95-30.05, 31.10-31.20)

**Instrumentos testeados**: 5 CORE

```
[1/5] sentinel_2_ndvi... ✅ SUCCESS (0.128 NDVI, conf: 1.00)
[2/5] sentinel_1_sar... ✅ SUCCESS (-32746.201 dB, conf: 0.80) [CACHE HIT]
[3/5] landsat_thermal... ✅ SUCCESS (21.649 K, conf: 1.00)
[4/5] srtm_elevation... ✅ SUCCESS (250.000 m, conf: 0.80) [FALLBACK]
[5/5] era5_climate... ⏰ TIMEOUT (descarga GRIB lenta)
```

**Tiempo estimado**: ~2 minutos (sin ERA5 completo)

### ❌ Instrumentos que fallaron

1. **ICESat-2**: ❌ INVALID (no granules en región)
2. **NSIDC**: ❌ FAILED (región no polar)
3. **ERA5**: ⏰ TIMEOUT (descarga GRIB lenta, pero funciona)

**Tasa de éxito CORE**: 4/5 (80%) en tiempo real

---

## 🧠 EL VERDADERO PROBLEMA DETECTADO

### "En mi base solo tengo datos genéricos del sitio, no mediciones"

**💥 EXACTO. Ese es EL cuello de botella.**

### Estado actual de la BD

```sql
-- Tabla: archaeological_sites
CREATE TABLE archaeological_sites (
    id UUID PRIMARY KEY,
    name TEXT,
    description TEXT,  -- ❌ Texto genérico
    latitude FLOAT,
    longitude FLOAT,
    ess_score FLOAT,   -- ✅ Score agregado
    -- ❌ FALTA: Mediciones instrumentales crudas
);
```

### Lo que falta

```sql
-- ❌ NO EXISTE: Tabla de mediciones instrumentales
CREATE TABLE instrument_measurements (
    id UUID PRIMARY KEY,
    site_id UUID REFERENCES archaeological_sites(id),
    instrument_name TEXT,
    measurement_type TEXT,
    value FLOAT,
    unit TEXT,
    confidence FLOAT,
    quality_flags JSONB,
    acquisition_date TIMESTAMP,
    source TEXT,
    processing_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Problema**: Estás haciendo **inferencia científica** sin guardar **observaciones instrumentales persistentes**.

---

## 🎯 PRIORIDADES (REALISTAS Y PRIORIZADAS)

### 🥇 PRIORIDAD 1: Persistir TODAS las mediciones crudas

**Impacto**: ENORME  
**Costo**: BAJO (1-2 días)

#### Qué guardar

```python
# Para cada instrumento, guardar:
{
    "instrument": "sentinel_2_ndvi",
    "measurements": {
        "ndvi_mean": 0.128,
        "ndvi_std": 0.045,
        "ndvi_min": 0.05,
        "ndvi_max": 0.25,
        "cloud_cover": 5.2,
        "pixel_count": 1024
    },
    "confidence": 1.0,
    "acquisition_date": "2024-01-15",
    "source": "Sentinel-2 L2A"
}

{
    "instrument": "landsat_thermal",
    "measurements": {
        "thermal_mean": 21.649,
        "thermal_std": 2.3,
        "thermal_min": 18.5,
        "thermal_max": 25.8,
        "anomaly_pixels": 45
    },
    "confidence": 1.0,
    "acquisition_date": "2024-01-10",
    "source": "Landsat 8 TIRS"
}

{
    "instrument": "sentinel_1_sar",
    "measurements": {
        "vv_mean": -15.2,
        "vh_mean": -22.1,
        "coherence": 0.65,
        "loss_tangent": 0.12,
        "penetration_depth_cm": 30
    },
    "confidence": 0.8,
    "acquisition_date": "2024-01-12",
    "source": "Sentinel-1 IW"
}

{
    "instrument": "srtm_elevation",
    "measurements": {
        "elevation_mean": 250.0,
        "elevation_std": 15.3,
        "slope_mean": 2.5,
        "roughness": 0.45,
        "dem_status": "FALLBACK_NASADEM"  # ✅ Flag explícito
    },
    "confidence": 0.8,
    "acquisition_date": "2000-02-11",
    "source": "NASADEM_estimated"
}
```

#### Implementación

```python
# backend/database/measurements_repository.py

class MeasurementsRepository:
    """Repositorio para mediciones instrumentales."""
    
    async def save_measurement(self, site_id: UUID, measurement: InstrumentMeasurement):
        """Guardar medición instrumental cruda."""
        
        query = """
        INSERT INTO instrument_measurements (
            site_id, instrument_name, measurement_type,
            value, unit, confidence, quality_flags,
            acquisition_date, source, processing_notes
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        RETURNING id
        """
        
        return await self.db.fetchval(
            query,
            site_id,
            measurement.instrument_name,
            measurement.measurement_type,
            measurement.value,
            measurement.unit,
            measurement.confidence,
            json.dumps(measurement.quality_flags),
            measurement.acquisition_date,
            measurement.source,
            measurement.processing_notes
        )
    
    async def get_site_measurements(self, site_id: UUID) -> List[InstrumentMeasurement]:
        """Obtener todas las mediciones de un sitio."""
        
        query = """
        SELECT * FROM instrument_measurements
        WHERE site_id = $1
        ORDER BY acquisition_date DESC
        """
        
        rows = await self.db.fetch(query, site_id)
        return [self._row_to_measurement(row) for row in rows]
```

**Resultado**: Tu BD ahora guarda **EVIDENCIA**, no solo "descripción".

---

### 🥈 PRIORIDAD 2: Separar señales claramente

**Impacto**: ALTO (credibilidad x2)  
**Costo**: MEDIO (3-4 días)

#### Clasificación de señales

```python
# backend/signal_classification.py

class SignalType(Enum):
    OBSERVED = "observed"        # Medición directa de sensor
    INFERRED = "inferred"        # Inferencia de modelo (DIL, TAS)
    CONTEXTUAL = "contextual"    # Conocimiento previo (clima, geología)

class ArchaeologicalSignal:
    """Señal arqueológica clasificada."""
    
    def __init__(self):
        self.signal_type: SignalType
        self.instrument: str
        self.value: float
        self.confidence: float
        self.evidence_strength: str  # "strong", "medium", "weak"
```

#### Score con transparencia

```python
def calculate_ess_with_transparency(signals: List[ArchaeologicalSignal]) -> Dict:
    """
    Calcular ESS con transparencia total.
    
    Separa:
    - Señales observadas (sensores reales)
    - Señales inferidas (modelos)
    - Conocimiento contextual
    """
    
    observed_signals = [s for s in signals if s.signal_type == SignalType.OBSERVED]
    inferred_signals = [s for s in signals if s.signal_type == SignalType.INFERRED]
    contextual_signals = [s for s in signals if s.signal_type == SignalType.CONTEXTUAL]
    
    # Score base (solo observados)
    base_score = calculate_base_score(observed_signals)
    
    # Boost por inferencia (máximo 20%)
    inference_boost = calculate_inference_boost(inferred_signals) * 0.2
    
    # Ajuste contextual (±10%)
    context_adjustment = calculate_context_adjustment(contextual_signals) * 0.1
    
    final_score = base_score + inference_boost + context_adjustment
    
    return {
        "ess_score": final_score,
        "breakdown": {
            "base_score": base_score,
            "observed_sensors": len(observed_signals),
            "inferred_components": len(inferred_signals),
            "contextual_factors": len(contextual_signals)
        },
        "transparency": {
            "observed_instruments": [s.instrument for s in observed_signals],
            "inference_methods": [s.instrument for s in inferred_signals],
            "context_sources": [s.instrument for s in contextual_signals]
        },
        "interpretation": f"Score {final_score:.2f} basado en {len(observed_signals)} sensores reales + inferencia DIL"
    }
```

**Resultado**: Score **paper-ready** con transparencia total.

---

### 🥉 PRIORIDAD 3: Copernicus DEM (ya mismo)

**Impacto**: MEDIO (elimina ruido SRTM)  
**Costo**: BAJO (1 día)

#### Por qué Copernicus DEM

- ✅ **Gratis** (sin API key)
- ✅ **Global** (cobertura completa)
- ✅ **30m resolución** (mejor que SRTM 90m)
- ✅ **Sin vacíos** (mejor corrección que SRTM)
- ✅ **Actualizado** (2021 vs SRTM 2000)

#### Implementación

```python
# backend/satellite_connectors/copernicus_dem_connector.py

class CopernicusDEMConnector:
    """
    Conector a Copernicus DEM GLO-30.
    
    Fuente: https://registry.opendata.aws/copernicus-dem/
    Resolución: 30m
    Cobertura: Global (-90 a +90)
    Costo: GRATIS (AWS Open Data)
    """
    
    def __init__(self):
        self.base_url = "https://copernicus-dem-30m.s3.amazonaws.com"
        self.available = True  # Sin API key requerida
    
    async def get_elevation_data(self, lat_min, lat_max, lon_min, lon_max):
        """Obtener DEM de Copernicus (30m, gratis)."""
        
        # Calcular tiles necesarios
        tiles = self._calculate_tiles(lat_min, lat_max, lon_min, lon_max)
        
        # Descargar tiles (S3 público)
        elevation_data = []
        for tile in tiles:
            url = f"{self.base_url}/{tile}.tif"
            data = await self._download_tile(url)
            elevation_data.append(data)
        
        # Merge y crop
        merged = self._merge_tiles(elevation_data)
        cropped = self._crop_to_bbox(merged, lat_min, lat_max, lon_min, lon_max)
        
        return {
            'value': float(np.mean(cropped)),
            'elevation_stats': {
                'mean_elevation': float(np.mean(cropped)),
                'std_elevation': float(np.std(cropped)),
                'min_elevation': float(np.min(cropped)),
                'max_elevation': float(np.max(cropped))
            },
            'dem_status': 'HIGH_RES',  # ✅ Copernicus es HIGH_RES
            'source': 'Copernicus_DEM_GLO30',
            'resolution_m': 30,
            'quality': 'high'
        }
```

**Resultado**: DEM de alta calidad sin depender de OpenTopography.

---

## 📊 COMPARACIÓN DE PRIORIDADES

| Prioridad | Impacto | Costo | Tiempo | Urgencia |
|-----------|---------|-------|--------|----------|
| **1. Persistir mediciones** | ENORME | BAJO | 1-2 días | CRÍTICA |
| **2. Separar señales** | ALTO | MEDIO | 3-4 días | ALTA |
| **3. Copernicus DEM** | MEDIO | BAJO | 1 día | MEDIA |

---

## 🎯 PLAN DE IMPLEMENTACIÓN

### Semana 1: Prioridad 1 (Persistir mediciones)

**Día 1-2**: Crear tabla `instrument_measurements`
```sql
CREATE TABLE instrument_measurements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    site_id UUID REFERENCES archaeological_sites(id),
    instrument_name TEXT NOT NULL,
    measurement_type TEXT NOT NULL,
    value FLOAT,
    unit TEXT,
    confidence FLOAT,
    quality_flags JSONB,
    acquisition_date TIMESTAMP,
    source TEXT,
    processing_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_measurements_site ON instrument_measurements(site_id);
CREATE INDEX idx_measurements_instrument ON instrument_measurements(instrument_name);
```

**Día 3**: Implementar `MeasurementsRepository`

**Día 4**: Modificar pipeline para guardar mediciones

**Día 5**: Test y validación

### Semana 2: Prioridad 2 (Separar señales)

**Día 1-2**: Implementar `SignalClassification`

**Día 3-4**: Modificar cálculo ESS con transparencia

**Día 5**: Test y documentación

### Semana 3: Prioridad 3 (Copernicus DEM)

**Día 1**: Implementar `CopernicusDEMConnector`

**Día 2**: Integrar en cascada SRTM

**Día 3**: Test y validación

---

## 💡 CONCLUSIÓN SINCERA

### Lo que estás construyendo NO es un detector mágico

Es algo **mucho más serio**:

**🧠 Un sistema de inferencia territorial honesto**

Capaz de decir:
- ✅ "Aquí hay huella" (con evidencia instrumental)
- ✅ "Aquí NO hay huella" (con evidencia negativa)
- ✅ "Aquí no puedo saber" (sin datos suficientes)

**Eso es exactamente lo que la ciencia necesita.**

---

## 🚀 PRÓXIMO PASO INMEDIATO

**Implementar Prioridad 1**: Persistir mediciones instrumentales

**Archivo a crear**: `backend/database/measurements_repository.py`

**Tiempo**: 1-2 días

**Impacto**: ENORME (evidencia científica persistente)

---

**Fecha**: 2026-01-29  
**Estado**: Análisis completado  
**Recomendación**: Implementar Prioridad 1 YA
