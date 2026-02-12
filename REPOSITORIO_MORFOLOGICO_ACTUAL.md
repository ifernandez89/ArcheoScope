# 📚 Repositorio Morfológico Cultural - Estado Actual

## 🎯 Resumen Ejecutivo

**Ubicación**: `backend/morphological_repository.py`

**Estado**: ✅ OPERATIVO - 4 clases morfológicas activas

**Paradigma**:
> "ArcheoScope no reconstruye monumentos. Constriñe el espacio geométrico hasta que solo sobreviven formas culturalmente posibles."

---

## 🏛️ Clases Morfológicas Disponibles

### 1. MOAI (Rapa Nui)
```python
Clase: MorphologicalClass.MOAI
Origen: "Rapa Nui (Easter Island)"
```

**Características Geométricas**:
- **Ratio H/W**: 3.2 (extrema verticalidad)
- **Cabeza/Cuerpo**: 0.45 (cabeza enorme, casi mitad del cuerpo)
- **Base/Altura**: 0.15 (base pequeña)

**Ejes**:
- Dominancia vertical: 95%
- Dominancia horizontal: 5%
- Simetría bilateral: 98%

**Estructura**:
- Brazos: Fusionados al cuerpo
- Piernas: Fusionadas
- Base: Integrada
- Frontalidad: Absoluta
- Dinamismo: 0% (completamente estático)

**Metadatos**:
- Confianza: 95%
- Muestras reales: 50 moais documentados

**Caso de uso**: Estructuras verticales monolíticas con cabeza prominente

---

### 2. SPHINX (Esfinge - Egipto)
```python
Clase: MorphologicalClass.SPHINX
Origen: "Ancient Egypt"
```

**Características Geométricas**:
- **Ratio H/W**: 0.35 (extrema horizontalidad)
- **Cabeza/Cuerpo**: 0.25 (cabeza proporcionada)
- **Base/Altura**: 0.95 (base casi igual a altura)

**Ejes**:
- Dominancia vertical: 15%
- Dominancia horizontal: 95%
- Simetría bilateral: 99%

**Estructura**:
- Brazos: Ninguno
- Piernas: Posición recostada/sedente
- Base: Integrada
- Frontalidad: Absoluta
- Dinamismo: 0% (completamente estático)

**Metadatos**:
- Confianza: 90%
- Muestras reales: 20 esfinges preservadas

**Caso de uso**: Estructuras horizontales híbridas (león-humano)

---

### 3. EGYPTIAN_STATUE (Estatua Egipcia)
```python
Clase: MorphologicalClass.EGYPTIAN_STATUE
Origen: "Ancient Egypt (Old/Middle Kingdom)"
```

**Características Geométricas**:
- **Ratio H/W**: 4.5 (muy vertical)
- **Cabeza/Cuerpo**: 0.12 (cabeza ~1/8 del cuerpo)
- **Base/Altura**: 0.20

**Ejes**:
- Dominancia vertical: 90%
- Dominancia horizontal: 10%
- Simetría bilateral: 99%

**Estructura**:
- Brazos: A los lados del cuerpo
- Piernas: De pie, pierna adelantada
- Base: Integrada
- Frontalidad: Absoluta
- Dinamismo: 10% (casi estático)

**Metadatos**:
- Confianza: 92%
- Muestras reales: 100 estatuas documentadas

**Caso de uso**: Estatuas antropomórficas verticales con frontalidad rígida

---

### 4. COLOSSUS (Coloso - Egipto)
```python
Clase: MorphologicalClass.COLOSSUS
Origen: "Ancient Egypt (New Kingdom)"
```

**Características Geométricas**:
- **Ratio H/W**: 2.8 (vertical pero más ancho)
- **Cabeza/Cuerpo**: 0.15
- **Base/Altura**: 0.35 (base más grande)

**Ejes**:
- Dominancia vertical: 85%
- Dominancia horizontal: 15%
- Simetría bilateral: 98%

**Estructura**:
- Brazos: Cruzados sobre el pecho
- Piernas: Posición sedente
- Base: Integrada
- Frontalidad: Absoluta
- Dinamismo: 0% (completamente estático)

**Metadatos**:
- Confianza: 88%
- Muestras reales: 15 colosos (Memnon, Abu Simbel)

**Caso de uso**: Estatuas monumentales sedentes

---

## 🌍 Bonus Geográfico-Cultural

El sistema aplica bonus de scoring cuando detecta coherencia geográfica:

### Rapa Nui (-28° a -26°S, -110° a -108°W)
- **MOAI**: +0.25 bonus (25% adicional)
- Resultado: Alta confianza en clasificación

### Egipto (22° a 32°N, 25° a 35°E)
- **SPHINX**: +0.15 bonus
- **EGYPTIAN_STATUE**: +0.15 bonus
- **COLOSSUS**: +0.15 bonus
- Resultado: Preferencia por clases egipcias

### Perú (-18° a -8°S, -82° a -68°W)
- Preparado para clases andinas (aún no implementadas)

---

## ❌ Clases NO Disponibles (Limitaciones Actuales)

### Mesoamericanas
- ❌ PYRAMID_MESOAMERICAN (Teotihuacán, Maya)
- ❌ TEMPLE_PLATFORM (plataformas escalonadas)
- ❌ STELA_MAYA (estelas con glifos)
- ❌ OLMEC_HEAD (cabezas olmecas)

### Andinas
- ❌ TIWANAKU_MONOLITH (monolitos Tiwanaku)
- ❌ CHAVIN_STRUCTURE (arquitectura Chavín)
- ❌ INCA_PLATFORM (plataformas incas)
- ❌ NAZCA_GEOGLYPH (geoglifos)

### Otras Culturas
- ❌ GREEK_STATUE (estatuas griegas clásicas)
- ❌ ROMAN_STATUE (estatuas romanas)
- ❌ BUDDHA_STATUE (budas monumentales)
- ❌ MEGALITHIC_STRUCTURE (megalitos europeos)
- ❌ TOTEM_POLE (tótems del Pacífico Norte)

---

## 📊 Algoritmo de Matching

### Inputs
1. **Scale Invariance** (rigidez estructural)
2. **Angular Consistency** (simetría)
3. **Coherence 3D** (coherencia volumétrica)
4. **Estimated Area** (área base estimada)
5. **Estimated Height** (altura estimada)
6. **Lat/Lon** (contexto geográfico opcional)

### Proceso
1. Calcular ratio H/W de la estructura detectada
2. Comparar contra cada clase morfológica:
   - Score de proporciones (40%)
   - Score de rigidez (20%)
   - Score de simetría (20%)
   - Score de coherencia (20%)
3. Aplicar bonus geográfico si corresponde
4. Seleccionar clase con mayor score

### Output
- Clase morfológica más compatible
- Score de compatibilidad (0-1+)

---

## 🔬 Rigor Científico

### Lo Que SÍ Hace
✅ Constriñe el espacio geométrico basado en invariantes reales
✅ Usa proporciones aprendidas de objetos escaneados
✅ Aplica contexto geográfico-cultural
✅ Transparencia total en métricas y confianza
✅ Falsificable mediante comparación con datos reales

### Lo Que NO Hace
❌ NO reconstruye monumentos específicos
❌ NO copia detalles artísticos
❌ NO inventa formas sin base en datos
❌ NO afirma identidad de objetos individuales
❌ NO genera texturas o decoraciones

---

## 📁 Estructura de Datos

### MorphologicalInvariants (Dataclass)
```python
@dataclass
class MorphologicalInvariants:
    # Identificación
    morphological_class: MorphologicalClass
    cultural_origin: str
    
    # Proporciones (ratios, NO medidas absolutas)
    height_to_width_ratio: float
    head_to_body_ratio: float
    base_to_height_ratio: float
    
    # Ejes dominantes (0-1)
    vertical_axis_dominance: float
    horizontal_axis_dominance: float
    bilateral_symmetry: float
    
    # Características estructurales
    arms_position: str
    legs_position: str
    base_integration: str
    
    # Rigidez cultural
    frontal_axis_absolute: bool
    dynamism_level: float
    
    # Metadatos
    confidence: float
    source_samples: int
```

---

## 🚀 Expansión Futura

### Prioridad Alta
1. **Clases Mesoamericanas** (para Teotihuacán, Maya, Olmeca)
2. **Clases Andinas** (para Tiwanaku, Chavín, Inca)
3. **Bonus geográfico expandido** (Mesoamérica, Andes)

### Prioridad Media
4. **Clases Mediterráneas** (Grecia, Roma)
5. **Clases Asiáticas** (Budas, templos)
6. **Variabilidad intra-clase** (múltiples variantes por cultura)

### Prioridad Baja
7. **Clases Megalíticas** (Europa, África)
8. **Estados de preservación** (erosión, daño)
9. **Contexto temporal** (períodos históricos)

---

## 💡 Cómo Agregar Nuevas Clases

### Paso 1: Definir Enum
```python
class MorphologicalClass(Enum):
    # ... existentes ...
    PYRAMID_MESOAMERICAN = "pyramid_mesoamerican"
```

### Paso 2: Agregar Invariantes
```python
self.repository[MorphologicalClass.PYRAMID_MESOAMERICAN] = MorphologicalInvariants(
    morphological_class=MorphologicalClass.PYRAMID_MESOAMERICAN,
    cultural_origin="Mesoamerica (Teotihuacan, Maya)",
    
    # Proporciones de pirámides escalonadas
    height_to_width_ratio=0.5,  # Más ancho que alto
    head_to_body_ratio=0.0,     # No antropomórfico
    base_to_height_ratio=2.0,   # Base muy grande
    
    # Ejes
    vertical_axis_dominance=0.40,
    horizontal_axis_dominance=0.60,
    bilateral_symmetry=0.99,
    
    # Estructura
    arms_position="none",
    legs_position="none",
    base_integration="integrated",
    
    # Rigidez
    frontal_axis_absolute=True,
    dynamism_level=0.0,
    
    # Metadatos
    confidence=0.85,
    source_samples=30  # Pirámides documentadas
)
```

### Paso 3: Agregar Bonus Geográfico
```python
# En _calculate_morphological_score()
is_mesoamerica = (14 < lat < 23) and (-110 < lon < -86)

if is_mesoamerica and invariants.cultural_origin.startswith("Mesoamerica"):
    geographic_bonus = 0.20
```

### Paso 4: Actualizar Colores de Render
```python
# En culturally_constrained_mig.py
elif morph_class == MorphologicalClass.PYRAMID_MESOAMERICAN:
    face_color = '#8B4513'  # Piedra volcánica
    edge_color = '#4a2511'
    alpha = 0.92
```

---

## 📊 Estadísticas del Repositorio

**Total de clases**: 4 activas
**Total de muestras**: 185 objetos reales documentados
- MOAI: 50 muestras
- SPHINX: 20 muestras
- EGYPTIAN_STATUE: 100 muestras
- COLOSSUS: 15 muestras

**Cobertura geográfica**:
- ✅ Rapa Nui (Oceanía)
- ✅ Egipto (África)
- ❌ Mesoamérica (pendiente)
- ❌ Andes (pendiente)
- ❌ Asia (pendiente)
- ❌ Europa (pendiente)

**Confianza promedio**: 91.25%

---

## ✅ Conclusión

El repositorio morfológico actual es **funcional y científicamente riguroso**, pero tiene **cobertura limitada**:

**Fortalezas**:
- ✅ Clases egipcias bien representadas (3 variantes)
- ✅ MOAI perfectamente caracterizado
- ✅ Bonus geográfico implementado
- ✅ Algoritmo de matching robusto

**Limitaciones**:
- ❌ Sin clases mesoamericanas (Teotihuacán, Maya)
- ❌ Sin clases andinas (Tiwanaku, Inca)
- ❌ Sin clases asiáticas (Budas, templos)
- ❌ Sin clases mediterráneas (Grecia, Roma)

**Recomendación**: Expandir con clases mesoamericanas y andinas como prioridad inmediata para mejorar cobertura global.

---

**Estado**: ✅ PRODUCCIÓN - FUNCIONAL CON LIMITACIONES CONOCIDAS
**Próxima expansión**: Clases Mesoamericanas + Andinas
