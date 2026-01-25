# ArcheoScope - 4 Sitios de Referencia para Calibración

## Fecha: 24 de Enero de 2026

---

## FILOSOFÍA: Simplicidad y Enfoque

En lugar de mantener una base de datos masiva de 50+ sitios arqueológicos, **ArcheoScope usa 4 sitios de referencia** - uno por cada ambiente crítico:

1. **DESIERTO** → Giza Pyramids (Egipto)
2. **VEGETACIÓN** → Angkor Wat (Camboya)
3. **HIELO** → Ötzi the Iceman (Alpes)
4. **AGUA** → Port Royal (Jamaica)

Estos 4 sitios sirven como **puntos de calibración** para verificar que:
- La clasificación de ambientes funciona correctamente
- Los instrumentos recomendados son apropiados
- La detección arqueológica es precisa
- La exclusión moderna está activa

---

## 1. SITIO DE REFERENCIA: DESIERTO

### Giza Pyramids Complex (Egipto)

**Coordenadas**: 29.9792°N, 31.1342°E

#### Ambiente
- **Tipo**: Desierto del Sahara
- **Características**: Árido, vegetación mínima, alta visibilidad arqueológica
- **Preservación**: Excelente (clima seco)

#### Instrumental Especializado
**Sensores Primarios**:
- Landsat Thermal (30m) - Anomalías térmicas día/noche
- Sentinel-2 (10m) - Firmas espectrales
- SAR Sentinel-1 (10m) - Penetración subsuperficial

**Por qué funciona**:
- Estructuras de piedra retienen calor diferente que arena
- Contraste térmico alto (ΔT = 10-15°C)
- SAR penetra arena seca
- Geometría rectangular clara

#### Datos Arqueológicos
- **Período**: Reino Antiguo de Egipto (2580-2560 BCE)
- **Tipo**: Complejo monumental
- **Área**: 2.5 km²
- **Características**: Gran Pirámide, Esfinge, templos, calzadas
- **UNESCO**: World Heritage Site #86

#### Condiciones de Detección Esperadas
```python
{
  "environment_detected": "desert",
  "confidence": 0.95,
  "archaeological_probability": 0.80-0.90,
  "site_recognized": True,
  "modern_exclusion_score": 0.05,  # Muy bajo = NO moderna
  "primary_sensors": ["landsat_thermal", "sentinel2", "sar"]
}
```

---

## 2. SITIO DE REFERENCIA: VEGETACIÓN

### Angkor Wat Temple Complex (Camboya)

**Coordenadas**: 13.4125°N, 103.8670°E

#### Ambiente
- **Tipo**: Selva tropical
- **Características**: Vegetación densa, alta humedad, visibilidad baja
- **Preservación**: Regular (vegetación invasiva)

#### Instrumental Especializado
**Sensores Primarios**:
- LiDAR aerotransportado - Penetra dosel vegetal
- Sentinel-2 (10m) - NDVI, firmas espectrales
- SAR Sentinel-1 (10m) - Penetra vegetación

**Por qué funciona**:
- LiDAR detecta estructuras bajo dosel
- SAR penetra vegetación húmeda
- Anomalías NDVI por vegetación diferencial
- Patrones geométricos ocultos visibles en LiDAR

#### Datos Arqueológicos
- **Período**: Imperio Khmer (siglo XII CE)
- **Tipo**: Complejo de templos
- **Área**: 162.6 km²
- **Características**: Templos, sistema hidráulico, red urbana
- **UNESCO**: World Heritage Site #668

#### Descubrimientos LiDAR
- Reveló ciudad extensa más allá de templos visibles
- Sistema de gestión de agua complejo
- Red de caminos antiguos
- Infraestructura urbana oculta

#### Condiciones de Detección Esperadas
```python
{
  "environment_detected": "forest",
  "confidence": 0.85,
  "archaeological_probability": 0.70-0.85,
  "site_recognized": True,
  "modern_exclusion_score": 0.10,
  "primary_sensors": ["lidar", "sentinel2", "sar"]
}
```

---

## 3. SITIO DE REFERENCIA: HIELO

### Ötzi the Iceman Discovery Site (Alpes)

**Coordenadas**: 46.7789°N, 10.8494°E

#### Ambiente
- **Tipo**: Glaciar alpino
- **Características**: Hielo permanente, alta altitud (3,210m), preservación excepcional
- **Preservación**: Excelente (congelación)

#### Instrumental Especializado
**Sensores Primarios**:
- ICESat-2 - Altimetría láser de hielo
- Sentinel-1 SAR - Polarimetría en hielo
- PALSAR L-band - Penetración profunda
- Landsat Thermal - Anomalías térmicas en hielo

**Por qué funciona**:
- Objetos orgánicos preservados en hielo
- Retroceso glaciar expone hallazgos
- Anomalías térmicas por materiales enterrados
- SAR polarimétrico detecta objetos en hielo

#### Datos Arqueológicos
- **Período**: Edad del Cobre (3350-3105 BCE)
- **Tipo**: Momia natural en glaciar
- **Área**: 0.001 km² (hallazgo puntual)
- **Características**: Cuerpo momificado, hacha de cobre, arco, flechas, ropa
- **Museo**: South Tyrol Museum of Archaeology

#### Significancia Científica
- Momia humana natural más antigua de Europa
- Vista sin precedentes de europeos del Calcolítico
- Descubierto por retroceso glaciar (cambio climático)
- Preservación perfecta de tejidos, ropa, equipo

#### Condiciones de Detección Esperadas
```python
{
  "environment_detected": "glacier",
  "confidence": 0.90,
  "archaeological_probability": 0.60-0.75,  # Más bajo (hallazgo pequeño)
  "site_recognized": True,
  "modern_exclusion_score": 0.02,
  "primary_sensors": ["icesat2", "sentinel1_sar", "palsar"]
}
```

**Nota**: La probabilidad arqueológica es más baja porque es un hallazgo puntual muy pequeño (cuerpo individual), no una estructura grande. Sin embargo, el sistema debe reconocerlo como sitio conocido.

---

## 4. SITIO DE REFERENCIA: AGUA

### Port Royal Submerged City (Jamaica)

**Coordenadas**: 17.9364°N, -76.8408°W

#### Ambiente
- **Tipo**: Mar poco profundo (12m)
- **Características**: Ciudad sumergida, sedimento anaeróbico, preservación excepcional
- **Preservación**: Excelente (enterramiento rápido)

#### Instrumental Especializado
**Sensores Primarios**:
- Multibeam Sonar - Batimetría de alta resolución
- Side-scan Sonar - Imágenes del fondo marino
- Magnetómetro - Detección de metales
- Sub-bottom Profiler - Penetración sedimentos

**Por qué funciona**:
- Sonar detecta estructuras sumergidas
- Magnetómetro detecta clavos, anclas, cañones
- Sub-bottom profiler ve bajo sedimento
- Preservación excepcional en sedimento anaeróbico

#### Datos Arqueológicos
- **Período**: Era Colonial (1518-1692 CE)
- **Tipo**: Ciudad sumergida
- **Área**: 0.13 km²
- **Características**: Edificios, calles, naufragios, artefactos
- **Evento**: Terremoto del 7 de junio de 1692

#### Significancia Científica
- Uno de los mejores sitios arqueológicos submarinos preservados
- "Cápsula del tiempo" de la vida colonial caribeña
- Ciudad entera sumergida en minutos
- Preservación excepcional por enterramiento rápido en sedimento

#### Condiciones de Detección Esperadas
```python
{
  "environment_detected": "shallow_sea",
  "confidence": 0.85,
  "archaeological_probability": 0.75-0.85,
  "site_recognized": True,
  "modern_exclusion_score": 0.15,  # Algo más alto (era colonial reciente)
  "primary_sensors": ["multibeam_sonar", "side_scan_sonar", "magnetometer"]
}
```

---

## SITIOS DE CONTROL (Negativos)

Además de los 4 sitios arqueológicos de referencia, el sistema usa **4 sitios de control** donde NO debe detectar arqueología:

### 1. Atacama Desert Natural Control
- **Coordenadas**: -24.0000°N, -69.0000°W
- **Ambiente**: Desierto natural
- **Esperado**: NO arqueología

### 2. Amazon Rainforest Natural Control
- **Coordenadas**: -3.4653°N, -62.2159°W
- **Ambiente**: Selva prístina
- **Esperado**: NO arqueología

### 3. Greenland Ice Sheet Natural Control
- **Coordenadas**: 72.5796°N, -38.4592°W
- **Ambiente**: Capa de hielo
- **Esperado**: NO arqueología

### 4. Pacific Ocean Natural Control
- **Coordenadas**: 0.0000°N, -140.0000°W
- **Ambiente**: Océano profundo
- **Esperado**: NO arqueología

**Propósito**: Verificar que el sistema NO genera falsos positivos en ambientes naturales sin intervención humana.

---

## PROTOCOLO DE CALIBRACIÓN

### Paso 1: Verificar Backend
```bash
python run_archeoscope.py
```

### Paso 2: Ejecutar Test de Calibración
```bash
python test_calibration_4_reference_sites.py
```

### Paso 3: Verificar Resultados

El test verifica para cada sitio:

1. ✅ **Clasificación de Ambiente Correcta**
   - ¿Detectó el ambiente correcto? (desierto, selva, hielo, agua)

2. ✅ **Instrumentos Apropiados**
   - ¿Recomendó los sensores correctos para ese ambiente?

3. ✅ **Detección Arqueológica**
   - Sitios de referencia: ¿Detectó arqueología? (debe = SÍ)
   - Sitios de control: ¿Detectó arqueología? (debe = NO)

4. ✅ **Reconocimiento de Sitio**
   - ¿Reconoció el sitio en la base de datos?

5. ✅ **Exclusión Moderna**
   - ¿Score de modernidad es bajo? (< 0.20)

### Criterios de Éxito

- **EXCELENTE**: 8/8 tests pasan (100%)
- **BUENO**: 6-7/8 tests pasan (75-87%)
- **REGULAR**: 4-5/8 tests pasan (50-62%)
- **POBRE**: <4/8 tests pasan (<50%)

---

## VENTAJAS DE ESTE ENFOQUE

### 1. Simplicidad
- Solo 4 sitios de referencia (no 50+)
- Fácil de mantener y actualizar
- Tests rápidos de ejecutar

### 2. Cobertura Completa
- Un sitio por cada ambiente crítico
- Cubre todos los tipos de instrumental
- Incluye controles negativos

### 3. Calibración Efectiva
- Verifica clasificación de ambientes
- Valida recomendaciones instrumentales
- Detecta falsos positivos/negativos

### 4. Científicamente Riguroso
- Sitios verificados por UNESCO y fuentes académicas
- Datos públicos disponibles
- Reproducible y transparente

---

## ACTUALIZACIÓN DE LA BASE DE DATOS

La base de datos simplificada está en:
```
data/archaeological_sites_database.json
```

Estructura:
```json
{
  "metadata": {
    "version": "2.0.0",
    "total_sites": 4,
    "environment_coverage": {
      "desert": "Giza Pyramids",
      "forest": "Angkor Wat",
      "ice": "Ötzi the Iceman",
      "water": "Port Royal"
    }
  },
  "reference_sites": {
    "giza_pyramids": {...},
    "angkor_wat": {...},
    "otzi_iceman": {...},
    "port_royal": {...}
  },
  "control_sites": {
    "atacama_desert_control": {...},
    "amazon_rainforest_control": {...},
    "greenland_ice_control": {...},
    "pacific_ocean_control": {...}
  }
}
```

---

## REFERENCIAS

### Giza Pyramids
- UNESCO: https://whc.unesco.org/en/list/86
- Digital Giza: http://giza.fas.harvard.edu/

### Angkor Wat
- UNESCO: https://whc.unesco.org/en/list/668
- Khmer Archaeology LiDAR Consortium

### Ötzi the Iceman
- Museum: https://www.iceman.it/en/
- Wikipedia: https://en.wikipedia.org/wiki/Ötzi

### Port Royal
- Texas A&M Nautical Archaeology: https://nautarch.tamu.edu/portroyal/
- Wikipedia: https://en.wikipedia.org/wiki/Port_Royal

---

**Última actualización**: 2026-01-24  
**Versión**: 2.0.0  
**Estado**: ✅ 4 SITIOS DE REFERENCIA DEFINIDOS
