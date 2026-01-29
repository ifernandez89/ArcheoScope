# Validación Contextual con Sitios Conocidos

## 🎯 Filosofía: Anclas Epistemológicas, NO Sensores

### ✅ Lo que SÍ hacen los sitios conocidos (sin mediciones):

1. **Definir "zonas normales" por contexto**
2. **Filtrar plausibilidad ambiental**
3. **Control negativo indirecto**
4. **Detectar comportamiento anómalo del algoritmo**
5. **Mantener al sistema honesto**

### ❌ Lo que NO hacen:

- NO son ground truth duro
- NO requieren mediciones satelitales históricas
- NO invalidan el enfoque
- NO bloquean el sistema
- NO son "sensores"

---

## 📊 Datos Genéricos Suficientes

Aunque solo tengas metadata básica:

```json
{
  "name": "Petra",
  "site_type": "CITY",
  "environment": "ARID",
  "terrain": "PLATEAU",
  "lat": 30.3285,
  "lon": 35.4444,
  "confidence": "HIGH",
  "has_documented_cavities": true
}
```

**Ya es útil para:**
- ¿En qué ambientes funcionan bien los detectores?
- ¿Dónde NO debería saltar una anomalía?
- ¿Qué entornos generan falsos positivos?

---

## 🔧 Usos Correctos

### 1️⃣ Filtro de Plausibilidad Ambiental

**Antes de analizar huecos:**

```python
if candidate.environment not in environments_seen_in_known_sites:
    penalize_score()
```

💡 **No afirma nada, reduce delirios.**

**Ejemplo:**
```
Candidata en: FOREST (selva densa)
Sitios conocidos: ARID (15), SEMI_ARID (8), PLATEAU (5)

→ Penalización: -15% al score
→ Razón: "Ambiente sin precedentes en sitios conocidos"
```

---

### 2️⃣ Control Negativo Indirecto (MUY útil)

**Idea clave:**

Si ArcheoScope marca anomalías de hueco fuerte:
- En sitios conocidos SIN cavidades documentadas
- En entornos donde nunca se excavó

➡️ **Algo está mal.**

```python
if known_site and void_score > threshold:
    flag_as_false_positive_candidate()
```

**Ejemplo:**
```
Candidata: lat=30.5, lon=35.2
Void Score: 0.82 (STRONG_VOID)

Sitios conocidos cercanos (radio 50km):
- "Jerash" (CITY, sin cavidades documentadas)
- "Umm Qais" (SETTLEMENT, sin cavidades documentadas)

→ Riesgo de falso positivo: 40%
→ Penalización: -20% al score
→ Score ajustado: 0.62 (PROBABLE_CAVITY)
```

---

### 3️⃣ Definir "Zonas Normales"

Aunque no tengas sensores históricos, sí tenés:
- Latitud
- Altitud aproximada
- Clima
- Tipo de suelo

**Construir rangos normales por contexto:**

```python
normal_context_profile = {
    "arid_plateau": {
        "expected_ndvi": (0.05, 0.20),
        "expected_thermal_variance": (2.0, 5.0),
        "expected_sar_noise": "low"
    },
    "mountain": {
        "expected_ndvi": (0.20, 0.50),
        "expected_thermal_variance": (3.0, 6.0),
        "expected_sar_noise": "medium"
    }
}
```

**Luego:**

```python
if candidate deviates_from normal_context_profile:
    anomaly += 1
```

**Esto es totalmente válido científicamente.**

---

### 4️⃣ Validación Blanda (Soft Validation)

**NO preguntar:** "¿Detecta el sitio?"

**SÍ preguntar:** "¿El comportamiento del algoritmo es razonable en lugares donde sabemos que hay arqueología humana?"

**Si:**
- ✅ No marca todo como hueco
- ✅ No explota en zonas obvias
- ✅ Se comporta con sobriedad

➡️ **El sistema es sano.**

**Ejemplo:**
```
Test en 50 sitios conocidos:
- 12 con cavidades documentadas → 10 detectados (83%)
- 38 sin cavidades documentadas → 5 falsos positivos (13%)

→ Sistema razonable
→ Ajustar umbral para reducir FP a <10%
```

---

## 🏗️ Implementación en ArcheoScope

### Tabla de BD: `known_archaeological_sites`

```sql
CREATE TABLE known_archaeological_sites (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    site_type VARCHAR(50),              -- temple, city, settlement, tomb, etc.
    environment VARCHAR(50),             -- arid, semi_arid, mountain, etc.
    terrain VARCHAR(50),                 -- plateau, valley, coastal, etc.
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    confidence_level VARCHAR(20),        -- HIGH, MEDIUM, LOW
    has_documented_cavities BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_known_sites_coords ON known_archaeological_sites (lat, lon);
CREATE INDEX idx_known_sites_env ON known_archaeological_sites (environment);
```

**NO requiere columnas de mediciones satelitales.**

---

### Módulo: `contextual_validator.py`

```python
from contextual_validator import contextual_validator

# Cargar sitios conocidos desde BD
contextual_validator.load_known_sites_from_db(db_connection)

# Validar candidata
validation = contextual_validator.validate_candidate(
    candidate_lat=30.0,
    candidate_lon=31.0,
    candidate_environment=EnvironmentType.ARID,
    candidate_terrain="plateau",
    void_detection_result=void_result
)

# Aplicar ajustes
adjusted_score = void_result.void_probability_score - validation.score_penalty
adjusted_confidence = void_result.confidence + validation.confidence_adjustment
```

---

## 📈 Resultados de Validación

### ValidationResult

```python
@dataclass
class ValidationResult:
    is_plausible: bool
    plausibility_score: float
    
    # Filtros
    environment_seen_before: bool
    terrain_compatible: bool
    context_deviation: float
    
    # Controles negativos
    false_positive_risk: float
    similar_known_sites_without_cavities: int
    
    # Ajustes
    score_penalty: float           # 0.0 - 0.15 (CAP para evitar sesgo)
    confidence_adjustment: float   # -0.5 - 0.0 (Sobre confianza epistémica)
    
    # Explicación
    validation_notes: str
```

### Ejemplo de Output

```
📋 VALIDACIÓN CONTEXTUAL:
   Plausibilidad: 0.725
   Es plausible: SÍ
   Ambiente visto antes: ✓
   Terreno compatible: ✓
   Desviación de contexto: 0.15
   Riesgo de falso positivo: 0.20
   Sitios cercanos sin cavidades: 2

   AJUSTES RECOMENDADOS:
   Penalización al score: -7.5%
   Ajuste de confianza epistémica: -10.0%

   NOTAS:
   ✓ Ambiente visto en sitios conocidos | ✓ Terreno compatible

   SCORES AJUSTADOS:
   Score original: 0.78 → Ajustado: 0.68
   Confianza original: 75% → Ajustada: 65%
```

---

## 🎯 Casos de Uso

### Caso 1: Ambiente Conocido, Sin Falsos Positivos

```
Candidata: Desierto de Atacama (ARID)
Sitios conocidos en ARID: 15

Validación:
✓ Ambiente visto antes
✓ Terreno compatible (plateau)
✓ Baja desviación de contexto (0.12)
✓ Sin sitios cercanos sin cavidades

Ajustes:
- Penalización: 0%
- Ajuste de confianza: 0%

→ Score se mantiene
```

### Caso 2: Ambiente Nuevo, Penalización Moderada

```
Candidata: Bosque templado (FOREST)
Sitios conocidos en FOREST: 0

Validación:
✗ Ambiente sin precedentes
✗ Terreno incompatible
⚠️ Alta desviación de contexto (0.65)

Ajustes:
- Penalización: -15% (MAX CAP)
- Ajuste de confianza epistémica: -20%

→ Score: 0.75 → 0.50 (AMBIGUOUS)
```

### Caso 3: Alto Riesgo de Falso Positivo

```
Candidata: Cerca de Petra (ARID, PLATEAU)
Void Score: 0.85

Sitios conocidos cercanos:
- Petra (CITY, sin cavidades documentadas)
- Little Petra (SETTLEMENT, sin cavidades documentadas)
- Beidha (SETTLEMENT, sin cavidades documentadas)

Validación:
✓ Ambiente visto antes
✓ Terreno compatible
⚠️ 3 sitios cercanos sin cavidades
⚠️ Riesgo de FP: 60%

Ajustes:
- Penalización: -15% (MAX CAP)
- Ajuste de confianza epistémica: -15%

→ Score: 0.85 → 0.55 (AMBIGUOUS)
→ Requiere validación adicional
```

---

## 🚀 Roadmap de Evolución

### Etapa Actual (Donde estás ahora)

✅ Sitios genéricos (solo metadata)  
✅ Sensores públicos actuales  
✅ Inferencia física indirecta  
✅ Validación contextual

**Perfecto. No te frena.**

### Próxima Etapa (Cuando todo camine)

1. **Generar tus propias mediciones derivadas**
   - Procesar datos satelitales para cada sitio conocido
   - Guardar en tabla `known_sites_measurements`

2. **Esas SÍ pasan a ser tu "ground truth interno"**
   - Comparar candidatas con mediciones reales de sitios conocidos
   - Ajustar pesos basado en resultados

3. **Vos estás creando el dataset que hoy no existe**
   - Cada análisis validado → nuevo dato
   - Sistema aprende de sus propios resultados

---

## ✅ Conclusión

### No tener mediciones en la BD:

❌ **NO te frena**  
❌ **NO invalida nada**  
✅ **Te obliga a hacer las cosas bien**

### Tus sitios conocidos:

👉 **Sirven como marco contextual y control epistemológico, NO como sensores.**

### Esto es científicamente más honesto que:

- Afirmar detección sin validación
- Usar ML supervisado sin ground truth real
- Ignorar el contexto arqueológico

---

## 🧪 Testing

```bash
# 1. Migración de BD
python apply_void_detection_migration.py

# 2. Poblar sitios conocidos (ejemplo)
psql -d archeoscope -c "
INSERT INTO known_archaeological_sites 
(name, site_type, environment, terrain, lat, lon, confidence_level, has_documented_cavities)
VALUES
('Petra', 'city', 'arid', 'plateau', 30.3285, 35.4444, 'HIGH', true),
('Jerash', 'city', 'semi_arid', 'plateau', 32.2719, 35.8906, 'HIGH', false),
('Palmyra', 'city', 'arid', 'desert', 34.5561, 38.2692, 'HIGH', false);
"

# 3. Test con validación contextual
python test_void_detection_with_db.py --lat 30.0 --lon 31.0
```

---

**Preparado para mantener al sistema honesto y científicamente riguroso.**
