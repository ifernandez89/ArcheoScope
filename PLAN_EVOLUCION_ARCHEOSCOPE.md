# Plan de Evolución de ArcheoScope - Roadmap Científico

**Fecha**: 2026-01-28  
**Estado Actual**: v2.2 - Sistema Maduro y Honesto  
**Techo Actual**: ESS ~0.55-0.60 (honesto)  
**Objetivo**: ESS ~0.60-0.65 (sin mentir)

---

## 🎯 Filosofía del Plan

### No es "Subir Scores"

Es **detectar historia, no cosas**.

### Principios

```
✅ Inferir profundidad sin sísmica física
✅ Multi-temporalidad sin Big Data
✅ Cambiar ambiente inteligentemente
✅ Analizar relaciones, no solo lugares
✅ Definir cuándo NO hay nada (poder negativo)
```

---

## 🚀 SALTO 1: Profundidad Inferida (Deep Inference Layer - DIL)

### Concepto

**No siempre necesitás GPR o sísmica física.**

Podés inferir profundidad combinando fuentes débiles coherentes.

### Cómo Funciona

Crear una capa "profunda" sintética cuando:

```
✅ SAR pierde coherencia
✅ Térmico persiste
✅ NDVI fluctúa
✅ Humedad histórica es estable
```

### Implementación

#### Fuentes a Integrar

1. **Sentinel-1 (multi-ángulo)**
   - Coherencia temporal
   - Pérdida de fase
   - Backscatter anómalo

2. **Landsat térmico nocturno**
   - Inercia térmica
   - Persistencia nocturna
   - Contraste día/noche

3. **NDWI / MNDWI**
   - Índice de agua normalizado
   - Humedad subsuperficial
   - Variación estacional

4. **Curvatura DEM** (cuando SRTM vuelva)
   - Micro-topografía
   - Anomalías de drenaje
   - Acumulación de flujo

#### Algoritmo DIL

```python
def calculate_deep_inference_layer(sar_coherence, thermal_persistence, 
                                   ndvi_variance, moisture_stability):
    """
    Calcular capa de profundidad inferida.
    
    No es "profundidad real"
    Pero se comporta como estructura enterrada difusa
    """
    
    # Pérdida de coherencia SAR (indica cambio subsuperficial)
    sar_loss = 1.0 - sar_coherence
    
    # Persistencia térmica (indica masa enterrada)
    thermal_factor = thermal_persistence
    
    # Variación NDVI (indica estrés vegetal sobre estructura)
    ndvi_stress = ndvi_variance
    
    # Estabilidad de humedad (indica drenaje alterado)
    moisture_factor = moisture_stability
    
    # Combinar con pesos
    dil_score = (
        sar_loss * 0.35 +
        thermal_factor * 0.30 +
        ndvi_stress * 0.20 +
        moisture_factor * 0.15
    )
    
    return dil_score
```

### Resultado Esperado

```
ESS Volumétrico: 0.55-0.60 (sin mentir ni inflar)
```

**Por qué funciona**: Múltiples señales débiles coherentes = señal fuerte inferida.

---

## 🚀 SALTO 2: Multi-Temporalidad Real (Temporal Archaeological Signature - TAS)

### Concepto

**Hoy usás escenas. Lo siguiente es trayectorias.**

### En Vez De

```
NDVI(t) → valor puntual
```

### Usar

```
ΔNDVI / Δt  → tasa de cambio (años)
Persistencia térmica → memoria enterrada
Frecuencia de estrés vegetal → uso humano prolongado
```

### Implementación Práctica

#### Fuentes Temporales

1. **Sentinel-2: 2016 → hoy**
   - 1 escena / estación (4 por año)
   - NDVI, NDWI, SWIR

2. **Landsat: 2000 → hoy**
   - 1 anual (20+ años)
   - Térmico, multispectral

3. **SAR: 2017 → hoy**
   - Húmedo vs seco
   - Coherencia temporal

#### Algoritmo TAS

```python
def calculate_temporal_archaeological_signature(time_series_data):
    """
    Calcular firma arqueológica temporal.
    
    Detecta:
    - Zonas que siempre reaccionan distinto
    - Memoria enterrada
    - Uso humano prolongado
    """
    
    # Extraer series temporales
    ndvi_series = time_series_data['ndvi']  # [2016-2026]
    thermal_series = time_series_data['thermal']  # [2000-2026]
    sar_series = time_series_data['sar']  # [2017-2026]
    
    # 1. Persistencia de anomalía NDVI
    ndvi_persistence = calculate_persistence(ndvi_series)
    
    # 2. Estabilidad térmica (baja varianza = masa enterrada)
    thermal_stability = 1.0 - np.std(thermal_series) / np.mean(thermal_series)
    
    # 3. Coherencia SAR temporal
    sar_coherence = calculate_temporal_coherence(sar_series)
    
    # 4. Frecuencia de estrés vegetal
    stress_frequency = count_stress_events(ndvi_series) / len(ndvi_series)
    
    # Combinar
    tas_score = (
        ndvi_persistence * 0.30 +
        thermal_stability * 0.30 +
        sar_coherence * 0.25 +
        stress_frequency * 0.15
    )
    
    return tas_score

def calculate_persistence(series):
    """Calcular persistencia de anomalía."""
    mean = np.mean(series)
    std = np.std(series)
    
    # Contar cuántas veces está fuera de 1 std
    anomalies = np.abs(series - mean) > std
    persistence = np.sum(anomalies) / len(series)
    
    return persistence

def count_stress_events(ndvi_series):
    """Contar eventos de estrés vegetal."""
    threshold = np.percentile(ndvi_series, 25)  # 25% más bajo
    stress_events = np.sum(ndvi_series < threshold)
    return stress_events
```

### Qué Detecta

```
✅ Zonas que siempre reaccionan distinto
✅ Memoria enterrada (persistencia térmica)
✅ Uso humano prolongado (estrés vegetal recurrente)
```

### Resultado Esperado

```
No sube ruido
Sube credibilidad
Desbloquea patrones invisibles en single-shot
```

---

## 🚀 SALTO 3: Cambiar Ambiente Inteligentemente

### No Ir "A Lo Extremo" al Azar

**Ir donde el sistema brilla.**

### Ambientes Ideales para ArcheoScope

| Ambiente | Por Qué Es Oro | ESS Esperado |
|----------|----------------|--------------|
| **Desierto hiperárido** | NDVI ≈ 0 → cualquier señal resalta | 0.65-0.75 |
| **Sabkhas / salares** | Contraste térmico brutal | 0.60-0.70 |
| **Tells urbanos** | Estratigrafía humana pura | 0.70-0.80 |
| **Paleocauces fósiles** | Memoria hídrica profunda | 0.55-0.65 |
| **Oasis antiguos** | Vegetación artificial histórica | 0.60-0.70 |

### Ejemplos Concretos (La Yugular)

#### 1. Atacama Interior (Chile)
```
Coordenadas: -23.5, -68.2
Por qué: Desierto más árido del mundo
Esperado: ESS > 0.65
```

#### 2. Mesopotamia (Irak)
```
Coordenadas: 33.3, 44.4
Por qué: Tells urbanos milenarios
Esperado: ESS > 0.70
```

#### 3. Delta del Indo (Pakistán)
```
Coordenadas: 26.0, 68.5
Por qué: Paleocauces + tells
Esperado: ESS > 0.65
```

#### 4. Sahara Central (Argelia)
```
Coordenadas: 26.0, 3.0
Por qué: Paleolago + arte rupestre
Esperado: ESS > 0.60
```

#### 5. Cuenca del Tarim (China)
```
Coordenadas: 40.0, 85.0
Por qué: Oasis antiguos + Ruta de la Seda
Esperado: ESS > 0.65
```

**Ahí ESS > 0.6 sin trucos.**

---

## 🚀 SALTO 4: Cambiar la Unidad de Análisis (Archaeological Gradient Network - AGN)

### Concepto

**Hoy analizás lugares. Lo siguiente es analizar relaciones.**

### En Vez De

```
"¿Hay algo acá?"
```

### Pasar A

```
"¿Este lugar conecta con otros de forma no natural?"
```

### Cómo Funciona

#### Construir Grafos

```python
def build_archaeological_gradient_network(sites):
    """
    Construir red de gradientes arqueológicos.
    
    Analiza relaciones entre sitios, no sitios aislados.
    """
    
    graph = nx.Graph()
    
    for site_a in sites:
        for site_b in sites:
            if site_a == site_b:
                continue
            
            # Calcular gradientes
            water_gradient = calculate_water_accessibility(site_a, site_b)
            slope_gradient = calculate_slope_between(site_a, site_b)
            visibility = calculate_intervisibility(site_a, site_b)
            accessibility = calculate_cost_distance(site_a, site_b)
            
            # Detectar conexión improbable
            if is_improbable_connection(water_gradient, slope_gradient, 
                                       visibility, accessibility):
                # Agregar arista
                graph.add_edge(site_a.id, site_b.id, 
                             weight=calculate_connection_strength(...))
    
    return graph

def is_improbable_connection(water, slope, visibility, accessibility):
    """
    Detectar nodos improbables (conexión humana intencional).
    
    Improbable = conectados a pesar de:
    - Sin agua entre ellos
    - Pendiente alta
    - No visibles entre sí
    - Pero accesibles (camino)
    """
    
    improbable = (
        water < 0.3 and  # Sin agua
        slope > 0.6 and  # Pendiente alta
        visibility < 0.4 and  # No visibles
        accessibility > 0.5  # Pero accesibles
    )
    
    return improbable
```

### Qué Detecta

```
✅ Sistemas humanos (no sitios aislados)
✅ Redes de caminos antiguos
✅ Jerarquías de asentamientos
✅ Conexiones intencionales vs naturales
```

### Resultado

```
No sube ESS puntual
Pero revela sistemas humanos complejos
```

---

## 🚀 SALTO 5: Cuándo NO Detectar (Negative Archaeology Layer - NAL)

### Concepto (Muy Poderoso)

**Definir formalmente: "Acá NO hay nada, con alta confianza"**

### Implementación

```python
def calculate_negative_archaeology_layer(etp):
    """
    Capa de arqueología negativa.
    
    Territorios:
    - Estables
    - Sin ruptura
    - Sin memoria
    - Sin persistencia
    
    Alta confianza en AUSENCIA.
    """
    
    # Criterios de ausencia confiable
    stable = etp.ess_volumetrico < 0.25
    no_rupture = etp.coherencia_3d > 0.7  # Muy coherente = natural
    no_memory = etp.persistencia_temporal < 0.3
    good_coverage = etp.instrumental_coverage_total > 0.6
    
    if stable and no_rupture and no_memory and good_coverage:
        return {
            'negative_confidence': 0.85,
            'reason': 'territorio_estable_sin_evidencia',
            'recommendation': 'no_re_analizar'
        }
    
    return None
```

### Qué Permite

```
✅ Contrastar (sitios vs no-sitios)
✅ Validar (sistema no inventa)
✅ Publicar ciencia seria (negativos confiables)
```

### Paradoja Poderosa

**Cuando sí detectás algo, es más creíble.**

---

## 🎯 ¿Hasta Dónde Puede Llegar ArcheoScope?

### Con Estos Saltos

```
ESS Volumétrico honesto:  0.60-0.65
Anomalías:                Pocas, débiles, reales
Coherencia:               Controlada
Falsos positivos:         Mínimos
```

### Pero Lo Más Importante

```
No detectás "cosas"
Detectás historia
```

---

## 📋 Recomendación de Orden (Práctico)

### Fase 1: Temporal (Inmediato)
```
1. Implementar Temporal Archaeological Signature (TAS)
   - Sentinel-2: 2016-2026 (10 años)
   - Landsat: 2000-2026 (26 años)
   - SAR: 2017-2026 (9 años)
   
   Esfuerzo: 2-3 semanas
   Impacto: Alto (desbloquea patrones temporales)
```

### Fase 2: Profundidad Inferida (Corto Plazo)
```
2. Agregar Deep Inference Layer (DIL)
   - Coherencia SAR temporal
   - Inercia térmica nocturna
   - NDWI/MNDWI
   - Curvatura DEM
   
   Esfuerzo: 1-2 semanas
   Impacto: Medio-Alto (sube ESS 0.05-0.10)
```

### Fase 3: Ambiente Extremo (Validación)
```
3. Probar en ambiente extremo real
   - Atacama interior
   - Mesopotamia
   - Sahara central
   
   Esfuerzo: 1 semana (testing)
   Impacto: Validación científica
```

### Fase 4: Relaciones (Largo Plazo)
```
4. Implementar Archaeological Gradient Network (AGN)
   - Grafos de conectividad
   - Nodos improbables
   - Sistemas humanos
   
   Esfuerzo: 3-4 semanas
   Impacto: Cambio conceptual (lugares → sistemas)
```

### Fase 5: Negativo (Madurez)
```
5. Implementar Negative Archaeology Layer (NAL)
   - Criterios de ausencia confiable
   - Territorio agotado
   - Publicación científica
   
   Esfuerzo: 1 semana
   Impacto: Credibilidad científica
```

---

## 📊 Roadmap Visual

```
v2.2 (Actual)
  ↓
  ├─→ TAS (Temporal) ────────────→ v2.3 (ESS +0.05)
  │                                   ↓
  ├─→ DIL (Profundidad Inferida) ──→ v2.4 (ESS +0.10)
  │                                   ↓
  ├─→ Ambiente Extremo ─────────────→ v2.5 (Validación)
  │                                   ↓
  ├─→ AGN (Relaciones) ─────────────→ v3.0 (Cambio conceptual)
  │                                   ↓
  └─→ NAL (Negativo) ───────────────→ v3.1 (Madurez científica)
```

---

## 🎯 Objetivo Final

### ArcheoScope v3.1

```
Capacidades:
✅ Multi-temporal (10-26 años)
✅ Profundidad inferida (sin sísmica)
✅ Ambientes extremos validados
✅ Análisis de sistemas (no solo sitios)
✅ Arqueología negativa (ausencia confiable)

Métricas:
ESS Volumétrico:  0.60-0.65 (honesto)
Falsos positivos: < 5%
Cobertura:        70-80%
Credibilidad:     Publicable

Filosofía:
No detecta "cosas"
Detecta "historia"
```

---

## 📚 Referencias Conceptuales

### Deep Inference Layer
> "Múltiples señales débiles coherentes = señal fuerte inferida"

### Temporal Archaeological Signature
> "No escenas, trayectorias. No momentos, memoria."

### Archaeological Gradient Network
> "No lugares, relaciones. No sitios, sistemas."

### Negative Archaeology Layer
> "Poder decir 'no hay nada' con confianza es tan valioso  
> como decir 'hay algo'."

---

**Elaborado por**: Kiro AI Assistant + Usuario  
**Fecha**: 2026-01-28  
**Versión**: Plan de Evolución v1.0  
**Estado**: 📋 DOCUMENTADO Y LISTO PARA IMPLEMENTACIÓN

---

## 🎉 Conclusión

**Este plan no busca inflar scores.**

**Busca detectar historia de forma más profunda, temporal y relacional.**

**Sin mentir. Sin trucos. Solo ciencia mejor.**

Y eso es lo único que importa.
