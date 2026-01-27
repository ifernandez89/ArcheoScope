# Plan de Validación del Sistema - 2026-01-26

## 🎯 Objetivo

Validar ArcheoScope con sitios arqueológicos conocidos para demostrar:
1. Capacidad de detección
2. Precisión de instrumentos
3. Convergencia instrumental
4. Ausencia de falsos positivos

## 📋 Tests Prioritarios

### Test 1: Giza, Egipto ⭐⭐⭐ CRÍTICO

**Coordenadas**:
```
Centro: 29.9792°N, 31.1342°E
Bbox:
  lat_min: 29.97
  lat_max: 29.99
  lon_min: 31.13
  lon_max: 31.15
```

**Ambiente esperado**: `desert`

**Instrumentos esperados**:
- ✅ MODIS LST (contraste térmico alto)
- ✅ Sentinel-2 (NDVI bajo, estructuras visibles)
- ✅ OpenTopography DEM (pirámides claras)
- ✅ Sentinel-1 SAR (geometría no natural)

**Expectativa**:
- Convergencia: 4-5 instrumentos
- Probabilidad: 70-90%
- Tiempo: 40-70s (sin SAR), 3-5min (con SAR)

**Comando de test**:
```bash
# Sin SAR (rápido)
python test_giza_simple.py

# Con SAR (completo)
SAR_ENABLED=true python test_giza_complete.py
```

**Criterio de éxito**:
- ✅ Convergencia ≥ 3 instrumentos
- ✅ Probabilidad ≥ 60%
- ✅ Ambiente = desert
- ✅ Tiempo < 2min (sin SAR)

---

### Test 2: Angkor Wat, Camboya ⭐⭐⭐ CRÍTICO

**Coordenadas**:
```
Centro: 13.4125°N, 103.8670°E
Bbox:
  lat_min: 13.40
  lat_max: 13.42
  lon_min: 103.86
  lon_max: 103.88
```

**Ambiente esperado**: `forest`

**Instrumentos esperados**:
- ✅ Sentinel-1 SAR (penetra vegetación) **CRÍTICO**
- ✅ Sentinel-2 NDVI (vegetación anómala)
- ✅ MODIS LST (contraste térmico)
- ✅ OpenTopography DEM (estructuras)

**Expectativa**:
- Convergencia: 3-4 instrumentos
- Probabilidad: 60-80%
- Tiempo: 50-80s (sin SAR), 3-5min (con SAR)
- **SAR es crítico** - sin SAR, convergencia baja

**Comando de test**:
```bash
# Sin SAR (limitado)
python test_angkor_simple.py

# Con SAR (RECOMENDADO)
SAR_ENABLED=true python test_angkor_complete.py
```

**Criterio de éxito**:
- ✅ Con SAR: Convergencia ≥ 3 instrumentos
- ✅ Con SAR: Probabilidad ≥ 50%
- ✅ Sin SAR: Convergencia ≥ 2 instrumentos
- ✅ Ambiente = forest

---

### Test 3: Machu Picchu, Perú ⭐⭐ IMPORTANTE

**Coordenadas**:
```
Centro: -13.1631°S, -72.5450°W
Bbox:
  lat_min: -13.17
  lat_max: -13.16
  lon_min: -72.55
  lon_max: -72.54
```

**Ambiente esperado**: `mountain`

**Instrumentos esperados**:
- ✅ ICESat-2 (terrazas, pendientes)
- ✅ Sentinel-1 SAR (estructuras)
- ✅ OpenTopography DEM (topografía modificada)
- ⚠️ Sentinel-2 (vegetación variable)

**Expectativa**:
- Convergencia: 2-3 instrumentos
- Probabilidad: 50-70%
- Tiempo: 30-60s (sin SAR), 3-5min (con SAR)
- **Comparar con Patagonia** (mismo ambiente)

**Comando de test**:
```bash
# Sin SAR
python test_machu_picchu_simple.py

# Con SAR
SAR_ENABLED=true python test_machu_picchu_complete.py
```

**Criterio de éxito**:
- ✅ Convergencia ≥ 2 instrumentos
- ✅ Probabilidad ≥ 40%
- ✅ Ambiente = mountain
- ✅ Mejor que Patagonia (más instrumentos válidos)

---

### Test 4: Patagonia + SAR ⭐ OPCIONAL

**Coordenadas**:
```
Centro: -50.4760°S, -73.0450°W
Bbox:
  lat_min: -50.55
  lat_max: -50.40
  lon_min: -73.15
  lon_max: -72.90
```

**Ambiente esperado**: `mountain`

**Instrumentos esperados**:
- ⚠️ ICESat-2 (calidad variable)
- ✅ Sentinel-1 SAR (estructuras)
- ⚠️ OpenTopography DEM (resolución limitada)

**Expectativa**:
- Convergencia: 1-2 instrumentos (con SAR)
- Probabilidad: 30-50%
- Tiempo: 3-5min (con SAR)

**Comando de test**:
```bash
# Con SAR (único modo útil)
SAR_ENABLED=true python test_patagonia_candidato_001_final.py
```

**Criterio de éxito**:
- ✅ SAR mide correctamente
- ✅ Convergencia ≥ 1 instrumento
- ✅ Probabilidad > 31.2% (mejora vs sin SAR)

---

## 📊 Matriz de Validación

| Test | Prioridad | Tiempo | Convergencia Esperada | Prob. Esperada | SAR Crítico |
|------|-----------|--------|----------------------|----------------|-------------|
| Giza | ⭐⭐⭐ | 40-70s | 4-5 | 70-90% | No |
| Angkor | ⭐⭐⭐ | 50-80s | 3-4 | 60-80% | Sí |
| Machu Picchu | ⭐⭐ | 30-60s | 2-3 | 50-70% | Recomendado |
| Patagonia+SAR | ⭐ | 3-5min | 1-2 | 30-50% | Sí |

## 🔧 Scripts de Test a Crear

### test_giza_simple.py
```python
#!/usr/bin/env python3
"""Test Giza - Validación completa del sistema"""

import requests
import json
from datetime import datetime

def test_giza():
    data = {
        "lat_min": 29.97,
        "lat_max": 29.99,
        "lon_min": 31.13,
        "lon_max": 31.15,
        "region_name": "Giza Plateau, Egypt"
    }
    
    print("=" * 80)
    print("TEST GIZA - VALIDACION COMPLETA")
    print("=" * 80)
    
    start = datetime.now()
    response = requests.post("http://localhost:8002/analyze", json=data, timeout=180)
    elapsed = (datetime.now() - start).total_seconds()
    
    if response.status_code == 200:
        result = response.json()
        
        # Guardar resultado
        with open(f"giza_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        # Validar
        env = result.get('environment_classification', {}).get('environment_type')
        prob = result.get('archaeological_results', {}).get('archaeological_probability', 0)
        conv = result.get('convergence_analysis', {}).get('instruments_converging', 0)
        
        print(f"\nRESULTADO:")
        print(f"  Ambiente: {env}")
        print(f"  Probabilidad: {prob*100:.1f}%")
        print(f"  Convergencia: {conv} instrumentos")
        print(f"  Tiempo: {elapsed:.1f}s")
        
        # Criterios de éxito
        success = (
            env == 'desert' and
            prob >= 0.6 and
            conv >= 3 and
            elapsed < 120
        )
        
        print(f"\nVALIDACION: {'✅ EXITO' if success else '❌ FALLO'}")
        return success
    else:
        print(f"ERROR: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_giza()
    exit(0 if success else 1)
```

### test_angkor_complete.py
```python
#!/usr/bin/env python3
"""Test Angkor - Validación SAR en selva"""

import requests
import json
from datetime import datetime
import os

def test_angkor():
    # Verificar SAR habilitado
    sar_enabled = os.getenv("SAR_ENABLED", "false").lower() == "true"
    if not sar_enabled:
        print("⚠️  SAR no habilitado. Ejecutar con: SAR_ENABLED=true python test_angkor_complete.py")
        return False
    
    data = {
        "lat_min": 13.40,
        "lat_max": 13.42,
        "lon_min": 103.86,
        "lon_max": 103.88,
        "region_name": "Angkor Wat, Cambodia"
    }
    
    print("=" * 80)
    print("TEST ANGKOR - VALIDACION SAR EN SELVA")
    print("=" * 80)
    print("SAR: HABILITADO ✅")
    
    start = datetime.now()
    response = requests.post("http://localhost:8002/analyze", json=data, timeout=300)
    elapsed = (datetime.now() - start).total_seconds()
    
    if response.status_code == 200:
        result = response.json()
        
        # Guardar resultado
        with open(f"angkor_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        # Validar
        env = result.get('environment_classification', {}).get('environment_type')
        prob = result.get('archaeological_results', {}).get('archaeological_probability', 0)
        conv = result.get('convergence_analysis', {}).get('instruments_converging', 0)
        measurements = result.get('instrumental_measurements', [])
        
        # Verificar que SAR midió
        sar_measured = any('sar' in str(m).lower() for m in measurements)
        
        print(f"\nRESULTADO:")
        print(f"  Ambiente: {env}")
        print(f"  Probabilidad: {prob*100:.1f}%")
        print(f"  Convergencia: {conv} instrumentos")
        print(f"  SAR midió: {'✅' if sar_measured else '❌'}")
        print(f"  Tiempo: {elapsed:.1f}s")
        
        # Criterios de éxito
        success = (
            env == 'forest' and
            prob >= 0.5 and
            conv >= 3 and
            sar_measured
        )
        
        print(f"\nVALIDACION: {'✅ EXITO' if success else '❌ FALLO'}")
        return success
    else:
        print(f"ERROR: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_angkor()
    exit(0 if success else 1)
```

## 📅 Cronograma de Ejecución

### Semana 1 (Inmediato)

**Día 1-2**:
- [ ] Crear scripts de test (Giza, Angkor, Machu Picchu)
- [ ] Test Giza sin SAR
- [ ] Documentar resultados

**Día 3-4**:
- [ ] Test Angkor con SAR
- [ ] Comparar con Giza
- [ ] Documentar diferencias

**Día 5**:
- [ ] Test Machu Picchu sin SAR
- [ ] Comparar con Patagonia
- [ ] Resumen semanal

### Semana 2 (Profundización)

**Día 1-2**:
- [ ] Re-test Giza con SAR
- [ ] Re-test Machu Picchu con SAR
- [ ] Análisis comparativo

**Día 3-4**:
- [ ] Test Patagonia con SAR
- [ ] Optimizar ICESat-2 (manejo inf/nan)
- [ ] Documentar mejoras

**Día 5**:
- [ ] Informe final de validación
- [ ] Recomendaciones para producción
- [ ] Plan de publicación

## ✅ Criterios de Éxito Global

### Sistema Validado Si:

1. **Giza**: ✅ Convergencia ≥ 3, Probabilidad ≥ 60%
2. **Angkor**: ✅ Con SAR: Convergencia ≥ 3, Probabilidad ≥ 50%
3. **Machu Picchu**: ✅ Convergencia ≥ 2, Probabilidad ≥ 40%
4. **Sin falsos positivos**: ✅ Zonas naturales < 30% probabilidad

### Sistema Listo para Producción Si:

- ✅ 3/3 tests críticos pasan
- ✅ Tiempo promedio < 2min (sin SAR)
- ✅ Documentación completa
- ✅ Reproducibilidad 100%

## 📝 Plantilla de Reporte

```markdown
# Reporte de Validación - [Sitio]

## Datos del Test
- Fecha: [fecha]
- Sitio: [nombre]
- Coordenadas: [bbox]
- SAR: [habilitado/deshabilitado]

## Resultados
- Ambiente detectado: [tipo] ([confianza]%)
- Probabilidad arqueológica: [valor]%
- Convergencia: [n]/[requerido] instrumentos
- Tiempo: [segundos]s

## Instrumentos
- [Instrumento 1]: [valor] [unidad] (umbral: [threshold])
- [Instrumento 2]: [valor] [unidad] (umbral: [threshold])
...

## Validación
- ✅/❌ Ambiente correcto
- ✅/❌ Convergencia alcanzada
- ✅/❌ Probabilidad esperada
- ✅/❌ Tiempo aceptable

## Conclusión
[Análisis del resultado]

## Archivos
- JSON: [filename]
- Logs: [filename]
```

---

**Fecha**: 2026-01-26  
**Estado**: Plan definido, listo para ejecución  
**Próximo paso**: Crear scripts de test y ejecutar Giza
